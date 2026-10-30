# OFFICE FINDINGS (RES-001)

Read-only pass over Nolan's Microsoft 365 account (Outlook mail and the OneDrive/SharePoint files he can see), 2026-10-29, under DEC-031.
These are store facts only. People appear by role, never by name. Security-sensitive details are left out: camera layout, alarm, cash/vault, keys, transport.

**Columns.** *As of* is the date of the source. *Status* tells you whether the fact still holds:
- **Current**: the source is from Oct 2026, or it is a standing policy.
- **Dated**: older material that is probably still true. Check it with Nolan before you treat it as canonical.
- **Superseded**: a newer source replaces it. Kept here for history.
- **Daily**: it changes every day (deals). Use it as a pattern, not a value.

Conf uses the REFERENCES_INDEX scale (High/Med/Low).

**Sources.**
- "Compliance drive" = a compliance staff OneDrive, under `Compliance (Master Folder)/03 Nature's Healing Center - Phoenix (dual)/`.
- "Mkt site" = SharePoint site `MarketingDepartment/Shared Documents/`.
- Mail is cited by subject and date.

## 1. Building and drawings

| # | Fact | Source | As of | Status | Conf | Affects |
|---|---|---|---|---|---|---|
| B1 | A full approved interior TI drawing set exists: RSP Architects project 3378.002.00, "Phoenix Retail Interior Phase". Sheets: G000/G101, A000 site, D101/D102 demo, **A101 floor plan + reflected ceiling plan**, A201 roof, **A310 door schedule + finish/material schedules**, A320 partitions, **A901 sections and interior elevations (Front POS, Backcounter POS, Retail Display South/West, enlarged POS plan)**, **A940 millwork**, I101 finish/furniture plan, and S/M/P/E sheets. | Mkt site `…/Deli Style Launch/_Design Files/Floor Plans/Interior TI Approved Set - PHX.pdf` | 2022-08 (rev 2022-10, approved 2022-12) | Dated: **Nolan 2026-10-29: the 2022 layout is not current**. Use it for heights, materials and fixture types, not for positions | High | GAP-101, GAP-001/002/104/108 |
| B2 | The AZDHS sheets A011 (floor plan) and A012 (lighting plan) are the source of the repo's Working Plan V5. Text and dimensions match REFERENCES_INDEX §1.1. A 2026 resubmission of the same sheets plus a security sheet was approved as a facility modification on 2026-05-28. | Compliance drive `…/Dispensary (Phoenix)/AZDHS/Application Submittals/Phoenix Dispensary Floor Plan Update - 2026/` | sheets 2023-05; set 2026-05 | Current | High | GAP-101 |
| B3 | Sheet A011 names the two small back rooms **FULFILLMENT 180.26 SF** and **PRODUCT STORAGE 163.44 SF**. Text alone does not show which drawn rect is which. | A011 (B2) | 2023-05 | Current | High (labels) / Low (mapping) | GAP-102 |
| B4 | **RETAIL ceiling: gypsum at 9'-0".** Some areas have a soffit at 7'-6" AFF. | A101 reflected ceiling plan (B1) | 2022 | Dated | High (9'-0") / Med (soffit extent) | **GAP-001** |
| B5 | Back rooms (break, hall, unisex, fulfillment, storage) have ACT-1 2×2 acoustic tile at 8'-0" or 9'-0" depending on the room. The storage rooms have gypsum. A012 also lists 2×2 ACT lighting. | A101 (B1); A012 | 2022 / 2023 | Dated | Med | GAP-001 |
| B6 | Accent ceiling CLG-1: Turf Softspan 48, colour D07 Dark Walnut, 4'×8' panels on stainless cables. This is likely the "dark ceiling baffles" seen in photo 05. | A310 (B1) | 2022 | Dated | High | ART lookdev |
| B7 | Ceiling lighting types: 2×2 troffer, recessed can, wall sconce, decorative fixture, pendant can, 1×4 linear pendant. The plan provides power drops for floor displays and power for lit signage at the soffit. A012 adds a checkout-counter light and a pendant light. It also marks "WINDOWS - NATURAL LIGHT". | A101 (B1); A012 | 2022–23 | Dated | High | ART lighting |
| B8 | Doors: **E101 retail entry is an aluminium storefront, 6'-0"×7'-0", glass.** Retail 101B has a side-folding open-air security grille 16'-4¾"×7'-6". Interior doors are hollow metal 3'-0"×7'-0"; one break-room door is 2'-8". There is a 3'-0"×7'-0" gypsum-cased open passage. | A310 door schedule (B1) | 2022 | Dated | High | **GAP-104** |
| B9 | A permit revision added a door on the east side of retail, removed the south door into storage, and turned the lounge into an office. It also replaced the main-entry storefront and reorganized the retail and break-room millwork. | City permit / C of O in the 2026 folder (B2) | completed 2023-06 | Current | High | GAP-112 (east exit exists) |
| B10 | Code facts: occupancy M, construction VB, no sprinklers, emergency lighting provided, occupant load 41. Three exits are provided where two are required. Retail/support area 1,882 SF, storage 1,797 SF. | Permit (B9) | 2023-06 | Current | High | ART exits |
| B11 | Display cases use Sugatsune XL-GC glass showcase hardware in black and chrome. Each has a quartz top with an eased edge, plastic-laminate shelves, an LED strip recessed in the curved top trim (radius about 1'-4¼"), and anti-glare film. The system is modular. | A940 (B1) | 2022 | Dated | High | GAP-002, ART display case |
| B12 | Shelving: brass brackets with a linear light between brackets. Pulls are vintage-bronze bar pulls and brushed-brass drawer pulls. Cabinet interiors are black melamine. | A940 / A310 (B1) | 2022 | Dated | High | ART jar wall |
| B13 | Counter, POS and display heights are drawn on A901/A940 but are not in the text layer. Someone has to read them off the sheets. | B1 | 2022 | Dated | n/a | **GAP-108** (open, lead found) |
| B14 | Floors: CONC-1 ground and sealed concrete; TL-1 Statuario Bianco 12×24 tile; TL-2 BF Ceramics "Madrid" 8×8 patterned tile (floor and wall); VCT-1 12×12; CPT-1 24×24 carpet. Transitions use brass/bronze Schluter trim. | A310 (B1) | 2022 | Dated | High | **GAP-113** (tile sizes) |
| B15 | Walls (Sherwin-Williams): PT-1 SW7646 First Star, PT-3 SW0016 Billiard Green, PT-4 SW6060 Moroccan Brown, PT-5 SW6057 Malted Milk, PT-6 SW9137 Niebla Azul, PT-7 SW7747 Recycled Glass, PT-8 SW6271 Expressive Plum. Base is 4" grey vinyl. FRP-1 white panels run to 4'-0" AFF. | A310 (B1) | 2022 | Dated | High | ART materials |
| B16 | Millwork finishes: PL-1 Italian Walnut laminate, PL-2 matte black laminate, ML-1 black patina metal laminate, QZ-1 Cambria "Rose Bay" quartz, QZ-2 "Vesuvius" solid surface. **The POS front is walnut veneer (WD-1).** WC-1 patterned wallcovering is used behind displays only. WC-2 woodgrain film covers the slat wall. | A310 (B1) | 2022 | Dated | High | ART counters |
| B17 | The green wall (blocking in the wall) and the backlit logo are supplied by others. The **owner-supplied neon sign is mounted at 72" AFF to the fixture bottom**. | A101/A901 keynotes (B1) | 2022 | Dated | High | GAP-111 (neon) |
| B18 | Restroom: Bobrick accessories, mirror 1'-8"×3'-6" at 3'-4" AFF, grab bars 42"/36"/18". | A901 (B1) | 2022 | Dated | High | **GAP-109** |
| B19 | Remodel scope: the north suite (about 1,932 SF) became retail, restrooms, lounge, break and fulfillment. The south suite (about 1,967 SF, the old retail) became stock rooms. | G000 narrative (B1) | 2022 | Dated | High | HUB/HUB 2 history |
| B20 | Exterior: one-storey stucco building, about 4,055 SF footprint, about 13.7' above grade. Corner lot about 112.5'×124'. 15 striped parking spaces, 1 of them accessible. Billboard on site, chain-link and wrought-iron fencing, covered bus stop at the frontage. | ALTA survey, Compliance drive `…/Real Estate/Property Documents/ALTA Surveys/` | 2021-08 | Dated | High | Exterior scene |
| B21 | The east wall is 8" reinforced CMU with stucco and partial metal siding. Inside it, a stud bearing wall carries 2×10 joists at 24" o.c. The east wall elevation shows **15'-6"**. The parapet is above the 9'-0" retail ceiling. | Wall evaluation and repair drawings, `…/Real Estate/Building Plans & Permits/Blueprints/` | 2022-01 | Dated | High | Exterior height |
| B22 | A Weights & Measures service report for the retail scales exists. It is image-only, so the scale count was not read. | `…/Dispensary (Phoenix)/Weights & Measures/` | ? | Dated | Low | GAP-107 |

## 2. Fixtures and equipment

| # | Fact | Source | As of | Status | Conf | Affects |
|---|---|---|---|---|---|---|
| F1 | The Dutchie closing report lists **12 registers**. This matches the plan's "up to 12". | "PHX EOS + EOD" closing report | 2026-06 | Current | High (count of POS stations) | **GAP-107** |
| F2 | Each budtender station has a register receipt printer, a debit reader and a scale. Deli bags and exit bags are stocked at the station. | Closing checklist ("Cleaning check list" thread) | 2026-03 | Current | High | ART POS, GAME weigh |
| F3 | Labels are Zebra 2.25"×2" direct-thermal stock. Receipt rolls are 2¼" and 3⅛". The label printer model is not stated (Zebra assumed). | Supply-order mails; label quote | 2026-09/10 | Current | Med | ART props |
| F4 | A locked, keyed **brand display case** on the floor was the Green Dot Labs case and is being handed to Shango. A photo is attached to the mail. | "Shango Display at Phoenix" | 2026-10-28 | Current | High | ART floor case |
| F5 | The "Fresh Goods from TFS" merch launch came with a merch display fixture delivered from Texwood Builds and installed in Oct 2026. This is likely the garment rack seen in R3C2. | "Upcoming TFS Merchandise Launch & Fixture Deliveries" | 2026-09-30 | Current | Med | GAP-111 |
| F6 | A refrigerated concentrate display case ("pastry fridge") sits on the sales floor, in a corner. **Nolan 2026-10-29: installed and visible in the reference material.** Which reference shows it was not identified (possibly one of the R4C1 coolers). | "Fridge for Concentrates" thread; Nolan | 2026-10 | Current | High (exists) / Low (which view) | GAP-111 (2 coolers in R4C1?) |
| F7 | There is a "PHX Marble Wrap" print file for a fixture wrap. This is possibly the white-marble surface in photo 05. | Mkt site `…/Arizona/Retail/PHX Marble Wraps/` | 2026-07 | Current | Med | ART materials |
| F8 | Counter space at the register is kept for deal sheets, EDLPs and in-house signs. Vendor table tents go on the sales-floor tables. Phoenix has less floor space than the other stores. | "3P Display in Stores" | 2026-10-28 | Current | High | ART dressing |

## 3. Operations

| # | Fact | Source | As of | Status | Conf | Affects |
|---|---|---|---|---|---|---|
| O1 | Hours are 8:00 am–10:00 pm, 7 days. | Phoenix P&P manual (mail "Updated Policies & Procedures", 2026-07-22); marketing flyer | 2026-07 | Current | High | GAME shift clock |
| O2 | There is one secure entry/exit. Staff verify ID before the door to the sales area opens. Guests are checked in to the Dutchie Guest List (scan ID, create guest). | P&P; budtender training PDF | 2026-07 / 2025-04 | Current | High | GAME queue |
| O3 | ID rules: 21+ with valid government photo ID. Arizona vertical IDs are accepted only within 30 days of turning 21. Out-of-state vertical IDs are accepted at 21+. Medical customers are checked against the state registry. | P&P | 2026-07 | Current | High | GAME ID check |
| O4 | Limits: adult-use 1 oz per transaction, of which no more than 5 g concentrate. Medical 2.5 oz per rolling 14 days. The POS blocks the sale until every check passes, including COA status. | P&P | 2026-07 | Current | High | GAME validation |
| O5 | Visibly impaired customers are refused sale. The manager on duty denies the sale and logs it. | P&P | 2026-07 | Current | High | GAME event |
| O6 | Every sale leaves in a child-resistant exit bag with the receipt. Front-of-house bags have handles and are printed "The Flower Shop". | P&P; delivery SOP | 2026 | Current | High | GAME/ART bag |
| O7 | Deli handling needs training: handwashing, gloves, sanitized scales and stations, accurate weighing, compliant labels. A deli label carries strain, batch, weight, THC/CBD, dates and the state warning. THC % also goes on the jar card. | P&P; FTTP outline | 2026-07 / 2026-10 | Current | High | GAME deli step |
| O8 | Receiving: each delivery is checked against the transfer manifest (amount, batch, strain), needs a COA, and is weighed into the POS. Any discrepancy means the product is quarantined. The regular deli shipment comes on Thursday. | P&P; tracker notes | 2026 | Current | High | GAME restock |
| O9 | Storage temperatures: room 68–82.4 °F, fridge 35.6–46.4 °F. Storage areas are labelled. | P&P | 2026-07 | Current | High | ART HUB signage |
| O10 | Waste: unusable product, including floor display product, is rendered unusable, bagged and tagged, and destroyed within 24 h. | P&P | 2026-07 | Current | High | GAME (optional) |
| O11 | Closing checklist: clean breakroom/bathroom; bring in cones; pull trash; put go-backs away; clear online orders after 9:30 pm; refill deli and exit bags; check receipt paper; clean the scale; wipe counters; sweep and mop last; manager signs. Closers also run a deli BOH audit and clean jars. | "Cleaning check list" mail; tracker notes | 2026-03 / 2026-10 | Current | High | GAME end-of-shift |
| O12 | Daily rhythm: 3 pm pre-shift huddle; sales checkpoints at 2 pm and 6 pm; rush at opening (a line has formed before 8 am) and in the evening (5–8 pm, online pickups peak then). | Pre-shift briefs; Sept wait-time report | 2026-09/10 | Current | Med-High | GAME traffic curve |
| O13 | Store aggregates: about 580–860 transactions a day (Fri/Sat highest, Sun/Mon lowest), average ticket about $27–34, about 2 units per sale. Median wait 1.4 min, average walk-in wait 3.7 min, median transaction 2.3 min. About 17 % of orders are online pickup. Average flower purchase is about 11 g. | Oct 2026 sales tracker; Sept 2026 wait-time report | 2026-09/10 | Current | High | GAME pacing |
| O14 | Systems: **Dutchie** is the POS and system of record. A LeafLogix daily inventory export includes a "Pricing Tier" column. The online menu and pay run on iHeartJane/JanePay. Loyalty runs on Alpine IQ. Payment is cash, PIN debit or ACH (Aeropay). | P&P; mails | 2026 | Current | High | UX register screens |
| O15 | Budtender title is "Wellness Expert". Training is the 5-day "FLOWERS" program: check-in, cart, discounts, payments, allotments, role-play, closing, certification. | Training PDFs (Mkt site Training Binder) | 2025-04 | Dated | High | GAME tutorial |
| O16 | The closing report has these sections: Income (Gross, Discounts, Returns, Net, Loyalty, Tax, Subtotal, **Rounding**, Total), Tax (Excise, Sales), Payments, Category, Customer (Rec/Med), Order type, Transactions, per-register. The Daily Tracker template has End-of-Day metrics, Discount Detail (override types) and opening/mid/closing manager notes. | Closing report PDF; Oct sales sheet | 2026-06/10 | Current | High | UX end-of-day screen |

## 4. Pricing, tax and deals

| # | Fact | Source | As of | Status | Conf | Affects |
|---|---|---|---|---|---|---|
| P1 | **Register rounding:** the Dutchie closing report has a Rounding line that is always negative, about $0.02 per sale (for example −$16.35 over 765 sales). **Nolan 2026-10-29: the register rounds to the nearest nickel.** This matches the JanePay mail ("nearest nickel", to match Dutchie). It differs from the tool's `priceFloor`, which floors. The always-negative Rounding line in the reports is not explained (it may come from how prices end). | Closing reports Apr–Jun 2026; "JanePay Rounding Update" 2026-06-23; Nolan | 2026-10 | Current | High (Nolan) | **GAP-204** |
| P2 | Tax is added at checkout and shelf prices are pre-tax. There are two lines, excise and sales tax. The budtender tool shows "25.1 % tax" combined. Medical and adult-use rates differ (applied by the POS). | Closing report; "Deli pricing + tax" 2026-10-26 | 2026-06/10 | Current | Med | GAP-204, Pricing |
| P3 | **FTTP V2 deli lanes (launched 2026-10-26 at Phoenix):** $2/g value lane (≤22 % THC, while it lasts, no substitution) · $3/g house smalls · $4/g house premium (house brands <30 % THC) · $5/g "Bring the Heat" (house ≥30 % THC). Ounces: $49.99 (value lane, Tue/Sat only), $56.99, $66.99, $89.99, flat. On Tue/Sat deal days the house lanes drop $1/g. Free grams: 9 g for the price of 7, 19 g for the price of 14 (no stacking). | FTTP Operational Outline, Scope & Strategy, one-sheet (mail "FTTP Program Q4 Launch Resources" 2026-10-15) | 2026-10 | Current | High | Pricing, DEC-020 |
| P4 | The live POS prices differ by a few cents from P3: house smalls oz $56.95, FTTP oz $49.95, premium 9 g $35 / 19 g $70. The final per-weekday price sheets are in a zip that was not read. | "Deli pricing + tax" screenshot 2026-10-26; "Deli Price Sheets - FTTPV2" 2026-10-23 | 2026-10 | Current | Med | Pricing |
| P5 | Third-party deli is still sold in **Tiers 1–5 at $6 / $8 / $12 / $15 / $18 per g**, on 1 / 3.5 / 7 / 14 / 28 g steps (for example Tier 1 $6/$18/$33/$50/$80). | Summer '26 price sheets; "Deli Sheets - UPDATE" 2026-09-11 | 2026-05/09 | Dated (tiers still on the Oct screenshot; exact steps may have changed) | Med | Pricing tiers |
| P6 | Pre-10/26 house deli: FTTP $2/g with a ⅛ oz minimum (oz $49.99), house fresh $3/g, TFS premium $4/g. | 2026-09-11 sheets | 2026-09 | **Superseded** by P3 | High | history |
| P7 | Deal sheets change every weekday and are organised brand-wide plus per category (flower, concentrates, edibles, vapes, prerolls). They **exclude deli**. Deal types: % off, BOGO, quantity tiers (2/3/5+), fixed bundles, gift with purchase at spend thresholds ($15/$20/$75/$100+), and manual coupons. A monthly EDLP list has a Phoenix-only version. | Pre-shift briefs 10/25–10/29; "November EDLP" | 2026-10 | Daily | High | GAME deals system |
| P8 | Seasonal promos are storewide % off (40–50 %) and exclude deli. "Night Splash" is a 10 % stackable discount that does not apply to merch. Employee discounts are not allowed on merch. | Pre-shift brief 10/29; merch mail 9/30 | 2026-09/10 | Daily | High | GAME events |
| P9 | The Q4 blended discount target is ≤40 %, moving toward 35 %. Unapproved register discounts must be logged. | FTTP Scope & Strategy | 2026-10 | Current | High | GAME score |

## 5. Products and assortment

| # | Fact | Source | As of | Status | Conf | Affects |
|---|---|---|---|---|---|---|
| A1 | **The store sells much more than deli flower.** The Dutchie categories are BEVERAGE, EDIBLE, EXTRACT, Flower, MERCH, PRE-PACK, PREROLL, TOPICAL, VAPE. Flower is about 70 % of net sales. Daily deals cover prepack flower, concentrates, edibles, vapes and prerolls. | Closing report 2026-06; pre-shift briefs 2026-10 | 2026-10 | Current | High | **conflicts with DEC-020** ("deli flower only") |
| A2 | The house brands are Deli Style, Dr. Greenthumb's, High Tide, High Variety, Rebel Grown, Shorties, TFS, The Flower Mine (the "TFM-" batch codes) and tōk. A master product list gives formats for each, for example DGT 3.5 g cans in three colourways, High Tide 10 mg seltzers, and High Variety/tōk Liquid Diamonds vapes. | Mkt site `…/TFS Brands - Branding/TFS Brands Product Master List/` | 2026 | Current | High (AZ-wide) | DEC-020 packaged lines |
| A3 | Third-party brands on Phoenix deal sheets in Oct 2026 include Alien Labs, Connected, Cookies, Grow Sciences, Fade Co., Presidential, Mohave, Clout King, MFused, Boutiq, Tropics, i.O. Extracts, STIIIZY, Jeeter, Abstrakt, Bud Bros, Baked Bros, Korova, Good Tide, Wana, Sluggers and ROVE. | Pre-shift briefs 10/25–10/29 | 2026-10 | Daily | High | data brands (trademark question open) |
| A4 | The deli jar card template has these fields: STRAIN NAME / THC 00.00 % / CLASSIFICATION (indica/sativa/hybrid) / TERPENES 0.0 % / terpenes 1–3. It prints two cards per page. Vendor variants say "DOMINANT TERPENES". | Mkt site `…/Standardized Deli Assets/Excel Deli Temp/TFS DELI TEMP.xlsx` | 2025 | Dated | High | GAP-PROC-03, UX jar card |
| A5 | New "Smalls" deli-jar logos (DGT, Rebel Grown, TFS) went to the floor on 2026-10-26. "Bring the Heat" jars use distinct coloured containers and shelving. | "Re: Smalls Deli Jar Logos" 2026-10-26; FTTP outline | 2026-10 | Current | Med | ART jars |
| A6 | Deli in-store marketing: TV slides show bold art and then the price tiers. The POS easel explains "smell, see, customize". There are deli stickers and bodega-style signs. | "TFS Deli Style MARKETING PLAN.pdf" | 2025 | Dated | High | ART signage |

## 6. Brand and visual identity (company-wide, Arizona)

| # | Fact | Source | As of | Status | Conf | Affects |
|---|---|---|---|---|---|---|
| V1 | Primary colours: Black #212322, Stone #B3A7A3, Beige #F2F1E6, White #FFFFFF. Secondary: Forest #324433, Grass #488D68, Lime #C6D6A6, Gold #E8BB49. | Mkt site `…/TFS Brands - Branding/The Flower Shop/Brand Sheet/TFSAZ - Brand Identity Sheet - 0526.pdf` | 2026-05 | Current | High | **GAP-114** (partial), UX tokens |
| V2 | Fonts (both free Google Fonts): Montserrat (Black/Bold) and Crimson Pro (ExtraBold/SemiBold/Regular), in two header/body pairings. | same | 2026-05 | Current | High | GAP-114, UX |
| V3 | SVG logos exist in Cream, Green, Black and White. | `…/The Flower Shop/Logos/SVG/` | 2026-05 | Current | High | ART signage (trademark call) |

## Not found
- Counter heights as text (GAP-108). They are on A901/A940; someone needs to read the sheets visually.
- Phoenix interior photos or renders, and photos of the restroom/JC/HUB (GAP-109/110 stay open).
- The opening checklist content, a scale model, a numeric tax rate, and a returns policy beyond "bought here, logged".
- Teams: the account is in no teams. Calendar was not needed.
