# DATA-002 handoff — packaged-goods catalog

**Status:** done. `Tools/Data/import_packaged.js` (Node, no dependencies, same style as `import_catalog.js`) → `UnityProject/Assets/_Game/Data/Catalog/packaged_catalog.json` (+ `.meta`).
**Input:** Dutchie "Current Inventory" export, 10/18–10/25/2026, read in place from `Downloads/Dispo Game Imports/` (default path; or pass a path). It was never copied into the repo; its source md5 is recorded in the JSON.

## What the importer does
- **Whitelist** (fails if any column is missing): Product Name, Category, Brand Name, Inventory Price, Strain Name, Inventory Room. Room is used only to drop non-sellable rows (Quarantine, POS RETURN, SAMPLES/PROMOS) and to set `medicalOnly`; the room string itself isn't output. Every other column is dropped: cost, vendor, quantity, weight, pricing tier, package/batch/external IDs, location, dates, UPC/SKU.
- The export has a 4-row preamble (export dates, the store's legal entity name). The importer finds the header row and treats the preamble as dropped.
- The export has **no SKU, size or THC/CBD columns**. `sizeG`, `packCount`, `thcMg` and `cbdMg` are parsed from the product name. Vapes and extracts have no THC %. The id is a slug of category, brand and name (0 collisions).
- 48 Dutchie sub-categories map to the DEC-034 categories (`subcategory` keeps the original). An unmapped sub-category fails the run. Bulk Flower (deli, 126 rows) is skipped because the tool owns it.
- Shelf price is the modal price across packages (0 conflicts in this export). `strainKey` is set only when the export's strain matches a tool batch, and only for prepacks, prerolls, vapes and extracts (SPEC_GAME004 §4).
- `limit` = {pool, grams, gap} per DEC-048. `storage` = FOH, fridge, cooler or GAP per DEC-050.
- **Guards:** output fields must be on the allowed list. A PII scan checks for emails, phones, SSNs, dates, honorific + name, licence/METRC-style IDs and person-role words. A scan fails if any text value from a dropped column or the preamble appears in the output (values that are already part of whitelisted text are exempt). `--selftest` plants leaks and asserts the scans catch them.

## Validation
- `--selftest` OK.
- Two imports give identical md5 `51477c9fc2f06e24fafc515fd7c3c88f`.
- `--check <export>` (with the dropped-value scan) and `--check` both OK.
- grep finds 0 hits for the entity name, "cost" or "vendor".
- Unity: not run. The file is plain JSON (string/number/bool/null) that `Dispo.Domain.Engine.Json` already parses; nothing reads it yet (GAME-004).

## Summary stats (954 items, 104 brands; skipped: 126 deli, 20 non-sellable room, 12 zero/penny price)
| Category | Items | Price range (median) | Limit gap | Storage gap | strainKey |
|---|---|---|---|---|---|
| VAPE | 297 | $15–79 ($45) | 0 | 0 (FOH) | 10 |
| PREROLL | 226 | $3–60 ($30) | 152 (infused) | 74 (plain) | 29 |
| EDIBLE | 193 | $5–68 ($16) | 193 | 4 (chocolate) | – |
| EXTRACT | 79 | $15–70 ($25) | 0 | 0 (cooler) | 14 |
| PRE-PACK | 73 | $20–120 ($45) | 11 (infused) | 73 | 22 |
| MERCH | 39 | $1.25–35 ($16) | 0 | 39 | – |
| BEVERAGE | 30 | $6–17 ($10) | 30 | 0 (fridge) | – |
| TOPICAL | 17 | $10–60 ($26) | 17 | 17 | – |
Storage: FOH 633, cooler 84, fridge 30, GAP 207. medicalOnly 11; infused 166.

## Open / for the Hub
- **IP:** the output keeps real brand and product names as data. Shipping them in a build is still the open trademark decision (GAP-PKG-07, PROJECT_STATE). If it goes generic, the game can mask the names at load time without re-importing.
- DEC-014 covers the deli engine data only; the goldens are unaffected. SPEC_GAME004 §5 placeholder prices can now give way to real shelf prices (GAP-PKG-04 → mostly closed, pre-tax).
- Never commit the in-repo `Imports/` drop (locally ignored per the Hub).

## Questions for Nolan (through the Hub)
1. **Edible/beverage limit.** Source: DEC-048 "≈0.1 g". Placeholder: concentrate pool, flat 0.1 g per package, GAP-COMP-02. Which pool do they count against, and is it per package or THC mg ÷ 1000 (100 mg → 0.1 g)?
2. **Infused prerolls, infused flower and shake.** Placeholder: whole weight against the flower pool, GAP. Does part of it count against the 5 g concentrate limit?
3. **Topicals and patches** (incl. "OTHER - CBD", which are pet CBD products). Placeholder: pool GAP. Do they count at all?
4. **Storage not covered by DEC-050.** Placeholder: GAP for chocolate, plain prerolls, prepacks, topicals and merch. Placeholder: cooler for baked goods (read as "perishable edibles"). Where does each sit?
5. **2 rec edibles/beverages are listed above 100 mg THC** (in sellable rooms, not medical-only). Real (e.g. multi-pack), or should they be medical-only?
