# BRAND-001 handoff: only approved brands ship (DEC-071)

**Status:** done; awaiting Hub review. Branch `claude/fervent-maxwell-13572b`.
**Approved (unchanged):** The Flower Shop / TFS, Dr Green Thumb (`DR. GREENTHUMB'S`), Rebel Grown, High Variety, Tok (`ToK`).

## 1. Inventory (before this change)
| Source | Records | Brands | Approved | Non-approved |
|---|---|---|---|---|
| `Data/Catalog/batches.json` (engine, `import_catalog.js`) | 1207 batches | 33 | 3 brands, 830 batches | 30 brands, 377 batches |
| `Data/Catalog/packaged_catalog.json` (`import_packaged.js`) | 954 items | 104 | 5 brands, 122 items | 99 brands, 832 items (plus brand slugs in ids and coined product-line words in 62 names: HYPHEN, FUZION, PUFF-GO, FLOWER POP, PYRIC, TWERPZ, SUPER FOG, BRIQ, WANA, LEAFERS) |
| PROC label params (`Tools/Blender/params`, `Art/Exports/Procedural/manifest.json`) | | 0 | | 0 (generic labels, PROC-004) |
| Jar label cards / UI (`SliceGame.JarLabel`, `SliceView`) | | runtime only | | text comes from `batches.json` `brand`, so fixed by the data |
| C# code, UI strings, slice data, tests, goldens, DP scenarios | | 0 | | 0 |

Union of non-approved brand spellings: 115 → **114 aliases** (`Grow Science` / `GROW SCIENCES` share one).

## 2. Does the recommendation logic read brand?
Tool v7.11.4 (`dev/v7114/tool.html`) and the C# port: brand is read **only** in `getEffectivePrices` → `getBrandPricingClass` (store `_brands[].pricingClass`) and `'brand'`-target deals (C# `Pricing.cs` L81/L105). The parser, exclusions, Similar, scoring, tier nudge, clusters and averaging never read it. `_coaTier` reads `'The Flower Shop'` at COA entry (tier is already baked into the data, and TFS is approved).
In the imported data the canonical inventory's 33 `brands` rows carry no `pricingClass`, and the importer rejects non-`tier` deals, so `BrandPricingClass` is empty and brand is **engine-neutral**. A 1:1 rename at import keeps output identical.
**Design:** an alias at import, not at presentation, so no real name ships at all. It's an injective map, so any future brand-keyed table stays equality-consistent if it gets the same `aliasBrand` (see Risks).

## 3. Implementation
- `Tools/Data/brand_aliases.json` (importer input, not shipped): approved list + 114 `{name, real[], lines{}, text}` entries. Fictional names are invented words. `text:false` marks common-word brands (MADE, SAUCE, PURE, COOKIES…): they're replaced in brand fields only, so strain names like "ORANGE COOKIES" are untouched.
- `Tools/Data/brands.js`: `aliasBrand` (an unknown non-approved brand **fails the import**), `scrubText` (names), `guardCatalog`, `--check`, `--selftest`.
- `import_catalog.js` 1.2.0: `brand: aliasBrand(...)` + the brand guard. `import_packaged.js` 1.1.0: aliased brand, scrubbed name, id rebuilt from them, and the brand guard inside `guard()`.
- Regenerated: `batches.json` (only `brand` differs: 0 other field diffs, map injective), `manifest.json`, `packaged_catalog.json` (only `brand`/`name`/`id` differ, 954 unique ids). `DP-020.json` `catalogMd5` 6fdc5535… → 8a358a0b….
- Goldens: generated from the real tool + inventory and hold no brand fields. `golden_game003.js` re-run is byte-identical to the committed file, so nothing to regenerate (DEC-014 satisfied).

## 4. Check
`node Tools/Data/brands.js --check` scans every tracked text file under `UnityProject/Assets/_Game`, `Tools/Blender/params` and the PROC manifest. Catalog `brand` fields must be approved or fictional, and no string anywhere may hold a real brand word or product line (whole word, case-insensitive). Both importers run the same guard on their output.

## Validation
- `node Tools/Data/brands.js --selftest` OK; `--check` OK (103 files). `import_packaged.js --selftest` OK.
- `import_catalog.js` and `import_packaged.js` regenerated from md5-matching sources (index.html 228684e9, inventory 09bfa4f0, archived Dutchie export).
- Unity EditMode (one `studio.ps1 unity-test-edit` run, fresh worktree, `Artifacts/TestResults/20261030-032851-734-42772-editmode.xml`): 185 total, 165 passed, 20 failed. All data/engine suites pass: EngineGolden 23/23, ParserGolden 95/95, TfsParity 11/11 (includes DP-020 on the new catalog md5), EngineFeature 4/4, Slice 21/21, Cart 10/10, DomainAssembly 1/1.
  The 20 failures are all `JarFillImportTests` (6) + `PackagedGoodsImportTests` (14) with "no LODGroup (the _LOD<n> suffix auto-setup)". This change touches no FBX, importer or model code, so it is most likely the first import in a fresh worktree. **Not re-run** (one-run budget, DEC-013). Reviewer: re-run EditMode in a warm worktree to confirm they pass on main too.

## Questions for Nolan (through the Hub)
1. **The Flower Mine** (`batches.json` 14 smalls batches, `packaged_catalog.json` 9 preroll packs): the name looks like a TFS house line, but it isn't on the DEC-071 list, so it's aliased to `Bloomshaft` for now. Is it a TFS brand that should stay? If yes, add it to `approved` and re-run both importers.
2. **THE FLOWER SHOP merch "LV WHITE SHIRT (S)"**: does "LV" stand for something trademarked? It's kept as-is for now.

## Risks / not done
- The fictional names were checked against the source brands and the scanner, but **not against a trademark search**. A coincidental match with some real brand elsewhere is possible.
- Common-word brands (`text:false`) and generic product terms (SWITCH VAPE, CANNON, MOON ROCK, SHORTIES as a format) aren't scrubbed from free text. Strain names (some breeder-branded) are out of scope.
- Images/FBX aren't scanned (binary). PROC-004 labels are generic by design.
- If a future import brings `_brands[].pricingClass` or brand-target deals, their brand keys must go through `aliasBrand` too. `import_catalog.js` currently rejects non-tier deals and doesn't import `_brands`, so this can't happen silently.
- Proposed DEC for the Hub to ratify: "Brand display names are aliased at import via `Tools/Data/brand_aliases.json`; `brands.js --check` must pass before any build."
