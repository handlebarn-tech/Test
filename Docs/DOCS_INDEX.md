# DISPENSARY GAME — DOCUMENT INDEX & CONTEXT ROUTER

This file exists to keep agents from loading unnecessary context.

| Need | Read |
|---|---|
| Project goal / milestone / core architecture | `MASTER_PLAN.md` |
| Port current Three.js/browser/budtender systems | `UNITY_MIGRATION_PLAN.md` |
| Find/build/import any art asset | `ASSET_PRODUCTION_PLAN.md` |
| Operating model: roles, sources of truth, read sets, packets, briefs, escalation, review, integration, Hub restart | `STUDIO_OS.md` **§0 only** (DEC-117); §56–57 templates, §63–65 gates; the rest is history |
| Run Unity/Blender/tests/builds/screenshots | `TOOLCHAIN_EXECUTION.md` |
| Design/implement customers, shifts, transactions and progression | `GAMEPLAY_SIMULATION_SPEC.md` |
| Codex durable repo guidance | `AGENTS.md` |
| Claude Code durable repo guidance | `CLAUDE.md` |
| **Studio Hub start** (Hub only) | `HUB_RESUME.md` |
| Live state: in flight, queue, priorities, Nolan items, builds | `PROJECT_STATE.md` (Hub only) |
| Task registry (IDs, titles, dependencies) | `BACKLOG.md`; a task's state = its packet folder `Tasks/Ready|Active|Done` |
| Ratified decisions (DEC-###), newest last | `DECISIONS.md`: read only the entries your packet cites, or the newest few |
| Unknown facts and placeholders (GAP-###) | `KNOWN_GAPS.md` |
| Decision-pressure gameplay (ratified DEC-057; wins over GSS on conflict) | `Design/SPEC_DECISION_PRESSURE.md` (only the § your packet cites); item status in `Design/DES-003_RECONCILIATION.md` |
| **Roadmap**: milestones to the finished game, what each contains (IDs), dependencies, critical path (no task state) | `Design/ROADMAP_POST_SLICE.md` (Hub-owned, DEC-119) |
| Nolan's V2 design pack (add-on; DP wins on conflict, DEC-063/066) | `Design/DESIGN_V2/` (start at its `README_FIRST.md`; exploit tests per `QA_TEST_PLAN.md`) |
| Compliance / packaged-goods / post-slice specs | `Design/SPEC_COMP002.md`, `Design/SPEC_GAME004.md` |
| Slice design, engine API, UX specs | `Specs/SLICE_DESIGN.md`, `Specs/ENGINE.md`, `Specs/UX_SLICE.md`, `Specs/UX_PS1.md`, `Specs/UX_COUNTER_INTEL.md` |
| Budtender-tool reconstruction contract, goldens, data schema | `Reconstruction/` |
| Store references (floor plan, CCTV, TI, back rooms) | `REFERENCES_INDEX.md` (by §) + `Reference/ROOM_FIXTURES.json` |
| Store-fact research (M365, AZ compliance) | `Research/` |
| Asset licenses, downloads, generator pipeline | `Assets/LICENSE_LEDGER.md`, `Assets/ASSET_CACHE_MANIFEST.json`, `Assets/Specs/` |
| Build health, performance budgets, machine | `BUILD_STATUS.md`, `PERF_BASELINE.md`, `MACHINE_PROFILE.md` |
| Worker handoffs and review verdicts | `Handoffs/<TASK_ID>.md`, `Reviews/` |
| Documentation audits | `Audits/` |

> **Router (AUDIT-001 C5, DEC-064):** this table is the one doc router; `MASTER_PLAN.md` §16 points here. Read a row's doc only when your packet needs it.

## Recommended repository destinations

When installed into the project:

```text
AGENTS.md
CLAUDE.md
Docs/
  MASTER_PLAN.md
  UNITY_MIGRATION_PLAN.md
  ASSET_PRODUCTION_PLAN.md
  STUDIO_OS.md
  PROJECT_STATE.md
  BACKLOG.md
  DECISIONS.md
  KNOWN_GAPS.md
  REFERENCES_INDEX.md
```

The attached historical record should be retained under a reference/history path, not injected into every session.

Example:

`References/ProjectHistory/Review_Budtender_Tool_Comprehensive_Chat_Record.md` *(not adopted: the record stayed at `References/Review_Budtender_Tool_Comprehensive_Chat_Record.md`, see below; AUDIT-001 C4)*

The actual current source repository outranks the historical record for implemented behavior.

## No-source handoff

For this handoff, the original Three.js/browser source is unavailable.

Read `NO_SOURCE_RECONSTRUCTION_BASELINE.md` before migration work.

The historical project record is retained under:
`References/Review_Budtender_Tool_Comprehensive_Chat_Record.md`
