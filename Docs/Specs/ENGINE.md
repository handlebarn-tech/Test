# ENGINE: recommendation engine API (GAME-001, GAME-003)

> **Pinned sources (AUDIT-001 E5, DEC-064):** the source hashes and counts below are as of the import pinned in `Docs/Reconstruction/DATA_SCHEMA.md` ("Pinned sources" block above §1). That block is the one place to update them; on a re-import (DEC-014/038) update it first, then regenerate the goldens.

Pure C# port of the TFS budtender v7.11.4 recommendation engine (GAME-001 slice; GAME-003 parser + remaining KEEP features) (MIG-001 "Recommended vertical-slice subset", DEC-001/002). Assembly `Dispo.Domain` (`noEngineReferences`), namespace `Dispo.Domain.Engine`, folder `UnityProject/Assets/_Game/Code/Domain/Engine/`. Every function cites its v7.11.4 source function and line.

## Data (generated, do not hand-edit)
`UnityProject/Assets/_Game/Data/Catalog/`, written by `node Tools/Data/import_catalog.js` (deterministic; `--check` re-runs the PII allow-list).

| File | Content |
|---|---|
| `batches.json` | 1207 batches: `id, strainName, batchCode, brand, tier, inStock, testDate, dateInferred, total, terpenes{id:pct}` (tested-ND zeros kept) |
| `terpenes.json` | 6 domain ids, 60 terpenes `{id,name,cls,d{6},aliases[]}`, `baScalars` |
| `parser_tables.json` | the tool's regex source text: `negPatterns` (10), `phraseMap` (46), `fuzzy` (8), `priceIntents` {noPrice, hasBudget, budget} (importer 1.1.0, pinned line ranges) |
| `engine_tables.json` | `intents` (287 keys `{d,neg,lbl,pri}`), `clusterBonus`, `tierNudge` |
| `pricing.json` | `taxRate` 25.1, `weights` [3.5,7,14,28], `tiers` (TIER_DEFAULTS), `dayDeals` by dow 0-6 |
| `manifest.json` | importer version, source md5s, output md5s, counts |

The snapshot is a fixture: stock is the master file's `status` at export 2026-10-29 (GAP-202). Re-import ⇒ regenerate goldens.

## Loading
```csharp
using Dispo.Domain.Engine;
Catalog cat = Catalog.Load(batchesJson, terpenesJson, tablesJson, pricingJson, parserJson); // strings; the caller does file IO
// parserJson is optional: without it the slice API works, QueryParser throws
```
`Catalog`: `Batches` (file order), `Terpenes` (id → `Terpene{Id,Name,Cls,D}`), `BaScalars`, `Intents`, `ClusterBonus`, `TierNudge`, `Pricing`, and `Groups()` (strain groups by `Catalog.NormName`, in-stock batches first, cached).

## Intent (the NPC emits an `INTENTS` key)
```csharp
IntentQuery q = Intents.Resolve(cat, "sleep");            // null when the key is unknown
// q.Crit {domain:min}, q.Neg {domain:max}, q.Primary, q.Label
```
Applies the parser's conflict rule (L16200) and the pain-functional default (L16211: pain crit, no sedation cap ⇒ `neg.sedation=55`, unless the key itself is a heavy/sleep word). Keys that match the full parser's result: `sleep`, `anxiety`, `pain`, `energy`, `sinking`. Multi-word phrases (`stress relief`, `insomnia` via PHRASE_MAP) need `QueryParser` (below) or explicit `Crit/Neg/Primary`.

## Recommend
```csharp
var state = new ShopState { ResultCount = 3, ActiveTiers = { "t3" }, NewCustomer = false, EmptyTierCountsAsHouse = true };
RecommendResult r = Recommender.Recommend(cat, q.Crit, q.Neg, q.Primary, state);
// r.Outcome: Ok | Fallback | None ; r.Strains: List<StrainResult> (best first)
// r.Calls: every FindStrains call made (1 or 2), with the crit/neg used
```
`StrainResult`: `Key` (normName), `Name`, `Ms` (rank score), `Tier`, `Cluster`/`Cluster2`, `AnxietyRisk` (15-88), `Domains` (display 2-99), `Raw` (unclamped), `Profile` (averaged %), `BatchCount`, `InStock`.

- `Recommender.FindStrains(cat, crit, neg, primary, state)` = `findStrains` L15355: in-stock → tier chips → crit/neg on display ints → new-customer anxiety ≤60 → `ms` → stable sort, top N.
- `Recommend` = `respond` L16637-16646: one retry with crit×0.60 (floored), caps +12 (max 99).
- `FindStrains/Recommend(..., FindOptions opts[, tf])`: `Excl`, `MaxAnx`, `Exclude`, `LikeKey` (cosine bonus), `MaxPrice` + `Dow`. The old signatures still work (opts = null).

## Natural-language queries (GAME-003)
```csharp
QueryResponse r = Responder.Ask(cat, "something like Kush Cake but more uplifting", state, dow);           // v7.11.4 parser
QueryResponse g = Responder.Ask(cat, "something for the day", state, dow, ParserOptions.Game);            // MC-7 + GAP-206 fixed
```
- `QueryParser.Parse(cat, q, opts)` → `ParsedQuery`: `Intent` (Recommend / Compare / Strain / TerpeneRank / Unknown), `Crit`, `Neg`, `Primary`, `Lbls`, `Tf`, `GroupKey`, `Strains`, `Terpene`, `Excl`, `Opts`, `PriceIntent` {NoPrice, HasBudget+Amount, Budget}, `Drive`. Order as `parseQuery` L16013 / `_parseQueryCore` L16024: exclusions → framing strip → compare → like-X → strain lookup (exact, then Levenshtein) → terpene rank → negation patterns → PHRASE_MAP (span blanked) → INTENTS longest-first (`_consumeKw`) → conflict rule → pain-functional default → fuzzy fallback.
- `Responder.Respond(cat, parsed, state, dow)` = `respond` L16539 without HTML. `QueryResponse`: `Kind`, `Outcome` (Ok / Fallback / None / ExcludedAll / Help / NotFound), `DriveNotice`, `ExclNote` (counts + `Head` text), recommend `Strains` + `RoleTags` (also filled on fallback; the tool shows tags only on Ok), `AskEffectForBudget`, strain `Card` + `CardExcl`/`CardExclNote` + `Near` (OOS → in stock and close to it, `Ms` = cosine), `Compare` (`KeyLabel`, `Diff`, `Winner`, `Line`), `TerpRank` rows, `LowestPrices` (price-only "cheap"). It writes the effective opts back to `parsed.Opts`, like the tool.
- `Responder.MoreOptions` (L19442), `Refine.Apply(parsed, key)` (REFINE L19583: lighter, heavier, addPain, addSleep, lowerAnx, moreEnergy, functional, moreBody, addFocus, moreUplift, addAnx), `RoleTags.Build` (L16264), `Similarity.Cosine` / `Similarity.Similar` (Similar tab L20824, top 6), `Exclusions.Status` / `Note` (L16001, L16524).
- Regexes run with `RegexOptions.ECMAScript` so `\b`, `\w`, `\d` keep JS meaning.

## Scoring (static `Scoring`)
`GetTierW(pct)`, `ScoreRaw(cat, p)`, `ScoreDomains(cat, p)`, `ClassifyCluster(p)` → `(Primary, Secondary)`, `CalcAnxietyRisk(p)`, `AverageProfile(cat, batches)`. `p` is `IReadOnlyDictionary<string,double>` terpene id → %. Domain ids are strings (`DomainIds.Sedation` = `"sedation"`, etc.). Some `INTENTS` entries have no `pri`, so `Primary` can be null. Constants (NF 2.7765, tier weights, cluster thresholds, anxiety coefficients, 8-week half-life) are in `EngineConstants` with source lines; tables come from the catalog.

## Pricing (static `Pricing`)
```csharp
PriceQuote pq = Pricing.GetEffectivePrices(cat.Pricing, tier, dow);   // pre-tax per weight + DealName (null = MSRP)
double post = Pricing.ApplyTax(pq.Prices[3.5], cat.Pricing.TaxRate);  // floor to $0.05 (GAP-204: mirrors v7.11.4)
```
`GetEffectivePrices(t, tier, brand, strainName, dow)` is the full L21172 resolver: `StrainOverrides` > `BrandPricingClass` > batch tier, then the first active matching deal from day deals + `CustomDeals` (targets tier / multiTier / pricingClass / brand; types weight_table / weight_flat / pct_msrp / use_tier). The snapshot has no overrides, brand classes or custom deals, so those lists start empty and are filled by code. `CheapestPostTax`, `HasPricingConfigured`. The 3-argument overload is unchanged.

## Determinism
No clock, randomness or IO inside the engine. JS `Math.round` ⇒ `JsMath.Round` (half up); `toFixed(6)` ⇒ `JsMath.ToFixed`. Sorts are stable (LINQ `OrderByDescending`), matching V8.

## Parity switches (defects; defaults = v7.11.4)
- `ShopState.EmptyTierCountsAsHouse` (V73-NT5): `true` = v7.11.4; `false` = game fix (an empty tier matches no chip).
- `ParserOptions.FixForTheDay` (MC-7): adds the v7.11.5 `'for the day'` key (daytime numbers). `ParserOptions.FixSleepAsk` (GAP-206): `_sleepAsk` matches `sleep\w*`. `ParserOptions.V7114` (default) / `ParserOptions.Game` (both on).

## Goldens
`golden_cases.json` (MIG-001, 39 cases) and `golden_cases_game003.json` (`node Tools/Data/golden_game003.js`: 54 more v7.11.4 queries + MC-7/GAP-206 under v7.11.4 and under the patched source) both replay from the raw query in `ParserGoldenTests`.
