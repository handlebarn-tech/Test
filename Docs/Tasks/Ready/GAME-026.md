# GAME-026 — Customer flow: entry check-in guard, one line, the player calls next (playtest 1)

**Dept:** Gameplay · **Role:** GAME · **Owner:** worker subagent (id + branch once launched) · **Reviewer:** pool (lead assigns) · **Touches:** none · **Interfaces:** `Docs/Specs/CONTROLS_FLOW_PS1.md` §7 (CF§7), `Docs/Reference/SCENE_ANCHORS.json` (REF-011, pending merge; branch `worktree-agent-a3e83b7d768da38d0` @ 9b111fa), `Docs/Reference/DOORS.json` (REF-012, pending merge) (header fields: REVIEW-W5U m2)
**Priority:** P0 · **Branch:** `task/GAME-026` worktree off `main` (after GAME-009 merges — same `ShiftSim.cs`/`SliceGame.cs`; after GAME-025 merges — the E-priority and pause code; World anchors optional, see Dependencies)

## Goal
Playtest 1 (DEC-096, `Docs/Design/PLAYTEST_2026-10-30.md`): customers must come through the entry, have the back of their ID scanned by the guard, wait in one line, walk to the register **only when the player calls them**, and show the ID again there (DEC-103). Spec: `Docs/Specs/CONTROLS_FLOW_PS1.md` (cited **CF§n**).

## Read
CF§4 (incl. §4.4), §5 (incl. §5.0), §6 (GAME-026 rows), §7.2–7.3, §8; DEC-103, DEC-079 (one line, GM floor map); `Docs/Design/SPEC_COMP002.md` §3 (cover check-in); `Docs/Specs/UX_PS1.md` §4 (ID stand, counter line strip); `Docs/Design/SPEC_SHIFT_DAY.md` §5–§6; `Docs/Handoffs/GAME-008.md`, `GAME-010.md`, `GAME-010b.md`; DEC-036 M2 and DEC-086 (both corrected by DEC-103 (4): the ID is shown again at the register), DEC-109 (ID-check split), DEC-048, DEC-076.

## Owns
- `Assets/_Game/Code/Simulation/Slice/ShiftSim.cs`, `Customers.cs` (new states `Arriving`, `AtCheckIn`, `Called`; one-at-a-time guard scan, no backlog/helper logic; register ID beat and the GAME-008 ID events moved to the register (CF§4.4); `RegisterAssignment` (CF§5.0); `CallNext()`, `ArriveAtCounter()`; remove auto-promotion; retire the cover prompt/decline path and take `CheckInDelay` out of `WaitPenalty` per CF§4.2)
- `Assets/_Game/Code/Presentation/Slice/SliceGame.cs`, `SliceView.cs` (anchor lookup with fallbacks CF§7, `NPC_Guard` + scanner green light, NPC routing through check-in/line/call point, register ID beat, Call-next prompt/button/toast, floor-map toast, `Auto-call next` assist). **Never run concurrently with GAME-025**: both own `SliceGame.cs` and `SliceView.cs`; start only after GAME-025 merges (REVIEW-W5U m1, STUDIO_OS §0.5).
- `Data/Slice/SliceConfig.json` (new keys `guardCheckSeconds` 3, `scanLightSeconds`, `registerIdSeconds`, `assignedStation` (optional), `callNextDelay`; `declineCheckInDelaySec` retired; new `_` comments), `SliceLines.json` (new keys: `callNext` = the two DEC-103 lines, `callOnlineOrder` (unused in PS1), the floor-map toast, `ID shown ✓`; the GAME-008 cover-prompt strings become unused)
- `Tests/EditMode/Slice/`, `Tests/PlayMode/Slice/` and the GAME-010 persona bots (they must call next)
No `Code/Domain/` edits (DEC-001); no World files.

## Deliverable
1. State path and patience rules exactly as CF§4.1 (patience drains at check-in and in line, frozen once called; `QueueWait` ends at the call; `ServiceStart` at arrival at the counter).
2. Check-in and ID (DEC-103):
   a. Guard scan per CF§4.2: every customer passes the stand; the guard scans the back of the ID, one at a time, `guardCheckSeconds` 3 s; green light + `OnIdScanOk` hook, then the guest joins the line; **red light** (`scanRejectChance` 0.02, expired/underage cases) → the guard turns the guest away, no player action, outcome `TurnedAwayAtDoor` (DEC-109). No cover prompt, no helper logic; a mid-scan arrival waits at `Anchor_CheckIn_Wait_<n>`.
   b. The ID again at the register per CF§4.4: every guest gets the `registerIdSeconds` ID beat on arrival at the counter; the selected guests get the ID panel there with the **register cases** (lead ruling DEC-109, CF§4.4 table): photo mismatch / borrowed ID, medical card name ≠ ID, out-of-state medical card (GAME-009), damaged/unreadable ID, AZ vertical > 30 days, plus valid IDs; Admit/Refuse and GAME-008 strikes. Expired/underage are never drawn at the register.
3. One line per CF§4.3 (`queueSlots` = queue anchors found).
4. Register assignment per CF§5.0 (GM floor map, DEC-079; `assignedStation` = 08 [GDD], zero-padded `Anchor_Register_08_Call/_Operator`). Call next per CF§5: E / Ⓐ / HUD button at the assigned register only, call toast from DEC-103's lines, all feedback beats in CF§5.2 (audio = event hook only), assist off by default and tagged.
5. DEC-076 entry lock behaviour (CF§5.4) only if the game-clock day mode is on `main`; otherwise note it in the handoff.
6. Anchors by CF§7 / REF-011 names (42 anchors; registers zero-padded `02`..`12`; `Anchor_CheckIn_Wait_0..3`; `Anchor_Queue_0..11`) with the alias fallbacks (`Anchor_CheckInDesk`, `Anchor_QueueSlot_0..3`, `Anchor_ServiceCustomer`, `Anchor_ServicePlayer`), then the SCENE_ANCHORS.json position, then `TEMP_` placeholders. Most anchors are Low confidence until ART-007 builds the objects: **a missing object never fails the run**; warn once listing what fell back.

## Validation
Compile / EditMode / PlayMode green; QA-002 gate and DEC-013 gate green. **Slice goldens will change** (guard time, call step, wait penalty): regenerate them in this branch, list old → new values in the handoff, and get QA sign-off through the lead before merge.
- EditMode: nobody reaches `Serving` without `CallNext()`; `CallNext()` refused when not at the register / a customer is called or serving / line empty; called customers never walk out; patience drains at check-in and in line; every check-in takes exactly `guardCheckSeconds` (no backlog term); red-light guests leave with no player action and no strike; expired/underage never reach the register; every served guest gets the register ID beat; selected guests get the ID panel at the register with CP§3 outcomes and only DEC-109 register cases; a scene with no REF-011 objects runs on fallbacks and logs one warning; no `CheckInDelay` in any wait penalty; `CallNext()` refused away from the assigned station; seed determinism (incl. the station pick).
- PlayMode: the slice bot plays a full shift calling next each time; a scripted test leaves the player idle at the register and asserts the line waits and walkouts happen; every customer's NPC passes `Anchor_CheckIn` before `Anchor_Queue_0`.
- Persona bots (GAME-010): perfect/slow/careless finish with the expected ordering; slow persona's call waits its 1.5× pacing (DEC-086).
- Capture: `SliceCaptureTests` adds (a) the guard scanning an ID at the stand (green light) with the line visible, (b) a called customer walking up with the `Called · walking up` HUD, (c) the ID panel at the register.

## Dependencies
GAME-009 merged; GAME-025 merged (E priority, pause). World anchors CF§7.2–7.3 (`Anchor_Guard_Post`, `Anchor_CheckIn`, `Anchor_CheckIn_Wait_<n>`, `Anchor_Queue_<n>`, `Anchor_Register_<n>_Call/_Operator`, `Anchor_CustomerSpawn` moved outside): **not blocking** — fallbacks keep the slice playable; the final capture waits for them. Entry door use needs GAME-025's door runtime and World's `Door_Entry_L/_R` (REF-012, pending merge). SPEC_COMP002 §3 and UX_PS1 §4 carry a DEC-103 note; their full rewrite is not this packet's.

## Handoff
`Docs/Handoffs/GAME-026.md` (≤40 lines). Questions go to your department lead (DEC-033, DEC-094).
