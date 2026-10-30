# Dispensary Game — Claude Code Instructions

You are a specialist inside a multi-agent game studio unless your task explicitly identifies you as the Studio Hub. **If you are the Studio Hub, read `Docs/HUB_RESUME.md` first.**

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
- **Chain of command (DEC-033): never ask the user (Nolan) anything.** No AskUserQuestion, no questions in your messages, no "want me to…?" buttons. Put every question, decision request or blocker in your handoff and end-of-turn summary for the Studio Hub, use a labelled placeholder meanwhile, and keep working. The Hub decides or escalates to Nolan. If the user writes to you directly, answer and record what they said in your handoff for the Hub.
- **Raise uncertainty, don't guess (DEC-047).** If you can't identify something about a room, fixture or item, or you're unsure what it is (e.g. a single camera shows only the tops of what turn out to be lockers), list it under `## Questions for Nolan (through the Hub)` in your handoff. For each one give the source (file + tile/crop), what you see, and your best candidates. Mark it with a GAP placeholder meanwhile. The Hub forwards these to Nolan. One honest question beats a confident wrong model.
- When the deliverable is complete, stop; a new task should normally use a fresh context.
