# REVIEW-PROC005d: PROC-005 round 4 (answers REVIEW-PROC005c)

**Reviewer:** fresh one-shot reviewer · **Verdict to:** Hub · **Date:** 2026-10-30
**Reviewed:** `claude/elated-satoshi-3a4844` @ `9d50044`, then head `398e5ef` (adds only `.meta` files + the handoff EditMode line), merged `--no-ff` onto `review/proc005d` from `main` @ `4cec77c` (the branch already contains main @ `4d1bcbd`; no conflicts). `Docs/Reference/ROOM_FIXTURES.json` on the branch is identical to main's (REF-016).
**Sources read:** `Docs/Tasks/Active/PROC-005.md`; `Docs/Reviews/REVIEW-PROC005c.md` (`review/proc005c` @ `35cb3ef`); `Docs/Handoffs/PROC-005.md` (round 4, FOR THE HUB, Not done); the round-4 diff `c3fed40..9d50044` (params, generator, manifest, validation, contact sheet, KNOWN_GAPS, checklist); RF rows `Counter_Register_South`, `Counter_Register_SouthWestReturn`, `POS_02..07`, `POS_StationKit`, `_about`; `Docs/Handoffs/REF-016.md`; `Docs/KNOWN_GAPS.md` GAP-131 / GAP-PROC-42.

## Verdict: PASS with minors

The REVIEW-PROC005c MAJOR is fixed: the South run carries 5 stations at the REF-016 x values, register 7 sits on SouthWestReturn per POS_07 with its customer face west, and the monitor moved to the customer half. Determinism holds, validation passes, Unity EditMode: see the table.

## SouthWestReturn facing: **W** (not a real source conflict)
Every piece of layout evidence puts R7's customer on the **west** face of the block:
- RF `POS_07` (REF-016): `faces: W`, `staff_side: E`, operator zone x 17.78–20.4 (staff aisle, east of the block), customer "at x ~14.1", orientation conf Med-High; src_primary **wall2_R2C1** (CCTV, camera SW looking N: monitor and keyboard face the operator on the E side, card terminal on the W edge, customer standing W on patterned tile).
- RF `Counter_Register_SouthWestReturn` matrix: `served_side` "its west face is R7's customer face"; note "carries register 7 facing west (wall2_R2C1)".
- `Docs/Handoffs/REF-016.md` (south-side settlement; GAP-131 narrowed) and `KNOWN_GAPS.md` GAP-131: "7 on the west-end block x 15.28–17.78 facing W".
- Geometry: the block's east face is the closed end of the staff aisle (A011/A012 vectors 3017/3019, A901 detail 17); customers cannot stand there. The TI drawings fix the block's size and position only; none gives a facing that disagrees.

The row's `faces: E` is a stale REF-013 field: it was written when the return was a pure staff-aisle closure with no register (its "front" was the side facing the aisle), and REF-016 added R7 to the matrix without updating `faces`. It is one un-updated field against its own matrix, not two sources disagreeing. **The worker's choice (customer face +Y → W, `plan_axis_x: -y (north)`, manifest `customer_faces: "W"`) is correct.** A REF doc fix of the row's `faces` (E → W) is still owed so consumers that read `faces` alone are not misled (minor 2).

## Checks
| Check | Result |
|---|---|
| South stations vs RF POS_02..06 | **Match.** Registers 2..6 at local x −2.1214 / −0.9632 / 0.1951 / 1.3533 / 2.5116 m (= x 21.2 / 25.0 / 28.8 / 32.6 / 36.4 ft − 28.16), axis +x. Manifest anchors carry `rf_fixture` POS_02..06. 5 walnut drawer cabinets on the contact sheet follow them. |
| R7 on SouthWestReturn vs RF POS_07 | **Match.** Local x 0.4724 m on axis −y (north) = y 23.2. Customer face +Y → W, so card terminal and wrap edge are west, drawers/open bays face the staff aisle (east). `Anchor_Register_07_Operator` lands at plan (18.78, 23.2), inside the POS_07 operator zone; `_Call` at x ≈ 14.08 = RF "customer stands at x ~14.1". Drawer cabinet slides to the north end (no sliver bay; generator `snap`), visible on the contact sheet. |
| Monitor vs RF POS_StationKit | **Match (side).** `pos_monitor` 0.42 m in from the staff edge: Blender y +0.039 on South/SWR (0.762 top) and +0.085 on North (0.671 top), i.e. customer half, yaw 180 (screen to staff). Keyboard, receipt printer, scanner on the staff half; card terminal toward the customer edge. Offsets GAP-RK-LAYOUT. |
| Counter sizes / North / EastReturn | Unchanged from round c (matched); FBX untouched this round. |
| GAP renumbering | GAP-PROC-22/23/24 → 40/41/42 avoids PROC-009's vehicle GAP-PROC-23..24; no stray old ids in the register params. |
| Determinism | `blender.ps1 register_counter_run` on the merged tree: exit 0; no FBX changed; validation JSON + manifest differ only by CRLF/LF (`git diff --ignore-cr-at-eol` empty). All 4 counters validate `passed: true`. |
| Unity EditMode (`studio.ps1 unity-test-edit`, merged tree) | **Pass:** 790 total, 788 passed, 0 failed, 2 skipped (`Artifacts/Results/20261030-131749-581-37576-unity-test-edit.json`), run on the merged tree with `9d50044`. This reproduces the worker's result on `c3fed40`. Head `398e5ef` adds only `.meta` files and the handoff line, which were merged after the run. |
| DEC-122 visual (register contact sheet) | South row shows 5 evenly spaced drawer cabinets on black open bays; SWR row shows one walnut cabinet at its north end, grey GAP-PROC-42 customer face, quartz top with grommet over the cabinet. Reads as the same kit as the North/East runs. |

## minor
1. **R7 scale-stand slot lands inside the South run counter.** `components.scale_stand_slot` is a fixed dx +1.8 ft along local +X ("staff's right"). On SouthWestReturn local +X is north, so R7's slot exports at plan ≈ (18.43, 21.4): inside `Counter_Register_South` (y 20.0–22.5). RF POS_07 puts the stand at the operator's **left**, `stand_rect` x 17.78–19.08, y 24.0–25.6 (centre y 24.8, i.e. 1.6 ft south of the monitor, local dx ≈ −0.49 m); the row says why ("the operator's right (north) is the run's counter"). The x/depth is right; only the along-axis offset is wrong. Low-confidence row (GAP-131) and nothing consumes `station_anchors` yet, so not blocking, but fix it (a per-station dx override) before ART-011/013 place stands from the manifest.
2. **RF `Counter_Register_SouthWestReturn.faces` still says E.** Doc fix for REF (E → W, or a note that `faces` there meant the aisle side); see the facing section. Until then ART must read the manifest's `customer_faces: "W"`, as the handoff says.
3. Carried from round c, unchanged and acceptable as labelled: boards plain (GAP-PROC-34), LOD3 single boxes, wood grain along world X until PROC-007 UVs.
4. **Texture `.meta` import settings are Unity defaults (head `398e5ef`).** The 68 FBX metas and the texture metas were committed straight from the import. Every `T_Proc_*` texture has `textureType: 0` and `sRGBTexture: 1`. The handoff's own note says Normal must be typed as a normal map and the HDRP Mask must have sRGB off. Fix that with the HDRP material builder, before any material reads these maps. Nothing consumes them yet.
5. Still owed (handoff "Not done"): the HDRP material builder reading `finishes`, and the `to_unity`/BoxCollider EditMode test.
