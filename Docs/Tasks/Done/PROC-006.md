# PROC-006 — Register workstation kit: evidence spec (phase 1 of 2)

**Dept:** Assets · **Role:** PROC/REF research · **Priority:** P1 (DEC-096 #5) · **Owner:** Assets lead subagent, worktree off `main` · **Reviewer:** Docs reviewer from the pool · **Touches:** none (reads World's files only) · **Interfaces:** consumes `Docs/Reference/ROOM_FIXTURES.json` + `Docs/REFERENCES_INDEX.md` (World); produces the spec that the phase-2 generator task builds from

## Goal
Nolan's playtest 1 (`C:/Users/handl/Downloads/Dispo Game Imports/GameFeedback10-30.txt`, "Register / Workstation Detail"; DEC-096): every register gets a label printer, receipt printer, barcode scanner, mouse, keyboard, under-counter storage (bags, boxes, personal items, cleaning supplies), a spray bottle hanging from a scale shelf, a rag. Write the evidence spec for these props so a generator task can build them without guessing.

## Rules
- Facts only from our references: REFERENCES_INDEX (and the photos/video stills it indexes), ROOM_FIXTURES, store TI docs, DEC entries. For each item record what the evidence shows (type, colour, approx size, placement, count per register) with the source (file + tile/crop).
- Where the evidence does not show it, mark `GAP-REG-<n>` and give best candidates; never invent a model or size. Generic, unbranded hardware unless a DEC approves a mark. No cash-handling equipment (DEC-051), no cameras/security hardware.
- Do not specify counter/register geometry: World is re-auditing the register layout (DEC-096 #2). Reference ROOM_FIXTURES ids only.
- Quality targets per DEC-084 (props LOD0 5–20k tris, LOD0–3, 2K PBR); stocking-style "believable uneven fill" applies to the under-counter storage.

## Deliverables
`Docs/Assets/Specs/REGISTER_KIT.md` (item table: id, evidence, size/param name, placement anchor, LOD/tri target, materials, GAP ids); a proposed phase-2 packet outline at the end; `Docs/Handoffs/PROC-006.md` with `## Questions for Nolan (through the Hub)`.

## Validation
Every row cites a source or a GAP id. Docs only.
