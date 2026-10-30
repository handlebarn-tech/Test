# Handoff: GAME-010b (DEC-086: slow 1.5×, bots work the ID stand)

**Status:** done, pending review. Branch `claude/task-game-010b` (off `main` 9694550). Test and doc changes only: no Simulation, Presentation or config edits.

## Changes
- `Tests/EditMode/Slice/SlicePersonaTests.cs`
  - Slow persona = 1.5× perfect: 67.5 / 45 / 22.5 s (REVIEW-W5M m1).
  - Every bot accepts GAME-008's cover prompt and works the stand between counter actions. A new `Persona.IdSec` sets the time per ID: perfect 10 s, slow 15 s, careless 5 s. Perfect and slow admit or refuse by `IdRules`; careless admits everyone (REVIEW-W5N m1).
  - `CarelessBot_GetsAStrike` [Ignore] → `CarelessBot_GetsAStrike_PerfectDoesNot`: the first seed in 1–20 where careless strikes is seed 3; perfect gets 0 on that seed.
  - Sweep rows also print IDs checked and strikes.
  - Sweep and grid stay `[Explicit]` (DEC-072).
- `Tests/EditMode/Slice/SliceTests.cs`
  - `RunBot(..., workStand)` admits valid IDs and refuses bad ones. Without the flag the stand is still never worked, which `IdCheckTests.AnIgnoredStand_…` relies on.
  - `SimBot_Seed1` runs with `acceptCover + workStand`, asserts no strikes, and counts Refused customers in the outcome sum.
- `Docs/Design/TUNING_PS1.md`: new bands. The m2 text says 63.1 (was "65" against a table showing 64.0). Slow row and the exploration log updated.

## Balance sweep (seeds 1–20, run once, un-Explicit for that gated run only)
| perfect | careless | slow |
|---|---|---|
| **84.1** (80–95 ✅) | **63.1** (< 60, accepted DEC-082) | **68.8** (60–80 ✅) |
- The cover prompt came on 9 of 20 seeds (27 IDs checked). Careless took 6 strikes; perfect and slow took 0.
- Seed 1: perfect 83.7, careless 61.6, slow 59.9.

## Validation (studio.ps1, DEC-013; `slots` showed 0/2 before the run)
- EditMode: **208 passed, 0 failed, 1 skipped** (the Explore grid). Gate A (TfsParity) and the goldens are green.
- PlayMode: not re-run. No PlayMode test, runtime code or config changed; the last PlayMode run on main is green.
- Seed 1 gets no cover prompt (`cover=None`), so `SimBot_Seed1` doesn't exercise the stand on that seed. `IdCheckTests` and the persona strike test cover it.

## Overlap
- GAME-009 (medical, parallel) may touch `SliceTests.cs` (RunBot) and `SliceConfig.json`. My edits are the `workStand` lines in RunBot and the SimBot_Seed1 hunk; on conflict, keep both. No config edits here.
- DEC-048 (medical < 5 %): the bots do nothing medical-specific; GAME-009 can add a MED-aware rule to `Persona` if needed.

## Questions for Nolan (through the Hub)
- None.
