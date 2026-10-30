# PROC-013b handoff: door sheet follow-ups (closed elevation; Hall_Break closer side)

**Worker:** PROC-013b · **Reports to:** Studio Hub · **Branch:** `claude/intelligent-lumiere-b0fd09`, based on `main` @ 3adc4d1 · Blender only, no Unity. Packet: `Docs/Tasks/Active/PROC-013b.md` (written by me from the BACKLOG row and REVIEW-PROC013 m2/m4/m5, as briefed).

## Done
- **m5, closed-state elevation:** the sheet code in `doors.py` (review-sheets section only) now renders a fifth tile, `closed`: the same push-side ortho elevation with every leaf at `closedRotation` (`assemble(..., frac=0)`). The label reads `drawn CLOSED`. Every `PROC_doors_<id>.png` is now 2800 × 560: push 3/4, swing 3/4, 40 % elevation, closed elevation, evidence.
  - Entry: the closed tile shows both leaves shut, the two meeting stiles side by side with the astragal seam between them, and the back-to-back pulls at the meeting edge. It is readable at 3× zoom (dark aluminium on dark aluminium at 1×).
  - Single leaves: each leaf sits inside its jambs under the head, with the undercut visible at the floor.
  - Openings and the grille have no leaf, so their closed tile matches the elevation.
- **m4, Hall_Break closer side (GAP-DOOR-1): sources read, geometry kept.**
  - A310 set 2.0 (door 105) gives a surface closer but not its mount side (REFERENCES_INDEX §6.2, DOORS.json `audit.selfClosing`).
  - CCTV wall2 R3C4 shows the hall face of door 105 with its whole head and frame top in view, and there is no closer on it. The leaf swings into the break room, so the hall face is the push side.
  - So if the scheduled closer is installed, it is on the break-room (pull) face: a regular-arm or top-jamb mount. Confidence Med: one low-res still, and the pull face is never seen.
  - The model has a parallel-arm closer on the push (hall) face. Moving it changes the `PROC_Door_Hall_Break_Leaf` mesh (and the Frame, for a top-jamb mount) while ART-013 consumes those FBXs, so I did not move it. The new closed tile next to the evidence crop shows the mismatch by eye.
- **m2:** already done in the ART-013 packet; nothing changed.

## Validation
- `blender -b --factory-startup --python-exit-code 10 -P Tools/Blender/generators/doors.py -- sheets` exits 0 and writes 15 per-door sheets plus the contact and LOD sheets. Those two are unchanged.
- No geometry, export, manifest or params change: the diff touches only the `# --- review sheets` section of `doors.py`, `Docs/Assets/Specs/PROC_doors_*.png`, the packet and this handoff. `git diff --stat 3adc4d1 HEAD -- Art/ Tools/Blender/params/` is empty. `params/doors.json` was left alone on purpose: the runner hashes the whole file into every manifest `params_sha256`, so even a caption edit would stale 28 manifest rows.
- Visual check: I put all 15 closed tiles side by side and checked them. Every leaf is shut inside its frame. Hardware: Entry has its pulls; the exits have push bars; Hall_Restroom has its kick plate. Office_HUB2's leaf is white. The arches and the grille have no leaf. The contact and LOD sheets came out byte-identical (deterministic), so git shows no change for them.

## Not done / known limits
- The Hall_Break closer is not moved (geometry freeze, see above).
- No separate zoomed meeting-stile detail tile; the closed elevation is enough at sheet zoom.

## For the Hub
- **GAP-DOOR-1 amendment (proposed text for the closer clause):** "closer mount side: A310 105 set 2.0 gives a surface closer, side unscheduled; CCTV wall2 R3C4 shows the hall (push) face head with no closer, so the 105 closer is on the break-room (pull) face (regular-arm or top-jamb), Med. The model still has it parallel-arm on the push face (PROC-013); move it at the next door re-export. Other doors: side unknown, push-face parallel arm kept as convention."
- **Follow-up for the next door re-export (PROC-016 lightmap UV pass):** move the `Door_Hall_Break` closer to the pull face (regular arm) in `doors.py` `leaf_hm` (`closer(..., face_y(..., -1, 0), -sw, ...)` → the pull face for this door, via a per-door params flag), then regenerate. The leaf mesh and FBX hash change; names and pivots do not.
- FOR NOLAN: nothing.
