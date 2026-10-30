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

## V2 additions (IMP-002, DEC-063)
V2 = `Docs/Design/DESIGN_V2/` (Nolan's add-on; DP wins on conflicts, DEC-063a). Row n = `Docs/Imports/IMP-001_DESIGN_V2_AUDIT.md` §2 row. All V2 numbers are [GDD] starting values (GAP-DP-02). Exploit tests: `DESIGN_V2/QA_TEST_PLAN.md`.
- The per-customer record stores the **parser input** (query text + chip + inventory snapshot id) and its hash, not a fact-ID path (REVIEW-IMP1 A2, DEC-057; V2 `01_SYSTEM_CONTRACTS.md` §5 DecisionRecord adapted; row 5).
- Reports are projections of recorded events; no separate counters that can drift. Event names start from V2's 24-event list (V2 `16_CROSS_SYSTEM_INTEGRATION.md` §17–18; row 47; EX-060).
- Abandonment attribution player vs structural: an abandonment counts against the player only for redundant consultation, avoidable idle, rework or preventable stock interruptions (V2 `03_SHIFT_PACING_QUEUE_MODEL.md` §11; row 27; EX-005, EX-061).
- Repetition telemetry flags: any opener family > 12 %, same intent > 25 %, same top product > 30 % (V2 `09_CONTENT_LONGEVITY.md` §10; row 20).
- Failure output: seed, fixture ids, input/output hashes, ledger diffs (V2 `11_MASTER_QA_SCENARIOS.md` "Failure reporting"; row 46).
- **Acceptance (A3, DEC-052):** the report section "questions that would have mattered" names the question only, with no TFS scores, ranks or result lists.

## DES-006 amendments (recommendation depth, DEC-096)
Source: `Docs/Design/RECOMMENDATION_DEPTH_AUDIT.md` (**RDA**).
- **Record (D1)** also stores the said/term pairs, verbatim vs translated, refine keys used, the New-customer toggle state and the outcome kind (Ok / Fallback / None / Help / AskEffectForBudget / Strain).
- **Explanation (D3)** may say `[GAME] they said "…"; you searched it as "…"`. It never says which reading was right.
- **`ShallowSaleRate`** = sales on a tier ≥ 2 customer with 0 questions, 0 re-reads or refines and 1 search. It goes in the shift log, the debug panel and GAME-010's persona table, and is the DEC-096 KPI for playtest 2. Target [GDD]: perfect bot ≈ 0; a tiles-only bot loses SERVICE.
- The Consultation tab adds a plain count, `Misread requests` (no scores).

## Handoff
`Docs/Handoffs/GAME-020.md` (≤40 lines). Questions: resolve from the sources in STUDIO_OS §0.6 first, then list the rest for the Hub (DEC-033/105).
