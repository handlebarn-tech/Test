# GAME-023 — Decision-pressure acceptance shift (spec §133)

**Role:** GAME / QA · **Priority:** P0 · **Branch:** `task/GAME-023` worktree off `main` (GAME-011, GAME-012, GAME-018..022 merged)

## Goal
Build the "highest-priority playable target" of `Docs/Design/SPEC_DECISION_PRESSURE.md` §133 and prove Gate D (§127): one deterministic full shift where an expert beats both "click the first card without enough information" and "ask every question" — without ever overriding TFS.

## Read
SPEC_DECISION_PRESSURE §118, §127, §133–135, §115 (DP-015..018, DP-027); `Docs/Design/ROADMAP_POST_SLICE.md` §2b–3; handoffs GAME-011, GAME-012, GAME-019..022.

## Owns
`Data/Scenarios/DP_AcceptanceShift.json` (new scenario; QA-002 harness format), bot strategies under `Tests/` (extend the GAME-010 persona harness), `Tests/EditMode/Gates/DpAcceptanceTests.cs`, a short tuning note appended to `Docs/Design/TUNING_PS1.md`. Simulation code only for missing hooks, listed in the handoff.

## Deliverable
1. One seeded 12–20-customer shift containing at least: 2 explicit easy, 2 ambiguous, 2 budget conflicts, 1 hidden still-unstated constraint, 1 no-perfect-service, 1 valid no-sale, 1 repeat, 1 repeat with changed preference, 1 stock substitution, 1 rush, 1 proactive-restock opportunity, 1 multi-system collision (§133).
2. Three bots on the pure sim: expert (asks the high-value questions, uses Similar/Compare when it pays, restocks in the recovery window), first-card (zero questions), ask-everything.
3. DP-027 multi-system collision: ambiguous customer + 3-person queue + critical jar + no help → at least three viable strategies with different SERVICE/FLOW/OPERATIONS strengths; none maximises all three.
4. A results table: per bot, the three scores, mean DecisionQuality, resolution mix vs the §118 sanity ranges.

## Validation
Compile / EditMode green; QA-002 gate green for every query used. Expert > first-card and expert > ask-everything on overall rating and mean DQ; DP-015..018 pass on this shift; outcomes impossible to perfect exist; a correct no-sale is possible. DEC-013 gate.

## Handoff
`Docs/Handoffs/GAME-023.md` (≤40 lines) with the results table. Questions go to the Studio Hub (DEC-033).
