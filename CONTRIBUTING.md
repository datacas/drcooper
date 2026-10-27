# Contributing

Thanks for your interest in DrCooper.

## Language

Everything committed to this repository is written in **English**:

- source code, identifiers, file and directory names;
- comments, doc comments and commit messages;
- branch names, issues, pull requests, reviews and commit discussions;
- documentation and diagrams.

Conversation with the maintainer is in **Spanish**. This applies to chat, not to repository content: an assistant may answer in Spanish and must still commit in English.

The rule applies from **2026-10-27 onward**. Nothing that already exists is translated: the canonical set in `docs/plan/`, the 121 issues, the milestones and the Project views stay in Spanish. Do not open a translation backfill.

When editing an existing Spanish artifact, keep Spanish for the fragment you touch and do not translate the surrounding text.

Anything you write in another language will be asked to be translated before merge.

## Before opening a PR

1. Find the parent issue or the increment in the **Issues** tab. `L`-sized issues are worked through increments, never as a single PR.
2. Check the blocking decisions and dependencies in [DECISIONES_Y_COBERTURA.md](docs/plan/DECISIONES_Y_COBERTURA.md) and [ROADMAP.md](docs/plan/ROADMAP.md).
3. If the issue is not ready yet, say so in the issue before writing code.

## Flow

- `main` is protected: **changes only land through a pull request**. No direct pushes, force pushes or branch deletion.
- Create a short, descriptive branch, for example `dc-007-rust-base`.
- A PR must include: what changes, which issue it closes or references (`Closes #N`), how it was tested and which limits remain.
- Acceptance is demonstrated with executed evidence: command or scenario, versions and environment, result and artifact. Code inspection does not replace a behaviour test.
- No capability is announced as available if it has only passed stubs or simulated tests; the plan distinguishes `contract_tested`, `integration_verified` and `production_ready`.

## Commits

Use [Conventional Commits](https://www.conventionalcommits.org/) in English, imperative mood, lower case:

```
feat(parser): resolve relative imports across worktrees
fix(sqlite): keep snapshots consistent on interrupted migrations
docs: publish the canonical document set
```

## Canonical documentation

The documents in `docs/plan/` form the **DC-DOCSET-0.3.0** set and are protected by hashes in [DOCUMENTOS_CANONICOS.json](docs/plan/DOCUMENTOS_CANONICOS.json). Do not edit them incidentally or regenerate the hashes to validate a copy: an intentional change requires a manifest review and a new version of the set.
