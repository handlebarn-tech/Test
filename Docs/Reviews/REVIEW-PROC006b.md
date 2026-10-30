# REVIEW-PROC006b: register workstation kit (generators + per-station arranger)

**Reviewer:** fresh, Hub-spawned (STUDIO_OS §0.7) · **Date:** 2026-10-30
**Reviewed:** `claude/proc-006b-92b9a0` @ 9728334, merge base 1b72b81, merged `--no-ff` onto `review/proc006b` from main 67ef2a0 with no conflicts.
**Sources read:** `Docs/Tasks/Active/PROC-006b.md`, the diff, `Docs/Handoffs/PROC-006b.md` (Validation, Not done), DEC-047/051/084/086/104/110/114, `Docs/Assets/Specs/REGISTER_KIT.md`, both contact sheets.

## Verdict: PASS with minors

## Checks
1. **Blender validation.** I ran `Tools/Blender/blender.ps1 register_kit Tools/Blender/params/register_kit.json` and it exited 0. All 16 `PROC_RK_*` pass. My tri counts match the handoff table exactly.
2. **Determinism of exports.** The rerun left every FBX (LFS) and every Unity copy byte-identical: git shows no change. The validation JSON and manifest differ only in CRLF/LF (`git diff --ignore-cr-at-eol` is empty).
3. **Arranger self-test.** `python Tools/Blender/tests/test_register_arranger.py` passes: 11 stations, 11 distinct optional sets. The test asserts everything the packet asks for:
   - the same seed gives the same JSON, and it equals the committed files;
   - each fixed item appears exactly once, on TOP;
   - the mouse is right of the keyboard's half-width;
   - at least 2 stations differ in optional items.
4. **PROC-005 toolkit self-test.** `tests/test_validation.py`, run under Blender, prints `[SELFTEST] all passed`.
5. **Citations (DEC-047).** Every item and anchor carries a `_src` or a GAP id, and the spec's GAP register maps GAP-REG-1..10 to DEC-104 R1–R7. The arranger's layout offsets and weights are tagged `GAP-RK-LAYOUT` / `GAP-RK-WEIGHTS`. No uncited store fact found; see minor 4 for product-convention dimensions.
6. **DEC-104 rules in the data.** Fixed at every station: keyboard, mouse (right), scanner, receipt printer, label printer. The label printer slot varies (7 left / 4 right). ISO spray p = 0.5, wipes sparse, rag blue, a small bin at every station. POS_09 spot-check: 16 items, `not_fitted` empty.
7. **Other packet rules.**
   - DEC-051: no cash-handling equipment.
   - DEC-086: manifest rows carry `collision_boxes`.
   - No Unity work and no scene placement.
8. **Visual read (DEC-084 / DEC-114).** The committed contact sheet is too small to judge (minor 2), so I rendered each LOD0 FBX at 640 px (workbench, cavity). They read as real products:
   - keyboard with individual keycaps and a numpad;
   - clamshell label printer;
   - top-exit receipt printer with a tear bar, vents and a front band;
   - handheld scanner in a stand with a coiled cord;
   - trigger spray bottle with a waisted grip;
   - wire-mesh bin with crumpled paper;
   - taped and open paper-stock cases with rolls;
   - draped and folded rags;
   - tumbler with a straw;
   - soft wipes pack with a lid.

   The 12 props under the 5k LOD0 guide are acceptable under DEC-114. The stations sheet shows 4 visibly different dressings.

## MAJOR
None.

## minor
1. **No 2K PBR or UV/texture set (packet Rules, DEC-084).** Materials are preview colours only. The handoff states this and blames the toolkit dependency (PROC-005 Q0.2/Q0.3). That dependency is tracked only inside BACKLOG PROC-010's "materials" scope. Hub's call: accept the deferral and make sure PROC-010 (or its split packet) covers the RK props.
2. **The committed contact sheet can't be used for the DEC-114 visual judgement.** `PROC_register_kit_contact_sheet.png` is 480 px wide (160 px per tile) and has no labels. The LOD3 column renders as faint ghost boxes. The props are fine (check 8); the review evidence is not.
3. **The ISO spray stands on the stand edge instead of hanging.** DEC-104 R3 and the spec source call it the "hanging" bottle ("a spray bottle hanging from a scale shelf"). The bottle has no hook or hanger geometry, and `STAND_RAIL` places it upright on the stand top (stations sheet, POS_09).
4. **Product-convention dimensions with no tag.** Keyboard `kb_d_m`, `case_h_m` and `key_h_m` have `gaps: []`. Only the 17.5 in width is cited. These are generic product dimensions, not store facts, but the Mouse row tags its convention size with GAP-REG-3 and the Keyboard row should be tagged the same way.
5. **Stale gap strings in the params.** `arranger.anchors.UNDER_UPPER`, `UNDER_LOWER` and `UNDER_UPPER_EDGE` say "anchor id pending ROOM_FIXTURES rev7". Rev7 has merged; the real open item is the under-shelf heights and depth, which is the handoff's Nolan question.
6. **GAP ids not registered.** GAP-REG-1..10, GAP-RK-LAYOUT and GAP-RK-WEIGHTS appear only in the spec and params. They are not in `KNOWN_GAPS.md` and not proposed in the handoff's For the Hub section.
7. **No Unity import check.** None was run, and the new `RegisterKit/` FBX copies have no `.meta`. The packet rules out Unity work, so this is noted only: first editor import is owed.

## For the Hub
- The handoff's World items (small-bin size conflict, monitor depth) and the FOR NOLAN under-counter question look well-founded. Its search list meets DEC-105.
