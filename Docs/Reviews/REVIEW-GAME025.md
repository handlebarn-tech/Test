# REVIEW-GAME025 — GAME-025 (mouse look, Esc pause, doors; playtest 1)

**Verdict: GO for playtest build 2, with one MAJOR that can't trigger in this build (fix before World's doors land) and minors.**
- I merged `worktree-agent-a832d8d16c249547d` (e434977) `--no-ff` into `review/game025` (68a5df1), cut from main 1eeb814. The merge was clean.
- No `Code/Domain/` or `Simulation/` edits. No World files touched.
- The test assembly gains a reference to `Dispo.Presentation`, for `DoorTests`.

## Gates (studio.ps1, 0/2 slots at start; DEC-013; run after `git lfs checkout`)
- `unity-compile`: csErrors=0.
- `unity-test-edit`: 790 total, 788 passed, **0 failed**, 2 skipped. Both skips are `[Explicit]` (DEC-072).
  - The worker's 20 ProcArt LODGroup failures don't reproduce. They came from LFS pointer files, as the lead suspected.
- **Gate A (DEC-067):** `TfsParityGateTests` 11/11, `EngineGoldenTests` 23/23, `ParserGoldenTests` 95/95.
- Other suites: `MedicalTests` 7/7 and the new `DoorTests` 8/8.
- `unity-test-play`: 10 passed, 1 skipped (GPU capture). This includes:
  - `Esc_PausesEveryScreen_AndFreezesSim`;
  - `Door_OpensForPlayer_LetsThrough_AutoCloses`;
  - the graybox walk tests;
  - `Bot_Seed1_FullShift`.
- `unity-capture`: graybox QA PASS (0.22 ft). Slice capture PASS, 28 shots, including `SLICE_02_Pause_Menu`.

## Checks
- **Source citations (Hub rule).**
  - Each [GDD] value is tagged in code and listed in the handoff (CF§6): open 0.45 s, auto-close 1.5 s, trigger 1.2 m, prompt 1.5 s, keyed doors refuse everyone, `openAngle` placeholder 90.
  - Missing DOORS.json fields log as CF§7.1 placeholders. Hardware and `npcUse` come only from DOORS.json, with no override in code.
  - Exception: see M1.
- **Esc pause: PASS.**
  - Esc toggles pause from every screen. While paused, `Update` returns before `Sim.Tick`, NPC moves, the cover countdown and the hold timer.
  - Pause cancels a POS hold. Doors read the `Paused` delegate. The screen underneath is untouched.
  - The PlayMode test covers World, Query, Pos, IdCheck and Report with 2 s frozen each.
  - Backspace now does `Back()`, and the Back buttons say so.
- **Cursor: PASS (logic only).** `WantsCursorLocked` is World && !Paused. The cursor is locked and hidden in World, and free on any UI screen or the pause menu. I did not check a real windowed build; the lead lists this as a follow-up.
- **No slice-golden change: PASS.** No sim code changed, and the price goldens and Gate A are green.
- **SliceDoor: PASS.**
  - It reads DOORS.json.
  - Rows with `leaves` 0 or null, and rows with no position, spawn nothing.
  - Propped-open doors load open with no auto-close (DEC-103).
  - `entryTimeLock` is off in the Quick shift (DEC-076).
  - No `Door_<Id>` objects exist today, so it logs `[Slice] doors: none found` and adds no TEMP geometry.

## MAJOR
- **M1:** `SliceDoor.cs` falls back to a 3 ft leaf width when `leafWidth_ft` is missing (`DoorRow.Parse`, `rowWidth`).
  - Leaf width is a store fact. The fallback cites no source and isn't logged as a placeholder, unlike `openAngle` and `selfClosing`.
  - **It can't fire today.** All 12 DOORS.json rows with leaves carry `leafWidth_ft`, and no door objects exist in the scenes.
  - Fix (one line): add `Placeholder("leafWidth_ft")` on the fallback and tag it GAP-CF or [GDD] in CF§7.1. Do this before World's doors land.

## Minors
- m1 The world prompt ("E Talk") stays visible under the pause overlay (shot 02). It's cosmetic; hide the HUD prompt while paused.
- m2 These follow-ups are already known:
  - Player builds carry no DOORS.json; a copy needs to go under `Assets` and be assigned.
  - The hardware rows in DOORS.json don't match DEC-110 (`JC`, `Ext_Delivery`); World's REF-013 owns them.
  - The cursor has only been checked by logic, not in a real windowed build.
  - NPC door rules apply only at the door, so GAME-026's pathing must keep customers off staff doors.
- m3 These came from main, not this branch: after `git lfs checkout`, Unity generated untracked `.meta` files for `Art/Procedural/Fixtures/WireShelving` (PROC-005, 102f126). Main is missing those metas, and the Assets lead should commit them. I left them uncommitted.
