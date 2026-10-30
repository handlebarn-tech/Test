# REVIEW-W5S — GAME-010b (DEC-086: slow persona 1.5×, bots work the GAME-008 ID stand, careless strike test live)

**Verdict: PASS with minors (GO to merge).** I merged `claude/task-game-010b` (eae2aeb) `--no-ff` into `review/wave-5s`, cut from main ce63bab. The merge was clean. The diff is tests and docs only (`SlicePersonaTests.cs`, `SliceTests.cs`, `TUNING_PS1.md`, the handoff). There are no edits to `Code/Domain/`, Simulation, Presentation or config.

## Gates (studio.ps1, one editor; GAME-009's EditMode run held the other slot)
- `unity-compile`: csErrors=0.
- `unity-test-edit`: 209 total, 207 passed, 0 failed, 2 skipped. Both skipped tests are `[Explicit]`: `Explore_TuningGrid` and `Sweep_Seeds1To20` (DEC-072).
- **Gate A (DEC-067):** `TfsParityGateTests` 11/11, `EngineGoldenTests` 23/23, `ParserGoldenTests` 95/95.
- `unity-test-play`: 8 passed, 1 skipped (GPU capture).
- I did not run `unity-capture`, because no scene, runtime or UI code changed.

## Checks
- **DEC-086 slow = 1.5×: PASS.** Slow's timings are 67.5 / 45 / 22.5 s, exactly 1.5 × perfect's 45 / 30 / 15 s. Its ID time is 15 s, also 1.5 × perfect's 10 s.
- **The bots answer the cover prompt (REVIEW-W5N m1): PASS.**
  - Every persona accepts the cover prompt and works the stand before the next counter action.
  - Perfect and slow judge each ID with `sim.IdValid`. Careless admits everyone.
  - The counter's pick deadline is now `max(next, ServiceStart) + PickSec`, so time spent at the stand delays the counter instead of overlapping it.
  - `RunBot` gains `workStand`. It is off by default, so `IdCheckTests.AnIgnoredStand_…` keeps its meaning.
- **PS1 exit test, part 2: PASS.** `CarelessBot_GetsAStrike_PerfectDoesNot` is live and passes. The log shows "seed 3: careless strikes 1 (An invalid ID got through)", and perfect has 0 strikes on seed 3.
- **Seed-1 results: PASS.** The seed-1 tests pass with perfect 83.7, careless 61.6 and slow 59.9. The re-run's seed-1 log matches the handoff.
- **The 20-seed sweep (84.1 / 63.1 / 68.8) is the worker's run; I did not re-run it.** The sweep is Explicit and takes about 75 s. TUNING_PS1's table and exploration log agree with the handoff, and REVIEW-W5M m2 (the "65" text) is fixed.

## Minors
- m1 `TUNING_PS1.md` line 46 still gives the seed-1 numbers as careless 62.4 and slow 43.1. The current values are 61.6 and 59.9, from the handoff and this run's log. Fix this in the next TUNING edit.
- m2 Seed 1 has no cover prompt (`cover=None`). So in the default suite, `SimBot_Seed1`'s new "a lawful bot never strikes" assert and `RunBot`'s `workStand` branch never act.
  - The lawful-judge path is covered only through the persona bot (perfect on seed 3).
  - Fix: a seeded `RunBot(..., workStand: true)` run on a seed with a cover prompt would cover it.
- m3 Careless's ID behaviour hangs on `!p.TrueChip`, which couples "random chip" to "admits every ID". This is fine for three personas. A separate `JudgesIds` flag would be clearer if more personas are added.
- m4 Overlap with GAME-009, which was running EditMode on `claude/task-game-009` during this review. Both branches touch `SliceTests.cs` `RunBot`. The handoff's rule applies: on conflict, keep both.
