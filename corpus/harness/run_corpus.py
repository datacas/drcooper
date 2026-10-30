#!/usr/bin/env python3
"""Executes the DC-001 synthetic corpus with plain tools and real language servers.

This checks that the corpus oracles are satisfiable and that failure modes are
distinguishable. It does not run DrCooper, which does not exist yet.

Usage: python3 -I corpus/harness/run_corpus.py [output.json]
"""
import json
import os
import platform
import queue
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SYN = REPO / "corpus" / "synthetic"
WS = SYN / "workspace"
STUBS = SYN / "stubs"
RESULTS = []
BASE_ENV = {
    "PATH": os.environ.get("PATH", ""),
    "HOME": tempfile.mkdtemp(prefix="dc-home-"),
    "PYTHONDONTWRITEBYTECODE": "1",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_SYSTEM": "/dev/null",
    "GIT_AUTHOR_NAME": "dc-harness",
    "GIT_AUTHOR_EMAIL": "dc-harness@example.invalid",
    "GIT_COMMITTER_NAME": "dc-harness",
    "GIT_COMMITTER_EMAIL": "dc-harness@example.invalid",
}
TMP_ROOT = Path(tempfile.mkdtemp(prefix="dc-corpus-"))


def scrub(value):
    text = json.dumps(value) if not isinstance(value, str) else value
    for needle, label in ((str(TMP_ROOT), "<tmp>"), (BASE_ENV["HOME"], "<tmp-home>"), (str(REPO), "<repo>"), (str(Path.home()), "<home>")):
        text = text.replace(needle, label)
    return json.loads(text) if not isinstance(value, str) else text


def record(scenario, check, result, expected, observed, **extra):
    """result: pass | fail | observed (no fixed oracle; value recorded as found)."""
    RESULTS.append(scrub({"scenario": scenario, "check": check, "result": result,
                          "expected": expected, "observed": observed, **extra}))
    print("%-9s %-8s %s" % (scenario, result, check))


def kill_group(proc):
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    proc.wait()


def run(cmd, cwd=None, timeout=30, stdin=None, env=None):
    proc = subprocess.Popen(cmd, cwd=cwd, stdin=subprocess.PIPE if stdin is not None else subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                            env=env or BASE_ENV, start_new_session=True)
    try:
        out, err = proc.communicate(stdin, timeout=timeout)
        return {"rc": proc.returncode, "out": out, "err": err, "timeout": False}
    except subprocess.TimeoutExpired:
        kill_group(proc)
        out, err = proc.communicate()
        return {"rc": None, "out": out, "err": err, "timeout": True}
    except FileNotFoundError as exc:
        return {"rc": None, "out": "", "err": str(exc), "timeout": False, "missing": True}


def classify(cmd, timeout=3, stdin="ping\n"):
    """Harness-level classifier proving the failure classes are distinguishable."""
    try:
        res = run(cmd, timeout=timeout, stdin=stdin)
    except FileNotFoundError:
        return "missing", {}
    if res.get("missing"):
        return "missing", res
    if res["timeout"]:
        return "timeout", res
    if res["rc"] not in (0, None):
        return "crashed", res
    out = res["out"]
    if out.startswith("Content-Length:"):
        head, _, body = out.partition("\r\n\r\n")
        try:
            json.loads(body)
        except ValueError:
            return "malformed", res
    return "ok", res


def tool_version(cmd):
    res = run(cmd, timeout=15)
    return (res["out"] or res["err"]).strip().splitlines()[0] if (res["out"] or res["err"]) else None


# ---------------------------------------------------------------- LSP client
class Lsp:
    def __init__(self, cmd, cwd):
        self.proc = subprocess.Popen(cmd, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, env=BASE_ENV, start_new_session=True)
        self.msgs = queue.Queue()
        self.stderr = bytearray()
        threading.Thread(target=self._read, daemon=True).start()
        threading.Thread(target=self._drain, daemon=True).start()

    def _drain(self):
        for chunk in iter(lambda: self.proc.stderr.read1(4096), b""):
            if len(self.stderr) < 4000:
                self.stderr += chunk

    def _read(self):
        buf = b""
        stream = self.proc.stdout
        while True:
            chunk = stream.read1(65536)
            if not chunk:
                self.msgs.put(None)
                return
            buf += chunk
            while True:
                head, sep, rest = buf.partition(b"\r\n\r\n")
                if not sep:
                    break
                length = int([h.split(b":")[1] for h in head.split(b"\r\n") if h.lower().startswith(b"content-length")][0])
                if len(rest) < length:
                    break
                body, buf = rest[:length], rest[length:]
                try:
                    self.msgs.put(json.loads(body))
                except ValueError:
                    self.msgs.put({"malformed": body.decode("utf-8", "replace")})

    def send(self, obj):
        data = json.dumps(obj).encode()
        try:
            self.proc.stdin.write(b"Content-Length: %d\r\n\r\n" % len(data) + data)
            self.proc.stdin.flush()
        except (BrokenPipeError, OSError):
            pass

    def request(self, rid, method, params, timeout):
        self.send({"jsonrpc": "2.0", "id": rid, "method": method, "params": params})
        end = time.time() + timeout
        while time.time() < end:
            try:
                msg = self.msgs.get(timeout=0.5)
            except queue.Empty:
                continue
            if msg is None:
                return {"disconnected": True}
            if self._answer_server_request(msg):
                continue
            if msg.get("id") == rid and "method" not in msg:
                return msg
        return {"timeout": True}

    def _answer_server_request(self, msg):
        """Servers ask for workspace configuration; answer with empty settings."""
        if "method" in msg and "id" in msg:
            items = msg.get("params", {}).get("items", []) if msg["method"] == "workspace/configuration" else None
            self.send({"jsonrpc": "2.0", "id": msg["id"], "result": [{} for _ in items] if items is not None else None})
            return True
        return False

    def settle(self, seconds, until="textDocument/publishDiagnostics"):
        """Pump messages so the server can finish loading its configuration."""
        end = time.time() + seconds
        while time.time() < end:
            try:
                msg = self.msgs.get(timeout=0.5)
            except queue.Empty:
                continue
            if msg is None:
                return
            self._answer_server_request(msg)
            if msg.get("method") == until:
                return

    def notify(self, method, params):
        self.send({"jsonrpc": "2.0", "method": method, "params": params})

    def close(self):
        kill_group(self.proc)

    def err(self):
        return bytes(self.stderr).decode("utf-8", "replace")[:600]


def lsp_definition(cmd, root, rel_file, lang_id, line, char, init_options=None, timeout=25):
    """initialize -> didOpen -> definition. Returns what was actually observed."""
    srv = Lsp(cmd, root)
    try:
        init = srv.request(1, "initialize", {"processId": None, "rootUri": Path(root).as_uri(),
                                              "workspaceFolders": [{"uri": Path(root).as_uri(), "name": "root"}],
                                              "capabilities": {"workspace": {"configuration": True, "workspaceFolders": True}},
                                              "initializationOptions": init_options or {}}, timeout)
        if "result" not in init:
            return {"stage": "initialize", "response": init, "stderr": srv.err()}
        srv.notify("initialized", {})
        path = Path(root) / rel_file
        srv.notify("textDocument/didOpen", {"textDocument": {"uri": path.as_uri(), "languageId": lang_id,
                                                              "version": 1, "text": path.read_text()}})
        srv.settle(8)
        resp = srv.request(2, "textDocument/definition", {"textDocument": {"uri": path.as_uri()},
                                                         "position": {"line": line, "character": char}}, timeout)
        return {"stage": "definition", "response": resp, "stderr": srv.err()}
    finally:
        srv.close()


# --------------------------------------------------------------------- checks
def copy_workspace(dst):
    shutil.copytree(WS, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "dist", "*.tsbuildinfo"))


def git(args, cwd):
    return run(["git"] + args, cwd=cwd)


def syn_wt():
    base = TMP_ROOT / "wt"
    repo = base / "repo"
    copy_workspace(repo)
    git(["init", "-q", "-b", "main"], repo)
    git(["add", "-A"], repo)
    git(["commit", "-q", "-m", "base"], repo)
    edits = {
        "packages/shared/src/price.ts": ('${price.currency}`', '${price.currency} [@@]`'),
        "packages/php-lib/src/Price.php": ("sprintf('%.2f %s', $this->amount, $this->currency)", "sprintf('%.2f %s', $this->amount, $this->currency) . ' [@@]'"),
        "packages/python-lib/src/dc_fixture/price.py": ('"{:.2f} {}".format(amount, currency)', '"{:.2f} {}".format(amount, currency) + " [@@]"'),
    }
    for tag in ("a", "b"):
        git(["checkout", "-q", "-b", "case-" + tag], repo)
        for rel, (old, new) in edits.items():
            p = repo / rel
            text = p.read_text()
            assert old in text, rel
            p.write_text(text.replace(old, new.replace('@@', tag)))
        git(["commit", "-q", "-am", "case " + tag], repo)
        git(["checkout", "-q", "main"], repo)
    wa, wb = base / "wt-a", base / "wt-b"
    git(["worktree", "add", "-q", str(wa), "case-a"], repo)
    git(["worktree", "add", "-q", str(wb), "case-b"], repo)

    def common(p):
        return git(["rev-parse", "--path-format=absolute", "--git-common-dir"], p)["out"].strip()

    ids = {n: common(p) for n, p in (("repo", repo), ("wt-a", wa), ("wt-b", wb))}
    record("SYN-WT", "one canonical repository identity across main checkout and both worktrees",
           "pass" if len(set(ids.values())) == 1 else "fail", "1 distinct git-common-dir", len(set(ids.values())))
    tops = {git(["rev-parse", "--show-toplevel"], p)["out"].strip() for p in (repo, wa, wb)}
    heads = [git(["rev-parse", "--abbrev-ref", "HEAD"], p)["out"].strip() for p in (wa, wb)]
    record("SYN-WT", "three distinct scopes, branches case-a and case-b",
           "pass" if len(tops) == 3 and heads == ["case-a", "case-b"] else "fail",
           {"scopes": 3, "branches": ["case-a", "case-b"]}, {"scopes": len(tops), "branches": heads})

    def outputs(root):
        env = dict(BASE_ENV, PYTHONPATH=str(root / "packages/python-lib/src"))
        return {
            "php": run(["php", "apps/php-cli/main.php"], cwd=root)["out"].splitlines()[:1],
            "ts_js": run(["node", "--experimental-strip-types", "--no-warnings", "apps/js-client/main.js"], cwd=root)["out"].splitlines()[:1],
            "py": run(["python3", "-I", "-c", "import sys;sys.path.insert(0,sys.argv[1]);import dc_fixture.price as p;print(p.format_price(3,'USD'))",
                       str(root / "packages/python-lib/src")], cwd=root, env=env)["out"].splitlines()[:1],
        }

    out_a, out_b = outputs(wa), outputs(wb)
    ok = all(("[a]" in v[0]) for v in out_a.values()) and all(("[b]" in v[0]) for v in out_b.values())
    record("SYN-WT", "same relative symbols, different values per worktree, in PHP, TS/JS and Python",
           "pass" if ok else "fail", "[a] in wt-a, [b] in wt-b for each language", {"wt-a": out_a, "wt-b": out_b})

    stale = run(["grep", "-rl", "\\[b\\]", "packages", "apps"], cwd=wa)["out"].strip()
    record("SYN-WT", "no case-b revision visible from the case-a worktree",
           "pass" if not stale else "fail", "no match", stale or "no match")

    moved = base / "wt-b-moved"
    git(["worktree", "move", str(wb), str(moved)], repo)
    listing = git(["worktree", "list", "--porcelain"], repo)["out"]
    same = common(moved) == ids["repo"] and "wt-b-moved" in listing and "[b]" in outputs(moved)["php"][0]
    record("SYN-WT", "moved worktree path keeps the canonical identity and its branch content",
           "pass" if same else "fail", "same git-common-dir, listed at new path, content [b]", bool(same))

    violations = []

    def worker(root, tag, other):
        for i in range(60):
            (root / "scratch.txt").write_text("%s-%d" % (tag, i))
            seen = (root / "scratch.txt").read_text()
            if not seen.startswith(tag):
                violations.append((tag, seen))
            if (other / "scratch.txt").exists() and (other / "scratch.txt").read_text().startswith(tag):
                violations.append((tag, "leak"))

    threads = [threading.Thread(target=worker, args=(wa, "a", moved)), threading.Thread(target=worker, args=(moved, "b", wa))]
    [t.start() for t in threads]
    [t.join() for t in threads]
    dirty = [git(["status", "--porcelain"], p)["out"].strip() for p in (wa, moved)]
    record("SYN-WT", "concurrent read/write schedule (2 x 60 iterations) leaks nothing across worktrees",
           "pass" if not violations and all(d == "?? scratch.txt" for d in dirty) else "fail",
           "0 violations; each worktree dirty only with its own scratch.txt", {"violations": len(violations), "status": dirty})


def syn_php():
    res = run(["php", "-l", "packages/php-lib/src/Price.php"], cwd=WS)
    res2 = run(["php", "-l", "apps/php-cli/main.php"], cwd=WS)
    run_out = run(["php", "apps/php-cli/main.php"], cwd=WS)
    record("SYN-PHP", "PHP syntax valid and CLI resolves the imported class at runtime",
           "pass" if res["rc"] == 0 and res2["rc"] == 0 and run_out["out"].splitlines()[:1] == ["12.50 EUR"] else "fail",
           "php -l rc 0 twice; first output line '12.50 EUR'",
           {"php": tool_version(["php", "--version"]), "lint_rc": [res["rc"], res2["rc"]], "out": run_out["out"].splitlines()[:1]})
    main = (WS / "apps/php-cli/main.php").read_text()
    record("SYN-PHP", "dynamic call site present and must stay unresolved (oracle input)",
           "pass" if "call_user_func([$price, $method])" in main else "fail", "dynamic callable in main.php", "present" if "call_user_func" in main else "absent")


def syn_tsjs():
    work = TMP_ROOT / "ts"
    copy_workspace(work)
    build = run(["tsc", "-b", "apps/ts-client"], cwd=work, timeout=90)
    record("SYN-TSJS", "tsc -b resolves path alias and project reference", "pass" if build["rc"] == 0 else "fail",
           "rc 0", {"tsc": tool_version(["tsc", "--version"]), "rc": build["rc"], "out": (build["out"] + build["err"])[:400]})
    js = run(["node", "--experimental-strip-types", "--no-warnings", "apps/js-client/main.js"], cwd=work)
    record("SYN-TSJS", "JS consumer imports the TS source and runs", "pass" if js["out"].strip() == "3.00 USD" else "fail",
           "3.00 USD", {"node": tool_version(["node", "--version"]), "out": js["out"].strip()})
    hits = sorted(run(["grep", "-rl", "formatPrice", "packages", "apps", "--include=*.ts", "--include=*.js", "--exclude-dir=dist"], cwd=work)["out"].split())
    expected = ["apps/js-client/main.js", "apps/ts-client/src/main.ts", "packages/shared/src/index.ts", "packages/shared/src/price.ts"]
    record("SYN-TSJS", "textual reference set equals the oracle file set (sanity check, not a semantic result)",
           "pass" if hits == expected else "fail", expected, hits)


def syn_py():
    work = TMP_ROOT / "py"
    copy_workspace(work)
    cmd = ["basedpyright", "--outputjson", "apps/python-cli"]
    bare = run(cmd, cwd=work, timeout=90)
    diag = json.loads(bare["out"])["generalDiagnostics"] if bare["out"].strip().startswith("{") else []
    missing = [d for d in diag if d.get("rule") == "reportMissingImports"]
    record("SYN-PY", "valid server, unresolved import: reportMissingImports without an environment",
           "pass" if len(missing) == 2 else "fail", "2 reportMissingImports (dc_fixture, dc_fixture.price)",
           {"basedpyright": tool_version(["basedpyright", "--version"]), "count": len(missing)})
    (work / "pyrightconfig.json").write_text(json.dumps({"extraPaths": ["packages/python-lib/src"]}))
    wired = run(cmd, cwd=work, timeout=90)
    diag2 = json.loads(wired["out"])["generalDiagnostics"] if wired["out"].strip().startswith("{") else []
    record("SYN-PY", "extraPaths for the library package resolves the imports",
           "pass" if not [d for d in diag2 if d.get("rule") == "reportMissingImports"] else "fail", "0 reportMissingImports",
           len([d for d in diag2 if d.get("rule") == "reportMissingImports"]))
    result = lsp_definition(["basedpyright-langserver", "--stdio"], str(work), "apps/python-cli/main.py", "python", 3, 6)
    locs = result.get("response", {}).get("result")
    record("SYN-PY", "star export shadowing: which file the server picks for format_price (ambiguity oracle input)",
           "observed", "ambiguous between price.py and extras.py; no guaranteed single answer",
           locs if locs is not None else result)
    declared = (WS / "apps/python-cli/pyproject.toml").read_text()
    record("SYN-PY", "separate environment descriptors; the CLI declares a dependency the library does not",
           "pass" if "dc-fixture-missing-dep" in declared and "dc-fixture-missing-dep" not in (WS / "packages/python-lib/pyproject.toml").read_text() else "fail",
           "dependency only in apps/python-cli", "as expected")


def fail_modes():
    nonexistent = str(TMP_ROOT / "does-not-exist" / "provider")
    modes = {"missing": [nonexistent], "crashed": ["sh", str(STUBS / "exit.sh")],
             "timeout": ["sh", str(STUBS / "timeout.sh")], "malformed": ["python3", "-I", str(STUBS / "malformed.py")]}
    seen = {}
    for name, cmd in modes.items():
        kind, res = classify(cmd)
        seen[name] = kind
        detail = {"rc": res.get("rc"), "stderr": (res.get("err") or "")[:80]} if res else {}
        record("SYN-OPS", "stub mode '%s' is classified distinctly" % name, "pass" if kind == name else "fail", name, kind, detail=detail)
    alive = run(["pgrep", "-f", str(STUBS / "timeout.sh")])["out"].strip()
    record("SYN-OPS", "timed-out stub process group is gone after the kill", "pass" if not alive else "fail", "no process", alive or "no process")
    for lang in ("PHP", "TSJS", "PY"):
        ok = len(set(seen.values())) == 4 and all(seen[k] == k for k in seen)
        record("FAIL-" + lang, "synthetic provider profile: missing, crash, timeout and malformed are four distinct statuses",
               "pass" if ok else "fail", ["missing", "crashed", "timeout", "malformed"], seen)


def real_providers():
    record("FAIL-PHP", "real PHP language server executables are absent from PATH (provider missing, observed)", "observed",
           "intelephense/phpactor/psalm not on PATH",
           {n: bool(shutil.which(n)) for n in ("intelephense", "phpactor", "psalm")})
    tsc_real = Path(shutil.which("tsc")).resolve()
    candidates = [tsc_real.parent.parent / "lib" / "tsserver.js", tsc_real.parent / "tsserver.js"]
    record("FAIL-TSJS", "the global compiler directory has no tsserver entry point (dependency class, observed)", "observed",
           "no tsserver.js beside the tsc resolved from PATH", {"tsc_version": tool_version(["tsc", "--version"]),
                                                              "tsserver_js_present": [c.exists() for c in candidates]})
    work = TMP_ROOT / "tsls"
    copy_workspace(work)
    ok_run = lsp_definition(["typescript-language-server", "--stdio"], str(work), "apps/ts-client/src/main.ts", "typescript", 2, 14)
    record("FAIL-TSJS", "real typescript-language-server: definition of formatPrice with its default tsserver",
           "observed", "definition resolves to packages/shared/src/price.ts or an explicit provider error",
           {"version": tool_version(["typescript-language-server", "--version"]), "stage": ok_run["stage"],
            "response": ok_run["response"], "stderr": ok_run["stderr"][:300]})
    bad = lsp_definition(["typescript-language-server", "--stdio"], str(work), "apps/ts-client/src/main.ts", "typescript", 2, 14,
                         init_options={"tsserver": {"path": str(TMP_ROOT / "no-typescript" / "tsserver.js")}}, timeout=25)
    resp = bad["response"]
    result_val = resp.get("result") if isinstance(resp, dict) else None
    has_error = isinstance(resp, dict) and ("error" in resp or resp.get("timeout") or resp.get("disconnected"))
    record("FAIL-TSJS", "tsserver entry point missing: no complete semantic success is reported",
           "pass" if (has_error or not result_val) else "fail", "explicit error, timeout, disconnect or empty result; never a definition",
           {"stage": bad["stage"], "response": resp, "stderr": bad["stderr"][:300]})
    servers = sorted(Path.home().glob(".nvm/versions/node/*/lib/node_modules/typescript/lib/tsserver.js"))
    if not servers:
        record("SYN-TSJS", "semantic definition through a working tsserver", "observed", "a working tsserver", "no tsserver.js found under the nvm node versions")
    else:
        pkg = json.loads((servers[0].parent.parent / "package.json").read_text())
        for rel, lang, line, char in (("apps/ts-client/src/main.ts", "typescript", 2, 14), ("apps/js-client/main.js", "javascript", 2, 14)):
            got = lsp_definition(["typescript-language-server", "--stdio"], str(work), rel, lang, line, char,
                                 init_options={"tsserver": {"path": str(servers[0])}})
            res = got["response"].get("result") if isinstance(got["response"], dict) else None
            uris = sorted({(x.get("uri") or x.get("targetUri", "")).replace(work.as_uri(), "<ws>") for x in (res or [])})
            record("SYN-TSJS", "cross-package definition of formatPrice from %s with tsserver %s" % (rel, pkg["version"]),
                   "pass" if uris == ["<ws>/packages/shared/src/price.ts"] else "fail",
                   ["<ws>/packages/shared/src/price.ts"], uris or got)
    missing = classify([str(TMP_ROOT / "no" / "basedpyright-langserver")])[0]
    record("FAIL-PY", "launch failure (missing executable) is separate from a valid server's unresolved import", "pass" if missing == "missing" else "fail",
           "missing", missing)


def syn_mem():
    data = json.loads((SYN / "memory/records.json").read_text())["records"]
    superseded = {r["supersedes"] for r in data if r["supersedes"]}
    current_a = sorted(r["id"] for r in data if r["scope"] == "scope-a" and r["id"] not in superseded)
    oracle = json.loads((SYN / "oracles.json").read_text())["SYN-MEM"]["expect"]
    record("SYN-MEM", "records yield the oracle's current set for scope-a and keep scopes separate",
           "pass" if current_a == oracle["current_scope_a"] and not any(r["scope"] == "scope-b" for r in data if r["id"] in current_a) else "fail",
           oracle["current_scope_a"], current_a)
    literal = oracle["literal_conserved"]
    record("SYN-MEM", "literal constraint present verbatim in the records", "pass" if any(r["text"] == literal for r in data) else "fail", literal, "found")


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    started = time.time()
    steps = (syn_php, syn_tsjs, syn_py, syn_wt, fail_modes, real_providers, syn_mem)
    try:
        for step in steps:
            step()
    finally:
        shutil.rmtree(TMP_ROOT, ignore_errors=True)
        shutil.rmtree(BASE_ENV["HOME"], ignore_errors=True)
    summary = {k: sum(1 for r in RESULTS if r["result"] == k) for k in ("pass", "fail", "observed")}
    report = {"schema_version": 1, "issue": "DC-001", "subject": "synthetic corpus only; DrCooper not executed",
              "base_commit": run(["git", "rev-parse", "HEAD"], cwd=REPO)["out"].strip(),
              "environment": {"os": platform.platform(), "python": platform.python_version()},
              "duration_s": round(time.time() - started, 1), "summary": summary, "checks": RESULTS}
    text = json.dumps(report, indent=2) + "\n"
    if out:
        out.write_text(text)
    print("summary", summary)
    sys.exit(1 if summary["fail"] else 0)


if __name__ == "__main__":
    main()
