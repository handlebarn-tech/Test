# Budtender engine reconstruction contract (MIG-001)

**Source of truth:** `C:/Users/handl/Downloads/tfs-budtender/deploy/2026-10-30-v7114/site/index.html`, v7.11.4, md5 `228684e9f02d703cf3a36692baf10d18` (DEC-001/002). All `L#####` references are 1-based lines in that file. Inventory: `inventory/tfs-inventory-master.json` md5 `09bfa4f00206b25f77fb2a49db2eea9c` (export `2026-10-29T19:13:36.534Z`).

**Status tags:** **OBS** = observed in source; **OBS+RUN** = observed and executed headlessly (see `GOLDEN_CASES.md`); **DOC** = only in docs (HUB/TRACKER/references), not in code; **UNK** = unknown; **DEAD** = defined in source, never called.

**Framing (OBS, About page L2066-2110; HUB "Current architecture"):** a terpene-profile *matching heuristic*, "not a pharmacological model". Accuracy has never been measured (HUB Known bugs; TRACKER SCI-8). The game keeps that framing.

---

## 0. Pipeline in one paragraph

`submit(q)` (L19542) → `parseQuery` (L16013) pulls out hard terpene exclusions, then `_parseQueryCore` (L16024) strips budtender framing words and product formats. It then routes the query to **compare** (two or more strain names plus "compare"/"vs"), **like-X-but-Y**, **strain lookup**, **terpene_rank** ("most X") or **recommend**. For recommend, it builds `crit` (domain minimums), `neg` (domain caps), a `primary` domain and labels from negation patterns, `PHRASE_MAP`, the 287-key `INTENTS` table, conflict resolution and the pain-functional default, with a fuzzy fallback last. `detectPriceIntent` adds a budget. `respond` (L16539) calls `findStrains` (L15355). `findStrains` groups batches by normalized strain name and averages **in-stock** batches with an 8-week half-life recency weight. It scores six domains per group (concentration tier × dominant bonus × BA scalar / NF). It filters by stock, tier chips, exclusions, crit/neg on the integer scores, max anxiety and max price. It ranks on the continuous score (primary ×1.5) minus a neg-headroom penalty, plus the cluster bonus, the brand-tier nudge, the like-X cosine and the new-customer myrcene penalty, and returns the top N (default 3). If nothing passes, it reruns once with crit ×0.60 and caps +12. Role tags (L16264) label cards 2..n relative to card 1.

---

## 1. Data inputs the engine reads

| Input | Where | Status |
|---|---|---|
| Batch record `{name,batch,total,p{terpId:%},tier,status,brand,date?,thc?,labAromas?}` | `STRAINS` map, loaded via `_sanitizeImport` L19718 (drops non-finite, negative or ≥50 values; keeps tested-ND zeros; recomputes `total` if missing) | OBS+RUN |
| Terpene DB: 60 terpenes, each `{name,cls:'mono'|'sesqui',chem[],d{6 domains},ev,notes,aliases[]}` | `DB` L15044-15105. `beta_eudesmol` has all-zero weights | OBS+RUN |
| Batch date | `s.date` (COA test date) or, when missing, inferred from the batch code by `parseBatchDate` L20514 (MMDDYY suffix, else embedded YYMMDD, years 24-30) via `_backfillDates` L17674, in memory only | OBS+RUN |
| Stock | `batchInStock(s)` L15472 = `s.status!=='oos'`. On the live cloud build the status comes from per-store `location_stock` (HUB architecture), not from the master JSON | OBS (cloud source DOC) |
| Pricing settings | `_pricing` L21061 (`taxRate 25.1`, tiers, dayDeals, strainOverrides, customDeals). Live has 0 saved pricing rows, so defaults apply (dev/v7115/price-changes.md) | OBS |
| Prefs | `_prefs` L17517: `resultCount 3`, `painFunctional true`, `floorMode false`, `showBars`, `showTerps`, `hideOos` | OBS |
| Session state | `_customerProfile` (`null`/`'new'`/`'exp'`) L14808; `_activeTiers` (tier chips) L18594 | OBS |

## 2. Intent parsing / NL search (OBS+RUN)

Order inside `_parseQueryCore` L16024-16246:

1. **Normalize** L16030-16038: `w/o`→`without`, `couchlock`→`couch lock`. Strip framing (`customer|patient|he|she|they…`, `wants|needs|looking for…`, `something|weed|flower…`) and product formats (`pre-rolls|carts|vapes|edibles|eighths|oz|grams…`). "a/some joint(s)" is stripped unless followed by pain words. Intent matching uses the stripped text `qi`; names and terpenes use the raw `ql`.
2. **Strain mentions** `_findStrainMentions` L15916: whole-word, longest name first, names ≥3 chars. Typo fallback `_fuzzyStrainMentions` L15933: Levenshtein ≤1 for 5-7-letter names and ≤2 for ≥8, names under 5 letters exact only, spaces ignored, unique closest only, up to 3 rounds.
3. **Compare** L16043-16046: `compare | vs | versus | difference between | which is better` with ≥2 mentions → `{intent:'compare', strains[≤3]}`.
4. **Like X but Y** L16048-16051: mention + `like|similar to` + `but|more|less|except|without` → parse Y without names, then `opts.exclude=[X]`, `opts.likeKey=X`.
5. **Strain lookup** L16054: any mention → `{intent:'strain', groupKey}` (first mention).
6. **Terpene rank** L16058-16061: `highest|most|which…most|top…for|which has` + a terpene alias (`_findTerpMention` L15958; longest alias wins; extra aliases `pinene→alpha_pinene`, `bcp`, `lavender→linalool` L15956).
7. **Negation patterns** L16066-16093 (10 regexes). Sedation caps: 42 (without/no…sleep, sedation, couch lock…), 42 (stay functional/awake), 38 (have to work/drive/focus; skipped when the query is a sleep ask, `_sleepAsk` L16086), 38 (need to drive / driving after, raw text), 50 (without getting too heavy / not too heavy). Anxiety: positive crit 50 and 55 ("won't make me paranoid"). Uplift cap 55 ("not too racy/wired…").
8. **PHRASE_MAP** L16098-16158: 54 regex phrases; a matched span is blanked so its words do not fire again (L16165-16172).
9. **INTENTS keyword table** L15619-15883: **287 keys**, scanned longest first, whole-word with an optional `s|es` plural (`_kwRe` L15891, `_consumeKw` L15900; a consumed span is blanked). Each `{d:{dom:min}, neg:{dom:max}, lbl, pri}`. Merge rule: crit = max, neg = min, and `primary` = the `pri` of the entry with the highest primary threshold. The About page says "281 search patterns understood" (L2066, static text).
10. **Conflict resolution** L16195-16210: when a domain is both crit and neg, the pair is kept if `neg > crit+5`. Otherwise an explicit negation hint wins (crit dropped) or the positive request wins (cap dropped). The primary is re-picked if dropped.
11. **Pain functional default** L16211-16216: if `crit.pain_inflammation` is set, no sedation cap, `crit.sedation<45`, `painFunctional` is on and no "heavy/sleep/night…" word appears → `neg.sedation=55`.
12. `tf` (terpene sort) = any terpene mention. When `tf` is set, results are re-sorted by that terpene's % (L16637).
13. **Fuzzy fallback** L16226-16245: 8 broad regexes (indica→sed35/anx30, sativa→up30, hybrid→anx35/up25, hurt→pain45, stress→anx40, tired→sed40, focus→foc20, happy→up28/anx25). The first match only. Else `{intent:'unknown'}` → help text.

**Exclusions** `_extractExclusions` L15979: `without|no|not|zero|avoid|free of|allergic to <terp>[, / & and or nor <terp>]` and `<terp>-free`. Families `pinene(s)→alpha+beta`, `terpinene→alpha+gamma`, `nerolidol→nerolidol+trans_nerolidol` (L15976). `exclStatus` L16001: over in-stock batches, `contains` if any value ≥ `EXCL_MAX_PCT=0.01` (L15975). A missing value is **unknown** and is excluded too ("ND" text or 0 = absent). If no strain is verified clear, the tool says so and shows nothing (`exclNote` L16524).

**Price intent** `detectPriceIntent` L21744 over `PRICE_INTENTS` L21696: `noPrice` (8 regexes) > `hasBudget` (19 regexes; the last integer in the match, 0 < amount < 10000) > `budget` (12 regexes). `hasBudget` sets `opts.maxPrice`, but only when pricing is configured (L16632). It filters out strains whose cheapest post-tax weight exceeds the budget + $0.01 (L15374).

**Drive notice** (L19545, L19557): any `drive/driving/drove` prepends "Cannabis and driving don't mix." This is a separate rule from the sedation cap.

## 3. Effect-domain scoring (OBS+RUN)

Domains (`DOMS` L15042): `sedation, uplift, anxiety_relief, pain_inflammation, focus_cognitive, antimicrobial`. The About page names (Euphoria/Uplift, Calm/Sedation, **Energy**, …, L2108) are static marketing text. There is **no Energy domain in code**, and antimicrobial is scored but never shown or queried.

Concentration tier `getTierW(p)` L15041: `p≥0.20 → 1.00` (dominant), `≥0.05 → 0.25` (active), `≥0.01 → 0.02` (subthreshold), else 0. Labels from `getTier` L15040.

`scoreDomains(p)` L15169-15201, per domain `d`:

```
r_d = Σ_terp  DB[t].d[d] × getTierW(pct) × b(pct) × getBaScalar(t)
b(pct) = pct≥0.20 ? 1 + min(1.0, (pct−0.20)/0.60) : 1        // dominant bonus, 2× at ≥0.80%
display_d = clamp( round(r_d / NF × 100), 2, 99 ),  NF = 2.7765  (L15121)
```

`scoreRaw` L15338-15353 is the same sum without rounding or clamping (`r_d/NF`). It is used for ranking. Terpene ids not in `DB` contribute nothing.

Observed consequence (RUN): in-stock strains commonly hit the 99 display ceiling on anxiety_relief and pain_inflammation (`golden_cases.json`). Integer filters are easy to pass, and ranking separates strains only by the raw floats.

## 4. Bioavailability (BA) correction (OBS+RUN)

`BA_SCALARS` L15127-15137: `alpha_pinene .60, beta_pinene .50, beta_myrcene .62, dl_limonene .58, linalool .55, terpinolene .55, trans_beta_ocimene .55, camphene .58, dl_borneol .55, geraniol .52, beta_caryophyllene .48, alpha_humulene .48, alpha_bisabolol .46, nerolidol .44, trans_nerolidol .44, guaiol .44, beta_farnesene .44, valencene .45`. Default `getBaScalar` L15138: `sesqui .46`, otherwise `.55`, and `.55` for unknown ids. The value multiplies the contribution, not the concentration. The terpinolene `.55` is a floor over a 0.18 vapor-survival figure: a "business choice" (TRACKER SCI-7d; v7.11.5 changes only the note text).

## 5. Synergy / multi-terpene interaction

- **No pairwise synergy term exists in scoring** (OBS: `scoreDomains` is a pure per-terpene sum). The "synergy" pairings appear only as Learn-tab educational HTML (e.g. L3742, L4058), which ranking does not read.
- Multi-terpene logic that does exist: **clusters** `CL` L15107-15115 + `classifyCluster` L15202-15271, and **CLUSTER_BONUS** L15327-15333 (OBS+RUN).
  - Cluster tests: 1 myrcene ≥.50; 2 BCP ≥.20 & humulene ≥.08; 3 BCP ≥.20 & limonene ≥.20; 4 α-pinene ≥.20 or α+β pinene ≥.35; 5 ocimene ≥.30, or terpinolene ≥.15 and ≥ the 2nd-largest terpene; 6 linalool ≥.20; 7 none (fallback).
  - Priority order `[4,5,6,2,3,1]`. Tiebreakers: drop 4 if myr ≥.80 & myr > 3×α-pin, or if α-pin <.20 & myr > 3×α-pin & myr ≥.50. Drop 5 if myr ≥.80 & myr > 2×max(ocim,terp). Drop 6 if myr ≥.80 & myr > 4.5×lin. BCP solo: BCP ≥.50 & hum <.08 forces 2 to the front. No match → 1 if myr ≥.20, else 7.
  - Bonus added to `ms` only for domains present in `crit`: `4:{focus .15, uplift .08}`, `5:{uplift .35, focus .20}`, `6:{anxiety .12, sedation .08}`, `2:{pain .12, anxiety .06}`, `1:{sedation .10, pain .06}` (no bonus for clusters 3 and 7).
- The historical "111-terpene DB" and "large interaction dataset" (UNITY_MIGRATION_PLAN §7) are **DOC**. The code has 60 DB entries. The Learn tab holds about 90 monographs (feature map), which are educational only.

## 6. Anxiety risk (OBS+RUN)

`calcAnxietyRisk` L15288-15315: start 50. Subtract `min(30,lin×80)`, `min(25,bcp×30)`, `min(12,apin×60)`, `min(10,bisa×70)`, `min(10,myr×8)`. Add `max(0,min(20, lim×12 − max(0,lin−0.10)×40))`, `min(18,terp×30)`, `min(14,ocim×25)`. Round, then clamp to 15..88. Labels `_anxLevel` L16377: <38 low, <55 moderate, else high. Used by the new-customer filter (≤60), the `lowerAnx` refine (`maxAnx 42`) and role tags.

## 7. Batch freshness / current-batch preference (OBS+RUN)

- **Profile = in-stock batches only** (`profileIds` L15475). OOS history is used only when every batch is OOS, and such a strain is never recommended.
- **Recency weighting** `averageProfile` L15483-15514: `w = exp(−ln2/8 × min(20, weeksOlderThanNewestDatedBatch))`, i.e. an 8-week half-life capped at 20 weeks (floor ≈0.177). An undated batch takes the oldest dated batch's weight. With no dates at all, weights are equal. Weights are normalized, each terpene is averaged, rounded to 6 dp, and zeros are dropped.
- **Freshness decay is NOT in scoring.** `FRESHNESS_CAP_WEEKS 20`, `DECAY_K {fast .015, medium .006, slow .003}`, `DECAY_TIER_MAP` (L15152-15161): `getFreshnessScalar` L15162 is **DEAD** (never called). `analyzeGroup` L15516 computes the mean `weeksOld` (from `Date.now()`) for the age badge only. `ASSUMED_AGE_WEEKS=0` (L15529).
- Group key `normName` L15434 (lowercase, non-alphanumerics → space). The group's representative `ids[0]` is an in-stock batch when one exists (L15464-15466).

## 8. Stock filtering (OBS+RUN)

Hard rule: `findStrains` L15362 drops groups whose representative is OOS. Terpene rank (L16579) and Similar (L20856) do the same. A strain lookup of an OOS strain shows it, then "In stock and close to it" (top N by cosine, L16551-16554).

Tier chips (L15363-15366): when any are on, a group passes only if `rep.tier||'house'` is selected. An empty tier counts as House Fresh: **defect V73-NT5**, fixed in the unreleased v7.11.5.

## 9. Ranking in `findStrains` (OBS+RUN) L15355-15427

Filters, in order: in stock → tier chip → exclusions → every `crit` met on display ints → every `neg` respected on display ints → `maxAnx` → `opts.exclude` → `maxPrice`. Score:

```
ms = Σ_{d∈crit} raw_d × (d==primary ? 1.5 : 1.0)        // if primary ∈ {sedation, pain_inflammation}: only the primary term counts
   − Σ_{d∈neg} (display_d / cap_d) × 0.25                 // when both > 0
   + Σ_{d∈crit} CLUSTER_BONUS[cluster.primary][d]
   + tierNudge[rep.tier]   // smalls .18, house .18, premium .18, fttp .16, t1 .08, t2 .04, t3 .01, t4 0; no tier → 0 (L15408-15412)
   + (likeKey ? cosine(avgProfile(X), p) : 0)
   − (profile=='new' ? (myr≥1.20 ? .45 : myr≥.80 ? .22 : 0) : 0)
```

After that: `applyProfileFilter` L14827 (profile `'new'` drops `anxietyRisk>60`; `'exp'` does nothing), sort by `ms` descending, slice n. `applyProfileSort` L14834 is **DEAD**.

**Fallback** (`respond` L16638-16646): if empty, run once more with `crit_d = floor(crit_d×0.60)` and `neg_d = min(99, neg_d+12)` → "No exact match for … Closest available". If that is still empty → "Nothing matched" with retry chips. "Show more options" (L19442) reruns with n=40 and appends the next 3 unseen.

**Refine chips** `REFINE` L19583-19595: they edit the previous crit/neg numbers directly (e.g. lighter: drop sedation crit, cap 40; heavier: sedation ≥50; lowerAnx: `maxAnx 42`). They then re-apply the `neg ≤ crit+5 → drop crit` rule (L19601).

**Role tags** `buildRoleTags` L16264-16332: card 1 = Best match. Each later card gets the first unused role from: (1) the largest domain delta >4 vs card 1 → Heaviest body / More uplifting / Strongest pain relief / Most focus; (2) sedation 5+ lower → Most functional; (3) anxiety risk 6+ lower → Lowest anxiety; (4) primary tie (<5) → largest positive secondary delta >4; (5) the lowest anxiety in the set → Lowest anxiety; else Mildest option.

**Card copy:** `buildScript` L15561 (per-cluster text + secondary line + "Low total terpenes" when `total<0.50`). The anxiety label and chips are in `renderStrain` L16382.

## 10. Similarity (OBS+RUN)

`slCosineSim` L20813: cosine over the union of terpene keys of two %-profiles (0 if either is empty). Similar tab `slRunEngine` L20824: blended liked profile = plain mean of the liked strains' `averageProfile`. Candidates = in-stock, not liked, `sim>0`, top 6. Also used by the like-X bonus (L15413) and by "close to it" (L16552).

## 11. Comparison (OBS+RUN)

`respond` compare L16555-16564: 2-3 groups. Key difference = the non-antimicrobial domain with the largest max−min display gap. Winner = the highest on that domain. "notably" when the gap is ≥10. Each card also lists cluster label and anxiety risk.

## 12. Pricing (OBS+RUN) L21008-21255

- Weights `STD_WEIGHTS [3.5,7,14,28]` L21010. Tiers `ALL_TIERS` L21013 + labels L21014.
- `TIER_DEFAULTS` L21018-21027 (pre-tax, 3.5/7/14/28): smalls 10.50/21/42/56.99 ($3/g); house 14/28/56/66.99 ($4); premium 17.50/35/70/89.99 ($5); fttp 7/14/28/56.99 ($2); t1 18/33/50/80 ($6); t2 24/43/75/140 ($8); t3 36/64/116/200 ($12); t4 47/86/154/308 ($15). (v7.11.5 unreleased: t2 14 g → $77.)
- `DEFAULT_DAY_DEALS` L21036-21059: Sun none. Mon t3 3.5 g flat $19.99. Tue and Sat: smalls 7/14/28/49.99, house 10.50/21/42/56.99, premium 14/28/56/66.99, t1 14/28/40/65, fttp oz 49.99. Wed and Thu: t2 17.50/35/60/110. Fri: t3 21/42/84/160, t4 30/70/140/280.
- Resolution `getEffectivePrices` L21172-21243. A strain override (by name, case-insensitive) wins. Then brand `pricingClass` (`house` → house unless the tier is smalls/premium; `fttp` → fttp; default `tier`). Otherwise the batch tier; an empty tier has no price. Base = the tier's MSRP. The **first** active matching deal (day list, then custom deals) wins: `weight_table` (merge), `weight_flat` (one weight), `pct_msrp` (with `excludeWeights`, `ozOverride`, `baseTier`), `use_tier`. Deal targets: `tier`, `multiTier`, `pricingClass`, `brand`.
- Tax `applyTax` L21134: `priceFloor(pre × (1 + 25.1/100))`. `priceFloor` L21123 = **floor** to $0.05 after a 4-dp round (e.g. 10.50 → $13.10). Whether it should round instead is open with Nolan (HUB "Price rounding").
- `isFirstWeekdayOfMonth` L21165 is **DEAD**. The master JSON brands carry no `pricingClass`, so every snapshot strain resolves through its batch tier.

## 13. Floor Mode (OBS)

`applyFloorMode` L17575 toggles `body.floor-mode`. CSS L169-175 hides `.rdesc` (role sentence), `.adv-chip:not(.no-hide)`, `.rcard-detail`, `.expand-btn`, `.rcard-advisory-row` and `.pin-btn`. Pure presentation: ranking is identical.

## 14. Feedback / Sold / search log (OBS)

- `fbAdd` L22644: `{strain_key, batch_id, batch_code, result ∈ matched|poor|uncertain, source ∈ customer|staff, effect?, sold, employee_id, location_id, voided, corrected_*}`. Duplicate = same employee + batch + source within 10 min (`FB_DUP_MS` L22615). Confidence by decisive count (matched + poor): <5 too few, <15 low, <30 medium, else higher (`_fbConf` L22632). Only Owner/Admin can correct (`fbCorrect` L22657). **Never used in ranking** (HUB architecture).
- `markSold` L22082 toggles a key on the search-log entry. `_logSearch` L22066 stores q (≤160 chars), intent, labels, shown keys, fallback/none flags, profile, staff/uid. Cap `USAGE_CAP` L22025.

## 15. Unknown / not in source

- Real-world effect validity of any coefficient: **UNK** (never measured; SCI-8).
- Live per-store stock at any moment: **UNK** to us (Supabase, read-only; the master `status` is one snapshot).
- Pairwise synergy coefficients: **UNK / not implemented**.
- The derivation of individual DB domain weights beyond their `notes` strings: **DOC** at best.
- Learned or outcome-weighted ranking (v7.1.0 history): removed. **DOC** only.
