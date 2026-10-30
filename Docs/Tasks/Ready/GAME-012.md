# GAME-012 — Deli stock + manager refill requests: floor jars, HUB backstock, service-readiness states

**Role:** GAME (Unity) · **Priority:** P1 · **Branch:** `task/GAME-012` worktree off `main`. **Starts after GAME-011 merges** (phase rates feed expected demand; its fast-forward stop hook; same `ShiftSim.cs`). No BOH/HUB anchor needed: the player never walks to backstock in PS2 (DEC-080).
**Re-scoped by DES-004c (DEC-079/080):** the player is a budtender who **requests a manager refill**. The physical refill loop (office cart, bags, weighing, cleaning) moved to the manager rank after GAME-024 (`SPEC_SHIFT_DAY.md` §9b).

## Goal
Make stock a counter decision. Each strain has one floor jar (house strains two) and 1 lb bags of backstock in the HUB. An empty jar with backstock is still recommendable by the tool (DEC-055/061) but can't be sold. A refill takes the jar off the floor for a timed window, handled by one manager at a time, so **when** and **for which strain** to ask matters (DP §48–49). House strains keep their second jar out during a refill.

## Read
`Docs/Design/SPEC_SHIFT_DAY.md` §9a, §9b (out of scope; read to know the boundary), §10 (closing flag + BOH audit data), §11 "Inventory" row, §12, §13; SPEC_DECISION_PRESSURE §40–50, §115 DP-016..020, §127 (Gate D); DEC-019 (454 g jar), DEC-027 (seeded fills), DEC-055 + DEC-061 (TFS eligibility = total), **DEC-079** (bags, house jars, managers refill), **DEC-080** (request + window); V2 `03_SHIFT_PACING_QUEUE_MODEL.md` §12–13; `DESIGN_V2/10_EXPLOIT_FAILURE_ANALYSIS.md` rows EX-013, 019, 021, 022, 024; `Docs/Handoffs/GAME-011.md`; `Docs/Specs/UX_SHIFT_DAY.md`.

## Owns
- `Simulation/Slice/InventoryService.cs`: floor jars (1 or 2) / BackGrams / RefillGrams; eligibility on total; `ServiceReadiness` incl. REFILLING; expected demand D; `RestockUrgency`.
- New `Simulation/Slice/ManagerRefills.cs`: request queue, FIFO, one at a time, window, tags.
- `ShiftSim.cs` hooks only: fires GAME-011's `StockStateChanged`.
- Config keys in `ShiftDayConfig.json`: house tiers (GAP-DAY-10 placeholder), backstock distribution, start-fill rules, H, EMA half-life, `refillWindowSimSec`, unneeded threshold.
- `Presentation/Slice/` request control and markers per UX-003; optional manager NPC walk (dressing); EditMode tests.
- **Not owned:** engine/Domain (never); report O16 layout (GAME-013 renders the Inventory data); the manager refill loop (§9b, manager rank).

## Deliverable
1. **Stock split** (§9a): full-day mode only. Quick shift stays one jar = total (goldens unchanged). `Catalog.SetInStock(false)` only when TotalGrams = 0 (today it fires at jar 0: change that path for full-day mode, DEC-055/061).
2. **House double jars:** tiers in `houseTiers` (placeholder `house`, `smalls`, `premium`; GAP-DAY-10) get 2 × 454 g jars. Sell from the fuller jar; an emptied jar is set aside.
3. **Backstock + start fills** (§9a): 1 lb bags, 10 % of batches 0 bags, otherwise uniform 1–9 (from DEC-079's ≈ 10 lb per shipment); start-fill rules from `inventory_rng`. All values labelled PLACEHOLDER / [GDD] in config.
4. **States** HEALTHY / LOW / CRITICAL / EMPTY_WITH_BACKSTOCK / REFILLING / SOLD_OUT per strain, with the D·H CRITICAL rule; transitions fire `StockStateChanged`.
5. **RestockUrgency**: internal only (telemetry, bot, debug panel). No UI prompt from it (DP §48).
6. **Refill requests** (§9a.4):
   - 3 s request action, refused at 0 bags;
   - FIFO, one at a time; cancel while queued; duplicate requests ignored;
   - when the manager takes it, the jar (the emptier jar for house strains) leaves for `refillWindowSimSec` 90 s;
   - completion is atomic: `min(454, leftover + BackGrams)`, and bags drop by the grams used;
   - no auto-refill without a request.
7. **EMPTY_WITH_BACKSTOCK / REFILLING at the counter:** the card stays (TFS eligible) and weigh/sell is blocked (EX-019). The player can request (Emergency tag) and the customer may wait, or the player chooses another card. GAME-019 handles the outcome (DP-005).
8. **Tags** Proactive / Reactive / Emergency / Unneeded + exact start state. Into GAME-020's log and the report's Inventory section: per-shift counts, manager wait times, unservable minutes per strain. The BOH audit summary (per batch: bags used / left) feeds GAME-013's closing step.

## Validation
Compile / EditMode / PlayMode green; QA-002 Gate A green (stock changes reach the TFS input only through eligibility = total > 0). Tests:
- **DP-016:** a proactive request before Rush 2 avoids the stockout; eligibility stays consistent.
- **DP-017:** neglect → EMPTY_WITH_BACKSTOCK or SOLD_OUT, with a service consequence.
- **DP-018:** requesting a HEALTHY low-demand jar → Unneeded tag; the jar is unservable for the window and a queued request waits behind it; no benefit.
- **DP-019:** jar 0 / back > 0 → still in TFS results; sale blocked until the refill completes.
- **DP-020:** jar 0 / back 0 → excluded per the preserved rule.
- **House:** a refill on a house strain keeps it sellable from the second jar.

Exploit tests (Critical/High before completion, DEC-066):
- EX-013: one jar can't be refilled twice at once; no grams created;
- EX-019: an unservable jar can't be sold from the menu;
- EX-021: constant requests cost window time and the manager slot;
- EX-022: backstock is never sellable;
- EX-024: no stock adjustment path in PS2 (assert).

EX-016/017/023 move to the manager loop (§9b).

Standard refill-aware bot over 200 seeds: ≥ 1 LOW → completed refill in ≥ 80 % of seeds, 2–4 meaningful refill decisions, ≤ 2 emergencies (V2 03 §13). Conservation test: Σ(jars + back + refill + sold) is constant per batch across a shift. DEC-013 gate.

## Handoff
`Docs/Handoffs/GAME-012.md` (≤40 lines): refill decision counts, mean manager wait in Rush 2, any placeholder you had to add. Questions go to the Studio Hub (DEC-033).
