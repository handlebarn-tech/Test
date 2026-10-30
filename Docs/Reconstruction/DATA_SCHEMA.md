# Data schema: batches, terpenes, prices (MIG-001, for DATA-001)

Sources: `tfs-budtender/inventory/tfs-inventory-master.json` (md5 `09bfa4f00206b25f77fb2a49db2eea9c`, `version "tfs-3.3"`, `exported 2026-10-29T19:13:36.534Z`) and the v7.11.4 page (`L#####` = line in `deploy/2026-10-30-v7114/site/index.html`). All counts come from that snapshot. `deploy/.../site/demo-data.json` (md5 `891575995bccf7a945bd4cf29374b512`) is the same 1207 batches plus `demo` and `source` keys.

## 1. Inventory master (`tfs-inventory-master.json`)

Top level: `{version, exported, custom:{<batchId>:Batch}, deleted:[id], brands:[Brand]}`. There is **no `pricing` key**, so prices come from page defaults (§4).

### Batch (1207 records in `custom`; the key is the batch id, e.g. `custom_1774052104570_qvxs`, `custom_web_0679_zegr072026`)

| Field | Present | Type / example | Engine use |
|---|---|---|---|
| `name` | 1207 | "Amplified" | **yes**: strain grouping key via `normName` (L15434). 366 groups, at most 25 batches per strain |
| `batch` | 1207 | "AMPD081825" | display; date inference `parseBatchDate` (L20514) |
| `p` | 1207 | `{terpId: pct}`, 56 distinct ids, all in `DB` | **yes**: the only scoring input. 21,597 values are `0` (= tested ND) |
| `total` | 1207 | 0.6801 … 6.5147, median 2.6046 | low-confidence note when `<0.50` (none in the snapshot) |
| `status` | 1207 | `active` 77 / `oos` 1130 | **yes**: `batchInStock` = `status!=='oos'` (L15472) |
| `tier` | 1207 | house 777, t3 147, fttp 92, t2 64, smalls 49, t1 30, premium 16, t4 4, `''` 28 | **yes**: tier nudge (L15408), tier chips, price tier |
| `brand` | 1207 | "Dr Green Thumb" | price class lookup (none set); display |
| `custom` | 1207 | `true` | none |
| `date` | 706 stored (1159 after batch-code backfill; 453 inferred) | "2026-08-04" (COA test date) | **yes**: recency weight in `averageProfile` (L15483); age badge |
| `thc` | 718 | 15.09 … 35.52 (% total THC) | not in ranking. Picks TFS Premium (≥30) in automation `tfs_rules.js tierFor` |
| `labAromas` | 1189 | `["orange","cinnamon",…]` | display (merged per strain, L15454) |
| `coaUrl` | 718 | public COA PDF on theflowershopusa.com | display / Lab Results only |
| `source` | 1189 | `"coa"` | none |
| `ts` | 1189 | epoch ms (import time) | none ("never import time" for dates, L15477) |
| `id` | 471 | duplicate of the key | none |

In-stock snapshot (77 batches / 67 strains): smalls 35, t3 19, house 6, t2 6, t1 5, fttp 4, premium 2. 2 are undated and 3 have no THC.

### Brand (33 in `brands`)
`{name, tier}` only. Tiers: t3 12, t2 7, t1 5, house 3, fttp 2, t4 1, `''` 3. No `pricingClass`, so `getBrandPricingClass` returns `'tier'` for all (L21140). The tier rules behind these (house brands, sheet logos, Premium ≥30% THC) are in `automation/tfs_rules.js` `SHEET`, `HOUSE`, `tierFor` (automation data, not runtime).

### `deleted` (30 ids)
Built-in/legacy ids removed at load (`loadStorage` L17662). None match a current `custom` key, so all 1207 are kept.

## 2. Terpene DB (in the page, not in the JSON): `DB` L15044-15105

60 entries keyed by id (`beta_myrcene`, `dl_limonene`, …): `{name, cls:'mono'|'sesqui', chem:[aroma tags], d:{sedation, uplift, anxiety_relief, pain_inflammation, focus_cognitive, antimicrobial}, ev:'low'|'medium'|'high', notes?, aliases:[]}`. Weights range from −0.15 to 1.00. Four DB terpenes never occur in the inventory (`alpha_bergamotene`, `germacrene_d`, `alpha_bisabolene`, `aromadendrene`). `beta_eudesmol` has all-zero weights. Companion tables for DATA-001 to import alongside: `BA_SCALARS` L15127, `CL` cluster rules L15107 (code, not data), `CLUSTER_BONUS` L15327, `_TERP_EXTRA_ALIASES` L15956, `_EXCL_FAMILY` L15976. Learn-tab monographs (`EDU` L19816, ~90 entries) are education copy. The tool's standing rule keeps them off-limits for edits, and they are not engine data.

## 3. Intent tables (in the page)
`INTENTS` L15619-15883 (287 keys `{d,neg,lbl,pri}`), `PHRASE_MAP` L16098-16158 (54 regexes), `negPatterns` L16066 (10), fuzzy fallback L16226 (8), `PRICE_INTENTS` L21696 (8/19/12), `REFINE` L19583 (11). Port these as data plus regex tests. Keep the regexes byte-identical, or rewrite them with the golden cases as the oracle.

## 4. Pricing (in the page): `TIER_DEFAULTS` L21018, `DEFAULT_DAY_DEALS` L21036, tax 25.1 (L21062)
Shapes: tier `{gpg, w:{3.5,7,14,28}}`. Deal `{id, name, active, target:{type:'tier'|'multiTier'|'pricingClass'|'brand', value|values}, dealType:'weight_table'|'weight_flat'|'pct_msrp'|'use_tier', w? | weight+flatPrice? | pct, excludeWeights, ozOverride, baseTier? | useTier?, day?}`. Override `{name, tier}`. Values are in `RECONSTRUCTION_CONTRACT.md` §12. v7.11.5 (unreleased) changes only Tier 2 14 g ($75 to $77).

## 5. What the engine consumes (minimum importer output)
Per batch: `id, strainName, batchCode, brand, tier, inStock, testDate?, dateInferred?, terpenes{id:pct incl. 0}, total`. Plus the terpene table (`DB` + BA scalars), the intent tables (§3) and the price tables (§4). Everything else is display (`labAromas`, `coaUrl`, `thc`) or provenance.

## 6. PII / exclusion list (DEC-006)

- **Inventory master, brands, DB, prices: no PII found.** Fields are product/lab data. `coaUrl` points to public company PDFs. The importer still allow-lists fields (§5) rather than copying records whole.
- **Exclude entirely** (never read or import): `tfs-budtender/dev/customers/**`, Downloads `*Patient*`, `*.xlsx`, `*.eml` exports, and the Supabase tables `searches`, `feedback`, `audit_log`, `memberships`, `profiles` and auth.
- **Fields that carry person data if ever encountered:** feedback `employee_id`, `corrected_by`, `location_id`. Search-log `q` (free text: staff may type a customer name; HUB GUIDE-4 "customer-name reminder"), `staff`, `uid`, `sid`, `prof`. Accounts `username`, `name`. Legacy `tfs_regulars_v1` customer profiles (removed in Phase 4, L22616). The game generates its own synthetic NPC and feedback data instead.
