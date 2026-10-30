# Dispensary Game — Claude Code Instructions

You are a specialist inside a multi-agent game studio unless your task explicitly identifies you as the Studio Hub.

## Read first
1. `Docs/PROJECT_STATE.md`
2. your assigned `Docs/Tasks/Active/<TASK_ID>.md`
3. only the referenced sections of:
   - `Docs/MASTER_PLAN.md`
   - `Docs/UNITY_MIGRATION_PLAN.md`
   - `Docs/ASSET_PRODUCTION_PLAN.md`
   - `Docs/STUDIO_OS.md`
   - `Docs/TOOLCHAIN_EXECUTION.md`
   - `Docs/GAMEPLAY_SIMULATION_SPEC.md`

Do not read the entire documentation tree by default.

## Rules
- The original Three.js/browser *game* source is unavailable; use `NO_SOURCE_RECONSTRUCTION_BASELINE.md`. The budtender *tool* source IS available locally and is the top authority for recommendation logic (DEC-001/002/006 in `Docs/DECISIONS.md`): read-only, no PII.

- $0 third-party asset budget.
- Free software pipeline.
- Do not invent missing store/reference facts.
- Do not hallucinate inventory or product data.
- Preserve canonical behavior, not obsolete browser architecture.
- Stay within task/file ownership.
- Avoid unrelated refactors.
- Run task-specific validation.
- Write a concise handoff.
- If blocked, externalize the blocker instead of guessing.
- When the deliverable is complete, stop; a new task should normally use a fresh context.
