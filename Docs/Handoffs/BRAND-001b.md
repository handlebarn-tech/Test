# BRAND-001b handoff: fictional-brand collision pass (DEC-078)

**Status:** done; awaiting Hub review. Branch `claude/task-brand-001b` (off main 989d702).

## Name check
One web search per name across all 114 fictional names (two parallel subagents, 2026-10-30). Each replacement was also searched once. This is a web search, **not** a trademark database (USPTO TSDR) search.

| Old (real source brand) | Collision found | New |
|---|---|---|
| Clearleaf (PURE) | DEC-078 real mark | **Glenmint** (searched clean; "Verdelle" was also clean but looks like the real "Verdant") |
| Quintessa ((the) ESSENCE) | DEC-078 real mark | **Mistaven** |
| Seekwell (Find) | hemp formulation startup + pending SEEKWELL mark (1-800 Contacts, 97891635) | Seekmarrow |
| Smartleaf (Wiser Buds) | SmartLeaf Health Services, a medical cannabis clinic (Calgary) | Cleverfrond |
| Sipwell (SIP) | Sipwell Wine Co., canned wine | Tipplemoor |
| Fizzhaven (KEEF) | "Fizz Haven" soda shop (WI), a beverage overlap | Fizzhollow |
| Emberlit (FIREBRAND) | EmberLit camp stoves, live mark 4353910 | Embervane |
| Pivotel (TURN) | Pivotel, an Australian telecom | Hingeway |
| Skyvane (Aeriz) | Levolux SKYVANE shading mark (status unclear) | Skyfenn |
| Bundlecraft (PROJECT PACKS) | Shopify/WooCommerce app | Parcelwright |
| Wanderpod (ROVE) | "Wanderpod" accommodation units (AU) | Roamcask |
| Pulsewell (VITAL) | PulseWell wellness app | Beatmoor |

The other 102 names came back clean. Notes from the search:
- Everwick, Rollbarrow and Flipvane had only dead USPTO filings.
- Wrought, Stubbins and Thornberry are plain words or surnames.
- Quillmark, Contrail and Topmark showed no cannabis, vape or smoke-shop hit.

**DEC-081 addition:** Nolan approved "The Flower Mine" as a TFS house line. It is added to `approved`, the Bloomshaft alias is gone (113 aliases), both imports and `brands.js --check` were re-run and pass, and DP-020 catalogMd5 is now 0e7675d71bc9e54b5f7e6b9db2a40eef. "LV WHITE SHIRT" stays as-is. No Unity run for this addition: the data change is brand-field only, the same as the run above.

## Changes
- `Tools/Data/brand_aliases.json`: 12 names changed. The real-brand keys are unchanged, so the map is still 1:1.
- Regenerated from md5-matching sources: `batches.json` (only `brand` changes), `manifest.json` and `packaged_catalog.json` (only brand, name and id change).
- `DP-020.json` catalogMd5 8a358a0b… → 214e59f5….

## Validation
- `node Tools/Data/brands.js --selftest` OK; `--check` OK (118 files). `import_packaged.js --selftest` OK.
- Unity EditMode (one `studio.ps1 unity-test-edit` run, `Artifacts/TestResults/20261030-034552-560-20632-editmode.xml`): 194 total, 174 passed, 20 failed. All data/engine suites pass: EngineGolden 23, ParserGolden 95, TfsParity 11 (includes DP-020), EngineFeature 4, Slice 21, Cart 10, OverLimit 9, DomainAssembly 1.
  The 20 failures are the same as in BRAND-001: `JarFillImportTests` 6 + `PackagedGoodsImportTests` 14, "no LODGroup (the _LOD<n> suffix auto-setup)". This worktree was already warm, so it is **not** a first-import artifact. Data-only changes can't cause it; it looks like a pre-existing, environment-dependent FBX import issue in this worktree. **For the Hub:** check whether the same tests pass on main in another worktree. If they fail there too, it's a PROC/QA task, not BRAND.

## Not done / risks
- Product-line words (DASHWELL, FUSELLE, PUFFRUN, PETAL DROP, CINDRALL, TWIRLEENS, GRAND MIST, BLOCKETT, CALMBEAM) were **not** web-checked. They weren't in this task's scope.
- A trademark-database search before a public build is still recommended.
