# PROC-002 handoff — jar fill / bud system

**Status:** done, validation passed. Branch `claude/task-proc-002-99e871` (off main e493fa1). Packet `Docs/Tasks/Active/PROC-002.md` (written by this workcell; no packet existed). No edits to `Code/Simulation|Presentation`, graybox scenes or `studio.ps1`.

## Delivered
- `Tools/Blender/generators/jar_fill.py` + `params/jar_fill.json`: seeded low-poly buds piled in the `PROC_DeliJar` cavity (read from `deli_jar.json`). 6 looks (ASSET_PRODUCTION_PLAN §8) × fill steps 0/10/20/40/70/100 % × LOD0/1/2. One FBX per look, objects `PROC_JarFill_<Look>_F<pct>_LOD<n>`. F000 = SOLD OUT (shake crumbs only).
- `run_generator.py`: `variants()` (one params → many assets), `unity_dir` copy, `preview_context()` / `preview_groups` renders, `contact_sheet <generator>`. PROC-001 outputs regenerate byte-identically (FBX, manifest entries, sheet unchanged).
- Unity: `Assets/_Game/Art/Procedural/JarFill/*.fbx` (+ .meta, default importer). Test `Code/Tests/EditMode/ProcArt/JarFillImportTests` (new asmdef `Dispo.ProcArt.Tests`).
- `Docs/Assets/Specs/PROC_PIPELINE.md` PROC-002 section; contact sheet `Docs/Assets/Specs/PROC_jar_fill_contact_sheet.png` (829 KB).

## Validation (2026-10-29)
- All four generators + both contact sheets run twice from a clean shell: sha256 identical for every FBX, manifest, Unity copy and sheet.
- Tris per visible step (budget): LOD0 4560 (5000), LOD1 1140 (1400), LOD2 28 (40). The generator fails over budget or if any vertex is <1 mm from the glass.
- `studio.ps1 unity-compile`: csErrors=0, CompileCheck OK. `unity-test-edit`: 30/30 (24 existing + 6 new).
- The Unity test confirms for every look: LODGroup auto-built with 3 LODs, every step/LOD present, meters + Y-up (all vertices inside the cavity in root space), tri budgets, fill top rises monotonically per step. This also answers PROC-001's open import question for scale/up and `_LOD<n>` auto-setup.

## Hook for the GAME task (not built; Simulation/Presentation not touched)
- Spawn `PROC_JarFill_<Look>.fbx` as a child of each jar at identity (same bottom-centre origin as `PROC_DeliJar`).
- Step from `InventoryService.Fill(batchId)` (grams / 454): `IsSoldOut` → F000; else the nearest of 10/20/40/70/100 (ties go up). A 451.5 g "full" jar (fill 0.994) maps to F100. Enable only that step's three LOD renderers (name contains `_F<pct>_`); the LODGroup stays as imported.
- Update on `InventoryService.Sold` for `e.BatchId` only.
- Look per batch: [GDD] placeholder until art data exists, e.g. a stable hash of the batch id mod 6 (never `string.GetHashCode`, it's salted per run). Do not invent per-strain looks.

## For the Hub
- Register **GAP-PROC-07** (bud looks are placeholders) and **GAP-PROC-08** (linear fill height, no measured fill) in `Docs/KNOWN_GAPS.md`.
- FBX materials import as Unity defaults from the FBX colours. HDRP Lit bud materials (detail normal, subtle SSS, §22) belong to ART. Scan-based buds (§22) can replace `blob()` at the same budgets.
- Move `Docs/Tasks/Active/PROC-002.md` to Done on merge.
- Not done: no in-scene look at the fill under HDRP lighting (no scene owned), and no per-instance random yaw. The hook can add yaw in 90° steps, because the jar is square.
