# DC-001 technical discovery

Status: functional scope and exclusions validated; initial strategic priorities ratified for preparing DC-002. Development activities confirmed by the maintainer are distinguished from unverified provider attribution and measured frequencies. Corpus validation remains pending. This is discovery evidence, not a benchmark or a declaration that DrCooper is implemented. Issue #1 remains open; preparing DC-002 does not require weeks of usage observation first.

## Evidence boundary and provenance

Inspection date: 2026-10-27. A capture timestamp was `2026-10-27T22:27:17.368087+00:00`. Commands ran in the maintainer's WSL2 environment through RTK; larger results were processed locally through Context Mode before returning allowlisted summaries. No agent prompts were launched in Claude Code or OpenCode.

The local checkout was on `main` at `e3b6830a6f645d9ec160a1ddcb49936bb410aca5`, before the discovery pack. PR #126 was confirmed merged at `efaf13120869ca33f6470809d456bd5efc4e90c4`; its final head was `3de5c8813ac8eec6f3bee1afc335b0e583df0d4f`. Its three documents were read through GitHub's contents API at the merge commit, without pulling, switching branches or replacing files:

- [flows.md](https://github.com/datacas/drcooper/blob/efaf13120869ca33f6470809d456bd5efc4e90c4/docs/discovery/flows.md)
- [corpus.md](https://github.com/datacas/drcooper/blob/efaf13120869ca33f6470809d456bd5efc4e90c4/docs/discovery/corpus.md)
- [scope.md](https://github.com/datacas/drcooper/blob/efaf13120869ca33f6470809d456bd5efc4e90c4/docs/discovery/scope.md)

Acceptance was read both from [issue #1](https://github.com/datacas/drcooper/issues/1) and the canonical [ISSUES.md](../plan/ISSUES.md), DC-001. Scope was checked against the master specification §§1–3, 18 and 22, [ROADMAP.md](../plan/ROADMAP.md), [BENCHMARKS.md](../plan/BENCHMARKS.md), and the blocking-decision map. The canonical documents take precedence over GitHub issue text.

Inspection was read-only with respect to tools, configurations, repositories and services. The only requested repository outputs are this report and its [corpus selection manifest](corpus-selection.json). No installation, update, reconfiguration, repository checkout, dependency resolution, graph build, memory write, destructive operation or production-data test was performed. No existing service was stopped. Short-lived LSP processes created by the probes were shut down or terminated after bounded waits.

Private repositories are excluded from the official corpus and this report. No private repository directories, Git metadata, source, identifiers or derived fixtures were collected. Configuration parsing returned only global tool names, versions, integration types and selected non-secret switches; it did not publish raw configuration, credentials, environment values, project registries or histories. No stored AgentMemory records or session logs were queried. External requests contained only public repository identifiers or a public Click documentation question.

Repository-specific memory scope was not declared in the repository instructions inspected. No slug was invented and nothing was saved to AgentMemory. No memory-scope decision is needed to complete this report.

## Status vocabulary

| Status | Evidence required | Does not establish |
|---|---|---|
| Installed | Executable/package exists, preferably with version response | Client wiring or useful results |
| Configured | A declaration, hook, plugin or instruction references it | Effective loading, successful authentication or execution |
| Operational at probe boundary | An actual named command/protocol/tool request responded as recorded | Other operations, languages, clients or recovery |
| Observed failure | A bounded probe returned an error or failed to finish | Failure in every workspace or an experienced daily problem |
| Maintainer-reported | The maintainer explicitly describes an experienced incident or confirms a fact | Independent reproduction, quantified frequency or proven root cause |
| Maintainer-confirmed activity | The maintainer confirms an activity and, where explicit, its habitual use | Execution through any particular MCP/provider or measured frequency |
| Proposed usage or priority | The maintainer supplies a tentative classification | Confirmed daily use, definitive ranking or measured frequency |
| Unverified | Not exercised, unavailable to this session, or outside read-only scope | Success, failure, absence or zero cost |

`contract_tested`, `integration_verified` and `production_ready` describe product/provider maturity in the plan. A version response or an LSP initialization here awards none of those labels to a DrCooper integration.

## Observed environment and dependencies

| Component | Observation | Boundary |
|---|---|---|
| OS | Ubuntu 22.04.5 LTS, x86_64; kernel `6.18.33.2-microsoft-standard-WSL2` | WSL2 observed; Windows host edition/build not inspected |
| Resources visible to WSL | 16 logical CPUs; `MemTotal: 20479628 kB` | No load, performance, contention or Windows resource allocation measured |
| Node / npm / pnpm | 22.23.2 / 10.9.8 / 12.6.0 | Node installation managed under NVM; commands responded |
| Python / uv | System Python 3.10.12 / uv 0.12.5 | Tool virtual environments differ from system Python |
| PHP | PHP 7.4.33 CLI, Zend 3.4.0, OPcache 7.4.33 | No application executed; other PHP 7.x runtimes not verified |
| Git / Docker | Git 2.34.1 / Docker client 29.8.2, build `7fc2dff` | Docker daemon, containers, images and production workloads not inspected |
| Rust / Cargo | 1.99.1 (`58cf8f9c3`, 2026-10-13) / 1.99.1 (`5f94df478`, 2026-08-27) | Installed toolchains, not a DrCooper build |
| Missing from inspected PATH | Composer, Intelephense, Phpactor, standalone `playwright-cli`, `orca`, `code` | PATH absence does not exclude cached packages, other shells, Windows-side installs or IDE extensions |

The first Python processing probe failed before inspection because system Python 3.10 has no `tomllib`. The inventory was rerun with standard-library JSON parsing and an allowlisted TOML section reader. Nothing was installed. This is evidence of runtime diversity, not a failure of an agent integration.

## Agent installations and integration surfaces

Paths below use `$HOME` as a portable tool-installation reference, never a private workspace path.

| Agent | Installed version and mechanism | Configuration inspected | What actually responded |
|---|---|---|---|
| Codex | First `codex --version`: 0.164.0. Later CLI and global npm package: 0.165.0. npm launcher under the active NVM Node prefix | `$HOME/.codex/config.toml`, `$HOME/.codex/hooks.json`, installed Context Mode plugin metadata; shared skills under `$HOME/.agents/skills` | CLI version; this session's Context Mode processing/search, Serena instructions and Context7 resolve/query calls |
| Claude Code | 2.1.312; native executable reached through `$HOME/.local/bin/claude`, resolved under its versioned local installation | `$HOME/.claude/settings.json`, global MCP declarations in `$HOME/.claude.json`, plugin registry and LSP definitions, skill directory | CLI version only; no Claude session or client-native tool call launched |
| OpenCode | 2.2.0; executable under `$HOME/.opencode/bin` | `$HOME/.config/opencode/opencode.json` and `opencode.jsonc`, tool plugin metadata and skill directory | CLI version only; effective merged configuration and client-native tools unverified |

The Codex version change occurred between read-only probes. No updater or package manager mutation was run by this discovery. Its cause and the version of the already-running host process were not determined. Future baselines must record versions at both start and end and reject mixed-version comparisons.

### Core tool matrix

`C` = configured surface observed; `O` = operational only at the stated boundary; `U` = not verified. A configured MCP name is not proof that its tools were exposed to the active client.

| Tool | Installation/dependencies | Codex | Claude Code | OpenCode |
|---|---|---|---|---|
| RTK | 0.48.0 native CLI; shared shell PATH | O: commands and `proxy` pass-through; instructions require RTK | C: PreToolUse RTK binding; hook execution U | CLI available to shell; automatic routing U |
| Context Mode | 1.0.169 cached for Codex and Claude; Node >=22.5.0; MCP SDK, `better-sqlite3`, FTS-backed search | C+O: plugin, batch/execute/search returned results | C: enabled plugin and SessionStart binding; execution U | No explicit Context Mode entry in the two inspected global files; effective integration U |
| Serena | 2.0.0 via uv; isolated CPython 3.13.15, requires Python >=3.11,<3.15; MCP 2.2.0, pygls 2.1.1, lsprotocol 2025.0.0 | C+O: stdio `serena start-mcp-server`; instructions tool responded | C: stdio MCP; actual client session U | No Serena entry in inspected global files; client session U |
| AgentMemory | CLI/package 0.9.30; Node >=20; iii SDK/helpers 0.22.1, dotenv and Zod | C: `npx -y @agentmemory/mcp`, global hooks; no memory tools exposed in this session's discovered tool list; calls U | C: same MCP package name, lifecycle hooks; calls U | No explicit AgentMemory entry in inspected global files; capture/recall U |
| Graphify | CLI 0.9.55, distribution `graphifyy`, uv environment CPython 3.10.12; NetworkX, NumPy, Tree-sitter and language grammars | CLI version O; no Graphify MCP tool exposed in this session; graph queries U | Installed Graphify skill; CLI version O outside Claude; graph queries U | CLI available to shell; integration U |
| Context7 | Remote MCP; external service/auth/network dependency; server release not reported | C+O: resolve and documentation query | C: global HTTP MCP; calls U | C: remote MCP in JSON; effective loading/calls U |

AgentMemory's CLI package version does not identify the version of the bridge resolved by an unpinned `npx @agentmemory/mcp` invocation, or the running server. No `npx` invocation was used to download or start a bridge. Tool source commit IDs were not established; package versions must not be represented as Git commits.

Other global MCP declarations cover issue tracking, error telemetry and reverse engineering. Their names/command launchers were inventoried without secrets, but no remote calls were made: they are not comparators for F-01–F-14. Product scope does not expand to replace them.

### Hooks, skills and LSP wiring

- Codex has `hooks = true`. Hook state and global hooks reference AgentMemory lifecycle capture and local agent-state instrumentation. Context Mode's cached plugin declares pre/post-tool, compaction and session/prompt/stop surfaces. Declaration and retained state do not prove that each hook fired on this run, nor that duplicate global/plugin bindings are deduplicated.
- Claude enables Context Mode 1.0.169, official PHP/TypeScript LSP plugins 1.0.0, BasedPyright LSP plugin 1.1.0 and an additional PHP LSP plugin 0.1.0. Global hooks cover session start/end, prompts, pre/post-tool, tool failure, compaction, subagents, notifications, task completion and stop; RTK is referenced by PreToolUse. The two enabled PHP plugin entries warrant a controlled loading check, not an assumption of an observed conflict. Cached older plugin versions are not proof of active use.
- Claude's custom PHP LSP definition invokes `php-lsp`; its Python definition invokes `basedpyright-langserver --stdio`. The official plugin registry entries were observed, but their effective provider selection was not demonstrated.
- OpenCode JSON config disables built-in Intelephense and Pyright entries and declares `php-lsp` for PHP, `typescript-language-server --stdio` for JS/TS variants and `basedpyright-langserver --stdio` for Python. Some commands use absolute paths into the current NVM/uv installation. This is a reproducible configuration dependency on those installation locations, not evidence that PATH changes have caused a past failure.
- OpenCode JSON declares Context7; JSONC separately declares a reverse-engineering MCP. Neither declares the six baseline tools as a complete set. Merge/precedence behavior and environment overrides were not executed. Its local plugin package declares `@opencode-ai/plugin` 1.15.10; compatibility with CLI 2.2.0 is unverified. A local instrumentation plugin file exists; no hook behavior was exercised.
- Shared skill directories contain memory workflows, code review/cycle workflows, frontend/framework guidance, CLI/browser guidance and related utilities. Claude additionally has a Graphify skill; OpenCode's inspected skill directory contains 16 Code Cycle skills. A skill is a discoverable instruction surface, not a running MCP or proof that its backing CLI exists. In particular, Orca/browser skills do not prove that standalone `orca`/`playwright-cli` binaries are on PATH.
- Serena's global backend is LSP, with a 240-second tool timeout. The active DrCooper project reported **no active language servers**. This repository has no implementation source; no semantic result was inferred from a documentation-only project. Per-language/provider selection and real cross-file navigation remain unverified.

## Executed probe ledger

These are observations from this run. No expected result is silently substituted for an observed one.

| ID | Command or scenario | Observed result | Practical limit |
|---|---|---|---|
| E-01 | `rtk proxy <tool> --version`; executable resolution and tool package metadata | Versions and installation mechanisms listed above; version commands returned 0 except the separate language-server flag probe below | Does not launch client sessions or prove application semantics |
| E-02 | Context Mode `ctx_batch_execute`, `ctx_execute`, `ctx_search` | Processed public docs and sanitized inventory; search retrieved flow/scope sections | Some initial search queries returned no results; complete retention/recovery of raw outputs was not tested |
| E-03 | Serena `initial_instructions` in active DrCooper project | Tool responded; project active; active language servers empty | Transport/tool availability only; no definition/reference/rename operation |
| E-04 | Context7 `resolve-library-id` for Click 8.1.7; `query-docs` for `/pallets/click/8.3.0` | Resolver advertised 8.4.2 and 8.3.0; query returned public source links for 8.3.0 | Connectivity demonstrated; version 8.1.7 was not available in the advertised version list and was not validated through Context7 |
| E-05 | Unauthenticated GET `http://localhost:3111/agentmemory/health` | HTTP 401 | Server endpoint reachable and protected; health, server version, read/write operations and project scoping U. `/health` returned 404; it is not evidence of server failure |
| E-06 | `rtk proxy php-lsp --version`; direct stdio JSON-RPC initialization | PHP LSP 0.26.0; initialize advertised definitions, references, implementations, symbols and prepared rename | Capability advertisement only. Process did not exit within the bounded post-shutdown wait and was terminated; graceful shutdown not verified |
| E-07 | `rtk proxy typescript-language-server --stdio`, initialize without a workspace | JSON-RPC error `-32603`: no valid TypeScript installation found | Observed failure with TLS 6.0.2 and installed TypeScript 7.0.2; does not prove failure in a project with a compatible local TypeScript dependency |
| E-08 | Same TLS initialize with `initializationOptions.tsserver.path` pointing to the global installation's `lib/tsserver.js` | Same initialization error; owned process terminated after bounded wait | No file/configuration changed. Checked target file was absent |
| E-09 | Check known files in installed TypeScript package | Package 7.0.2 declares `tsc`; `lib/tsserver.js`, `lib/tsserverlibrary.js`, `lib/typescript.js` absent | An installed compiler is not sufficient evidence of a usable tsserver dependency; no replacement installed |
| E-10 | Direct `basedpyright-langserver --stdio` initialize/shutdown/exit | ServerInfo `basedpyright` 1.40.2; semantic capabilities advertised; exit 0 | No documents opened or diagnostics requested. `--version` on the language-server entry point separately failed with missing connection-stream error; compiler CLI version probe succeeded |
| E-11 | RTK proxy of synthetic Python stdout/stderr markers and `sys.exit(7)` | Exit 7, exact stdout marker and exact stderr marker preserved | Demonstrates raw proxy forwarding only, not every RTK filter's fidelity, compaction ratio or raw-log retention |
| E-12 | GitHub commit/content/tree APIs for the three public corpus repositories | Public visibility, exact commits, manifests, license files and language files retrieved | Remote metadata/source inspection only; no checkout, dependency installation, project tests or benchmark |
| E-13 | SHA-256 comparison for the 10 entries in `DOCUMENTOS_CANONICOS.json`; tracked protected-file diff | 10/10 match; no protected-file diff | Baseline integrity verified; protected content not modified |

LSP probes ran from `/tmp`, opened no project files and passed `processId: null`, `rootUri: null`, `workspaceFolders: null`, `capabilities: {}` in `initialize`. PHP used no extra argument; TypeScript and BasedPyright used `--stdio`. Requests were framed with `Content-Length`. An 8-second response bound, shutdown request, exit notification and bounded process wait were used. The explicit TypeScript path in E-08 was a request parameter only, not persisted configuration. No production process was signalled.

The synthetic RTK probe was equivalent to:

```text
rtk proxy python3 -c "import sys; print('DC001_SYNTHETIC_STDOUT'); print('DC001_SYNTHETIC_STDERR', file=sys.stderr); sys.exit(7)"
```

These probes are not the canonical Bench runner. They provide no latency distribution, token saving, semantic accuracy, maintenance estimate or replacement verdict. Exit timeouts cannot be interpreted as lifecycle/rollback test results.

## Flow-by-flow technical contrast

This table supplements the five required fields already present in `flows.md`. Proposed agent assignments are client coverage targets, not a claim of everyday use. `Configured` below refers only to declarations observed in this inspection.

| Flow | Input → expected result | Current tool / agent evidence | Failure to avoid | Demonstration and remaining boundary |
|---|---|---|---|---|
| F-01 | Symbol/location → definitions, implementations, references with provider/version | Serena configured in Codex/Claude; native LSP declarations in Claude/OpenCode | Partial/empty result claimed complete | E-03, E-06–10 establish surfaces and one dependency failure; cross-file semantic accuracy on all three clients U |
| F-02 | Symbol + replacement → reference-aware bounded edit | Serena editing tools exposed to Codex; Claude MCP configured; OpenCode semantic edit path U | Wrong symbol/overload or broken references | No edit performed under read-only scope; use disposable public/synthetic corpus later |
| F-03 | Command → compact output preserving exit/errors and recoverable raw evidence | RTK command available to all shells; Codex instruction routing, Claude hook configured | Hidden failure counted as saving | E-11 verifies proxy exit/stdout/stderr; native per-client hook routing, filters and raw recovery U |
| F-04 | Large output → local processing and focused context | Context Mode operational in Codex, configured in Claude; OpenCode wiring U | Raw context flood or irrecoverable source | E-02 demonstrates processing/retrieval; full raw recovery, capacity and other clients U |
| F-05 | Prior decision → source- and scope-correct recall | AgentMemory configured in Codex/Claude; OpenCode U | Cross-project leakage or lost decision | E-05 proves only protected endpoint reachability; no private recall or write, no cross-agent recovery proven |
| F-06 | Symbol/file → callers/callees/impact tied to commit | Graphify CLI responds; Claude skill exists; active graph/MCP U | Stale graph treated as current evidence | No graph generated/read; public corpus graph oracle proposed; version output is not graph validation |
| F-07 | Library/version/question → sourced matching documentation or abstention | Context7 operational in Codex; configured in Claude/OpenCode | Wrong-version documentation claimed applicable | E-04 exposes an explicit 8.1.7/8.3.0 coverage gap; exact public source is the fallback |
| F-08 | Fresh installation/config → stable connection in three clients | Multiple installers, configs and plugin surfaces observed | PATH/runtime/protocol drift or silent global policy edits | Inventory only; install/connect/uninstall tests intentionally not run |
| F-09 | Update → compatible restart and rollback | Separate Node, native, uv, Cargo and plugin versions observed | One update breaks multiple integrations | Codex version drift recorded; cause and rollback U. No update executed |
| F-10 | WSL restart/concurrent reconnect → service, operation and transport recovery | Three clients installed; active Codex session only | Stale locks/orphans or duplicated writes | No WSL/service/client restart; recovery U; owned LSP process behavior is not this flow |
| F-11 | Provider unavailable → explicit partial degradation; unrelated functions survive | E-07–09 show TLS failure while E-02/04/10/11 worked separately | Global failure or false completeness | Evidence of independent tools only; no DrCooper isolation contract or per-client capability renegotiation proven |
| F-12 | Two sessions/two worktrees → canonical project, isolated branches/scopes | Git available; no private worktree metadata inspected | Mixed/duplicated memory and index | Synthetic two-worktree topology specified; no worktree or concurrent session created |
| F-13 | Idle knowledge → reversible maintenance preserving literal constraints | AgentMemory hooks configured; no maintenance result inspected | Lost exception/date/decision | Synthetic conservation records proposed; no idle maintenance or memory write executed |
| F-14 | Same suite/two engines or versions → comparable explicit verdict | No DrCooper implementation/runner exists | Regression hidden by output reduction | Public pins and synthetic oracles proposed; no benchmark, comparator verdict or performance claim |

The maintainer's follow-up below supplies partial usage classifications and experienced incidents. It does not establish definitive per-flow frequencies or priorities. An observed configuration ambiguity or probe failure must not be rewritten as a past user incident. DC-002 owns quantitative baselines and the operational observation period.

## Maintainer usage and incident validation

Source M-01: the maintainer's first usage/incident follow-up. Source M-03: the subsequent explicit activity validation and ratification of initial strategic priorities. M-03 supersedes M-01's tentative usage classifications where they differ; the incident reports remain attributable to M-01. Both are human evidence, separate from E-01–13. Habitual activity confirmed by the maintainer is not an independently measured frequency or evidence that a specific provider performed it. Unknown flows remain `proposed` or `unverified`, never `observed` by inference from installation.

| Agent | Maintainer-confirmed activity | Proposed or unverified flows | Attribution and measurement boundary |
|---|---|---|---|
| Codex | Project development, code analysis/modification and commands; F-01 code navigation and F-03 command execution confirmed as habitual development activities | F-02/04/05/06/07 frequency and effective integration use remain `proposed`; F-08–12 are identified operational needs with frequency `unverified` | F-01/F-03 provider attribution remains `unverified`: habitual navigation does not prove Serena/LSP use, and commands do not prove RTK use. No quantified frequency supplied |
| Claude Code | Development, technical analysis, code review and commands; F-01 and F-03 confirmed as habitual development activities | Specific F-02–07 integration classifications remain `proposed`, apart from the confirmed F-03 activity; F-08–12 have incident/maintenance history but no validated per-flow frequency | No provider is inferred from activity: neither Serena/LSP nor RTK nor any other MCP is confirmed for a particular operation. No quantified frequency supplied |
| OpenCode | WSL2 development and model/provider configurations through OmniRoute; F-03 effective use of development commands/tools, not yet quantified | F-01/02/04/05/06/07 effective baseline-tool integrations remain `unverified`; F-08–12 remain scenarios to verify | Actual F-03 activity does not confirm RTK or any other specific integration. Prior shared-environment concurrency reports do not establish worktree/scoping correctness |

For all three agents, F-13/F-14 are DrCooper target/future capabilities, not confirmed current usage. The maintainer has not classified other unverified flows as never used. Provider-routing incidents do not establish MCP or agent-internal faults.

### Experienced incidents reported by the maintainer

| Agent/context | Reported incident | Evidence boundary and flow relevance |
|---|---|---|
| Codex | Excessive RAM/swap consumption with concurrent services; multiple Serena/LSP instances; blocked/degraded processes under memory and I/O pressure | Experienced resource/concurrency issues, relevant to F-03/04/10/11/12. No process trace, resource measurement, incident count or causal isolation collected in this discovery |
| Codex | Context Mode installation/initialization problems | Experienced lifecycle issue relevant to F-08/09; exact version, trigger and reproduction not supplied |
| Codex | Limits in saving AgentMemory records with project scope | Experienced scope issue relevant to F-05/12; not independently retested against the observed installed version. No memory write or private record inspection performed |
| Claude Code | High resource consumption with simultaneous sessions/LSP servers; slow or blocked commands under WSL memory/I/O pressure | Experienced resource/concurrency issues relevant to F-03/10/11/12; no independent reproduction or quantified baseline |
| Claude Code | Operational overhead maintaining multiple services/configurations | Experienced maintenance burden relevant to F-08/09/10; no hours/minutes or intervention counts established |
| OpenCode/provider-routing context | Model availability errors/retries through OmniRoute; provider credential/authentication-header configuration problems | Provider-path incidents relevant to F-11 and setup diagnosis. Do not attribute them automatically to MCP or OpenCode internals. No credential values, headers, endpoints or provider account details collected |

These reports substantiate that resource pressure, lifecycle work and scope handling are real concerns. They do not establish whether each productivity symptom originated in infrastructure, an agent, a tool or provider routing. Future synthetic reproductions must remain independently authored; these general failure classes do not authorize deriving fixtures from private projects or exporting private incident artifacts.

### Ratified initial strategic priorities

| Initial priority | Flows | Intended concern | Validation state |
|---|---|---|---|
| P0 | F-08/09/10/11 | Reliability, installation, updates, recovery and fault isolation | Ratified by M-03; first strategic group for DC-002 preparation |
| P0 | F-03/04 | Resources/context efficiency and complete result recovery | Ratified by M-03; not a usage-frequency classification |
| P0 | F-05/12 | Shared memory, cross-agent continuity and project isolation | Ratified by M-03; no correctness or improvement claim implied |
| P1 | F-01/02/06/07 | Navigation, editing, impact and documentation | Ratified by M-03; committed roadmap guarantees/dependencies remain intact |
| P1 | F-13/14 | Knowledge evolution and reproducible evaluation | Ratified by M-03; future capabilities, not confirmed current use |

This ordering is approved for preparing DC-002, designing scenarios and establishing the measurement protocol now. Weeks of observation are not a prerequisite for that work. Quantified frequencies, productivity impact and any measured improvement remain evidence to collect, not conditions for deciding which problems to address first. Do not require retrospective maintenance estimates as if they were measured evidence.

Strategic flow priorities do not override the roadmap's committed P0 guarantees or dependencies and are not evidence of superiority. Baseline results may support later priority adjustments; any scope change must be documented and approved. No scope change or threshold is inferred from this ratification.

## Official corpus selection

The official corpus consists of public upstream sources pinned below plus newly authored synthetic scenarios. No private repository is a candidate, even as a source of identifiers or fixture structure. Upstream source is not vendored by this report. Metadata comes from the pinned public revision; current repository license classification is not a substitute for the pinned license file.

| ID | Public repository / revision | Exact commit | Role and observed source coverage |
|---|---|---|---|
| PUB-PHP | [symfony/console v3.4.47](https://github.com/symfony/console/tree/a10b1da6fc93080c180bba7219b5ff5b7518fe81) | `a10b1da6fc93080c180bba7219b5ff5b7518fe81` | Legacy PHP, namespaced classes, autoloading, application/command relationships and tests. Inspected `Application.php`, `Command/Command.php`, `Tests/ApplicationTest.php` |
| PUB-TSJS | [reduxjs/redux v4.2.1](https://github.com/reduxjs/redux/tree/f4b3ab9ac5370c5520d08383c5fc88e1e1c64587) | `f4b3ab9ac5370c5520d08383c5fc88e1e1c64587` | JavaScript implementation, public TypeScript declarations and TS consumer tests. Confirmed `src/index.js`, `src/createStore.js`, `index.d.ts`, `test/typescript/store.ts`; do not assume this revision has TS implementation files |
| PUB-PY | [pallets/click 8.1.7](https://github.com/pallets/click/tree/874ca2bc1c30d93a4ac6e36a15ed685eafe89097) | `874ca2bc1c30d93a4ac6e36a15ed685eafe89097` | Python relative imports, re-exports, decorators and callbacks. Inspected `src/click/__init__.py`, `core.py`, `decorators.py`; tests and typing configuration exist |

Symfony Console is a component repository, not a representative all-in-one legacy application. Redux is valuable for JS/TS declaration boundaries, not evidence of general modern TS application coverage. Click does not establish all Python environment layouts. Synthetic cases explicitly fill those gaps. None of these repositories is designated a formal workspace monorepo by this discovery; multiple examples or packages alone do not establish workspace semantics.

### Dependencies, reproducibility and license constraints

| Source | Recorded dependency evidence | Reproduction limit and distribution constraints |
|---|---|---|
| Symfony Console | `composer.json`: PHP `^5.5.9\|>=7.0.8`, polyfill-mbstring `~1.0`, debug `~2.8\|~3.0\|~4.0`; dev dependencies recorded by the upstream manifest | No root `composer.lock` in the retrieved root listing; Composer absent on PATH. Freeze a separately generated dependency lock/environment under a future authorized execution, never claim ranges are exact resolutions. MIT `LICENSE` at this commit, blob `9e936ec0448b8549e5edf08e5ac5f01491a8bfc8`: preserve copyright and permission notice if redistributing source. PHP 7.4 runtime installed; other target 7.x runtimes unverified |
| Redux | `package.json`: TypeScript `^3.8.3`, Babel runtime `^7.9.2`; lockfile v2 `package-lock.json`, blob `99a3a0fb5066d7b1e2b0487d1716ae509e6c8954` | Locked examples: TypeScript 3.9.6, Jest 25.5.4, Babel runtime 7.13.10, ESLint 6.8.0, Rollup 2.44.0, each with integrity entry. Installed global TS 7.0.2 is not this locked toolchain. Root MIT `LICENSE.md`, blob `55bc8dfbe90cb54a2d6611e97007e5ee026486da`; preserve notice. Exclude logos/artwork and separately licensed logo assets from any copied sample |
| Click | `setup.cfg`: Python >=3.7; `setup.py`: conditional colorama on Windows, importlib-metadata below Python 3.8. Pinned `requirements/tests.txt`: pytest 7.4.0, iniconfig 2.0.0, packaging 23.1, pluggy 1.2.0 | Test requirements blob `6a6808865865c3f44824c2c3a3f4a8ae1aeb463d`; dev requirements include additional referenced files and are not a hash-locked full environment. `LICENSE.rst` BSD-3-Clause, blob `d12a849186982399c537c5b9a8fd77bf2edd5eab`: retain copyright/conditions/disclaimer and respect non-endorsement. Do not copy artwork |

Source bytes and upstream manifest/lock versions are reproducible at these commits. Fully resolved runtime/test environments for all three languages are **not** claimed reproducible yet: no dependencies were installed and no environment images or archive SHA-256 values were captured. Git blob IDs are object identifiers, not SHA-256 archive checksums. Record any future archive/image digest independently. Review dependency licenses separately before vendoring a resolved dependency tree; repository-level licenses do not cover arbitrary dependencies or assets.

Use each public commit's own manifest and license, verify `git rev-parse HEAD` against the pinned SHA in an authorized disposable checkout, retain the upstream lockfile bytes where present, and record the eventual runtime/provider/client versions with the run. Do not fetch a floating branch for a baseline. Do not run upstream lifecycle scripts in an existing workspace. These are future reproduction steps, not commands executed by this inspection.

### Proposed synthetic corpus, authored independently

These are scenario specifications, not existing files or executed tests. Fixture IDs and intended oracles are frozen in the selection manifest; source file hashes and fixture commits stay unavailable until materialization. All names/data must be newly invented, public-safe and independent of private projects. Use the repository's MIT license for newly authored fixture source, with no upstream-derived snippets.

| ID | Minimal topology and input | Expected oracle / failure boundary | Coverage |
|---|---|---|---|
| SYN-PHP | `packages/php-lib/src/Price.php`, `apps/php-cli/main.php`, independent `composer.json` roots; class declaration, imported call and dynamic callable/include case; PHP 7.0-compatible syntax | Exact static definition edge and caller path; dynamic edge must be marked unresolved/partial, never guaranteed safe rename. Run syntax validation separately on PHP 7.4 and the eventual minimum target runtime | PHP cross-file references, multi-package monorepo, coverage limits; F-01/02/06 |
| SYN-TSJS | `packages/shared/src/price.ts`, `packages/shared/src/index.ts`, `apps/ts-client/src/main.ts`, `apps/js-client/main.js`; workspace manifest, TS project references and path alias | Known cross-package definition/reference set; re-export edge; JS consumer edge; rename must update only expected files in a disposable copy. Pin actual tsserver runtime independently of `tsc` | TS implementation gap, JS/TS interop, aliases, monorepo; F-01/02/06 |
| SYN-PY | `packages/python-lib/src/dc_fixture/price.py`, `__init__.py`, `apps/python-cli/main.py`, separate environment descriptors; relative import and star-export variant | Deterministic direct import edge; explicit ambiguity for dynamic/star exports; changing one environment cannot satisfy another package's missing dependency | Python cross-file references and multi-environment monorepo; F-01/02/06 |
| SYN-WT | One synthetic Git repository containing the three package families; two linked worktrees on `case-a` and `case-b`, same relative symbol names and intentionally different values | One canonical repository identity, two branch/worktree scopes; cross-worktree queries cannot return the other branch's revision as current. Include a moved worktree path and concurrent read/write schedule later | Worktrees across all languages, canonical identity, concurrency; F-05/10/12 |
| FAIL-PHP | Point a disposable PHP provider profile at a guaranteed nonexistent synthetic executable; add independent stub exit and timeout modes | Report provider unavailable/crashed/timeout distinctly, advertise semantic coverage unavailable; unrelated command/docs capability still responds | Mandatory PHP provider failure; F-01/11 |
| FAIL-TSJS | Same synthetic missing/crashing/stalled provider modes; additionally a fixture dependency tree with no tsserver entry point | Explicit dependency/provider error; `tsc` presence cannot produce a complete semantic success. Preserve diagnostic/code/provenance | Mandatory TS/JS provider failure and observed dependency class; F-01/11 |
| FAIL-PY | Missing BasedPyright executable and synthetic wrong-environment import; stub exit/timeout modes | Separate launch failure from valid-server unresolved import; mark incomplete coverage; unaffected capabilities remain usable | Mandatory Python provider failure; F-01/11 |
| SYN-MEM | Artificial records: decision, literal exception, fixed date, superseding decision and two intentionally different scopes | Expected source IDs, exact conserved constraints, no unauthorized cross-scope recall; reversible archive/dedupe; no invented fact | F-05/12/13, semantic conservation and DC-052 handoff |
| SYN-OPS | Public-safe command markers, synthetic stderr + exit 7; local-only provider stubs returning malformed JSON-RPC, disconnect, 429/503 and delayed response | Exit/errors retained; no secret sentinel exported; no duplicate write on reconnect; retry/abstention reported; absence never scored as successful prediction | F-03/04/07/08–11/14 design coverage; no network service or credentials required |

Provider profiles, worktrees, concurrent sessions and local HTTP stubs must be created only inside disposable synthetic harness state in a later execution. Do not disable an installed MCP, kill a real LSP, modify a global agent configuration or restart the maintainer's WSL to inject these failures. Test lifecycle/recovery with consent in the operational protocol, not as an incidental discovery command.

### Corpus coverage and verification matrix

| Required dimension | PHP | TS/JS | Python | Evidence state |
|---|---|---|---|---|
| Public, pinned real source | PUB-PHP | PUB-TSJS | PUB-PY | Commit/manifests/license and selected file existence observed; not checked out |
| Cross-file references | Application/Command/tests + SYN-PHP | JS exports/declarations/TS consumers + SYN-TSJS | Re-exports/core/decorators + SYN-PY | Source inspection + explicit intended oracles; semantic results U |
| Formal monorepo | SYN-PHP within SYN-WT root | SYN-TSJS within SYN-WT root | SYN-PY within SYN-WT root | Synthetic topology specified; not materialized |
| Two worktrees | SYN-WT | SYN-WT | SYN-WT | Two-branch oracle specified; not executed |
| At least one provider failure per language | FAIL-PHP | FAIL-TSJS | FAIL-PY | All specified; only a direct real TLS dependency failure observed in this run |
| Sensitive/fault-injection cases | Synthetic only | Synthetic only | Synthetic only | No private derivation or real service fault injection |

## Scope and classification review

The objective remains a local intelligence engine serving Codex, Claude Code and OpenCode, initially in WSL2 Ubuntu, with optional independent external providers. The inventory supports the need to investigate integration diversity; it does not establish reduced maintenance, successful replacement, or that every declared component is used daily.

The draft's `Essential` / `Committed` / `Experiment` labels need to be read on two axes: release obligations versus optional provider activation. Two wording limitations are material:

1. The draft defines `Essential` as needed for the first replacement decision while assigning essentials to R2 and R4. The roadmap explicitly allows replacement **per validated flow**. R1 execution/memory equivalence must not be made dependent on completing all R2/R4 capabilities. Product-level essentials retain their scheduled release; they are not new dependencies for every flow.
2. The draft groups optional LLM/JEV adapters as `Experiment`. Their **activation and live-provider validation** are optional/conditional, but R4's architecture, deterministic fallback, adapter contracts and correct capability exposure are release obligations. The classification must not silently drop those obligations. JEV's real API/adoption validation remains conditional in DC-042; executing a double is not real integration.

These are clarifications against already-approved documents, not proposed roadmap changes. No canonical decision or classification was rewritten.

| Release | Approved obligation retained | Discovery implication / excluded overclaim |
|---|---|---|
| R1 | CLI/MCP, identity/scopes, SQLite/FTS, authorized execution, full output, memory, sessions, doctor/recovery; minimum Bench and CI gate; verified local artifact update/rollback; lifecycle contract across three clients | Inventory/probes are inputs to that matrix. Do not promise full Serena replacement. Service recovery, operation completion and transport reconnection need separate checks. Standalone/shared behavior remains an ADR-02 evidence decision |
| R4 | Persistent Discover → Verify → Commit/Propose; deterministic core without AI; optional independent LLM/JEV adapters; budgets for money, local resources and export volume; provenance, semantic conservation, governance and rollback | Current tools' independent failure does not prove DrCooper isolation. No external provider opt-in or maturity assumed. R2 structural reversible maintenance remains earlier and independent of graph/AI |
| R6 | Verifiable packages/channels, TUI, assisted scope/source-preserving migration and rollback; pilot validates replacement per flow against baseline without unjustified maintenance | WSL2 observed here is not proof of native Windows/macOS/Linux release support. Packaging, TUI and mascot cannot compensate for integrity/isolation/recovery gaps |

Unchanged exclusions: general agent framework/replacement/orchestration; compiler/full LSP reimplementation; own cloud/enterprise multitenancy/complex remote collaboration/Obsidian/mandatory embeddings; literal parity with every predecessor tool; autonomous code editing during knowledge maintenance; irreversible unvalidated memory migration. One application binary does not remove Git, LSP or external dependencies and cannot intercept every native agent command. LLM and JEV remain independent, optional and disabled by default. Visual identity does not block the core.

DC-002 owns measurements, pilot duration, thresholds and maintenance accounting; DC-003 owns authorization/export threat boundaries; DC-004/005 own runtime/transport/capability contracts; DC-006 owns provider/dependency choices; DC-052 owns comparable classification and conservation oracles. This report does not resolve their ADRs or expand DC-001 into implementation.

### Maintainer scope approval

Source M-02: the maintainer explicitly validates DC-001's functional scope and exclusions in the follow-up, under the following conditions. This approval resolves D-03; it does not approve the usage inventory or corpus by implication.

1. Unify and improve current capabilities while reducing maintenance, resource use and context without losing quality, security or essential functionality.
2. Replace capabilities per flow only after satisfactory reproducible benchmark evidence; retain underlying dependencies such as LSP servers when needed. Simultaneous replacement of every tool is not required.
3. R1 remains a functional local CLI/MCP core with project identity, shared memory, controlled execution, recovery, reversible installation and minimal Bench.
4. R4 remains the complete KEE with deterministic maintenance, semantic conservation, governance, resource limits, provenance and rollback.
5. R6 remains distribution, user experience, migrations and replacement validation through tests and real usage.
6. JEV and LLM remain independent, optional and disabled by default. Their absence cannot block DrCooper or deterministic maintenance; dependent features are not offered when their provider is unavailable.
7. No private repository, source fragment, configuration, identifying path or derived private-project content enters DrCooper's public repository, fixtures or CI. The official corpus is exclusively public authorized projects and synthetic fixtures. Any later private test requires separate explicit authorization, remains local and exports no private content.
8. DrCooper integrates with Codex, Claude Code and OpenCode through common contracts, preserves agent independence and does not become their replacement or a general-purpose orchestrator.
9. Token/resource savings never justify loss of essential information, incorrect results or greater operational risk.
10. Keep Essential, Committed and Experiment distinct. Later delivery alone does not make committed R3/R5/R6 capabilities experimental. Optional provider activation does not remove committed adapter/capability-contract obligations.

No product expansion or canonical-document change was requested. Visual identity remains non-blocking. Existing release gates and source-of-truth documents remain intact. Usage validation and corpus evidence have their own acceptance boundary and must be completed before issue closure.

## Hypotheses and decisions pending

| ID | Statement | Evidence state / owner |
|---|---|---|
| H-01 | Multiple packaging/runtime/configuration surfaces may increase maintenance | Mechanisms observed; maintenance overhead and resource/concurrency incidents reported in M-01. Frequency, intervention time and causal attribution remain unmeasured; DC-002 |
| H-02 | Duplicate PHP declarations or overlapping hooks may cause ambiguity or duplicated capture | Declarations observed, actual duplicate invocation/conflict not observed; isolated client-loading test later |
| H-03 | Absolute NVM paths and unpinned MCP bridge resolution may be sensitive to installation changes | Configuration dependency observed, historical breakage not established; DC-006/lifecycle protocol |
| H-04 | A compatible project-local tsserver may allow TLS 6.0.2 to work | Not tried; current global compiler lacks the checked server files. Provider/version policy remains DC-006 |
| D-01 | Which activities and priorities are confirmed, and which usage details remain unverified? | M-03 confirms habitual F-01/F-03 activities in Codex/Claude, effective F-03 activity in OpenCode and the initial strategic ranking. Provider attribution, other proposed integrations and measured frequencies remain unverified; no new priority approval is required to prepare DC-002 |
| D-02 | Which failure scenarios were personally experienced, if any? | Answered at incident-class level by M-01. Incidents are maintainer-reported, not independently reproduced; versions, counts, productivity impact and causal attribution remain unverified |
| D-03 | Does the maintainer validate the objective, R1/R4/R6 reading and unchanged exclusions, including the two classification clarifications? | Validated by M-02 under its ten conditions. Scope approval only; no approval of usage inventory/corpus or authority to close the issue |

No authorization for private repositories, external AI export, tool installation or provider repair is requested to complete DC-001's official corpus selection. Those would be separate tasks. Daily use can be marked unknown rather than invented; quantitative maintenance estimates can wait for DC-002.

### Finite discovery handoff to DC-002

Confirmed problem classes, explicit unknowns, ratified initial priorities and the public/synthetic scenario design are sufficient inputs to begin preparing DC-002. Do not repeatedly ask the maintainer to certify integrations they have marked unverified, or wait weeks before drafting the measurement protocol. Use targeted public/synthetic execution to establish provider attribution and technical behavior; collect frequency and operational impact under the protocol. Longitudinal replacement evidence belongs to the later evaluation, not to a prerequisite for starting it.

DC-001's corpus evidence remains a distinct deliverable: the three public revisions are pinned, but synthetic fixture bytes, worktree/monorepo execution and per-language provider-failure coverage are still unexecuted. No claim that the corpus has passed, no automatic issue closure and no inference of benchmark improvement follows from the handoff. This sequencing clarification changes no canonical issue dependency or release gate.

## DC-001 acceptance matrix

| Criterion / work requirement | Evidence produced | Assessment | Remaining work |
|---|---|---|---|
| Each flow has input, expected result, current tool, agent and failure to avoid | Original 14-row pack plus this observed 14-row contrast, E-01–11, M-01 and M-03 | Structure complete; habitual/effective activities and initial priorities confirmed at their stated boundary; incident classes supplied | Preserve `proposed`/`unverified` for unconfirmed integrations. Collect provider attribution and quantified usage under the evaluation protocol; not a weeks-long prerequisite for preparing DC-002 |
| Corpus covers PHP legacy, TS/JS, Python, worktrees, monorepo, cross-file references and at least one provider failure per language | Three exact public commits, license/dependency evidence, selection manifest, synthetic topology/failure oracles | Selection and design specified; source metadata verified; fixture/runtime coverage not yet executed | Materialize/freeze synthetic fixture bytes in an implementation step; run coverage in the authorized evaluation protocol. No passed corpus run claimed |
| Objective, R1/R4/R6 and exclusions reviewed; visual identity non-blocking | Source comparison, classification clarifications and explicit M-02 approval | Validated by maintainer under the ten recorded conditions; D-03 resolved | Preserve scope conditions and committed R3/R5/R6 classification. Canonical documents unchanged; this approval does not close other criteria |
| Inventory current tools and scenarios per agent | Agent/tool/LSP/hook/skill matrices, explicit probe boundaries and M-01/M-03 usage/incident tables | Installed/configured/probe-operational/unverified separated from maintainer-confirmed activity, reported incidents and proposed integrations | End-to-end provider attribution and measured frequencies remain evidence gaps; initial strategic priorities are ratified and may guide DC-002 preparation now |
| Read-only, privacy and canonical-file restrictions | Sanitized evidence; public/synthetic-only manifest; E-13; no external publication | Inspection restrictions respected; no private corpus selected | Review only the added report/manifest before any future commit/PR; never include raw user configuration or session output |

DC-001 must not be automatically closed or represented as fully accepted on the scope approval alone. Remaining usage validation and corpus evidence are independent; benchmark and integration gaps are not counted as successes. All metrics not measured remain unavailable, not zero.

## Artifact validation

Executed after writing both artifacts, using Python 3.10 standard-library checks inside Context Mode:

| Check | Observed result |
|---|---|
| JSON parsing and selected structural assertions | Pass: 3 public source records with 40-hex commit IDs, explicit licenses, 9 synthetic scenario definitions, no executed corpus runs and no benchmark metrics |
| Official source allowlist | Pass: only Symfony Console, Redux and Click as source repositories; report references additionally allow the public DrCooper repository |
| Flow IDs | Pass: all 14 distinct flow rows and all 14 IDs represented in the proposed scenario map; this checks design completeness, not executed flow coverage |
| Local Markdown links | Pass: every local file target in this report exists; pinned remote links were read through GitHub APIs earlier |
| Secret/path pattern checks | Pass: no absolute user-home paths, private-key header, GitHub token pattern, API-key literal pattern or credential-assignment pattern detected in either new artifact |
| Privacy provenance review | Both artifacts were authored from sanitized global tool facts, the public sources and independently designed synthetic scenarios. No private repository was enumerated or used as input; no raw configuration, history or stored memory copied. Pattern checks alone are not a proof that arbitrary text is public |
| Canonical SHA-256 verification | Pass: all 10 manifest entries match; no protected tracked-file diff |
| `rtk git diff --check` | Exit 0 for tracked changes; new artifacts are untracked, so their whitespace was separately checked after writing |

No runtime test suite is claimed for documentation or for the proposed corpus. The report and manifest remain uncommitted output files in the existing checkout; no branch, commit, push, PR, issue comment or issue closure was created. The pre-existing untracked `.serena/` directory was left alone. Before any later PR, repeat privacy review on the actual staged diff and base it on a branch from the current approved `main`; this inspection did not synchronize the stale local checkout.
