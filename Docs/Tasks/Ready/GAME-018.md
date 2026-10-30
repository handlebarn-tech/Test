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
Compile / EditMode / PlayMode green; QA-002 gate green. Tests: Similar and Compare results equal the engine's direct call for the same input (parity, as the `EngineFeatureTests` class in `Tests/EditMode/ParserGoldenTests.cs`); a sold-out favourite yields the engine's Similar list (DP-024 part); each action advances time by its cost. DEC-013 gate.

## V2 additions (IMP-002, DEC-063)
V2 = `Docs/Design/DESIGN_V2/` (Nolan's add-on; DP wins on conflicts, DEC-063a). Row n = `Docs/Imports/IMP-001_DESIGN_V2_AUDIT.md` §2 row. All V2 numbers are [GDD] starting values (GAP-DP-02). Exploit tests: `DESIGN_V2/QA_TEST_PLAN.md`.
- **TFS input snapshot = parser input** (query text + chip + inventory snapshot id), hashed; never a structured fact-ID list sent to the engine (REVIEW-IMP1 A2, DEC-057; V2 `01_SYSTEM_CONTRACTS.md` §4 adapted; row 5). A result may change only when that hash or the inventory changes (V2 `15_TFS_ORACLE_CAPTURE_SPEC.md` "Known-input refinement").
- Stale result: if stock changes after the cards were shown, the card is marked stale and Confirm re-validates; a stale result never sells missing stock (V2 `08_UX_INTERACTION.md` §11, `16_CROSS_SYSTEM_INTEGRATION.md` §6; row 39; EX-020).
- A Similar/Compare re-run with an unchanged input hash counts as redundant (EX-011; V2 `10_EXPLOIT_FAILURE_ANALYSIS.md`; row 45).
- Parity oracle = the shipped engine (v7.11.4 + DEC-015/016, DEC-060; A1).

## Handoff
`Docs/Handoffs/GAME-018.md` (≤40 lines). Questions go to the Studio Hub (DEC-033).
