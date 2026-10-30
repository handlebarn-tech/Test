# Handoff: GAME-010 (retune for tension + QA bot personas)

**Status:** done, pending review. Two of three bands not met; see Gaps. Branch `claude/task-game-010-2ab042`; main merged in (GAME-006 cart 0fca821, GAME-007 limits dba04b4). No Domain edits.

## Changes
- `SliceConfig.json` ([GDD], before → after; full table and reasons in `Docs/Design/TUNING_PS1.md`): customersPerShift 12→16; arrival gaps 45/15→150/60 s (DEC-056 shift 25–40 min); patience N/R/P 150/90/120→300/180/240 (O13 waits); fast/slowSeconds 30/120→20/90; twoItemAskChance 0.25→0.5 (W4W m3); overLimitAskChance 0.06→0.1 (W5G m4, seed 1 now has 1); lowStockFraction 0.25→0.10 (keeps seed 1's DEC-027 SOLD OUT with 16 customers).
- `Tests/EditMode/Slice/SlicePersonaTests.cs` (new): `Persona` perfect / careless / slow (human pacing 45/30/15 s, slow 2×), `Run()` sells through the cart and follows the GAME-007 trim rule (careless ignores limits), `Sweep_Seeds1To20` (Explicit, Balance, ~75 s), `PerfectBot_Seed1_Below100_BeatsCarelessAndSlow` (PS1 exit part 1), `OverLimit_PerfectTrims_CarelessLosesTheSale`, `CarelessBot_GetsAStrike` ([Ignore] until GAME-008 adds a strike source), `Explore_TuningGrid` (Explicit, Explore).
- Value fixes in tests for the new config: `SliceTests` (16 customers, spawn time, SpeedFit rows, clock worst case), `SliceBotTests` (count from config), `CartTests` line 168 (over-limit customers excluded: they are OverLimitTests' job).
- Env: this worktree had LFS pointers for the JarFill FBXs (6 JarFillImportTests failures); `git lfs pull` fixed it. No code change.

## Sweep (seeds 1–20, avg satisfaction)
| perfect | careless | slow |
|---|---|---|
| **83.6** (80–95 ✅) | **62.9** (< 60 ❌) | **52.5** (60–80 ❌) |
Seed 1: perfect 79.2 (< 100: PS1 exit part 1 ✅), careless 57.1, slow 46.1. Shifts 32–36 min. Units/sale ≈ 1.5 (cap: 2 asks).

## Validation (studio.ps1, DEC-013 gate)
- EditMode: **196 passed, 0 failed, 3 skipped** (Explicit sweep/grid, GAME-008 strike hook; the sweep was run un-Explicit in the previous gated run). PlayMode: **8 passed, 1 skipped** (GPU capture); slice bot 16/16 served, $602.90, SOLD OUT Rainbow Drip. Compile clean (0 CS errors). Goldens (prices, intents, TfsParity Gate A) unchanged and green.

## Gaps / decisions for the Hub
1. **Slow 52.5 < 60.** Walkouts (4.3/shift) around the rush. Lifting it with gaps/patience removes perfect's only pressure. Options: `rushPatienceMult` 0.75→1.0 (recommended, one sweep), or define slow as 1.5×, or accept.
2. **Careless 62.9 > 60.** §3.2 fit is lenient (random chip averages fit 0.68); price + speed give up to 40 points anyway. Needs a DES call on fit sharpness (sim change) or GAME-008 strikes.
3. `budgetPerGram` is inert (Tue smalls deal and house tier meet almost every budget); budgets that bite need a design change.
4. `SLICE_DESIGN.md` §1/§2.1/§8 still show the old values (12 customers, 45/15 s, patience 150/90/120); not in my Owns. DES/Hub should point it at TUNING_PS1.

## Overlap / rebase
- GAME-005 (`SliceBotTests.cs`): my only change is `customersPerShift` instead of 12 (2 lines). If it conflicts, take theirs and re-apply that.
- GAME-008 (active): flip `CarelessBot_GetsAStrike`'s [Ignore] once ID checks strike. It also edits `SliceConfig.json` and the bots: keep my values.
- The PlayMode slice bot is unchanged apart from the count; with 150 s gaps a seed-1 shift is ~1 900 sim s (about 95 s real at timeScale 20, deadline 240 s).

## Questions for Nolan (through the Hub)
- None. Items 1–3 are design calls for the Hub/DES.
