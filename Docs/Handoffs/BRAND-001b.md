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

"The Flower Mine" stays aliased to Bloomshaft until Nolan answers (DEC-078).

## Changes
- `Tools/Data/brand_aliases.json`: 12 names changed. The real-brand keys are unchanged, so the map is still 1:1.
- Regenerated from md5-matching sources: `batches.json` (only `brand` changes), `manifest.json` and `packaged_catalog.json` (only brand, name and id change).
- `DP-020.json` catalogMd5 8a358a0b… → 214e59f5….

## Validation
- `node Tools/Data/brands.js --selftest` OK; `--check` OK (118 files). `import_packaged.js --selftest` OK.
- Unity EditMode: see below.

## Not done / risks
- Product-line words (DASHWELL, FUSELLE, PUFFRUN, PETAL DROP, CINDRALL, TWIRLEENS, GRAND MIST, BLOCKETT, CALMBEAM) were **not** web-checked. They weren't in this task's scope.
- A trademark-database search before a public build is still recommended.
