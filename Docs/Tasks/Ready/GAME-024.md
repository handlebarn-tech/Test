# GAME-024 — Career competencies, promotion gates, versioned save v1

**Role:** GAME · **Priority:** P2 · **Branch:** `task/GAME-024` worktree off `main` (GAME-020 and GAME-023 merged; GAME-021 for memory persistence)

## Goal
Spec DP-009 (`Docs/Design/SPEC_DECISION_PRESSURE.md` §71–81, §120–121): career progression rewards balanced competence over several shifts, unlocks control (never a better recommendation engine), and survives between sessions.

## Read
SPEC_DECISION_PRESSURE §71–86, §115 (DP-029..031), §120–121, §129; `Docs/GAMEPLAY_SIMULATION_SPEC.md` §41, §44 (amended), §81; `Docs/Handoffs/GAME-020.md`, `GAME-021.md`, `GAME-023.md`.

## Owns
`Simulation/Career/` (new: competencies, gates), `Simulation/Save/` (new: versioned save v1), `Data/Career/CareerConfig.json`, a minimal career screen in `Presentation/` (labels only), EditMode tests. No `Code/Domain/` edits.

## Deliverable
1. Competencies 0–100: Service Judgment, Throughput, Inventory Discipline, Operational Accuracy, Reliability (multi-shift), Leadership (placeholder until staff exist) from GAME-020's shift records (§72–77); rolling update `old × 0.8 + recent × 0.2` [GDD] (§79); shown as Developing / Reliable / Strong / Expert (§78).
2. Promotion gates Budtender → Trusted → Lead → Assistant Manager with the §80 placeholder values [GDD]; a gate passed unlocks a flag only (the unlocks themselves come with PS2–PS4 systems). No unlock changes TFS behaviour (§81).
3. Save v1 (§120): schema version, career phase, competencies, customer memories (GAME-021), inventory, transactions, game day, unlocks; pending orders/staff left as empty reserved blocks. Migration: a missing field gets a deterministic safe default (§121); no save reset.

## Validation
Compile / EditMode green; QA-002 gate green. Tests: DP-029 speed-only bot cannot pass Trusted; DP-030 detail-only bot cannot pass Trusted; DP-031 balanced expert progresses within N seeded shifts; one lucky shift cannot pass a Reliability gate; save round-trip and a v0→v1 migration with missing fields. DEC-013 gate.

## Handoff
`Docs/Handoffs/GAME-024.md` (≤40 lines). Questions go to the Studio Hub (DEC-033).
