# REVIEW-W4U — REF-009b (REVIEW-W4R fixes + DEC-062 room answers), docs only

**Verdict: PASS with minors (GO to merge).** `task-ref-009b` @ 233ee85 merged `--no-ff` into `review/wave-4u` off main 8a5723f; clean merge. Files: `ROOM_FIXTURES.json` (rev5, 86 rows), `REFERENCES_INDEX.md` §7, `KNOWN_GAPS.md`, `PROJECT_STATE.md`, handoff. No blockers or majors.

## 1. JSON validity, format, bounds — PASS
- Parses; 86 fixtures (FOH 13, Office 27, Break 22, Restroom 8, BOH 8, Hall 4, Vestibule 4); round-trips byte-for-byte through `json.dumps(indent=1)`, so the format matches rev3.
- Bounds against REFERENCES_INDEX §1.3 (doors with a 0.35 ft tolerance): every new or moved FOH, Hall, Restroom and BOH row is inside its room, and no FOH fixture overlaps the vestibule. The remaining out-of-bounds rows are older wall-edge or shell rows (vestibule shell and doors, lavatory/mirror on the wall line, office deli shelf), unchanged from W4R. One new one: m1.
- Overlaps among new rows are stacked or wall items by design (scanner on the ex-register-1 desk, ladder/desk/fridge/cooler re-spaced along the wall with no footprint overlap, bench and table no longer overlap).

## 2. Rows against DEC-051 / DEC-062 — PASS
- **FOH:** the wall order is ladder (NE corner), then desk, fridge, cooler (DEC-062) ✔. The product racks are the 4 rolling racks only, wall racks stay removed, and the rack length is Low under GAP-127 ✔.
- **Hall:** `Panel_Blank` is a 1.0 × 0.1 × 1.5 ft plain panel; no keypad detail, and the exclusion sentence is in `_about` (DEC-006/031) ✔.
- **Break room:** bulletin board on the hallway wall (contents not modelled) ✔; JC with a mop sink, mops/brooms and a small cleaning-supply rack ✔.
- **Restroom:** heading west on entry, straight ahead (west wall) is the sink and mirror, the paper-towel dispenser is to the sink's left (south), the toilet is far right (north), the tool chest is between them (below the grab bar), and the large storage cabinet is unplaced under GAP-109 ✔ (consistent with the A011 corners).
- **BOH:** `Rack_Chrome_Cartons` (drink cartons plus misc boxes; "brand not modelled") and `Scanner_Barcode` on the ex-register-1 desk ✔.
- No brand names, logos or safe/cash/camera detail were added. The only "safe/cash/camera" hits are exclusion sentences. ✔

## 3. REVIEW-W4R m1–m5 — all closed
- m1: new GAP-127 is on 22 rows, and the KNOWN_GAPS wording matches the rows ✔.
- m2: DEC-062 settles that the 4 rolling racks are the only FOH racks ✔.
- m3: `Bench_Wood` x 17.75 (17.1–18.4) vs table (14.55–17.05), no overlap ✔.
- m4: §7.3 no longer mentions a towel dispenser ✔.
- m5: GAP-121 now says "two tall black cabinets" / "a tall box NE"; "safe" appears only in the exclusion sentence ✔.
- n2 (fan on the cabinets) ✔; n1 (electrical box colour dropped) ✔.

## Minors
- m1 `Mops_Brooms_JC` is centred at x 22.9, on the JC east-wall line, so its footprint reaches x 23.4, past the break-room edge (23.31). Move to x ≈ 22.4 (inside the JC, x 19.9–22.9).
- m2 Some changed rows are Low but carry no GAP id: `Accessories` (dispenser positions "Low") and `Panel_Blank` (placement from A011, which is sourced, so it is probably fine). Add `gap: GAP-127` to `Accessories`.
- m3 Confidence labels disagree with the notes on several GAP-127 rows: ladder, bulletin board, tool chest, scanner and fan are "Med" while the notes say position or size is Low. Convention is presumably "Med = exists, Low = placement"; state that in `_about` or set Low.
- n1 REFERENCES_INDEX §6.6 (TI facts) still lists a "semi-recessed towel dispenser", while DEC-062 says an old silver manual dispenser. `Accessories` follows Nolan; add a one-line "superseded by DEC-062".
- n2 `ToolChest_Black` (2.75 ft tall) touches `GrabBar_West` at the 33 in mark; fine as a "kept below" claim, but give it 2.6 ft if ART sees z-fighting.
- n3 The GAP-109 line in KNOWN_GAPS is now a long run-on; consider splitting when next edited.

## For the Hub
The two open questions (is `Board_Bulletin_West` the same board as `Board_Cork`; which wall is the large restroom cabinet) are properly placeholdered (both kept / unplaced under GAP-109). Open REF-008 items Q4, Q17, Q20 stay open. ART can use rev5 now; fix m1 before the break-room build.
