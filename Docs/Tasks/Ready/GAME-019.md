# GAME-019 — Service evaluation + resolutions (DecisionQuality, no-sales, ASK_* responses)

**Role:** GAME · **Priority:** P1 · **Branch:** `task/GAME-019` worktree off `main` (GAME-017 and GAME-018 merged)

## Goal
Spec DP-002 + DP-003 + part of DP-004 (`Docs/Design/SPEC_DECISION_PRESSURE.md` §19–33, §38): grade how well the player handled the fictional customer, separately from customer satisfaction and from the TFS engine. A correct no-sale can earn credit; a lazy one can't.

## Read
SPEC_DECISION_PRESSURE §0A (evaluation boundary), §2.4–2.6, §14, §19–33, §38, §115 (DP-004..009, 013..015), §126; `Docs/GAMEPLAY_SIMULATION_SPEC.md` §12, §15–17, §36, §58; `Docs/Specs/SLICE_DESIGN.md` §3; `Docs/Design/DES-003_RECONCILIATION.md` (name mapping, DEC-P1); `Docs/Handoffs/GAME-017.md`, `GAME-018.md`.

## Owns
`Simulation/Slice/` new `ServiceEvaluator.cs` (+ moving `ShiftSim.Fit/Score` into it unchanged in behaviour), `Response`/outcome extensions, no-sale action; `Presentation/Slice/` no-sale button + ASK_* lines per UX-005; SliceConfig/SliceLines new keys; EditMode tests. No `Code/Domain/` edits.

## Deliverable
1. `ServiceEvaluator` (evaluation layer, its own class and test file): `ServiceUtility` = TFS alignment (today's `Fit`: the engine's own ranking for the *true* intent, DEC-P1) + constraint, budget, quantity, similar-request, consultation and availability handling (§19). Hard vs soft constraints per §20. Evaluated on events only (§122). It may call the engine; it never changes what the player sees.
2. `BestAvailableResolution` over the service actions available at decision time (§21: sell ranked / other valid candidate, ask another question, Similar, Compare, cheaper valid alternative, informed no-sale; retrieve/restock once GAME-012 exists) → `DecisionRegret`, `DecisionQuality` (§22–23, `decisionRegretTolerance` [GDD] + the §23 bands).
3. Per-customer purchase threshold drawn around `acceptThreshold` [GDD] (§25); `Response` extended in place with ASK_CHEAPER / ASK_STRONGER / ASK_LESS_SEDATING / ASK_SIMILAR / ASK_WHY / COMPARE (GSS §17); each ASK_* reveals a KNOWN field via GAME-017's hook (§27).
4. Player action "Nothing fits right now" → `InformedNoSale` when no viable TFS-supported path meets the customer's stated willingness to buy, else `AvoidableNoSale` (§30–31). `ServiceResolution` enum (§32) beside the kept `CustomerOutcome`.
5. Consultation-depth fit (§14) added as a satisfaction term (existing `Satisfaction` formula keeps its name and weights; one new weight [GDD]). `QueueCost` = Σ waiting patience loss per action, hidden (§38).

## Validation
Compile / EditMode / PlayMode green; QA-002 gate green (the evaluator must not touch engine state). Tests: DP-004 budget conflict, DP-005 flexible budget, DP-006 no perfect resolution → moderate satisfaction + excellent DQ, DP-007 satisfied customer + heavy queue damage → DQ/flow reduced, DP-008 correct no-sale, DP-009 avoidable no-sale, DP-013/014 enthusiast normal vs rush, DP-015 queue triage (one high-value question worth it, five not). Reproducible by seed. DEC-013 gate.

## Handoff
`Docs/Handoffs/GAME-019.md` (≤40 lines), including the tuning table of new [GDD] keys. Questions go to the Studio Hub (DEC-033).
