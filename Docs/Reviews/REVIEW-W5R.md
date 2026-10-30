# REVIEW-W5R — IMP-003 delta d2975fe: DEC-086 rulings + DEC-088 real values in the PROC fix checklist

**Verdict: PASS (GO).** Branch `review/wave-5r` (off `main` 386f07e) merges `claude/brave-brattain-30c797` @ d2975fe cleanly. Only d2975fe is new (the rest merged with W5F). Docs only: `IMP-003_PROC_FIX_CHECKLIST.md` + `Handoffs/IMP-003.md`. Reviewer: standing Docs reviewer (DEC-085), 2026-10-30. Review ID = next free; the Hub may renumber.

## Against DEC-086 (Hub rulings)
- C1 collision = option (a) manifest boxes, no `COL_*` render meshes ✔. C3 validation JSON written on failure, kept as the PROC gate ✔. C4 `mesh_stats` extras as diagnostics, never gating on non-manifold ✔. R4/RC3 card terminal included as an unbranded prop ✔.
- I1: ID stand at the entrance check-in, counter never re-checks: matches DEC-086 (closes REVIEW-W5F m3) ✔. Cash drawer and EntryVestibule stay rejected (R1/RC3, exterior) ✔.

## Against DEC-088 (Nolan's answers)
- W7 FOH rolling racks: 3 shelves including the top, small wheels, 4 casters (2 per side at the ends) ✔. Caster size isn't given, so it stays GAP ✔.
- W7 BOH runs: 4-ft sections, middle ones roll, ends fixed; needs per-section `caster_enabled` ✔.
- B1 lockers 2 × 6 = 12 doors, Med: `columns 2`, `rows 6`, ≈ 0.30 × 0.30 m each in the 2.0 × 6.0 ft unit (arithmetic checks) ✔.
- D5 deli counter front: re-asked, tile front kept as a labelled placeholder ✔.
- **W8 is the right call, not a guess:** RF `Rack_East_Wall` 8.7 ft and `Rack_West_Run` 8.0 ft ("2-bay") give 2 sections and no middle one, so "2 fixed sections for now, REF to resolve" (GAP-127) is the honest placeholder ✔.

## Note for the Hub (no change needed)
- DEC-088 says it "closes GAP-PROC-13"; the checklist keeps post/wire/collar/caster/foot sizes under GAP-PROC-13 (Nolan gave counts, not component sizes). The checklist is the more accurate reading. When registering GAPs, word GAP-PROC-13 as "component sizes" so it isn't marked closed.
- W8's run-length conflict goes on the next REF pass list.

## Addendum — f2580f7 (DEC-090 deli counter front; W8 label)
**Verdict: PASS with one minor (GO).** f2580f7 is already in this branch's merge (40d2e2a: the worker's branch tip had moved to f2580f7 when `review/wave-5r` was cut), so no new merge was needed.
- **D5 matches DEC-090:** the front is plywood with a decorative wrap, and the teal/white checker is the wrap's print, Med ("a texture on the plywood front, not real tile"). No glass case is stated, so it is an optional placeholder param under GAP-PROC-14 ✔. Handoff Q5 marked answered ✔.
- **W8** relabelled "REF follow-up for the PROC worker (do not guess; Hub-confirmed open item)": same content ✔.
- **m1 (stale, fix on next delta):** checklist §Q1 (line ~283) still lists "checker-tile counter front (TL-type tile, real grout lines)" as LOD0 detail. Under DEC-090 that is a printed wrap on plywood: no grout geometry, a wrap texture, plus plywood edge/seam detail. Leaving it would have the PROC worker model real tile against D5. (Handoff line 57, "not an L with a tile front", is the historical drop-4 summary; it could say "wrap front" but needs no change.)
- **m1 closed by 45060f8** (merged here): §Q1 now reads "plywood counter front with the printed teal/white checker wrap as a texture (DEC-090/D5): plywood edge and seam detail, wrap edges and wear, no tile or grout geometry". One line changed, nothing else ✔. **Final: PASS (GO).**
