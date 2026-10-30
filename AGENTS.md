# Dispensary Game — Agent Instructions

This repository is operated as a Hub-and-Workcell game studio.

## Start here
Read:
1. `Docs/PROJECT_STATE.md`
2. your assigned task file under `Docs/Tasks/Active/`
3. only the Master/Migration/Asset/Studio-OS sections referenced by that task.

Do not preload all project documents.

## Canonical docs
- `Docs/MASTER_PLAN.md` — project direction
- `Docs/UNITY_MIGRATION_PLAN.md` — legacy/browser → Unity/C# port
- `Docs/ASSET_PRODUCTION_PLAN.md` — free/custom asset work
- `Docs/STUDIO_OS.md` — agent/worktree/review process
- `Docs/TOOLCHAIN_EXECUTION.md` — Unity/Blender/build/test automation
- `Docs/GAMEPLAY_SIMULATION_SPEC.md` — customer/shift/transaction game design

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
- Write `Docs/Handoffs/<TASK_ID>.md` before finishing.
- **Chain of command (DEC-033): never ask the user (Nolan) anything.** No AskUserQuestion, no questions in your messages, no "want me to…?" buttons. Put every question, decision request or blocker in your handoff and end-of-turn summary for the Studio Hub, use a labelled placeholder meanwhile, and keep working. The Hub decides or escalates to Nolan. If the user writes to you directly, answer and record what they said in your handoff for the Hub.
- **Raise uncertainty, don't guess (DEC-047).** If you can't identify something about a room, fixture or item, or you're unsure what it is (e.g. a single camera shows only the tops of what turn out to be lockers), list it under `## Questions for Nolan (through the Hub)` in your handoff. For each one give the source (file + tile/crop), what you see, and your best candidates. Mark it with a GAP placeholder meanwhile. The Hub forwards these to Nolan. One honest question beats a confident wrong model.

## Context discipline
One workcell = one bounded deliverable.
If scope changes materially, finish a handoff and use a fresh session.

## Completion
A task is complete only when its acceptance criteria are evidenced.
