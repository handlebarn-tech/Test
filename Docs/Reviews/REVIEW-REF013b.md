# REVIEW-REF013b — REF-013 fix round (answers REVIEW-REF13 M1, m1–m3; REVIEW-ART7 m3; DEC-115)

**Verdict: PASS (0 major, 2 minor).** M1 is fixed: every HUB size is now a labelled GAP-132 placeholder. The DEC-115 rulings are applied field by field, and the moved break-room and FOH rows check out geometrically.

I reviewed `worktree-agent-ae92283c8f8687a3d` @ `3890936` (one fix commit on top of `aa01aa4`, which held REF-013 @ 73e0e0c plus main). This file is on `review/ref13b`, cut from `main` @ 67ef2a0, with the worker branch merged `--no-ff` (clean, no conflicts). Inputs read: the packet, REVIEW-REF13, the handoff's Fix round, Validation and Not-done sections, DEC-110 and DEC-115, and the fix diff. I checked everything with a scratch script that read the three JSONs at 3890936 and compared them with its parent.

## Checks
1. **Round-trip: PASS.** DOORS, ROOM_FIXTURES and SCENE_ANCHORS are each byte-identical with `json.dumps(indent=1, ensure_ascii=False)` and LF-only. SCENE_ANCHORS is unchanged in the fix round.
2. **M1, HUB sizes: PASS.**
   - `HUB/Desk_Computer`, `HUB/Counter_Long_EastWall` and `HUB2/Cabinets_Storage_OfficeWall` now carry `gap: GAP-132`.
   - Their notes split the confidence: position Med (DEC-110 W3, and A011 for the room), size_ft Low. The notes say where each size comes from: a convention placeholder; a ±3 ft CCTV-perspective read plus depth and height placeholders, with the A940 34" explicitly excluded; and a copy of the graybox.
   - KNOWN_GAPS GAP-132 is reopened, narrowed to these three sizes, and makes no question (DEC-105).
3. **DEC-115 (1), hinges: PASS.** Both flips are geometrically consistent with the DOORS `_about` conventions:
   - `HUB2_HUB`: S jamb, hinge (18.995, 51.1), closed yaw −90 (north), open +90 → east, into HUB. Standing on the HUB 2 push side, the hinge is on the right, which matches A011.
   - `Ext_Delivery`: N jamb, hinge (0.1, 49.5), closed yaw +90, open +90 → west, out. That is also right-handed from the HUB 2 side.
   - `hinge_unity_m` z = −y × 0.3048 checks for both. The anchors (1.5 ft and 3.5 ft) did not move and are still correct.
   - The audit is Med with A011 + DEC-115 (1) as sources. GAP-137 is gone from the hinge field, but the rows still carry GAP-137 through clearOpening.
4. **DEC-115 (2), hardware: PASS (REVIEW-REF13 m1 closed).**
   - Entry is `storefrontPull` (Med), sourced to DEC-115 (2), A310 E101 and CF §7.1. The `_about` enum includes it.
   - Push bars appear only on Emergency_RetailE, Ext_Emergency_SE and Ext_Delivery.
   - Every lever is sourced to its A310 lockset: JC 2.0 CLX3357 High, restroom 3.0 ML2068 Med, 104 set 1.0 High.
   - Hall_Office and HUB2_HUB have no scheduled hardware, so they are Low with GAP-138. No "lever elsewhere" or "only from CCTV" text is left.
5. **DEC-115 (3), defaultState: PASS (m2 closed).** Exactly the 8 named rows are Low with GAP-138, with the source text "inferred from absence … does not prove closed". The value `closed` is kept.
6. **Field-audit integrity: PASS.**
   - Every audited field on all 15 rows has a source.
   - Every Low field has a gap.
   - Each row's `gap` is the union of its field gaps.
   - The parent-vs-fix diff shows only the fields tabled in the handoff.
7. **REVIEW-ART7 m3: PASS.**
   - **Break room.** The table, bench and whiteboard moved to y 37.0, and the bulletin board to y 39.75–42.75, still on the west wall (DEC-062).
     - No overlaps with other break-room rows.
     - The bench (y 34.5–39.5) is clear of the hall-door sweep (to y 32.9) and the JC sweep (y 43.1–45.8).
     - The only route to the JC door is east of the bench. Its pinch points are 2.5 ft (bench to fridge) and about 2.0 ft centre-to-corner, or about 1.7 ft net of the wall face, as the worker reports. Both are ≥ 1.5 ft.
     - All four rows stay GAP-127 placeholders.
   - **FOH trash.** The bin (x 28.4–29.9, y 29.95–31.45) sits against the south face of the propped Vest_FOH leaf (open leaf x 28.4–31.4 at y 29.8). It is at the latch end and inside the closing sweep (2.42 ft from the hinge, R 3.0), so it really does hold the door. `propsDoor` is defined in `_about`.
8. **Scope: PASS.** The fix commit touches only Owns files: the handoff, KNOWN_GAPS, REFERENCES_INDEX, DOORS and ROOM_FIXTURES. The builder lookup rename and the `propsDoor` swing-skip are left to ART and documented in the handoff (the builder is ART-owned).

**Validation run by me:** the round-trip, the field-audit asserts, the gap-union check, the hinge geometry, and the overlap and sweep checks on the moved rows. I could not run `room_fixtures_layout.py --check` on the real layout, for the reason the handoff states: it still looks up `Counter_Register_SouthReturn`. I relied on my own geometry instead.

## Minors
- m1 **ROOM_FIXTURES has one `confidence` per row, so the three HUB rows still read `confidence: Med`.** The size is Low only in the notes and through the GAP-132 tag. That fits the schema (21 other Med rows also carry gaps), but a consumer that reads only `confidence` sees Med. No action is needed unless the Hub wants per-field confidence in ROOM_FIXTURES, which would be a schema change for a later REF task.
- m2 **The bulletin-board note still begins "Placed between the hall door (y 33.0) and the whiteboard".** That is stale: the board is now south of the whiteboard. The appended REVIEW-ART7 m3 sentence corrects it, but the first clause now contradicts the position. Fix it in the next REF touch; this is not blocking.

## For the Hub
- The ART merge pass owes four things, listed in the handoff: rename the builder lookup to `Counter_Register_SouthWestReturn`; make the swing check skip `propsDoor` fixtures; flip the HUB2_HUB and Ext_Delivery hinges in the graybox; rebuild the break-room table group. Until then, keep NPCs off `Anchor_Door_JC_*`.
- REVIEW-REF13 m3 (frame 30'-6" vs 29.0) is routed to the ART-007 final pass by DEC-115 (5). REF-013 does not change it.
