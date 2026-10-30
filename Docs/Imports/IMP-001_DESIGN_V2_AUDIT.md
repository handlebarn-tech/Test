# IMP-001 — Audit of Nolan's DISPO_GAME_DESIGN_V2 import

**Status:** audit only. Nothing in the pack is adopted until it passes review and **Nolan approves it** (PROJECT_STATE "Pending from Nolan"). Integration is a later task.
**Input:** `C:/Users/handl/Downloads/Dispo Game Imports/DISPO_GAME_DESIGN_V2/`, read in full and in place (not edited, copied or moved). The `.py` files were read but **not run**.
**Manifest:** `sha256sum -c MANIFEST.sha256` → **27/27 OK**. The 28th file is the manifest itself. No extra or missing files.
**Compared against:** `DECISIONS.md` (DEC-001/002/006/014/015/016/032/034–051), `GAMEPLAY_SIMULATION_SPEC.md` (GSS), `Design/ROADMAP_POST_SLICE.md`, the Ready packets GAME-006..010, `Specs/UX_PS1.md`, `SliceConfig.json`, and DES-003 on `review/wave-4q` (not merged): `SPEC_DECISION_PRESSURE.md` (cited as **DP §n**), `DES-003_RECONCILIATION.md`, the DES-003 handoff (proposed DEC-P1..P6), and the new packets QA-002, UX-005 and GAME-017..024.
**Verdicts:** ADOPT = use as written · ADAPT = use, changed to fit canon · REJECT = do not use · COVERED = canon or DES-003 already has it · PARK = sound, but for gated PS4 (no work now).

## Headline
1. **V2 is a ChatGPT expansion of the same design line as DP (DES-003).** It never cites DP or DES-003. It says it builds on a "DISPO_GAME_NEW_CHAT_DESIGN_HANDOFF", which is not in the pack. About 70 % of its systems are already in DP and the DES-003 packets. The value it adds is **numbers, schemas and test catalogues** for those systems, not new direction.
2. **The TFS boundary is clean.** V2 pins v7.11.4 (DEC-002), keeps hidden truth out of live TFS (DP §5), and allows TFS calls only for post-hoc evaluation (DEC-P1). It forbids difficulty, outcome or expiry from touching TFS. **Nothing in V2 overrides the budtender tool's recommendation logic.** Two points need care (C3, C6).
3. **It has no PII.** It has no real store data and makes almost no store-fact claims. The few it makes are listed in §4.
4. **Real conflicts with DES-003:** ambiguity scale, the DecisionQuality formula, the resolution enum, the promotion model and values, the reservation model, and UX keys (§3). In each case DP is the Nolan-authored spec and keeps precedence unless Nolan says otherwise (V2's own hierarchy, 16 §20, puts "explicit Nolan decision" above V2).
5. **No new packets are needed.** Approved V2 content becomes starting values and acceptance additions for existing packets (§5).

---

## 1. Inventory (28 files, ~330 KB)
| File | Covers |
|---|---|
| `README_FIRST.md` | Pack purpose, TFS boundary (v7.11.4 authority), file list, V1→V2 corrections, merge order. |
| `01_SYSTEM_CONTRACTS.md` | Truth ownership table, invariants (INV-TFS/CUST/INV/TXN/SEED/DIFF/PROG), named RNG streams, True/Reveal/Known/TFSInput layers, DecisionRecord, counterfactual info analysis, BestAvailableResolution (lexicographic), inventory event ledger, staff/task/PO state machines. |
| `02_CUSTOMER_GENERATION_BIBLE.md` | Profile schema, constraint classes (hard/soft/context/hidden-revealable), 6 archetypes with shares, ambiguity 0–3 with distributions, viability classes, 14-step generation pipeline, compatibility rules, consultation preference, question families, RevealPlan, dialogue realization, anti-repetition windows, acceptance logit, follow-up states, repeat lifecycle, fictional outcome. |
| `03_SHIFT_PACING_QUEUE_MODEL.md` | 32/26/35-min shifts, phase tables, Gamma bounded-renewal arrivals, per-archetype service medians, patience medians, active-service patience, queue bands, abandonment attribution, recovery, restock pacing, events, quiet-time compression, sim results, acceptance gates. |
| `04_DIFFICULTY_SYSTEM.md` | 11 internal axes, 5 player sliders, Beginner/Standard/Expert table, PressureBudget points, escalation order, assists, no hidden dynamic difficulty. |
| `05_PROGRESSION_CAREER.md` | Ladder Budtender→Trusted/Senior→Lead→AM→Manager, 6 competencies, per-customer IS/RQ/QE/NSJ/DQ formulas, shift competency formulas, median-of-6 evidence model, 4 gate tables, unlocks, specialization, grind prevention. |
| `06_ECONOMY_ORDERING.md` | Economic state, contribution metric, purchasing headroom, demand bands, safety-stock formula, reorder point, supplier model, breadth/depth, CoverageScore, risk states, expiry, deals, labour, storage zones, ordering UI, policy stress test. |
| `07_MANAGER_STAFF_GAMEPLAY.md` | Staff model and AI, roles, escalation, Lead actions, breaks, AM pre-shift planning, readiness, receiving, inventory exceptions, manager horizon, staffing plan, merchandising, intervention cost, fatigue. |
| `08_UX_INTERACTION.md` | Interaction state machine, key/controller bindings, focus model, customer HUD (known-only), question UI, TFS modes, ProductIntent, retrieval, weighing, POS, warning tiers, rush shortcuts allow/deny, manager UX, back/cancel contract, accessibility, UI perf targets. |
| `09_CONTENT_LONGEVITY.md` | Repetition risks vs systems, 0–50+ h experience arc, variety matrix, 15 scenario types, mastery objectives, repeat share cap, batch turnover, authoring priority, repetition telemetry. |
| `10_EXPLOIT_FAILURE_ANALYSIS.md` | 70 exploits (EX-001..070) with severity, fix, over-correction risk and QA link. |
| `11_MASTER_QA_SCENARIOS.md` | Index of 100 scenarios (70 exploit regressions + 30 feature cases), execution tiers. |
| `12_CONTRADICTION_AUDIT.md` | V2's self-audit against its handoff (40 rows), numeric consistency, open unknowns. |
| `13_IMPLEMENTATION_SEQUENCE.md` | Epics A–J with acceptance gates, explicit deferrals. |
| `14_RESEARCH_VALIDATION_NOTES.md` | 5 outside citations (queues, server availability, assortment, safety stock) and sim caveats. |
| `15_TFS_ORACLE_CAPTURE_SPEC.md` | How to capture v7.11.4 fixtures locally, snapshot schema, parity tolerances, difficulty parity matrix. |
| `16_CROSS_SYSTEM_INTEGRATION.md` | Causal chain, cause/effect matrix, per-service may/may-not rules, 24-event vocabulary, 8 integration tests, conflict hierarchy. |
| `CONFIG/default_tuning.yaml` | All V2 numbers (shift profiles, customer mix, patience, queue, gates, economy, staff, pressure budget). |
| `CONFIG/data_contracts.yaml` | Schema summary (KnownCustomerFact, TFSInputSnapshot, InventoryEvent, Transaction, Staff/Task/PO states, DecisionRecord, ShiftState) and 7 invariants. |
| `QA/qa_scenarios.json` | 100 scenarios + abstract fixtures (`INV_*`, `C_*`). No TFS expected outputs, by design. |
| `VALIDATION/shift_queue_sim.py` | Single-server discrete-event queue harness (numpy/pandas). |
| `VALIDATION/shift_queue_results.csv` | Its output (5 difficulty/policy rows). |
| `VALIDATION/inventory_policy_stress.py` | 18-SKU stylised ordering sim, 5 policies. |
| `VALIDATION/inventory_policy_results.csv` | Its output. |
| `VALIDATION/progression_gate_stress.py` | Monte Carlo of the median-of-6 gates over 7 synthetic profiles. |
| `VALIDATION/progression_gate_stress.csv` | Its output. |
| `VALIDATION/PROGRESSION_GATE_STRESS.md` | Short interpretation of the gate stress test. |
| `MANIFEST.sha256` | SHA-256 of the other 27 files (verified OK). |

---

## 2. Per-system verdicts
| # | System (V2 source) | Verdict | Matches / conflicts | Goes to |
|---|---|---|---|---|
| 1 | TFS boundary, version pin (README; 01 §1–2 INV-TFS-01, INV-CUST-01; 16 §3) | COVERED | DEC-001/002/009; DP §0A, §2.1–2.2, §5; DES-003 Gate A | QA-002 (no change) |
| 2 | TFS oracle capture + difficulty parity matrix (15) | COVERED | DEC-014 goldens (`EngineGoldenTests`), QA-002 parity gate, DP-028. V2's "never snapshot v7.11.5" is consistent with the goldens staying v7.11.4 (see DES-003 N1). | QA-002 |
| 3 | Named deterministic RNG streams, `Hash64(shiftSeed, stream, entity)` (01 §3; INV-SEED-01; EX-027/028/062/069) | ADAPT | Not in DP. GSS has seeded sim only. Concrete and testable: adding dialogue must not reshuffle arrivals. | GAME-017 (generator), GAME-024 (save persists stream state) |
| 4 | Known-fact provenance `{fact_id, value, source, revealed_at, confidence}`, append-only (01 §4; data_contracts) | COVERED/ADAPT | DP §4 `KnownField<T>` + RevealSource. V2 adds `revealed_at`/`confidence`: fold into GAME-017's field. | GAME-017 |
| 5 | DecisionRecord + immutable TFSInputSnapshot hash (01 §4–5; 16 §5) | ADAPT | DP §116–117 logs; GSS §94. V2's per-query input hash is the useful addition (proves "result changed only because input changed", 15 §Known-input). | GAME-020 (record), QA-002 (hash assertions) |
| 6 | Counterfactual InformationSufficiency: post-shift, re-run canonical TFS with one unasked answer added (01 §6; 05 §3.1) | ADAPT | Allowed under DEC-P1 (evaluation may call TFS, never writes back). DP has InformationCompleteness/Risk (§15–16) but no counterfactual. Strong anti-autopilot tool (EX-001/003). | GAME-019 (metric), GAME-020 (report) |
| 7 | BestAvailableResolution, lexicographic, TFS rank as exposed (01 §7) | ADAPT | DP §21 (over service actions). V2's ordering is a usable concrete rule; must stay over service actions, not strain ranking. | GAME-019 |
| 8 | Inventory event ledger + ledger invariant (01 §8; INV-INV-01) | COVERED | GSS §30, `InventoryService` single authority; DP §2.3 | — |
| 9 | Reservation flow `Available→Reserved→Sold`, deli scoop temporary handling (01 INV-INV-02; 08 §12; EX-013/016/017) | ADAPT (later) | **Conflicts with GAME-006** ("Cancel changes nothing (no reservation, unchanged rule)"). GSS §67 has reservation. See C5. | GAME-012/014 or PS4, not PS1 |
| 10 | Staff/task/PO state machines (01 §9–11; 07) | PARK | DP §87–92 (PS4 gated); GSS §60–61 | PS4 roadmap |
| 11 | Customer profile schema (02 §3) | COVERED/ADAPT | DP §3 + GAME-017 field list. V2 adds `viability_class`, `ambiguity_level`, `conflict_tags`, `budget.type HARD/SOFT`. | GAME-017 |
| 12 | Constraint classes hard/soft/context/hidden-revealable; "no critical fact unknowable" (02 §4, §12) | ADOPT | DP §20 (hard/soft); V2's "context" and "hidden-but-revealable" classes and the reveal-route rule are sharper. | GAME-017 |
| 13 | Six archetypes (02 §5) | COVERED | GSS §11 lists the same six. V2 adds Standard shares (22/24/14/16/14/10) and a 35 % cap. Slice has 3 (`SliceConfig`). | GAME-022 (shares as [GDD] placeholders) |
| 14 | Ambiguity tiers 0–3 + per-difficulty distributions (02 §6) | ADAPT | **Conflicts with DP §7 tiers 0–4** (DP has a "contradictory" tier 4). See C1. | GAME-017/022 |
| 15 | Viability classes SOLVABLE/TRADEOFF/NO_VIABLE + prevalence bands; generator may inspect inventory (02 §7–9) | ADAPT | DP §28–29 NoPerfectFitRate + patterns A–G. V2 gives bands and a retry cap (12, degrade to SOLVABLE). Viability check must use the TFS oracle, never a second fit model (C6). | GAME-022 |
| 16 | Compatibility rules (02 §9) | ADOPT | Not in DP. Prevents nonsense profiles (e.g. hard budget + price-insensitive). | GAME-017 |
| 17 | Consultation preference QUICK/NORMAL/DEEP with second ranges (02 §10) | COVERED/ADAPT | DP §13–14 DesiredConsultationDepth. V2 seconds = [GDD] starting values. | GAME-017/019 |
| 18 | Question families (02 §11) | COVERED | DP §9 Q1–Q8 (V2 adds "comparison priority", "quantity"; Q5 product type gated on PS3) | GAME-017 |
| 19 | Dialogue realization pipeline + example openers (02 §13) | ADAPT | GSS §10, §48; DP §6. Openers must pass copy rule H1 (COMP-001: no effect promises). Example lines are customer speech, so they are fine. | GAME-017 (`SliceLines.json`) |
| 20 | Anti-repetition windows 20/50 customers (02 §14; 09 §10) | ADOPT | Not in DP. Testable, cheap. | GAME-017 (+ GAME-020 telemetry flags) |
| 21 | Acceptance logit with TFS-tier term (02 §17) | ADAPT | DP §25 per-customer PurchaseThreshold; slice `acceptThreshold` + `Fit(trueFamily)`. **V2 grades only on known constraints**, which would let a customer accept a product that breaks an unrevealed avoidance. See C3. | GAME-019 |
| 22 | Follow-up states + 2-loop cap (02 §18) | ADAPT | DP §26 / GSS §17 have 9 responses (keep those names). The loop cap is new and useful (EX-010). | GAME-019 |
| 23 | Repeat lifecycle, 9 templates, RepeatMemory schema (02 §19; 09 §7) | COVERED/ADAPT | DP §53–59; GAME-021. V2's templates and 10–20 % repeat cap are good content targets. | GAME-021 |
| 24 | Fictional post-use outcome, never judges TFS (02 §20) | COVERED | DP §60, DEC-P2 | — |
| 25 | Shift pacing + queue model: phase tables, Gamma renewal, service/patience medians, acceptance gates (03; tuning yaml) | ADAPT | DP §61–64 (25–40 min, example 34 min); DEC-P5. V2's 32-min Standard fits. **Not for the slice**: GAME-010 keeps its 16-customer quick shift (slice patience 90–150 s, 3 archetypes). | DES-004 → GAME-011 |
| 26 | Active-service patience multipliers + 60 s relief cap (03 §8) | ADOPT | DP §12 friction; not this mechanic. Closes EX-010 infinite Compare. | GAME-019 |
| 27 | Abandonment attribution player vs structural (03 §11) | ADOPT | DP §38 QueueCost; no attribution rule yet. Needed so progression doesn't punish impossible traffic. | GAME-020, GAME-024 |
| 28 | Recovery windows, restock pacing 2–4/shift, quiet-time compression rules (03 §12–15) | ADAPT | DP §49, §61–63; GSS §69. Concrete targets. | DES-004, GAME-011/012 |
| 29 | Difficulty presets table, axes, 5 sliders (04 §2–4) | ADAPT | DP §66–70 (fields only, no numbers). V2 numbers = [GDD] starting values. 5 player sliders are extra scope: defer until presets play well. | GAME-022 |
| 30 | PressureBudget points (04 §5; EX-068) | ADOPT | Not in DP. Stops accidental impossible stacks. | GAME-022 |
| 31 | Assists orthogonal to difficulty, assist-aware targets, no hidden DDA (04 §11–12) | ADOPT | GSS §45; UX-002 assists. | GAME-022, UX-005 |
| 32 | Per-customer IS/RQ/QE/NSJ + DQ composite (05 §3) | ADAPT | **Conflicts with DP §22–23, §34** (DQ = regret-based; QE sits in ServicePerformance, not DQ). See C2. RQ/NSJ score bands are usable. | GAME-019/020 |
| 33 | Shift competency formulas + anti-compensation floor (05 §4) | ADAPT | DP §71–77 (inputs only, no formulas). V2 gives formulas. | GAME-024 |
| 34 | Evidence model: median of last 6 eligible shifts, stability rule, seed-repeat gives no evidence (05 §5, §11) | ADAPT | **Conflicts with DP §79** rolling `0.8·old + 0.2·recent`. See C4. | GAME-024 |
| 35 | Gate values, 4 gates incl. Manager, "Trusted/Senior" naming (05 §6) | ADAPT | **Conflicts with DP §80 values** (V2 is higher; DP has 3 gates). Both are placeholders (GAP-DP-02). See C4. | GAME-024 |
| 36 | Promotion review screen, no demotion, specialization (05 §8–10) | ADAPT / PARK | DP §81, §86. Specialization = PS4+. | GAME-024 (review screen), PS4 |
| 37 | Economy, ordering, safety stock, supplier, CoverageScore, deals, storage (06) | PARK | DP §93–100; GSS §74–76; ROADMAP PS4 gated. CoverageScore uses TFS only as oracle (OK under DEC-P1). Deals must exclude deli (RES-001 P7/P8; GAME-016); V2 doesn't say so (C8). | PS4 roadmap (DES) |
| 38 | Manager/staff gameplay (07) | PARK | DP §87–92; GSS §60–61. Staff call the same TFS (DP §88). | PS4 roadmap |
| 39 | UX interaction state machine, warning tiers, back/cancel contract, ProductIntent, stale-result handling (08 §2, §10–11, §15, §20; 16 §6) | ADAPT | UX-002/`UX_PS1.md`, UX-005. Stale-snapshot validation closes EX-020. | UX-005, GAME-018 |
| 40 | Key/controller bindings (08 §3–4) | ADAPT | **Conflicts with `UX_PS1.md`** (avoids C and 1–5; R = Refuse in the ID panel). See C7. | UX-005 |
| 41 | Customer HUD shows known facts only, unknown fields absent; generic question menu (08 §6–7; EX-012/059) | ADOPT | DP §4, §17 (CUSTOMER INFO status). V2's "absent, not ???" rule is a sharp anti-leak rule. | UX-005 |
| 42 | Rush shortcuts allowed / forbidden lists (08 §18) | ADOPT | Consistent with DP §48 (don't automate). | UX-005 |
| 43 | Accessibility list + UI perf targets (08 §21–22) | COVERED/ADAPT | UX-002 (text scaling, condition M1), GSS. | UX-005 |
| 44 | Content longevity arc, scenario list, mastery objectives (09) | ADAPT (later) | GSS, ROADMAP order. The 0–50 h arc agrees with PS1→PS4. Scenario list feeds GAME-023 and later content. | GAME-023 (scenario seeds), content backlog |
| 45 | Exploit catalogue EX-001..070 (10) | ADOPT (as checklist) | DP-001..032 cover ~25 of them. The rest (ledger idempotency, save-reroll, PO cancel, etc.) are new. Severity rule: Critical before a system ships. | QA-002 + each owning packet |
| 46 | QA scenarios JSON (11; QA/) | ADAPT | Templated: the 70 exploit rows carry generic action text, and fixtures are abstract (`BAT-A`, family "A"), not real batches. Usable as a **test plan**, not runnable fixtures. Bind to real catalog batches per DEC-014. | QA-002 harness |
| 47 | Integration event vocabulary (24 events) + "reports are projections of events" (16 §17–18; EX-060) | ADOPT | GSS has `ProductReserved` etc. partly; DP §122 event-driven. | GAME-020 |
| 48 | Conflict hierarchy (16 §20) | COVERED | Matches DEC-001 + Hub process; Nolan decision on top. | — |
| 49 | Implementation epics A–J + deferrals (13) | REJECT (as plan) | Superseded by ROADMAP PS1→PS1b→PS2→PS3→PS4 and DES-003 packets. The deferral list matches GSS §100 / DP §131. | — |
| 50 | Outside research (14) | ADOPT (as notes) | Generic operations references, not store facts. The links were not checked. | DES-004 / PS4 reading |

---

## 3. Conflicts and recommended resolutions
| ID | Conflict | Recommendation |
|---|---|---|
| **C1** | Ambiguity: V2 0–3 (02 §6) vs DP 0–4 with tier 4 "contradictory" (DP §7). | Keep **DP 0–4**. Re-map V2 shares as [GDD] (Standard e.g. 25/40/20/10/5: V2 tier 3 split into DP 3 and 4). Decide in GAME-022. |
| **C2** | DecisionQuality: V2 `DQ = .40RQ + .30IS + .20QE + .10NSJ` vs DP `DQ = 1 − clamp(Regret/Tolerance)` and `ServicePerformance = .55DQ + .15QE + .10CDF + .20Speed`. V2 puts QE inside DQ and again in Service Judgment (double count). | Keep **DP's structure** (DQ = regret only; QE separate). Use V2's IS counterfactual as an **input to DecisionRegret** (a missed critical fact = regret), and its RQ/NSJ bands as starting regret values. GAME-019. |
| **C3** | Acceptance: V2's logit uses only **known** constraints + the TFS tier shown. DP-002 (hidden avoidance) and slice `ShiftSim.Fit(trueFamily)` (DEC-P1) grade against the **true** intent through the TFS oracle. Under V2 a customer happily buys something that breaks an avoidance they never mentioned, so not asking is never punished at the counter. Only the post-shift IS catches it. | Keep **DEC-P1**: the customer reacts using the TFS oracle on true intent (evaluation only). V2's logit terms (price, wait, consultation, repeat) can be the other components of the per-customer threshold. |
| **C4** | Promotion: V2 median-of-6 + stability, gates Senior 70/65/60/75/65 … plus a Manager gate and "Trusted/Senior". DP: rolling 0.8/0.2, Trusted 60/55/50/70, 3 gates. | **Nolan's design call** (Hub decision D1). V2 has a structural stress test (`progression_gate_stress.csv`) and closes EX-032 hot-streak. EWMA is simpler. Placeholder: DP as in GAME-024 until decided. |
| **C5** | Reservation: V2 reserves stock on product intent and holds deli scoop as temporary handling. GAME-006 deliberately has **no reservation** (cancel changes nothing). | PS1 keeps GAME-006 (one player, one register, no concurrency, so nothing to race). Reservation becomes necessary only with staff or several registers. Add it to GAME-012/014 or PS4 when concurrency exists; GSS §67 already describes it. |
| **C6** | Viability / no-perfect-fit generation "solves the constraint bundle against store state" (02 §8 step 9) without saying how fit is judged. | The check must call the TFS engine (DEC-P1 oracle) on the true profile. No V2-side fit model. Write it into GAME-022 acceptance. |
| **C7** | Keys: V2 `C` Compare, `R` reopen TFS, `1–5` result slots, `Q` questions, `Tab` Floor Mode. `UX_PS1.md`: new keys avoid I, C, M, F3, 1–5 (dialogue); `R` = Refuse in the ID panel. | UX-005 owns the map. Take V2's **focus model** (one owner of keys at a time), which resolves `R`/`1–5` per panel, but don't take V2's letters wholesale. |
| **C8** | Deals: V2 deals are generic (06 §14, 07 §17). Real store: weekday deals exclude deli (RES-001 P7/P8; GAME-016). | PS4/GAME-016 keep the deli exclusion. V2 deal mechanics apply to packaged only. |
| **C9** | Shift numbers: V2 Standard ~19 arrivals / 32 min; ROADMAP PS1 exit uses a 16-customer shift; GAME-010 targets 16 for the quick shift. | No clash once scoped. V2 numbers are **PS2 (DES-004/GAME-011)** inputs; the slice quick shift keeps GAME-010's values. |
| **C10** | Inventory states: V2 EMPTY_WITH_BACKSTOCK gates the physical path (EX-019, 08 §13) but doesn't say whether TFS still lists the batch. | Follow DEC-P4 (placeholder: TFS eligibility = building total) and DES-003 question N2 to Nolan. No new question. |
| **C11** | Validation harness caveats (not a canon conflict). (a) `shift_queue_sim.py` restarts the Gamma renewal clock at each phase, so the table's nominal rates give ~19.1 + 2 specials ≈ 21 expected arrivals, but the sim yields 19.3. A Unity port must copy that behaviour or retune. (b) Question cost is a fixed adder per ambiguity tier, so "ask-none wins on queue" is true by construction, not a finding. (c) `inventory_policy_stress.py` uses one z = 1.28 for all SKUs, not the 06 §7 service classes (1.65/1.41/1.04). (d) The gate stress test samples competencies independently (SD 6). It is structural only, as V2 itself says. | Treat all V2 numbers as [GDD] starting values (GAP-DP-02). Any port re-validates in C# EditMode (GAME-011/022/024). |

---

## 4. Store-fact claims (Nolan must confirm before use)
V2 makes few store claims, and labels most of its numbers as tuning. Checked:
- **Confirmed by canon:** no daily limit, per-transaction only (EX-064 = DEC-049). Limit aggregates across categories (EX-063 = DEC-048). TFS v7.11.4 paths (15 = DEC-002). Unity 6000.6.7f1 (12 = DEC-003). Packaged items are fetched, not self-serve (08 §13 ≈ DEC-050). Deli is the core workflow (DEC-020/034).
- **Unconfirmed: these need Nolan** (they matter only when PS2/PS4 work starts; placeholders are fine until then):
  1. **Storage zones** (06 §16): V2 lists deli/FOH, packaged FOH, BOH ambient, **cold storage**, **cooler/perishable**, **receiving staging**. Canon has a fridge (drinks) and a cooler (concentrates, perishable edibles) (DEC-050), plus BOH/FOH racks (DEC-041). It has no separate "cold storage" and no named receiving area.
  2. **Supplier behaviour** (06 §9): lead time 1–3 shifts, fill rate 88–100 %, emergency premium 8–20 %, partial fills and substitutions. Canon has only "regular deli shipment on Thursday" (RES-001 O8).
  3. **Expiry / sell-by** (06 §13): which categories have a real horizon (edibles? beverages?). Canon has none. V2 correctly forbids potency decay.
  4. **Staffing and breaks** (07 §4, §8): roles (counter, deli/scale, packaged retrieval, entry support, restock, receiving), one break window per staff member per block, "policy bounds". Canon: a security guard scans IDs at entry (DEC-048), and GAME-008 has the player sometimes cover check-in. Store headcount per shift and break policy are unknown.
  5. **Career titles** (05 §1): Budtender → Trusted/Senior → Lead → Assistant Manager → Manager. This is a design label in both V2 and DP. Should it match the real store's titles?

---

## 5. Proposed integration plan (only after review + Nolan's approval)
**Prerequisites:** W4Q (DES-003) merged; DEC-P1..P6 ratified; Hub decisions D1–D2 below.
**Mechanism:** one doc task (suggest **IMP-002**, docs-only). It copies the approved V2 files verbatim to `Docs/Design/Imports/DESIGN_V2/` (as DES-003 did with the DP spec). It adds "Read: DESIGN_V2 §x" lines and acceptance bullets to the packets below. It changes no code and creates no new GAME packets.

In dependency order:
1. **QA-002** (Gate A harness, can run now): add the V2 exploit catalogue as a checklist. Critical rows EX-013..016, 018, 020, 049, 050, 057..059, 063, 070 must map to a test or to an owning packet. Add input-hash assertions (row 5). Bind fixtures to real catalog batches, not `BAT-A` (row 46).
2. **PS1 (GAME-006..010, UX-002): no change.** V2 adds nothing PS1 needs. EX-063/064 are already in GAME-007 and DEC-049. Reservation is deferred (C5).
3. **GAME-017:** constraint classes + reveal-route rule (12), compatibility rules (16), anti-repetition windows (20), RNG streams (3), fact provenance fields (4), generator retry cap. Ambiguity per C1.
4. **UX-005:** focus model, known-only HUD (41), warning tiers / back-cancel / stale result (39), rush shortcut lists (42), assists (31). Keys per C7.
5. **GAME-018:** ProductIntent + stale-snapshot check before commit (39).
6. **GAME-019:** counterfactual IS as a regret input (6, C2), BestAvailableResolution ordering (7), RQ/NSJ bands, 2-loop follow-up cap (22), active-service patience + 60 s cap (26), acceptance per C3.
7. **GAME-020:** event vocabulary + reports as event projections (47), DecisionRecord (5), abandonment attribution (27), repetition flags (20).
8. **GAME-021:** 9 repeat templates, repeat share 10–20 % (23).
9. **GAME-022:** preset numbers (29) remapped per C1, PressureBudget (30), viability bands (15) with the TFS-oracle check (C6), archetype shares (13).
10. **DES-004 → GAME-011/012 (PS2):** V2 03 queue model as the starting proposal (25, 28), with the C11 caveats. Restock pacing 2–4 per shift.
11. **GAME-023:** pick seeds from V2's scenario list (44).
12. **GAME-024:** evidence model and gates per D1 (33–36); persist RNG stream state (3).
13. **PS4 (gated):** V2 06/07 become the reference design for DES's PS4 roadmap when the gate opens (37, 38), together with the §4 store answers.

### Decisions for the Hub (design, not store facts; the Hub decides or escalates)
- **D1 Promotion model (C4):** V2 median-of-6 + stability + 4 gates, or DP rolling 0.8/0.2 + 3 gates. Recommendation: V2's **model** (it closes a real exploit and has a stress test) with **DP-level gate values** for the first gates, and all values GAP-DP-02.
- **D2 Precedence:** where V2 and DP differ (C1–C3), DP wins unless Nolan says otherwise. Recommendation: yes, and C1–C3 are resolved as above.

---

## 6. Plain-language summary for Nolan
Your V2 pack is a detailed, numbers-heavy version of the decision-pressure ideas we already took in from your spec (DES-003). It doesn't touch how the budtender tool recommends strains, and it contains no customer data. Most of it fits plans we already have. What it adds: exact starting numbers for shift pacing, difficulty and promotions; rules that keep customers from feeling repetitive; and a list of 70 ways a player could game the system, each with a test.

**What we'd use:** the customer-generation rules, the anti-cheese list (as a test plan), the queue and shift numbers for the full-shift milestone (PS2), the difficulty "pressure budget", the "did the player miss a question that mattered?" check, and the UX rules about never leaking hidden customer facts.
**What we'd change:** where V2 and your earlier spec disagree (ambiguity levels, how decision quality is scored, how a customer judges a product), your earlier spec wins. The one real choice is **how promotions work**: V2 uses "your typical result over the last 6 shifts", and the earlier spec uses "a running average". We recommend V2's way with gentler starting thresholds.
**What waits:** ordering, suppliers, staff and manager play stay parked until the management milestone (PS4).
**Nothing changes in the current milestone (PS1).**
To approve: say "approve as recommended", or edit any line above. We'd also need short answers on storage areas, deliveries, expiry, staffing/breaks and job titles (§4) before PS2/PS4, not now.
