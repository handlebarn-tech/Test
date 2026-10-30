# PROC-013: Door family at the quality bar (playtest 2)

**Priority:** P1 · **Base:** `main` · **Blender only, no Unity** · **Reviewer:** fresh; strong visual review (DEC-122).

## Goal
Real doors for the store: PT2 #1 asks for transparent glass main storefront doors with a higher-quality asset, and PT2 #7 for a full door audit (`Docs/Design/PLAYTEST2_2026-10-30.md`). This task builds the door assets. ART-013 places them and seals the walls. It is carved out of PROC-010's architecture kit (BACKLOG).

## Read
`Docs/Reference/DOORS.json` (every door: type, size, hinge, hardware, closer/lock, defaultState, per DEC-110/115) and its `_about`; `Docs/REFERENCES_INDEX.md` §2 (CCTV), §3 (BAND photos), §6 (TI door schedule/details); DEC-023 (licences), DEC-051, DEC-084, DEC-086 (collision boxes), DEC-097 (UV channels), DEC-114, DEC-122; `Docs/Assets/Specs/PROC_PIPELINE.md`; the PROC-005 runner/proclib under `Tools/Blender/` (use as-is).

## Owns
`Tools/Blender/generators/doors.py`, `Tools/Blender/params/doors.json`, `Art/Exports/Procedural/Doors/**` + appended manifest rows, door sheets `Docs/Assets/Specs/PROC_doors_*.png`, `Docs/Handoffs/PROC-013.md`.

## Deliverables
- One parametric generator covering every door type in DOORS.json. **The storefront entry is transparent glass** in an aluminium frame, with the hardware DOORS.json records. Glass is a separate material slot so Unity can make it transparent.
- Frames/jambs sized so ART-013 can seal the wall opening: the rough-opening size is an export attribute.
- Hinge side and swing from DOORS.json, with the pivot on the hinge axis. Hardware (lever/pull/push bar/closer) is real geometry per the record. Anything DOORS.json leaves open is a labelled GAP param.
- DEC-084 quality (LOD0–3, 2K PBR or the PROC-005 finish library, real construction and wear). UV ch1 lightmap per DEC-097.
- Labelled contact sheet at a readable size, plus a per-door sheet beside its CCTV/photo evidence where one exists.

## Validation
Pipeline validation passes (mechanical checks, DEC-122). Pivots sit on hinge axes. Sizes match DOORS.json within 5 mm. The sheets are readable for the visual review.
