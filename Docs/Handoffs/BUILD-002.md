# Handoff — BUILD-002 (studio tooling hardening + build manifest)

**Status:** done; all validation passes. Branch `claude/task-build-002-65a668`, not merged. Evidence: `Docs/BUILD_STATUS.md` (BUILD-002 table).

## Changed (`Tools/Studio/studio.ps1`, `studio.config.example.json`)
1. Missing `studio.config.json` is copied from the example with a one-line note, for every command (W1 m6).
2. `Wait-UnitySlot`: machine-wide lock `%LOCALAPPDATA%\DispoStudio\unity-slot.lock` held from the editor count until Unity has started (W2C m4).
   Timeout `unitySlotTimeoutMinutes` (default 45) → `status: blocked`, exit 2. Excludes import workers and `unity.exe serve`.
3. New `studio.ps1 blender <generator> [params]` → `Tools/Blender/blender.ps1` (passes `blenderExecutable` as `BLENDER_EXE`).
   New `studio.ps1 assets-fetch [args]` → `python -I Tools/Assets/fetch_assets.py`; blocked (exit 2) if the file is absent.
4. Result JSON adds §8 fields `operation, status (pass|fail|blocked), startedUtc, finishedUtc, commit, worktree, logs, outputs`.
   Old fields `command, ok, exitCode, durationSec, log, summary` are unchanged and `summary` stays a string, so callers and `status` keep working.
5. `unity-build` writes `Builds/Windows64-Dev/BUILD_MANIFEST.json`: version, target, buildDateUtc, commit, dirtyPaths, unityVersion,
   enabled scenes, catalogManifestMd5, assetCacheManifestMd5 (null until ASSET-002 merges), smoke, result path.
6. `doctor`: runs `git lfs install --local` if the repo has no LFS filter; reports `gitLfs` and `lfsPatterns` (DEC-023 ThirdParty patterns).

## Validation (this machine, commit 6f45430)
doctor pass · compile 280 s (cold) · edit 24/24 · play 1/1 · graybox OK · capture 24 shots QA PASS · build 480 s, smoke READY scenes=9, manifest written.
Lock contention and timeout tested: both return blocked, exit 2. `blender deli_jar` and `assets-fetch --help` (ASSET-002 copy, temporary) both exit 0.
W2C n2: the build repopulates `m_RuntimeSettings` in the editor (file shows it; reverted) and the player smoke run is clean.

## Notes / follow-ups
- ASSET-002 (unmerged, 2478f86) owns the LFS `.gitattributes` lines and `fetch_assets.py`; I did not duplicate them.
  With its `.gitattributes` applied, doctor reports `9/9 tracked`. After that merge, make `lfsPatterns` a failing bool check.
- The lock only protects runs of this `studio.ps1`; worktrees on older branches still use the racy gate until they rebase.
- `unity-graybox` regeneration is not byte-identical: it rewrote Retail/BackRooms/Hub/Exterior with no layout change (reverted). ART should know (DEC-029, W2C m1).
- `blender deli_jar` rewrites `Art/Exports/Procedural/manifest.json` with line-ending-only churn (reverted).
