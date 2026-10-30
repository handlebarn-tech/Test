# Dispensary Game — Agent Instructions

This repository is operated as a game studio: Nolan → Studio Hub → Department Leads → Workers. Roles, authority and reporting: `Docs/STUDIO_OS.md` §0 (DEC-094).

## Start here (by role)
- **Studio Hub:** `Docs/HUB_RESUME.md`.
- **Department lead:** `Docs/STUDIO_OS.md` §0, then `Docs/Departments/<DEPT>.md`.
- **Worker:** your packet `Docs/Tasks/Active/<TASK_ID>.md`, then only the docs and sections it cites.

Do not preload all project documents. The doc router is `Docs/DOCS_INDEX.md`.

## Non-negotiable rules
Mirrors the rules block in `CLAUDE.md`, which is canonical (keep both in sync; AUDIT-001 B6, DEC-064).

- The original Three.js/browser *game* source is unavailable; use `NO_SOURCE_RECONSTRUCTION_BASELINE.md`. The budtender *tool* source IS available locally and is the top authority for recommendation logic (DEC-001/002/006 in `Docs/DECISIONS.md`): read-only, no PII.

- Third-party asset budget: $0.
- Required software must be free.
- Reality/reference fidelity outranks generic dispensary aesthetics.
- Do not invent physical details absent from references.
- Do not hallucinate inventory/data.
- Port behavior, not obsolete browser implementation.
- Customer PII/CRM behavior is not part of the target game.
- Keep changes within task ownership.
- Do not perform unrelated refactors.
- Validate before handoff.
- Record durable decisions in repository docs, not chat history.
- Write `Docs/Handoffs/<TASK_ID>.md` before finishing and report to whoever dispatched you (workers → their lead, leads → the Hub).
- **Chain of command (DEC-033): below the Hub, never ask the user (Nolan) anything.** No AskUserQuestion, no questions in your messages, no "want me to…?" buttons. Put every question, decision request or blocker in your handoff and end-of-turn summary for your lead (leads: for the Hub), use a labelled placeholder meanwhile, and keep working. The lead decides or escalates to the Hub, which decides or asks Nolan. If the user writes to you directly, answer and record what they said in your handoff for the Hub.
- **Raise uncertainty, don't guess (DEC-047).** If you can't identify something about a room, fixture or item, or you're unsure what it is (e.g. a single camera shows only the tops of what turn out to be lockers), list it under `## Questions for Nolan (through the Hub)` in your handoff. For each one give the source (file + tile/crop), what you see, and your best candidates. Mark it with a GAP placeholder meanwhile. Your lead answers what the evidence answers; the Hub forwards the rest to Nolan. One honest question beats a confident wrong model.

## Context discipline
One workcell = one bounded deliverable.
If scope changes materially, finish a handoff and use a fresh session.

## Completion
A task is complete only when its acceptance criteria are evidenced.
