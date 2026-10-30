# PROC-006b — Register workstation kit: generators with per-station variation (phase 2)

**Dept:** Assets · **Role:** PROC · **Priority:** P1 (DEC-096 #5) · **Owner:** — (launch when a worker slot frees) · **Reviewer:** Unity A2 `local_4e865bb8-479c-41c5-8628-7f3e7cb2a4c3` · **Touches:** none · **Interfaces:** spec `Docs/Assets/Specs/REGISTER_KIT.md` (PROC-006); attach anchors bind to World's ROOM_FIXTURES rev7 register/operator-zone ids when REF-011 merges (until then, named anchor params with `"gap"` notes); shared with PROC-005: `Tools/Blender/` runner/proclib (use them as-is, never edit them here) and the export manifest (append rows only)

## Goal
Build the register kit props RK-01..RK-09 from the spec, plus a seeded per-station dressing arranger, so no two of the 11 register stations look the same.

## Rules
- First update the spec: replace GAP-REG-1..10 with DEC-104's answers. They are:
  - mouse on the right at every register;
  - a label printer at every register, with placement varying per station;
  - the hanging bottle is ISO cleaner, present at only some stands;
  - under-counter boxes = receipt/label paper stock (Med confidence);
  - rag blue;
  - main cleaning supplies live in restroom storage, so under-counter cleaning items are sparse;
  - receipt printer feeds out the top;
  - small bins at registers.
  
  Anything DEC-104 doesn't settle stays a labelled GAP param.
- **DEC-104 non-uniform rule:** small items vary per station in presence, placement and condition. One seed per station gives a deterministic result. Fixed items are the ones DEC-104 puts at every register: mouse (always right), keyboard, scanner, receipt printer, label printer. Everything else is optional per station, with weights. The arranger outputs one placement JSON per station.
- Quality bar DEC-084 per prop: LOD0 5–20k tris, LOD0–3, 2K PBR, real construction details and wear; unbranded is not generic. Collision is manifest boxes (DEC-086). No cash-handling equipment (DEC-051).
- Generator files `Tools/Blender/generators/register_kit.py`, `params/register_kit.json`, plus an arranger module. Headless via `Tools/Blender/blender.ps1`.
- No Unity work and no scene placement (World owns placement).
- DEC-110: measure sizes and positions from the floor plan/TI drawings, CCTV and game files before raising any question about them.
- DEC-105: before any FOR NOLAN question, search DECISIONS, KNOWN_GAPS, Handoffs/REF-008, Research and list what you searched; never re-ask anything answered or skipped.

## Deliverables
Spec updated; generators + params + arranger; FBX exports via LFS + manifest + validation JSON; a contact sheet of all props and one sheet showing 4 differently dressed stations; `Docs/Handoffs/PROC-006b.md`.

## Validation
Validation passes for every prop. Tri figures are reported against DEC-084. The arranger is deterministic (same seed gives the same JSON) and an assert-based self-test proves the fixed items are always present, the mouse is always on the right, and at least 2 stations differ in optional items.
