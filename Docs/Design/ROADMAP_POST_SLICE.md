# ROADMAP — after the vertical slice (DES-002)

**Status:** ratified as the post-slice plan (PS1b by DEC-057; AUDIT-001 E2, DEC-064). **Row states here are as of DES-002/DES-003; the live state of every task is `Docs/BACKLOG.md`.** Original line: proposal for the Studio Hub. Task IDs from GAME-006 on are new proposals; the Hub may renumber. Rows use the `Docs/BACKLOG.md` format.
**Extended 2026-10-30 by DES-003** with Nolan's decision-pressure spec (`SPEC_DECISION_PRESSURE.md`, cited as DP §n; status per item in `DES-003_RECONCILIATION.md`): new §2b, PS2 rows GAME-021..024, notes on GAME-011/012/015/016 and PS4.
**Add-on 2026-10-30 by IMP-002** with Nolan's V2 pack (`DESIGN_V2/`, DEC-063; audit `Docs/Imports/IMP-001_DESIGN_V2_AUDIT.md`, cited as V2 `<file>` §n): starting numbers for PS2 rows DES-004/GAME-011/012 and the PS1b/PS2 packets GAME-017..024; PS4 note. DP wins where V2 differs (DEC-063a). No PS1 change.
**Citation key (AUDIT-001 C7, DEC-064):** "spec §n" / "GSS §n" = `GAMEPLAY_SIMULATION_SPEC.md`; "DP §n" = `Design/SPEC_DECISION_PRESSURE.md`; "V2 <file> §n" = `Design/DESIGN_V2/`. In DP, DP-001…032 are the §115 tests; the §123 workcells are cited as DP-WC-001…011.
**Labels:** [SRC] = store fact, law or tool source (cited) · [GDD] = game-design decision · GAP = unknown with a labelled placeholder (see the specs).

## 0. Where we are
- **Slice on main:** one 12-customer deli-flower shift at one register. Chip intent → engine → 3 cards → assisted weigh → POS (28 g cap, "21+ ID verified", nickel rounding) → jar fill / LOW / SOLD OUT → report (GAME-002, GAME-002b, DEC-036/044).
- **In flight:** ART-003/004 lookdev + HUB swap, PROC-002/003 jar fill, GAME-005 fill hook, PERF-001, BUILD-005.
- **Known fun gaps** (GAME-002 handoff "Tuning"; SLICE_DESIGN §9):
  1. A perfect player scores 100 on every customer; budgets are always met. No tension.
  2. Every sale is one strain, one weight. The only decision is the chip.
  3. The legal rules exist only as silent blocks (DEC-036). DEC-032 wants some of them to be decisions.
  4. No restock, so stock never makes the player move; no opening/closing, so it isn't a "shift".
  5. Deli only, but flower is ~70 % of real sales (RES-001 A1, DEC-034).

## 1. Ordering rule (DEC-008, spec §104)
"Shortest path to fun" = **the most new player decisions per unit of new art and new data.** Management only after testers can play several shifts and want to improve (spec §104, §103 G7).

| Candidate | New decisions | New art | New data/facts needed | Verdict |
|---|---|---|---|---|
| Cart + compliance decisions (COMP-002) + retune | trim an over-limit cart, ID calls, medical vs adult-use, two-item asks | almost none (UI, an ID card) | none beyond COMP-001 / RES-001 | **First (PS1)** |
| Full shift day: open/close, traffic curve, deli restock | when to leave the counter to restock, rush handling | BOH/HUB dressing (ART-003/004 already doing rooms) | backstock quantities (GAP) | **Second (PS2)** |
| Packaged assortment (GAME-004) | add-ons, format/dose matching, FOH fetch | many package meshes, racks, coolers | **no packaged catalog exists** (GAP-PKG-01) | **Third (PS3)** |
| Management (ordering, deliveries, merchandising, staff) | longer-term trade-offs | office, HUB receiving | demand history, costs | **Gated (PS4)**, not decomposed |

PS3 goes last mainly because it needs product data we don't have: placeholders work for a prototype, but a real catalog has to come from Nolan (Dutchie/LeafLogix export, RES-001 O14).

---

## 2. PS1 — "Counter Decisions" (next milestone)
**Goal:** the same counter, but every customer can now force a real call. Maps to spec G3 (pressure) + part of G6 (archetypes). Design: `SPEC_COMP002.md`.
**Exit test (playtest):** in a seeded 16-customer shift a perfect-information bot scores < 100 average, a careless bot gets ≥ 1 strike, and three human testers each name at least one decision they "had to think about" (spec §104 bullets 1–3).

| ID | P | Title | Depends on | State |
|---|---|---|---|---|
| UX-002 | P1 | PS1 UX spec: cart/POS lines, limit meter, ID card inspect panel, medical POS mode, strike toast + report rows (wireframes) | DES-002 | Ready |
| GAME-006 | P1 | Cart: multi-line deli sales (2 strains / 2 weights per customer), cart-aware POS total, M1 cap on cart grams, generator two-item asks | GAME-002b, UX-002 | Ready |
| GAME-007 | P1 | COMP-002 §2 purchase-limit meter + over-limit asks (trim decision) + strike ledger in the report | GAME-006 | Ready |
| GAME-008 | P1 | COMP-002 §3 ID-check events: "cover check-in" during the rush, 7 ID cases, accept/refuse, strikes | GAME-007 (strike ledger), UX-002 | Ready |
| GAME-009 | P2 | COMP-002 §4 medical customers: MED badge, 14-day rolling meter from seeded history, 9.1 % tax, out-of-state card → adult-use | GAME-007 | Ready |
| GAME-010 | P1 | Retune for tension: budget/patience tables, 16 customers, QA bot personas (perfect / careless / slow), exit-test harness | GAME-006 | Ready |
| REVIEW-PS1 | P0 | Review PS1 wave (GAME-006..010, UX-002) + playtest exit test | all PS1 | Later |
| COMP-002 | P2 | (design done: `Docs/Design/SPEC_COMP002.md`; implementation = GAME-007/008/009) | — | Done on DES-002 merge |

Parallelism: UX-002 and GAME-010 can start at once; GAME-006 needs UX-002's cart wireframe only for its view layer (it may start on the Simulation side first). GAME-008 and GAME-009 can run in parallel after GAME-007. All are Unity tasks: keep ≤2 editors (studio-parallelism rule), so GAME-006 → GAME-007 → (GAME-008 ‖ GAME-009) is the editor queue, GAME-010 is mostly Simulation/EditMode.

## 2b. PS1b — "Customer Intelligence" (DES-003, from DP §3–38, §101–117)
**Goal:** the player wins by learning the right facts before using the real TFS tool, not by clicking the top card; the game can credit a good decision even when the customer ends up only moderately happy. Same counter, same jars. Design: GSS §49, §92, §105 as amended; spec DP §0A boundary in every packet.
**Exit test:** Gates B and C (DP §125–126): DP-002/003/010/011 and DP-004/006/007/008 pass in EditMode; on a seeded 16-customer shift an "ask the right question" bot beats both "first card, no questions" and "ask everything" on mean DecisionQuality (GAME-020 metric); QA-002 parity gate green throughout.

| ID | P | Title | Depends on | State |
|---|---|---|---|---|
| QA-002 | P0 | TFS parity gate (Gate A) + DP scenario harness: identical TFS input → identical output across sim state; hidden fields never reach TFS input | — (EditMode; can start now) | Ready |
| UX-005 | P1 | Counter-intelligence UX: question menu, KNOWN-facts strip + CUSTOMER INFO status, query preview, Similar/Compare/Details entry, "Nothing fits right now" no-sale, dev debug panel, report v2 decision sections | UX-002 merge | Ready |
| GAME-017 | P1 | Customer knowledge: TRUE fields on `Customer`, KNOWN profile, opener reveal sets, ambiguity tiers, questions Q1–Q4/Q6–Q8, tolerance + friction, completeness/risk, query composer → `QueryParser` (DP-001/002/003/010/011) | GAME-006, GAME-007, GAME-010 merged; QA-002; UX-005 for the view | Ready |
| GAME-018 | P1 | TFS workflows at the counter: Similar, Compare, Details through the ported `Responder`/`Similarity` (parity), as player choices with time cost | GAME-017 | Ready |
| GAME-019 | P1 | Service evaluation + resolutions: `ServiceEvaluator` (ServiceUtility, BestAvailableResolution, DecisionRegret, DecisionQuality), per-customer purchase threshold, ASK_* responses + follow-up reveals, informed/avoidable no-sale, `ServiceResolution`, consultation-depth fit, QueueCost (DP-004..009, 013..015) | GAME-017, GAME-018 | Ready |
| GAME-020 | P1 | Decision telemetry + shift scoring: per-customer/per-shift logs (DP §116–117), debug explanation (§114), SERVICE/FLOW/OPERATIONS + star gate + severe flags (§101–112) replacing satisfaction-average stars | GAME-019 | Ready |
| REVIEW-PS1b | P0 | Review PS1b + Gates B/C | all PS1b | Later |

Order: QA-002 and UX-005 start now (no Unity editor / doc-only). GAME-017 → GAME-018 → GAME-019 → GAME-020 is one editor queue on `Simulation/Slice/` after PS1's GAME-006/007 (same files). PS1b is placed before PS2 because DP §133 calls the information game the highest-priority playable target and it needs no new art.

## 3. PS2 — "Full Shift Day"
**Goal:** a shift that starts, peaks twice and closes, and stock that makes the player leave the counter. Spec G4 + G5 (§6, §7, §31–32, §73).
**Store facts used:** hours 08:00–22:00 (RES-001 O1, DEC-036 M3); rushes at opening and 17:00–20:00 (O12); closing checklist (O11); regular deli shipment on Thursday (O8); deli BOH audit at close (O11); BOH/FOH wire racks (DEC-041).
**Exit test:** a 3-phase shift (open → two rushes → close) plays in 25–40 real minutes [GDD, DP §62; was 20–30, DEC-056 (was DEC-P5)]; at least one jar runs LOW and the player restocks it from BOH; the report shows the O16-style sections.

| ID | P | Title | Depends on | State |
|---|---|---|---|---|
| DES-004 | P1 | Shift-day design (renamed from DES-003, an ID now used by the decision-pressure intake): DP §61–65 as input; compressed 08–22 clock, traffic curve from O12/O13, opening-lite (2–5 min, spec §7), closing-lite (O11 subset), restock rules, report v2 fields (O16). **V2 starting proposal** (DEC-063, all [GDD]): Standard 32 min in 7 phases Opening 2 / Steady 5 / Rush 1 6 / Recovery 4 / Rush 2 6 / Late 5 / Report 4, ≈ 18–20 arrivals (Beginner 26 min ≈ 13, Expert 35 min ≈ 22); Gamma bounded-renewal arrivals (k 2.5) + 2 seeded special slots; service medians per archetype 32–76 s; queue patience medians 140 / 230 / 330 s; acceptance gates 2–6 % abandonment, mean peak queue 2.5–3.5; recovery 3–4 min after a ≥ 5 min rush; quiet-time compression never skips a decision (V2 `03_SHIFT_PACING_QUEUE_MODEL.md` §1–17, `CONFIG/default_tuning.yaml`; audit rows 25, 28). Caveats (audit C11): phase rates are nominal (a port must restart the renewal clock per phase or retune); the V2 harness is a **single server**, so DES-004 states how many of the 11 registers (DEC-039) are open (REVIEW-IMP1 §3); fits DEC-056 25–40 min | REVIEW-PS1 | Later |
| UX-003 | P2 | Shift-day UX: phase banners, opening/closing task list, restock prompts (LOW/CRITICAL/deal/trend cues, never "restock this now", DP §48), report v2 | DES-004 | Later |
| GAME-011 | P1 | Shift phases + traffic curve + compressed clock (replaces the 12-customer slice shift; slice stays as a "quick shift" mode); DP §61–64: Recovery phase, variable time compression, `PressureLevel` 0–1 for audio/NPC/pacing/telemetry (never TFS), demand inputs incl. deal, repeat customers, availability (DP §51). V2: phase table + arrivals + patience from DES-004; named RNG streams (V2 `01_SYSTEM_CONTRACTS.md` §3); abandonment attribution (V2 03 §11); exploit rows EX-025/026 (`DESIGN_V2/QA_TEST_PLAN.md`) | DES-004 | Later |
| GAME-012 | P1 | Deli restock loop: jar LOW → walk to BOH → pick the same batch's backstock → refill jar (carry system spec §63); backstock grams per batch = GAP-DAY-01 placeholder. DP §40–50: ServiceReady/Back/Total stock, states HEALTHY/LOW/CRITICAL/EMPTY_WITH_BACKSTOCK/SOLD_OUT (CRITICAL from recent demand), internal `RestockUrgency`, interruptible task states, restock tags proactive/reactive/emergency; TFS eligibility per DEC-055 (was DEC-P4; = DEC-055, confirmed by DEC-061); acceptance adds DP-016..019. V2: 2–4 meaningful restock decisions per Standard shift, > 2 emergencies is a diagnostic (V2 `03_SHIFT_PACING_QUEUE_MODEL.md` §13); EMPTY_WITH_BACKSTOCK gates the physical path, not TFS (V2 `08_UX_INTERACTION.md` §13); reservation arrives here or in GAME-014 if concurrency exists (audit C5); exploit rows EX-013/016/017/019/021–024 | DES-004, ART-005, DEC-P4 | Later |
| GAME-013 | P2 | Opening/closing tasks + report v2 (Income/Tax/Category/Customer Rec-Med sections, O16); decision/flow/inventory sections come from GAME-020 | GAME-011, GAME-020 | Later |
| GAME-021 | P1 | Repeat customer memory (DP §53–59): persistent fictional ids, purchase memory with the TFS query used, outcome tags, memory pre-fills KNOWN fields, confidence/decay, same strain new batch | GAME-017, GAME-019 | Ready |
| GAME-022 | P1 | Difficulty profiles Beginner/Standard/Expert + no-perfect-service patterns A–G (DP §28–29, §66–70) | GAME-019, QA-002 | Ready |
| GAME-023 | P0 | Decision-pressure acceptance shift (DP §133): one seeded 12–20-customer shift with the full mix, expert vs first-card vs ask-everything bots; Gates B–D | GAME-011, GAME-012, GAME-018..022 | **Blocked** (DEC-059 m2: needs GAME-011/012 packets; do not dispatch) |
| GAME-024 | P2 | Career competencies + promotion gates + versioned save v1 (DP §71–81, §120–121); Gate F | GAME-020, GAME-023 | Ready |
| ART-005 | P1 | BOH/HUB stock dressing + restock anchors (racks per DEC-041, deli backstock location = GAP-DAY-02) | ART-004 merge | Later |
| PERF-002 | P2 | Perf pass with a full-day NPC count | GAME-011, PERF-001 | Later |
| REVIEW-PS2 | P0 | Review PS2 + playtest exit test | all PS2 | Later |

## 4. PS3 — "Packaged Floor" (GAME-004)
**Goal:** the other ~30 % of sales (RES-001 A1): add-ons, format/dose asks, FOH fetches, the 5 g concentrate cap and edible rules. Design: `SPEC_GAME004.md`.
**Exit test:** ≥ 30 % of customers buy at least one packaged item [GDD target near A1's 70/30 split]; average ≈ 2 units per sale (RES-001 O13); packaged stock visibly depletes in FOH (spec §23).

| ID | P | Title | Depends on | State |
|---|---|---|---|---|
| DATA-002 | P1 | Packaged catalog schema + placeholder catalog (every SKU tagged PLACEHOLDER) and an importer ready for a real Dutchie/LeafLogix export (GAP-PKG-01) | SPEC_GAME004 | Later |
| PROC-004 | P1 | Package generator variants for 9 formats (SPEC_GAME004 §6), using PROC-001 `package_base`; sizes are GAP-PROC-04/05 placeholders | PROC-001, PROC-003 | Later |
| ART-006 | P1 | FOH fulfillment racks + coolers (GAP-111, REFERENCES_INDEX §2.3), concentrate fridge (RES-001 F6), merch rack (F5), floor display case (F4) placement | ART-005, PROC-004 | Later |
| UX-004 | P2 | Packaged UX: category tabs, format/dose filter, packaged cards, cart lines | DATA-002 | Later |
| GAME-014 | P1 | Packaged sales: shelf stock authority, FOH fetch, cart lines, concentrate 5 g sub-cap + edible validator (COMP-002 §5) | GAME-007, DATA-002, ART-006 | Later |
| GAME-015 | P1 | Non-flower recommendation: strain-linked items via the engine (tool parity), constraint match for the rest [GDD] (SPEC_GAME004 §4; TFS boundary note there, DEC-054 (was DEC-P3)) | GAME-014, DEC-054 (was DEC-P3) | Later |
| GAME-016 | P2 | Deals v1: weekday category deals that exclude deli (RES-001 P7/P8); values GAP; acceptance adds DP-025/026 (deal demand → stock pressure, never a TFS fit change) | GAME-014 | Later |
| REVIEW-PS3 | P0 | Review PS3 + playtest exit test | all PS3 | Later |

## 5. PS4 — Management (gated, not decomposed)
Ordering → deliveries (Thursday deli, manifest check, RES-001 O8) → HUB receiving → merchandising (spec §75–76) → staffing (§61). **Gate:** spec §104 met after PS2 at least. DES writes the PS4 roadmap only when the Hub opens the gate. Constraints already fixed by DP §87–100 (GSS §60, §75): staff skills change information gathering and speed, never the recommendation model; complex customers escalate to the player; ordering has lead time, storage limits and imperfect demand signals; management reaches the floor only through authoritative inventory (Gate G, DP-032). Covers spec DP-010/DP-011. **V2 reference design, parked (DEC-063d):** V2 `06_ECONOMY_ORDERING.md` and `07_MANAGER_STAFF_GAMEPLAY.md` (economy, safety stock, suppliers, CoverageScore via the TFS oracle only, staff AI, breaks, receiving) are the DES input when the gate opens. Their open store questions (storage zones, deliveries, expiry, staffing/breaks, job titles; IMP-001 handoff Q1–5) are asked then. Deals keep the deli exclusion (RES-001 P7/P8, audit C8).

## 6. Cross-cutting
- **Tool parity stays the top rule** (DEC-001/002/006): nothing in PS1–PS3 changes engine scoring. New logic is [GDD] and lives in Simulation.
- **Gate A (DP §124):** from QA-002 on, every gameplay PR keeps `TfsParityGateTests` green: identical TFS input + inventory + pricing → identical TFS output whatever the queue, rush, difficulty, memory or KNOWN state. Evaluation code (GAME-019 `ServiceEvaluator`) may call the engine but never writes back to it.
- **V2 add-on (DEC-063):** `DESIGN_V2/` is an add-on to DP; DP wins on conflicts. The parity oracle is the **shipped** engine (v7.11.4 + DEC-015/016, DEC-060); a TFS input snapshot is the **parser input** (DEC-057), never a structured fact path; the report never shows TFS scores or ranks (DEC-052). V2's 70 exploits are a test plan (`DESIGN_V2/QA_TEST_PLAN.md`) built in QA-002's harness by the owning packets.
- **Copy rule H1** (COMP-001) applies to every new line: needs may be stated by customers; system text never promises an effect.
- **Brand names:** real brands in data are an open trademark call for Nolan before any public build (PROJECT_STATE, REVIEW-W2A m2). PS3 placeholders use generic names.
