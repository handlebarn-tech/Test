# PROC-004 handoff — packaged-goods generator family

**Status:** done, validation passed (see below). Branch `claude/task-proc-004-e1b126` (off main 6aa6f90). Packet `Docs/Tasks/Active/PROC-004.md` (written by this workcell). No edits to `Code/Simulation|Presentation`, graybox scenes or `studio.ps1`.

## Delivered
- `Tools/Blender/generators/packaged_goods.py` + `params/packaged_goods.json`: 14 items for the DEC-034 categories, one FBX each (`PROC_Pkg_<Item>`): PrepackJar, FlowerPouch, PrerollTube, PrerollMultipack, VapeCartBox, EdibleBox, EdibleBag, ExtractJar, BevCan, BevBottle, TopicalTube, MerchTee, MerchLighter, MerchGrinder.
- Data-driven. An item is a list of parts, and each part is a loft of `[width, depth, z]` rings (superellipse or rounded rect). A new SKU shape is a params entry, not new code. Each item has a `brand_rgb`, and the label rectangle becomes a `M_Proc_PkgLabel` slot plus `UVMap_Label` 0..1. The label is a neutral placeholder: no logos, trademarks or text.
- LOD0 / LOD1 / LOD2 (far block in the brand colour, plan §20). Budgets are per item and enforced; the table is in `PROC_PIPELINE.md` (worst case 520/256/28, against 600/300/40).
- Unity: `Assets/_Game/Art/Procedural/Packaged/*.fbx` (+ .meta, default importer). Test `Code/Tests/EditMode/ProcArt/PackagedGoodsImportTests` (14 cases: 3-LOD LODGroup, bottom-centre origin, size vs params, budgets, label slot, uv2).
- `run_generator.py`: `contact_sheet <gen>` also works for ungrouped assets; `own_sheet` assets stay off the default sheet. Sheet `Docs/Assets/Specs/PROC_packaged_goods_contact_sheet.png` (783 KB).
- `.gitattributes`: added the **same two LFS lines as BUILD-005** (identical hunk, so the merge is trivial). BUILD-005 is not on `main` yet. Only the new `PROC_Pkg_*` FBX are committed (as LFS pointers). The older procedural FBX were left out on purpose; BUILD-005 owns their conversion.

## Validation (2026-10-29)
- Every generator (deli_jar, package_base ×2, jar_fill, packaged_goods) and all 3 contact sheets ran twice from a clean shell: 47 files sha256-identical between the runs. The earlier FBX and sheets are byte-identical to HEAD. The manifest only gained the `PROC_Pkg_*` entries.
- `studio.ps1 unity-compile`: csErrors=0, CompileCheck OK. `unity-test-edit`: 163/163, including the 14 new `PackagedGoodsImportTests` cases (DEC-013 gate passed, no wait).

## For the Hub
- Register **GAP-PROC-10** (all packaged sizes are placeholders of common retail forms; no measured SKUs) and **GAP-PROC-11** (label/brand art is a neutral slot until the brand-name IP question with Nolan is settled) in `Docs/KNOWN_GAPS.md`.
- Not covered (from plan §41.4): tincture bottle, disposable/AIO box, battery blister, rolling papers, cones. Each is a params entry when wanted. The mug was skipped because the handle needs a non-loft part.
- On round bodies the label is a planar front projection: faces at the label's side edges can run slightly past 0..1 in `UVMap_Label`. A clamped label shader is fine for that.
- Materials are preview colours. HDRP Lit (glass, foil, metal) and the label texture atlas belong to ART/DES.
- Move `Docs/Tasks/Active/PROC-004.md` to Done on merge.
