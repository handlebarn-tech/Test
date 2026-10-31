# PROC-013b: door sheet follow-ups (closed elevation tile; Hall_Break closer side)

**Priority:** P3 · **Base:** `main` · **Blender only, no Unity** · **Reviewer:** fresh; strong visual review (DEC-122). Follow-up to PROC-013 (REVIEW-PROC013 m2/m4/m5, BACKLOG `PROC-013b` row).

## Goal
Make the closed fit of every door reviewable by eye, and settle the Hall_Break closer mount side as far as sources allow, **without changing door geometry or FBX names** (ART-013 is consuming `Art/Exports/Procedural/PROC_Door_*.fbx` now).

## Read
`Docs/Reviews/REVIEW-PROC013.md` (m2, m4, m5); `Docs/Handoffs/PROC-013.md`; `Docs/Reference/DOORS.json` row `Hall_Break`; `Docs/REFERENCES_INDEX.md` §6.2 (A310 set 2.0 for 105); `Docs/KNOWN_GAPS.md` GAP-DOOR-1; `References/Index/cctv/wall2_R3C4.jpg`; DEC-047, DEC-122.

## Owns
Sheet code in `Tools/Blender/generators/doors.py` (the `# --- review sheets` section only), sheet-only fields in `Tools/Blender/params/doors.json`, `Docs/Assets/Specs/PROC_doors_*.png`, `Artifacts/Renders/Doors/**`, this packet, `Docs/Handoffs/PROC-013b.md`. **Not** the geometry builders, exports, manifest, `run_generator.py`, `proclib.py`, `KNOWN_GAPS.md` (propose GAP text in the handoff).

## Deliverables
1. **Closed-state elevation tile** on every per-door sheet (`PROC_doors_<id>.png`): ortho elevation from the push side with every leaf at `closedRotation` (0 % open), so the Entry pair's meeting stiles and astragal and every leaf's fit in its frame can be checked by eye. Labelled "closed".
2. **Hall_Break closer side (m4 / GAP-DOOR-1):** read the sources; if they settle the mount side, cite them; otherwise keep the GAP. Any move of the closer is a geometry change and goes to a later re-export (PROC-016), not this task.
3. m2 (export path) is already done in the ART-013 packet: no change.

## Validation
- `doors.py -- sheets` exits 0 and writes all 15 per-door sheets plus the contact and LOD sheets.
- FBX/manifest unchanged: `git diff --stat main -- Art/ Docs/Assets/Specs/*manifest*` empty.
- Visual check of every per-door sheet: the closed tile shows each leaf shut inside its frame; Entry shows the meeting stile pair and astragal.

## Handoff
`Docs/Handoffs/PROC-013b.md` (STUDIO_OS §57). One line to the Hub.
