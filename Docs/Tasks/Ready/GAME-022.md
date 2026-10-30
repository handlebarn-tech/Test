# GAME-022 — Difficulty profiles + no-perfect-service patterns

**Role:** GAME · **Priority:** P1 · **Branch:** `task/GAME-022` worktree off `main` (GAME-019 merged; QA-002 merged)

## Goal
Spec DP-007 (`Docs/Design/SPEC_DECISION_PRESSURE.md` §28–29, §66–70): difficulty changes information, complexity, scarcity and concurrency — never TFS results for identical inputs (DP-028, hard gate).

## Read
SPEC_DECISION_PRESSURE §2.4, §28–29, §66–70, §115 (DP-028), §118–119; `Docs/GAMEPLAY_SIMULATION_SPEC.md` §45 (amended); DEC-027 (seeded low jars); `Docs/Design/TUNING_PS1.md`; `Docs/Handoffs/GAME-019.md`.

## Owns
`Data/Slice/Difficulty/{Beginner,Standard,Expert}.json` (new), `Simulation/Slice/` profile loading + pattern generator in `CustomerGenerator`/inventory seeding, EditMode tests. No `Code/Domain/` edits; no profile key may reach engine options.

## Deliverable
1. `DifficultyProfile` (§67): ambiguity rate, multi-constraint rate, conflict rate, `noPerfectFitRate`, top-choice scarcity, arrival and patience multipliers, target concurrent tasks, repeat/enthusiast/indecisive rates, weigh tolerance, stock-pressure multiplier. Three profiles per §68–70 [GDD]; Standard = today's tuning.
2. No-perfect-service patterns A–G (§29) generated from valid operational combinations: budget vs TFS best fit, stock (via the DEC-027 low-jar seeding), stated-preference tension, quantity, similarity (needs GAME-018), multi-constraint; D (product type) waits for PS3. Rates per §28 starting ranges.
3. Difficulty and pattern ids recorded in GAME-020's shift log.

## Validation
Compile / EditMode / PlayMode green. **DP-028:** QA-002 gate extended so the same TFS query + inventory + pricing gives identical output under all three profiles. Each pattern produces at least one customer whose best resolution is below full satisfaction in a seeded run. Seed determinism. DEC-013 gate.

## Handoff
`Docs/Handoffs/GAME-022.md` (≤40 lines). Questions go to the Studio Hub (DEC-033).
