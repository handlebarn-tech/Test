# REF-009b — REVIEW-W4R minor fixes (docs)

**Role:** REF · **Branch:** worktree/branch off `main` (REF-009 merged in 71b48cb)

Fix `Docs/Reviews/REVIEW-W4R.md` m1–m5 in `Docs/Reference/ROOM_FIXTURES.json`, `Docs/REFERENCES_INDEX.md` §7 and `Docs/KNOWN_GAPS.md`:
- m1 one GAP id (next free, e.g. GAP-127) for the Low inferences beyond DEC-051 (desk→fridge→cooler order etc.), referenced from those rows.
- m2 restore the removed FOH wall racks as Low rows with a GAP + a question for Nolan (are there wall racks besides the 4 rolling racks?).
- m3 bench x ≥ 17.7 (beside the table). m4 stale §7.3 text (dispenser → first-aid kit). m5 GAP-121 string.
- n2 fan on the file cabinets.
No invented facts; JSON format unchanged (round-trips with `json.dumps(indent=1)`). Owns only those three files + `Docs/Handoffs/REF-009b.md`. ≤15-line summary for the Hub.
