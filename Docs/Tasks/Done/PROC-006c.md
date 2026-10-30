# PROC-006c — Register kit follow-ups from REVIEW-PROC006b

**Priority:** P2 · **Base:** `main` (PROC-006b merged, e1e8a68) · **No Unity.**

## Goal
Close the review minors on the register kit that need no materials work: `Docs/Reviews/REVIEW-PROC006b.md` § minor items **2, 3, 4, 5, 6**. (Item 1, 2K PBR, is PROC-010's materials scope; item 7, Unity `.meta` import, rides with PROC-007.)

## Owns
`Tools/Blender/generators/register_kit.py`, `Tools/Blender/params/register_kit.json`, the arranger module PROC-006b added, `Docs/Assets/Specs/REGISTER_KIT.md`, `Art/Exports/Procedural/RegisterKit/**` + its manifest rows, `Docs/Assets/Specs/PROC_register_kit_*.png`, `Docs/Handoffs/PROC-006c.md`. Shared runner/proclib: use as-is.

## Deliverables
- m2: a contact sheet usable for the DEC-114 judgement (labelled tiles, readable size, LOD column visible).
- m3: the ISO spray hangs (hook/hanger geometry, hanging placement) per DEC-104 and the spec source.
- m4: keyboard convention dimensions tagged like the mouse row (GAP-REG-*).
- m5: the stale `UNDER_*` anchor gap strings rewritten to the real open item (under-counter heights/depth, open with Nolan).
- m6: every GAP id the kit uses (GAP-REG-1..10, GAP-RK-LAYOUT, GAP-RK-WEIGHTS) proposed as `KNOWN_GAPS.md` entries in your handoff's `## For the Hub` (text + source), so the Hub can register them.
- Rules unchanged from `Docs/Tasks/Done/PROC-006b.md` (DEC-084/104/105/110/114, DEC-051).

## Validation
PROC-006b's validation and arranger self-test still pass; re-export changed props.
