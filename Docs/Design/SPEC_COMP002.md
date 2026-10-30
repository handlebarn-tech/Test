# SPEC — COMP-002 post-slice compliance mechanics (DES-002)

> Game design, not legal advice. Every legal number comes from `Docs/Research/AZ_COMPLIANCE.md` (COMP-001 rule IDs A1…H3) or a RES-001 store fact (`Docs/Research/OFFICE_FINDINGS.md`, IDs O1…P9). Anything else is [GDD] (tuning) or a GAP placeholder. No law is invented here.

**DEC-032 classes:** DECISION = a fun player call · AUTO = the game/POS enforces it silently · FLAVOR = world/text only · CUT = omitted, with reason.
**Milestone:** PS1 "Counter Decisions" (`ROADMAP_POST_SLICE.md` §2). Builds: GAME-006 (cart), GAME-007 (limits), GAME-008 (ID), GAME-009 (medical).

## 1. Mapping overview
| # | Mechanic | Rules | Class | Task |
|---|---|---|---|---|
| 1 | POS hard cap 28.0 g flower / transaction | A1, A4, O4, DEC-036 M1 | AUTO (stays) | done (GAME-002); GAME-006 makes it cart-wide |
| 2 | Purchase-limit meter on the POS | A1, A8 | AUTO (display) | GAME-007 |
| 3 | Over-limit asks → trim the cart | A1 | **DECISION** | GAME-007 |
| 4 | "Ring it as two sales" request | A2, A3, OPEN-2 | CUT until OPEN-2 | — |
| 5 | ID check while covering check-in | B1, B2, O2, O3 | **DECISION** | GAME-008 |
| 6 | Missed bad ID / violation consequence | B4 | FLAVOR text + strike | GAME-007/008 |
| 7 | Medical customer: card verified | A6, O3 | AUTO (one badge) | GAME-009 |
| 8 | Medical 14-day rolling meter | A5, O4 | AUTO (meter) + **DECISION** (trim vs budget) | GAME-009 |
| 9 | Out-of-state medical card → adult-use sale | A7 | **DECISION** | GAME-009 |
| 10 | Medical tax 9.1 % | F4 | AUTO | GAME-009 |
| 11 | Concentrate 5 g sub-cap | A1, A8, O4 | AUTO (+ meter) | GAME-014 (PS3) |
| 12 | Edible 10 mg / 100 mg caps, no child-attractive shapes | E1, E2 | AUTO (catalog validator, art brief) | DATA-002 / GAME-014 (PS3) |
| 13 | Adult-use daily cap (repeat visit) | A2, OPEN-2 | CUT until OPEN-2 | — |
| 14 | Visibly impaired customer → manager refuses | B3, O5 (store policy) | DECISION (rare) | PS2 backlog (GAME-013 or later) |
| 15 | Lab results on request | D6 | DECISION already (Inspect) | — |
| 16 | Agent badge, POS camera dome, entry signs, CR exit bag, scale seal | C2, C4, G2, D4/O6, D1 | FLAVOR | ART backlog (COMP-001 L7) |
| 17 | Waste, recalls, delivery, seed-to-sale entry, label entry | G4–G7, D5 | CUT (COMP-001 "Omitted") | — |

## 2. Purchase-limit meter + over-limit asks (GAME-007)
**Rules.** Adult-use: ≤ 1 oz per single transaction, ≤ 5 g of it concentrate (A1, 36-2858(A)(1)(c)). Ounce = 28.0 g (A4, conservative). The real POS blocks the sale until every check passes (O4).

**Design.**
- AUTO: the POS keeps blocking Confirm when cart flower grams > `adultUseLimitGrams` (DEC-036 M1, now summed over the cart). Over-limit selling stays **impossible**, as at the real register (O4). This deliberately replaces COMP-001 L1's "selling over = strike": the real POS can't do it, so the game can't either (DEC-032 last sentence).
- AUTO display: a meter on the POS panel, `cartFlowerGrams / 28.0 g` (and, from PS3, `cartConcentrateGrams / 5.0 g`). Colours: under 75 % neutral, 75–100 % amber, over = red + Confirm disabled with "Over the 1 oz limit" (existing toast).
- DECISION: the customer generator sometimes asks for more than the cap. The player must **trim** and choose what to keep: drop the second strain, step a weight down (28 → 14 g), or swap to keep the best-fitting item. The customer reacts to what was trimmed: keeping the primary-intent item scores normally; trimming the primary item costs fit.
- If the player cannot make the cart legal (or refuses), the customer leaves as a no-sale.

**Ask shapes** (deli only in PS1; weights from `STD_WEIGHTS` [SRC] L21010):
| Ask | Total | Legal trim options |
|---|---|---|
| "an ounce of X and an eighth of Y" | 31.5 g | 28 of X; or 14 X + 3.5 Y; or 7 X + 3.5 Y |
| "two ounces" of one family | 56 g | 28 g |
| "a half of X and a half of Y and a quarter of Z" | 35 g | any combo ≤ 28 g |

**Numbers.**
| Key | Value | Label |
|---|---|---|
| `adultUseLimitGrams` | 28.0 | [SRC] A1, A4 (exists) |
| `adultUseConcentrateLimitGrams` | 5.0 (inactive until PS3) | [SRC] A1/A8 (exists, unused) |
| `overLimitAskChance` | 0.06 | [GDD] (COMP-001 L1 suggested ~3 %; doubled for PS1 so a 16-customer shift usually has one; retune in GAME-010) |
| `meterAmberFraction` | 0.75 | [GDD] |
| `primaryTrimFitPenalty` | 0.5 × fit of the dropped primary item | [GDD] |

## 3. ID-check events (GAME-008)
**Store facts.** One secure entry; staff verify ID before the door to the sales area opens and check guests in (O2). 21+ with a valid government photo ID; AZ vertical (under-21-format) IDs only within 30 days of turning 21; out-of-state vertical IDs accepted at 21+; medical customers are checked against the state registry (O3). Acceptable ID list: B2 (A.R.S. 4-241(K)).

**Design.** ID checking happens at check-in (O2), so the counter does **not** re-check (DEC-036 M2 stays). The [GDD] mechanic: during a rush the check-in desk backs up and the player is asked to **cover check-in** for the next few arrivals. That keeps the real flow and makes ID checking an occasional rush decision, never every sale (COMP-001 L2: "never every sale").
- Trigger: on rush start, with `coverCheckInChance`, a prompt "Check-in is backed up — cover the door?" [GDD]. Accept → the next `coverCheckInCount` arrivals show an ID card panel before they join the queue; meanwhile the counter queue's patience keeps draining (that's the cost). Decline → no ID events, a small satisfaction hit for the next arrivals' wait (they waited longer at check-in) [GDD].
- Each ID: player picks **Admit** or **Refuse**. The card shows photo, DOB, expiry, state, format (horizontal/vertical), type. The in-game date is shown on the panel [GDD].
- Outcomes [GDD]: admit valid → normal; refuse valid → that customer leaves (counts as a walkout, satisfaction 0); admit invalid → **strike** with flavor text "A minor/invalid ID got through. Stores can be fined up to $2,000 per violation." (B4, 36-2854(B)(2)); refuse invalid → small bonus to the shift's compliance row.
- Strikes never end the shift (DEC-032). Report row: `strikes`, plus "Manager review" flag at `strikeReviewThreshold` [GDD].

**ID cases** (validity from B2 and O3; mix weights [GDD]):
| Case | Valid? | Source | Weight |
|---|---|---|---|
| AZ license, 21+, unexpired | yes | B2 | 40 |
| Out-of-state license, 21+, unexpired | yes | B2 | 15 |
| Passport / military ID, 21+, unexpired | yes | B2 | 10 |
| AZ vertical, turned 21 ≤ 30 days ago | yes | B2, O3 | 10 |
| AZ vertical, turned 21 > 30 days ago | **no** | B2, O3 | 5 |
| Out-of-state vertical, 21+ | yes (store policy) | O3 (see GAP-COMP-03) | 5 |
| Expired license (any) | **no** | B2 ("unexpired") | 10 |
| Under 21 (any format) | **no** | B1 | 5 |

**Numbers.**
| Key | Value | Label |
|---|---|---|
| `coverCheckInChance` | 0.5 per rush | [GDD] |
| `coverCheckInCount` | 3 arrivals | [GDD] (≈ 1 in 8 customers over a 16-customer shift with one rush; COMP-001 L2 "1 in ~8") |
| ID case weights | table above | [GDD] |
| `strikeReviewThreshold` | 2 | [GDD] |
| fine flavor text | "up to $2,000 per violation" | [SRC] B4, 36-2854(B)(2) |
| `minAgeYears` | 21 | [SRC] B1 |
| `verticalGraceDays` | 30 | [SRC] B2, O3 |

## 4. Medical customers (GAME-009)
**Rules.** Patients may buy ≤ 2.5 oz in any rolling 14 days (A5, O4); the agent checks the registry card before each sale (A6; at check-in per O3); out-of-state cards cannot buy medical but may buy adult-use at 21+ (A7); medical pays TPT only, no excise (F1, F4).

**Design.**
- AUTO: a MED customer arrives with "MED card verified" on the POS (like M2's "21+ ID verified"); no data entry (A6 → one badge, COMP-001 "Omitted: medical system data entry").
- AUTO meter: "14-day remaining" = `medicalLimitGrams14d` − seeded purchases in the last 14 days. The 28 g adult-use cap does **not** apply to a medical sale; the remaining 14-day allotment does.
- DECISION: some MED customers have little allotment left and ask for more than remains → trim, as in §2.
- DECISION: an **out-of-state medical card** is shown at the POS as "Card: out-of-state". The player must switch the sale to adult-use (excise applies, 28 g cap). Ringing it as medical is blocked with a hint the first time, a strike after that [GDD]. (In the real POS this is likely automatic; the decision is a [GDD] teaching moment, flagged GAP-COMP-04.)
- Price: medical uses the same pre-tax tool price as adult-use (DEC-001 pricing) and `medicalTaxRate`; whether the store has medical-only pricing is GAP-COMP-05.

**Numbers.**
| Key | Value | Label |
|---|---|---|
| `medicalLimitGrams14d` | 70.87 (2.5 oz × 28.35) | [SRC] A5 via COMP-001 CHANGES (note: adult-use uses 28.0 g/oz; the 2.5 oz figure uses 28.35; GAP-COMP-06) |
| `medicalTaxRate` | 0.091 | [SRC] F4 (provisional with OPEN-4) |
| `medicalCustomerShare` | 0.10 | **GAP-COMP-01** placeholder; the real Rec/Med split exists in the Dutchie closing report (O16) but the value was not read |
| seeded 14-day history | 0–3 prior purchases of 3.5–28 g, uniform | [GDD] |
| `outOfStateMedChance` | 0.2 of MED customers | [GDD] |

## 5. Packaged-product rules (activate in PS3, GAME-014)
- Concentrate 5 g sub-cap (A1/A8, O4): AUTO; meter row appears when a cart holds an extract/vape.
- **What counts toward the caps for non-flower is unknown** (A9, OPEN-3). Placeholder until answered: extracts and vapes count their net concentrate grams toward the 5 g cap; prerolls and prepacks count their flower grams toward 28 g; edibles, beverages and topicals count 0 g. This is a labelled **GAP-COMP-02 placeholder**, never shown to players as law.
- Edible caps (E1): catalog validator rejects any edible > 10 mg THC per serving or > 100 mg per package. Shapes/names (E2, H3): art brief rule for PROC-004/ART-006.

## 6. Rolling and repeat limits
- Medical: the 14-day meter in §4 is the only rolling limit in PS1.
- Adult-use repeat visits the same day: statute is per transaction only (A2); store policy unknown (OPEN-2). **CUT** until Nolan answers (GAP-COMP-07). No repeat customers in PS1 anyway (spec §39 is G6).

## 7. Report rows (UX-002 lays them out)
`strikes` (with a one-line reason each), `idsChecked`, `badIdsCaught`, `validIdsRefused`, `overLimitTrims`, `medSales`, `medTaxCollected`, `adultUseTaxCollected` (excise and TPT split optional, COMP-001 S1).

## 8. GAPs raised (proposed for `Docs/KNOWN_GAPS.md`)
- GAP-COMP-01 | game | share of medical customers | placeholder 10 % | Dutchie closing report Rec/Med row (O16) or Nolan
- GAP-COMP-02 | law/store | how prerolls, vapes, edibles, beverages and topicals count toward the 1 oz / 5 g caps (the POS "allotments", O15) | placeholder §5 | Nolan / P&P
- GAP-COMP-03 | law/store | O3 accepts out-of-state vertical IDs at 21+ while B2's 30-day rule reads as general; we follow store policy O3 | Med | re-read 4-241(K) / Nolan
- GAP-COMP-04 | store | does the POS auto-switch an out-of-state medical card to adult-use, or does the budtender choose? | placeholder: player chooses | Nolan
- GAP-COMP-05 | store | medical-only pricing or discounts | placeholder: same pre-tax price | Nolan
- GAP-COMP-06 | law | ounce definition (28.0 vs 28.35 g) differs between our adult-use cap and medical figure | Low | OPEN-1 official text
- GAP-COMP-07 | store | adult-use daily/repeat-visit policy | cut | Nolan (OPEN-2)
- GAP-COMP-08 | building | check-in desk position for the "cover check-in" event (O2 says staff check ID before the sales-floor door) | placeholder: an anchor at the entry door inside the vestibule | REF/ART from A011 + Nolan
