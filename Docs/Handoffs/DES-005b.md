# DES-005b handoff — DEC-103 into the flow spec, W5U minors, DES-007

**Status:** done, doc-only. **For:** Gameplay lead. **Files:** `Docs/Specs/CONTROLS_FLOW_PS1.md`, `Docs/Tasks/Ready/GAME-025.md`, `GAME-026.md`, `Docs/KNOWN_GAPS.md` (GAP-DAY-04 + new GAP-CF-01..08 block only), `Docs/Design/ROADMAP_POST_SLICE.md` (appended §7), new `Docs/Design/TONE.md`, `Docs/Specs/UX_PS1.md` (one pointer line in §8).

## DEC-103 in the spec (CF§)
- Call lines "Next in line!" / "Next guest!" at random; "Online order!" stored, unused (no online orders in PS1) (§5.2). One line (§4.3). No second door (§4.2, §7.1).
- Guard scans the back of the ID, 3 s [GDD]; green light 0.6 s + `OnIdScanOk` hook, then the line (§4.2). No backlog, no cover prompt, no helper logic; one `Anchor_CheckIn_Wait`; `declineCheckInDelaySec` / `CheckInDelay` retired.
- ID shown again at the register: 2 s ID beat for every guest; GAME-008's ID events move from the stand to the register (§4.4). Corrects DEC-086 / DEC-036 M2.
- Propped open: `Vest_FOH`, `Vest_BOH`, `Hall_Office`, `HUB2_HUB` (§3.2, §7.1). Leaves spawn only for `leaves` 1/2; not-placed rows skipped; entry = `Door_Entry_L/_R`, out (west), `entryTimeLock` (REF-012, pending merge).
- GM floor-map assignment: `RegisterAssignment` / `assignedStation` or seeded pick (§5.0, DEC-079). Emergency-exit alarm stays GAP-CF-04, not re-asked (DEC-105). DEC-106 touches none of my rows.

## W5U minors
m1 GAME-026 Owns: never concurrent with GAME-025. m2 both headers: Dept, Owner, Reviewer, Touches, Interfaces (CF§7 + DOORS.json + SCENE_ANCHORS.json). m3 GAP-DAY-04 → DEC-096.

## §7 changes World must make
1. `Anchor_CheckIn_Wait_<n>` series → **one** `Anchor_CheckIn_Wait` (REF-011 SCENE_ANCHORS.json).
2. New optional `Anchor_IdScanner` (guard's scanner/light spot).
3. Per-station `Interact_Terminal_<n>` / `Interact_Scale_<n>` at assignable stations; World no longer names "the player's station".
4. `Anchor_Register_<n>_Call` also hosts the register ID beat (no geometry change).
5. DOORS.json already matches (propped four, entry pair, `leaves` 0/null); keep `notes`/`gap` marking not-placed rows.

## For the lead
- **Q-L1:** ID events at the register (my placeholder, CF§4.4) vs keeping them at the stand. Realism risk: an expired or under-21 ID that already passed the guard's scan reads oddly at the register. Options: keep only cases a scan can't catch, or keep the events as the PS1 compliance beat as written.
- SPEC_COMP002 §3 ("counter does not re-check", the cover prompt) and UX_PS1 §4 (cover prompt, stand panel) need their owners to amend them. DECISIONS should note that DEC-103 corrects DEC-086 / DEC-036 M2.
- GAME-026 now also retires the GAME-008 cover strings and `AtStand`. Goldens change anyway (QA sign-off already required).

## Questions for Nolan (through the Hub)
None. Per DEC-105 I searched DECISIONS (079/086/096/101/103–106), KNOWN_GAPS, `Handoffs/REF-008.md` and `Research/` (OFFICE_FINDINGS O2/O11: alarms are deliberately left out). Open points: floor-map location and "Online order!" use. Both have placeholders and are not needed for PS1.
