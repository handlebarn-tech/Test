# GAME-010 — Retune for tension + QA bot personas

**Role:** GAME / QA · **Priority:** P1 · **Branch:** `task/GAME-010` worktree off `main` (can start now; rebase on GAME-006 when it merges)

## Goal
A perfect player scores 100 on every slice customer (GAME-002 handoff "Tuning"). Retune so good play is rewarded but not automatic, and build the bot personas the PS1 exit test needs (`Docs/Design/ROADMAP_POST_SLICE.md` §2).

## Read
`Docs/Specs/SLICE_DESIGN.md` §1–3, §5, §8; `Docs/Handoffs/GAME-002.md`, `GAME-002b.md`; `Docs/GAMEPLAY_SIMULATION_SPEC.md` §45, §91, §104; RES-001 O12/O13 in `Docs/Research/OFFICE_FINDINGS.md` (pacing targets).

## Owns
`SliceConfig.json` values (tuning only), the bot/persona harness and tests under `Assets/_Game/Code/Tests/`, a tuning note `Docs/Design/TUNING_PS1.md`. Simulation code only for persona hooks. No Domain edits.

## Deliverable
1. Personas in the pure-sim bot: **perfect** (true family, best price fit), **careless** (random chip, ignores budget and limits), **slow** (correct, 2× service time).
2. `customersPerShift` 16 [GDD]; retune `budgetPerGram` options, patience and `acceptThreshold` so over seeds 1–20 the averages land at: perfect 80–95, careless < 60, slow 60–80. Every changed value stays [GDD] and is listed before/after in `TUNING_PS1.md`.
3. A seed-sweep EditMode test that prints the three averages (no scene).
4. Exit-test hooks for PS1 (strike and trim counts once GAME-007/008 land; skip-guarded until then).

## Validation
Compile/EditMode/PlayMode green; the sweep table is in the handoff. Slice goldens (prices, intents) unchanged. DEC-013 gate.

## Handoff
`Docs/Handoffs/GAME-010.md` (≤40 lines). Questions go to the Studio Hub (DEC-033).
