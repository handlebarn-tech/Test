# GAME-026 — Customer flow: entry check-in guard, one line, the player calls next (playtest 1)

**Role:** GAME · **Priority:** P0 · **Branch:** `task/GAME-026` worktree off `main` (after GAME-009 merges — same `ShiftSim.cs`/`SliceGame.cs`; after GAME-025 merges — the E-priority and pause code; World anchors optional, see Dependencies)

## Goal
Playtest 1 (DEC-096, `Docs/Design/PLAYTEST_2026-10-30.md`): customers must come through the entry, be ID-checked by a guard, wait in one line, and walk to the register **only when the player calls them**. Spec: `Docs/Specs/CONTROLS_FLOW_PS1.md` (cited **CF§n**).

## Read
CF§4, §5, §6 (GAME-026 rows), §7.2–7.3, §8; `Docs/Design/SPEC_COMP002.md` §3 (cover check-in); `Docs/Specs/UX_PS1.md` §4 (ID stand, counter line strip); `Docs/Design/SPEC_SHIFT_DAY.md` §5–§6; `Docs/Handoffs/GAME-008.md`, `GAME-010.md`, `GAME-010b.md`; DEC-036 M2, DEC-048, DEC-076, DEC-086.

## Owns
- `Assets/_Game/Code/Simulation/Slice/ShiftSim.cs`, `Customers.cs` (new states `Arriving`, `AtCheckIn`, `Called`; guard check queue; `CallNext()`, `ArriveAtCounter()`; remove auto-promotion; `CheckInDelay` out of `WaitPenalty` per CF§4.2)
- `Assets/_Game/Code/Presentation/Slice/SliceGame.cs`, `SliceView.cs` (anchor lookup with fallbacks CF§7, `NPC_Guard`, NPC routing through check-in/line/call point, Call-next prompt/button/toast, `Auto-call next` assist)
- `Data/Slice/SliceConfig.json` (new keys `guardCheckSeconds`, `callNextDelay`; new `_` comments), `SliceLines.json` (new key `callNext` only)
- `Tests/EditMode/Slice/`, `Tests/PlayMode/Slice/` and the GAME-010 persona bots (they must call next)
No `Code/Domain/` edits (DEC-001); no World files.

## Deliverable
1. State path and patience rules exactly as CF§4.1 (patience drains at check-in and in line, frozen once called; `QueueWait` ends at the call; `ServiceStart` at arrival at the counter).
2. Guard check-in per CF§4.2: every customer passes the stand; guard checks one at a time for `guardCheckSeconds`; GAME-008 cover routes the covered arrivals to the player at the same stand, guard keeps checking the rest; decline = physical extra wait. The counter never re-checks.
3. One line per CF§4.3 (`queueSlots` = queue anchors found).
4. Call next per CF§5: E / Ⓐ / HUD button at the player's register only, all feedback beats in CF§5.2 (audio = event hook only), assist off by default and tagged.
5. DEC-076 entry lock behaviour (CF§5.4) only if the game-clock day mode is on `main`; otherwise note it in the handoff.
6. Anchors by CF§7 names with old-name fallbacks (`Anchor_CheckInDesk`, `Anchor_QueueSlot_<n>`, `Anchor_ServiceCustomer`, `Anchor_ServicePlayer`) and `TEMP_` placeholders; warn once listing what fell back.

## Validation
Compile / EditMode / PlayMode green; QA-002 gate and DEC-013 gate green. **Slice goldens will change** (guard time, call step, wait penalty): regenerate them in this branch, list old → new values in the handoff, and get QA sign-off through the lead before merge.
- EditMode: nobody reaches `Serving` without `CallNext()`; `CallNext()` refused when not at the register / a customer is called or serving / line empty; called customers never walk out; patience drains at check-in and in line; covered arrivals go to the player, others to the guard; decline adds exactly `declineCheckInDelaySec` of check-in wait and no separate `CheckInDelay` penalty; seed determinism.
- PlayMode: the slice bot plays a full shift calling next each time; a scripted test leaves the player idle at the register and asserts the line waits and walkouts happen; every customer's NPC passes `Anchor_CheckIn` before `Anchor_Queue_0`.
- Persona bots (GAME-010): perfect/slow/careless finish with the expected ordering; slow persona's call waits its 1.5× pacing (DEC-086).
- Capture: `SliceCaptureTests` adds (a) the guard checking a customer at the stand with the line visible, (b) a called customer walking up with the `Called · walking up` HUD.

## Dependencies
GAME-009 merged; GAME-025 merged (E priority, pause). World anchors CF§7.2–7.3 (`Anchor_Guard_Post`, `Anchor_CheckIn`, `Anchor_CheckIn_Wait_<n>`, `Anchor_Queue_<n>`, `Anchor_Register_<n>_Call/_Operator`, `Anchor_CustomerSpawn` moved outside): **not blocking** — fallbacks keep the slice playable; the final capture waits for them. Entry door use needs GAME-025's door runtime and World's entry `Door_<Id>`.

## Handoff
`Docs/Handoffs/GAME-026.md` (≤40 lines). Questions go to your department lead (DEC-033, DEC-094).
