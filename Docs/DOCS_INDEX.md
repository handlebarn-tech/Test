# DISPENSARY GAME — DOCUMENT INDEX & CONTEXT ROUTER

This file exists to keep agents from loading unnecessary context.

| Need | Read |
|---|---|
| Project goal / milestone / core architecture | `MASTER_PLAN.md` |
| Port current Three.js/browser/budtender systems | `UNITY_MIGRATION_PLAN.md` |
| Find/build/import any art asset | `ASSET_PRODUCTION_PLAN.md` |
| Run agents/worktrees/reviews/handoffs | `STUDIO_OS.md` |
| Run Unity/Blender/tests/builds/screenshots | `TOOLCHAIN_EXECUTION.md` |
| Design/implement customers, shifts, transactions and progression | `GAMEPLAY_SIMULATION_SPEC.md` |
| Codex durable repo guidance | `AGENTS.md` |
| Claude Code durable repo guidance | `CLAUDE.md` |

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

`References/ProjectHistory/Review_Budtender_Tool_Comprehensive_Chat_Record.md`

The actual current source repository outranks the historical record for implemented behavior.

## No-source handoff

For this handoff, the original Three.js/browser source is unavailable.

Read `NO_SOURCE_RECONSTRUCTION_BASELINE.md` before migration work.

The historical project record is retained under:
`References/Review_Budtender_Tool_Comprehensive_Chat_Record.md`
