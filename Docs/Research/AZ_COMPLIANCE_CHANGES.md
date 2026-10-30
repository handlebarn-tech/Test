# AZ compliance → prioritized change list (COMP-001)

> Game design research, not legal advice. Rule numbers (A1, B1…) refer to `Docs/Research/AZ_COMPLIANCE.md`. The Hub routes these; COMP-001 edits no spec or code.

## Verdict on "overselling"
**The slice as designed cannot oversell.** One sale per customer, weight tiles 3.5/7/14/28 g, and 28 g is under the 1 oz single-transaction cap (A1, A4) whichever ounce definition is used. But nothing *enforces* it, so the first multi-item cart, custom weight or GAME-003 parsed request ("two ounces") would break DEC-032. Fix = a cheap POS guard now, plus a mechanic later.

No slice wording breaks a rule: customer lines state their own need, chips are search labels, and no card or toast makes a health claim (H1).

## MUST-FIX — slice (GAME-002, small)
| ID | Change | Where | Why | Test |
|---|---|---|---|---|
| M1 | POS hard cap: Confirm blocked when the transaction's total grams > `adultUseLimitGrams` (28.0); toast "Over the 1 oz limit". Concentrate sub-cap omitted until non-flower products exist. | SLICE_DESIGN §3.1 step 7 / §4; `SliceConfig` | A1: 36-2858(A)(1)(c). DEC-032: player must never oversell | EditMode: 28 g passes; 28.5 g (or 2 × 14 g + 3.5 g if carts ever exist) blocked |
| M2 | State that every queued customer passed the check-in ID desk (21+, adult-use). POS confirm panel shows a static "21+ ID verified" line. No player action. | SLICE_DESIGN §2 / §3.1; UX_SLICE POS panel | B1/C3: sale requires verified age; the slice currently sells to customers with no stated ID check | Doc check; POS screenshot shows the line |
| M3 | Shift clock start and end stay within 07:00–22:00 (pick e.g. 14:00 start; GDD value). | SLICE_DESIGN §1 (clock) / UX `shift.clockGameTime` | G1: R9-18-308(A)(1)(a) | Assert clock range in `SliceConfig` validation |

## New `SliceConfig` constants (sourced)
| Constant | Value | Source |
|---|---|---|
| `adultUseLimitGrams` | 28.0 | 36-2858(A)(1)(c) "one ounce"; 28 g conservative (A4, ounce undefined) |
| `adultUseConcentrateLimitGrams` | 5.0 (unused in slice) | 36-2858(A)(1)(c) |
| `salesHoursStart` / `salesHoursEnd` | 07:00 / 22:00 | R9-18-308(A)(1)(a) |
| `taxRate` | 0.251 (unchanged) = excise 0.16 + TPT 0.091, additive | 42-5452(A)(D); Phoenix 2.8% from 2025-07-01 (OPEN-4) |
| later: `medicalLimitGrams14d` | 70.87 (2.5 oz) | 36-2816(A) |
| later: `medicalTaxRate` | 0.091 | ADOR FAQ (TPT only) |

## SHOULD — slice if cheap (flavor, no player burden)
- S1 POS tax line may split "Excise 16% · TPT 9.1%" (F2/F5). Optional; not legally required, keep total identical.
- S2 Inspect/Detail already shows lab-derived data: it doubles as "test results on request" (D6). No change.
- S3 Exit: the sold jar/bag is a child-resistant container (D4); ART prop note only.

## LATER — mechanics (post-slice, DEC-032 "fun decisions")
| ID | Mechanic | Rules | Notes |
|---|---|---|---|
| L1 | **Limit meter at POS** + customer-generator "over-limit" asks (~3% of customers: "two ounces", or 1 oz + 5 g concentrate + more). Player must cap or split; selling over = violation strike in the shift report, not game over. | A1, A8 | Turns overselling into a decision. Needs carts/multi-item |
| L2 | **ID check event** at the counter when the check-in desk is busy (rush): cases = valid, expired, under-21 license, "turned 21 < 30 days ago" vertical license (valid), out-of-state license (valid). Missed bad ID = strike. | B1, B2, B4 | 1 in ~8 customers; never every sale (fun) |
| L3 | **Medical customers**: card verify click, 14-day remaining meter from a seeded history, no excise (9.1% tax). Out-of-state card → adult-use sale. | A5–A7, F4 | Adds a price/limit trade-off |
| L4 | Repeat customers same day: per transaction legal; daily cap only if store policy says so. | A2 | Blocked on OPEN-2 |
| L5 | Visibly intoxicated customer may be refused (store policy, labeled as such). | B3 | Optional flavor mechanic |
| L6 | Packaged products (DEC-020): catalog validator for edible 10/100 mg caps and banned shapes; 5 g concentrate cap active. | E1, E2, A8 | Before any edible/vape ships |
| L7 | World flavor pass: licensed-scale seal (D1), POS camera dome (C4), entry license + pregnancy warning signs (G2), no-consumption sign (H2), agent badge (C2). | | ART backlog |

## OMITTED (fun > realism)
Waste/destruction logs (G5, spec §829), recalls (G6), delivery (G7), daily inventory paperwork beyond the shift report (G3), seed-to-sale data entry (G4), medical system data entry (A6 → one click), label data entry (D5 → prints itself).

## Copy rule (all text, all waves) — H1
Customers may state needs ("something for pain"). Player-facing system text never promises an effect: no "treats", "cures", "will help your …". Use "people often pick this for …" style if a why-line returns. Already consistent with GAMEPLAY_SIMULATION_SPEC §386/§2005.

## Proposed DEC entries
- **DEC-0xx** POS enforces the AZ adult-use cap: ≤ 28.0 g flower per transaction (≤ 5 g concentrate when relevant); over-limit Confirm is blocked in the slice; later an over-limit sale is a logged violation strike, never silent. (A1, M1, L1)
- **DEC-0xx** Slice customers are adult-use, 21+, ID-verified at check-in (automated); medical customers and counter ID checks are post-slice mechanics. (B1, M2, L2, L3)
- **DEC-0xx** Sales clock stays within 07:00–22:00. (G1, M3)
- **DEC-0xx** Tax model: adult-use = pre × (1 + 0.16 + TPT), medical = pre × (1 + TPT); TPT 9.1% Phoenix (provisional, OPEN-4); tool's 25.1% remains authoritative. (F1–F4)
- **DEC-0xx** Copy rule: no efficacy claims in system text. (H1)

## Questions only Nolan can settle
1. Does the store cap purchases per day, or only per transaction? (OPEN-2)
2. Is ID checked at a front desk/vestibule before the sales floor, and does the budtender re-check at the register? (M2, L2)
3. Can you share a recent receipt's tax lines (excise vs TPT split, Phoenix rate)? (OPEN-4)
