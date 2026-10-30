# TUNING_PS1 — slice retune for tension (GAME-010)

Goal (ROADMAP_POST_SLICE §2, GAME-010): good play is rewarded but no longer automatic. Measured with the pure-sim QA bots in
`Code/Tests/EditMode/Slice/SlicePersonaTests.cs`, seeds 1–20, after GAME-006 (cart) merged. Score = report `avgSatisfaction`
(walkouts count 0).

## Bots (QA pacing, [GDD]; not game config)
| Persona | Chip | Card | Service pacing (per ask: pick → present; accept → POS) |
|---|---|---|---|
| perfect | true family | best `wFit·fit + wPrice·priceFit` over cards 1–3 + one More options page | pick 45 s, POS 30 s, re-pick 15 s |
| careless | random family | random fillable card, blind to budget and limits | same as perfect |
| slow | as perfect | as perfect | 2× (90 / 60 / 30 s) |
Pacing is human-scale: RES-001 O13 median transaction 2.3 min. Every ask is sold through the cart (`AddItem`, then `Confirm()`).

## Changed values (all [GDD], `Data/Slice/SliceConfig.json`)
| Key | Before | After | Why |
|---|---|---|---|
| `customersPerShift` | 12 | 16 | GAME-010 packet / PS1 exit test |
| `arrivalGapNormalSec` | 45 | 150 | DEC-056: a shift of 25–40 real min (16 customers ≈ 32–36 min with human pacing) |
| `arrivalGapRushSec` | 15 | 60 | the one rush (customers 6–9) still backs the queue up, without guaranteed walkouts |
| patience N / R / P (s) | 150 / 90 / 120 | 300 / 180 / 240 | RES-001 O13: average walk-in wait 3.7 min, median 1.4 min |
| `fastSeconds` / `slowSeconds` | 30 / 120 | 20 / 90 | speed matters at human pace (perfect picks at 45 s → speedFit 0.64) |
| `twoItemAskChance` | 0.25 | 0.5 | REVIEW-W4W m3: units/sale toward the real ≈ 2 (O13); the generator caps at 2 asks, so ≈ 1.5 |
| `lowStockFraction` | 0.25 | 0.10 | 16 customers shift the seeded jar fills (customers draw first); at 0.25 seed 1 lost its DEC-027 SOLD OUT, at 0.10 it sells out on 17/20 seeds. LOW label now < 10 % |

Unchanged on purpose: `budgetPerGram` {4, 6} (every grid from {2, 3.5} to {4, 6} moved perfect by < 1.5 points: the Tue smalls deal
and the house tier meet almost every budget, so the budget is inert in the slice); `acceptThreshold` 50 (60/65/70 moved careless by
≤ 2 points, it only turns accepts into no-sales that still record their last score); weights `wFit/wPrice/wSpeed`.

## Result (seeds 1–20)
`Sweep_Seeds1To20` (Explicit, category Balance, ~75 s), final config:

| Persona | avg satisfaction | target | walkouts | no-sales | units/sale |
|---|---|---|---|---|---|
| perfect | **85.6** | 80–95 ✅ | 0.5 | 0.0 | 1.50 |
| careless | **64.9** | < 60 ❌ | 0.3 | 4.5 | 1.43 |
| slow | **52.3** | 60–80 ❌ | 4.7 | 0.0 | 1.51 |

Seed 1 (default suite, `PerfectBot_Seed1_Below100_BeatsCarelessAndSlow`): perfect 80.9, careless 59.3, slow 46.1.
Shift length ≈ 32–36 sim min (= real min at timeScale 1). Seed-1 card-1 bot (`SimBot_Seed1…`): 16/16 served, sat 98.1, SOLD OUT Rainbow Drip.

## Gaps (for the Hub)
- **Slow below band (52 vs 60–80).** Its losses are walkouts (4.7/shift, score 0), mostly around the rush. Config can lift it
  (longer gaps or patience), but each step that saves slow also takes perfect's only pressure away (perfect hits 99+ when the
  queue never builds). Options: (a) define "slow" as 1.5× instead of 2×; (b) `rushPatienceMult` 0.75 → 1.0; (c) accept slow
  < 60 as the intended cost of being slow. Recommendation: (b), re-run the sweep; else (a). Not changed here (one decision per run).
- **Careless above band (65 vs < 60).** The §3.2 fit is lenient (a random chip averages fit 0.68 because Ms/Ms_top over the full
  strict list rarely drops far), and price + speed hand out up to 40 points regardless. No config value in GAME-010's scope
  separates it further without hurting perfect. Options: (a) GAME-007 strikes give careless its real penalty (PS1 exit test only
  needs ≥ 1 strike, hook ready); (b) a DES call on fit sharpness (e.g. rank-based fit), which is a scoring/sim change.
- `budgetPerGram` is inert (see above); making budgets bite needs a design change (e.g. budgets on non-deal days), not a value.

## Exploration log (all seeds 1–20, before → final)
| Setup | perfect | careless | slow |
|---|---|---|---|
| pre-cart, bots 25/20/10 s, gaps 45/15 (old pacing) | 90.4 | 70.8 | 46.2 |
| pre-cart, bots 15/15/5 s | 99.7 | 75.6 | 68.3 |
| cart, human bots, gaps 110/30, patience ×1.5, two 0.5 | 79.7 | 59.5 | 40.2 |
| cart, human bots, gaps 150/40, patience ×2, speed 30/120 | 84.5 | 63.5 | 53.1 |
| cart, human bots, gaps 150/40, patience ×2, speed 20/90 | 80.8 | 59.6 | 51.3 |
| **final**: gaps 150/60, patience ×2, speed 20/90, two 0.5 | 85.6 | 64.9 | 52.3 |
Findings: (1) with any pacing, slow = 2× perfect cannot both stay in its band unless arrivals leave slack, because the queue,
not the score formula, is what separates them (walkouts score 0); (2) the fit model is lenient (a random chip still averages fit
0.68), so careless only drops when two-item asks and queue pressure add up.
