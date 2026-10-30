# REVIEW-W4O — DATA-002 packaged catalog importer

**Reviewed:** `claude/task-data-002-ff62ac` @ 4e86e13, merged into `review/wave-4o` (from main 79fdfc9).
**Verdict: GO with one fix applied on the review branch (M1).** PII and safety checks pass.

## 1. Whitelist and failure mode: PASS
- The importer reads exactly 6 of the 21 export columns: Product Name, Category, Brand Name, Inventory Price, Strain Name and Inventory Room.
  A missing column throws (`export is missing whitelisted column(s)`). An unmapped sub-category also throws.
- This differs from the brief's list, for good reasons. The export has **no SKU, size or THC/CBD columns**, so size, pack count and mg
  are parsed from the product name. Two columns go beyond the brief: Strain Name is output only when it matches a public tool batch
  (`strainKey`), and Inventory Room is used only to filter rows and set `medicalOnly`; it is never output.
- The 15 dropped columns are Location Name, Allocation Status, Quantity, **Inventory Cost**, Weight, Pricing Tier, **Vendor Name**,
  Package ID, Batch Name, expiry/use-by/audit dates, External Inventory ID, UPC and Provincial SKU.
- Output keys are checked against an allow-list. `--selftest` plants a cost field, an email, a phone, a METRC tag and a vendor value,
  and the guard catches all of them.

## 2. PII grep of `packaged_catalog.json` (independent of the importer's guard): PASS
- Keys: only the allow-listed fields (954 × 18 item keys plus header/counts).
- 0 emails, 0 phone numbers, 0 dates, 0 honorific+name, 0 long alphanumeric IDs. The only cost/vendor/licence/permit/METRC/note/
  room/sample match is the count key `nonSellableRoom`.
- Cross-check against the raw export (openpyxl script, outside the repo): for every value in the 15 dropped columns, check whether it appears in the output.
  - There were 17 Vendor Name hits. **All 17 equal the item's own brand** (vertically integrated brands), which is public label text.
    No vendor-only name appears.
  - There were 2 Package ID / External ID hits ("merlot", "slim bat"). These are colour/model words inside merch product names, not IDs.
  - None of the 8 preamble cells (export dates, legal entity name) appears in the output.

## 3. Raw export and determinism: PASS
- `git rev-list --all --objects` has 0 `.xlsx/.xls/.csv` paths. The export lives in `Downloads/Dispo Game Imports/`, outside the
  repo, and `Imports/` is in `.git/info/exclude`.
- The original commit reproduces byte-identically (md5 `51477c9f…`, matching the handoff). After M1, two runs both give `bf7a376e…`.
  `--check <export>` (dropped-value scan) passes.

## 4. DEC-034 / DEC-048 / DEC-050: PASS after M1
- DEC-034: all 48 sub-categories map to the 8 packaged categories, and Bulk Flower (deli) is skipped because the tool owns it.
- DEC-048: flower pool = prepack/preroll, concentrate pool = vape/extract, and edibles/beverages use the 0.1 g placeholder with
  GAP-COMP-02. Topicals have pool GAP. Infused flower carries a GAP. Pack names give the total weight ("10PK … 3.5G"), so
  `grams = sizeG` is correct for packs.
- DEC-050: FOH holds vapes, gummies/candy and infused prerolls. The fridge holds beverages. The cooler holds extracts and baked goods (read as "perishable edibles", flagged in the handoff). Everything else is GAP.
- **M1 (major, fixed here):** the size and mg regex `\d+(?:\.\d+)?` missed leading-dot sizes. `.5G` parsed as 5 g and `.75G` as 75 g,
  which affected **9 items** (3 dab pens at a 75 g concentrate limit, 15× the 5 g cap, so they could never be sold; 4 rosin systems
  and 2 infused prerolls at 10× their size). The fix is `\d*\.?\d+` in the 4 parse regexes, plus a selftest assert. The re-import changes
  exactly those 9 items, and no single item now exceeds its pool limit. The handoff's md5 is stale: it's now `bf7a376e…`.

## 5. Brand IP: FLAGGED, not yet shipped
- The handoff flags real brand and product names as the open trademark decision (GAP-PKG-07). Nothing references the JSON yet, so it
  is not in any build.
- **n1:** GAME-004 must not reference `packaged_catalog.json` from a scene or Resources until GAP-PKG-07 is decided, or must add
  load-time name masking. Put this in the GAME-004 packet.

## Notes
- n2: two rec edibles/beverages list >100 mg THC (handoff question 5). This is data, so it's left as is; the question goes to Nolan through the Hub.
- n3: `drop()` ignores dropped values shorter than 6 characters in the leak scan. The independent check used 4 characters and found nothing extra.
- Unity load check (optional) not run. The output is plain JSON that parses in Node, and nothing in Unity reads it yet.
