# SPEC — GAME-004 packaged assortment (DES-002)

**Milestone:** PS3 "Packaged Floor" (`ROADMAP_POST_SLICE.md` §4). Implementation tasks: DATA-002, PROC-004, ART-006, UX-004, GAME-014, GAME-015, GAME-016.
**Labels:** [SRC] = store fact (RES-001 row in `Docs/Research/OFFICE_FINDINGS.md`), law (COMP-001 rule) or tool source · [GDD] = game-design decision · GAP-PKG-nn = unknown, placeholder in use.
**Hard rule:** no packaged product, price or quantity is a store fact unless cited. There is **no packaged catalog** in the repo (the budtender tool is deli flower only, DEC-020/034), so every SKU below is a labelled placeholder until real data arrives (GAP-PKG-01).

## 1. Scope (DEC-034)
The real store's Dutchie categories are BEVERAGE, EDIBLE, EXTRACT, Flower, MERCH, PRE-PACK, PREROLL, TOPICAL, VAPE; flower is ~70 % of net sales; daily deals cover prepack flower, concentrates, edibles, vapes and prerolls (RES-001 A1, P7). The slice sells deli only; PS3 adds the eight packaged categories.

| Category (Dutchie) | Game format examples | Known facts | Compliance (SPEC_COMP002 §5) | Priority [GDD] |
|---|---|---|---|---|
| PRE-PACK (flower) | sealed 3.5 g can/jar | house DGT 3.5 g cans in three colourways (A2) | counts flower grams toward 28 g | 1 |
| PREROLL | single, multipack | category exists (A1) | flower grams toward 28 g (GAP-COMP-02) | 2 |
| VAPE | cartridge, disposable | High Variety / tōk Liquid Diamonds vapes (A2) | concentrate grams toward 5 g (GAP-COMP-02) | 3 |
| EDIBLE | gummies, chocolate | ≤ 10 mg/serving, ≤ 100 mg/package (E1); no child-attractive shapes (E2) | 0 g placeholder (GAP-COMP-02) | 4 |
| EXTRACT | jar/syringe of concentrate | refrigerated concentrate case on the sales floor (F6) | concentrate grams toward 5 g | 5 |
| BEVERAGE | can/bottle | High Tide 10 mg seltzers (A2) | 0 g placeholder; mg caps as edible (E1 assumed, GAP-PKG-08) | 6 |
| TOPICAL | balm, lotion | category exists (A1) | 0 g placeholder | 7 |
| MERCH | apparel, accessories | "Fresh Goods from TFS" merch + display fixture (F5); Night Splash and employee discounts exclude merch (P8) | none (not cannabis) | 8 |

Priority follows spec §53 (deli → packaged flower → preroll → vape → edible → concentrate → others). PS3 may ship categories 1–4 first and the rest as a follow-up if the wave runs long.

## 2. Where packaged stock lives (FOH = fulfillment room)
Known [SRC]: A011 labels the west room **FOH FULFILLMENT 180.26 SF** (GAP-102 closed). FOH has chrome wire racks with clear sorted bins, a white fridge and **two glass-door coolers** (CCTV R4C1, REFERENCES_INDEX §2.3: FOH wire racks ×2 8.0 × 1.4 ft, fridge 1.6 × 3.6 ft; DEC-041 FOH still). BOH has chrome wire racks of packaged stock and stacked black cases (R4C2, DEC-041). HUB holds pallets/cases (bulk). On the **sales floor**: a refrigerated concentrate case in a corner (F6), a locked brand display case (F4), a merch garment rack (F5, R3C2). Register counter space is kept for deal sheets, EDLPs and in-house signs (F8). Fridge range 35.6–46.4 °F (O9).

Game placement [GDD on SRC fixtures]:
| Fixture | Holds (game) | Basis | Player action |
|---|---|---|---|
| FOH wire racks, sorted bins | PRE-PACK, PREROLL, VAPE, EDIBLE, TOPICAL (sell stock) | R4C1/DEC-041 show packaged stock in bins; **which category sits where is GAP-PKG-02** | walk to FOH, pick from the bin (spec §23 "retrieve FOH stock") |
| FOH glass-door coolers (2) | BEVERAGE (+ chocolate edibles) | coolers exist (R4C1); contents unknown, **GAP-PKG-03** | pick from cooler |
| FOH white fridge | none (staff fridge placeholder) | contents unknown, GAP-PKG-03 | — |
| Sales-floor concentrate case | EXTRACT | F6 (High) | pick from the case (position GAP-111) |
| Locked brand display case | display only (one brand, visual) | F4 | flavor |
| Merch garment rack | MERCH | F5 (Med), R3C2 | pick from rack |
| BOH racks | backstock for FOH bins | DEC-041 | restock (PS2 GAME-012 loop extended) |
| HUB | cases/pallets | REFERENCES_INDEX §2.1 | out of scope until PS4 receiving |

**Why behind-the-counter fetch:** the photos show packaged stock in FOH/BOH bins, not open shelves on the sales floor, and the spec's packaged flow is "identify → retrieve FOH stock → scan → bag" (§23). It adds physical movement the slice lacks (spec §4.4). Fetch distance is the cost the player manages under rush pressure.

## 3. Transaction flow
`identify (card/filter) → add to cart → fetch from fixture (carry, spec §63) → POS line → bag` (spec §23). No weighing. Shelf stock is one authority per SKU (as `InventoryService` for jars, spec §30); bin and cooler visuals deplete in steps [GDD]. Cart, limit meter and caps from SPEC_COMP002 §2/§5.

## 4. Recommendation for non-flower
The budtender tool (v7.11.4) scores **strains/batches of deli flower** only. Anything else is new design.

| Case | What applies | Label |
|---|---|---|
| PRE-PACK and PREROLL of a strain that exists in the tool DB | the engine's strain profile and ranking (same `FindStrains` scores; the item is offered as another form of that strain) | **tool parity** for the scores; the SKU→strain link is [GDD] data (DATA-002 field `strainKey`) |
| VAPE / EXTRACT named for a tool strain | engine strain profile used as a **hint** only; extraction changes terpene ratios, so fit is scored at `concentrateFitFactor` × strain fit | [GDD] (the tool says nothing about concentrates) |
| Strain-less items (edibles, beverages, topicals, unlinked vapes/extracts) | **constraint match**: category, dose (mg), pack size, price vs budget, brand ask. No effect claim. | [GDD] |
| MERCH | no recommendation; impulse add-on line from the customer generator | [GDD] |

**TFS boundary note (DES-003, DP §0A; ruling pending as DEC-P3, decide before GAME-015):** the TFS tool has no non-flower model, so the game must not present one. (a) `concentrateFitFactor` may only scale the *evaluation* fit (satisfaction / GAME-019 ServiceUtility); it never reorders or filters the strain cards the player sees, and it is not shown as a fit score. (b) For strain-less items the "constraint match" is a catalog filter on stated format, dose, pack size, price and brand, sorted by a neutral key (price, then name); it is not a ranking and makes no effect claim.

Design rules for the [GDD] parts:
- Customer asks for strain-less items are about **format, dose, price or brand** ("a 100 mg pack of gummies", "a cheap disposable"), never about an effect the item would cause (COMP-001 H1 copy rule). Effect-family asks (sleep, pain…) still go to flower/prepack/preroll via the engine; a player who hands a strain-less item to an effect ask gets `nonStrainEffectFit` [GDD].
- UI: a category tab + filter chips (format, dose, price band). Strain-linked items appear as an extra "also as: prepack / preroll" row on the existing flower cards (UX-004).
- Scoring reuses the slice formula (fit/price/speed, SLICE_DESIGN §3.4); fit for constraint matches = share of the customer's constraints met [GDD].

| Key | Value | Label |
|---|---|---|
| `concentrateFitFactor` | 0.8 | [GDD] |
| `nonStrainEffectFit` | 0.3 | [GDD] |
| `addOnChance` (merch / second packaged item) | 0.25 | [GDD]; tune toward ≈ 2 units per sale (O13) |
| `packagedAskShare` | 0.30 | [GDD], from flower ≈ 70 % of sales (A1) |

## 5. Pricing (all GAP)
No packaged price is known (GAP-PKG-04). Known shape only: shelf prices are pre-tax, tax added at checkout (P2); deals change per weekday per category and **exclude deli** (P7); seasonal % promos exclude deli (P8); Night Splash 10 % and employee discounts don't apply to merch (P8); blended discount target ≤ 40 % (P9). Average ticket ≈ $27–34 and ≈ 2 units per sale (O13) are tuning targets, not prices.

Placeholders (pre-tax; every value is **GAP-PKG-04, not a store fact**; DATA-002 marks each SKU `placeholder: true`):
| Format | Placeholder price | Basis of the placeholder |
|---|---|---|
| Prepack 3.5 g | the tool's deli price for the linked strain's tier at 3.5 g | reuse `TIER_DEFAULTS` [SRC L21018] so no new number is invented |
| Preroll single (1 g) | tool tier price per gram × 1 g | same |
| Preroll multipack | single × count | [GDD] |
| Vape 0.5 g / 1 g | GAP-PKG-04 placeholder $20 / $35 | [GDD] round number |
| Extract 1 g | GAP-PKG-04 placeholder $25 | [GDD] |
| Edible 100 mg pack | GAP-PKG-04 placeholder $15 | [GDD] |
| Beverage 10 mg can | GAP-PKG-04 placeholder $6 | [GDD] (10 mg from A2) |
| Topical | GAP-PKG-04 placeholder $25 | [GDD] |
| Merch | GAP-PKG-04 placeholder $25 | [GDD] |
Tax: adult-use 25.1 % (DEC-001), medical 9.1 % (SPEC_COMP002 §4); POS nickel rounding (DEC-035). Deals (GAME-016): types % off, BOGO, quantity tiers, bundles, gift-with-purchase (P7); values GAP-PKG-05.

## 6. Assets (PROC-004 / ART-006)
Reuse PROC-001 `package_base` (box / pouch) and add variants: can (prepack, beverage), tube (preroll), cart box (vape), small jar (extract, topical), pouch (edibles), folded garment/cap (merch). All dimensions are placeholders (GAP-PROC-04/05/06); label art is generic, no real brand marks until Nolan's trademark call (PROJECT_STATE "Open"). Edible packaging follows E2/H3: no cartoon, fruit, animal or toy imagery. Tri budgets per PROC-001 runner.

## 7. GAPs raised (proposed for `Docs/KNOWN_GAPS.md`)
- GAP-PKG-01 | data | no packaged catalog (SKUs, strains, mg, sizes, stock) | placeholder catalog | Dutchie or LeafLogix inventory export from Nolan (O14), PII-free
- GAP-PKG-02 | building | which category sits on which FOH/BOH rack/bin | §2 placeholder | Nolan / a closer FOH still
- GAP-PKG-03 | building | contents of the two FOH glass-door coolers and the white fridge | §2 placeholder | Nolan
- GAP-PKG-04 | pricing | every packaged price | §5 placeholders | the export above, or the weekday price sheets (P4 zip not read)
- GAP-PKG-05 | pricing | deal values per weekday/category | none (deals off) | pre-shift briefs pattern (P7) or Nolan
- GAP-PKG-06 | store | are any packaged goods on open sales-floor shelves (self-browse), or all fetched by staff? | placeholder: fetched (except merch, extract case) | Nolan
- GAP-PKG-07 | store | which brands to show, and real names or generic (trademark) | generic | Nolan (PROJECT_STATE open item)
- GAP-PKG-08 | law | beverage mg caps (we assume edible caps E1 apply) | Low | COMP follow-up read of R9-18-313
