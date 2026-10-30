# REVIEW-PROC6 — PROC-006 phase 1, register workstation kit evidence spec

**Verdict: PASS with minors (GO).** I reviewed `worktree-agent-a5f8a932c9a5f07a9` @ 1070e9c. It changes two files, both docs: `Docs/Assets/Specs/REGISTER_KIT.md` and `Docs/Handoffs/PROC-006.md`. I did **not** merge it, because the lead named no `review/assets-<n>` branch; the lead merges it. This verdict is on `review/proc6-verdict`, off main.

Inputs read: the packet, the handoff, the diff, and the cited sources: REFERENCES_INDEX §2/§2.2, the ROOM_FIXTURES rows `Scanner_Barcode`, `Cart_Deli_Prep` and `Desk_Corner_Dual_Monitor`, DEC-021/039/051/071/084/091/096, and GAP-107. I cut all 30 cited pixel boxes from the 4 source images at 3× and checked each by eye.

## Checks
1. **Every row cites a file + crop or a GAP id, and the crops show what the row claims: PASS** (exceptions m1, m2).
   - RK-02: R2C3 shows a white box with an orange lid.
   - RK-03: all 3 crops show a dark handheld scanner in a stand.
   - RK-04: all crops show full-size black keyboards.
   - RK-06a/b: kraft bundles and yellow coils, as stated.
   - RK-06c: a white stack on the stand's lower shelf and a grey box.
   - RK-06e: a white bottle, a blue/white soft pack and a large white bottle. The pump bottle (1140,195) is only a pale blob; the row correctly calls it Low.
   - RK-07: CART shows a white bottle with a red trigger, hung over the rail.
   - RK-08: a grey cloth draped over a shelf edge.
   - Trash bins: a black wire bin (WIDE) and a white wastebasket (CEN) are present.
   - RK-05 (mouse) is GAP, which is correct: neither crop resolves a mouse.
2. **No invented sizes, models or brands: PASS.** Only two sizes are given:
   - Scanner `[0.4, 0.7, 0.6]` ft matches the RF `Scanner_Barcode` row (whose notes say "size Low").
   - The keyboard's ≈17.5 in is REFERENCES_INDEX §2.2's stated convention.
   - Every other size is a GAP-REG id. No model names appear, and the GAP candidates are size classes only.
3. **DEC-051, DEC-071 and DEC-084: PASS** (m3 is a wording issue).
   - No cash equipment. The WIDE keyboard crop shows the low black box with a drawer front, which supports its exclusion.
   - No cameras, and no brand marks; the logo panel is allowed only if a DEC-071 mark is approved.
   - LOD0 targets of 3–18k tris sit within the 5–20k guide, except the mouse at 3–6k, which is fine for its size.
   - LOD0–3 and 2K PBR are stated.
4. **No counter geometry, and anchors read "pending ROOM_FIXTURES rev7": PASS.** The spec uses only the TOP, UNDER and STAND areas and names no graybox ids.

## Minors
- m1 **RK-01, WIDE (235,367)–(315,405):** this box mainly shows a beige flat object (paper or a terminal face) lying on a black unit. It is not a clearly visible receipt printer.
  - Fix: mark this source Low or drop it. CEN (220,330) and EAST (1725,125) carry the row.
- m2 **RK-01, EAST (1165,115)–(1245,160):** this shows an orange item on top of a black box. That could just as well be a label printer with an orange lid, like R2C3.
  - Fix: note the ambiguity in GAP-REG-1/2. It is not counted as a receipt-printer sighting.
- m3 **RK-06e "generic unbranded labels" and RK-07 "generic white label":** DEC-084 says unbranded ≠ generic.
  - Fix: reword as "realistic fictional label art, no real marks (DEC-071/084)" before phase 2 copies it.

The lead's call to add the trash bin in phase 2 is outside this review. The evidence supports it: both bins are visible in WIDE and CEN.
