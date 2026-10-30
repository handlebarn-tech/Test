# REVIEW-W4M — ART-005 (REVIEW-W4F m1/m2/n1, Retail_Lookdev at boot, capture folder suffix)

**Verdict: PASS.** Branch `review/wave-4m` = `main` (79fdfc9) + a `--no-ff` merge of `claude/task-art-005` (08425eb). The merge was clean with no conflicts. I made no code or data changes.

## 1. Validation (this worktree, DEC-013 gate via studio.ps1)
| Check | Result |
|---|---|
| unity-graybox ×2 | both `unchangedScenes=4 lookdev unchanged`; `git status` clean after each |
| **Forced rebuild** (`-grayboxForce`, run directly) | `walls=19 fixtures=74 cameras=23 anchors=137; lookdev lights=69 millwork=12 panels=7`. All 5 scenes are **content-identical** to the committed ones (YAML blocks compared with fileIDs masked: Retail 1022, BackRooms 274, Hub 173, Exterior 49, Retail_Lookdev 578 blocks, 0 differ). Reverted afterwards. |
| unity-compile | OK, 0 CS errors |
| unity-test-edit | 163/163 |
| unity-test-play | 8 passed, 1 skipped (GAME's opt-in `Capture_EachScreen`). Includes the new `NoAccentPanel_CoversARetailCamera`, `TiHeights_…` (34" top), the anchor tests and the slice bot (12/12, $265.20, Kush Cake sold out, 0 fallbacks) |
| unity-build smoke | `STUDIO_SMOKE_READY scenes=11`, no crash, no early exit; the player log shows the slice ready (77 jars) with **no** TEMP-fallback warning, so loading Retail_Lookdev at boot does not break the name-based anchor lookup |
| unity-capture | 24 shots, QA 23 views, **max 0.22 ft ≤ 0.5, PASS**; slice capture passed (10 shots). Output `Artifacts/Screenshots/80bf0a8` |
| unity-capture again, same commit | wrote `Artifacts/Screenshots/80bf0a8-20261030-021221-662-30460`; the first folder was kept (Hub d works) |

## 2. Deliverables
- **m1, 2" top:** `millwork.top` 0.167 ft, and the note cites A940 detail 11 (1½" edge = detail 12 / 4D). The 34" finished height still holds (`TiHeights` test). PASS.
- **m2, R2C3:** `PanelRects` drops any CLG-1 panel within `cameraClear` (1 ft) of a Retail camera, and downlights follow the real panel list (7 panels, was 8). `REF_R2C3_Retail` now shows the register run and deli wall with no panel in front. PASS.
- **n1:** the 8 `Â§` sequences are now `§`, and the JSON is clean UTF-8. PASS.
- **Hub a:** `Retail_Lookdev` is second in `SceneBootstrap.AdditiveScenes`. Retail_Lookdev has no `Anchor_*`/`Interact_*` objects (0 found), so it cannot shadow GAME's `GameObject.Find` lookups. PASS.
- **Hub d:** one line in `studio.ps1` adds a `-<stamp>` suffix when the commit folder already exists. Verified above. PASS.
- **Hub c (fonts):** correctly not fetched (ASSET task). Still **[NEEDS-ASSET]**.

## 3. DEC-029 — PASS
ART-005 changes only `Retail_Lookdev.unity` among the scenes. The 14.7k-line scene diff is a full regeneration: random fileIDs plus about 20 fewer objects (panel 0_2, its cables, and the downlight changes). The forced rebuild proves the committed scene is exactly what the builder outputs. `SceneBootstrap` and `studio.ps1` are the two Hub-approved out-of-lane lines in the packet.

## Notes (none block)
- n1 **Test is looser than the builder.** `NoAccentPanel_CoversARetailCamera` checks only that no camera sits inside a panel's footprint, while the builder enforces 1 ft of clearance. A future grid change could put a panel 0.5 ft from a camera and still pass. ART: assert with `cameraClear` grown bounds when next in this file.
- n2 **Leftover indent.** The `foreach (var (j, i, r) in panelRects)` body in `LookdevBuilder` keeps the old double-loop indentation and braces. Cosmetic only.
- n3 **LFS checkout gap (environment, not ART-005).** In this worktree the two `oak_veneer_05` JPGs were left as LFS pointers. Any editor run then imports no texture and saves `LD_WD1_Walnut.mat` with `_MainTex` = fileID 0 and without `_NORMALMAP`. GAME-005's handoff reported the same churn. `git lfs checkout` fixed it here, and the tree stayed clean afterwards. Hub/BUILD: new worktrees should run `git lfs checkout`, or `studio.ps1 doctor` should flag pointer files under `_Game/Art`. Otherwise a worker can commit the broken material.
- n4 Each build still dirties `HDRPDefaultResources/HDRenderPipelineGlobalSettings.asset` (ART-005 reported this too). I reverted it and did not commit it.

## For the Hub
1. Merge `review/wave-4m`.
2. Consider a BUILD follow-up for n3 (LFS pointer check in `doctor`, or `git lfs checkout` in worktree setup).
3. Fonts remain [NEEDS-ASSET]. W4F n2 (exposure vs photos) is still open.
