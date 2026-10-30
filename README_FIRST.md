# READ THIS FIRST — DISPO GAME

> **Historical bootstrap (AUDIT-001 B4, DEC-064):** the start order and "First production task" below come from the original handoff and are done. Current start: workers read `CLAUDE.md` → `Docs/PROJECT_STATE.md` → their packet; the Hub reads `Docs/HUB_RESUME.md` first. Kept for context.

> **Authority (DEC-001/002/009; AUDIT-001 C1, DEC-064):** for recommendation logic the order is (1) the local TFS tool source, v7.11.4 build, at `C:/Users/handl/Downloads/tfs-budtender` (read-only, no PII); (2) `Docs/DECISIONS.md`; (3) the live site (identical to the local build, DEC-009); (4) the historical chat record. Text below that ranks the live site or the chat record first predates DEC-001 and is kept for context.

This folder is designed to be handed directly to Claude Code.

## Important

The original Three.js/browser project is **not included and is not expected to be accessible**.

Do not block on it.

The supplied project-history record is the behavioral reconstruction baseline.

## Start order

1. `AGENTS.md` or `CLAUDE.md`
2. `Docs/MASTER_PLAN.md`
3. `NO_SOURCE_RECONSTRUCTION_BASELINE.md`
4. `Docs/DOCS_INDEX.md`
5. `Docs/STUDIO_OS.md` for orchestration
6. Open `Docs/TOOLCHAIN_EXECUTION.md` for Unity/Blender/build/test automation
7. Open `Docs/GAMEPLAY_SIMULATION_SPEC.md` for customers, transactions, shifts and progression
8. Open `Docs/UNITY_MIGRATION_PLAN.md` only for legacy-system/data/recommendation reconstruction
9. Open `Docs/ASSET_PRODUCTION_PLAN.md` only for art/asset work

## References

- `References/Floor Plan.pdf`
- `References/CCTV Camera Wall.png`
- `References/Review_Budtender_Tool_Comprehensive_Chat_Record.md`

## Core rule

Do not preload every file into every agent.

The Hub routes specialists to the minimum relevant context.

## First production task

Create a documented reconstruction contract from the project-history record. In parallel, run STUDIO-DOCTOR from the Toolchain Execution Contract to discover Unity, Blender and the target machine. Then initialize the Unity project, measured graybox and vertical-slice simulation according to dependency order.


## Live behavioral reference

The budtender system has a public deployment:
https://tfs-phx-budtender.netlify.app/

It currently identifies as v7.11.4.

Read:
`References/LIVE_TFS_BUDTENDER_v7.11.4.md`

When network access is available, workers should inspect the live deployment for current UI/behavior before relying only on the older historical record.
