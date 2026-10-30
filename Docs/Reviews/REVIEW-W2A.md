# REVIEW-W2A — GAME-001 + PROC-001 independent review

**Reviewer:** REVIEW specialist · **Date:** 2026-10-29 · **Branch:** `review/wave-2a` = `main` @ d2504fd + `--no-ff` merges of `claude/task-game-001-b68d0f` (f29ba6b) and `claude/task-proc-001-38ca78` (565befe). Both merged with no conflicts.

## Verdict: **GO with notes**

No blockers or majors. Every gate re-ran green on the merged branch, importer and Blender outputs are byte-deterministic (also on a fresh autocrlf checkout), and six spot-checked functions match their v7.11.4 source lines. The minor notes below do not block the merge.

## Gates re-run on the merged branch

| Check | Result |
|---|---|
| `studio.ps1 doctor` | pass (all checks) |
| `studio.ps1 unity-compile` | pass: `csErrors=0; CompileCheck OK` (cold import, 213 s) |
| `studio.ps1 unity-test-edit` | **24/24 passed** (`Artifacts/TestResults/20261029-215708-editmode.xml`) |
| `import_catalog.js` ×2 | identical md5s, equal to `manifest.json` (manifest `f6c7e56d…`, batches `6fdc5535…`); `git status` clean after regen |
| `import_catalog.js --check` | `allow-list OK`, exit 0 |
| Fresh clone checkout (`core.autocrlf=true`) | catalog md5s match manifest; FBX md5s match regenerated outputs |
| PII (DEC-006) | batch keys = exactly DATA_SCHEMA §5 (`id, strainName, batchCode, brand, tier, inStock, testDate, dateInferred, total, terpenes`); ids are `custom_<ts>_<rand>`; no emails / employee / customer / phone / user fields in any catalog file |
| `Dispo.Domain` | `noEngineReferences: true`, `references: []`, no `using Unity*` |
| REVIEW-W1 M1 / DEC-017 | RC-04 and RC-11 are in `SliceCases` and replay the recorded `parsed` crit/neg/primary from `golden_cases.json` |
| PROC generators ×2 (deli_jar, package_box, package_pouch) | all three FBX byte-identical across runs and to the committed files; manifest content identical (see m3) |
| Tri budgets | jar 442/800 · 122/200; box 88/300 · 24/60; pouch 476/500 · 116/120 — all within |
| Sizes / location | FBX 29–49 KB, contact sheet 607 KB (≤1 MB); nothing from PROC under `UnityProject/` |
| Hygiene | no secrets, no tfs-budtender files copied in (43 files added vs main, none from the source tree), only importer output |

## Source spot-checks (v7.11.4 `index.html`, md5 `228684e9…`, read-only)
1. `getTierW` L15041: thresholds .20/.05/.01 → 1.00/.25/.02 — match.
2. `NF` L15121 = 2.7765 — match.
3. `getBaScalar` L15138: BA_SCALARS, else missing → 0.55, sesqui 0.46 / else 0.55 — match.
4. `classifyCluster` L15202: priority `[4,5,6,2,3,1]`, Cl.4 myrcene tiebreakers (≥0.80 & >3×apin; apin<0.20 & >3× & ≥0.50) — match.
5. `calcAnxietyRisk` L15288: base 50, anxiolytic caps 30/25/12/10/10 with factors 80/30/60/70/8 — match.
6. (bonus) `findStrains` L15385-15393 primary ×1.5, neg penalty `(actual/limit)×0.25` when both >0; `respond` L16639-16640 fallback `floor(v×.60)`, `min(99, v+12)` — match.

## Findings

### Blocker
None.

### Major
None.

### Minor
- **m1 (GAME-001).** Packet asks for "constants in data or config, not scattered literals". Scalars are centralized in `EngineConstants` with line cites, but cluster thresholds (`Scoring.Chk`) and `calcAnxietyRisk` coefficients stay inline. Justified (they are code in the source too, and cited), acceptable for the slice; move to a table if they ever need tuning.
- **m2 (GAME-001).** `batches.json` carries real brand names (Dr Green Thumb, Cookies, Alien Labs, …). Allowed by §5 and not PII, but shipping real trademarks in a game is a separate IP/legal question for the Hub before any public build.
- **m3 (PROC-001).** On Windows (`core.autocrlf=true`) the checked-out `Art/Exports/Procedural/manifest.json` is CRLF, the generator writes LF, so a rerun shows the file as modified with an empty diff. Harmless; fix with `Art/Exports/**/manifest.json text eol=lf` in `.gitattributes` (PROC/Hub).
- **m4 (setup).** A fresh worktree has no `Tools/Studio/studio.config.json` (gitignored), so `studio.ps1` throws until one is copied in. Known friction; worth one line in HUB_RESUME or the packet template.

## Doc changes on this branch
- `Docs/KNOWN_GAPS.md`: registered GAP-PROC-01…06 from `PROC_PIPELINE.md`.

### Note m5 (wave-1 project, not these branches)
Every batchmode `unity-compile` rewrites `Assets/HDRPDefaultResources/HDRenderPipelineGlobalSettings.asset`, emptying `m_RuntimeSettings.m_List` (20 rids → `[]`). Reverted here, not committed. Workers running Unity will keep seeing this dirty file; BUILD/ART should decide whether the committed list or the batchmode result is canonical and commit that once.
