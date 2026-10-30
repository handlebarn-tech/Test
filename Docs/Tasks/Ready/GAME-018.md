# GAME-018 — TFS workflows at the counter: Similar, Compare, Details

**Role:** GAME · **Priority:** P1 · **Branch:** `task/GAME-018` worktree off `main` (GAME-017 merged; UX-005 for the view)

## Goal
The player chooses *which* preserved TFS workflow to use (`Docs/Design/SPEC_DECISION_PRESSURE.md` §0A "allowed gameplay", §9 Q6, §21): Similar from a liked strain, Compare of 2–3 cards, Details. The engine already has them with goldens (GAME-003: `Responder` compare, `Similarity.Similar`, `Refine`); the slice UI cut them (SLICE_DESIGN §11). Each use costs time and moves consultation depth.

## Read
SPEC_DECISION_PRESSURE §0A, §9 (Q6), §14, §21, §29 (pattern F), §115 (DP-013, DP-024); `Docs/GAMEPLAY_SIMULATION_SPEC.md` §18–19, §28; `Docs/Handoffs/GAME-003.md`; `Docs/Specs/UX_COUNTER_INTEL.md` (UX-005).

## Owns
`Simulation/Slice/` (workflow actions on `ShiftSim`, time costs), `Presentation/Slice/` (Similar / Compare / Details per UX-005), SliceConfig/SliceLines new keys, EditMode tests. No `Code/Domain/` edits: call the ported functions as they are.

## Deliverable
1. **Similar:** from a KNOWN similar reference (Q6 or repeat memory later) → `Similarity.Similar` on live stock; results shown as the engine returns them, no game re-sort.
2. **Compare:** 2–3 shown cards → the engine's compare output (`Responder`), decision-relevant rows only (GSS §19).
3. **Details:** today's Inspect panel becomes a timed action.
4. Each action has a [GDD] time cost and adds to `ConsultationSeconds` / actual consultation depth (consumed by GAME-019).
5. Workflow-usage counters for the report (GAME-020: "TFS workflow usage quality").

## Validation
Compile / EditMode / PlayMode green; QA-002 gate green. Tests: Similar and Compare results equal the engine's direct call for the same input (parity, as `EngineFeatureTests`); a sold-out favourite yields the engine's Similar list (DP-024 part); each action advances time by its cost. DEC-013 gate.

## Handoff
`Docs/Handoffs/GAME-018.md` (≤40 lines). Questions go to the Studio Hub (DEC-033).
