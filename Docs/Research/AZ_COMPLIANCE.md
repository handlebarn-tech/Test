# Arizona cannabis compliance → game rule table (COMP-001)

> **Game design research, not legal advice.** Written 2026-10-29 for DEC-032 (realism vs fun). All sources visited 2026-10-29.

**Sources.** Statutes: azleg.gov (A.R.S.). Tax: azdor.gov, phoenix.gov. ADHS rules (A.A.C. Title 9, Ch. 17/18): the official apps.azsos.gov PDFs returned 403, so the rule text was read on Cornell LII's verbatim mirror (`https://www.law.cornell.edu/regulations/arizona/Ariz-Admin-Code-SS-<section>`). Treat rule quotes as **mirror text** until checked against the official PDF (OPEN-1).

**Classes (DEC-032):** MECHANIC = a player decision · AUTOMATED = game/POS enforces silently · FLAVOR = in the world, no rule · OMITTED = cut, with reason. **Slice?** = in the 12-customer slice now (Y), later (L), or never (–).

## A. Purchase and possession limits
| # | Rule | Citation | Plain summary | Class | Slice? | Game change |
|---|---|---|---|---|---|---|
| A1 | Adult-use sale cap | A.R.S. 36-2858(A)(1)(c) ([link](https://www.azleg.gov/ars/36/02858.htm)); R9-18-309(A) | A store may sell a consumer at most **1 oz per single transaction**, of which **≤ 5 g concentrate**. | AUTOMATED (POS hard cap) + MECHANIC (over-limit asks, later) | Y | POS refuses any cart over `adultUseLimitGrams` (28 g); slice can't reach it today, but the guard must exist. See CHANGES M1 |
| A2 | Per transaction, not per day | 36-2858 says "single transaction"; no daily cap found in statute or R9-18-309 | A same-day return visit is not barred by statute; the customer's own 1 oz possession limit (36-2852(A)(1)) still applies. Many stores add a daily policy. | MECHANIC (later, repeat customers) | L | Ask Nolan for store policy (OPEN-2) |
| A3 | Adult possession | 36-2852(A)(1) ([link](https://www.azleg.gov/ars/36/02852.htm)) | 21+ may possess ≤ 1 oz, ≤ 5 g of it concentrate. | FLAVOR | – | none |
| A4 | Ounce in grams | not defined in statute or rules read | 28 g vs 28.3495 g is unresolved. The tool's largest weight (28 g) is under either. | AUTOMATED | Y | Use 28.0 g as the cap (conservative, matches `STD_WEIGHTS`) |
| A5 | Medical 14-day cap | 36-2801(1)(a)(i), 36-2816(A) ([link](https://www.azleg.gov/ars/36/02816.htm)); R9-17-314 | Patient/caregiver may buy ≤ **2.5 oz in any rolling 14 days**. | MECHANIC (POS meter) | L | Medical customers get a "14-day remaining" meter fed from a seeded history |
| A6 | Medical pre-sale check + logging | 36-2806.02(A)(B) ([link](https://www.azleg.gov/ars/36/02806-02.htm)); 36-2807 (60-day lookback) | Before each sale, the agent checks the registry card in the ADHS verification system and logs amount, card, date/time. | AUTOMATED | L | POS "card verified" step is one click; no data entry |
| A7 | Visiting (out-of-state) patients | 36-2804.03(C) ([link](https://www.azleg.gov/ars/36/02804-03.htm)) | Out-of-state cards may possess but **cannot buy medical**; they may buy adult-use if 21+. | MECHANIC (later) | L | Out-of-state card → sell as adult-use (excise applies, 1 oz cap) |
| A8 | Concentrate sub-limit | 36-2858(A)(1)(c) | ≤ 5 g concentrate per sale. | AUTOMATED | L | Needed only when non-flower products arrive (DEC-020) |
| A9 | Edible equivalency toward the oz | not found in statute or rules read | No mg→g conversion found. | — | L | OPEN-3 before edibles ship |

## B. ID, age, refusal
| # | Rule | Citation | Plain summary | Class | Slice? | Game change |
|---|---|---|---|---|---|---|
| B1 | Verify age at sale | 36-2858(A)(2); 36-2854(A)(6) ([link](https://www.azleg.gov/ars/36/02854.htm)); R9-18-309(A)(1) | Agent must reasonably verify 21+ with a government photo ID from the A.R.S. 4-241(K) list. | AUTOMATED (slice) → MECHANIC (later) | Y | Slice: every customer passed the check-in desk; POS shows "21+ ID verified". Later: occasional ID check by the player. CHANGES M2 |
| B2 | Acceptable IDs | A.R.S. 4-241(K) ([link](https://www.azleg.gov/ars/4/00241.htm)) | Unexpired AZ DL/ID; other state, DC, territory or Canada license with photo+DOB; military ID; passport / resident card; consular ID; border crossing card. An under-21 license stops counting 30 days after the holder turns 21. | MECHANIC (later) | L | ID-check minigame cases: expired, under-21, "turned 21 last month on the vertical license" (valid ≤ 30 days) |
| B3 | Visibly intoxicated customer | none found in cannabis statutes/rules | No legal duty found (unlike liquor). Refusal rests on owner control (36-2851(7)) and store policy. | MECHANIC (later, store policy) | L | If used, label it store policy, not law |
| B4 | Under-21 offenses | 36-2853(B)(E)(F) ([link](https://www.azleg.gov/ars/36/02853.htm)) | Under-21 possession, fake ID use: civil/petty → misdemeanor. Store faces ADHS discipline, fines ≤ $2,000/violation (36-2854(B)(2)). | FLAVOR (consequence text) | L | Missed fake ID = shift "violation" strike, not game over |

## C. Facility access
| # | Rule | Citation | Plain summary | Class | Slice? | Game change |
|---|---|---|---|---|---|---|
| C1 | Restricted areas | R9-18-312 | Only officers, board members and facility agents; others supervised. | AUTOMATED (customers never path behind counter) | Y | Already true (queue manager owns paths) |
| C2 | Facility agent license | R9-18-308(A)(6)–(10) | Every employee holds a valid agent license, on them while working. | FLAVOR (badge on player lanyard) | L | Badge prop |
| C3 | Lobby ID check / visitor log | not found in R9-18-312 | A check-in vestibule is store practice, not a found rule. | AUTOMATED / FLAVOR | Y | Justifies B1 automation; do not call it law |
| C4 | Camera at each POS, 30-day retention | R9-18-312 | Each point of sale has a camera able to identify the buyer. | FLAVOR | L | CCTV dome over the register (REF-001 has 17 feeds) |

## D. Deli flower, scales, packaging, labels
| # | Rule | Citation | Plain summary | Class | Slice? | Game change |
|---|---|---|---|---|---|---|
| D1 | Scale must be licensed (W&M) | A.R.S. 3-3451(A) ([link](https://www.azleg.gov/ars/3/03451.htm)), 3-3401(13) | A sales-by-weight scale must be licensed/certified by AZ Weights & Measures. Class II/NTEP not confirmed in an AZ primary source. | FLAVOR | L | Seal sticker on the stand scale (ART) |
| D2 | Net weight accuracy | A.A.C. R3-7-101 → NIST HB 133 (unverified) | Package must hold at least the labeled weight within tolerance. | AUTOMATED | Y | Assisted scale shows exact target (already) |
| D3 | Deli-style weighing at counter | none found | No rule bans or describes it; the real store does it (DEC-021). Child-resistant packaging is required "on exit", which permits packing at the counter (inference). | FLAVOR | Y | none |
| D4 | Child-resistant on exit | R9-18-310; 36-2854 | Product leaves in child-resistant packaging. No opaque-packaging rule found. | FLAVOR (exit bag/jar) | L | CR container/bag handed over on sale |
| D5 | Label content | R9-18-310 | License #, strain, batch, form, weight, total THC/CBD, "KEEP OUT OF REACH OF CHILDREN" warning, ingredients, QR code. | AUTOMATED (label prints) | L | Printed label prop; no player data entry |
| D6 | Lab results on request | R9-18-309(A) | Store must show test results if asked. | MECHANIC (already: Inspect/Detail) | Y | Inspect satisfies it; later, "can I see the COA?" line |

## E. Product rules (post-slice; DEC-020 adds packaged goods later)
| # | Rule | Citation | Plain summary | Class | Slice? | Game change |
|---|---|---|---|---|---|---|
| E1 | Edible caps | 36-2854(A)(7)(a); R9-18-313 | ≤ 10 mg THC per serving, ≤ 100 mg per package; scored servings. | AUTOMATED (catalog data) | L | Catalog validator rejects edibles over cap |
| E2 | Child-attractive shapes/names | 36-2860(A) ([link](https://www.azleg.gov/ars/36/02860.htm)) | No human/animal/insect/fruit/toy/cartoon shapes, no kids'-brand look-alikes. | AUTOMATED (art guideline) | L | ART brief for edible packages |
| E3 | Samples, display, smell jars | not found | Not addressed in rules read. | FLAVOR (store practice) | – | Don't present as law |

## F. Pricing and tax
| # | Rule | Citation | Plain summary | Class | Slice? | Game change |
|---|---|---|---|---|---|---|
| F1 | Excise 16% (adult-use only) | A.R.S. 42-5452(A) ([link](https://www.azleg.gov/ars/42/05452.htm)) | 16% of price on adult-use sales; medical exempt. | AUTOMATED | Y | Slice customers are all adult-use; matches 25.1% |
| F2 | Rates add, don't compound | 42-5452(D); ADOR FAQ (deduction code 807) | Excise is not in the TPT base: total = pre × (1 + 0.16 + TPT). | AUTOMATED | Y | Matches slice `ApplyTax(pre, 0.251)`; no change |
| F3 | Phoenix TPT | phoenix.gov [news, July 2025](https://www.phoenix.gov/newsroom/finance-news/phoenix-tax-rates-to-see-slight-increase-starting-july-1); ADOR | State 5.6 + Maricopa 0.7 + Phoenix 2.8 (from 2025-07-01) = 9.1% → 25.1% total, matching the tool. phoenix.gov chart titles still say 8.6% (stale?). | AUTOMATED | Y | Keep 25.1% (tool authority, DEC-001); OPEN-4 |
| F4 | Medical tax | ADOR [FAQ](https://azdor.gov/transaction-privilege-tax/adult-use-marijuana/definitions-and-frequently-asked-questions) | Medical pays retail TPT only (9.1%). | AUTOMATED | L | `medicalTaxRate` 0.091 when medical customers arrive |
| F5 | Receipt itemization | none found | No rule requires itemizing excise. | FLAVOR | L | Splitting excise/TPT on the receipt is optional; don't call it required |
| F6 | Discounts, deals, free product | none found (only adult-to-adult gifting, 36-2852(A)(3)) | Day deals are not restricted by anything found. Store giveaways: unclear. | AUTOMATED | Y | Day deals stay; avoid "free product" promos until OPEN-5 |

## G. Hours, signage, records, waste
| # | Rule | Citation | Plain summary | Class | Slice? | Game change |
|---|---|---|---|---|---|---|
| G1 | Hours | R9-18-308(A)(1)(a) | Open ≥ 30 h/week, sales only between **7:00 a.m. and 10:00 p.m.**; hours posted. | AUTOMATED | Y | Shift clock must stay in 07:00–22:00 (CHANGES M3) |
| G2 | Required signage | R9-18-308(A)(13) | License and pregnancy/fetus warning (with DCS notice) visible at entry. No "under 21" sign rule found. | FLAVOR | L | Entry signage decals (ART) |
| G3 | Inventory control | R9-18-314 | Designated agent, audit ≥ every 30 days, investigate losses, 5-year records; daily start/end inventory. | AUTOMATED | Y | Jar grams already tracked per batch; end-of-shift report = flavor of the daily count |
| G4 | Seed-to-sale system | 36-2854 (tracking "at all points"); Metrc requirement unverified | Tracking required; vendor name/date not confirmed. | FLAVOR | – | Don't name Metrc in-game until verified |
| G5 | Waste/destruction | R9-18-308(A)(2)(f), R9-18-314(C)(6) | Make unusable; log reason, date, method, agent. | OMITTED | – | Spec §829 already cuts compliance destruction |
| G6 | Recalls | ADHS recall page; no rule procedure found | — | OMITTED | – | Possible later event, not core |
| G7 | Delivery | R9-18-312.01 (from 2024-11-01) | ID + signature at door, ≤ $10,000 per vehicle. | OMITTED | – | Out of game scope |

## H. Budtender conduct
| # | Rule | Citation | Plain summary | Class | Slice? | Game change |
|---|---|---|---|---|---|---|
| H1 | Health claims | 36-2859(C)(1)(4) ([link](https://www.azleg.gov/ars/36/02859.htm)) | Ads may not make health statements known to be untrue or target under-21s. Counter talk is not "advertising", but the game should not claim cures. | AUTOMATED (copy rule) | Y | Copy rule: no "treats/cures/will fix"; spec §386/§2005 already say outcomes are not medical predictions. Slice wording checked: compliant |
| H2 | Consumption on premises | 36-2851(7), 36-2853(C) | Public smoking is an offense; owners may ban use on site. | FLAVOR | L | "No consumption on premises" sign |
| H3 | Under-21 marketing | 36-2859(C) | No cartoons/toys aimed at minors. | AUTOMATED (art guideline) | L | ART/UX brief |

## Open legal ambiguities (for the change list)
- **OPEN-1** ADHS rule quotes are from Cornell LII (official PDFs blocked). Mirror may lag; R9-17-314 shows last amended 2020-11-01. Re-check against apps.azsos.gov before any public claim.
- **OPEN-2** Same-day repeat purchases: statute caps per transaction only. Does the real store enforce a daily limit? (Nolan)
- **OPEN-3** No edible/vape → flower equivalency found for the 1 oz cap.
- **OPEN-4** Phoenix city TPT: 2.8% per July 2025 release vs 8.6% combined chart titles. Read ADOR rate table row (Phoenix, code 017) or ask Nolan for a real receipt.
- **OPEN-5** Store giveaways/free product: not addressed in statute or rules read.
- **OPEN-6** Scale class (Class II / NTEP), customer-visible display and tare rules: not found in an AZ primary source.
- **OPEN-7** SB1105 (2025, amends 36-2804/36-2857, registration/local authority) seen only in a bill tracker; not counter-relevant.
