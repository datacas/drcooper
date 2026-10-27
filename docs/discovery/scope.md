# DC-001 — Product limits and delivery review

Status: **DRAFT, not validated by the maintainer.** Restates decisions already in `drcooper_ESPECIFICACION_MAESTRA.md` and `docs/plan/ROADMAP.md`; it proposes no new scope. The maintainer's review of this page is the closing step of DC-001.

## Objective

One installable local-first engine (Rust, CLI and MCP) for Codex, Claude Code and OpenCode that replaces the current set of independent tools with less configuration and fewer operational failures. The promise must be proved with reproducible benchmarks and a pilot, not asserted (§1, §22).

## Capabilities by commitment

| Class | Capability | Release | Why |
|---|---|---|---|
| Essential | CLI/MCP adapters, canonical identity, SQLite, safe execution, memory, recovery, minimal Bench | R1 | Without these nothing can replace the current tools or be measured |
| Essential | Zero-Maintenance Installation contract: install, connect three agents, uninstall, reinstall, update, fail, recover | R1 | The main pain of §2.1 |
| Essential | Managed LSP/AST, safe edits, documentation, structural memory consolidation | R2 | Core day-to-day flows F-01, F-02, F-07 |
| Essential | Deterministic KEE without any AI provider | R4 | Engine must work offline and without keys |
| Experiment | Code graph beyond essential relations | R3 | Utility must be shown before widening (`ROADMAP.md`) |
| Experiment | Optional LLM and JEV adapters, validated with doubles first | R4 | Always optional and independent; real integration only if available and authorised |
| Experiment | Learning governance, inbox, JEV as experimental classifier | R5 | Out of the first replacement decision |
| Experiment | TUI, remote update channels, assisted memory migration, multi-platform packages | R6 | Distribution maturity, after the pilot shows value |

R1, R4 and R6 are the deliveries the issue asks to review:

- **R1 — Core:** first executable product. Exit gate: install and reconnect verified, run/compare/report, CI regression gate.
- **R4 — Full KEE:** Discover → Verify → Commit/Propose with idle execution; complete without providers; three budgets, semantic conservation, lineage, rollback.
- **R6 — Distribution:** verifiable packages and channels, TUI, assisted migration; the pilot validates replacement per flow without unjustified maintenance.

## Exclusions

From §3.2 and §3.3; none is added here.

- Generalist agent framework, replacement of Codex/Claude/OpenCode, or task orchestrator.
- Reimplementation of compilers or full LSP servers.
- Own cloud, enterprise multitenancy, complex remote collaboration, Obsidian, mandatory local embeddings.
- Literal duplication of every tool of Serena, Engram, Graphify and RTK.
- Autonomous code editing during knowledge maintenance.
- Irreversible automatic migration of old memories without validation.
- Claiming that one binary removes Git, LSP servers or external APIs; claiming interception of every native agent command.
- Requiring JEV or an LLM to start or use the engine.

## Visual identity

`brief_identidad.md` and DC-045 (TUI) concern identity. They do not block R0 or the engine core: the specification already states that graphic deliverables are not functional capabilities of the engine (`docs/plan/DECISIONES_Y_COBERTURA.md`).

## For maintainer review

1. Are the essential/experiment classes right, or does something move up or down?
2. Is any exclusion missing, or any listed one too strict?
3. Is the R1/R4/R6 summary what you expect from each delivery?
