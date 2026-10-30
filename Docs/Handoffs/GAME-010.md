# Handoff: GAME-010 (retune for tension + QA bot personas)

**Status:** done, pending review. Two of three bands not met; see Gaps. Branch `claude/task-game-010-2ab042`; main merged in (GAME-006 cart 0fca821, GAME-007 limits dba04b4). No Domain edits.

## Changes
- `SliceConfig.json` ([GDD], before → after; full table and reasons in `Docs/Design/TUNING_PS1.md`): customersPerShift 12→16; arrival gaps 45/15→150/60 s (DEC-056 shift 25–40 min); patience N/R/P 150/90/120→300/180/240 (O13 waits); fast/slowSeconds 30/120→20/90; rushPatienceMult 0.75→1.0 (DEC-082); twoItemAskChance 0.25→0.5 (W4W m3); overLimitAskChance 0.06→0.1 (W5G m4, seed 1 now has 1); lowStockFraction 0.25→0.10 (keeps seed 1's DEC-027 SOLD OUT with 16 customers).
- `Tests/EditMode/Slice/SlicePersonaTests.cs` (new): `Persona` perfect / careless / slow (human pacing 45/30/15 s, slow 2×), `Run()` sells through the cart and follows the GAME-007 trim rule (careless ignores limits), `Sweep_Seeds1To20` (Explicit, Balance, ~75 s), `PerfectBot_Seed1_Below100_BeatsCarelessAndSlow` (PS1 exit part 1), `OverLimit_PerfectTrims_CarelessLosesTheSale`, `CarelessBot_GetsAStrike` ([Ignore] until GAME-008 adds a strike source), `Explore_TuningGrid` (Explicit, Explore).
- Value fixes in tests for the new config: `SliceTests` (16 customers, spawn time, SpeedFit rows, clock worst case), `SliceBotTests` (count from config), `CartTests` line 168 (over-limit customers excluded: they are OverLimitTests' job).
- Env: this worktree had LFS pointers for the JarFill FBXs (6 JarFillImportTests failures); `git lfs pull` fixed it. No code change.

## Sweep (seeds 1–20, avg satisfaction)
| perfect | careless | slow |
|---|---|---|
| **84.0** (80–95 ✅) | **64.0** (< 60 ❌, accepted DEC-082) | **52.0** (60–80 ❌) |
Seed 1: perfect 83.7 (< 100: PS1 exit part 1 ✅), careless 62.4, slow 43.1. Shifts 32–36 min. Units/sale ≈ 1.5 (cap: 2 asks).

## Validation (studio.ps1, DEC-013 gate)
- EditMode: **197 passed, 0 failed, 2 skipped** (sweep run un-Explicit for this gate, then Explicit again; grid; GAME-008 strike hook). PlayMode: **8 passed, 1 skipped** (GPU capture); slice bot 16/16 served, $602.90, SOLD OUT Rainbow Drip. Compile clean (0 CS errors). Goldens (prices, intents, TfsParity Gate A) unchanged and green.

## Gaps / decisions for the Hub
1. **Slow 52.0 < 60, still open.** DEC-082's `rushPatienceMult` 1.0 had no effect (walkouts 4.3→4.4): a slow 2-item service (≈ 4 min) exceeds the 150 s gap all shift, so walkouts are structural, not rush-only. Left: slow = 1.5×, or accept.
2. **Careless 64.0 > 60: accepted for PS1 (DEC-082).** §3.2 fit is lenient (random chip averages fit 0.68); price + speed give up to 40 points anyway. Needs a DES call on fit sharpness (sim change) or GAME-008 strikes.
3. `budgetPerGram` inert: no change (DEC-082).
4. `SLICE_DESIGN.md` §1/§2.1/§8 still show the old values (12 customers, 45/15 s, patience 150/90/120); not in my Owns; DOC-002 (DEC-082).

## Overlap / rebase
- GAME-005 (`SliceBotTests.cs`): my only change is `customersPerShift` instead of 12 (2 lines). If it conflicts, take theirs and re-apply that.
- GAME-008 (active): flip `CarelessBot_GetsAStrike`'s [Ignore] once ID checks strike. It also edits `SliceConfig.json` and the bots: keep my values.
- The PlayMode slice bot is unchanged apart from the count; with 150 s gaps a seed-1 shift is ~1 900 sim s (about 95 s real at timeScale 20, deadline 240 s).

## Questions for Nolan (through the Hub)
- None. Items 1–3 are design calls for the Hub/DES.
