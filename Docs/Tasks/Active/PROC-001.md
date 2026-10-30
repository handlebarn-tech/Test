# PROC-001 — Blender headless pipeline + first procedural generator

**Role:** ART-PROC · **Priority:** P1 (pulled forward) · **Branch:** `task/PROC-001` worktree off `base/wave-2`

## Goal
A repeatable, headless Blender 5.2.3 pipeline (DEC-007) that turns parameter files into game-ready meshes, proven on two generators: a deli flower jar and a packaged-product base (box/pouch).

## Read
`Docs/ASSET_PRODUCTION_PLAN.md` §B, §5, §8 and the procedural sections; `Docs/TOOLCHAIN_EXECUTION.md` (Blender sections); `Docs/STUDIO_OS.md` §48 (repo layout); `Docs/REFERENCES_INDEX.md` for any jar/package evidence.

## Owns
- `Tools/Blender/` (wrapper `blender.ps1`, generator Python modules, parameter JSON)
- `Art/Exports/Procedural/` at repo root (FBX or glTF outputs + manifest). **Do not write into `UnityProject/`** (ART-001 and GAME-001 own it now; import is a later task).
- `Docs/Assets/Specs/PROC_PIPELINE.md`
- Do **not** edit `Tools/Studio/studio.ps1` (ART-001 is changing it); the Hub wires a `blender` command later.

## Deliverable
1. `Tools/Blender/blender.ps1 <generator> <params.json>` runs `blender -b -P` and exits non-zero on error.
2. Generators `deli_jar` and `package_base`, parameterized: dimensions, lid, label-region UVs, LOD0/LOD1.
3. Dimensions come from REFERENCES_INDEX evidence if present; otherwise conventional placeholders, each marked with a GAP id in the params file. Do not invent store facts.
4. Output in meters, +Y up for Unity, transforms applied, named UV maps, triangle counts in the manifest.
5. Determinism: two runs give identical exports, or explain any timestamp-only difference.

## Validation
- Both generators run headless from a clean shell.
- Manifest tri counts are within the budget you state in PROC_PIPELINE.md.
- Front/side renders to `Artifacts/Renders/` (gitignored), plus one committed contact sheet ≤1 MB under `Docs/Assets/Specs/`.

## Handoff
`Docs/Handoffs/PROC-001.md` (≤40 lines). Report to the Studio Hub.
