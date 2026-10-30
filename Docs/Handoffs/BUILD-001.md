# Handoff — BUILD-001 (Unity HDRP project + studio wrapper)

**Status:** done, all validation gates pass. Not committed (Hub reviews/commits). Evidence: `Docs/BUILD_STATUS.md`.

## Created
- `UnityProject/` (Unity 6000.6.7f1, HDRP 17.6.0, Input System 1.20.1, Test Framework 1.8.0, AI Navigation 2.0.16).
- `Assets/_Game/{Art,Audio,Code,Data,Prefabs,Scenes,UI,VFX}`, `Assets/ThirdParty/` (`.gitkeep` in empty folders so git keeps them).
- `Assets/_Game/Code/{Domain,Simulation,Presentation,Editor,Tests/EditMode}` with asmdefs; sample test asserts Dispo.Domain references no Unity assembly.
- `Editor/ProjectSetup.cs` (batchmode setup + `VerifyRenderPipeline`), `Editor/CI/StudioCI.cs` (`CompileCheck`, `BuildWindows64`).
- `Presentation/SceneBootstrap.cs`: loads the additive scenes, logs `STUDIO_SMOKE_READY`.
- `Tools/Studio/studio.ps1`: doctor, unity-compile, unity-test-edit, unity-build (includes timed smoke launch + kill), status.
  Results: `Artifacts/Results/<stamp>-<cmd>.json` `{command, ok, exitCode, durationSec, log, summary}`; logs in `Artifacts/Logs/`. Exit 0 ok / 1 fail / 2 blocked (project lockfile held).
- `.gitattributes` (Unity YAML text LF, binaries binary, no LFS); `.gitignore` += `*.slnx`, `.vscode/`, MemoryCaptures, Recordings.

## Commands
```
powershell -NoProfile -ExecutionPolicy Bypass -File Tools/Studio/studio.ps1 <command>
# one-time / re-runnable setup:
Unity.exe -batchmode -nographics -quit -projectPath UnityProject -executeMethod Dispo.Editor.ProjectSetup.Run -logFile ...
```

## Timings (this machine)
create project 76 s · first setup/HDRP import 250 s · compile 56 s · edit tests 39 s · build 6m43s (+smoke ~10 s).

## Notes / issues
- HDRP global settings are created by HDRP's own asset postprocessor during setup (logs a "created for you" warning; expected).
- Log line `[Licensing::Module] Error: Access token is unavailable` appears every run; harmless (entitlement resolves).
- Player log: D3D "GetFrameStatistics is broken" notice; harmless.
- Build uses `-nographics`; worked fine for HDRP shader compilation.
- Lighting_Night is in Build Settings but not loaded at boot (day/night swap is gameplay's job).
- Deviation: result JSON uses the BUILD-001 packet schema, not the fuller TOOLCHAIN §8 schema. No BUILD_MANIFEST yet.
- No flakiness observed (each gate run once).
