# REF-009b handoff — REVIEW-W4R fixes

**Status:** done on `task-ref-009b`. Changed `Docs/Reference/ROOM_FIXTURES.json` (rev5, 79 → 86 rows; still round-trips with `json.dumps(indent=1)`), `Docs/REFERENCES_INDEX.md` §7 and `Docs/KNOWN_GAPS.md`. Docs only.

## Fixes
- **m1:** new **GAP-127** for the Low placements beyond DEC-051, set as `gap: GAP-127` on 23 rows:
  - FOH: the desk/chair/fridge/cooler group order, the 4 rolling racks, and the entry props.
  - Break room: whiteboard, table and bench.
  - Office: the six DEC-051 office rows.
  - The REF-008 Q16/18/20 props (hall recessed cabinet, BOH carton shelf, LED strip).
  - Rows that already had a GAP keep it.
- **m2:** answered by DEC-062: the 4 rolling racks are the only FOH product racks, so the wall racks stay removed (no GAP-128). The rack length is noted as Low, sized from the room and photos.
- **m3:** `Bench_Wood` x 17.4 → 17.75 (x 17.1–18.4), so it sits beside the table (x 14.55–17.05) instead of overlapping it.
- **m4:** §7.3 no longer mentions a towel dispenser; the first-aid kit is on the pilaster.
- **m5:** the GAP-121 graybox string now says "two tall black cabinets" and "a tall box NE". The file has no safe wording beyond the `_about` exclusion sentence.
- **n2:** `Fan_Portable` is back on the file cabinets (R3C3): under the standing desk on the cabinet top. Its height is cut to 1.0 ft so it clears the desk top.
- **n1 (bonus):** the electrical box's colour was dropped and its height marked Low.

## DEC-062 addendum (main merged in, 48bcb25)
- **FOH:** new `Ladder_FireEscape` (black) in the NE corner of the shared wall, then desk, fridge, cooler, re-spaced at y 34.3–45.7. The NE end follows from R4C1 looking south (cooler right of fridge), so the group rows no longer carry GAP-127.
- **Hall:** `WallCabinet_Recessed` → `Panel_Blank`, a plain blank panel. It is security hardware, so no detail is modelled (DEC-006/031); the exclusion is added to `_about`.
- **Break room / JC:**
  - New `Board_Bulletin_West` on the hallway (west) wall, between the hall door and the whiteboard.
  - The JC gets `Mops_Brooms_JC` and `Rack_CleaningSupplies_JC` beside the A011 mop sink.
- **Restroom:**
  - Toilet, sink, mirror and towel-dispenser notes are updated to Nolan's layout.
  - New `ToolChest_Black` between the sink and the toilet, kept below the grab bar.
  - New `Cabinet_Storage_Large`, unplaced under GAP-109 (see Q2).
- **BOH:** `Shelf_High_Cartons` → `Rack_Chrome_Cartons`, contents drink cartons and misc boxes, no brand. New `Scanner_Barcode` on the ex-register-1 desk (closes REF-008 Q19).
- **Gaps:** GAP-127 is reworded to the remaining placeholders (22 rows), GAP-128 is dropped, and GAP-109 now records that no photos are available. REF-008 Q16/18/19/21/22 are closed; Q4, Q17 and Q20 stay open.

## Validation
The JSON parses and round-trips. Fixture names that exist in two rooms (`Chair_Desk`, `Rack_East_Wall`) were checked: only the FOH rows changed and the BOH rows are untouched. No Unity or ART work.

## Questions for Nolan (through the Hub)
1. **Break room, DEC-062 bulletin board:** is it the same board as the wood-framed corkboard on the hall side of that wall (`Board_Cork`, R3C4)? Candidates: same board (then drop `Board_Bulletin_West`); a second board inside the break room. Placeholder: both kept.
2. **Restroom, DEC-062 "the back wall is one large storage cabinet":** which wall is that? The west wall facing the door already holds the sink, chest and toilet. Candidates: the north wall east of the toilet; above the west-wall fixtures; the wall behind you as you enter. Placeholder: unplaced (GAP-109).
3. Still open from REF-009: locker width × height and wall (GAP-126).
