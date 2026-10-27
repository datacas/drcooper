# AGENTS.md

Operating rules for any agent working in this repository.

## Language

- **Repository artifacts: English.** Code, identifiers, file names, comments, doc comments, commit messages, branch names, issues, pull requests, reviews, documentation, diagram labels. No exceptions.
- **Conversation with the maintainer: Spanish.** Always, regardless of the language of the code being discussed.
- The rule splits by destination, not by topic: you may explain a change in Spanish and still commit it in English.
- **Forward only, from 2026-10-27.** Nothing that already exists gets translated: the 121 issues, the milestones, the Project views and the canonical set stay in Spanish. Do not propose a backfill, a "coherence" pass or a translation PR.
- **Editing existing Spanish text:** keep Spanish for the fragment you touch and leave the surrounding text alone. A mixed artifact is worse than a Spanish one.

## Repository state

DrCooper is a specification and product plan, not an implementation. There is no code yet, and authorised execution starts at R0 (discovery).

Source of truth: `docs/plan/ISSUES.md` (52 parent issues) and `docs/plan/INCREMENTOS.md` (69 increments). GitHub issues mirror them; the documents win.

## Change flow

`main` is protected. Every change lands through a pull request:

1. Branch from `main` with a short descriptive name (`dc-007-rust-base`).
2. Commit with Conventional Commits, imperative, English.
3. Open a PR that states what changes, links the issue (`Closes #N`), shows executed evidence and lists what remains unverified.
4. Never push to `main`, force push, or delete a branch without explicit confirmation.

## Evidence

- Acceptance requires executed evidence: command or scenario, versions and environment, observed result, artifact.
- Reading code is not verification.
- Do not claim `production_ready` for anything that only passed stubs or doubles. The plan distinguishes `contract_tested`, `integration_verified` and `production_ready`.

## Files to leave alone

- `docs/plan/**` and `brief_identidad.md` — canonical, hash-protected, Spanish.
- `LICENSE` — MIT, attribution to the owner.

## Context

- [README.md](README.md) — product and repository map.
- [CONTRIBUTING.md](CONTRIBUTING.md) — PR flow, language policy, commit format.
- [docs/plan/DECISIONES_Y_COBERTURA.md](docs/plan/DECISIONES_Y_COBERTURA.md) — blocking decisions before implementation.
