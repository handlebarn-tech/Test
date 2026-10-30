# REVIEW-REF016: store-evidence matrix (evidence reviewer, DEC-120 (3))

**Reviewed:** `worktree-agent-a9f9579ab68e3b5d2` @ `14332c3` · **Merge base:** `4e1b088` · **Review branch:** `review/ref016` (cut from `main` @ `751b85a`, worker merged `--no-ff`; the merge was clean)
**Read:** packet `Docs/Tasks/Active/REF-016.md`; the diff (ROOM_FIXTURES rev9, DOORS rev4, SCENE_ANCHORS v3, REFERENCES_INDEX §1–§9, handoff); handoff Validation and Not-done; `Docs/Design/PLAYTEST2_2026-10-30.md` #3/#4/#6/#8–#10; DEC-039, DEC-120.
**Evidence opened directly, in packet order:** TI approved set p.35 (E101) and p.13 (A901 det. 17) as words and a render; A011 vectors (PyMuPDF `get_drawings()`/`get_text`); CCTV Camera Wall 2 tiles R2C1, R2C3, R2C5 (full-resolution crops); CCTV Register Back Center Wide (top-left magnified); `graybox_layout.json` for the implemented column. I did not open ART-013 or any Unity review.

## Verdict: FAIL

The failing acceptance item is **Deliverable 2, south-side register positions** (and the Validation rule that measured values show their measurement). The register count, Register 7, staff and customer sides, the emergency-exit wall and the guard/ID position all hold against the evidence. The x positions of registers 02..06 rest on a misreported TI measurement (M1).

## Checks

| # | Check | Method | Result |
|---|---|---|---|
| 1 | JSONs parse | `json.load` on the three files at `14332c3` | PASS |
| 2 | DEC-047: every row cites a source | every one of the 132 RF rows has `matrix.src_primary` and `implemented.status`; I diffed the changed values (`size_ft`/`pos_ft`/`rot`/`faces`) against `main` and each one has a source in its row | PASS. 15 untouched rows have Low fields and no GAP id (m4) |
| 3 | South count: TI | p.35 E101 words: `POS` at x 644/710/875/947/1021 pt with A-10/12/14/16/18, all on one line y 774 → **5 circuits**. p.13 A901 det. 17: 5 `TV` boxes at x 438/506/669/743/816 pt | PASS (5) |
| 4 | South pitch: TI | the same words at 18 pt/ft. Gaps between neighbours: A901 **3.78 / 9.06 / 4.11 / 4.06 ft**; E101 **3.67 / 9.17 / 4.00 / 4.11 ft**. The render shows two outlets, a ~9 ft blank run, then three outlets | **FAIL: M1** |
| 5 | South count/pitch: CCTV | R2C5 (from the SE, looking W along the run): **4** monitors visible on the straight run, receding at an even spacing, with the R2C1 scene (register 7, yellow-hood customer, green-jersey operator) beyond them. R2C3 and the wide still show even spacing too | consistent with ~4.0 ft pitch; contradicts the TI 2+3 grouping (M1) |
| 6 | Numbering direction / Register 7 | R2C1 at full resolution: the camera looks N with the entry on the far left, so it sits in the SW. The foreground block runs N–S. Its monitor screen and keyboard face an operator on the east (right) side, the card terminal is on the west edge, and the customer stands west of it. The run continues east from the block's north end, with staff (south) on patterned tile and customers (north) on marble. DEC-039 also reads the north side "10 … 8" with 8 nearest the door, which is the same staff-perspective convention, so 7 = west and 6 = east is consistent | PASS (facing, block, side). y along the block: m1 |
| 7 | Staff vs customer side | the wide still, R2C1 and R2C3 all show monitors at the back (customer half) of the top with screens toward staff, keyboards and printers toward staff, and card terminals at the customer edge | PASS |
| 8 | Emergency exit wall | A011, frame x0 = 1044.6 pt (west face; 3017 x 1319.4 = 15.28 ft), y = 29 − (723.4 − pt)/17.987. Results: 3571 ends at pt 586.4 → **21.38**; 3567 starts at 646.4 → **24.72**; 3413/3420 interior face 47.19 → 48.26 at y **18.31** (step **1.07**); 3610 leaf from (1924.7, 590.2) → hinge (48.93, **21.59**), 53.9 pt = 3.0 ft at 45°, so the hinge is N and the leaf swings out east. "EMERGENCY EXIT" label at (1992, 612) | PASS. The open slot is confirmed from the build: graybox opening 20.5–24.0 with a 3.0 ft leaf hinged at y 24.0 (yaw −90) leaves 20.5–21.0 open |
| 9 | Sink / east rack | A011 3899 x 1830 → 43.67, 3843 x 1842 → 44.33, y 700–721 pt → 27.7–28.9; "HAND WASHING" label at (1580–1648, 624). Rack 3693/3705 x 1868–1893 → 45.8–47.18, y 459 pt → 14.3 | PASS |
| 10 | Guard / ID | Wide still, top-left at 2×: the uniformed guard is at a dark podium. The bright glazed door is nearer the camera along the west wall (image left) and the framed licences are further along (image right), so the order south → north is door, guard, licences, with a white stool beside the podium | PASS (position north of the door). Anchor geometry: m3 |
| 11 | Implemented column vs builder input | `graybox_layout.json`: stations 07/02..06 at x 31.0/27.8/24.6/21.4/17.8/14.8 on y 22.6; `FX_Sink_E` 45.6–46.99 × 24.6–26.8; `Retail_IDCheck_Stand` y 10.25–11.75; `W_Ext_E_Retail` opening 20.5–24.0; door leaf (47.09, 24.0) yaw −90 / open 90; `Anchor_Guard_Post` (2.5, 9.8) yaw 180; R07 anchors at x 31.0 | PASS (all match the matrix's "as built" text) |
| 12 | Deliverables 3/4/5 | bulletin-board note no longer has the stale y 35.75 clause; small-bin size and monitor-y rulings carry pixel spans and GAP ids; §9.3 has 33 rows | PASS |

## MAJOR

**M1. The south station x positions cite a TI pitch the TI does not show, and the conflict between the TI and CCTV is not recorded (Deliverable 2 positions; Validation "measured values show their measurement"; DEC-120 "the stronger source wins and the row says so").**

`POS_02..06.matrix.src_primary`, `notes`, REFERENCES_INDEX §9.1, the §9.2 row "South POS count / pitch" and the §8.1 register paragraph all state "pitch 3.75–4.08 ft" from A901 det. 17 / E101. The worker's own listed offsets (3.78 / 7.53 / 16.61 / 20.69 / 24.77 ft) give a **9.08 ft** gap between the second and third outlets, and E101 shows the same 2 + 3 grouping (9.17 ft gap). The TI therefore spans about 21 ft in two clusters. The matrix instead places five stations evenly at 3.8 ft over 15.2 ft (x 21.2–36.4).

CCTV (R2C3, R2C5, wide still) shows even spacing, so today's store probably differs from the 2022 rough-ins. That may be the right call, but the record has to:
- report the TI grouping as it is drawn;
- say which source wins for x and why (TI outranks CCTV in DEC-120 unless the row argues that the store changed);
- keep the conf/GAP tag on the result.

As written, ART-013 would build from a measurement that misstates its top-ranked source. Also reconcile, or at least note, that R2C5 shows 4 monitors on the straight run against the 5 that TI/DEC-039 give (one may be hidden).

## minor

- **m1. Register 7's y.** `POS_07.notes` says R2C1 shows the monitor "mid-block" and places it at y 25.2 (south of the block's mid-point, 23.5). In R2C1 the monitor sits in the north part of the block, and the operator stands roughly level with the run's staff face (y ≈ 22.5–24). The value is Low and tagged GAP-131. Correct the description or the value.
- **m2. DOORS `Emergency_RetailE` has two targets.** `target_opening` is still REF-013's 21.65–24.65 (source text "wall gap 21.52–24.78"). The new `rough_opening` is 21.38–24.72, and the note says "opening = rough_opening". §9.3 row 27 compares against both. Keep one target, or label the other as the clear leaf span.
- **m3. Guard anchor geometry.** `Anchor_Guard_Post` (0.9, 7.9) leaves 0.8 ft between the wall face and the stand, which is too little for a standing body. The evidence supports "behind the podium relative to the floor, north of the door", not a precise x. Flag the stand x / guard x pairing as a placeholder for ART-013 (GAP-134 already covers it).
- **m4. Low fields without a GAP id.** 15 untouched rows (Office `Chair_Task_2`, `Board_West_BlackFrame`, `Shelves_Floating_x3`, `Trash_StepCan`, `Mat_Door`; Hall `Panel_Blank`; BreakRoom `Hoop_Mini`, `Hooks_Coats`, `Mats_Floor_x2`; Restroom `Accessories`; Vestibule `Shelf_Supplies`; FOH `Chair_Desk`, `Props_Floor`; BOH `Rack_South_Wall`, `Chair_Desk`) are Low in every field but have `gaps: []`. They are cited, so this is not a DEC-047 MAJOR. The handoff's check covered only hand-written records.
- **m5. `Trash_Big_East_Sink` is stale.** Its note still says "by the east hand-wash sink, clear of the emergency exit (y 20.5–24)", and its `served_side` is "customer", but the sink is now on the south wall and the SE pocket is staff floor under the kept closed L. The handoff flags it as a possible duplicate of the moved big bin. Record that in the row.
- **m6. Confidence too high on the R07 call/operator anchors.** They carry row confidence Med while their y is Low by the worker's own statement. Use the weakest field (the REVIEW-REF013b m1 principle).

Not run: `Tools/Studio/room_fixtures_layout.py --check`. It is ART-owned and fails on a stale row name, as the handoff says.
