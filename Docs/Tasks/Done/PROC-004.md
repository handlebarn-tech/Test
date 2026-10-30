# PROC-004 — Packaged-goods generator family (Blender headless)

**Role:** ART-PROC · **Priority:** P1 · **Branch:** `claude/task-proc-004-e1b126` off `main` (6aa6f90) · **Depends:** PROC-001/002 (done), BUILD-005 (LFS for procedural FBX; not on `main` yet)

## Goal
The store also sells packaged goods (DEC-034): prepack flower, prerolls, vapes, edibles, extracts, beverages, topicals and merch. Build one deterministic generator family that makes their neutral package meshes, so DES-002 and GAME-004 can place them post-slice. The slice stays deli-only.

## Read
`Docs/Handoffs/PROC-001.md`, `PROC-002.md`; DEC-034; `Docs/ASSET_PRODUCTION_PLAN.md` §8 "Cannabis product forms", §18 "Product packaging families — procedural", §20 Product-density (per-package material / LOD), §21 (fictional brands), §41.4 CA-PKG-*; `Docs/Assets/Specs/PROC_PIPELINE.md`.

## Inputs
- No package dimensions exist in `References/`. Every size is a placeholder of a common retail form (GAP-PROC-10).
- Brand names and logos are an open IP question with Nolan. Label art stays generic: a flat neutral label slot plus `UVMap_Label`, no logos, no trademarks, no text (GAP-PROC-11).

## Owns
- `Tools/Blender/generators/packaged_goods.py`, `Tools/Blender/params/packaged_goods.json`; a minimal `contact_sheet` extension in `Tools/Blender/run_generator.py` (per-generator sheet for ungrouped assets).
- `Art/Exports/Procedural/PROC_Pkg_*.fbx` + manifest entries; `UnityProject/Assets/_Game/Art/Procedural/Packaged/` (FBX + .meta).
- `Code/Tests/EditMode/ProcArt/PackagedGoodsImportTests.cs`.
- `Docs/Assets/Specs/PROC_packaged_goods_contact_sheet.png`, a PROC-004 section in `PROC_PIPELINE.md`.
- `.gitattributes`: the same two LFS lines as BUILD-005 (identical hunk, so the merge is trivial).
- Not: `Code/Simulation|Presentation`, graybox scenes, `Tools/Studio/studio.ps1`.

## Deliverable
1. `Tools/Blender/blender.ps1 packaged_goods Tools/Blender/params/packaged_goods.json` builds one FBX per item: prepack jar + mylar pouch, preroll tube + multipack carton, vape cart box, edible box + bag, extract jar, beverage can + bottle, topical tube, merch (folded tee, lighter, grinder).
2. Shapes are lofts of parameterised rings (round / superellipse / rounded rect). Each item has a `brand_rgb` and a label rectangle: front faces inside it use a `Label` material slot and map to 0..1 in `UVMap_Label`.
3. LOD0 (modelled seams/caps), LOD1 (fewer segments), LOD2 (one far block in the brand colour, §20 "Far"). Budgets per item in the params file, enforced by the runner.
4. Unity copy + EditMode test: every item imports with a 3-LOD LODGroup, meters/Y-up (bounds match the params), budgets, label slot on LOD0.

## Validation
- Generator twice → byte-identical FBX, manifest, Unity copies and sheet (sha256).
- Earlier generators (deli_jar, package_base, jar_fill) still regenerate byte-identically.
- `studio.ps1 unity-compile` + `unity-test-edit` green (DEC-013 gate: ≤2 Unity.exe, wait/retry 60 s).
- Contact sheet ≤1 MB.

## Handoff
`Docs/Handoffs/PROC-004.md` (≤40 lines). Report to the Studio Hub. Never ask Nolan (DEC-033).
