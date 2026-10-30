# ROADMAP — after the vertical slice (DES-002)

**Status:** proposal for the Studio Hub. Task IDs from GAME-006 on are new proposals; the Hub may renumber. Rows use the `Docs/BACKLOG.md` format.
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

## 3. PS2 — "Full Shift Day"
**Goal:** a shift that starts, peaks twice and closes, and stock that makes the player leave the counter. Spec G4 + G5 (§6, §7, §31–32, §73).
**Store facts used:** hours 08:00–22:00 (RES-001 O1, DEC-036 M3); rushes at opening and 17:00–20:00 (O12); closing checklist (O11); regular deli shipment on Thursday (O8); deli BOH audit at close (O11); BOH/FOH wire racks (DEC-041).
**Exit test:** a 3-phase shift (open → two rushes → close) plays in 20–30 real minutes [GDD]; at least one jar runs LOW and the player restocks it from BOH; the report shows the O16-style sections.

| ID | P | Title | Depends on | State |
|---|---|---|---|---|
| DES-003 | P1 | Shift-day design: compressed 08–22 clock, traffic curve from O12/O13, opening-lite (2–5 min, spec §7), closing-lite (O11 subset), restock rules, report v2 fields (O16) | REVIEW-PS1 | Later |
| UX-003 | P2 | Shift-day UX: phase banners, opening/closing task list, restock prompts, report v2 | DES-003 | Later |
| GAME-011 | P1 | Shift phases + traffic curve + compressed clock (replaces the 12-customer slice shift; slice stays as a "quick shift" mode) | DES-003 | Later |
| GAME-012 | P1 | Deli restock loop: jar LOW → walk to BOH → pick the same batch's backstock → refill jar (carry system spec §63); backstock grams per batch = GAP-DAY-01 placeholder | DES-003, ART-005 | Later |
| GAME-013 | P2 | Opening/closing tasks + report v2 (Income/Tax/Category/Customer Rec-Med sections, O16) | GAME-011 | Later |
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
| GAME-015 | P1 | Non-flower recommendation: strain-linked items via the engine (tool parity), constraint match for the rest [GDD] (SPEC_GAME004 §4) | GAME-014 | Later |
| GAME-016 | P2 | Deals v1: weekday category deals that exclude deli (RES-001 P7/P8); values GAP | GAME-014 | Later |
| REVIEW-PS3 | P0 | Review PS3 + playtest exit test | all PS3 | Later |

## 5. PS4 — Management (gated, not decomposed)
Ordering → deliveries (Thursday deli, manifest check, RES-001 O8) → HUB receiving → merchandising (spec §75–76) → staffing (§61). **Gate:** spec §104 met after PS2 at least. DES writes the PS4 roadmap only when the Hub opens the gate.

## 6. Cross-cutting
- **Tool parity stays the top rule** (DEC-001/002/006): nothing in PS1–PS3 changes engine scoring. New logic is [GDD] and lives in Simulation.
- **Copy rule H1** (COMP-001) applies to every new line: needs may be stated by customers; system text never promises an effect.
- **Brand names:** real brands in data are an open trademark call for Nolan before any public build (PROJECT_STATE, REVIEW-W2A m2). PS3 placeholders use generic names.
