# GAME-019 — Service evaluation + resolutions (DecisionQuality, no-sales, ASK_* responses)

**Role:** GAME · **Priority:** P1 · **Branch:** `task/GAME-019` worktree off `main` (GAME-017 and GAME-018 merged)

## Goal
Spec DP-002 + DP-003 + part of DP-004 (`Docs/Design/SPEC_DECISION_PRESSURE.md` §19–33, §38): grade how well the player handled the fictional customer, separately from customer satisfaction and from the TFS engine. A correct no-sale can earn credit; a lazy one can't.

## Read
SPEC_DECISION_PRESSURE §0A (evaluation boundary), §2.4–2.6, §14, §19–33, §38, §115 (DP-004..009, 013..015), §126; `Docs/GAMEPLAY_SIMULATION_SPEC.md` §12, §15–17, §36, §58; `Docs/Specs/SLICE_DESIGN.md` §3; `Docs/Design/DES-003_RECONCILIATION.md` (name mapping, DEC-052 (was DEC-P1)); `Docs/Handoffs/GAME-017.md`, `GAME-018.md`.

## Owns
`Simulation/Slice/` new `ServiceEvaluator.cs` (+ moving `ShiftSim.Fit/Score` into it unchanged in behaviour), `Response`/outcome extensions, no-sale action; `Presentation/Slice/` no-sale button + ASK_* lines per UX-005; SliceConfig/SliceLines new keys; EditMode tests. No `Code/Domain/` edits.

## Deliverable
1. `ServiceEvaluator` (evaluation layer, its own class and test file): `ServiceUtility` = TFS alignment (today's `Fit`: the engine's own ranking for the *true* intent, DEC-052 (was DEC-P1)) + constraint, budget, quantity, similar-request, consultation and availability handling (§19). Hard vs soft constraints per §20. Evaluated on events only (§122). It may call the engine; it never changes what the player sees.
2. `BestAvailableResolution` over the service actions available at decision time (§21: sell ranked / other valid candidate, ask another question, Similar, Compare, cheaper valid alternative, informed no-sale; retrieve/restock once GAME-012 exists) → `DecisionRegret`, `DecisionQuality` (§22–23, `decisionRegretTolerance` [GDD] + the §23 bands).
3. Per-customer purchase threshold drawn around `acceptThreshold` [GDD] (§25); `Response` extended in place with ASK_CHEAPER / ASK_STRONGER / ASK_LESS_SEDATING / ASK_SIMILAR / ASK_WHY / COMPARE (GSS §17); each ASK_* reveals a KNOWN field via GAME-017's hook (§27).
4. Player action "Nothing fits right now" → `InformedNoSale` when no viable TFS-supported path meets the customer's stated willingness to buy, else `AvoidableNoSale` (§30–31). `ServiceResolution` enum (§32) beside the kept `CustomerOutcome`.
5. Consultation-depth fit (§14) added as a satisfaction term (existing `Satisfaction` formula keeps its name and weights; one new weight [GDD]). `QueueCost` = Σ waiting patience loss per action, hidden (§38).

## Validation
Compile / EditMode / PlayMode green; QA-002 gate green (the evaluator must not touch engine state). Tests: DP-004 budget conflict, DP-005 flexible budget, DP-006 no perfect resolution → moderate satisfaction + excellent DQ, DP-007 satisfied customer + heavy queue damage → DQ/flow reduced, DP-008 correct no-sale, DP-009 avoidable no-sale, DP-013/014 enthusiast normal vs rush, DP-015 queue triage (one high-value question worth it, five not). Reproducible by seed. DEC-013 gate.

## V2 additions (IMP-002, DEC-063)
V2 = `Docs/Design/DESIGN_V2/` (Nolan's add-on; DP wins on conflicts, DEC-063a). Row n = `Docs/Imports/IMP-001_DESIGN_V2_AUDIT.md` §2 row. All V2 numbers are [GDD] starting values (GAP-DP-02). Exploit tests: `DESIGN_V2/QA_TEST_PLAN.md`.
- **Question that mattered (counterfactual):** after the customer, re-run the engine on the parser input plus one unasked, legitimately available answer; a question is *critical* if the result set or a hard constraint changes (V2 `01_SYSTEM_CONTRACTS.md` §6, `05_PROGRESSION_CAREER.md` §3.1; row 6). Evaluation only (DEC-052). It feeds **DecisionRegret** (a missed critical fact adds regret). It is not a separate DQ term: DP's regret-based DecisionQuality stays (audit C2, DEC-063a).
- RQ / NSJ score bands as starting regret values (V2 05 §3.2, §3.4; row 32).
- BestAvailableResolution ordering, applied over service actions: feasibility → known hard constraints → availability → engine rank as exposed → non-chemistry preferences → operational tie-break (V2 01 §7; row 7).
- Follow-up loop cap: at most 2 follow-ups; a third needs an Enthusiast/Indecisive customer (V2 02 §18; row 22).
- Active-service patience: useful consultation slows decay (0.25–0.50×), redundant loops speed it up (1.25×), relief capped at 60 s per customer (V2 `03_SHIFT_PACING_QUEUE_MODEL.md` §8; row 26).
- Purchase threshold: the customer judges the product with the DEC-052 oracle on the **true** intent (audit C3). V2's price, wait, consultation and repeat terms (02 §17) may be the threshold's other components.
- **Acceptance (A3, DEC-052):** the report may name the question that would have mattered; it never shows TFS scores, ranks or a re-run result list.
- Exploits: EX-002, 003, 004, 008, 009, 010, 066 (V2 `10_EXPLOIT_FAILURE_ANALYSIS.md`; row 45).

## Handoff
`Docs/Handoffs/GAME-019.md` (≤40 lines), including the tuning table of new [GDD] keys. Questions go to the Studio Hub (DEC-033).
