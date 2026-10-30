# GAME-010 handoff — WIP (usage limit hit, not done)

## Done
- Packet moved to `Docs/Tasks/Active/`. `customersPerShift` 12 → 16 [GDD].
- `Tests/EditMode/Slice/SlicePersonaTests.cs`: persona bots (perfect / careless / slow, [GDD] bot timings 25/20/10 s, slow ×2) + seed-1..20 `Average()`; a TEMP `Explore_TuningGrid` test (remove before merge).
- 12 → config-driven counts in `SliceTests.cs` and `SliceBotTests.cs` (PlayMode, 2 lines; GAME-005 also touches this file: rebase by taking GAME-005's file and re-applying the two `customersPerShift` lines).

## First sweep (16 customers, seeds 1-20, avg satisfaction)
| budgetPerGram | patience | perfect | careless | slow |
|---|---|---|---|---|
| 4/6 (current) | ×1 | 90.4 | 70.8 | 46.2 |
| 4/6 | ×0.5 | 85.8 | 67.6 | 42.4 |
| 3/5 | ×1 | 90.4 | 70.8 | 46.2 |
| 2.5/4 | ×1 | 89.9 | 70.1 | 46.0 |
| 2/3.5 | ×1 | 88.9 | 69.0 | 45.4 |
Budgets barely matter; queue wait dominates. Perfect is already in band (80-95). Careless too high (target < 60): raise `acceptThreshold` (50 → ~60 makes a wrong-family pick 40 a reject sooner) — not yet swept. Slow too low (target 60-80): slow bot timings (50/40 s) may be too harsh, or soften `waitPenaltyPerSec`/cap.

## Left
- Sweep acceptThreshold and wait penalty; set values in SliceConfig.json; write `Docs/Design/TUNING_PS1.md` (before/after).
- Replace the TEMP grid with the sweep test (prints 3 averages, asserts bands) + skip-guarded PS1 exit hooks (strikes/trims after GAME-007/008).
- Last EditMode run: 142/150 pass, 8 fail (not yet triaged; likely 12→16 effects incl. seed-1 SOLD OUT assert, since customer count shifts the RNG used for start fills). PlayMode not run.

## Questions for Nolan (through the Hub)
- None yet. Hub: is changing slow-bot timing acceptable, or must slow hit 60-80 by config alone?
