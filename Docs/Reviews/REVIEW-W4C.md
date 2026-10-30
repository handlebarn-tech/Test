# REVIEW-W4C — REF-006 + REF-007 (FOH/BOH desks, jar spec, SE exit, HUB swap)

**Verdict: GO.** GAP-120 is **confirmed** against A011. Branch `review/wave-4c` = `main` (aa926f9) + `--no-ff` merge of `claude/task-ref-006` (tip 59a2c12, clean, no conflicts) + this review + three annotations in REFERENCES_INDEX §1.3–1.4.

## 1. Images — PASS
I viewed all four raw files and both derived crops.
- `References/Incoming/` no longer exists; all four files moved to `References/` with the existing naming. Rows for all six files are in §0 (DEC-041/042/043).
- **FOH / BOH stills:** no people. The FOH still shows the wall card reader by the door (access hardware). These stills are references, not crops, and like every CCTV still they never ship; no action.
- **`deli_jars_scale_cart_crop.webp`:** no people, no network rack, no thermostat, no security-labelled drawer and no screen content. In the top-left corner (≈x 0–90, y 80–160) there is a small unlabelled black desktop box, a mouse and cables hanging from the rack above. These cannot be identified as network gear and are background clutter. Low risk. Optional: ART can crop to x ≥ 90 when it uses this crop.
- **`deli_jar_wall_retail_crop.jpg`:** people-free. The raw photo's shopper starts at about x 605, and the crop ends at x 590. Confirmed by eye.

## 2. Jar spec — PASS
- **Smalls jar:** I re-fetched Amazon B0GX12Q9G8 myself. The title is "USYOGO POP Airtight … 4L/4.2Qt Jar … (2Pc) and 3.3Oz Scoop (2Pc)", and the details table lists **6.1"L × 5.3"W × 10.4"H**. The material is given only as "BPA-free" / "food-grade … sturdy plastic", which matches REF-007's "resin not named". Sourced; High is justified. The metric conversion (0.155 × 0.135 × 0.264 m) is correct.
- **Acrylic canister ≈6 × 5–6 × 10–10.5", Low-Med:** reasonable. The measured front ratios (1.6–1.9) fall within the published jar's 1.70–1.96, and the office photo reads consistently against the scale. The method is stated, and so is its limit (there is no direct measurement). Keep it a labelled estimate.
- **Tong cups:** recorded as **not modelled** (§2.4 row, handoff), per DEC-043.
- The PROC hand-forward is correct. GAP-PROC-02 says black lids, but the photos show white push-button lids.

## 3. SE exit and GAP-120 — CONFIRMED (key finding)
I read the A011 vector text and rendered the sheet. North is up, with the office at the west end of the back-room row, the same as V5.
- **541.34 SF PRODUCT STORAGE is the west room**: its width dimension reads 18'-9¼", and the office and the west "ACCESS CONTROLLED ENTRANCE / EXIT" both open into it. **818.53 SF is the east room** (28'-3¼"). Depth is 29'-0" in both.
- The partition runs north–south between them. The connecting door is at its **north end**, and its leaf swings into the east room.
- The SE "ACCESS CONTROLLED ENTRANCE / EXIT" is at the **SE corner of the 818.53 room**, on its south wall (by eye ≈x 44.5–47.5, consistent with REF-007's 44.4–47.2), and it swings out.
- The graybox (`graybox_layout.json`) has `W_HUB_HUB2` at x = 28.495 (the wide room west), `DOOR_HUB_HUB2` on that wall at y 48.1–51.1, and `EXT_EMERGENCY_HUB` at x 24.8–27.8. So the graybox does mirror A011. **GAP-120 stands, High.**
- The naming is unaffected: HUB = 818.53 (bigger, per Nolan's "bigger side"), and HUB 2 = 541.34 is the literal "first room" off the office. The §2.1 tile→room mapping holds. REVIEW-W3B m5 is correctly resolved: the exit opens from HUB.

**Additional A011 facts for the ART fix (not in REF-007; added to §1.4, all scaled by eye at 1/4"=1', Med):**
- The **Office→HUB 2 door** sits at the east end of the office south wall (x ≈7.5–10.5), not at V5's x 4.0–5.8.
- The **west delivery door** is at y ≈49.5–52.8 (V5: 47.8–51.2).
- The A011 widths do not quite close. 18.77 + 0.41 partition + 28.27 = 47.45 ft, against the 47.19 ft V5 shell (≈3"). ART should anchor the partition from A011's 18'-9¼" and absorb the residual in HUB.

## 4. Consistency and PII — PASS
- **DEC-037** (positions from A011/current plan) is honoured: GAP-102 is closed and GAP-120 is raised from A011. **DEC-039:** untouched. **DEC-040/041:** a desk and computer in each of FOH and BOH, with the chair added by DEC-041 because none is visible, which matches §2.3.
- REF-006's HALL 35.16 finding (A011 labels the FOH–BOH vestibule HALL) is confirmed on the sheet. I annotated the §1.3 vestibule row. **V5's "HALL 35.16" by the restroom is a V5 label error**; it has no geometry impact.
- No person names, phones, emails, permit or licence numbers in the diff (grep plus read). The brand and strain names on the jar cards are not inventory data (the §2 rule).

## For the Hub
1. **Assign the ART GAP-120 fix:** mirror the HUB/HUB 2 pair. The partition goes at about x 19 from A011's 18'-9¼", with the connecting door at its north end swinging into HUB. Move the Office door to x ≈7.5–10.5 and the delivery door into HUB 2, put the SE exit at the HUB south-wall SE corner, and move the HUB/HUB 2 fixtures with their rooms.
2. DEC-041/042/043 still cite `References/Incoming/…` paths (Hub file). The new paths are in REFERENCES_INDEX §0.
3. PROC-002: adopt the published smalls size, keep the canister as a labelled estimate, use white lids.
4. Not done: I did not re-measure §2.3 fixture sizes (all Low) or §2.4 shelf spacing beyond spot reading.
