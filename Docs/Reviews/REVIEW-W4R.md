# REVIEW-W4R — REF-009 DEC-051 answers applied to back-room fixtures (docs only)

**Verdict: PASS with minors.** Branch `review/wave-4r` (off `main` 6000433) merges `task-ref-009` @ d3f3a02. Reviewer: UX-002 workcell session, 2026-10-30.
**Merge note:** one content conflict in `KNOWN_GAPS.md` (main added the GAP-DP-01/02 rows next to GAP-126). Resolved by keeping REF-009's narrowed GAP-126 and both GAP-DP rows (merge commit 9c19b8f).

## 1. JSON validity and format
- Parses; 79 fixtures (71 − 10 removed + 18 added), version "rev3". The file round-trips byte-for-byte through `json.dumps(indent=1)`, so the format matches rev2. Row keys are unchanged (base set ± `gap` / `contents`).
- Bounds script (same as REVIEW-W4N, REFERENCES_INDEX §1.3 rooms + A011 vestibule): every placed fixture is inside its room, and no FOH fixture overlaps the vestibule.
- Overlaps among new/moved rows: stacked items (machines on the worktable; cabinets, IT box, computer, fan on the standing desk; first-aid kit on the pilaster) are intentional. Two are not, see m3 / n2.

## 2. Each change against DEC-051
| Q | DEC-051 | REF-009 | OK |
|---|---|---|---|
| Q1 | FOH computer rack, fridge, cooler on the wall shared with BOH | the three moved to the east wall, rot 90, faces W; Med; GAP-124 closed | ✔ (order along the wall is an inference: Low + handoff Q2; see m1) |
| Q2 | straight ahead: small rack of deli bags, exit bags, misc tools, vape batteries; right: aluminium trash (props door) + electrical box; left: product racks start | entry heads west from the vestibule door, so straight = west wall (`Rack_Bags_Tools`), right = north (`Trash_Aluminium`, `ElectricalBox_Wall`), left = south (racks) | ✔ geometry consistent. "grey" and "~4–7 ft AFF" on the electrical box are not in DEC-051 (Low; n1) |
| Q3 | 4 product racks on rollers, slide forward/back | `Rack_Rolling_1–4`, DEC-050 contents kept | ✔ count. Removing the A011/R4C1 wall racks is an inference (m2) |
| Q4 | Nolan doesn't know | vestibule placeholder kept, GAP-122 | ✔ |
| Q5 | one locker unit ≈ 2 × 6 ft | 2 × 1.5 × 6 ft, position null, GAP-126 narrowed; the w/h reading is flagged as a question | ✔ |
| Q6 | west-wall frame is a whiteboard | `Whiteboard_West`, content not recorded | ✔ |
| Q7 | lunch table against the whiteboard wall; bench longer than the table, doesn't fit under | `Table_Lunch` 4 ft vs bench 5 ft, bench on the table's east side | ✔ wording; footprints overlap (m3) |
| Q8 | wall box is a first-aid kit | `Dispenser_PaperTowel` → `FirstAid_Kit` | ✔ (index text stale, m4) |
| Q9 | plain tall black cabinets | `Cabinet_Tall_Black_A/B`, "closed box, no interior, no hardware detail" | ✔ (no "secure storage" wording anywhere) |
| Q10 | generic desktop machines incl. a laminator | `Machines_Desktop` on the worktable | ✔ |
| Q11 | skipped | `DrumKit_Small` placeholder unchanged | ✔ |
| Q12 | portable fan | `Fan_Portable`; but drawn on top of the IT box at 6.5 ft AFF, where R3C3 shows it on the file cabinets | ✔ identity; placement n2 |
| Q13 | several file cabinets under a standing desk used as a shelf; rack and computer above | `Desk_Standing_East` + `FileCabinets_UnderDesk` + `Computer_Desktop` + `Rack_IT_Box` (now 3 ft tall, on the desk) | ✔ |
| Q14 | black bar is part of the door | no fixture | ✔ |
| Q15 | IT rack, plain box | `Rack_IT_Box` plain black box | ✔ |

## 3. PII and security (DEC-006/031/045/051)
- Added lines contain no safe types or positions, cash-handling equipment or camera-system hosting. The only hits for safe/cash/camera are the exclusion sentences (`_about`, REFERENCES_INDEX §7 intro, handoff). `Computer_Desktop` is generic, with "screen content not recorded". No people and no images. ✔
- **m5 (carried from REVIEW-W4N n1, now sharper):** the GAP-121 graybox-contradiction string still says "the steel cabinets on the SOUTH wall" (renamed rows) and "graybox has … 'safe' NE". It names a graybox object, not a real one. But with DEC-051 sanitising this exact topic, reword it to "two tall black cabinets" and "a tall box NE" so the file has no safe wording at all.

## Findings (none blocking)
- **m1 — inferences without a GAP id:** the desk → fridge → cooler order (Low, handoff Q2) and the other Low placements beyond DEC-051 carry no GAP id. The Hub asked for "beyond DEC-051 = labelled placeholder + GAP". Fix: one GAP (e.g. GAP-127 "REF-008/009 placement placeholders: FOH group order, rolling-rack spans, FOH entry props, bench/table layout, REF-008 Q16–20") in KNOWN_GAPS, with its id in those rows' `gap` field. This also closes REVIEW-W4N m1.
- **m2 — wall racks removed:** REF-009 drops `Rack_West_Wall` (A011 + R4C1, was Med) and `Rack_East_Wall` (A011), saying the 4 rolling racks replace "the A011 wall strips". DEC-051 gives the rack count but doesn't say there are no wall racks. Add a question for Nolan ("are there fixed wall shelves in FOH besides the 4 rolling racks?") and keep the old rows under the new GAP, or note why R4C1's west-wall rack is one of the four.
- **m3 — table/bench overlap:** `Table_Lunch` (x 14.55–17.05) and `Bench_Wood` (x 16.75–18.05) overlap 0.3 ft along y 38.5–42.5. DEC-051 says the bench is beside the table, not under it. Move the bench x to ≥ 17.7.
- **m4 — stale index text:** REFERENCES_INDEX §7.3 still says "Plain north wall west of it (poster, towel dispenser)"; the dispenser is now the first-aid kit on the pilaster.
- **m5:** graybox-contradiction wording (§3).
- **n1:** `ElectricalBox_Wall` "grey" and its height are not in DEC-051; mark them Low in the note or drop the colour.
- **n2:** `Fan_Portable` sits at the same x/y as the IT box, stacked on it at 6.5 ft; R3C3 shows it on the file cabinets. Put it on the desk top beside the box.
- **n3:** `Trash_Aluminium` and `ElectricalBox_Wall` footprints touch (0.05 ft); harmless, since the box is wall-mounted above.

ROOM_FIXTURES rev3 is usable by ART now; m2 and m3 are the two to fix before the FOH and break-room build.
