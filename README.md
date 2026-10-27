# DrCooper

**Your code's second brain.**

DrCooper is a local intelligence engine for coding agents — Codex, Claude Code and OpenCode — that unifies semantic navigation, execution and context, persistent memory, a code graph, documentation and knowledge evolution. LLM and JEV are optional and independent: the core works without them.

> **Status:** planning. This repository holds the specification and the product plan; there is no implementation yet. Authorised execution starts with R0 (discovery), not with code.

## Documentation

The canonical set is **DC-DOCSET-0.3.0**, dated 2026-10-26. It is published byte for byte, with its original SHA-256 hashes.

| Document | Contents |
|---|---|
| [Product plan](docs/plan/README.md) | Entry point, conventions and limits |
| [Master specification](drcooper_ESPECIFICACION_MAESTRA.md) | Product, architecture, contracts and criteria |
| [Roadmap](docs/plan/ROADMAP.md) | R0–R6 deliveries and exit gates |
| [Backlog](docs/plan/ISSUES.md) | 52 parent issues with verifiable acceptance |
| [Increments](docs/plan/INCREMENTOS.md) | 69 subtasks of the 23 L-sized issues |
| [Decisions and coverage](docs/plan/DECISIONES_Y_COBERTURA.md) | Pending ADRs and traceability |
| [DrCooper Bench](docs/plan/BENCHMARKS.md) | run / compare / report contract |
| [Audits](docs/plan/AUDITORIA_CAMBIOS.md) | First review and [second](docs/plan/AUDITORIA_SEGUNDA.md) |
| [Brand brief](brief_identidad.md) | Mascot and visual direction |
| [Manifest](docs/plan/DOCUMENTOS_CANONICOS.json) | Inventory, versions, sizes and hashes |

> The canonical set is currently written in Spanish. It is frozen at 0.3.0 and is not translated in place: doing so would break the manifest hashes. A translation is a new revision of the set, not an edit.

## Backlog on GitHub

The 52 parent issues and their 69 increments are published in the **Issues** tab, grouped by the `R0`–`R6` milestones and labelled by area, priority and size. Increments are sub-issues of their parent and each can have its own PR. Plan dependencies point at the real GitHub numbers.

The execution board is **[DrCooper — Plan](https://github.com/users/datacas/projects/3)**, with four views: `Plan` (parents), `Ejecución` (increments by state), `R0` (immediate work) and `P0` (blocking priority). The `Status` field and the close/PR workflows live in the Project; the source of truth remains this repository and the issues.

## How work happens here

`main` is protected: **every change lands through a pull request**. Direct pushes, force pushes and branch deletion are not allowed. A PR must describe the change, link the corresponding issue and provide the acceptance evidence defined in the plan.

Before implementing an issue, check its blocking decisions and dependencies in [DECISIONES_Y_COBERTURA.md](docs/plan/DECISIONES_Y_COBERTURA.md) and [ROADMAP.md](docs/plan/ROADMAP.md). L-sized issues are not handled as a single PR: they are split into increments.

## Language

Everything that lives in this repository is written in **English**: code, identifiers, comments, commit messages, branch names, issues, pull requests, documentation and file names.

Conversation with the maintainer is in **Spanish**. That is a rule about how the assistant talks to the owner, not about what gets committed.

See [CONTRIBUTING.md](CONTRIBUTING.md#language) for the full policy.

## Publication note

The documents keep the state and the claims of their 2026-10-26 revision (for example, "there is no remote repository" or "no issue is published"). The set stays intact so the manifest and its hashes remain verifiable. Publishing the repository and the backlog happened later and does not alter the canonical content.

## License

[MIT](LICENSE). You may use, modify and distribute the project; attribution is appreciated.
