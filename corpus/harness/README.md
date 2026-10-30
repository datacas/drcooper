# Corpus harness (DC-001)

`run_corpus.py` executes the synthetic corpus with plain tools and real language servers. It checks that the corpus oracles are satisfiable and that failure modes are distinguishable. It does not run DrCooper, which does not exist yet, so a pass here is not a DrCooper result.

```bash
python3 -I corpus/harness/run_corpus.py corpus/harness/results/run-<date>.json
```

Everything runs in a disposable temp directory with an isolated `HOME` and no global Git identity; the repo checkout is only read. Every subprocess has a hard timeout and runs in its own process group, which is killed on timeout.

Result values: `pass` and `fail` are checked against a fixed oracle; `observed` records what a real tool did when the oracle is "whatever it does, explicitly".

Requirements: `git`, `php`, `node` (type stripping), `tsc`, `typescript-language-server`, `basedpyright` and `basedpyright-langserver`. The tsserver-backed checks need a `typescript/lib/tsserver.js` under `~/.nvm/versions/node/*/lib/node_modules`; without one they are recorded as `observed`, not `pass`.

Not covered: PHP semantic analysis (no PHP language server is installed), rename safety, and any DrCooper component.
