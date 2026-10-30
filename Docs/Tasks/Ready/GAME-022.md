# GAME-022 — Difficulty profiles + no-perfect-service patterns

**Role:** GAME · **Priority:** P1 · **Branch:** `task/GAME-022` worktree off `main` (GAME-019 merged; QA-002 merged; **GAME-021 merged**: both touch `Customers.cs` generator code, so they run one after the other; AUDIT-001 A3, DEC-064)

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

## V2 additions (IMP-002, DEC-063)
V2 = `Docs/Design/DESIGN_V2/` (Nolan's add-on; DP wins on conflicts, DEC-063a). Row n = `Docs/Imports/IMP-001_DESIGN_V2_AUDIT.md` §2 row. All V2 numbers are [GDD] starting values (GAP-DP-02). Exploit tests: `DESIGN_V2/QA_TEST_PLAN.md`.
- Starting preset numbers (V2 `04_DIFFICULTY_SYSTEM.md` §4; row 29): multi-constraint 15–25 / 35–50 / 55–70 %; patience × 1.35 / 1.00 / 0.88; meaningful restocks 1–3 / 2–4 / 3–5; concurrent major tasks 0–1 / 1 / 1–2.
- **Ambiguity uses DP tiers 0–4** (audit C1). V2's 0–3 shares re-mapped: Standard **25/40/25/5/5** (V2 Standard 25/40/25/10, with V2 tier 3 split evenly into DP tiers 3 and 4; REVIEW-W4V m2, DEC-066; was "e.g. 25/40/20/10/5").
- **PressureBudget:** each shift gets points (Beginner 2–5, Standard 6–10, Expert 10–15) spent on high-ambiguity slots, no-perfect-fit slots, rush tier, critical opening stock, etc. Generation cannot exceed it (V2 04 §5; row 30; EX-068).
- Viability bands solvable / tradeoff / no-viable per profile (V2 02 §7; row 15). The viability check calls the engine through the DEC-052 oracle on the true profile; there is no V2-side fit model (audit C6).
- Archetype shares 22/24/14/16/14/10 with a 35 % cap per shift, as a Standard placeholder (V2 02 §5; row 13).
- Raise difficulty in this order: ambiguity → constraint combos → inventory trade-offs → concurrency → traffic → patience last (V2 04 §6; row 29).
- Assists stay separate from difficulty; targets are assist-aware; no hidden dynamic difficulty (V2 04 §11–12; row 31). The 5 player sliders (V2 04 §3) wait until the presets play well.
- QA-091 (weigh tolerance parity) joins DP-028 (V2 `11_MASTER_QA_SCENARIOS.md`; row 46).

## Handoff
`Docs/Handoffs/GAME-022.md` (≤40 lines). Questions go to your department lead (DEC-033, DEC-094).
