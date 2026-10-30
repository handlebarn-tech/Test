# ASSET-001 — $0 asset license ledger + acquisition list

**Role:** ART-SOURCING (research + doc) · **Priority:** P1 · **Branch:** `task/ASSET-001` worktree off `base/wave-2`

## Goal
Turn the candidate benchmarks in `ASSET_PRODUCTION_PLAN.md` into a verified, license-checked acquisition list for M5 (hero retail) and M6 (stock/BOH), so later art tasks only fetch and import.

## Read
`Docs/ASSET_PRODUCTION_PLAN.md` §B, §C, §0, §4–8 and later candidate sections; `Docs/MASTER_PLAN.md` §13 (zero-dollar rule).

## Owns
- `Docs/Assets/LICENSE_LEDGER.md`: one row per asset with source URL, exact license + version, attribution text, commercial-game use allowed, redistribution in repo allowed, file size, intended use, status.
- `Docs/Assets/ACQUISITION_LIST.md`: prioritized, slice and M5 first.

## Rules
- Check current license terms on the web; quote license names, not long text.
- **Do not download assets** in this task. Record URLs and sizes only.
- Reject anything not free for commercial use, behind paid tiers, or of unclear provenance (check Sketchfab items one by one).
- Prefer CC0; flag anything needing attribution.
- Cover audio (CC0 ambience, POS beeps, door chime), fonts (OFL) and HDRIs, not only meshes and textures.

## Validation
Every row has a license verified at a URL you visited, with the visit date.

## Handoff
`Docs/Handoffs/ASSET-001.md` (≤40 lines). Report to the Studio Hub.
