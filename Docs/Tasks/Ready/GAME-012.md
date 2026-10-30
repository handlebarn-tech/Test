# GAME-012 — Deli restock loop: jar + backstock, service-readiness states, interruptible restock

**Role:** GAME (Unity) · **Priority:** P1 · **Branch:** `task/GAME-012` worktree off `main`. **Starts after GAME-011 merges** (phase rates feed expected demand; its fast-forward stop hook; same `ShiftSim.cs`). ART-005 supplies the BOH backstock anchor. If ART-005 hasn't merged, use a labelled placeholder anchor in the BOH rack zone and note it.

## Goal
Make stock pull the player off the counter. Jars now hold service-ready grams and BOH holds the rest. An empty jar with backstock is still recommendable by the tool (DEC-055/061) but can't be sold until somebody walks to BOH and refills it. The player reads LOW / CRITICAL / trend cues and decides when to go (DP §48–49).

## Read
`Docs/Design/SPEC_SHIFT_DAY.md` §9a, §10 (closing refill + BOH audit data), §11 "Inventory" row, §12, §13; SPEC_DECISION_PRESSURE §40–50, §115 DP-016..020, §127 (Gate D); DEC-019 (454 g jar), DEC-027 (seeded fills), DEC-041 (BOH racks), DEC-055 + DEC-061 (TFS eligibility = jar + backstock); V2 `03_SHIFT_PACING_QUEUE_MODEL.md` §12–13, V2 `08_UX_INTERACTION.md` §13; `DESIGN_V2/10_EXPLOIT_FAILURE_ANALYSIS.md` rows EX-013, 016, 017, 018, 019, 021–024; `Docs/Handoffs/GAME-011.md`; `Docs/Specs/UX_SHIFT_DAY.md`.

## Owns
- `Simulation/Slice/InventoryService.cs`: JarGrams / BackGrams / CarriedGrams; eligibility on total; `ServiceReadiness`; expected demand D; `RestockUrgency`.
- New `Simulation/Slice/RestockJob.cs`: job state machine, tags.
- `ShiftSim.cs` restock hooks only: fires GAME-011's `StockStateChanged`; sets the Unneeded flag for attribution.
- Config keys in `ShiftDayConfig.json`: backstock distribution, start-fill rules, H, EMA half-life, carry cap, transfer seconds, unneeded threshold.
- `Presentation/Slice/` restock interactions (BOH pick, carry, Transfer) per UX-003; EditMode tests.
- **Not owned:** engine/Domain (never); report O16 layout (GAME-013 renders the Inventory data GAME-012 provides); ART-005 meshes.

## Deliverable
1. **Stock split** (§9a): full-day mode only. Quick shift stays jar = total (goldens unchanged). `Catalog.SetInStock(false)` only when TotalGrams = 0 (today it fires at jar 0: change that path for full-day mode, DEC-055/061).
2. **Backstock + start fills** (§9a): GAP-DAY-01 placeholder distribution and the start-fill rules (≥ 3 LOW bestsellers with backstock, 2–3 mid jars, 1 LOW with none) from `inventory_rng`. All values labelled PLACEHOLDER / [GDD] in config.
3. **States** HEALTHY / LOW / CRITICAL / EMPTY_WITH_BACKSTOCK / SOLD_OUT with the D·H CRITICAL rule; transitions fire `StockStateChanged`.
4. **RestockUrgency**: internal only (telemetry, bot, debug panel). No UI prompt from it (DP §48).
5. **Restock job** (§9a.4): walk → pick (atomic Back→Carried, batch id kept, carry ≤ 2) → walk → Transfer (8 s, atomic at completion, `min(unit, 454 − jar)`). Interrupt keeps carried units, and an interrupted Transfer moves nothing. Leftover partial units can go back to BOH. Allowed mid-service, with a "be right back" line.
6. **EMPTY_WITH_BACKSTOCK at the counter:** the card stays (TFS eligible). Weigh/sell is blocked until a refill (EX-019); the player can refill (Emergency tag) or choose another card. GAME-019's evaluation handles the customer outcome (DP-005).
7. **Tags** Proactive / Reactive / Emergency / Unneeded + exact start state; per-shift counts and EMPTY_WITH_BACKSTOCK minutes into GAME-020's log and the report's Inventory section. The BOH audit summary (per batch: units used / left) feeds GAME-013's closing step.
8. **Measure** the real round-trip time from the player register to the BOH anchor at 1×. Report it in the handoff and don't fake walk speed. Target 35–50 s.

## Validation
Compile / EditMode / PlayMode green; QA-002 Gate A green (stock split never changes the TFS input except through eligibility = total > 0). Tests:
- **DP-016** proactive restock before Rush 2 avoids the stockout, eligibility consistent;
- **DP-017** neglect → EMPTY_WITH_BACKSTOCK or SOLD_OUT, with a service consequence;
- **DP-018** HEALTHY low-demand restock with a queue → Unneeded tag, flow cost, no benefit;
- **DP-019** jar 0 / back > 0 → still in TFS results, sale blocked until refill;
- **DP-020** jar 0 / back 0 → excluded per the preserved rule.

Exploit tests (Critical/High before completion, DEC-066):
- EX-013 / 016 single allocation (no grams created on cancel/interrupt);
- EX-017 grams leave stock only at sale commit;
- EX-018 batch id kept through pick/transfer;
- EX-019 menu can't sell an empty jar;
- EX-021 healthy-jar restock is capped by capacity and costs time;
- EX-022 BOH is never sellable;
- EX-023 whole-unit picks;
- EX-024 no stock adjustment path exists in PS2 (assert).

Standard restocking bot over 200 seeds: ≥ 1 LOW→restock in ≥ 80 % of seeds, 2–4 meaningful restock decisions, ≤ 2 emergencies (V2 03 §13). Conservation test: Σ(jar + back + carried + sold) is constant per batch across a whole shift. DEC-013 gate.

## Handoff
`Docs/Handoffs/GAME-012.md` (≤40 lines): measured round trip, restock decision counts, any placeholder you had to add. Questions go to the Studio Hub (DEC-033).
