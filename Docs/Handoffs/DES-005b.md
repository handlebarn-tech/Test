# DES-005b handoff — DEC-103 into the flow spec, W5U minors, DES-007

**Status:** done, doc-only; `main` merged in (115292c, which has DOORS.json + SCENE_ANCHORS.json) and re-checked. **For:** Gameplay lead. **Files:** `Docs/Specs/CONTROLS_FLOW_PS1.md`, `Docs/Tasks/Ready/GAME-025.md`, `GAME-026.md`, `Docs/KNOWN_GAPS.md` (GAP-DAY-04 + new GAP-CF-01..08 block only), `Docs/Design/ROADMAP_POST_SLICE.md` (appended §7), new `Docs/Design/TONE.md`, `Docs/Specs/UX_PS1.md` (§4 DEC-103 note, §8 tone pointer), `Docs/Design/SPEC_COMP002.md` (§3 DEC-103 note; lead-delegated).

## DEC-103 / DEC-109 in the spec (CF§)
- Call lines "Next in line!" / "Next guest!" at random; "Online order!" stored, unused (no online orders in PS1) (§5.2). One line; no second door (§4.2–4.3).
- Guard scans the back of the ID, 3 s [GDD]: green light → line; red light (expired/underage, `scanRejectChance` 0.02 [GDD]) → turned away, no player action (DEC-109). No backlog, cover prompt or helper logic; `CheckInDelay` retired.
- ID again at the register: a 2 s beat for every guest; player decisions there = photo mismatch, med-card name ≠ ID, out-of-state med card (GAME-009), damaged ID, plus valid IDs, with GAME-008 strikes (§4.4, DEC-109).
- Doors (DOORS.json): leaves only for `leaves` 1/2; entry `Door_Entry_L/_R` out (west), `entryTimeLock`; propped `Vest_FOH`, `Vest_BOH`, `Hall_Office`, `HUB2_HUB` (§3.2, §7.1).
- Anchors (SCENE_ANCHORS.json): zero-padded `Anchor_Register_02..12_Call/_Operator`, player station 08 [GDD] by GM floor map (§5.0, DEC-079); `Anchor_CheckIn_Wait_0..3` inside the entrance; aliases kept; missing objects fall back and warn once, never fail (§7).
- Emergency-exit alarm stays GAP-CF-04 and is not re-asked (DEC-105). DEC-106 touches none of my rows.

## W5U minors
m1 GAME-026 Owns: never concurrent with GAME-025. m2 both headers: Dept, Owner, Reviewer, Touches, Interfaces (CF§7 + DOORS.json + SCENE_ANCHORS.json). m3 GAP-DAY-04 → DEC-096.

## §7 changes World must make
None. §7 now follows DOORS.json and SCENE_ANCHORS.json as merged. Placing `Interact_Terminal` / `Interact_Scale` at station 08 is ART-007's job (already their contract).

## For the lead
- I put "AZ vertical, turned 21 > 30 days ago" at the register (a format rule, not something the age scan catches) [GDD]. Move it to the door's red light if you read the scanner differently.
- GAME-026 retires GAME-008's cover prompt strings and `AtStand`, and adds 3 new ID cases (weights [GDD]). Goldens change (QA sign-off already required).
- SPEC_COMP002 §3 and UX_PS1 §4 got one-line DEC-103/109 notes only; their full text rewrite is still open for their owners.

## Questions for Nolan (through the Hub)
None. Per DEC-105 I searched DECISIONS (079/086/096/101/103–109), KNOWN_GAPS, `Handoffs/REF-008.md` and `Research/` (OFFICE_FINDINGS O2/O11; alarms are deliberately left out). Where the floor map hangs and how "Online order!" is used both have placeholders and are not needed for PS1.
