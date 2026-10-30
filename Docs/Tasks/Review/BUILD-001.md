# BUILD-001 — Unity HDRP project + studio wrapper

**Role:** BUILD · **Priority:** P0 · **Branch:** main checkout (first Unity task; no parallel Unity workers)

## Context
`Docs/MACHINE_PROFILE.md`, `Docs/DECISIONS.md` (DEC-003/004), `Docs/TOOLCHAIN_EXECUTION.md` §6–15 and §32, `Docs/MASTER_PLAN.md` §8 (scene list).

## Owns (writes only these)
- `UnityProject/` (new)
- `Tools/Studio/`, `Tools/Unity/`
- `Docs/BUILD_STATUS.md`
- Additions to `.gitignore` if needed

## Deliverable
1. Create `UnityProject/` headlessly with Unity 6000.6.7f1 (`-batchmode -createProject`). `Packages/manifest.json`: HDRP 17.6.0 (built-in), Input System, Test Framework, AI Navigation. Linear color space; HDRP asset + HDRP global settings created and assigned by a batchmode editor script (no GUI wizard). Force Text serialization, Visible Meta Files.
2. Folders `Assets/_Game/{Art,Audio,Code,Data,Prefabs,Scenes,UI,VFX}`, `Assets/ThirdParty/`.
3. Assembly definitions: `Dispo.Domain` (pure C#, `noEngineReferences: true`), `Dispo.Simulation`, `Dispo.Presentation`, `Dispo.Editor`, and `Dispo.Domain.Tests` (EditMode) with one passing sample test.
4. Additive scene skeleton per MASTER_PLAN §8 (`Bootstrap`, `Retail`, `BackRooms`, `Hub`, `Exterior`, `GameplaySystems`, `NPCs`, `Audio`, `Lighting_Day`, `Lighting_Night`) created by an editor script, all in Build Settings; Bootstrap loads the others additively at runtime.
5. `Tools/Studio/studio.ps1` (Windows PowerShell 5.1 compatible) with `doctor`, `unity-compile`, `unity-test-edit`, `unity-build` (Windows standalone dev build to `Builds/`), `status`. Reads `Tools/Studio/studio.config.json` (example committed). Every command logs to `Artifacts/Logs/` and writes a JSON result `{command, ok, exitCode, durationSec, log, summary}`.
6. `Docs/BUILD_STATUS.md` with the evidence.

## Validation (evidence required)
- `studio.ps1 unity-compile` → ok, 0 errors.
- `studio.ps1 unity-test-edit` → sample test passes (NUnit XML in Artifacts).
- `studio.ps1 unity-build` → exe produced; launch once briefly (timed run, then kill) and record that it starts without crashing (check Player.log).
- Editor script confirms `GraphicsSettings.defaultRenderPipeline` is an HDRP asset.
- Never run two Unity instances on the same project at once.

## Handoff
`Docs/Handoffs/BUILD-001.md` (≤40 lines): commands, timings, issues, flakiness.
