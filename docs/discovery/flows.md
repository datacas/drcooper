# DC-001 — Real flows inventory

Status: **DRAFT, not validated by the maintainer.** Derived from `drcooper_ESPECIFICACION_MAESTRA.md` (§§1, 2.1, 2.2, 3.3, 7, 17) and `docs/plan/BENCHMARKS.md`. Nothing here was observed on the maintainer's machine.

How to read it: every row marked `inferred` is a hypothesis taken from the specification. The maintainer confirms, corrects or removes it; the corrections are the real output of this document.

## Current tools (inferred)

The specification speaks of "5–6 independent tools and MCP servers" (§2.1) without naming them. The comparators named in §17.1 give the most likely set:

| Tool | Role today | Source |
|---|---|---|
| Serena (with LSP) | Semantic navigation and symbol edits | §17.1, `BENCHMARKS.md` `semantic` |
| RTK | Command execution with filtered output | §1 item 2, §17.1 |
| Context Mode | Out-of-window processing and output indexing | §1 item 3, §17.1 |
| AgentMemory (Engram as inspiration) | Persistent memory across sessions | §1 item 4, §9 |
| Graphify | Code graph, callers/callees, impact | §1 item 5, §17.1 |
| Context7 | Version-aware library documentation | §1 item 6, §17.1 |

Open: which of these are actually installed, which agents each one is wired into, and whether any other tool (hooks, scripts, IDE plugins) belongs in the list.

## Agents

Codex, Claude Code and OpenCode (§2.2). The engine cannot intercept every native command of an agent (§3.3), so the flows below mark where a flow depends on agent-side hooks or instructions instead of the engine.

Open: per-agent daily scenarios. The table lists the agents where each flow must be exercised; the maintainer states which agent actually carries which flow day to day.

## Flows

Columns follow the acceptance criterion of DC-001: input, expected result, current tool, agent, failure to avoid.

| ID | Input | Expected result | Current tool | Agent | Failure to avoid |
|---|---|---|---|---|---|
| F-01 | Symbol name or location | Definition, implementations and references, with the provider and its version named | Serena / LSP | Codex, Claude Code, OpenCode | Empty or partial result presented as complete when the LSP is down or still indexing |
| F-02 | Symbol and replacement body | Edit applied to the symbol only, references checked first | Serena | Codex, Claude Code, OpenCode | Textual edit that breaks references or touches the wrong overload |
| F-03 | Shell command (tests, build, linter) | Compact output; exit status, failures and stderr intact; raw output recoverable | RTK | Claude Code (hook-based); Codex, OpenCode (instruction-based, `inferred`) | Hidden error counted as saving; filtered output that drops the failing line |
| F-04 | Large output (log, test run, diff) | Processed outside the context window; only the derived answer enters the conversation | Context Mode | Codex, Claude Code, OpenCode | Raw output flooding the context, or an index that cannot return the original |
| F-05 | Decision made in an earlier session or another agent | Recalled with source and scope | AgentMemory | Codex, Claude Code, OpenCode | Lost decision; memory from another project or scope leaking in |
| F-06 | Symbol or file about to change | Callers, callees and impact set, with the commit it was built for | Graphify | Codex, Claude Code | Stale graph treated as current evidence |
| F-07 | Library and question | Answer from the installed version's documentation, or abstention | Context7 | Codex, Claude Code, OpenCode | Documentation of the wrong version; answer without a source |
| F-08 | Fresh machine or fresh agent config | Three agents connected with stable configuration | Manual, per tool | Codex, Claude Code, OpenCode | Start-up broken by PATH, runtime or protocol drift; silent edits to global policy |
| F-09 | Update of the product, an LSP or an agent | Everything still starts; rollback available | Manual, per tool | Codex, Claude Code, OpenCode | One tool update breaking several MCP servers |
| F-10 | WSL restart or concurrent reconnect | Sessions recover without manual repair | Manual | Codex, Claude Code, OpenCode | Orphan processes, stale locks, memory or index left inconsistent |
| F-11 | One provider down (LSP, graph, network, LLM) | The rest keeps working; the degraded part is reported as such | Independent tools | Codex, Claude Code, OpenCode | One failure disabling unrelated capabilities |
| F-12 | Two sessions on two worktrees of one repository | Separate scopes, one canonical project identity | None consistent today (`inferred`) | Codex, Claude Code, OpenCode | Memory and index mixed or duplicated across worktrees |
| F-13 | Idle period with accumulated memory | Deduplicated, archived reversibly, decisions and constraints preserved literally | None today (`inferred`) | Engine-side, agent-agnostic | Consolidation that drops a constraint, exception or date |
| F-14 | Two versions or two tools on the same suite | Verdict `pass`, `regression`, `inconclusive` or `incomparable` | None today (`inferred`) | Engine-side, agent-agnostic | Regression hidden behind a token saving |

Flows F-01 to F-07 are the day-to-day capabilities; F-08 to F-12 are the operational pain of §2.1; F-13 and F-14 are the new capabilities that the specification adds (§§10, 17).

## Open questions for the maintainer

1. Which tools from the table are really in use, and which others are missing?
2. Which flows run on which agent every day, and which are rare?
3. Which failures from the last months were actually hit (not hypothetical)? These are the most valuable corpus scenarios.
4. How many hours per week go to maintenance today? This is the baseline for DC-002.
