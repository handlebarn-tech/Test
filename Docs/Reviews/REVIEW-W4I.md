# REVIEW-W4I — PROC-004 (packaged-goods generator, 14 items x 3 LODs)

**Verdict: PASS (GO to merge).** `claude/task-proc-004-e1b126` @ 94d683e merged `--no-ff` into `review/wave-4i` off main. Only conflict: the packet moved to `Docs/Tasks/Done/PROC-004.md` (kept). No blockers or majors.

1. **Determinism - PASS.** `packaged_goods` run twice: 14 items each, and the sha256 of every FBX and procedural contact sheet is identical before, after run 1 and after run 2 and equals the committed files. The contact sheet is identical across 2 regenerations. Only `manifest.json` shows CRLF churn (reverted, not committed). Sheet viewed: 14 rows (bottles, cans, pouches, boxes, jars, tubes, grinder, lighter, tee), LOD0 front/side and LOD1/LOD2. Each LOD reads as the same object. The side-view column makes pouches look like thin spikes, which is expected. Label slots are blank pale rectangles.
2. **Brands - PASS.** No logos, text or trademarks. Labels are a neutral `M_Proc_PkgLabel` slot with `UVMap_Label`. Colours are preview `brand_rgb` values. GAP-PROC-11 in params defers real brands to the IP decision.
3. **LODs, budgets, LFS - PASS.** Worst case 520/256/28 tris against budgets 600/300/40 (table in PROC_PIPELINE.md, enforced per item by the generator and by `PackagedGoodsImportTests`). All 43 tracked FBX are LFS pointers. 28 are `PROC_Pkg_*` (14 in `Art/Exports`, 14 in `Assets/_Game/Art/Procedural/Packaged`). `doctor`: lfsPatterns 11/11.
4. **Unity - PASS.** `unity-compile` csErrors=0. `unity-test-edit` 163/163 (includes 14 PackagedGoodsImportTests). I ran one editor through the runner and did not test two editors at once (DEC-013).
5. **Categories and sizes - PASS.** The params hold 8 categories (prepack_flower 2, preroll 2, vape 1, edible 2, extract 1, beverage 2, topical 1, merch 3), matching the DEC-034 list. All dimensions are placeholders (GAP-PROC-10).

## Minors
- m1 Hub must register GAP-PROC-10 and GAP-PROC-11 in KNOWN_GAPS (per handoff).
- m2 Round-body label UVs can run slightly past 0..1; use a clamped label shader.
- m3 Not covered: tincture, AIO box, battery blister, papers, cones, mug. Each would be a params entry.
- m4 I did not compare every item's LOD triangle count to the table by hand; I relied on the generator's enforcement and the 14 import tests.
