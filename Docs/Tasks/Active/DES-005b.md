# DES-005b — Fold DEC-103 into the flow spec; W5U minors; DES-007 roadmap + tone note

**Role:** DES · **Dept:** Gameplay · **Priority:** P0 · **Branch:** worktree off `main` (doc-only) · **Owner:** lead subagent · **Reviewer:** Docs pool
**Touches:** `Docs/Design/ROADMAP_POST_SLICE.md` (Hub-owned; the Hub delegated this edit in DEC-101) · **Interfaces:** `Docs/Specs/CONTROLS_FLOW_PS1.md` §7

## Goal
Bring the DES-005 spec and packets in line with Nolan's real-store answers (DEC-103), fix REVIEW-W5U minors, and do DES-007 (DEC-101).

## Read
DEC-079, DEC-086, DEC-096, DEC-101, DEC-103 in `Docs/DECISIONS.md`; `Docs/Reviews/REVIEW-W5U.md`; `Docs/Specs/CONTROLS_FLOW_PS1.md`; `Docs/Tasks/Ready/GAME-025.md`, `GAME-026.md`; `Docs/Handoffs/DES-005.md`; `Docs/KNOWN_GAPS.md` (GAP-DAY-04, format); `Docs/Design/PROPOSAL_PLAYTEST1_LONGTERM.md`; `Docs/Design/ROADMAP_POST_SLICE.md`.

## Owns
`Docs/Specs/CONTROLS_FLOW_PS1.md`, `Docs/Tasks/Ready/GAME-025.md`, `GAME-026.md`, `Docs/KNOWN_GAPS.md` (Gameplay rows only: GAP-CF-01..08, GAP-DAY-04), `Docs/Design/ROADMAP_POST_SLICE.md` (append rows only), a tone note `Docs/Design/TONE.md` (new) plus a one-line pointer to it from `Docs/Specs/UX_PS1.md` §dialogue (or wherever dialogue/event lines are specified), `Docs/Handoffs/DES-005b.md`.

## Deliverable
1. DEC-103 into the spec and packets:
   - call lines "Next in line!", "Online order!" and "Next guest!";
   - one line;
   - no second door;
   - the guard scans the back of the ID, and a green light plus a sound sends the guest into the line;
   - the ID is shown again at the register (this corrects DEC-086: reconcile with the GAME-008 register ID stand);
   - check-in takes seconds and never backs up (drop the backlog and helper logic);
   - FOH/BOH, the north office door and the HUB connector are propped open by default (update §7 door needs);
   - the GM assigns registers on a floor map (DEC-079): replace the "station with `Interact_Terminal`" placeholder with an assignment model;
   - the emergency exit alarm stays a GAP.
   Close the answered GAPs.
2. REVIEW-W5U m1: add "never concurrent with GAME-025" to GAME-026's Owns. m2: add the §0.5 header fields (Dept, Owner, Touches, Interfaces = CF§7 + `Docs/Reference/DOORS.json` / `SCENE_ANCHORS.json`) to both packets. m3: GAP-DAY-04's closing basis → DEC-096.
3. KNOWN_GAPS: add GAP-CF-01..08 with their state after DEC-103.
4. DES-007: add the accepted long-term ideas to `ROADMAP_POST_SLICE.md` as phased rows (DEC-101); write `TONE.md` (≤1 page: grounded deadpan humour, coming from the simulation, played straight, with do and don't examples) where dialogue and event writers will read it.

## Validation
Every change cites its DEC; no new store facts beyond DEC-103; [GDD] labels kept.

## Handoff
`Docs/Handoffs/DES-005b.md` (≤30 lines), with a list of any lines World must change in §7. Report to the Gameplay lead; never ask Nolan (DEC-033).
