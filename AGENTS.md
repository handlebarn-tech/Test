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

## Context discipline
One workcell = one bounded deliverable.
If scope changes materially, finish a handoff and use a fresh session.

## Completion
A task is complete only when its acceptance criteria are evidenced.
