# REVIEW-W3A — GAME-003 parser port + BUILD-002 tooling

**Reviewer:** REVIEW specialist · **Date:** 2026-10-29 · **Branch:** `review/wave-3a` = `main` (0f9db68) + `--no-ff` merge of `claude/task-game-003-738ff2` (6ea6411, d164121) + `--no-ff` merge of `claude/task-build-002-65a668` (c918124, 34093e0). Both merges were clean with no conflicts. Neither branch was based on the current `main`, so these results come from the merged tree.

## Verdict: **GO with notes**

There are no blockers. Every gate in the packet re-ran green on the merged tree. Seven ported functions match v7.11.4 line by line. The notes below are follow-ups. One of them, n1, should be fixed before GAME-002 merges.

## Gates (this machine, merged tree)
| Command | Result |
|---|---|
| `unity-compile` | CompileCheck OK, csErrors=0 (44 s) |
| `unity-test-edit` | **123/123 passed** (`Artifacts/TestResults/20261029-224334-editmode.xml`) |
| `doctor` | pass. `gitLfs True`. `lfsPatterns` reports "missing … (ASSET-002 adds them)", as designed |
| `status` | pass |
| `blender deli_jar Tools/Blender/params/deli_jar.json` | pass, exit 0. It also rewrote `Art/Exports/Procedural/manifest.json` with line-ending-only churn, which I reverted (the BUILD-002 handoff mentions this) |
| `assets-fetch --help` | `blocked`, exit 2, "Tools/Assets/fetch_assets.py not present on this branch" (correct before ASSET-002) |
| `unity-build` | pass in 514 s. Smoke `STUDIO_SMOKE_READY scenes=9`, exitedEarly=False, crash=False. The HDRP `m_RuntimeSettings` editor rewrite was reverted (W2C n2) |

## Checks
### 1. GAME-003
- **Tests:** The XML lists `Mig001_FromRawQuery` 39/39, `Game003_ParserCoverage_V7114` 54/54, `Defect_V7114AndGameExpected` 2/2 (MC-7 and GAP-206), `EngineFeatureTests` 4/4 and the GAME-001 fixtures 24/24. The total is 123.
- **DEC-016 double goldens:** Present. `golden_game003.js` checks that the tool page's md5 matches the pinned v7.11.4 (`228684e9…`). It patches each fix as a single source line, after confirming the original text is on that line. It runs both pages in a temp directory and deletes the directory afterwards. So the game-expected values come from running the tool, not from hand-written numbers.
- **Spot-check against the read-only `deploy/2026-10-30-v7114/site/index.html`.** All seven match.
  1. `findStrains` L15355–15413. The filter order is stock → tier → exclusions → crit/neg → maxAnx → exclude → maxPrice. `maxPrice` uses the cheapest post-tax price with a +0.01 margin. The like-X cosine is added after the tier nudge.
  2. `_extractExclusions` L15979. The alias table is built as `bcp` + `_EXCL_FAMILY` + DB aliases, sorted longest first with a stable sort. Both list regexes match, as do the `w/o` and isomer-space rewrites and the family name losing its trailing `s`.
  3. `_findStrainMentions` L15916 and `_strainNameIndex` L15908. Names are kept only if they have at least 3 characters, sorted longest first with a stable sort. The matched span is blanked with spaces.
  4. `_fuzzyStrainMentions` and `_lev` L15930–15954. The tolerance is 2/1/0 by name length, the window is w±1, a tie aborts, and there are 3 rounds.
  5. `slCosineSim` L20813. It uses the union of keys in the same order and returns 0 when either norm is 0.
  6. `detectPriceIntent` L21744. The order is noPrice → hasBudget (last digit group, 0 < amt < 10000) → budget. A digit run too long to parse is skipped, which is also what the JS does.
  7. `REFINE`/`refineSearch` L19583. All 11 chips, the `_mx`/`_mn` semantics and `moreBody`'s 55 floor match.
- **`Dispo.Domain`** is still `noEngineReferences: true` with `references: []`.
- **DEC-028 boundary:** `Catalog.Groups()` caching, label code and rep-batch fields are unchanged. `Catalog.cs` only adds `Terpene.Aliases`, `Parser`, `Group(key)` with its own `_byKey` cache, and the `parserJson` optional parameter. Existing GAME-001 signatures are kept by overloads. See n1.

### 2. BUILD-002
- **Same arguments:** `doctor`, `status`, `unity-compile` and `unity-test-edit` take the same arguments as before. The result JSON keeps `command, ok, exitCode, durationSec, log, summary`, with `summary` still a string, and adds the §8 fields `operation, status, startedUtc, finishedUtc, commit, worktree, logs, outputs`. Spot-checked in the results above.
- **Missing config:** I moved `studio.config.json` away and ran `doctor`. It printed the "Created … from studio.config.example.json" note, copied the file byte-identical to the example, and the doctor passed. I then restored the original.
- **Lock timeout:** I held `%LOCALAPPDATA%\DispoStudio\unity-slot.lock` and set `unitySlotTimeoutMinutes` to 0.2. `unity-compile` waited 3 × 5 s, then returned `status: blocked` with "slot wait timed out after 0.2 min" and exit 2. The config was restored.
- **Two concurrent invocations (same worktree):**
  - Started 3 s apart: B waited on the lock, then waited for the 2-editor count. A ran, then B ran. Both passed, so launches are serialized as intended.
  - Started in the same second: B crashed. See n2.
- **`BUILD_MANIFEST.json`:** It was written next to the exe with version `Windows64-Dev-34093e0`, the full commit, unityVersion 6000.6.7f1, the 10 enabled scenes, `catalogManifestMd5 bdb16559…`, `assetCacheManifestMd5 null` (ASSET-002 has not merged), the smoke string and the result path. `dirtyPaths` was 2: this review file and the HDRP asset rewrite. The `catalogManifestMd5` file is `eol=lf`, so the working-tree md5 equals the committed bytes, as the comment claims.

### 3. Hygiene
I grepped the diff for secrets, tokens, e-mails and phone numbers and found none. No tfs-budtender files are copied in. `parser_tables.json` holds only the tool's regex source and the domain values. `golden_cases_game003.json` holds synthetic queries and strain names. `golden_game003.js` copies the inventory into an OS temp directory and deletes it. No `.html` or inventory files are tracked.

## Findings
### Blocker / Major
None.

### Minor
- **n1. Stale per-catalog caches (fix before or in GAME-002's merge).** `Catalog._byKey`, `QueryParser.NameCache` and `QueryParser.ExclCache` are built once per `Catalog` and never cleared. The tool rebuilds `_strainNameIndex` whenever `_strainGroupsCache` changes. Once GAME-002's `SetInStock` (DEC-028 S1) resets `_groups`, all three caches must be reset as well. The handoff names only `_byKey`. The static dictionaries also hold every `Catalog` ever loaded, which matters only if catalogs get reloaded. `ConditionalWeakTable` or an instance field would fix that.
- **n2. Same-second runs collide.** `$Stamp` has one-second resolution. Two commands of the same kind started in the same second in one worktree share a log file, because Unity's `-logFile` holds the file open. The second run then dies in `Write-Line` with exit 1 and writes no result JSON. Separate worktrees are unaffected, since each has its own `Artifacts/`. A fix is to add milliseconds or the PID to `$Stamp`.
- **n3. The project-lock check runs once, before the slot wait.** A second run on the same worktree that passes `Test-ProjectLocked` while the first is still waiting can later launch a second editor on the same project. Unity then refuses the project, and the result is `fail` instead of `blocked`. A fix is to re-check `Test-ProjectLocked` after taking the slot lock. I did not reproduce this; it is narrow in practice.
- **n4. `doctor` changes shared git config.** `git lfs install --local` writes to the common `.git/config` and hooks, which every worktree shares, so this is a repo-wide change and not one tied to a worktree. This matches DEC-023 and the change is harmless. It is noted so the Hub knows `doctor` is no longer read-only.
- **n5. Name/value mismatch.** `BUILD_MANIFEST.json`'s `dirtyPaths` is a count, not a list of paths. It could be renamed `dirtyPathCount`, or the paths could be listed.
- **n6. Carried from the handoff:** ASSET-002 must merge before `lfsPatterns` becomes a failing check. `unity-graybox` scene churn is still not deterministic (W2C m1).

## Hub decisions requested (from the GAME-003 handoff; I recommend all three)
1. NPC parsing uses `ParserOptions.Game` (MC-7 and GAP-206 on). The tests keep `V7114` parity.
2. Parser tables and terpene aliases come only from importer ≥1.1.0, under DEC-014.
3. `golden_cases_game003.json` is regenerated by `golden_game003.js` in the same change as any re-import.
- Errata: PHRASE_MAP has 46 entries, not 54 (RECONSTRUCTION_CONTRACT §2 item 8).
- The quirk where "sativa" fuzzy-matches "Za Tiva" is kept for parity. GAME-002 NPC lines should avoid bare "sativa"/"indica" words.
