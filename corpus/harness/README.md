# Corpus harness (DC-001)

`run_corpus.py` executes the synthetic corpus with plain tools and real language servers. It checks that the corpus oracles are satisfiable and that failure modes are distinguishable. It does not run DrCooper, which does not exist yet, so a pass here is not a DrCooper result.

```bash
python3 -I corpus/harness/run_corpus.py corpus/harness/results/run-<date>.json
```

Everything runs in a disposable temp directory with an isolated `HOME` and no global Git identity; the repo checkout is only read. Every subprocess has a hard timeout and runs in its own process group, which is killed on timeout.

Result values: `pass` and `fail` are checked against a fixed oracle; `observed` records what a real tool did when the oracle is "whatever it does, explicitly".

Requirements: `git`, `php`, `node` (type stripping), `tsc`, `typescript-language-server`, `basedpyright`, `basedpyright-langserver` and `php-lsp`. The tsserver-backed checks need a `typescript/lib/tsserver.js` under `~/.nvm/versions/node/*/lib/node_modules`; without one they are recorded as `observed`, not `pass`.

Rename findings recorded by the harness: tsserver's default rename keeps the exported name through an alias (`formatMoney as formatPrice`) and leaves consumers untouched; renaming every consumer needs `providePrefixAndSuffixTextForRename=false` and the consumer files open, and without them project-reference consumers are missed. Python rename follows the star export and touches `__init__.py`. `php-lsp` resolves `Price`, finds its references and renames `Price::format` at the static call sites, but the dynamic `call_user_func` site is left pointing at the old name and PHP then warns at runtime.

Not covered: the alternative PHP servers (intelephense, phpactor and psalm are not installed; `php-lsp` is the configured one), a real client's retry policy (the HTTP stubs only check that failure classes are distinguishable and that an idempotency key prevents a duplicate write), and any DrCooper component.
