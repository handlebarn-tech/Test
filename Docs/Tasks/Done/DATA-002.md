# DATA-002 — Packaged-goods catalog importer (Dutchie export → PII-free game data)

**Role:** DATA · **Priority:** P1 (PS3 packaged goods) · **Branch:** worktree off `main`

## Goal
Turn Nolan's Dutchie inventory export into a deterministic, PII-free, cost-free `packaged_catalog.json` the game reads for the eight packaged categories (DEC-034), closing GAP-PKG-01/04 with real names, sizes, doses and shelf prices.

## Read
`CLAUDE.md`; DEC-006, DEC-014, DEC-034, DEC-048, DEC-050 (`Docs/DECISIONS.md`); `Tools/Data/import_catalog.js` (house importer pattern); `Docs/Design/SPEC_GAME004.md` §2, §4, §5, §8; GAP-PKG rows.

## Input (untrusted, read-only, never copied into the repo)
A Dutchie "Current Inventory" export (`.xlsx`) from `C:/Users/handl/Downloads/Dispo Game Imports/` (archived 2026-10-30 to `C:/Users/handl/Downloads/Dispo Game Imports Archive/2026-10-30_dutchie-inventory/`, DEC-070) or a path passed on the command line. Inspect the header row and category column only before writing code.

## Owns
- `Tools/Data/import_packaged.js` (new; Node, no dependencies, same style as `import_catalog.js`).
- `UnityProject/Assets/_Game/Data/Catalog/packaged_catalog.json` (new; GAME-001 data layout).
- `Docs/Handoffs/DATA-002.md`.
- Don't touch the deli importer, its outputs, goldens or Unity code.

## Deliverable
1. Explicit input-column **whitelist**; every other column (cost, vendor, quantity, package/batch/external IDs, location, dates) is never read into the output. Missing whitelisted column → hard fail.
2. Output mapped to DEC-034 categories, with `limit` (pool + grams; DEC-048) and `storage` (FOH / fridge / cooler; DEC-050). Unknowns are `GAP`, never guessed.
3. Self-test (`--check`): output key allow-list, no value from a dropped column survives, PII scan (emails, phones, license/METRC-style IDs).
4. Deterministic: same input → byte-identical output.

## Validation
`node Tools/Data/import_packaged.js <export>` twice → identical md5; `node Tools/Data/import_packaged.js --check <export>` passes; JSON parses.

## Handoff
`Docs/Handoffs/DATA-002.md` (≤60 lines): summary stats only (counts per category, price ranges), never rows. Questions for Nolan go through the Hub (DEC-033/047). Flag that real brand names in a shipped build are an open IP decision (GAP-PKG-07).
