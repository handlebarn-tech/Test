# GAME-025 handoff: mouse look, Esc pause, doors (playtest 1)

**Branch:** `worktree-agent-a832d8d16c249547d` (main 9dac6d9 + DES-005b cf5d614 merged) · **Spec:** CONTROLS_FLOW_PS1 (CF) §1–§3, §7.1 · **Status:** ready for review

## What changed
- `GrayboxTestPlayer.cs`: look is always on while the cursor is locked (no right-button hold); a click re-locks a free cursor while walking. Raw yaw/pitch: no smoothing, acceleration or bob; pitch ±85°; invert Y; FOV set at runtime on `Eye`. Settings are kept in `PlayerPrefs` (`look.sensitivity`, `look.invertY`, `look.fovVertical`), never read by the sim. Public fields and `ScriptedWorldMove` are unchanged.
- `SliceGame.cs`: Esc → `TogglePause()` from every screen; Backspace → `Back()`. Pause skips `Sim.Tick`, NPC movement, the cover countdown and the doors, and cancels a POS hold; the screen underneath is not touched. The cursor is locked in `World` and free on any UI screen or while paused. E priority: ID check > talk > (call next, GAME-026) > door toggle. `Doors` TextAsset slot added.
- `SliceView.cs` + `Slice.uss`: top-layer pause menu (Resume / Settings / Controls / Quit to desktop with a confirm). Settings has sensitivity, invert Y, FOV, text size and the auto-fill assist. The HUD prompt shows "Locked" / "Staff only". Back buttons now read "Back (Backspace)".
- New `SliceDoor.cs`: `DoorRow` (DOORS.json reader with CF§7.1 placeholders), `DoorState` (state machine) and `SliceDoor` (runtime: finds `Door_<Id>` / `_L` `_R` and their `_Hinge` pivots by name, uses trigger boxes at `Anchor_Door_<Id>_A/_B`, swings by the signed `openAngle`, turns the colliders off unless closed, lets NPCs use doors by `npcUse`). Rows with `leaves` 0/null or no `pos_ft` spawn nothing. `entryTimeLock` stays off (the slice is a Quick shift).
- Today: no `Door_<Id>` objects exist in any scene, so the slice logs `[Slice] doors: none found` and the openings work as before. No TEMP door geometry is added.

## [GDD] values (CF§6)
`lookSensitivity` 0.10 °/count (0.02–0.40) · `fovVertical` 70° (60–90) · `pitchClamp` ±85° · `doorOpenSeconds` 0.45 s (ease-out) · `doorAutoCloseDelay` 1.5 s · trigger 1.2 m × opening width · prompt 1.5 s · keyed doors refuse everyone · missing `openAngle` → 90.

## Validation
All runs used `studio.ps1` (DEC-013).
- **Compile:** 0 errors.
- **EditMode:** 225 total, 203 passed, 20 failed, 2 skipped. All 20 failures are Assets' known ProcArt "no LODGroup" failures (6× `JarFillImportTests`, 14× `PackagedGoodsImportTests`); they are not fixed here. The 8 new `DoorTests` pass, and so do the slice price goldens and Gate A (`TfsParityGateTests`). No sim code changed.
- **PlayMode:** 11 total, 10 passed, 0 failed, 1 skipped (`Capture_EachScreen` needs a GPU). `GrayboxWalkTests`, `Bot_Seed1_FullShift`, the new `Door_OpensForPlayer_LetsThrough_AutoCloses` and `Esc_PausesEveryScreen_AndFreezesSim` all pass.
- **Capture:** graybox OK (24 shots, QA PASS); slice capture passed with 28 shots, including the new `Pause_Menu`. There is no door mid-swing shot because World's doors are not on `main`.
- The EditMode run came before the last one-line change (`WantsCursorLocked`); that change compiled and passed in PlayMode.
- **Environment note:** this fresh worktree had Git LFS pointers instead of the FBX files, which broke `SpawnJars` in PlayMode. `git lfs checkout` (local store, no download) fixed it, and other workers' fresh worktrees may hit the same thing.
- **Not checked in a real windowed build:** batchmode does not hold a cursor lock, so the test asserts `WantsCursorLocked` instead of the real cursor state.

## Deviations
- **Pause test in PlayMode, not EditMode.** Pause lives in the MonoBehaviour, so `Esc_PausesEveryScreen_AndFreezesSim` covers "pause stops Tick and the hold timer". Tests call `TogglePause()` (the method Esc calls) because the project has no Input System test fixture.
- **The Report screen's Enter close is not built** (it was never built). Back from Results still goes to World (`Back()` is unchanged). UX_COUNTER_INTEL §13.8 "Backspace on Results = Edit search" belongs to whoever builds that spec.

## For the lead / World (not questions for Nolan)
1. **DOORS.json in builds:** `SliceGame.Doors` is unassigned, and the Editor falls back to reading `Docs/Reference/DOORS.json` from disk, so a player build gets no door data. When World's doors land, a copy of the file must live under `Assets` (owner: World/Data) and be assigned in `Gameplay_Slice`. I don't own either.
2. **DOORS.json vs DEC-110 W6 (for World):** `JC.hardware = pushBar` should be `lever`, and `Ext_Delivery.hardware = lever` should be `pushBar`. Code reads the file as given and does not override it.
3. **Placeholders logged:** `selfClosing` is `unknown` on Entry, Emergency_RetailE, Office_HUB2, HUB2_HUB, Ext_Delivery and Ext_Emergency_SE (REF-012's own GAPs). The placeholder is true.
4. **The NPC door rule is enforced only at the door.** Refused NPCs have no collider, so GAME-026's waypoint pathing must keep customers off staff doors.

## Questions for Nolan (through the Hub)
None. DEC-105 search: DECISIONS.md (DEC-076, 103, 105, 110), KNOWN_GAPS (GAP-CF-03/04, GAP-138/139), UX_SLICE §4/§7, UX_PS1 §7, UX_COUNTER_INTEL §13.8, DOORS.json `_about`.
