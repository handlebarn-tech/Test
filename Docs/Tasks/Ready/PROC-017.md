# PROC-017: Entry and queue kit (ID-check stand, queue stanchions, kraft exit bag)

**Priority:** P1 · **Base:** `main` · **Blender only, no Unity** · **Reviewer:** fresh; strong visual review (DEC-122). Carved out of PROC-010 (checklist §20, R3b.3, R5.3), like PROC-013.

## Goal
GAME-026 makes customers enter through the guard's ID check, wait in one line and get called (DEC-103/109). The props that flow happens around are still graybox boxes. Build them at the quality bar so ART-013 / NPC-001 can place them: believable customer flow (DEC-096).

## Read
`Docs/Reference/ROOM_FIXTURES.json` rows `IDCheck_Stand`, `IDCheck_Scanner`, `Queue_Stanchions` (+ `matrix`); `Docs/REFERENCES_INDEX.md` §1.5 (queue lanes), §3 (BAND 05 bags), §9 (REF-016: entry and ID stand per A011); `Docs/Imports/IMP-003_PROC_FIX_CHECKLIST.md` §20 I1, R3b.3, R5.3 "Exit bag"; the drops to adapt (copy, never move; no `__pycache__`): `C:/Users/handl/Downloads/Dispo Game Imports/Dispo_Game_Round2_Workstream/Tools/Blender/generators/id_check_stand.py` (+ params), `.../Dispo_Game_Blender_PROC_Round3_Rebuild/Tools/Blender/generators/queue_stanchions.py` (+ params), `.../Dispo_Game_Blender_PROC_Round5_HQ/Tools/Blender/generators/deli_supplies.py` (exit bag only); DEC-023, DEC-043, DEC-051, DEC-071, DEC-079, DEC-084, DEC-086, DEC-097, DEC-109, DEC-114, DEC-122; `Docs/Assets/Specs/PROC_PIPELINE.md`; runner/proclib under `Tools/Blender/` (use as-is).

## Owns
New `Tools/Blender/generators/entry_queue_kit.py`, `Tools/Blender/params/entry_queue_kit.json`, exports `Art/Exports/Procedural/PROC_Entry_*` + appended manifest rows, sheets `Docs/Assets/Specs/PROC_entry_queue_kit_*.png`, `Docs/Handoffs/PROC-017.md`. **Not** `run_generator.py`, `proclib.py`, `proctex.py` or existing generators/params (PROC-005's fix round owns them; helpers go in your file and are listed in the handoff). On a manifest conflict when rebasing, regenerate your rows.

## Deliverables
1. **ID-check stand** (`IDCheck_Stand` 2.0 × 1.5 × 3.5 ft, Low) with the guard's ID scanner as a generic device (`IDCheck_Scanner` 0.5 × 0.4 × 0.3 ft): fix I1 (declared height includes the scanner, or the scanner is excluded from the expected size). Scanner green-light as an emissive material slot GAME-026 can drive. No security-camera or alarm detail (DEC-051).
2. **Queue stanchions:** post 3.0 ft (0.914 m), weighted lathe base with rubber ring, cassette head with end clip and receiver slot, belt webbing texture; black (R3b.3). Post + belt segment as separate parts so lanes are assembled in Unity (no layout baked in; lane sizes in RI §1.5 / `Queue_Stanchions` are placement data for ART-013, cite them in the sheet).
3. **Kraft paper exit bag** (R5.3; DEC-043 "branded paper bags", BAND 05): open and folded states; TFS print only as an approved mark (DEC-071) or blank + GAP. Size GAP (RG5-2/RG5-3) unless a source gives it.
- DEC-084 quality (LOD0–3), manifest collision boxes (DEC-086), UV per DEC-097 as the current runner allows (lightmap ch1 is PROC-016).
- Labelled contact sheet plus per-item tiles beside their CCTV/BAND evidence where one exists.

## Validation
Pipeline validation passes for every variant (DEC-122). Sizes match the cited ROOM_FIXTURES/checklist values within 5 mm or are labelled GAP params. Sheets readable for the visual review.

## Handoff
`Docs/Handoffs/PROC-017.md` (STUDIO_OS §57): source table per item, tri figures vs DEC-084, GAPs under `## For the Hub`, questions only after the DEC-105 search. One line to the Hub.
