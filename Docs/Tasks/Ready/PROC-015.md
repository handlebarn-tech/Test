# PROC-015: North/east-wall sales-floor anchors at the quality bar

**Priority:** P1 · **Base:** `main` · **Blender only, no Unity** · **Reviewer:** fresh; strong visual review (DEC-122).

## Goal
The sales floor's big customer-facing anchors still exist only as graybox boxes. Build them as real assets so ART-013 (and later passes) can place them from evidence: store/layout accuracy (DEC-096, PT2). ART-013 places them; this task builds them.

## Read
`Docs/REFERENCES_INDEX.md` §1.5 (sizes/positions: living wall, menu screen, merch rack, ATM, display case on the register counter), §3 (BAND photos), §8, §9 (REF-016 matrix; A011 sink position); `Docs/Reference/ROOM_FIXTURES.json` rows `Sink_HandWash`, `DisplayCase_Lit_NorthRun` (and their `matrix`); `Docs/Imports/IMP-003_PROC_FIX_CHECKLIST.md` §15 V1–V3 (display case items; the Round 2 drop `display_cases.py` under `C:/Users/handl/Downloads/Dispo Game Imports/Dispo_Game_Round2_Workstream/` may be adapted, copy never move, no `__pycache__`); DEC-023, DEC-051, DEC-071/081 (approved brand marks), DEC-084, DEC-086, DEC-097, DEC-114, DEC-122, DEC-131 (H1: ATM rules); `Docs/Assets/Specs/PROC_PIPELINE.md`; the runner/proclib under `Tools/Blender/` (use as-is).

## Owns
New `Tools/Blender/generators/sales_floor_anchors.py`, `Tools/Blender/params/sales_floor_anchors.json`, exports `Art/Exports/Procedural/PROC_SalesFloor_*` + appended manifest rows, sheets `Docs/Assets/Specs/PROC_sales_floor_anchors_*.png`, `Docs/Handoffs/PROC-015.md`. **Not** `run_generator.py`, `proclib.py`, `proctex.py` or any existing generator/params (PROC-005's fix round owns those; a helper you need goes in your generator file and is listed in the handoff for later promotion). On a manifest conflict when rebasing, regenerate your rows; never hand-merge others'.

## Deliverables
One parametric generator, one variant per anchor, sizes from RI §1.5 / ROOM_FIXTURES (cite per param; unknowns are named GAP params):
1. **Living wall** 9.2 × 1.2 ft footprint (RI §1.5): backing panel + layered foliage clusters (card or mesh), height GAP unless a photo/CCTV gives it.
2. **TFS lettering** on/near the living wall per DEC-071 (approved store mark only; geometry text, no invented logo art; if no photo shows the lettering, build a blank-plate variant and GAP the art).
3. **Rounded merch rack** 4.6 × 1.4 ft (RI §1.5), freestanding, with hook/shelf anchors (no product; stock comes from data later).
4. **Deli hand-wash sink** at the A011 size ≈1.9 × 1.6 ft (RI §1.5 / REF-016; `Sink_HandWash`), wall-hung, faucet, soap/towel dispensers as generic shapes.
5. **ATM shell** 2.2 × 1.8 ft footprint (RI §1.5): generic, unbranded, closed, blank screen, no cash-mechanism detail, no interaction (DEC-131 H1).
6. **Lit countertop display case** 1.4 × 1.4 ft footprint (RI §1.5, `DisplayCase_Lit_NorthRun`, height per that row or GAP): top glass, black body, emissive strip; collision encloses the glass (checklist §15 V1–V3). Glass is its own material slot.
- DEC-084 quality (LOD0–3, PROC finish library / 2K PBR), collision = manifest boxes (DEC-086), UV per DEC-097 as the current runner allows (lightmap ch1 is PROC-016; do not work around the runner).
- Labelled contact sheet at a readable size, plus per-anchor tiles beside their RI/CCTV/BAND evidence where one exists.

## Validation
Pipeline validation passes for every variant (mechanical checks, DEC-122). Footprints match the cited RI §1.5 / ROOM_FIXTURES sizes within 5 mm or the param is a labelled GAP. No unapproved brand marks, no cash or security hardware (DEC-051/131). Sheets readable for the visual review.

## Handoff
`Docs/Handoffs/PROC-015.md` (STUDIO_OS §57): per-anchor source table, tri figures vs DEC-084 guides, GAPs proposed under `## For the Hub`, questions only after the DEC-105 search (list what you searched). One line to the Hub.
