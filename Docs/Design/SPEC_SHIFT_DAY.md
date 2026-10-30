# SPEC — PS2 "Full Shift Day" (DES-004)

**Status:** design for the Studio Hub, 2026-10-30, DES-004; door lock updated by DES-004b (DEC-076); store answers DEC-079 and the manager-refill ruling DEC-080 applied by DES-004c. Doc-only. Packets: `Docs/Tasks/Ready/GAME-011.md`, `GAME-012.md`, `UX-003.md` (they run after PS1/PS1b).
**Precedence:** tool parity (DEC-001/002/006) > DP (`SPEC_DECISION_PRESSURE.md`) > V2 (`DESIGN_V2/`, DEC-063a) > this spec's [GDD] numbers. Store facts (RES-001, DECs) beat generic choices.
**Citation key:** DP §n = `Design/SPEC_DECISION_PRESSURE.md`; V2 03 §n = `Design/DESIGN_V2/03_SHIFT_PACING_QUEUE_MODEL.md`; GSS §n = `GAMEPLAY_SIMULATION_SPEC.md`; O*n* = RES-001 `Docs/Research/OFFICE_FINDINGS.md` §3. Labels: **[SRC]** store fact/law (cited) · **[GDD]** game-design decision, tune in playtest · **GAP-DAY-nn** unknown store fact with a labelled placeholder (§14).
**Validation script:** `Docs/Design/VALIDATION_DAY/shift_day_sim.py` runs V2's own queue harness, unchanged, on the tables in §3. Output: `shift_day_results.csv`.

---

## 1. What PS2 changes
The slice is one 12/16-customer stretch at one register. PS2 makes it a day: the doors open, two rushes and a recovery happen, jars run low and the player has to decide when to ask a manager for a refill, and the store closes.

| Stays | Changes |
|---|---|
| TFS engine, parser, chips, cards, POS, limits, ID, medical (PS1), KNOWN/questions/evaluation (PS1b) | `customersPerShift` + spawn gaps → phase table + arrival process (GAME-011) |
| `ShiftSim` as the authority (extended, not replaced) | jar = all stock → floor jar(s) + HUB backstock; the player **requests a manager refill** (GAME-012, DEC-055/061, DEC-079/080) |
| The slice/GAME-010 shift, kept as a **Quick shift** mode with its own config and goldens | game clock 08:00–22:00, phase banners, opening/closing-lite, report v2 sections (GAME-011/013, UX-003) |

## 2. Phase order and game clock — caveat 0 (order) resolved
DP §61 lists Opening → Steady → Rush 1 → Recovery → Rush 2 → Late → Closing. The real store has its first rush **at opening**: "a line has formed before 8 am", and its second at 17:00–20:00 when online pickups peak [SRC O12]. Fidelity outranks the generic order (CLAUDE.md), so DES-004 keeps every DP phase and moves Steady after Recovery. **Proposed DEC-DAY-A.** The phase table lives in config, so the DP order is a data swap if the Hub prefers it.

| # | Phase (DP §61 name) | Std sim min | Game clock (display) | Doors | What it is |
|---|---|---:|---|---|---|
| 0 | Opening / Preparation | 2 | 07:30 → 08:00 [GDD: staff start time not sourced] | closed | opening-lite tasks (§10); "Open doors" button ends it early |
| 1 | Rush 1 ("door rush") | 5 | 08:00 → 09:30 | open | door line already waiting [SRC O12] + elevated arrivals |
| 2 | Recovery | 4 | 09:30 → 12:00 | open | low arrivals; preparation window (DP §49) |
| 3 | Steady Floor | 6 | 12:00 → 17:00 | open | normal traffic; contains the 14:00 checkpoint [SRC O12] |
| 4 | Rush 2 (Pressure Event) | 6 | 17:00 → 20:00 | open | evening rush [SRC O12]; the shift's peak |
| 5 | Late Shift | 5 | 20:00 → 22:00 | open | taper; doors lock at 22:00 on the dot [SRC DEC-076]; customers inside are still served |
| 6 | Closing Summary | 4 (nominal) | from when the last customer leaves (≥ 22:00) | locked | closing-lite (§10), report v2 (§11) |

- **Sim time** (shift seconds) drives everything; the **game clock** is a piecewise-linear display map of sim time per phase (structural compression, DP §63). Ratios vary from ≈ 15× (Opening) to ≈ 50× (Steady); nothing reads the clock for logic.
- **Door lock at 22:00** [SRC DEC-076, O1]: the doors lock at 22:00 on the dot and nobody new can enter, so no arrival is scheduled at or after 22:00 (door line, phase draws and specials included). Customers already inside (queued or at the counter) are **served to completion** under the normal rules, and their patience still applies. DEC-036 M3 applies to entry, not to finishing service (DEC-076).
  - After 22:00 the clock keeps running at Late's display ratio. Closing begins when the last in-store customer leaves (or at once if the store is empty).
  - Measured with V2's harness (`VALIDATION_DAY/shift_day_drain.py`, targeted bot), service after 22:00 runs: Standard mean 45 s / p90 118 s / max 303 s (66 % of shifts have some); Expert 44 / 112 / 226 s; Beginner 31 / 85 / 205 s. That is inside the real-minute budget (§7).
- After a Rush ≥ 5 min the next phase is low-rate (V2 03 §12): Rush 1 → Recovery holds. Rush 2 → Late is a taper, not a recovery: by design, the evening rush runs into close.
- Shift start hour: the slice config's `shiftStartHour` 14 belongs to the Quick shift only.

## 3. Phase tables [GDD] (V2 starting numbers, re-tuned for the §2 order)
Format = V2 `default_tuning.yaml` `shift_profiles`. Rates are arrivals/min for the **player's register** (§5). `door` = customers queued at doors-open.

| Profile | Opening | Rush 1 | Recovery | Steady | Rush 2 | Late | Closing | k | specials | door | Total |
|---|---|---|---|---|---|---|---|---:|---:|---:|---:|
| Beginner | 2 @ 0 | 4 @ .66 | 4 @ .30 | 5 @ .54 | 4 @ .90 | 4 @ .54 | 3 @ 0 | 3.0 | 1 | 2 | 26 min |
| **Standard** | 2 @ 0 | 5 @ .70 | 4 @ .30 | 6 @ .50 | 6 @ 1.00 | 5 @ .54 | 4 @ 0 | 2.5 | 2 | 3 | **32 min** |
| Expert | 2 @ 0 | 6 @ .72 | 4 @ .32 | 6 @ .55 | 7 @ .94 | 6 @ .55 | 4 @ 0 | 2.2 | 2 | 3 | 35 min |

Door line: "at least a couple" wait at 08:00 [SRC DEC-079]; 2/3/3 by profile [GDD within that]. Lengths match V2 26/32/35 and DEC-056's 25–40 min.

**Harness result** (V2 `shift_queue_sim.py` with only the arrivals and profiles swapped; 700 seeds Standard, 350 Beginner/Expert):

| Profile / policy | arrivals | abandon % | mean wait s | mean peak queue | p90 peak | median service s |
|---|---:|---:|---:|---:|---:|---:|
| Standard targeted | **19.96** | **4.47** | 52 | **3.24** | **5** | 60.6 |
| Standard ask-all | 19.96 | 19.36 | 101 | 4.19 | 6 | 93.3 |
| Standard ask-none | 19.96 | 1.09 | 28 | 2.68 | 4 | 44.7 |
| Beginner targeted | 13.75 | 0.27 | 27 | 1.92 | 3 | 56.8 |
| Expert targeted | 22.49 | 7.47 | 55 | 3.42 | 5 | 64.1 |

Standard passes every V2 03 §17 gate (18–20 arrivals, 2–6 % abandonment, mean peak 2.5–3.5, p90 ≤ 5, service 55–70 s). Expert sits above 6 %, as in V2 (6.6 %), which is acceptable for Expert. Ask-none looks efficient on queue numbers alone; DecisionQuality (GAME-019/020) is what penalises it (V2 03 §16).

## 4. Arrival process — caveat 1 (phase-rate renewal) resolved
**Rule [GDD] = V2 harness behaviour, ported exactly:** within each phase, gaps are `Gamma(shape=k, scale=(60/λ)/k)` seconds and **the renewal clock restarts at the phase start** (the first gap is measured from the phase boundary; an arrival drawn past the phase end is discarded). Zero-rate phases produce nothing.
- **Nominal ≠ realised.** Restarting loses about one partial gap per phase, so realised counts are below λ·T. Measured on V2's original Standard table (700 seeds): per phase 0.05 / 2.35 / 5.38 / 0.91 / 6.30 / 2.40 against nominal 0.24 / 2.70 / 5.76 / 1.20 / 6.48 / 2.70; total 19.4 with specials. V2's validated 19.3 already includes this loss, so **no retune is needed if the port restarts per phase**. A continuous (non-restarting) process would add ≈ 1.5 arrivals and fail the gates.
- **Door line:** `door` customers arrive at doors-open + U(0, 20) s, drawn from `arrival_rng` after the phase draws.
- **Special slots:** `specials` arrivals at U(300, min(1620, lockSec − 60)) s, where `lockSec` = end of Late = 22:00. V2's U(300, 1620) would put Beginner's special after its 1380 s lock in about 18 % of shifts (REVIEW-W5D m6). They are filled from the repeat / difficult-customer / event pool (GAME-021/022/023 provide content; until then they are ordinary customers tagged `special`).
- **Pre-generated schedule:** the whole arrival list is generated at shift start from `arrival_rng`, so the schedule is the same whether or not the player fast-forwards (§7). Customer contents come from `customer_profile_rng`, patience from `patience_rng` (V2 01 §3 streams, `streamSeed = Hash64(shiftSeed, streamName)`). Quick shift keeps its single `Random(seed)` so its goldens stay valid.
- **Abandonment and repeat visits:** an abandoned customer does not re-enter. DEC-049 "max buyer back in line" is a special-slot template, not an extra arrival.
- **Service-time guard (V2 03 §17):** in play, service time is the player's own, not sampled. GAME-011 measures median service with the GAME-010/017 bot and in the first playtest. If it is above 70 s, scale all rates by `arrivalRateScale = 60 / medianService` (config) **before** touching patience. Real median transaction is 2.3 min [SRC O13]; the game's ≈ 60 s is deliberate compression.

## 5. Registers — caveat 2 (how many of the 11 are open) resolved
The store has 11 sales-floor registers [SRC DEC-039/040]. The V2 harness is a single server, and PS2 has no staff gameplay (PS4, DEC-063d).

**Decision [GDD], proposed DEC-DAY-B:**
1. **The player runs exactly one register: the one the GM assigns for this shift.** The GM assigns registers on a floor map [SRC DEC-079]. The Opening shift note shows the assignment on a small floor map. It is drawn from `assignableRegisters` (config, `event_rng`), which holds only the slice's existing player station until the other stations have working anchors (ART). The §3 tables are the player's **share** of store traffic, so the single-server validation holds.
2. **Other registers are ambient presentation only.** NPC coworkers stand at `openRegistersByPhase` other stations with ambient customers. They have no sim effect: they don't take from the player's queue, sell stock or touch inventory or TFS. They exist for life on the floor and for PERF-002's NPC count. Placeholder (GAP-DAY-03): Opening 0, Rush 1 4, Recovery 2, Steady 3, Rush 2 5, Late 3, Closing 0. A reality cross-check, not a target: 580–860 tx/day over 14 h with a 2.3 min median transaction [SRC O13] averages about 1.6–2.4 busy registers, so 2–5 staffed at peaks is plausible.
3. **One shared line** [SRC DEC-079]: customers are called up as registers free. Presentation: one visible line from the entry; the front customer peels off to whichever register frees up. Ambient customers go to coworkers, and the player's customers (their share, §3) come to the player when the player is free. The HUD queue count shows only the player's share. The sim is unchanged.
4. Ambient coworkers never sell from the deli jars in PS2: jar depletion is the player's own (keeps DP-016/017 attributable). Real stores drain far faster ("a popular strain can sell a pound in under an hour" [SRC DEC-079]); PS2 makes up for it with seeded start fills (§9a), and ambient drain is a PS4 option. PS4 staffing replaces ambient registers with real servers and retunes (V2 03 §5 warns the single-server table must not be reused unchanged for a staffed floor).

## 6. Service and patience [GDD, V2 03 §6–9]
- Queue patience = V2: class mix low/normal/high 20/60/20 %, medians 140 / 230 / 330 s, lognormal σ 0.35, difficulty multiplier 1.35 / 1.00 / 0.88, threshold hidden and seeded. Drains only while queued (the slice rule). Door-line customers start at full patience; their wait outside is off-screen.
- Active-service patience (`EngagementState` 0.25–0.5× / 0.75× / 1.0× / 1.25×, relief cap 60 s): GAME-019 owns it if it ships it; otherwise GAME-011 adds it with V2's values.
- Queue presentation states CLEAR / NORMAL / PRESSURE / CRITICAL / OVERLOAD at 0 / 1–2 / 3–4 / 5–6 / 7+ waiting. Presentation only (UX-003, PressureLevel), never a hard rule.
- Service time: player-driven. The V2 archetype medians (32–76 s) and question adders are the **bot** model for the harness and EditMode bots.

## 7. Time compression — caveat 3 (never skip a decision) resolved
Two layers, both [GDD]:
1. **Structural** (§2): each phase covers a block of store hours. Conversations, weighing and tasks run at natural speed (DP §63).
2. **Quiet-time fast-forward:** the player holds the Fast-forward control. Sim time then runs at `ffRate` = 4× (config). It can **start** only when every condition holds (V2 03 §15, made concrete):
   - nobody being served and nobody queued;
   - the next scheduled arrival (§4 list) is ≥ `ffHorizonSec` = 20 s of sim time away;
   - no jar is CRITICAL or EMPTY_WITH_BACKSTOCK (LOW is allowed: the player has already seen it);
   - no opening/closing task or receipt-paper task is in progress (the player isn't mid-action) and no modal is open (pending manager refills don't block it; their completion is a stock-state transition and stops it);
   - not the Opening or Closing phase (those have their own early-end buttons).

   It **stops automatically**, returning to 1× in the same tick, on the first of: `ffHorizonSec` before the next arrival; any stock-state transition (HEALTHY→LOW etc.); a phase boundary (banner); a special-slot or event trigger; any player input other than the hold.
- **It cannot skip a decision:** arrivals are scheduled in sim time (§4), so fast-forward changes only how many real seconds pass, never who arrives or when in sim time. Stock only changes through sales, which can't happen during fast-forward, and through manager refills, whose completion times are fixed in sim time. Test: same seed with and without fast-forward → identical arrival list and customer contents; with a scripted bot taking identical actions, identical stock at each arrival.
- **Pause** freezes every sim-affecting system: arrivals, patience, tasks, transfers (V2 EX-025). Menus, Details and the debug panel do **not** slow the clock (EX-026). Only an explicit accessibility assist may (UX-003), and the run is then tagged `assist`.
- **Real-time budget:** Standard = 32 sim min. Fast-forward saves at most the quiet Recovery/Late stretches, typically 1–3 real min. The exit test measures real minutes; the 25–40 window has room either way.

## 8. PressureLevel 0–1 [GDD, DP §64]
`PressureLevel = EMA_10s( clamp01( 0.45·min(waiting/5, 1) + 0.25·(λ_phase/λ_max) + 0.15·min(stockProblems/3, 1) + 0.15·min(refillsPending/2, 1) ) )`
- `stockProblems` = strains that are CRITICAL, EMPTY_WITH_BACKSTOCK or REFILLING. `refillsPending` = manager refill requests not yet completed. `λ_max` = the profile's highest phase rate. An active major event adds +0.1 (clamped).
- Consumers: audio intensity, NPC idle/fidget, UX-003 queue tint, telemetry (logged at every player decision, V2 03 §10). **Never** an input to TFS, parser, query composer or `ServiceEvaluator` (Gate A test).
- Staff coverage (DP §64) is 0 in PS2; PS4 adds it.

## 9. Events [GDD, DP §65, V2 03 §14]
Standard: at most 1 major and 1–2 minor events, all emergent or plausible.
| Event | Kind | Source | Owner |
|---|---|---|---|
| Top seller runs low / out during a rush | major (emergent, not scripted) | start fills (§9a) + demand | GAME-012 |
| Door line at 08:00 | structural | O12 | GAME-011 |
| Special customer (repeat, difficult Compare, "max buyer back in line" DEC-049) | minor, special slots | DP §65, DEC-049 | GAME-011 slot; content GAME-021/022 |
| Receipt paper runs out at the player's register: POS can't finish until a 10 s "change roll" task | minor | O11 "check receipt paper" | GAME-011 (`event_rng`, ≤ 1 per shift, never in Opening/Closing) |
| Delivery arrives, deal rush, staff needs help | — | O8 Thursday deli; deals; staff | out of PS2 (PS4 / GAME-016 / PS4) |

## 9a. Restock model (GAME-012): the budtender requests a manager refill [DP §40–50, DEC-055/061, DEC-079/080, V2 03 §13]
In PS1/PS2 the player is a budtender, and **deli refills are always done by managers** at the certified office cart [SRC DEC-079]. So the player's restock decision is **when to request a refill** and for which strain. The physical loop is the manager-rank mechanic in §9b (DEC-080).

**Stock per deli batch** (Simulation):
- `JarGrams[]`: the floor jar(s), each ≤ 454 g [SRC DEC-019, DEC-079].
  - **One 1 lb jar per strain; house strains have two** [SRC DEC-079]. Which tiers count as "house" is GAP-DAY-10. Placeholder: tiers `house`, `smalls`, `premium` (the P3 house lanes) → 2 jars.
  - Sales draw from the fuller jar until it empties, then from the other. An empty house jar is set aside (off the floor) [SRC DEC-079: it waits in the office].
- `BackGrams`: HUB storage-cabinet backstock in 1 lb (454 g) bags [SRC DEC-079].
- `RefillGrams`: grams in a jar that is away with the manager.
- `TotalGrams` = sum.
- **TFS eligibility = TotalGrams > 0** [SRC DEC-055, confirmed DEC-061]. `InventoryService.Sell` today calls `SetInStock(false)` when the jar hits 0. In full-day mode it must do so only when TotalGrams hits 0. Quick shift is unchanged: one jar, no backstock, so jar = total.
- **Backstock at Opening [GDD from SRC DEC-079 "≈ 10 lb of one strain per shipment"]:** per batch, 0 bags with 10 % probability (sold through: the jar is the last of it), otherwise uniform 1–9 bags (`inventory_rng`). No deliveries during a shift (PS4).
- **Start fills [GDD, extends DEC-027]:** seeded as left by last night's closer.
  - At least 3 bestseller single-jar strains LOW with backstock (the Opening/Recovery proactive choice).
  - 2–3 popular jars at 0.25–0.45 fill (they cross LOW/CRITICAL in Rush 2).
  - 1 LOW jar with 0 bags (true SOLD OUT path, DP-020).
  - At least 1 house strain with one jar already empty (shows the second-jar buffer).

  GAME-012 tunes so the Standard bot meets 2–4 meaningful refill decisions (V2 03 §13).

**9a.1 States** (Simulation, `ServiceReadiness`, per strain). S = grams in floor jars that are on the floor; n = jars the strain has (1 or 2).
| State | Rule |
|---|---|
| HEALTHY | S ≥ `lowStockFraction` (0.25) × 454 × n and not CRITICAL |
| LOW | 0 < S < 0.25 × 454 × n, not CRITICAL |
| CRITICAL | 0 < S ≤ D·H (below) |
| EMPTY_WITH_BACKSTOCK | S = 0, BackGrams + RefillGrams > 0, no refill under way. Still TFS-eligible; it can't be sold until a refill completes (EX-019) |
| REFILLING | S = 0 and a refill for the strain is under way. TFS-eligible, unsellable |
| SOLD_OUT | TotalGrams = 0. TFS-ineligible per the preserved inventory rule |

A strain with S > 0 and a refill requested or under way keeps its state, plus a "refill requested" marker (e.g. a house strain whose second jar is still out).

**Expected demand** D (g/sim-min) [GDD] = max( EMA of sold grams/min for the batch (half-life 3 min), share_b × λ(t+H) × ḡ ), where:
- `share_b` = (appearances of the batch in TFS results shown this shift + 1) / (results shown + inStockBatches), i.e. observed usage;
- λ(t+H) = the phase rate H ahead, so an upcoming rush counts (DP §43);
- ḡ = mean grams per sale line so far (prior 11 g, the store's average flower purchase [SRC O13]);
- H = 4 sim min.

`share_b` reads the TFS result **lists** after the fact. It never feeds back into TFS.

**9a.2 RestockUrgency** (internal; telemetry, bots, debug only; never shown as "refill this now", DP §48) = StockRisk × ExpectedDemand × OperationalImportance, where:
- StockRisk = clamp01(D·H / max(S, 1));
- ExpectedDemand = D / max over batches;
- OperationalImportance = share_b / max share.

**9a.3 Player cues** (UX-003): LOW / CRITICAL tags on the jar and its card; a recent-demand trend arrow (EMA up/down); a backstock-present marker; "refill requested" / "with manager" markers. No forecast numbers (DP §52) and no countdown (DP §39).

**9a.4 Refill request** [GDD on SRC DEC-079/080]:
1. **Request:** "Request refill" for a strain, from the register terminal or at the jar. A 3 s action; no walking. Refused when BackGrams = 0 ("no backstock left": the jar is the last of it).
2. **Manager queue:** requests are handled first-in-first-out, **one at a time** (GAP-DAY-11). A queued request can be cancelled; one under way can't. A second request for the same jar is ignored (EX-013).
3. **Window:** when the manager takes the request, the jar leaves the floor (its grams → RefillGrams) for `refillWindowSimSec` = 90 s of sim time (GAP-DAY-11 placeholder).
   - Single-jar strain: unservable for the window.
   - House strain: the manager takes the emptier jar, and the second jar stays out and sellable [Hub ruling DEC-080].
   - Until the manager takes the request, the jar stays on the floor and keeps selling: the manager queue is a real delay in a rush.
4. **Completion** (atomic): the jar returns with `min(454, leftover + BackGrams)` g, and BackGrams drops by what was used. Grams move only at completion; the conservation test holds throughout. Completion fires a stock-state transition (it stops fast-forward, §7).
5. **Mid-service:** the player may request a refill for the strain the customer wants. The customer can wait (active patience, GAME-019) or the player picks another card (GAME-019 evaluates the outcome, DP-005).
6. An optional manager NPC walks the jar off and back (dressing, no sim effect). There is no auto-refill without a request (GAP-DAY-12): neglect has its consequence (DP-017, EX-022).

**9a.5 Tags** (DP §46; log the exact start state as well; "start" = the request):
- **Proactive:** requested while HEALTHY or LOW.
- **Reactive:** requested while CRITICAL.
- **Emergency:** requested while EMPTY_WITH_BACKSTOCK, or during service for the card being sold.
- **Unneeded** (DP-018): requested while HEALTHY and below a RestockUrgency threshold. It costs real stock (a sellable jar leaves the floor) and the manager slot (later requests wait). It is a FLOW/OPERATIONS input per GAME-020.

DP-018's "player leaves the counter" becomes "the player pulls a sellable jar and occupies the manager". Diagnostic: more than 2 emergencies in a Standard shift (V2 03 §13).

## 9b. Manager refill loop: manager rank, not PS2 (DEC-080)
These move out of GAME-012 to the manager rank, unlocked through the career ladder (GAME-024 / V2 promotions, DEC-063b). The implementation packet is to be written when GAME-024 lands. The facts are fixed [SRC DEC-079]:
- **Where:** the refill happens only at the **silver rolling cart in the office**, the only state-certified place to refill deli containers. The deli scale sits on the cart. Cleaning supplies are under it: isopropyl alcohol, rags, scraper, bins, tongs. Emptied house jars wait on the **wooden shelf above the cart** until the second jar is empty or low. Backstock bags are in the **HUB storage cabinets against the office wall**.
- **Procedure:**
  1. Collect the jar(s).
  2. Dump the leftover into a bowl on the scale.
  3. Adjust inventory in the system.
  4. Fill both jars from the bags.
  5. Move the product from back-of-house to recreational in the system.
  6. Clean (managers also clean jars after sell-through).
  7. Return the jars to the floor.
- **Carried over from DES-004's physical job design:**
  - interruptible states NOT_STARTED / IN_PROGRESS / INTERRUPTED / COMPLETED (DP §50);
  - atomic bag pick and jar fill, batch id kept (EX-018);
  - carry cap, whole-bag picks (EX-023);
  - no grams created or lost on interrupt or cancel (EX-016/017);
  - real walk times from the graybox.
- **Gameplay at manager rank:** NPC budtenders' refill requests become the player's queue, so the §9a decision flips to triage. This meets PS4 staffing (DP §87–100).
- **Art/ref needs:** office cart + shelf + HUB cabinet anchors (ART/REF; DEC-042 photo shows the cart).

## 10. Opening-lite and closing-lite [GSS §7, §73; O11]
**Opening** (2 sim min, ends early on "Open doors"; no customers): (a) walk the jars, where LOW/CRITICAL show; (b) read the shift note: today's day of week and "expect a line at open and an evening rush" (DP §52: expectation, not forecast); (c) see the assigned register on the floor map (§5); (d) request refills for jars that are already LOW (proactive, §9a). Nothing to tick off: GSS §73 says no trivial switches.

**Closing** (after the last in-store customer leaves; doors locked since 22:00), an O11 subset chosen for decisions [SRC O11, selection GDD]:
1. **Flag jars for the closing manager:** mark the LOW/empty jars that need a refill tonight (managers refill and clean jars [SRC DEC-079]). It feeds the report's Inventory section; no carry-over to the next shift until save v1 (GAME-024).
2. **Deli BOH audit:** a summary of each batch's backstock used today vs left, in 1 lb bags, feeding the report inventory section. Read-only in PS2; no discrepancies are generated (receiving/quarantine is PS4, O8).
3. **Clean scale + wipe counter:** one 5 s interaction, flavour [SRC O11].
4. **Manager signs** = the report's Sign button [SRC O11 "manager signs"].

The rest of O11 (cones, trash, bathroom, mop, online orders) stays out: no decision. GAME-013 owns 1–4; GAME-011 owns the phase that hosts them.

## 11. Report v2 fields [SRC O16]
Section order follows the store's closing report. A section the build doesn't model is omitted, not zero-filled with invented data.
| O16 section | PS2 content | Owner |
|---|---|---|
| Income: Gross, Discounts, Returns, Net, Loyalty, Tax, Subtotal, **Rounding**, Total | Gross / Net / Tax / Subtotal / Rounding (nickel, DEC-035) / Total. Discounts only if deals exist (GAME-016). Returns, Loyalty omitted | GAME-013 |
| Tax: Excise, Sales | from the engine's pricing tax lines; rec vs med rate (GAME-009) | GAME-013 |
| Payments | **omitted**: payment method isn't modelled (cash / PIN debit / ACH exist [SRC O14], no data to split) | — |
| Category | Deli flower only in PS2 (packaged = PS3) | GAME-013 |
| Customer (Rec/Med) | counts from GAME-009 | GAME-013 |
| Order type | in-store only (online pickup ≈ 17 % [SRC O13] not modelled in PS2) | GAME-013 |
| Transactions, per-register | the player's register; ambient registers have no sales (§5) | GAME-013 |
| **Shift flow** (game) | per phase: arrivals, served, abandoned (structural vs attributable), peak queue, mean wait | GAME-011 |
| **Inventory** (game) | refill requests by tag, minutes each strain spent unservable (EMPTY_WITH_BACKSTOCK / REFILLING), SOLD_OUT batches, BOH audit | GAME-012 → GAME-013 |
| SERVICE / FLOW / OPERATIONS + stars | GAME-020 (unchanged; PS2 adds inputs) | GAME-020 |

No TFS scores or ranks anywhere (DEC-052). Manager notes (O16 Daily Tracker) are out.

## 12. Telemetry and attribution [V2 03 §10–11]
- Log per shift: per-phase arrivals/served/abandoned, service seconds after 22:00 (`overtimeSimSec`), peak waiting, mean/p90 wait, time-to-clear after each rush, PressureLevel at every player decision, refill requests (start state, tag, wait for the manager, window), stock-state minutes, fast-forward seconds used, pause seconds. Extends GAME-020's log (DP §116–117); the schema is GAME-020's.
- **Abandonment attribution** is `player_attributable` only if one of these held during the abandoner's wait:
  - redundant consultation above allowance (GAME-019);
  - avoidable idle (the player at the counter, nobody served, ≥ 10 s while someone waits);
  - avoidable rework (wrong card / void).

  Otherwise it is `structural_pressure`. FLOW penalises attributable abandonment only.

## 13. Exit test and acceptance (PS2, ROADMAP §3)
- A Standard shift with the 3-phase arc (open → two rushes → close) plays in **25–40 real minutes** (DEC-056), measured over 3 human playtests.
- Targeted bot over 200 seeds in EditMode (pure sim, bot service model): arrivals 18–20, abandonment 2–6 %, mean peak 2.5–3.5, p90 ≤ 5 (V2 03 §17). Ask-all is worse on FLOW; ask-none is worse on DecisionQuality (GAME-020).
- In ≥ 80 % of Standard seeds at least one jar goes LOW and the bot requests a manager refill that completes. 2–4 meaningful refill decisions; ≤ 2 emergencies for the refill-aware bot.
- **Store hours (DEC-076):** EditMode asserts across 200 seeds of every profile: no arrival (phase, door line, special) at or after the 22:00 lock; every customer inside at 22:00 is served or leaves on their own patience, never cut off by the clock; Closing starts only once the store is empty. It extends `SliceTests` store-hours coverage (GAME-011).
- DP-016 / 017 / 018 / 019 / 020 pass (GAME-012). The determinism test of §7 passes (GAME-011). Gate A parity green throughout. V2 exploit rows: EX-025/026 (GAME-011); EX-013/019/021/022/024 (GAME-012); EX-016/017/023 are physical-handling rows that move with the manager refill loop (§9b) — Critical/High need their test before the system is complete (DEC-066).
- Report shows the §11 sections.

## 14. Gaps (placeholders in use) — for KNOWN_GAPS via the Hub
| GAP | Unknown store fact | Placeholder | Who |
|---|---|---|---|
| GAP-DAY-01/02/04/05/06/07/08 | backstock, location, line, packing, door line, who refills, registers | **closed by DEC-079** (values in §5, §9a) | — |
| GAP-DAY-03 | how many registers are staffed per daypart | 0/4/2/3/5/3/0 by phase (§5) | RES-002 (schedule-derived, DEC-031) |
| GAP-DAY-10 | which deli strains are "house" (two jars on the floor): tier `house` only, or also `smalls` and `premium` (the P3 house lanes)? | tiers house + smalls + premium → 2 jars (43 of 77 in-stock batches) | Nolan |
| GAP-DAY-11 | how long a jar is off the floor for a manager refill, and whether one manager handles requests one at a time | `refillWindowSimSec` 90 s (Standard), one at a time | Nolan |
| GAP-DAY-12 | do managers refill a low jar without being asked? | no: only on the budtender's request | Nolan |
| GAP-DAY-13 | capacity of the house-smalls jar (the DEC-042 product) | 454 g like the others | REF (product page) |
| GAP-DP-02 | (existing) every [GDD] number here | the values above | playtests |

## 15. Packets (dependency order; all after PS1 + PS1b, i.e. after GAME-020)
1. **UX-003** (doc-only, may start any time after this spec merges): wireframes for §2 banners/clock, §5 register map, §7 fast-forward, §9a cues/refill request, §10 tasks, §11 report.
2. **GAME-011** (Unity, Simulation/Slice): phases, clock, arrivals, registers-as-ambient, patience, fast-forward, PressureLevel, events, attribution. Needs REVIEW-PS1 and GAME-020 merged; UX-003 for the view.
3. **GAME-012** (Unity, Simulation/Slice): stock split (floor jars + HUB bags), house double jars, states, manager-refill requests and window, tags, TFS eligibility. Needs GAME-011 (phase rates in D, fast-forward stop hook). No BOH anchor needed in PS2; the manager NPC walk is optional dressing.
4. **Manager refill loop** (§9b): moves to the manager rank, after GAME-024.

Then GAME-013 (opening/closing tasks + O16 report, row unchanged), GAME-023 (unblocked once GAME-011/012 exist as packets; DEC-059 m2). PERF-002 uses §5's ambient NPC counts. Editor queue: GAME-011 → GAME-012 serialised (same `ShiftSim.cs`/`InventoryService.cs`).
