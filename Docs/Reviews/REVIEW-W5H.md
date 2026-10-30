# REVIEW-W5H — BRAND-001: approved brands only (DEC-071)

**Verdict: PASS (GO) with minors.** Branch `review/wave-5h` (off `main` 0810b83) merges `claude/fervent-maxwell-13572b` (71e3732 + 98ce92c) cleanly. Reviewer: UX-002 workcell session, 2026-10-30.

## Tests (studio.ps1, DEC-013; this worktree is warm, with many prior imports)
`unity-test-edit` on the merged branch: **185/185 passed** (`Artifacts/TestResults/20261030-033540-139-42720-editmode.xml`). That covers EngineGolden 26, ParserGolden 99, EngineFeature 5, TfsParityGate 15 (incl. DP-020 on the new catalog md5), Slice 22, Cart 11, DomainAssembly 2, and **ProcArt JarFillImport 8 + PackagedGoodsImport 16**.
→ The worker's 20 ProcArt "no LODGroup" failures **don't reproduce**. They come from the first FBX import in a fresh worktree (the `_LOD<n>` auto-setup), and the branch has nothing to do with them; it touches no FBX, importer or model code.

## Recommendation parity (DEC-001/002/014)
- **Engine catalog** `batches.json`: same 1207 ids. The **only** field that differs is `brand` (377 batches); there are no other field or top-level diffs. Map checked: injective, no collisions; the 3 approved deli brands (`The Flower Shop`, `Dr Green Thumb`, `Rebel Grown`) are unchanged.
- **Does the engine read brand?** Only through `Pricing.GetStrainPricingTier` → `BrandPricingClass` and `"brand"`-target deals (`Pricing.cs:81,105`). `BrandPricingClass` is never filled by the importer or loader (the only writer is a unit test with "Acme"), and `pricing.json` has no brand keys or brand deals. Brand is therefore engine-neutral: the ranking, Ms, prices and tags can't change.
- **Ranked output:** the engine goldens (computed from the real v7.11.4 tool, keyed by strain/batch, no brand field) and the parser goldens all pass on the new catalog, and Gate A passes. That is the before/after ranked-output diff; any rank or price change would fail them. The handoff gives no separate diff script.
- **DEC-014:** goldens hold no brand, and the worker's `golden_game003.js` re-run is byte-identical, so nothing needed regenerating. `manifest.json` and `DP-020.json` `catalogMd5` were updated together with the data. ✔

## Approved five untouched
- Packaged catalog: the counts before and after are identical: `THE FLOWER SHOP` 46, `DR. GREENTHUMB'S` 40, `HIGH VARIETY` 25, `ToK` 9, `REBEL GROWN` 2.
- 832 items changed `brand`/`id`, which equals the non-approved count; 62 had `name` scrubbed. No other fields changed (price, category and counted grams are untouched).
- `brand_aliases.json` lists the approved spellings incl. TFS. ✔

## Fictional names (114)
- They are invented, or ordinary words, and none echoes its source brand (e.g. STIIIZY→Tallowfin, Jeeter→Tallwick, Wyld→Thornberry). The "x" collab pattern and product-line renames (HYPHEN→DASHWELL etc.) are consistent.
- **m1 — two names collide with real brands** (quick web check, not a trademark search):
  - **Clearleaf** (for PURE) is an actual UK medical-cannabis company (CB Insights profile). Rename it; it's in the same industry.
  - **Quintessa** (for "(the) ESSENCE") is a well-known Napa wine estate. It's a different industry, but a famous mark. Rename it.
  - "Smartleaf" (for Wiser Buds) gave no hit as a brand.
  - The handoff's own risk note (no trademark search) stands. A one-pass search of the 114 before any public build is cheap.
- **n1:** keep "The Flower Mine" aliased (→ Bloomshaft) until Nolan answers the handoff's Q1; it is not on the DEC-071 list.

## PII (DEC-006/048/050)
`import_packaged.js --check <archived export>` → `guard OK: packaged_catalog.json (954 items, dropped-value scan on)`. The import still reads only the whitelisted columns. `brand_aliases.json` holds brand names only, which are not PII, and it is an importer input, not shipped. ✔

## Guard (`Tools/Data/brands.js`)
- `--selftest` OK. `--check` OK on the branch (103 files).
- **Probe 1:** one batch's brand changed to the unknown real brand "Kiva Confections" → `BRAND CHECK FAIL (DEC-071) … $.batches.419.brand: "Kiva Confections" not approved`.
- **Probe 2:** "STIIIZY" planted in a packaged item name → `FAIL … $.items.0.name: "STIIIZY" in …`.
- Both files were restored with `git checkout`; the tree is clean.
- **n2:** free-text detection only knows the 114 listed brands. A new unknown brand inside a *name* would pass, while one in a `brand` field fails. That's fine because both importers fail on unknown brands at import. Keep running the check in both importers.

## For the Hub
- Merge on GO.
- Have BRAND-001 (or a small follow-up) rename **Clearleaf** and **Quintessa** and re-run both importers + `--check` (m1).
- Ratify the proposed rule: "brand names aliased at import via `brand_aliases.json`; `brands.js --check` passes before any build".
- Forward the handoff's Q1 (The Flower Mine) and Q2 ("LV" shirt) to Nolan.
