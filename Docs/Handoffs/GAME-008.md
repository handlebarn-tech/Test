# Handoff: GAME-008 (cover the ID stand, ID checks) + W5G m1/m2

**Status:** done, pending review. Branch `claude/task-game-008` (off `main` dba04b4). No `Code/Domain/` edits, no graybox edits.

## Changes
- **Sim** (`ShiftSim`, new `IdCheck.cs`):
  - At rush start (once per shift, own `Random(seed + 11)`), `coverCheckInChance` 0.5 offers the cover prompt (`Cover` = Offered, `CoverOffered` event).
  - **Accept:** the next `coverCheckInCount` 3 not-yet-arrived customers get an `IdCard`. They wait at the stand (`CustomerState.AtStand`, `Stand` list) until the player admits or refuses them. The counter queue keeps draining.
  - **Decline:** those arrivals get `CheckInDelay` = `declineCheckInDelaySec` 20 s [GDD], added to the wait penalty.
  - An unworked stand drains patience too (they walk out), so the shift always ends.
- **Rules** (`IdRules.IsValid`, the law): unexpired, where the expiry day itself counts (B2); 21+ (B1); an Arizona vertical ID only within 30 days of turning 21 (B2/O3). An out-of-state vertical at 21+ is valid (O3, GAP-COMP-03).
- **Generator:** `IdCardGenerator.Make` builds each SPEC §3 case against the in-game date `shiftDate` 2026-10-27 (a Tuesday = `shiftDayOfWeek`). Weights are SPEC §3, from config. Names come from fictional first/last lists; states from a short list.
- **Outcomes** (SPEC §3):
  - admit valid → queues;
  - admit invalid → queues + strike `strikeBadId`; the toast adds the B4 fine line;
  - refuse valid → Walkout (`IdRefusedValid`, no walkout toast; its own toast);
  - refuse invalid → new `CustomerOutcome.Refused`, excluded from satisfaction and queue-wait averages.
  - Report: `IdsChecked`, `BadIdsCaught`, `ValidIdsRefused`, shown in the report's Compliance block.
- **View** (UX_PS1 §4):
  - **Cover prompt** (Y/N, Esc = decline): waits until no screen is open, then auto-declines after `coverPromptSeconds` 8.
  - **Stand:** a marker shows while covering. **E** opens the ID panel when the player is in reach.
  - **ID panel:** header, today's date, an ID-1 card (portrait for vertical IDs), A/R, Esc.
  - **HUD:** while covering it becomes the Counter line strip (patience word + icon, max 5, stand count). Result toasts use §8 strings.
- **Stand anchor:** `Anchor_CheckInDesk` by name. There is no ART anchor yet, so `TEMP_Anchor_CheckInDesk` sits beside the entry (plan x 3, y 13). GAP-COMP-08, for ART.
- **W5G m1:** checked, no change. `.meter-red .meter-fill` is `var(--bad)` = #D55E00, the UX_SLICE §6 vermilion, which renders orange-red.
- **W5G m2:** the cover prompt and ID panel honour 125/150 % (UX_COUNTER_INTEL §10). At 125/150 % the panel fills the safe area and the card scales. A readout column repeats DOB / EXP / TYPE / FORMAT full size; a portrait card may ellipsize them, never overflow. Toasts move off the panel. The 100 % portrait card is 400×635, so DOB/EXP/TYPE/FORMAT fit uncut.

## Validation (studio.ps1, DEC-013)
- **Compile and tests:** compile OK. EditMode **204/204**, including Gate A (TfsParity + goldens). PlayMode 8 passed + 1 skipped.
- **PlayMode bot:** forces the prompt, covers, judges perfectly: 3 IDs checked, 0 strikes. Seed 1 unchanged: 12/12, $364.00, Kush Cake sold out.
- **New `IdCheckTests` (11):**
  - boundaries: 21st birthday today vs tomorrow; vertical day 30 vs 31; expiry today vs yesterday; out-of-state vertical;
  - 300 IDs per case land on their side;
  - weights; date = shift weekday; same seed → same IDs;
  - the prompt fires once at rush start; decline delay;
  - refuse valid = walkout; admit invalid = 1 strike; refuse bad = caught;
  - an ignored stand still ends the shift.
- **`unity-capture` PASS, 24 shots:** prompt, horizontal and vertical ID panel at 100/125/150 % with layout asserts. Shots: `Docs/Assets/Specs/GAME-008_*.png`.

## Overlap / for others
- GAME-010: `SliceConfig.json`, `SliceTests.cs` (`RunBot` gains `acceptCover`), `Customers.cs` (new enum values `AtStand`, `Refused`). Code that sums served+walkouts+noSales must add `Refused` when a cover is accepted.
- PERF-001: `PerfCapture`'s bot ignores the prompt (auto-declines after 8 s).
- At 125/150 % the full-safe-area ID panel hides the Counter-line strip (UX §4 vs §10 conflict). UX to decide.
- Not built: the `ID age helper` assist (UX §4, off by default).
