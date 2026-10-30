# REVIEW-W2D — REF-002 (HUB CCTV + register scale stand)

**Verdict: GO (with notes).** Branch `review/wave-2d` = `main` + `--no-ff` merge of `claude/task-ref-002-77ac90` + this review + GAP-110 edit.
Method: independent visual read. HUB-wall crops placed side by side with the matching `cctv/wall2_*` crops; stand evidence read in wall2 R2C3/R2C4/R3C2 and BAND 07/10. No people identified; only fixtures were read.

## 1. Tile identity — PASS
All 7 claimed pairs are the same camera (same pose, same objects, minor time/crop change): HUB R1C1=R5C1, R1C2=R4C3, R1C3=R4C4, R2C1=R5C2, R2C2=R5C3, R2C3=R5C4, R2C4=R5C5. HUB R1C4 (desk + chair, green door) has no main-wall match → new view. HUB R2C4 repeats R2C1 (and so R5C5 repeats R5C2, as REF-001 already noted). Confirmed.

## 2. Room assignment (left column = HUB 2, rest = HUB) — PASS, Med is right
- "Left two pictures" = left column: R1C1 and R2C1 are one cluttered room (copier, yellow-lid totes, work table, gray square tile); R1C2 is clearly the orange-post rack room, so the left column is the only reading that gives "two pictures of one room". Agree.
- "The rest are in the bigger side" = the rack room = HUB (818.53 vs 541.34 SF). The rack room spans 6 tiles/5 distinct views and holds the desk + keyboard + office chair (plan HUB "desks + computers"). Extra support found in review: the green logo door in R1C4 has an **EXIT sign** above it, consistent with HUB's "deliveries" door to the outside.
- Tension to keep visible: by plan circulation the room you physically enter *first* is HUB (HUB 2 is only reached through HUB), so "first room" read literally would point the other way. "Bigger side" is the explicit, size-based phrase and wins; REF-002 already reads "first" as listing order and asks Nolan to confirm. Med stands; not a blocker for ART-002 graybox.
- Minor counter-cue: the copier room also has a work table, which could be read as a "desk" area. The R1C4 desk with keyboard + chair is the stronger match.
- R1C1's far doorway shows a wood counter and shelving with black bags — not a contradiction (HUB has a long bench and back-wall shelving in R1C4), but not proof either.
- Reversal of REF-001 is correctly propagated: §2 rows R4C3–R5C5, §4 coverage, GAP-105, and DEC-024 all agree (HUB 2 = R5C1/R5C2/R5C5).

## 3. Register scale stand — PASS (size Low, as stated)
- R2C3: chrome wire stands with scales at the staff side of the counter, centre and centre-right, open wire shelves below with small items; clear box on the counter at centre-right. Seen.
- R2C4: stands below counter level beside the POS monitors (centre, left). Seen.
- R3C2: scales at the foreground counter on both sides of the lit display case; the stand frames are hard to separate from the counter at this angle — weakest of the four, but consistent.
- BAND 10 (rotated): chrome wire stand with scales, spray bottle on a lower shelf, black trash bin beside. Clearly seen.
- BAND 07: scale with round metal pan and clear round draft shield (lower right). Seen. Note this is the scale's own shield; the counter-top acrylic box in R2C3 is a separate item — REF-002's open question to Nolan is the right handling.
- Size: ≈1.5 × 1.5 ft fits — each stand is narrower than the 3.0 ft register pendant pitch (§5) and about one POS monitor wide. Common chrome-wire carts are 18×18 or 18×24 in; keep **Low** and let ART use 1.5 × 1.5 ft.

## 4. Fixture spot-check (6+ of 19) — PASS
| Row | Cited tile | Result |
|---|---|---|
| HUB central island ≈4×3 bays | R1C3 | 4 bays across clearly; depth 2–3 — fine at count Low |
| HUB desk + office chair | R1C4 | yes (keyboard, black chair) |
| HUB rolling carts blue + red | R1C4 | yes |
| HUB yellow tote stack + hand truck | R2C2 | yes (wheels visible) |
| HUB orange posts; black door + yellow sign | R1C2 | yes |
| HUB 2 copier; stack of 4 yellow-lid totes | R1C1 | yes, exactly 4 |
| HUB 2 work table, patterned front; black cabinets | R2C1 | yes |
| HUB 2 wire merch rack with green panel | R1C1 | yes |
No overclaims found.

## 5. KNOWN_GAPS — PASS
GAP-105 closed with a correct residual (poses/doors); GAP-107 consistent with §2.2. GAP-110 updated here to "CCTV only, Med" per Hub request.

## 6. PII / files — PASS
Crops 40–52 KB, source webp 314 KB (all ≤1 MB). Text describes fixtures only; no names, faces or traits of people.

## Notes for the Hub (non-blocking)
1. `Docs/DECISIONS.md` DEC-022 still cites `References/Incoming/hub_cctv_nolan_2026-10-29.webp`; the file is now `References/CCTV HUB Wall 2026-10-29.webp`. Hub-owned file — fix when DEC-024 drops "pending REVIEW-W2D".
2. DEC-024 can be finalised: REVIEW-W2D GO.
3. Owner questions from REF-002 remain the right ones (HUB 2 confirm; shield type/stand photo; which door is which).
