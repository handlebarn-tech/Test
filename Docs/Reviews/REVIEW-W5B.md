# REVIEW-W5B — DOC-004: processed imports archived (DEC-070) + importer fallback

**Verdict: PASS (GO)**, with one ID clash for the Hub. Branch `review/wave-5b` (off `main` 33e57a1) merges `claude/task-doc-004` @ 66f8602 cleanly. Reviewer: UX-002 workcell session, 2026-10-30.

## Old-path references
A repo-wide grep for `Dispo Game Imports` (not followed by `Archive`), `DISPO_GAME_DESIGN_V2/` and the export file name finds:
- **Annotated in place, original text kept** + "(archived 2026-10-30 to `…Imports Archive/2026-10-30_<name>/`, DEC-070)": DESIGN_V2 README_FIRST provenance, IMP-001 audit, REVIEW-IMP1, REVIEW-W4O, DATA-002 handoff and packet, IMP-001 and IMP-002 packets. ✔
- **Deliberately kept:** DECISIONS (DEC-069 history). ✔
- **Correctly pointing at the live folder as "fresh imports only":** the importer's `DROP_DIR` comment, HUB_RESUME's DEC-070 rule, and PROJECT_STATE lines 34/37/38 (where future imports land). ✔
- **Stale, Hub-owned (not edited, as the packet requires):** PROJECT_STATE line 35 still gives the V2 pack's location as `Downloads/Dispo Game Imports/DISPO_GAME_DESIGN_V2/`. The handoff flags it; the Hub should update it.
- The archive exists (`2026-10-30_DISPO_GAME_DESIGN_V2/`, `2026-10-30_dutchie-inventory/` holding the single export). The Imports folder now holds only a fresh `blender_proc_vNext/` (DEC-069 toolkit, not a DOC-004 item) and no `.xlsx`.

## Importer fallback (`Tools/Data/import_packaged.js`)
- **Logic:** default export = exactly one `.xlsx` in `Imports/` (fresh); only if there are **none** does it fall back to the archived `2026-10-30_dutchie-inventory/`. With 2+ fresh files it errors, and the message names the folder it searched. A passed path still wins. The fallback changes only which file is picked; `load()` → the column `WHITELIST` → `build()` → `guard()` (PII patterns + dropped-column leak scan) run unchanged on every path. ✔
- **Wrong-file probes** (scratch copy of the tool with `DROP_DIR` pointed at a temp folder; the live Imports folder was not written to, DEC-070):
  - a stray non-zip `stray.xlsx` → `not an .xlsx (zip) file`. It fails loudly and does **not** silently fall back to the archive.
  - two `.xlsx` files → `pass the export path, or put exactly one .xlsx … (found 2 …)`.
  - A real `.xlsx` that isn't a Dutchie export fails at `export is missing whitelisted column(s)` (code path read, not run). ✔
- **Runs on the merged branch:**
  - `node Tools/Data/import_packaged.js --selftest` → `selftest OK`.
  - `--check <archived export>` → `guard OK: packaged_catalog.json (954 items, dropped-value scan on)`: the md5 matches the one the catalog was built from.
  - The default run with no argument resolved the archive, and `packaged_catalog.json` is **byte-identical** (git shows no change; counts 954 items, priceConflicts 0). ✔
- **n1:** `ARCHIVE_DIR` hard-codes the 2026-10-30 folder. That's fine for the one export DATA-002 was built from; a future re-import should pass its path or land fresh in `Imports/`.

## Hub items
- **ID clash:** `DOC-004` is already in BACKLOG on `main` (row 91, "fast recommendation" in GSS §28, added by DOC-003/REVIEW-W4Z). This housekeeping task needs another ID (e.g. DOC-005, or OPS-xxx) in BACKLOG and its handoff filename. The handoff says so too; renaming is the Hub's call.
- Update PROJECT_STATE line 35 to the archive path.
