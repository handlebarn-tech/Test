# REVIEW-PROC006c: register kit follow-ups (REVIEW-PROC006b minors 2–6)

**Reviewed:** `claude/zealous-kalam-4192dd` @ `d4c4bc3` · **Merge base:** `d207f31` · **Review branch:** `review/proc006c` (main @ `7f286ff` + worker branch, `--no-ff`) · **Reviewer:** fresh, Hub-spawned (STUDIO_OS §0.7)
**Sources read:** `Docs/Tasks/Active/PROC-006c.md`; the diff `d207f31..d4c4bc3`; `Docs/Handoffs/PROC-006c.md` (Validation, Not done, For the Hub); `Docs/Reviews/REVIEW-PROC006b.md` minors 2–6; DEC-124 in `Docs/DECISIONS.md`.

## Verdict: FAIL

One acceptance item fails: **DEC-124 / m5**. Everything else passes. The worker's base (`d207f31`) predates DEC-124 (`f0300b1` landed three minutes before the worker's commit), so the miss is timing, not care.

## Checks
1. **Blender validation.** I ran `Tools/Blender/blender.ps1 register_kit Tools/Blender/params/register_kit.json`. It exited 0, and all 16 `PROC_RK_*` validation JSONs report pass. The tri counts match the handoff: SprayBottle_ISO is 5160 / 1380 / 476 / 48; the other props are unchanged.
2. **Determinism.** After my rerun every FBX (Art export and Unity copy) is byte-identical to the commit. The validation JSONs and the manifest differ only in CRLF/LF (`git diff --ignore-cr-at-eol` is empty). This covers the second determinism run listed under the handoff's Not done.
3. **Arranger self-test.** `python Tools/Blender/tests/test_register_arranger.py` passes, and the committed station JSONs equal a fresh arranger run. It prints **10** distinct optional sets, not the 11 the handoff reports (minor 1). I also confirmed the handoff's claim that main's station JSONs were stale: the test fails on the `d207f31` tree with "POS_02: committed JSON is stale".
4. **PROC-005 toolkit self-test.** `blender -b --factory-startup -P Tools/Blender/tests/test_validation.py` prints `[SELFTEST] all passed`.
5. **Citations (DEC-047).** The new `sb_hook_*` params, the `STAND_RAIL` edge note and the keyboard's convention dimensions all carry a `_src` or a GAP id (GAP-REG-8, GAP-REG-11). I found no uncited store value in the diff.
6. **m2: contact sheet (visual, DEC-122/DEC-114).** I judged `Docs/Assets/Previews/PROC_register_kit_contact_sheet.png` (1500 × 4800) myself.
   - It has 16 rows × 5 tiles (LOD0 3/4, LOD0 side, LOD1, LOD2, LOD3). Each tile is labelled with the prop, LOD, tris and frame width, and the labels are readable at full size.
   - LOD3 renders as solid shapes, and the LOD steps are visible on every row.
   - The sheet is usable for the DEC-114 judgement. **Pass.**
7. **m3: the ISO spray hangs.**
   - The contact sheet shows a wire S-hook (ring round the trigger neck, arm up behind the head, hook over) on all four LODs. The LOD3 hook is a box approximation, as intended.
   - In the stations sheet, the bottle hangs off the stand-top edge on the operator side, below the hook.
   - The manifest carries `attach_point_unity_xyz` and a `hangs` note, and `STAND_RAIL._src` defines what `pos_m` means for hanging items.
   - **Pass.**
8. **m4: keyboard tagging.** The keyboard has `gaps: ["GAP-REG-11"]`, a `_src` that names `kb_d_m`/`case_h_m`/`key_h_m` as convention, and a GAP-REG-11 row in the spec register. **Pass.**
9. **m5 and DEC-124: the under-counter anchors.** **Fail.** See MAJOR 1.
10. **m6: GAP ids proposed.** For the Hub proposes GAP-REG-1..11, GAP-RK-LAYOUT and GAP-RK-WEIGHTS with text and sources. None are in `KNOWN_GAPS.md` yet, as expected. **Pass, except** that the GAP-RK-LAYOUT text carries the same superseded two-shelf/"open with Nolan" wording (part of MAJOR 1).
11. **Scope.** All changed paths are within the packet's `Owns` (spec, params, generator, arranger sheet script, RegisterKit exports and their manifest rows, Previews, handoff). There is no Unity work and no cash equipment (DEC-051).

## MAJOR
1. **The under-counter model contradicts DEC-124 (acceptance source; packet m5).** DEC-124 (Nolan) says one open shelf, full counter width, at mid height, and no drawers. It replaces the two-shelf `UNDER_UPPER`/`UNDER_LOWER` placeholder. The branch does not follow it:
   - The branch keeps both anchors: `register_kit.json` `arranger.anchors.UNDER_UPPER` (z 0.45) and `UNDER_LOWER` (z 0.12).
   - **27 placed items** across all 11 `RegisterStations/POS_xx.json` sit on `UNDER_LOWER`, a shelf the store does not have.
   - The rewritten gap strings, the spec's Anchors paragraph and the proposed GAP-RK-LAYOUT entry all still say the question is "open with Nolan via the Hub (PROC-006b handoff Q1)". DEC-124 answered it.

   What remains a GAP under DEC-124 is only the exact shelf height and depth.

## minor
1. **Wrong figure in the handoff.** The arranger self-test prints 10 distinct optional sets; the handoff says 11. The test's threshold (≥ 2 differ) still holds, so the only problem is the misreported number.
2. **The stations sheet has no panel labels.** The four panels in `PROC_register_kit_stations_sheet.png` are not marked with their POS id. The handoff says POS_02/06/07/09, but a reader cannot tell which panel is which, for example which one shows the hanging spray.
3. **Previews are not colour-true.** The spray body renders opaque grey, not the translucent white the spec gives (RK-07). The cause is preview colours only, which is REVIEW-PROC006b minor 1 / PROC-010 scope; no action is needed here.

## For the Hub
- The fix for MAJOR 1 is small and stays inside this packet's `Owns`: params, arranger output, spec paragraph, and the GAP-RK-LAYOUT proposal text. It does not touch the props or FBX exports, which pass as they are.
- Once fixed, everything else in this review stands.
