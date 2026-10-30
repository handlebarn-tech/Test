# PERF-001 — Machine performance baseline for the playable slice

**Role:** PERF · **Priority:** P2 · **Branch:** `claude/task-perf-001-dcc05b` worktree off `main` (a245942)

## Goal
A repeatable performance baseline for the vertical slice on this machine (RTX 4050 Laptop 6 GB / 32 GB RAM), so later art (ART-003/004, PROC-002/003) can be checked against budgets.

## Read
`Docs/MACHINE_PROFILE.md` (provisional target), `Docs/TOOLCHAIN_EXECUTION.md` §35–36, `Docs/Tasks/Done/BUILD-003.md`, `SliceBotTests.cs` (bot step), DEC-013.

## Owns
`UnityProject/Assets/_Game/Code/Presentation/Perf/`, the `-perf` hook in `SceneBootstrap.cs`, `enableFrameTimingStats` in ProjectSettings, a `perf` command in `Tools/Studio/studio.ps1`, `Docs/PERF_BASELINE.md`, `Docs/Handoffs/PERF-001.md`.

## Deliverable
1. **Capture path:** dev player arg `-perf <json>`: after Bootstrap loads, a bot plays the slice shift (seed 1, same steps as `SliceBotTests`), with vsync off and runInBackground on; writes JSON (frame time avg/p50/p95/p99/max, 1% low FPS, CPU/GPU frame time, draw calls, batches, SetPass, triangles, vertices, memory, load time, shift result) and quits. Timeout writes `completed:false`.
2. **Runner:** `studio.ps1 perf` launches the existing dev build at 1920×1080 windowed, samples peak VRAM with `nvidia-smi`, writes `Artifacts/Perf/<commit>-<stamp>.json`. No editor, so no DEC-013 slot.
3. **Baseline doc:** `Docs/PERF_BASELINE.md`: budgets vs measured, measured commit, top 3 costs. No optimisation.

## Validation
`unity-compile`, `unity-test-edit`, `unity-build`, `perf` (×2 for repeatability). DEC-013 gate (max 2 Unity.exe, 60 s retry).

## Handoff
`Docs/Handoffs/PERF-001.md` (≤40 lines). Report to the Studio Hub.
