# Synthetic corpus (DC-001)

Independently authored, MIT-licensed fixtures. Nothing here derives from private code or upstream sources.
Specification: [technical-discovery.md](../../docs/discovery/technical-discovery.md#proposed-synthetic-corpus-authored-independently).
Frozen scenario IDs: [corpus-selection.json](../../docs/discovery/corpus-selection.json).

- `workspace/`: SYN-PHP, SYN-TSJS and SYN-PY topologies (one monorepo root).
- `stubs/`: local-only provider stubs for FAIL-* and SYN-OPS (exit, timeout, malformed JSON-RPC).
- `memory/`: SYN-MEM artificial records.
- `oracles.json`: expected edges and failure boundaries.
- `SHA256SUMS`: frozen fixture hashes. Verify with `sha256sum -c SHA256SUMS` from this directory.

SYN-WT (two worktrees) is built from `workspace/` inside a disposable Git repository by the harness; it is not committed here.
Nothing in this directory has been run against DrCooper. These are inputs and oracles, not results.
