# GAME-021 — Repeat customer memory

**Role:** GAME · **Priority:** P1 · **Branch:** `task/GAME-021` worktree off `main` (GAME-017 and GAME-019 merged; GAME-018 for Similar recovery)

## Goal
Spec DP-006 (`Docs/Design/SPEC_DECISION_PRESSURE.md` §53–60): returning fictional customers remember what they bought and how it went, so prior play matters. Memory gives the player legitimate facts for a new TFS query; it never adjusts TFS scores (§60, GSS §40 as amended).

## Read
SPEC_DECISION_PRESSURE §53–60, §115 (DP-012, DP-021..024), §128; `Docs/GAMEPLAY_SIMULATION_SPEC.md` §38–40 (amended), §81; DEC-006 (no PII), DEC-028 (`RepBatchId`), DEC-049 (repeat visits are allowed); `Docs/Handoffs/GAME-017.md`, `GAME-019.md`.

## Owns
`Simulation/Slice/` new `CustomerMemory.cs` (memory store indexed by persistent id, §122), generator hooks for returning customers and memory-driven lines; SliceConfig/SliceLines new keys; EditMode tests. Persistence across game sessions comes with GAME-024's save v1; until then memory lives for a multi-shift run in one session.

## Deliverable
1. `CustomerMemory` (§53) and `PurchaseMemory` (§54) with the TFS query/context used (from GAME-020's record). Persistent ids are generated tokens; no names, no real data (DEC-006).
2. Outcome tags (§55) assigned by the sim as fictional feedback.
3. Returning customers: `repeatCustomerRate` [GDD]; their lines come from memory (§56); memory pre-fills KNOWN fields with source REPEAT_MEMORY and a confidence that decays with days since visit (§57–58); "something different today" overrides memory.
4. Same strain, new batch (§59): memory stores the batch id; the engine's batch-aware results decide what is recommended now.

## Validation
Compile / EditMode / PlayMode green; QA-002 gate green. Tests: DP-012 decisive regular (fast service is optimal), DP-021 positive repeat (faster query, engine still the authority), DP-022 "too sleepy" history becomes a KNOWN avoidance the player can put into the query, no hidden reranking, DP-023 Strain X batch A → batch B follows the engine's current batch, DP-024 favourite sold out → engine Similar list. Memory never holds PII (field whitelist test). DEC-013 gate.

## Handoff
`Docs/Handoffs/GAME-021.md` (≤40 lines). Questions go to the Studio Hub (DEC-033).
