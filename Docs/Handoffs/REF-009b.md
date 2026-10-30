# REF-009b handoff — REVIEW-W4R fixes

**Status:** done on `task-ref-009b`. Changed `Docs/Reference/ROOM_FIXTURES.json` (rev4, 79 → 81 rows; still round-trips with `json.dumps(indent=1)`), `Docs/REFERENCES_INDEX.md` §7 and `Docs/KNOWN_GAPS.md`. Docs only.

## Fixes
- **m1:** new **GAP-127** for the Low placements beyond DEC-051, set as `gap: GAP-127` on 23 rows:
  - FOH: the desk/chair/fridge/cooler group order, the 4 rolling racks, and the entry props.
  - Break room: whiteboard, table and bench.
  - Office: the six DEC-051 office rows.
  - The REF-008 Q16/18/20 props (hall recessed cabinet, BOH carton shelf, LED strip).
  - Rows that already had a GAP keep it.
- **m2:** FOH `Rack_West_Wall` and `Rack_East_Wall` are restored from the pre-REF-009 file as Low rows with `pos_ft: null`, under new **GAP-128**. Their notes record the old positions and the knock-on effects: the rolling racks shift about 1 ft east if the west rack exists; the east wall now holds the DEC-051 group.
- **m3:** `Bench_Wood` x 17.4 → 17.75 (x 17.1–18.4), so it sits beside the table (x 14.55–17.05) instead of overlapping it.
- **m4:** §7.3 no longer mentions a towel dispenser; the first-aid kit is on the pilaster.
- **m5:** the GAP-121 graybox string now says "two tall black cabinets" and "a tall box NE". The file has no safe wording beyond the `_about` exclusion sentence.
- **n2:** `Fan_Portable` is back on the file cabinets (R3C3): under the standing desk on the cabinet top. Its height is cut to 1.0 ft so it clears the desk top.
- **n1 (bonus):** the electrical box's colour was dropped and its height marked Low.

## Validation
The JSON parses and round-trips. Fixture names that exist in two rooms (`Chair_Desk`, `Rack_East_Wall`) were checked: only the FOH rows changed and the BOH rows are untouched. No Unity or ART work.

## Questions for Nolan (through the Hub)
1. **FOH (GAP-128), A011 shelving strips + R4C1 west-wall rack:** are there fixed wall shelves in FOH besides the 4 rolling racks? Candidates: yes, west wall only; yes, both walls; no. Placeholder: both rows unplaced.
2. REF-009 Q1 (locker width × height and wall) and Q2 (desk/fridge/cooler order) are still open (GAP-126, GAP-127).
