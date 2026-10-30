# REVIEW-PROC006c: register kit follow-ups (REVIEW-PROC006b minors 2–6)

**Reviewed:** `claude/zealous-kalam-4192dd` @ `53de5ff` (`d4c4bc3` and the DEC-124 commit `53de5ff`) · **Merge base:** `d207f31` · **Review branch:** `review/proc006c` (main @ `7f286ff` + worker branch @ `53de5ff`, `--no-ff` merge `59a682f`) · **Reviewer:** fresh, Hub-spawned (STUDIO_OS §0.7)
**Sources read:** `Docs/Tasks/Active/PROC-006c.md`; the full diff `d207f31..53de5ff`; `Docs/Handoffs/PROC-006c.md` (Done, Validation, Not done, For the Hub); `Docs/Reviews/REVIEW-PROC006b.md` minors 2–6; DEC-124 in `Docs/DECISIONS.md`.

**Revision note:** the first verdict on this branch (`90c7077`, FAIL, 1 MAJOR) was written against `d4c4bc3`. The worker had pushed `53de5ff` before my merge, so merge `59a682f` already contains it. All validation below ran on that merged tree. In the files the packet owns, the tree is identical to `53de5ff`.

## Verdict: PASS with minors

## Checks
1. **Blender validation.** I ran `Tools/Blender/blender.ps1 register_kit Tools/Blender/params/register_kit.json`. It exited 0, and all 16 `PROC_RK_*` validation JSONs report pass. The tri counts match the handoff: SprayBottle_ISO is 5160 / 1380 / 476 / 48; the other props are unchanged.
2. **Determinism.** After my rerun every FBX (Art export and Unity copy) is byte-identical to the commit. The validation JSONs and the manifest differ only in CRLF/LF (`git diff --ignore-cr-at-eol` is empty). This covers the second determinism run listed under the handoff's Not done.
3. **Arranger self-test.** `python Tools/Blender/tests/test_register_arranger.py` passes: 11 stations, 10 distinct optional sets (the packet needs at least 2). The committed station JSONs equal a fresh arranger run. On the `d207f31` tree the same test fails with "POS_02: committed JSON is stale", which confirms the handoff's note that main's station JSONs were stale.
4. **PROC-005 toolkit self-test.** `blender -b --factory-startup -P Tools/Blender/tests/test_validation.py` prints `[SELFTEST] all passed`.
5. **Citations (DEC-047).** Each of these carries a `_src`, a GAP id, or both: the new `sb_hook_*` params, the `STAND_RAIL` edge note, the keyboard's convention dimensions (GAP-REG-11), and `UNDER_SHELF`/`UNDER_SHELF_EDGE` (DEC-124; z = half the 34 in counter, REFERENCES_INDEX 6.4; GAP-RK-LAYOUT). I found no uncited store value in the diff.
6. **m2: contact sheet (visual, DEC-122/DEC-114).** I judged `Docs/Assets/Previews/PROC_register_kit_contact_sheet.png` (1500 × 4800) myself.
   - It has 16 rows × 5 tiles (LOD0 3/4, LOD0 side, LOD1, LOD2, LOD3). Each tile is labelled with the prop, LOD, tris and frame width, and the labels are readable at full size.
   - LOD3 renders as solid shapes, and the LOD steps are visible on every row.
   - The sheet is usable for the DEC-114 judgement. **Pass.**
7. **m3: the ISO spray hangs.**
   - The contact sheet shows a wire S-hook (ring round the trigger neck, arm up behind the head, hook over) on all four LODs. The LOD3 hook is a box approximation.
   - In the stations sheet, the bottle hangs off the stand-top edge on the operator side.
   - The manifest carries `attach_point_unity_xyz` and a `hangs` note, and `STAND_RAIL._src` defines what `pos_m` means for hanging items.
   - **Pass.**
8. **m4: keyboard tagging.** The keyboard has `gaps: ["GAP-REG-11"]`, a `_src` that names `kb_d_m`/`case_h_m`/`key_h_m` as convention, and a GAP-REG-11 row in the spec register. **Pass.**
9. **m5 and DEC-124: the under-counter anchors.**
   - `UNDER_UPPER`/`UNDER_LOWER`/`UNDER_UPPER_EDGE` are gone from the params, the arranger, the sheet script and all 11 station JSONs. The only remaining mention is the spec's note that `UNDER_SHELF` replaced them.
   - `UNDER_SHELF` (z 0.43 m) and `UNDER_SHELF_EDGE` cite DEC-124, and height and depth stay GAP-RK-LAYOUT with the DEC-110 search stated.
   - The stations sheet draws one shelf slab spanning the full TOP width (`-h..h`).
   - Placements: 44 items on `UNDER_SHELF` and 3 on `UNDER_SHELF_EDGE`. Items that do not fit go to `not_fitted` (14 across 11 stations) and are never forced.
   - The tallest under-shelf item (open paper stock, 0.27 m) clears the counter top.
   - The spec paragraph and the proposed GAP-RK-LAYOUT entry no longer say "open with Nolan".
   - **Pass.**
10. **m6: GAP ids proposed.** For the Hub proposes GAP-REG-1..11, GAP-RK-LAYOUT and GAP-RK-WEIGHTS with text and sources, in the KNOWN_GAPS format. None are in `KNOWN_GAPS.md` yet, as expected. **Pass.**
11. **Scope.** All changed paths are within the packet's `Owns`: spec, params, generator, arranger and sheet script, RegisterKit exports with their manifest rows, Previews, and the handoff. There is no Unity work and no cash equipment (DEC-051).

## MAJOR
None.

## minor
1. **The handoff contradicts itself on distinct sets.** Its Validation section still says "11 distinct optional sets", but the DEC-124 bullet under Done and my run both say 10. The test threshold holds, so only the record is wrong.
2. **The stations sheet has no panel labels.** The four panels in `PROC_register_kit_stations_sheet.png` are not marked with their POS id (the handoff says POS_02/06/07/09), so a reader cannot tell which panel is which.
3. **Previews are not colour-true.** The spray body renders opaque grey, not the translucent white the spec gives (RK-07). This is the preview-colours issue already in REVIEW-PROC006b minor 1 / PROC-010 scope; no action is needed here.

## For the Hub
- Merge `review/proc006c`. It also carries the superseded first verdict as commit `90c7077`; this file replaces it.
- Register the m6 GAP entries from the handoff's For the Hub section. The PROC-006b FOR NOLAN Q1 (under-counter) is closed by DEC-124.
