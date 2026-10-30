# REVIEW-W3C — COMP-001 + RES-001 + ASSET-002

**Reviewer:** REVIEW (docs/research) · 2026-10-29 · branch `review/wave-3c` (off `main` c36dc3d)

## Verdict: **PASS with fixes applied** — ready for the Hub to merge to `main`.

No blockers left. Two minor security trims were made in RES-001 (below). The open items are notes for the Hub; none block the merge.

## Merges
`git merge --no-ff` onto `review/wave-3c`, in order: `claude/task-comp-001-c5bcd5` (ca257dc), `claude/task-res-001-6aa95e` (87cf679), `claude/task-asset-002-ed2b8b` (239120e). **No conflicts** (the branches touch disjoint files).

## 1. PII (DEC-006/031): clean
Grepped `OFFICE_FINDINGS.md`, `OFFICE_FILE_LEADS.md` and `Handoffs/RES-001.md`, and the removed lines of the RES-001 history (8bc2cc3 → 32505e5), for:
- emails, phone numbers: **0**
- person names: **0** (every Title-Case pair is a brand, product, paint, folder or business name; "Nolan" is the owner, as in DEC-031)
- personal drive paths: **0** (personal OneDrive segments replaced by "Compliance drive")
- license / permit / registration numbers: **0** (the only number is the RSP architect project number 3378.002.00, which is not a license)
- credentials, security details: no camera layout, alarm, vault, keys or transport

**Fixes on this branch (deletions):**
- `OFFICE_FINDINGS.md` F1: dropped "each with a fixed cash bank" (cash-handling detail, excluded by the file's own header).
- `OFFICE_FILE_LEADS.md` "Never import": dropped the folder location of the credential spreadsheet.

Left in, judged fine: B8 security grille size (a customer-visible door-schedule item, needed for GAP-104); the licensee entity name in a folder path (a business, not a person).
The other branches hold the DEC-023 cache path `C:/Users/handl/...`. That path is already in `DECISIONS.md` on main, so it is not new exposure.

## 2. COMP-001: accurate
I re-fetched eight rows from their primary sources on 2026-10-29:

| Row | Source | Result |
|---|---|---|
| A1/A8 sale cap | azleg.gov 36-2858(A)(1)(c) | ✔ 1 oz per single transaction, ≤ 5 g concentrate |
| B1 age verify | 36-2858(A)(2) | ✔ reasonably verified 21+ with a government photo ID |
| A3 possession / gifting | 36-2852(A)(1),(3) | ✔ |
| A5 medical | 36-2816(A) | ✔ 2.5 oz per rolling 14 days |
| B2 IDs | 4-241(K) | ✔ list matches; under-21 license invalid 30 days after 21st birthday (K paras 1, 3) |
| F1/F2 excise | 42-5452(A),(D) | ✔ 16 %, excluded from the TPT base and local taxes (additive) |
| E2 shapes | 36-2860(A)(2) | ✔ |
| G1 hours | R9-18-308(A)(1)(a) via Cornell LII | ✔ ≥ 30 h/week, 7:00–22:00; LII shows amended 2024-11-01. apps.azsos.gov still returns 403, so OPEN-1 stays |

- **Must-fix list matches DEC-036.** M1 (28.0 g cap), M2 ("21+ ID verified") and M3 (clock range) are all there. DEC-036 narrows M3 to store hours 08:00–22:00 (RES-001 O1), which sits inside the legal window, so there is no conflict. CHANGES.md still says 07:00–22:00 and "pick 14:00". DEC-036 governs. No edit made: the file belongs to COMP.
- **Open ambiguities, still open:**
  - **Phoenix TPT (OPEN-4).** The city's 2025 bulletin and third-party rate tables give 2.8 % city / 9.1 % combined. phoenix.gov's 2026 combined-rate page still titles its charts 8.6 % and 8.3 %, and its PDF link returns 404. Unresolved. Keep 25.1 % (tool authority, DEC-001).
  - **Ounce definition (A4).** Still undefined in statute. 28.0 g is the conservative choice.

## 3. RES-001: consistent
Six findings spot-checked:
1. A1 assortment → DEC-034 ✔
2. P1 nearest-nickel register → DEC-035 ✔ (the card keeps `priceFloor`; GAP-204 in KNOWN_GAPS still says "open with Nolan". Hub to update)
3. O1 hours 8–22 → DEC-036 M3 ✔
4. B4/B8/B14/B17/F1 heights, doors, tile, neon, 12 registers → DEC-037 ✔
5. P3–P5 FTTP V2 → DEC-038 (the game keeps v7.11.4 pricing) ✔
6. B2/B3 A011 sheets → REFERENCES_INDEX §1 ✔, with one note: the index says the plan was built from "A011/A013" while RES-001 says A011/A012 (lighting). Likely a typo in one of the two. Hub/REF to check against the 2026 PDF (REF-004).

The Superseded row (P6) is not cited as current anywhere outside OFFICE_FINDINGS ✔. O4 limits agree with COMP A1 ✔.

## 4. ASSET-002: passes
- `python -I Tools/Assets/fetch_assets.py --verify` → `verify: 249 rows, 0 bad` ✔
- No binaries committed: the diff vs main is only `.md/.json/.py/.gitignore/.gitattributes` ✔
- Sketchfab: all 15 entries in `fetch_list_p0.json` and all 111 Sketchfab rows in the manifest have `redistributable: false` ✔
- `.gitignore` adds `UnityProject/Assets/_LocalThirdParty/` (+ `.meta`), as DEC-023 specifies ✔
- LFS: 9 patterns (png jpg exr hdr fbx glb wav ogg ttf), all under `UnityProject/Assets/_Game/Art/ThirdParty/**`, matching the DEC-023 list exactly ✔
- The ASSET-002 branch brings in ASSET-001 (ledger, acquisition list, handoff) through its own merge d007d1c. Merging W3C therefore also lands ASSET-001. That is expected; I did not re-review ASSET-001 in depth.

## For the Hub
1. Update GAP-204 in KNOWN_GAPS to reflect DEC-035.
2. OPEN-4 (Phoenix TPT): a real receipt's tax lines would settle it (P2 found no numeric rate).
3. A011/A012 vs A011/A013 naming: resolve in REF-004.
4. The COMP CHANGES M3 text (07:00/14:00) is superseded by DEC-036 (08:00–22:00); GAME-002 should follow DEC-036.

Sources: [36-2858](https://www.azleg.gov/ars/36/02858.htm), [36-2852](https://www.azleg.gov/ars/36/02852.htm), [36-2816](https://www.azleg.gov/ars/36/02816.htm), [4-241](https://www.azleg.gov/ars/4/00241.htm), [42-5452](https://www.azleg.gov/ars/42/05452.htm), [36-2860](https://www.azleg.gov/ars/36/02860.htm), [R9-18-308 (LII)](https://www.law.cornell.edu/regulations/arizona/Ariz-Admin-Code-SS-R9-18-308), [Phoenix TPT news](https://www.phoenix.gov/newsroom/finance-news/phoenix-tax-rates-to-see-slight-increase-starting-july-1), [Phoenix combined rates](https://www.phoenix.gov/administration/departments/finance/privilege-sales-use-tax/about-tpt-use-tax/current-combined-tax-rates-phoenix-state-county.html).
