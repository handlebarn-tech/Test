# ENGINE: recommendation engine API (GAME-001)

Pure C# port of the TFS budtender v7.11.4 recommendation slice (MIG-001 "Recommended vertical-slice subset", DEC-001/002). Assembly `Dispo.Domain` (`noEngineReferences`), namespace `Dispo.Domain.Engine`, folder `UnityProject/Assets/_Game/Code/Domain/Engine/`. Every function cites its v7.11.4 source function and line.

## Data (generated, do not hand-edit)
`UnityProject/Assets/_Game/Data/Catalog/`, written by `node Tools/Data/import_catalog.js` (deterministic; `--check` re-runs the PII allow-list).

| File | Content |
|---|---|
| `batches.json` | 1207 batches: `id, strainName, batchCode, brand, tier, inStock, testDate, dateInferred, total, terpenes{id:pct}` (tested-ND zeros kept) |
| `terpenes.json` | 6 domain ids, 60 terpenes `{id,name,cls,d{6}}`, `baScalars` |
| `engine_tables.json` | `intents` (287 keys `{d,neg,lbl,pri}`), `clusterBonus`, `tierNudge` |
| `pricing.json` | `taxRate` 25.1, `weights` [3.5,7,14,28], `tiers` (TIER_DEFAULTS), `dayDeals` by dow 0-6 |
| `manifest.json` | importer version, source md5s, output md5s, counts |

The snapshot is a fixture: stock is the master file's `status` at export 2026-10-29 (GAP-202). Re-import ⇒ regenerate goldens.

## Loading
```csharp
using Dispo.Domain.Engine;
Catalog cat = Catalog.Load(batchesJson, terpenesJson, tablesJson, pricingJson); // strings; the caller does file IO
```
`Catalog`: `Batches` (file order), `Terpenes` (id → `Terpene{Id,Name,Cls,D}`), `BaScalars`, `Intents`, `ClusterBonus`, `TierNudge`, `Pricing`, and `Groups()` (strain groups by `Catalog.NormName`, in-stock batches first, cached).

## Intent (the NPC emits an `INTENTS` key; no NL parsing in the slice)
```csharp
IntentQuery q = Intents.Resolve(cat, "sleep");            // null when the key is unknown
// q.Crit {domain:min}, q.Neg {domain:max}, q.Primary, q.Label
```
Applies the parser's conflict rule (L16200) and the pain-functional default (L16211: pain crit, no sedation cap ⇒ `neg.sedation=55`, unless the key itself is a heavy/sleep word). Keys that match the full parser's result: `sleep`, `anxiety`, `pain`, `energy`, `sinking`. Multi-word phrases (`stress relief`, `insomnia` via PHRASE_MAP) are the parser's job (next wave); pass explicit `Crit/Neg/Primary` instead.

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
- Not ported yet (next wave): exclusions, like-X, maxAnx/refine, maxPrice filter, role tags, compare, Similar, terpene rank, full NL parser.

## Scoring (static `Scoring`)
`GetTierW(pct)`, `ScoreRaw(cat, p)`, `ScoreDomains(cat, p)`, `ClassifyCluster(p)` → `(Primary, Secondary)`, `CalcAnxietyRisk(p)`, `AverageProfile(cat, batches)`. `p` is `IReadOnlyDictionary<string,double>` terpene id → %. Domain ids are strings (`DomainIds.Sedation` = `"sedation"`, etc.). Some `INTENTS` entries have no `pri`, so `Primary` can be null. Constants (NF 2.7765, tier weights, cluster thresholds, anxiety coefficients, 8-week half-life) are in `EngineConstants` with source lines; tables come from the catalog.

## Pricing (static `Pricing`)
```csharp
PriceQuote pq = Pricing.GetEffectivePrices(cat.Pricing, tier, dow);   // pre-tax per weight + DealName (null = MSRP)
double post = Pricing.ApplyTax(pq.Prices[3.5], cat.Pricing.TaxRate);  // floor to $0.05 (GAP-204: mirrors v7.11.4)
```
Tier deals only (`weight_table`, `weight_flat`), which is all the defaults use; the importer fails if a default deal needs more. Strain overrides and brand pricing classes are not ported (none exist in the snapshot).

## Determinism
No clock, randomness or IO inside the engine. JS `Math.round` ⇒ `JsMath.Round` (half up); `toFixed(6)` ⇒ `JsMath.ToFixed`. Sorts are stable (LINQ `OrderByDescending`), matching V8.

## Parity switches (defects; defaults = v7.11.4)
- `ShopState.EmptyTierCountsAsHouse` (V73-NT5): `true` = v7.11.4; `false` = game fix (an empty tier matches no chip).
