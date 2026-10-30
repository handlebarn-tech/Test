# REVIEW-W5M — GAME-010 (retune for tension + QA bot personas)

**Verdict: PASS with minors (GO to merge).** `claude/task-game-010-2ab042` @ 2d81a7b merged `--no-ff` into `review/wave-5m` off main 1abafc1; clean merge (no conflict with GAME-006/007; GAME-007 and DEC-082 are already in the branch's base). Changes: `SliceConfig.json` values, new `SlicePersonaTests.cs`, small test fixes (`SliceTests`, `SliceBotTests`, `CartTests`), `TUNING_PS1.md`, handoff. No `Code/Domain/` or runtime edit.

## Gates (single editor via `studio.ps1`; two editors at once not tested)
- `unity-compile` csErrors=0 (35 s). `unity-test-edit` **196 passed, 0 failed, 3 skipped** of 199 (65 s wall, 50 s in tests). `unity-test-play` 8 passed, 1 skipped (GPU capture), 131 s.
- **Gate A (DEC-067): green**: `TfsParityGateTests` pass, with the Engine/Parser goldens.

## Checks
- **Explicit tests (DEC-072) — PASS.** `Sweep_Seeds1To20` is `[Test, Explicit, Category("Balance")]` and `Explore_TuningGrid` is `[Test, Explicit, Category("Explore")]`; both skip in the default run (confirmed in the XML result). `CarelessBot_GetsAStrike` is `[Ignore]` until GAME-008 adds a strike source. The slowest default tests are `SellOut_IsTheOnlyAllowedChange` 9 s, `PerfectBot_Seed1…` 5 s, `Lines_EveryTemplateVariant…` 4 s, and `OverLimit_PerfectTrims…` 3 s.
- **Default EditMode speed — acceptable, slightly over the target.** About 50 s in tests (65 s wall) against the "~30 s class" you asked for. The extra time is Gate A (sell-out loop ×2 parser modes, added by QA-002b), not GAME-010's tests (its default tests add about 8 s). No sweep or grid runs by default.
- **Config vs TUNING_PS1 — PASS.** Every changed key matches the before/after table: customersPerShift 16, arrival gaps 150/60 s, patience 300/180/240, fast/slow 20/90, rushPatienceMult 1.0 (DEC-082), twoItemAskChance 0.5, overLimitAskChance 0.1, lowStockFraction 0.10. `budgetPerGram`, `acceptThreshold` and the weights are unchanged, as documented.
- **DEC-056 — PASS.** 16 customers with 150/60 s gaps give a 32–36 min shift (25–40 min target). Seed 1 still ends with a SOLD OUT jar (the reason for `lowStockFraction` 0.10; 17 of 20 seeds sell out).
- **DEC-082 — as ruled.** `rushPatienceMult` 0.75 to 1.0 was applied and had no effect on slow (52.5 to 52.0), which the handoff reports honestly. The result table: perfect **84.0** (band 80–95, met), careless **64.0** (target < 60, accepted for PS1), slow **52.0** (target 60–80, missed, reported only). The PS1 exit test part 1 holds (`PerfectBot_Seed1_Below100…`: perfect 83.7 on seed 1, beating careless 62.4 and slow 43.1). I did not re-run the Explicit sweep; the numbers are the handoff's.

## Minors
- m1 Slow's loss is structural (a 2-item slow service of about 4 min exceeds the 150 s arrival gap all shift), so no value in scope fixes it; options are slow = 1.5× or accept. The careless fit leniency needs a DES call (rank-based fit) or GAME-008 strikes (the hook is ready).
- m2 `TUNING_PS1.md` quotes careless as "65" in the gaps text and 64.0 in the table; harmless.
- m3 `SLICE_DESIGN.md` §1/§2.1/§8 still show the old values (12 customers, 45/15 s, patience 150/90/120); DOC-002 per DEC-082. Handoff overlap notes (GAME-008 flips `CarelessBot_GetsAStrike`'s `[Ignore]`; keep these values) stand.
- m4 The handoff noted that this worktree had LFS pointers for the JarFill FBX files (`git lfs pull` fixed it); the same applies to anyone running EditMode in a fresh worktree, not a code issue.
