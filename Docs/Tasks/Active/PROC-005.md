# PROC-005 — Integrate the approved ChatGPT toolkit + fix every audit finding

**Dept:** Assets · **Role:** PROC · **Priority:** P1 · **Owner:** Assets lead subagent (2026-10-30 resume), worktree off `main`; first merge `claude/clever-lamport-837e7f` (core slice 4ef04ae + wire-shelving WIP 87807ad; next steps in its `Docs/Handoffs/PROC-005.md`) · **Reviewer:** Unity A `local_0dd63bac-df1d-448d-9203-641ead6b6837` (Blender + Unity import checks)

## Goal
DEC-092: bring the adopted toolkit packages from `C:/Users/handl/Downloads/Dispo Game Imports/` (read-only; copy, never move) into `Tools/Blender/` (proclib helpers, run_generator changes, generators, params, materials loader, label generator, validation layer). Then work the checklist `Docs/Imports/IMP-003_PROC_FIX_CHECKLIST.md` item by item until every item is done or explicitly deferred with a reason.

## Rules
- **Quality bar DEC-084:** realistic LOD0 detail, 2K–4K PBR, LOD0–LOD3, UV2; LOD0 guides of props 5–20k, fixtures 20–80k, hero 30–150k tris. Never low-poly or generic-looking. "Unbranded" = no unapproved marks (approved: DEC-071 + DEC-081).
- **Real dimensions only:** from ROOM_FIXTURES, REF docs, DEC-039/042/043/079/088/090; unknowns are named params + GAP ids (e.g. GAP-PROC-13/14).
- Collision = manifest boxes; validation JSON on failure (DEC-086). Existing generators' output (jars, fill, packaged goods) must not change unless the checklist says so; diff the exports.
- Materials loader: CC0/MIT sources only (DEC-023/087), recorded in `ASSET_CACHE_MANIFEST.json`; downloads go to the shared cache, never into git.
- No people likeness, cameras or security hardware. Headless Blender via `Tools/Blender/blender.ps1`; never import the drops' `__pycache__`.
- Work in slices and commit per package/family so review can start early.

## Deliverables
Integrated code + params; exports to `Art/Exports/Procedural/` (FBX via LFS) with manifest + validation JSON; a contact sheet/turntable per new family; checklist updated with done/deferred per item; `Docs/Handoffs/PROC-005.md`.

## Validation
All existing PROC/ProcArt tests green (EditMode via `studio.ps1`, DEC-013); new validation passes; tri/texture figures per family vs DEC-084 guides.
