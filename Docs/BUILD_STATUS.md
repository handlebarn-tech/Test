# BUILD STATUS

**Updated:** 2026-10-29 by BUILD-001 · **Unity:** 6000.6.7f1 · **HDRP:** 17.6.0 · **Target:** StandaloneWindows64 (dev)

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

## Not yet covered
`unity-test-play`, build manifest (TOOLCHAIN §14), screenshot capture.
