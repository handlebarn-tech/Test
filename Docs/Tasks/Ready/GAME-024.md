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

## V2 additions (IMP-002, DEC-063)
V2 = `Docs/Design/DESIGN_V2/` (Nolan's add-on; DP wins on conflicts, DEC-063a). Row n = `Docs/Imports/IMP-001_DESIGN_V2_AUDIT.md` §2 row. All V2 numbers are [GDD] starting values (GAP-DP-02). Exploit tests: `DESIGN_V2/QA_TEST_PLAN.md`.
- **Promotion model (DEC-063b), replaces the rolling-update gating in Deliverable 1–2:** per competency, the promotion statistic is the **median of the last 6 eligible shifts**; at most one of them below gate − 10; fewer than 4 eligible shifts = `INSUFFICIENT_EVIDENCE`; a repeated scenario seed gives no new evidence; low-complexity tutorial shifts stop counting after mastery (V2 `05_PROGRESSION_CAREER.md` §5, §11; rows 34–35). A displayed rolling value (DP §79) may stay for the career screen only.
- **Gate values: gentler starting thresholds [GDD]** (DEC-063b). Use the DP §80 levels (Trusted SJ 60 / TP 55 / ID 50 / OA 70; Lead SJ 70 / TP 65 / ID 65 / OA 80 / REL 65; AM REL 75 / ID 75 / LEAD 60 / OA 85), not V2's higher table (V2 `05_PROGRESSION_CAREER.md` §6; row 35). Rank names stay DP's (Trusted, not "Trusted/Senior"; the store-title question is parked for PS2/PS4).
- Competency formulas with an anti-compensation floor, `SJ = 0.75·weighted + 0.25·min(components)` (V2 05 §4; row 33). Unavailable dimensions are N/A, not 0.
- Revenue never enters a gate (V2 05 §11; row 33; EX-007).
- Save v1 persists the named RNG stream states, so a reload never rerolls committed customers or events (V2 `01_SYSTEM_CONTRACTS.md` §3, INV-SEED-01; row 3; EX-027/028/062).
- Tests add V2's stress profiles as bots: speedrunner, perfectionist-slow, careless, inventory-only and revenue-only fail Trusted; balanced passes (V2 `VALIDATION/progression_gate_stress.csv`, reference only, never run the `.py`). Re-tune for the gentler gates. Exploits EX-029..032 (row 45).

## Handoff
`Docs/Handoffs/GAME-024.md` (≤40 lines). Questions go to your department lead (DEC-033, DEC-094).

## DES-004c addition (DEC-080)
The **manager refill loop** is a manager-rank mechanic unlocked through these gates, as one of the PS2–PS4 unlocks in Deliverable 2. Design: `Docs/Design/SPEC_SHIFT_DAY.md` §9b. Facts from DEC-079: the office silver rolling cart is the only certified refill place; HUB cabinet bags; the empty-jar shelf; cleaning. GAME-024 provides only the unlock flag. The loop itself is a separate packet, written when GAME-024 lands.
