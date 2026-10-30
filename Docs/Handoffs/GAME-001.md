# Handoff: GAME-001 (DATA-001 importer + C# domain engine slice)

**Status:** done; validation below. Branch `claude/task-game-001-b68d0f` (off `base/wave-2`), not merged. API for DES-001: `Docs/Specs/ENGINE.md`.

## Delivered
- `Tools/Data/import_catalog.js` (Node 22, v1.0.0). Reads the pinned v7.11.4 `index.html` (md5 check, aborts on mismatch) and `tfs-inventory-master.json`, read-only. Takes the literals `DOMS, DB, BA_SCALARS, CLUSTER_BONUS, INTENTS, TIER_DEFAULTS, DEFAULT_DAY_DEALS, STD_WEIGHTS`, `_tierVal`, taxRate, evaluated in an empty vm context. Applies `_sanitizeImport`, `_safeRecord`, `deleted`, `_backfillDates`. `--check` re-validates the allow-list.
- `UnityProject/Assets/_Game/Data/Catalog/`: `batches.json` (1207 batches, 77 in stock, 366 groups, 453 inferred dates), `terpenes.json` (60), `engine_tables.json` (287 intents, cluster bonus, tier nudge), `pricing.json`, `manifest.json` (source + output md5s). A local `.gitattributes` pins LF, since `core.autocrlf=true` would otherwise break the md5s on checkout.
- `Code/Domain/Engine/`: `Json` (a minimal reader; Dispo.Domain has no package refs), `Catalog`, `Scoring` (`getTierW`, `scoreRaw/scoreDomains`, `classifyCluster`, `calcAnxietyRisk`, `averageProfile`, plus an `EngineConstants` block with source lines), `Recommender` (`Intents.Resolve`, `findStrains`, `respond` fallback), `Pricing`. Every function cites its source function and line.
- `Code/Tests/EditMode/EngineGoldenTests.cs`: 11 recommend goldens (the slice set plus X-03), 5 intent-key parity checks, 252 pricing cells, 4 batchScores, Zero Gravity averaging, the V73-NT5 game-expected check, and a JSON parser check.

## Validation
- `studio.ps1 unity-compile`: `csErrors=0; CompileCheck OK`. `unity-test-edit`: **24/24 passed** (`Artifacts/TestResults/20261029-214658-editmode.xml`).
- Determinism: three importer runs gave identical md5s (manifest `f6c7e56d…`, batches `6fdc5535…`).
- `import_catalog.js --check`: allow-list OK. Negative test: an injected `employee_id` makes it fail with exit 1.
- Source md5s match MIG-001 (html `228684e9…`, inventory `09bfa4f0…`).

## Parity notes / deviations
- The slice takes `crit/neg/primary` from the golden `parsed` block. NL parsing is the next wave. `Intents.Resolve(key)` matches the full parser for `sleep, anxiety, pain, energy, sinking`. It does not for phrase-map keys (`insomnia` → the parser yields 55/40, but the INTENTS entry is 45/35).
- The pain-functional default checks its "wants sedation" regex against the key rather than the query.
- Not ported: exclusions, like-X, maxAnx/refine, maxPrice filter, role tags, compare, Similar, terpene rank, strain overrides / brand pricing classes. The importer fails if a default deal needs a deal type that is not ported.
- None of the defects MC-7, GAP-206 or V73-NT5 is reachable by the slice goldens. V73-NT5 has a parity switch (`ShopState.EmptyTierCountsAsHouse`, default v7.11.4), tested on a synthetic batch because no in-stock batch in the snapshot has an empty tier.

## Proposed DEC entries (Hub decides)
1. The game's engine data comes only from `import_catalog.js` output; a re-import must regenerate the goldens (MIG-001 harness) in the same change.
2. V73-NT5: the game ships `EmptyTierCountsAsHouse=false` (the v7.11.5 behaviour) once tier chips exist in the UI; tests keep both values.
3. MC-7 / GAP-206 are parser defects. Fix them when the NL parser is ported, each with a v7.11.4 golden plus a game-expected golden.
4. NPC intents are emitted as `INTENTS` keys whose resolved crit/neg equal the parser's (verified set above). DES-001 picks keys from that set or supplies explicit crit/neg.
