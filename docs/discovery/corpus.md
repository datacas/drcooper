# DC-001 — Initial corpus

Status: **DRAFT, not validated by the maintainer.** No repository or sample has been chosen, copied or frozen. This document fixes the selection rules and the coverage matrix; the maintainer fills the candidate column.

Basis: `docs/plan/BENCHMARKS.md` (suites, frozen samples, privacy), spec §2.2 (languages, LSP servers), §17.

## Selection rules

- Three languages: legacy PHP (including 7.x), TypeScript/JavaScript, Python (§2.2).
- Frozen by commit hash. A sample never follows a branch.
- No sensitive data: no secrets, credentials, customer data or private content. Prefer public repositories with a licence that allows copying; a private repository needs explicit maintainer consent and redaction before it enters any run.
- Real samples come from authorised repositories only; synthetic fixtures cover what real code cannot show safely (provider failures, injected faults).
- Expected results (oracles) are written independently of Serena, LSP or any candidate (`BENCHMARKS.md`). Development cases are kept apart from a reserved set.
- Size: small enough to run cold and warm repeatedly on the maintainer's WSL2 machine.

## Coverage matrix

Acceptance requires the corpus to cover worktrees, monorepo, cross-file references, and at least one provider failure per language. Each cell names the scenario type; the candidate source is filled by the maintainer.

| Dimension | PHP (legacy) | TS/JS | Python | Candidate source |
|---|---|---|---|---|
| Cross-file references (definition, references, rename impact) | Includes dynamic constructs (variable calls, includes) | Includes re-exports and path aliases | Includes relative imports and star imports | TBD (maintainer) |
| Monorepo | One repository with several packages or apps | Workspace with shared packages | Several projects with separate environments | TBD (maintainer) |
| Worktrees | Two linked worktrees of one repository, different branches | Same | Same | One repository is enough for all three languages |
| Provider failure | PHP LSP missing, crashing or timing out | `typescript-language-server` missing or version mismatch | BasedPyright missing or misconfigured environment | Synthetic fault injection on the samples above |

Provider failure scenarios per language are mandatory. Expected behaviour in each: the failure is reported, unrelated capabilities keep working, nothing is presented as a complete answer (F-01, F-11 in `flows.md`).

## Additional scenario classes

Needed by other R0 issues, listed here so the corpus is not built twice:

- Semantic conservation: documents with labelled constraints, exceptions, dates and decisions (DC-052).
- Memory: a small labelled dataset of decisions with sources and scopes (`memory` suite).
- Large outputs: logs and test runs of known content, to check raw recovery (`execution`, `context` suites).

## Open questions for the maintainer

1. Which repositories (public or authorised) represent each language best? One legacy PHP candidate is the hardest to find without private code.
2. Is there a repository that is already a monorepo and used with worktrees, so one source covers several rows?
3. Which real provider failures happened per language? They replace synthetic faults where possible.
4. Where do frozen samples live (outside this repository, to avoid committing third-party code), and who owns their licence review?
