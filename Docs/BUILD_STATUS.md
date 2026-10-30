# BUILD STATUS

**Updated:** 2026-10-29 by BUILD-002 · **Unity:** 6000.6.7f1 · **HDRP:** 17.6.0 · **Target:** StandaloneWindows64 (dev)

| Gate | Command | Result | Duration | Evidence |
|---|---|---|---|---|
| Doctor | `studio.ps1 doctor` | pass | 0.5 s | `Artifacts/Results/20261029-211426-doctor.json` |
| Compile + HDRP check | `studio.ps1 unity-compile` | pass, 0 `error CS` | 56 s | `Artifacts/Results/20261029-211428-unity-compile.json`, log line `defaultRenderPipeline=...HDRenderPipelineAsset globalSettings=HDRenderPipelineGlobalSettings` |
| EditMode tests | `studio.ps1 unity-test-edit` | 1/1 passed | 39 s | `Artifacts/TestResults/20261029-211529-editmode.xml` |
| Windows build + smoke | `studio.ps1 unity-build` | exe built (206 MB), smoke ready, no crash | 470 s (build 6m43s) | `Artifacts/Results/20261029-211614-unity-build.json`, `Artifacts/Logs/20261029-211614-player-smoke.log` (`STUDIO_SMOKE_READY scenes=9`, D3D12 on RTX 4050) |

Artifacts/ and Builds/ are gitignored; evidence is local to this machine.

## Project facts
- `UnityProject/` created with `-batchmode -createProject`; settings applied by `Dispo.Editor.ProjectSetup.Run` (idempotent): Linear, Force Text, Visible Meta Files, Input System only, HDRP asset `Assets/Settings/HDRP/HDRenderPipelineAsset.asset` on Graphics + all quality levels. HDRP auto-created `Assets/HDRPDefaultResources/` (global settings + default volume profile).
- Packages added: HDRP 17.6.0, Input System 1.20.1, Test Framework 1.8.0, AI Navigation 2.0.16.
- Assemblies: `Dispo.Domain` (noEngineReferences), `Dispo.Simulation`, `Dispo.Presentation`, `Dispo.Editor`, `Dispo.Domain.Tests` (EditMode).
- Scenes (`Assets/_Game/Scenes`, all in Build Settings, Bootstrap first): Bootstrap loads Retail, BackRooms, Hub, Exterior, GameplaySystems, NPCs, Audio, Lighting_Day additively; Lighting_Night is built but not loaded at boot.

## BUILD-002 re-run (2026-10-29, commit 6f45430)
| Gate | Result | Duration |
|---|---|---|
| `doctor` (fresh worktree, config auto-created) | pass; gitLfs ok; lfsPatterns reported missing until ASSET-002 merges | 2 s |
| `unity-compile` | pass, 0 `error CS` (cold Library) | 280 s |
| `unity-test-edit` / `unity-test-play` | 24/24 · 1/1 | 16 s · 36 s |
| `unity-graybox` / `unity-capture` | pass · 24 shots, QA maxDeviationFt=0.22 PASS | 15 s · 90 s |
| `unity-build` + smoke + manifest | pass, `STUDIO_SMOKE_READY scenes=9`, no crash; `Builds/Windows64-Dev/BUILD_MANIFEST.json` | 480 s |
| `blender deli_jar ...` / `assets-fetch --help` | pass (forwarders) | 43 s · 1 s |

W2C n2 closed: the build re-populates `HDRenderPipelineGlobalSettings.m_RuntimeSettings` in the editor and the player runs clean.

## Not yet covered
Milestone versioning for `Builds/<version>/` (the manifest sits next to the dev exe), known-issues/test-summary fields in the manifest.
