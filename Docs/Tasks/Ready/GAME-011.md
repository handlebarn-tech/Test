# GAME-011 — Shift phases, traffic curve, compressed clock, fast-forward, PressureLevel

**Role:** GAME (Unity) · **Priority:** P1 · **Branch:** `task/GAME-011` worktree off `main`. **Starts after** REVIEW-PS1 and PS1b's GAME-020 are merged (same `Simulation/Slice/` files). UX-003 is needed for the view layer only; the Simulation side may start first. **Runs before GAME-012** (same `ShiftSim.cs`; DEC-064 A3).

## Goal
Replace the slice's fixed customer list with a full shift day: Opening → door-rush → Recovery → Steady → evening rush → Late → Closing, on a compressed 08:00–22:00 clock. Arrivals follow the validated phase tables, and quiet time can be fast-forwarded without ever skipping a decision. The slice/GAME-010 shift stays as a **Quick shift** mode.

## Read
`Docs/Design/SPEC_SHIFT_DAY.md` §1–8, §9 (events), §10 (phase hosting only), §11 "Shift flow" row, §12, §13; SPEC_DECISION_PRESSURE §61–65; V2 `Docs/Design/DESIGN_V2/03_SHIFT_PACING_QUEUE_MODEL.md` §3, §7–11, §15, §17; V2 `01_SYSTEM_CONTRACTS.md` §3 (RNG streams); `DESIGN_V2/QA_TEST_PLAN.md` rows EX-025/026; `Docs/Handoffs/GAME-010.md`, `GAME-019.md`, `GAME-020.md`; `Docs/Specs/UX_SHIFT_DAY.md` (UX-003).

## Owns
`Simulation/Slice/`:
- `ShiftSim.cs`: phase driver, arrival schedule, door line, specials, patience classes, fast-forward gate, pause;
- new `ShiftPhases.cs` (phase table, clock map, `PressureLevel`);
- new `ArrivalSchedule.cs`;
- `Customers.cs`: generator reads `customer_profile_rng` / `patience_rng` in full-day mode.

Also: `SliceData.cs` config classes; new `Data/Slice/ShiftDayConfig.json` (the three profiles from SPEC_SHIFT_DAY §3, `arrivalRateScale`, `ffRate`, `ffHorizonSec`, `openRegistersByPhase`, receipt-paper event); a Quick/Full-day mode switch in `Presentation/Slice/` (`SliceGame.cs`, `SliceView.cs`) for banners, clock, fast-forward, ambient registers; EditMode tests. **Not owned:** `InventoryService.cs` stock split (GAME-012), report O16 sections (GAME-013), Domain/engine (never).

## Deliverable
1. **Phase table + clock** (§2–3): Beginner/Standard/Expert in config. Sim time drives logic; the clock is a display map. **No sale at or after 22:00** (§2, DEC-036 M3): the doors lock at 21:45 (end of Late, GAP-DAY-09 placeholder); last call serves the queue for ≤ `lastCallSimSec` 180 s with the clock mapped 21:45 → 21:59; at the window end the POS locks and anyone left goes `closed_out` (structural, polite line). Closing tasks then run without the POS, and the Sign button ends the shift. "Open doors" ends Opening early.
2. **Arrivals** (§4), exactly the V2 harness rule: Gamma(k, (60/λ)/k) gaps, **renewal clock restarted at each phase start**, overflow discarded; door line at doors-open + U(0, 20) s; specials at U(300, 1620) s tagged `special`. The whole list is pre-generated from `arrival_rng`. Named streams `streamSeed = Hash64(shiftSeed, name)`. Quick shift keeps its single `Random(seed)` and its goldens.
3. **Registers** (§5): the player serves one register. `openRegistersByPhase` ambient coworker stations (GAP-DAY-03 placeholder values, labelled) are presentation-only: no queue, stock, TFS or report effect (test).
4. **Patience** (§6): V2 classes/medians/σ/difficulty multipliers. Add `EngagementState` active patience only if GAME-019 didn't.
5. **Fast-forward** (§7): start conditions and auto-stop triggers as listed; `ffRate` 4×. Pause freezes all sim-affecting systems (EX-025); menus don't slow time (EX-026). Fast-forward and pause seconds are logged. Expose a hook (`StockStateChanged` event) that GAME-012 fires to stop fast-forward.
6. **PressureLevel** (§8) with the formula and EMA. It drives audio/NPC/HUD tint and is logged at every decision; never read on any TFS/parser/evaluator path.
7. **Demand inputs (DP §51):** PS2 covers traffic, archetype mix and availability. Deals arrive with GAME-016 (PS3), and repeat customers through the special slots (GAME-021).
8. **Events** (§9): special slots + ≤ 1 receipt-paper event per shift (`event_rng`, 10 s task, never in Opening/Closing).
9. **Telemetry + attribution** (§12): per-phase flow numbers into GAME-020's log; `player_attributable` vs `structural_pressure` by the four criteria (`closed_out` is always structural) (the Unneeded-restock criterion reads a flag GAME-012 sets; until then false). The report's "Shift flow" section.
10. **Service guard** (§4 last bullet): measure median service with the GAME-010/017 bot. Record it in the handoff; if > 70 s, set `arrivalRateScale` and say so.

## Validation
Compile / EditMode / PlayMode green; QA-002 Gate A green. Tests:
- **(a) Arrival port parity:** mean arrivals over 700 seeds, Standard 19.96 ± 0.5, Beginner 13.75 ± 0.5, Expert 22.49 ± 0.6 (`Docs/Design/VALIDATION_DAY/shift_day_results.csv`). Per-phase means within ± 0.3 of the harness: GAME-011 adds a per-phase dump to the script if needed; the script is DES-owned, so note any edit in the handoff.
- **(b) Determinism:** same seed with and without fast-forward → identical arrival list and customer contents; with a scripted bot taking identical actions, identical stock at each arrival.
- **(b2) Store hours:** over 200 seeds × 3 profiles, no sale timestamp maps to ≥ 22:00, and the clock never shows 22:00 while the POS can confirm. `closed_out` per Standard shift ≈ 0.02 (`VALIDATION_DAY/shift_day_drain_results.txt`).
- **(c)** Fast-forward refuses to start while anyone is queued or a jar is CRITICAL / EMPTY_WITH_BACKSTOCK, and stops ≥ `ffHorizonSec` before an arrival.
- **(d)** Pause freezes patience, tasks and arrivals (EX-025). Opening Details/menus doesn't change sim dt (EX-026).
- **(e)** Ambient registers change nothing in sim state (snapshot equality with them on/off).
- **(f)** PressureLevel is absent from every TFS input snapshot (Gate A).
- **(g)** Targeted bot on Standard, 200 seeds, bot service model: abandonment 2–6 %, mean peak 2.5–3.5, p90 ≤ 5.

Quick shift goldens unchanged. DEC-013 gate.

## Handoff
`Docs/Handoffs/GAME-011.md` (≤40 lines): measured median service, real-minute playtime of one Standard run, any table change. Questions go to your department lead (DEC-033, DEC-094).
