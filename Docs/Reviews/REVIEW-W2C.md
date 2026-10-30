# REVIEW-W2C — ART-001 graybox + QA harness

**Reviewer:** REVIEW specialist · **Date:** 2026-10-29 · **Branch:** `review/wave-2c` = `main` + `--no-ff` merge of `claude/task-art-001-e39b67` (79246a5), plus the ProjectSettings commit f8fdfb0. Fresh worktree, cold Library.

## Verdict: **GO with notes**

There are no blockers. All six gates re-ran green on a fresh checkout, the overlay reproduces at 0.22 ft, and the transcription matches REFERENCES_INDEX. The notes are follow-ups and do not block the merge.

## Gates (this machine, fresh worktree)
| Command | Result |
|---|---|
| `doctor` | all checks passed |
| `unity-graybox` | Build OK walls=19 fixtures=35 cameras=23, csErrors=0 (includes the cold import, about 3 min) |
| `unity-compile` | CompileCheck OK, csErrors=0 |
| `unity-test-edit` | 1/1 passed |
| `unity-test-play` | 1/1 passed (Retail → east arch → vestibule → BOH, no fall) |
| `unity-capture` | 23 REF views + top-down; QA `maxDeviationFt=0.22 missing=0 tolerance=0.5 PASS` (`Artifacts/Screenshots/79246a5/`) |

The DEC-013 gate was not triggered: fewer than 2 editors were running whenever this review launched Unity.

## Checks
1. **Gates:** all pass (see the table above).
2. **Overlay:** I inspected `overlay_topdown.png` by eye. Walls, openings and fixtures sit on the plan's gaps and fills, and nothing is visibly off. The numbers match the worker's: interior walls are ≤0.12 ft off, and the outline is 0.13–0.22 ft off (the plan's outline stroke). Four rooms spot-checked in `graybox_layout.json` against REFERENCES_INDEX §1.3 match exactly: Retail 0–47.19 × 0–29.0, Restroom 0–8.0 × 29.5–36.1, Break Room 14.10–23.31 × 29.5–46.3, HUB 2 28.70–47.19 × 46.8–76.03. FOH, BOH and the vestibule also match. The interior doors are 3'-0" wide, centred on the drawn symbols (Office→HUB, Hall→Office, Hall→Restroom and HUB→HUB 2 all checked).
3. **GAP tags / no invention:** All 12 placeholder heights carry a GAP id, and the builder puts it in every object name (`[h=…ft GAP-…]`, `[opening … GAP-…]`). The HUB/HUB 2 fixtures (GAP-110) and the HUB cameras (GAP-105) are all Low, which satisfies DEC-018. The JC is Low (GAP-103/109) and the exterior cameras are Low guesses. **GAP-104 now records the vestibule-door fact** (`Docs/KNOWN_GAPS.md`).
4. **`studio.ps1`:** `Wait-UnitySlot` runs inside `Assert-UnityReady`, so every Unity command honours it. It excludes AssetImportWorker processes. `doctor`/`status` don't call it, and existing commands still pass. The EditMode/PlayMode switch keeps the old `-editmode.xml` name.
5. **ProjectSettings (decided: commit):** Committed as f8fdfb0 "BUILD: commit HDRP-normalized ProjectSettings". These are the values Unity 6000.6.7f1 + HDRP writes on every open, so committing them stops the dirty files in every worktree.
   - `GraphicsSettings` `m_LightsUseLinearIntensity`/`m_LightsUseColorTemperature` 0→1: HDRP requires both and forces them at runtime. No behaviour change.
   - `QualitySettings` Ultra (the current level) `lodBias` 2→1: HDRP cameras take their LOD bias from the HDRP frame settings, and there are no LODGroups yet. No visible change today. If a future task relies on `QualitySettings.lodBias`, it is now 1.
   - `HDRenderPipelineGlobalSettings` `m_RuntimeSettings.m_List` emptied: the editor rewrites it on open, and I take it to be refilled for player builds. **Not verified by a `unity-build` in this review** (see n2).
6. **Hygiene:** no file over 10 MB; no Library/Temp/UserSettings/Logs tracked; no PII in the diff.

## Findings
### Blocker / Major
None.

### Minor
- **m1. Non-deterministic scene rebuild.** Each `unity-graybox` run rewrites all four scenes (about 4.3k lines of diff) with new fileIDs and no content change. The scenes were reverted here. **Rule for ART-*: commit scene files only when `graybox_layout.json` or the builder changed.** A stable-fileID builder is optional later.
- **m2. Queue lanes are `Low` with no position GAP id** (only the GAP-002 height). REVIEW-W1 m3 found that the stanchions are vector in the plan, so Med is justified. Left for REF/ART; harmless.
- **m3. Overlay coverage:** `graybox_qa.py` samples 12 interior walls + 8 outline edges. The vestibule walls and the Office band wall at the Hall are not sampled; the eye check covers them.
- **m4. `Wait-UnitySlot` has no timeout, and the gate is check-then-launch.** Two scripts can both see 1 editor and start together. This is acceptable for the 2-editor policy at the studio's scale.

### Nits
- n1. `Graybox_TempSun` lives in Exterior until Lighting_Day is populated (already flagged by the worker).
- n2. The next BUILD task's `unity-build` should confirm that the player build is unaffected by the emptied `m_RuntimeSettings` list.

## Files touched by the reviewer
`Docs/Reviews/REVIEW-W2C.md` (new), `Docs/KNOWN_GAPS.md` (GAP-104 row), the three ProjectSettings/HDRP files (f8fdfb0).
