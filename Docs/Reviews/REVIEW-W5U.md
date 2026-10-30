# REVIEW-W5U — DES-005, playtest 1 intake: controls and customer-flow spec, packets

**Verdict: PASS with minors (GO).** I reviewed `worktree-agent-afdc1983fe7bb696c` @ 5c8031b: 6 new files, +478 lines, docs only. This file is committed on `review/w5u`, cut from 5c8031b. Inputs read: the packet, the handoff, the diff, and the cited sources: DEC-037/048/076/086/096, KNOWN_GAPS GAP-DAY-04, OFFICE_FINDINGS O2, and the code the spec names. Lead rulings already made and not re-reviewed: GrayboxTestPlayer is Gameplay-owned, "one line" closes GAP-DAY-04, and the archive-path deviation is accepted.

## Checks
1. **Deliverable 1, the verbatim copy: PASS.**
   - The body below the header is byte-identical to the archived `GameFeedback10-30.txt`, apart from one trailing newline at end of file. The md5 `ea0b387e…` in the header matches the archived file.
   - The header gives the source, build slice-38b9e5c and the date.
   - The original is gone from `Dispo Game Imports/`. It sits in `Dispo Game Imports Archive/2026-10-30_GameFeedback10-30/` (accepted deviation).
2. **Deliverable 2, the spec: PASS.** The §1.1 causes match the code:
   - Right mouse button: `GrayboxTestPlayer:46`.
   - Pitch ±80: `GrayboxTestPlayer:50`.
   - Sensitivity 0.1: `GrayboxTestPlayer:12`.
   - Cursor set to None: `SliceGame:488`.
   - Esc → `Back()`: `SliceGame:264`.
   - FOV is set only on the reference cameras, not on `Eye`: `GrayboxBuilder:129`.
   - Auto-promotion of `Queue[0]`: `ShiftSim:125-127`.
   - `CheckInDelay` is added into `WaitPenalty`: `ShiftSim:236,414`. This confirms the double-count the spec removes.
   - Pause rules, door model, flow states, how the GAME-008 stand coexists with the guard, and call-next all cover the packet's 2a/2b.
3. **[GDD] labels: PASS.** Every new value is labelled [GDD] or marked as an existing value.
4. **No invented store facts: PASS.**
   - The cited facts check out: storefront 6'-0" (DEC-037), stand directly left inside the entrance with a guard (DEC-048), 22:00 lock (DEC-076), no vestibule (DEC-086), Dutchie Guest List and "before the door" (O2).
   - The unknowns are GAP-CF-01..08 and appear as 7 Nolan questions in the handoff; 03 and 04 are merged into one question.
5. **Deliverable 3, the packets: PASS.** GAME-025 and GAME-026 cite CF§s and do not copy spec text. Owns, deliverables, validation (EditMode, PlayMode and capture) and dependencies are all present. GAME-026 flags the golden change for QA sign-off.
6. **§7 contract: PASS.** It is headed "needs; World commits names", and every row is marked proposed, new need, or exists with a position change.
7. **Deliverable 4, the proposal: PASS.** All 8 ideas are present, each with what, why, rough phase and dependencies. Scope is left to the Hub.

## Minors
- m1 **GAME-025 and GAME-026 both own `SliceGame.cs` and `SliceView.cs`.** This is acceptable only because GAME-026 starts after GAME-025 merges. Never run them concurrently (§0.5); add a line saying so to GAME-026's Owns.
- m2 **Both packet headers lack the §0.5 fields** `Dept`, `Owner`, `Touches` and `Interfaces`. They follow GAME-017, which predates those fields. Add the fields when the packets are activated. `Interfaces` should name CF§7 and REF-012 `DOORS.json`.
- m3 **FYI for the Hub:** KNOWN_GAPS already marks GAP-DAY-04 "CLOSED by DEC-079". DEC-079 is the deli-restock entry, so that looks like a miscitation; DEC-096 is the right basis. The Hub should fix the citation when it numbers GAP-CF-01..08.
