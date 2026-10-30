# REVIEW-W5I — BRAND-001b: fictional-brand collision pass + The Flower Mine (DEC-078/081)

**Verdict: PASS (GO).** Branch `review/wave-5j` (off `main` 5dfa0c5) merges `claude/task-brand-001b` (a1fa377, 95c78d2, 19aabbb) cleanly. Reviewer: UX-002 workcell session, 2026-10-30.

## Checks
- **Approved list = DEC-071 + DEC-081 exactly:**
  - DEC-071: The Flower Shop / THE FLOWER SHOP / TFS; Dr Green Thumb / Dr Greenthumb / DR. GREENTHUMB'S; Rebel Grown / REBEL GROWN; High Variety / HIGH VARIETY; Tok / ToK.
  - DEC-081: The Flower Mine / THE FLOWER MINE.
  - The Bloomshaft alias is removed (113 aliases), and "Bloomshaft" appears nowhere in the data or tools. The 14 deli batches now carry "The Flower Mine". ✔
- **Renames:** 12 names changed, each keeping its real-brand key, so the map stays one-to-one. Clearleaf → Glenmint and Quintessa → Mistaven close REVIEW-W5H m1 (DEC-078).
- **Spot web-check** (4 searches covering all 12 new names): no exact-name brand found for Glenmint, Mistaven, Cleverfrond, Tipplemoor, Roamcask, Embervane, Skyfenn, Fizzhollow, Beatmoor, Hingeway, Parcelwright or Seekmarrow. **n1:** the "Glen-" prefix is strongly tied to Scotch whisky marks, and "Tipplemoor"/"Roamcask" read as drink names. That's not a collision, but worth a glance in the pre-release trademark pass (DEC-078).
- **Data:**
  - `batches.json`: same 1207 ids; only `brand` differs (73 batches).
  - `packaged_catalog.json`: 954 items; only `brand`/`id` differ (87), and all ids are unique.
  - `DP-020.json` `catalogMd5` = `manifest.json` batches md5 `0e7675d71bc9e54b5f7e6b9db2a40eef`. ✔
- **Guard:**
  - `brands.js --selftest` OK; `--check` OK (118 files, 113 aliases).
  - **Probe:** a batch brand changed to the unknown real brand "Kiva Confections" → `BRAND CHECK FAIL (DEC-071) … not approved`. Reverted; the tree is clean. ✔
- **PII:** `import_packaged.js --check <archived export>` → `guard OK (954 items, dropped-value scan on)`. ✔
- **Unity** (one `studio.ps1 unity-test-edit`, DEC-013): **194/194 passed** (`Artifacts/TestResults/20261030-035205-693-7076-editmode.xml`). That includes EngineGolden 26, ParserGolden 99, EngineFeature 5, TfsParityGate 15 (incl. DP-020), Slice 22, Cart 11, OverLimit 10, DomainAssembly 2, **ProcArt 24**.

## ProcArt LODGroup failures
They do **not** occur in this worktree. Here all 24 ProcArt tests pass, both in W5H (185/185) and now (194/194). So the 20 failures are specific to the worker's worktree and its FBX import state; they're unrelated to brand data, and "pre-existing on main" is not established. If they recur in other worktrees, they need a small PROC/QA look at `_LOD<n>` auto-setup, not BRAND.

## Nits
- n2: the handoff's "Changes" section still gives DP-020 md5 `214e59f5…` (the pre-DEC-081 value); the committed file and its DEC-081 paragraph say `0e7675d7…`, which is correct.
- n3: the handoff's table labels Fizzhaven's source as KEEF; in `brand_aliases.json` it is HIGH TIDE (KEEF is Fizzbarrow). The data is right.

## For the Hub
Merge on GO. The DEC-078 trademark-database pass before any public build still stands, and it should include the product-line words, which BRAND-001b didn't web-check.
