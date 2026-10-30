# SLICE DESIGN — M4 vertical slice (DES-001)

**Scope:** exactly what GAME-002 builds for DEC-008: one shift at one register. Customer → intent → recommend a real in-stock batch → sale → inventory and jar change → shift report. Anything not here is cut (§9).
**Labels:** **[SRC]** = source-derived (citation given); **[GDD]** = game-design decision (new mechanic; never present it as a tool feature). Every number lives in `SliceConfig` (§8). Code must not hard-code any of them.
**Engine authority:** MIG-001 slice subset (`Docs/Handoffs/MIG-001.md`), v7.11.4 line refs via `Docs/Reconstruction/RECONSTRUCTION_CONTRACT.md` (RC §n below).

---

## 1. Shift

| Rule | Value | Label |
|---|---|---|
| Customers per shift | 12, then the shift ends when the last one has left | [GDD] |
| Arrivals | Customer 1 spawns at t=0. Normal gap 45 s. Customers 6–9 are the **rush window**, gap 15 s | [GDD] (spec §6/§28 "one rush event", §87) |
| Shift day | `shiftDayOfWeek`, default Tuesday (2). Drives day deals | [GDD] value; deals [SRC] RC §12 `DEFAULT_DAY_DEALS` L21036 |
| Determinism | Seeded RNG (`seed`, default 1). Same seed → same customers, lines, budgets, weights | [GDD] (spec §82) |
| Win/fail | No game over. The report gives 1–3 stars from average satisfaction (§3.4). "Rough shift" flag if walkouts + no-sales ≥ 4 | [GDD] |
| Opening/closing phases | Cut. The shift starts with the store open and the player at the register | [GDD] |

**End-of-shift report fields** [GDD] (subset of spec §42–43; revenue is not the score):
`customersServed` (bought), `walkouts` (left from the queue), `noSales` (left after rejections), `revenuePostTax`, `revenuePreTax`, `gramsSold`, `avgServiceSeconds` (service start → sale/leave), `avgQueueWaitSeconds`, `avgSatisfaction` (0–100, all 12 customers; a walkout counts as 0), `avgRecFit` (0–1, sold items only), `interpretationAccuracy` (% where the player's chip = the customer's true family), `topIntents` (counts per family), `soldOut` (batches that hit 0 g), `lowStock` (batches below the low threshold), `stars`, `roughShift`.

## 2. Customer generator

### 2.1 Archetypes (3 of the spec's 6) [GDD] (spec §11)
| Archetype | Weight | Queue patience | Has budget | Line style |
|---|---|---|---|---|
| Novice | 30 | 150 s | no | long, hesitant opener |
| Regular | 45 | 90 s | no | short, direct |
| Price shopper | 25 | 120 s | yes (§2.4) | direct + budget clause |

Rush: patience × 0.75 for customers spawned in the rush window. Enthusiast, Decisive repeat (needs Similar) and Indecisive (needs Compare) are cut. Novice does **not** set the tool's new-customer profile (that is next-wave, MIG-001); it changes lines and patience only.

### 2.2 Intent families: six, each a verified golden parse [SRC]
The NPC carries a hidden **true family**. Its spec (crit/neg/primary) is the exact parse that the golden case shows, so the engine call is golden-checked end to end. The slice ships these in `SliceIntents.json`, not via the NL parser.

| Family | `lbl` (chip text) | crit | neg (cap) | primary | Source | Draw weight [GDD] |
|---|---|---|---|---|---|---|
| sleep | sleep | sedation 38 | — | sedation | RC-01, INTENTS L15620 | 20 |
| insomnia | insomnia | sedation 55, anxiety_relief 40 | — | sedation | RC-11, PHRASE_MAP L16107 (not the INTENTS key, which gives 45/35) | 10 |
| stress | stress relief | anxiety_relief 32 | — | anxiety_relief | RC-03, INTENTS | 15 |
| anxiety | anxiety relief | anxiety_relief 35 | — | anxiety_relief | RC-09, INTENTS | 15 |
| pain | pain relief | pain_inflammation 38 | sedation 55 | pain_inflammation | RC-04: INTENTS + pain-functional default L16211 | 20 |
| energy | energy | uplift 28 | sedation 36 | uplift | RC-10, INTENTS | 20 |

Draw weights are game tuning, **not** a claim about real store demand. GAME-002 test: each row equals `golden_cases.json` → `parsed` for its RC id.

### 2.3 Request weight [GDD]
From `STD_WEIGHTS` [SRC] L21010: 3.5 g (50), 7 g (30), 14 g (15), 28 g (5).

### 2.4 Budget (price shopper only) [GDD]
`budget = grams × budgetPerGram`, with `budgetPerGram` drawn from {4.00, 6.00} (equal odds), post-tax dollars, rounded down to $1. Example: 3.5 g at $4 → $14. Smalls 3.5 g is $13.10 post-tax at list price, or $8.75 on the Tue/Sat deal [SRC] (L21018, L21036, tax L21134). So low budgets are meetable while smalls are in stock (35 in-stock batches in the snapshot), though not always by the best-fitting strain. That trade-off is intended. Budget is **not** passed to the engine (no `maxPrice`): spotting it is the player's job, and scoring catches it (§3.3).

### 2.5 Product form
Deli flower only. Every in-stock catalog batch is treated as a deli jar [GDD; **Nolan to confirm**, see handoff]. No form constraint is generated.

### 2.6 Customer lines (templated, no NL parsing) [GDD on [SRC] wording]
`line = opener(archetype) + core(family) + weightClause(grams) + budgetClause?`
- **Core** uses the tool's own regression wording so a future parser reads it the same: sleep "something for sleep" (RC-01); insomnia "I've got insomnia" (L16107 phrase); stress "something for stress relief" (RC-03); anxiety "something for anxiety" (RC-09); pain "something for pain" (RC-04); energy "something for energy" (RC-10). 2–3 variants per family, all containing that keyword.
- **Openers:** Novice "Hi… I don't really know much about this stuff, but I'm looking for", "Um, hey. Not sure how this works. I want"; Regular "Hey, I'm looking for", "What do you have that's"; Price shopper "Hey, I'm looking for".
- **Weight:** 3.5 "an eighth", 7 "a quarter", 14 "a half", 28 "an ounce".
- **Budget:** "I've only got about ${budget}."
- **Rule:** a rendered line must contain no INTENTS key (L15619 table) other than its family keyword, and none of these words: night, relax, chill, work, drive, focus, first time, never tried, heavy. GAME-002 test renders every template × variant and checks it against the imported INTENTS key list.

## 3. Recommend interaction and scoring

### 3.1 Flow [GDD on [SRC] Floor-Mode principle, triage #50]
1. Customer reaches the service point and says the line (text bubble; voice cut).
2. Player opens the terminal and taps **one of six intent chips** (§2.2). This is the interpretation skill; no free-text search.
3. Engine: `FindStrains(spec(chip), n=3)` on live stock → `Ok`, `Fallback` ("No exact match… Closest available", [SRC] L16638) or `None` ("Nothing matched", [SRC]).
4. Up to 3 cards. Each shows: strain name, brand, tier label, **post-tax price for the requested weight**, grams left, cluster label (`classifyCluster`, [SRC] L15202). Role tags, terpene bars and detail view are cut (§9; display bars saturate at 99, GAP-208). Layout is UX-001's.
5. Player picks a card (or re-chips; no limit while the customer waits).
6. If the batch has < requested grams, the POS blocks it with "Not enough in the jar" [SRC hard rule spec §12]. The player must pick another card.
7. Customer responds (§3.5). On ACCEPT: POS confirm screen (weight, pre-tax, tax, post-tax) → **Confirm** → sale (§4). **Cancel** returns to the cards with no inventory change.

### 3.2 Recommendation fit (0–1) [GDD using [SRC] engine]
Computed against the customer's **true** family, not the chip:
```
strict = FindStrains(trueSpec, n=ALL)                // live stock
if chosen ∈ strict:              fit = clamp(ms_chosen / ms_top(strict), 0, 1)
elif chosen ∈ relaxed(trueSpec): fit = fitRelaxedFactor × clamp(ms_chosen / ms_top(relaxed), 0, 1)
else:                            fit = 0
```
`relaxed` = the one-shot relaxed pass (crit ×0.60 floored, caps +12; [SRC] L16639), run explicitly. If `ms_top ≤ 0`, fit = 1 for the top entry and 0 for the rest. The fit models the tool's matching heuristic, not a real effect (RC framing; spec §16).

### 3.3 Price fit and speed (0–1) [GDD]
```
priceFit = no budget ? 1 : price ≤ budget ? 1 : max(0, 1 − 2 × (price − budget) / budget)
speedFit = t ≤ fastSeconds ? 1 : max(0, 1 − (t − fastSeconds) / (slowSeconds − fastSeconds))   // t = service start → card pick
waitPenalty = min(waitPenaltyCap, waitPenaltyPerSec × max(0, queueWait − waitGraceSeconds))
```

### 3.4 Satisfaction (0–100) [GDD] (spec §15)
```
satisfaction = round(100 × clamp(wFit·fit + wPrice·priceFit + wSpeed·speedFit − waitPenalty, 0, 1))
stars = avgSatisfaction ≥ 80 ? 3 : ≥ 60 ? 2 : 1
```

### 3.5 Response (deterministic, for testability) [GDD] (spec §17/§36 subset)
- `satisfaction ≥ acceptThreshold` → **ACCEPT**.
- Else **REJECT** with a reason line: priceFit < 0.5 → "That's more than I wanted to spend."; else fit < 0.5 → "Hm, that's not really what I'm after."; else "I don't know… anything else?". The player may pick again.
- Rejections reaching `maxRejections` → **LEAVE** (no sale, `noSales` +1). The satisfaction recorded is the last computed.
- Cut: COMPARE, ASK_WHY, ASK_CHEAPER, ASK_STRONGER, ASK_LESS_SEDATING, ASK_SIMILAR.

## 4. Sale → inventory → visible change

| Rule | Value | Label |
|---|---|---|
| Stock authority | One `InventoryService` holds grams per batch. Engine stock, POS, jars and the report all read it | [SRC principle] spec §30; stock filter RC §8 |
| Starting grams | `startGramsPerBatch` = 28 g for every in-stock batch | [GDD] placeholder: the master JSON has `status` only, no quantities (DATA_SCHEMA §1). **Nolan to confirm or supply** |
| Which batch is sold | The card's representative batch `ids[0]`, the in-stock batch the engine shows | [SRC] L15464 |
| Event | `Sell(batchId, grams, pricePreTax, pricePostTax)`, emitted once on Confirm | [GDD] (spec §30 event list) |
| Price | `TIER_DEFAULTS` + day deal + tax 25.1 % floored to $0.05 | [SRC] RC §12, L21018/L21036/L21134 (GAP-204 floor kept) |
| Weighing | Assisted: the scale shows the exact target weight; no skill minigame | [GDD] (spec §21 "Assisted") |
| Payment | Abstracted: Confirm = paid. Cash drawer, change, card are cut | [GDD] (spec §24) |
| Reservation | None. Grams change only on Confirm; Cancel changes nothing (satisfies spec §88 "canceled transaction restores") | [GDD] |
| At 0 g | Batch status → OOS. The next `FindStrains` excludes it and re-averages its strain from the remaining in-stock batches | [SRC] `batchInStock` L15472, `averageProfile` L15483 |

**Visible changes** [GDD]:
- Jar fill level = grams / startGrams (linear; 0 = empty jar mesh).
- Below `lowStockFraction`: a "LOW" label on the jar. At 0: a "SOLD OUT" label.
- The customer leaves carrying a bag.
- The HUD money counter adds the post-tax price (HUD layout: UX-001).

## 5. Queue and patience [GDD] (spec §26–27, minimal)
- One lane of `queueSlots` = 4 slots, entry → slot 3…0 → service point → exit. Queue manager owns slots; customers never path to the counter themselves.
- A 5th arrival waits at the spawn point and counts as queued.
- Patience drains only while queued. At 0 the customer leaves (**walkout**, satisfaction 0). There is no drain during service; slowness hurts `speedFit` instead.
- Patience state `Calm` (>50 %), `Impatient` (≤50 %), `Leaving`. Shown through behavior/pose cues; whether there is also a HUD indicator is UX-001's call.

## 6. Needs from GAME-001 (engine, `Dispo.Domain`)
Names are proposals. GAME-001's `ENGINE.md` wins if it differs; GAME-002 adapts.
```csharp
// Intent spec (built from SliceIntents.json; GAME-002 owns that file)
public sealed class IntentSpec { IReadOnlyDictionary<string,int> Crit; IReadOnlyDictionary<string,int> Neg; string Primary; string Label; }

// Live stock: the engine must not cache in-stock status
public interface IStockView { bool InStock(string batchId); }

public enum RankKind { Ok, Fallback, None }
public sealed class RankedStrain {
  string GroupKey; string DisplayName; string RepBatchId;  // rep = ids[0], L15464
  double Ms;                                              // ranking score, L15355-15427
  int ClusterId; string ClusterLabel; int AnxietyRisk; string Tier; string Brand;
}
public sealed class RankResult { RankKind Kind; IReadOnlyList<RankedStrain> Items; }

// findStrains + the one retry. relaxedOnly=true runs only the relaxed pass (needed for §3.2)
RankResult FindStrains(IntentSpec spec, IStockView stock, int n, bool relaxedOnly = false);

// Pricing
public readonly struct PriceQuote { decimal PreTax; decimal PostTax; }
bool TryQuote(string batchId, double grams, DayOfWeek day, out PriceQuote q);   // false = no price (empty tier)

// Catalog
IReadOnlyList<Batch> Batches;   // Id, StrainName, BatchCode, Brand, Tier, InStock (snapshot), TestDate
IReadOnlyCollection<string> IntentKeys;   // INTENTS key list, for the line-safety test (§2.6)
```
Hard requirements: `FindStrains` with `n=int.MaxValue` returns every passing group (for §3.2), and results are deterministic for a given stock state.

## 7. Needs from ART-001 (graybox anchors)
Named empty GameObjects (or data points) in the Retail scene. Positions in the REF-001 frame; ART-001 picks exact spots.
| Anchor | Where (REF-001 §1.5) |
|---|---|
| `Anchor_CustomerSpawn` | inside the entry doors |
| `Anchor_QueueSlot_0..3` | along one stanchion lane (x≈6–15, y≈11–19.5) |
| `Anchor_ServiceCustomer` | customer side of one station on the register run's north leg (x 20–42, y≈7–8) |
| `Anchor_ServicePlayer` | budtender side of the same station |
| `Interact_Terminal` | POS monitor at that station |
| `Interact_Scale` | scale at that station |
| `Anchor_JarSlot_000..N` | north deli flower jar wall (x 19–45, y 0.2–1.4), overflow onto the east jar wall (x 45.6–47). N ≥ in-stock batch count (77 in the current snapshot) |
| `Anchor_CustomerExit` | the exit side of the entry doors |
The register-run station is a [GDD] layout choice: which counter really weighs deli flower is not recorded (GAP-107; **Nolan to confirm**). The slice needs **1** station only.

## 8. SliceConfig: every constant
| Key | Value | Label |
|---|---|---|
| `customersPerShift` | 12 | GDD |
| `arrivalGapNormalSec` / `arrivalGapRushSec` | 45 / 15 | GDD |
| `rushFirstIndex` / `rushLastIndex` | 6 / 9 (1-based) | GDD |
| `shiftDayOfWeek` | 2 (Tue) | GDD |
| `seed` | 1 | GDD |
| archetype weights N/R/P | 30 / 45 / 25 | GDD |
| patience N/R/P (s) | 150 / 90 / 120 | GDD |
| `rushPatienceMult` | 0.75 | GDD |
| family weights sleep/insomnia/stress/anxiety/pain/energy | 20/10/15/15/20/20 | GDD |
| weight odds 3.5/7/14/28 g | 50/30/15/5 | GDD (weights SRC L21010) |
| `budgetPerGram` options | {4.00, 6.00} | GDD |
| `resultCount` | 3 | SRC `_prefs.resultCount` L17517 |
| `fitRelaxedFactor` | 0.5 | GDD |
| `fastSeconds` / `slowSeconds` | 30 / 120 | GDD |
| `waitGraceSeconds` / `waitPenaltyPerSec` / `waitPenaltyCap` | 60 / 0.002 / 0.30 | GDD |
| `wFit` / `wPrice` / `wSpeed` | 0.60 / 0.25 / 0.15 | GDD |
| `acceptThreshold` | 50 | GDD |
| `maxRejections` | 2 | GDD |
| star cutoffs | 80 / 60 | GDD |
| `roughShiftThreshold` | 4 (walkouts + noSales) | GDD |
| `queueSlots` | 4 | GDD |
| `startGramsPerBatch` | 28 | GDD placeholder (no source quantity) |
| `lowStockFraction` | 0.25 | GDD |
| tax / rounding | 25.1 % / floor $0.05 | SRC L21062, L21123 |

Sanity check (seed-independent): an exact top-card pick for a no-budget customer within 30 s and a 0 s wait gives 0.60 + 0.25 + 0.15 = 1.00 → 100. A wrong-family pick with fit 0 at full price/speed fit gives 40 → REJECT. Fit alone at 0.2 with perfect price and speed gives 52 → ACCEPT (lenient by design for the slice; tune later).

## 9. Cut from the slice
NL free-text search and parser (chips instead); negations, exclusions/allergies, compare, like-X, Similar, strain lookup, terpene rank; new-customer profile; tier chips and `maxPrice` engine filter; role tags, card scripts, detail view and domain bars; "show more options"; refine chips; feedback aggregation; packaged products and other forms; weighing skill modes; payment methods, cash drawer and receipts; restock, deliveries, BOH/FOH transfer, waste, cleaning; opening/closing phases; multiple registers and AI staff; traffic director; second rush/events; repeat customers; voice/audio barks; save/load; tutorial; progression and difficulty; drive notice; display-saturation fix (GAP-208).
