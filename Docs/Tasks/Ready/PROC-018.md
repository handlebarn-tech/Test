# PROC-018: HUB 2 storage cabinets + deli refill station (prep cart, canister shelf)

**Priority:** P1 · **Base:** `main` · **Blender only, no Unity** · **Reviewer:** fresh; strong visual review (DEC-122). Carved out of PROC-010 (checklist R3b.1, R3b.2).

## Goal
Playtest 1 asked for an accurate HUB and office (DEC-096). Two sourced fixture groups there are still boxes: the black cabinets on the HUB 2 office wall and the deli refill station in the office (DEC-079). Build them at the quality bar; ART-009 (manager refill, PS2) and later dressing passes place them.

## Read
`Docs/Reference/ROOM_FIXTURES.json` rows `Cabinets_Storage_OfficeWall` (HUB2), `Cart_Deli_Prep`, `Shelf_Deli_Canisters` (Office) (+ `matrix`); `Docs/REFERENCES_INDEX.md` §2.1 (HUB 2 R1C1/R2C1 black cabinets), §2.4 (prep cart, canister shelf, refill scale), §8.2; `Docs/Imports/IMP-003_PROC_FIX_CHECKLIST.md` R3b.1 and R3b.2 (every bullet, including the lead ruling Q6: plain closed cabinets, no interior); drops to adapt (copy, never move; no `__pycache__`): `C:/Users/handl/Downloads/Dispo Game Imports/Dispo_Game_Blender_PROC_Round3_Rebuild/Tools/Blender/generators/hub_storage.py`, `refill_station.py` (+ params); DEC-023, DEC-042, DEC-043, DEC-079, DEC-084, DEC-086, DEC-097, DEC-114, DEC-122; GAP-110, GAP-132 in `Docs/KNOWN_GAPS.md`; `Docs/Assets/Specs/PROC_PIPELINE.md`; runner/proclib under `Tools/Blender/` (use as-is).

## Owns
New `Tools/Blender/generators/hub_storage.py`, `refill_station.py`, `Tools/Blender/params/hub_storage.json`, `refill_station.json`, exports `Art/Exports/Procedural/PROC_HUB2_Cabinet*`, `PROC_Office_DeliPrepCart*`, `PROC_Office_DeliCanisterShelf*` + appended manifest rows, sheets `Docs/Assets/Specs/PROC_hub_storage_*.png`, `PROC_refill_station_*.png`, `Docs/Handoffs/PROC-018.md`. **Not** `run_generator.py`, `proclib.py`, `proctex.py` or other existing generators/params (PROC-005's fix round owns them). On a manifest conflict when rebasing, regenerate your rows.

## Deliverables
1. **HUB 2 cabinets** per R3b.2: two black closed cabinets 3.0 × 1.5 × 7.0 ft each (6.0 × 1.5 ft row, `Cabinets_Storage_OfficeWall`), no shelves, stock anchors or opening doors; exterior detail only (folded edges, reveal lines, plinth/feet, seeded wear). Evidence/GAP text as R3b.2 says (presence sourced; type/size GAP-110/132).
2. **Deli prep cart** per R3b.1: 2.5 × 1.6 × 2.9 ft, stainless, 2 levels, push handle, casters touching the legs, "FOR DELI USE ONLY" rail label (RI §2.4 store text), spray bottles on the rail, distinct supplies under it (isopropyl bottle, rags, scraper, bins, tongs).
3. **Canister shelf** per R3b.1: 3.5 × 0.9 ft wood board on black brackets, top ≈1.46 m AFF, anchors for ~5 empty canisters.
4. **Refill scale** per R3b.1 "Scale" bullets (light grey body ≈0.17 × 0.20 × 0.08 m Low, 0.2032 m glass bowl with closed bottom and wall thickness, LCD + keys + chrome scoop); blue LCD as an emissive slot.
- DEC-084 quality (LOD0–3), manifest collision boxes (DEC-086), UV per DEC-097 as the current runner allows (lightmap ch1 is PROC-016).
- Labelled contact sheets plus tiles beside the HUB 2 / office CCTV evidence.

## Validation
Pipeline validation passes for every variant (DEC-122). Sizes match the cited rows/checklist within 5 mm or are labelled GAP params. Every R3b.1/R3b.2 checklist bullet is done or deferred with a reason in the handoff (do not edit the checklist file; PROC-005 owns it). Sheets readable.

## Handoff
`Docs/Handoffs/PROC-018.md` (STUDIO_OS §57): bullet-by-bullet R3b.1/R3b.2 status, tri figures, GAPs under `## For the Hub`, questions only after the DEC-105 search. One line to the Hub.
