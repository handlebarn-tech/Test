# PROC-002 — Jar fill / bud system (Blender generators)

**Role:** ART-PROC · **Priority:** P1 · **Branch:** `claude/task-proc-002-99e871` off `main` (e493fa1) · **Depends:** PROC-001 (done)

## Goal
Deterministic, headless Blender generator for deli-flower bud meshes and fill levels inside the 454 g (1 lb) deli jar (DEC-019), so the jar wall can show a jar's stock from full down to SOLD OUT (DEC-027).

## Read
`Docs/ASSET_PRODUCTION_PLAN.md` §8 (Flower workflow, Deli jar system: `FlowerVolume` / `BudInstances` / `ShakeBottom`, `fillLevel`, `budMeshSet`) and §22 (deli-flower pipeline: instancing, random rotation/scale, no huge bud meshes per jar); `Docs/Assets/Specs/PROC_PIPELINE.md`; `Docs/Handoffs/PROC-001.md`; GAME-002 handoff + `InventoryService` on `claude/task-game-002-7f57d6` (read only).

## Inputs
- Jar cavity: `Tools/Blender/params/deli_jar.json` (read, so fill stays in sync with the jar; all its sizes are GAP-PROC-01 placeholders).
- Fill contract: `InventoryService.Fill(batchId) = grams / startGramsPerBatch` (454), `IsSoldOut` at 0 g, `IsLow` below `lowStockFraction` 0.25.
- Visual families: the six bud looks from §8 Flower workflow (green dense, green airy, purple-heavy, orange-pistil-heavy, frosty/light, darker compact). There is no per-strain look data in the catalog; mapping batch → look is a [GDD] placeholder.

## Owns
- `Tools/Blender/generators/jar_fill.py`, `Tools/Blender/params/jar_fill.json`; minimal extensions to `Tools/Blender/run_generator.py` (variants, Unity copy, per-generator previews/sheet).
- `Art/Exports/Procedural/PROC_JarFill_*.fbx` + their manifest entries.
- `UnityProject/Assets/_Game/Art/Procedural/JarFill/` (FBX + .meta).
- `UnityProject/Assets/_Game/Code/Tests/EditMode/ProcArt/` (new EditMode test asmdef).
- `Docs/Assets/Specs/PROC_JarFill_contact_sheet.png`, the PROC-002 section of `PROC_PIPELINE.md`.
- Not: `Code/Simulation|Presentation`, graybox scenes, `Tools/Studio/studio.ps1`.

## Deliverable
1. `Tools/Blender/blender.ps1 jar_fill Tools/Blender/params/jar_fill.json` builds one FBX per visual family. Each holds every fill step (SOLD OUT 0 % plus a few steps up to full) × LOD0/LOD1/LOD2, named `PROC_JarFill_<Family>_F<pct>_LOD<n>`, placed in the jar cavity (same origin as `PROC_DeliJar`).
2. Buds: seeded low-poly jittered ellipsoids with random rotation/scale, two material slots (body + accent: pistils/purple/frost) per family. LOD0 buds with shake on the floor; LOD1 coarse buds; LOD2 a single block column.
3. Per-step triangle budgets stated in PROC_PIPELINE.md and enforced by the generator. Every vertex inside the cavity.
4. FBX copied into `_Game/Art/Procedural/JarFill/`; EditMode test checks import (names, steps, LODGroup, scale/up, cavity bounds, budgets).
5. Hook description for the later GAME task (fill → step, batch → family).

## Validation
- Generator twice → byte-identical FBX + manifest (sha256).
- `Tools/Studio/studio.ps1 unity-compile` and `unity-test-edit` green (DEC-013 gate: ≤2 Unity.exe, wait/retry 60 s).
- Contact sheet ≤1 MB: rows = families, columns = fill steps.

## Handoff
`Docs/Handoffs/PROC-002.md` (≤40 lines). Report to the Studio Hub.
