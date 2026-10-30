# REVIEW-W4N — REF-008 back-room CCTV mapping (docs only)

**Verdict: PASS with minors.** Branch `review/wave-4n` (off `main` 79fdfc9) merges `claude/task-ref-008-8fc507` @ 2682860. Reviewer: UX-002 workcell session, 2026-10-30.
**Merge note:** `main` no longer has `Docs/Tasks/Active/`, so the merge raised a file-location conflict for the packet. It was resolved as `Docs/Tasks/Done/REF-008.md`, as in earlier reviews. Diff = 5 text files (handoff, KNOWN_GAPS, REFERENCES_INDEX, ROOM_FIXTURES.json, packet); no images committed.

## 1. Fixtures sampled against tiles (2× crops of Camera Wall 2 + the two desk stills; crops kept in scratch only)
| # | Fixture | Tile | Result |
|---|---|---|---|
| 1 | Office `Neon_TheFlowerShop` west wall | wall2_R3C3 (green neon at the left edge, camera looking N) | ✔ |
| 2 | Office `Desk_Corner_Dual_Monitor` / `Monitors_Dual` NW | R3C3 | ✔ |
| 3 | Office `Worktable_Stainless` + `Board_North_Fabric` + `Shelves_Floating_x3` on the north wall | R3C3 (folding legs, pin board, 2–3 shelves) | ✔ |
| 4 | Office `DrumKit_Small`, `Plant_Potted` foreground | R3C3 (cymbals, plant) | ✔ |
| 5 | Office `FileCabinet_Black` + box fan, `Trash_StepCan` east | R3C3 right edge; R3C4 through the open door | ✔ |
| 6 | `Door_Hall_Office` black, leaf poster on the office face | R3C4 | ✔ |
| 7 | Hall `Door_Hall_Break` "EMPLOYEES ONLY" + fire label; `Board_Cork` with taped notices | R3C4 | ✔ |
| 8 | Break `Pilaster_Chase`, `Dispenser_PaperTowel`, `Poster_LaborLaw` | wall2_R3C5 | ✔ |
| 9 | Break counters (north run + east return, dark top), `Sink_Double`, `Fridge_Magnets` | R3C5 | ✔ |
| 10 | Break `Bench_Wood`, `Hoop_Mini`, `Hooks_Coats`, `Mats_Floor_x2` | R3C5 | ✔ |
| 11 | Break `Lockers_Staff` (grey tops, cap and orange strap) / `Door_JC` black with a note | R3C5 foreground / right | ✔ (matches DEC-047) |
| 12 | FOH `Desk_WireRack_Computer`, `Fridge_TopFreezer`, `Cooler_GlassDoor_2Door` side by side | FOH still | ✔ (wall = GAP-124, Low is honest) |
| 13 | FOH `Rack_Island_1` with bins; red/white floor tape; vestibule `Shelf_Supplies` (wood/black) + TL-2 tile through the door | FOH still | ✔ |
| 14 | BOH `Desk_ExRegister1` (keyboard + small device, Q19), `Shelf_High_Cartons` left of the black door (Q18), `Light_Strip_Pendant` | BOH still | ✔ |
No sampled fixture contradicts its tile. The 2 chat-only views (chat_office_L, chat_FOH_R) can't be re-checked; rows sourced only from them are rated Med/Low, which is fair.

## 2. JSON and positions
- Parses: 71 fixtures + 4 graybox contradictions; keys consistent. Confidence: 7 High / 32 Med / 32 Low.
- Bounds script (footprint from pos, size and rot, 0.6 ft wall tolerance, REFERENCES_INDEX §1.3 rooms, vestibule per GAP-122): **every placed fixture sits inside its room.** Two rows are `pos_ft: null`: `Lockers_Staff` (GAP-126) and FOH `Props_Floor` (scatter, no fixed place).
- Confidence labels are honest. A011-only rows are Med/Low, CCTV + A011 rows Med/High, chat-only props Low. **m2:** `Lockers_Staff` is rated High with a null position; the High is for existence (a store fact), which the notes make clear but the field doesn't.

## 3. Security and people
- The JSON lists no camera positions, alarm, access-control or safe detail. Hits for "camera"/"alarm"/"safe" are only the exclusion sentence, a "near the camera" phrase and one graybox-contradiction line. The IT rack is a plain 2×2×6 ft box ✔. The FOH still shows a small wall device beside the door; it is correctly left out.
- No images are committed; staff are described by role only ✔.
- **n1:** the GAP-121 contradiction string says the graybox has a "'safe' NE". It names a graybox object, not a real one, but a neutral word such as "the graybox's tall box at NE" would be cleaner. Optional.

## 4. Questions (DEC-047)
- 22 questions; each of Q1–Q20 gives the tile/file, what is seen, candidates and a placeholder ✔. Q21–Q22 are photo/file requests ✔. Q9 asks only what kind of cabinet, "no contents needed" ✔.
- **m1:** only 6 rows carry a `gap` id (GAP-124 ×5, GAP-126). Placeholders for Q2–Q20 ("not modelled", "box fan", "LED strip" …) have no GAP id in the JSON or KNOWN_GAPS. DEC-047 asks for GAP-labelled placeholders. Fix: one umbrella GAP (e.g. GAP-127 "REF-008 Nolan questions Q2–Q20") added to KNOWN_GAPS, with that id in each affected row's `gap` field. Not blocking.

## 5. Decisions applied
- **DEC-040/041:** FOH and BOH desks are placed from the stills, each with a `Chair_Desk` (note cites DEC-040, the chair fact) ✔.
- **DEC-047:** break-room lockers recorded and the position left null (GAP-126) instead of guessed ✔.
- **DEC-050:** `contents` on the fridge (drinks), cooler (concentrates, perishable edibles) and the four FOH racks (vapes, edibles, infused prerolls); FOH staff-only stated in `_about` and §7.6 ✔. No brand names in the new text (the one in §2.3 predates this task).

## Findings
- m1 placeholders for Q2–Q20 lack a GAP id (§4). m2 locker confidence field reads as position confidence (§2). n1 graybox "'safe'" wording (§3).
- None blocks the merge. ART can use ROOM_FIXTURES.json now; GAP-121/122/123 are the big graybox fixes for ART.
