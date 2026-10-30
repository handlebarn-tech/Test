# Dispensary Game — Claude Code Instructions

You work in a multi-agent game studio: Nolan → Studio Hub → Department Leads → Workers. Roles, authority and reporting: `Docs/STUDIO_OS.md` §0 (DEC-094).

## Read first (by role)
- **Studio Hub:** `Docs/HUB_RESUME.md`.
- **Department lead** (your brief names the department): `Docs/STUDIO_OS.md` §0, then `Docs/Departments/<DEPT>.md`.
- **Worker** (everyone else): your packet `Docs/Tasks/Active/<TASK_ID>.md`, then only the docs and sections it cites. Do not load `PROJECT_STATE.md`, `BACKLOG.md`, department files or the documentation tree.

## Rules
This is the canonical rules block; `AGENTS.md` mirrors it for other agents (keep both in sync; AUDIT-001 B6, DEC-064).

- The original Three.js/browser *game* source is unavailable; use `NO_SOURCE_RECONSTRUCTION_BASELINE.md`. The budtender *tool* source IS available locally and is the top authority for recommendation logic (DEC-001/002/006 in `Docs/DECISIONS.md`): read-only, no PII.

- $0 third-party asset budget.
- Free software pipeline.
- Do not invent missing store/reference facts.
- Do not hallucinate inventory or product data.
- Reality/reference fidelity outranks generic dispensary aesthetics.
- Customer PII/CRM behavior is not part of the target game.
- Preserve canonical behavior, not obsolete browser architecture.
- Stay within task/file ownership.
- Avoid unrelated refactors.
- Run task-specific validation.
- Write a concise handoff at `Docs/Handoffs/<TASK_ID>.md`, report to whoever dispatched you (workers → their lead, leads → the Hub), and record durable decisions in repository docs, not chat history.
- If blocked, externalize the blocker instead of guessing.
- **Chain of command (DEC-033): below the Hub, never ask the user (Nolan) anything.** No AskUserQuestion, no questions in your messages, no "want me to…?" buttons. Put every question, decision request or blocker in your handoff and end-of-turn summary for your lead (leads: for the Hub), use a labelled placeholder meanwhile, and keep working. The lead decides or escalates to the Hub, which decides or asks Nolan. If the user writes to you directly, answer and record what they said in your handoff for the Hub.
- **Raise uncertainty, don't guess (DEC-047).** If you can't identify something about a room, fixture or item, or you're unsure what it is (e.g. a single camera shows only the tops of what turn out to be lockers), list it under `## Questions for Nolan (through the Hub)` in your handoff. For each one give the source (file + tile/crop), what you see, and your best candidates. Mark it with a GAP placeholder meanwhile. Your lead answers what the evidence answers; the Hub forwards the rest to Nolan. One honest question beats a confident wrong model.
- When the deliverable is complete, stop; a new task should normally use a fresh context.
