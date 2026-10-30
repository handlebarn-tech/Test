# GAME-020 — Decision telemetry, debug explanation, SERVICE / FLOW / OPERATIONS scoring

**Role:** GAME / QA · **Priority:** P1 · **Branch:** `task/GAME-020` worktree off `main` (GAME-019 merged)

## Goal
Spec DP-008 (`Docs/Design/SPEC_DECISION_PRESSURE.md` §34–35, §101–117): every customer and shift is logged and explainable, TFS values and gameplay values are labelled apart, and the shift score stops being an average of customer satisfaction.

## Read
SPEC_DECISION_PRESSURE §2.6, §34–35, §101–117; `Docs/GAMEPLAY_SIMULATION_SPEC.md` §37, §42–43, §80, §94–95; `Docs/Specs/SLICE_DESIGN.md` §5 (current stars); `Docs/Design/TUNING_PS1.md` (GAME-010); `Docs/Specs/UX_COUNTER_INTEL.md` (UX-005 debug panel + report sections); `Docs/Handoffs/GAME-019.md`.

## Owns
`Simulation/Slice/` (`ShiftReport` extension, a per-customer `ServiceRecord`, log writer), `Presentation/Slice/` report sections + dev debug panel (F3, debug builds only, GSS §80), SliceConfig new keys, EditMode tests. No `Code/Domain/` edits.

## Deliverable
1. Per-customer record (§116): archetype, ambiguity tier, KNOWN state at recommendation, **exact TFS query/input**, questions/relevant questions, completeness, wait, consultation time, TFS candidates and order (labelled TFS), chosen batch, best resolution, utilities, regret, DQ, satisfaction, resolution, purchase. Stored on the transaction as `recommendationContext` (GSS §37).
2. Per-shift log (§117), JSON next to today's report output, seed + difficulty included.
3. Rejection explanation (§114): TFS query used, card chosen, facts not yet learned, gameplay cause. Never "the game knew the card was wrong".
4. `ServicePerformance` (§34) and QuestionEfficiency (§35); SERVICE, FLOW, OPERATIONS scores (§102–104; OPERATIONS uses what exists now: stockouts, inventory errors, strikes; restock rows wait for GAME-012); revenue separate (§105).
5. Star gate (§106) + severe-failure caps (§107: GAME-007 strikes/manager review, avoidable abandonment, repeated major mistakes) **replacing** the satisfaction-average stars; GAME-010's persona targets are re-run and the before/after table goes in the handoff.
6. Report v2 sections (§108–112) and the debug panel fields (§113), TFS fields and gameplay fields visually separated; `DecisionQuality` never shown as a fit score.

## Validation
Compile / EditMode / PlayMode green; QA-002 gate green. Tests: every DP scenario from GAME-017/019 produces a complete record and an explanation; a speed-only and a detail-only bot each lose at least one category (pre-check for DP-029/030); revenue does not move the star gate. DEC-013 gate.

## Handoff
`Docs/Handoffs/GAME-020.md` (≤40 lines). Questions go to the Studio Hub (DEC-033).
