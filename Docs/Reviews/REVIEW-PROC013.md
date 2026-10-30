# REVIEW-PROC013: door family (glass storefront + every DOORS.json door)

- **Re-checked against:** `main` @ 1404e5c (REF-016 merged, DOORS.json rev4): verdict unchanged.
- **Reviewed:** `claude/nervous-williams-4af82b` @ 8226128 · **merge base:** `main` @ 751b85a
- **Reviewer:** fresh session (STUDIO_OS §0.3/§0.7), strong visual review (DEC-122)
- **Sources read:** packet `Docs/Tasks/Active/PROC-013.md`; the diff (77 files); handoff Validation and Not-done; `Docs/Reference/DOORS.json` (all 15 rows); `Tools/Blender/params/doors.json` `_src` fields; DEC-097, DEC-122; KNOWN_GAPS (GAP-104/137/138); every `PROC_doors_*.png` sheet (contact sheet, Entry and Hall_Break sheets in detail, with their evidence crops).

## Verdict: PASS with minors

## Checks
| Check | Result |
|---|---|
| DEC-047: every construction value sourced or GAP | Pass. Each params family has a `_src` naming its TI/REFERENCES_INDEX source or a GAP-DOOR-n id; door facts are read live from DOORS.json, not copied. Finishes each carry a `src`. |
| Coverage | 15/15 DOORS.json rows → 28 assets (1 storefront pair = Frame+LeafL+LeafR, 11 swing = Frame+Leaf, 2 arches, 1 grille). |
| Pipeline validation (DEC-122 mechanical) | 28/28 `Validation/PROC_Door_*.json` show `"passed": true`, `errors: []`. Only warnings: LOD0 below the 5000 tri guide on leaves (DEC-114: guide only). Not re-run by me; I read the committed results. |
| Sizes vs DOORS.json (±5 mm) | Manifest `leaf_size_m`: 0.9144 × 2.1336 m for 3'-0" × 7'-0" leaves, JC 0.81382 m = 2.67 ft. Exact. Arch RO 0.946 m wide over a 3'-0" (0.914 m) clear opening plus lining. |
| Pivots / hinge / swing | Leaf origin = hinge axis at floor; `closedRotation`/`openAngle` copied from DOORS.json per leaf. Checked Entry by hand: L hinge frame-local x −0.917, R +0.917, L swing +Z, R swing −Z in its own local (= frame +Z after its 180° yaw), so both leaves swing out to the same side, as DOORS.json says. Vest_FOH (+90) and JC/Hall_Break (−90) swing sides match the sign convention in DOORS.json `_about`. |
| Glass storefront (PT2 #1) | Separate slot `M_Proc_Door_Glass_GL1`, listed in `transparent_slots`; reads transparent in the EEVEE sheets. Dark aluminium stiles/rails, butt hinges, back-to-back vertical pulls at 42 in (A310 3'-6"). Matches the CCTV wall 2 R2C1 crop (dark-framed glass pair under an exit sign). |
| Hardware per record | pushBar on Emergency_RetailE, Ext_Delivery, Ext_Emergency_SE; lever on the rest; storefrontPull on Entry; closer drawn on `selfClosing` true doors and as GAP-138 placeholder on `unknown`; kick plate on Hall_Restroom (A310 103). Matches DOORS.json. |
| Rough opening for ART-013 | `rough_opening_m`, `soffit_opening_m`, `wall_t_graybox_m`, `hinge_pivots_unity_xyz`, `yaw_deg` present on every Frame row. |
| Re-check vs `main` @ 1404e5c (REF-016 DOORS.json rev4) | Pass. No change to any field the generator reads (type, leaves, leaf size, hinge_jamb, swing, closedRotation, openAngle, leafObjects, hardware, selfClosing, lock, defaultState, graybox_wall, gap); graybox_layout.json unchanged. New fields: `implemented` (scene state, ART-013's job), and for Emergency_RetailE `rough_opening` y 21.38-24.72 = 3.34 ft = 1.018 m with 2 in HM jambs (A011) and `wall_recess`. PROC-013's Emergency_RetailE RO width is 1.022 m: 4.3 mm over, inside the 5 mm tolerance, and same 2 in jamb. The recess is placement for ART-013, not door geometry. |
| Manifest | 13 369 lines added, 0 removed: append-only. |
| Sheets readable | Contact sheet 2800×1680 and per-door sheets are labelled with type, size, RO, hinge, swing, hardware, closer, lock, defaultState, GAPs. Readable. |
| Visual fidelity | Hall_Break: black leaf/frame and lever side (hinge left from the push side) match CCTV wall2 R3C4. SE door green matches hub_R1C4 (Low). Office_HUB2 white leaf per ROOM_FIXTURES. Arches: rounded white lining matches BAND 06. |

## MAJOR
None.

## minor
1. **UV ch1 lightmap (DEC-097) not delivered.** It is a packet deliverable. The worker correctly reports it needs `proclib.finish_object` and the runner, both outside Owns; DEC-097 assigns the exporter change to the pipeline. Route: a pipeline task that adds UV ch1 and re-exports every PROC family, doors included. ART-013 lightmapping depends on it.
2. **Export path differs from Owns.** Files are at `Art/Exports/Procedural/PROC_Door_*` (runner-hard-coded `EXPORT_DIR`), not `Art/Exports/Procedural/Doors/**`. Harmless, but the PROC-013 and ART-013 packets should be amended to the real path (or the runner gets an `export_dir` param in the same pipeline task).
3. **GAP-DOOR-1..9 are cited but not yet in `KNOWN_GAPS.md`.** The integrator must register them at merge, or the GAP labels in params/manifest point at nothing (DEC-047).
4. **Hall_Break closer side vs its still.** The model mounts a parallel-arm closer on the push (hall) face. CCTV wall2 R3C4, which shows the hall face, has no closer visible at the head. Closer mount side is a convention (GAP-DOOR-1), so either note it in GAP-DOOR-1 or move the closer to the pull side when the materials/hardware pass revisits it.
5. **Sheets show only the 40 %-open state.** The "elevation" tile is drawn with the leaf open, so the Entry pair shows a wide centre gap and no closed meeting-stile/astragal view. A closed elevation would make the closed fit reviewable by eye. Readability only; the generator's own closed-fit self-check passes.
6. **LOD0 leaf tris 2.9k–3.6k** trip the DEC-084 5000 guide warning. Accepted under DEC-114 (guide, not a floor); noted for the record.
