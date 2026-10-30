# PERF BASELINE

**Task:** PERF-001 · **Measured:** 2026-10-29 · **Build commit:** `a245942` (main) + the PERF-001 capture hook only (no content change).
**Not included:** ART-003/004 lookdev, PROC-002 fill meshes in the slice (GAME-005), PROC-003. Re-measure after each merges.

## How to reproduce
```
studio.ps1 unity-build   # dev player -> Builds/Windows64-Dev/
studio.ps1 perf          # -> Artifacts/Perf/<commit>-<stamp>.json + Artifacts/Results/<stamp>-perf.json
```
`perf` runs the dev player windowed at 1920×1080 with `-perf <json>`: after Bootstrap loads all 9 additive scenes, a bot plays the
seed-1 shift (same steps as `SliceBotTests`) at timeScale 20, vsync off, and the player quits after writing the JSON. The first 60
frames are skipped. Render/memory numbers come from `ProfilerRecorder` (dev build only); CPU/GPU frame time from `FrameTimingManager`
(`enableFrameTimingStats` is now on); VRAM peak from `nvidia-smi` (whole GPU, so an upper bound). No editor, so no DEC-013 slot.

## Machine
RTX 4050 Laptop 6 GB (D3D12), Core Ultra 9 185H, 32 GB RAM, Unity 6000.6.7f1 HDRP, quality level **Ultra**. 2–3 other Unity editors
(other sessions) were running during both runs, so frame time is noisy.

## Budgets vs measured (2 runs)
| Metric | Budget | Run 1 | Run 2 | Status |
|---|---|---|---|---|
| Frame time avg | ≤ 16.7 ms (60 FPS) | 9.37 ms | 7.34 ms | OK |
| Frame time p95 | ≤ 16.7 ms | 12.9 ms | 10.7 ms | OK |
| Frame time p99 | ≤ 33.3 ms (30 FPS floor) | 33.3 ms | 23.5 ms | borderline |
| 1% low FPS | ≥ 30 *(proposed)* | 13.7 | 23.6 | **FAIL** |
| Max frame | — | 294 ms | 148 ms | hitches |
| CPU frame avg / p95 | ≤ 12 ms *(proposed)* | 9.3 / 12.8 | 7.3 / — | OK, but CPU-bound |
| GPU frame avg / p95 | ≤ 12 ms *(proposed)* | 5.9 / 8.8 | 5.6 / — | OK |
| Draw calls avg / max | ≤ 2000 *(proposed)* | 138 / 272 | 138 / 272 | OK |
| SetPass avg / max | ≤ 300 *(proposed)* | 37 / 72 | 37 / 72 | OK |
| Batches | — | 0 | 0 | not reported under HDRP/SRP Batcher |
| Triangles avg / max | ≤ 3 M *(proposed)* | 10.7 k / 20.3 k | 10.6 k / 20.3 k | OK (counter likely undercounts SRP passes) |
| Gfx memory (Unity) max | ≤ 3.5 GB *(proposed)* | 782 MB | 782 MB | OK |
| VRAM peak (nvidia-smi, whole GPU) | ≤ 5 GB (MACHINE_PROFILE) | 802 MB | 803 MB | OK |
| Total reserved memory max | — | 1.62 GB | 1.62 GB | OK |
| RAM (game) | ≤ 12 GB editor+game | ~1.6 GB reserved | same | OK |
| Load (process start → all scenes loaded) | ≤ 15 s *(proposed)* | 5.2 s | 5.3 s | OK |
| Shift result | 12/12 served | served=12, 0 walkouts, $265.20, 3★ | same | deterministic |

Budgets marked *proposed* are PERF-001's suggestion; the Hub should confirm them (they replace "provisional" in MACHINE_PROFILE).
Counts and memory repeat exactly between runs; frame-time numbers vary ~25 % with machine load, so compare averages of ≥2 runs.

## Top 3 costs (flagged, not optimised)
1. **Frame hitches.** p99 23–33 ms, max 148–294 ms, 1% low 14–24 FPS: the only metric below target. Not yet profiled. Suspects: NPC
   spawn via `GameObject.CreatePrimitive` + `Destroy` per customer, UI Toolkit screen rebuilds on `Show()`, GC, and timeScale 20
   multiplying per-frame sim/NPC work; contention with the other editors also contributes. Next step: Profiler deep capture of the
   `-perf` run.
2. **CPU-bound, not GPU-bound.** CPU 7–9 ms vs GPU 5.6–5.9 ms on an almost empty graybox: HDRP's fixed per-frame CPU render cost
   dominates. Lookdev will add GPU cost, but the CPU side is the first ceiling.
3. **HDRP memory floor.** ~0.8 GB VRAM and 1.6 GB reserved RAM before any real art (1080p Ultra render targets, HDRP resources).
   Art has ~4.2 GB of the 5 GB VRAM ceiling left; check that after ART-003/004 and PROC jars land.

## Re-measure 2026-10-30 (REVIEW-W4J): lookdev build + re-run of the a245942 build
`7ee9ae0` = main b52c60b (ART-003/004 lookdev, W4F) + PERF-001. Three `studio.ps1 perf` runs with 1, 2 and 2 other editors open.
`a245942 (re-run)` = PERF-001's own player, re-run once with **0** other editors and once with **2**.

| Metric | a245942 PERF-001 (2–3 editors) | a245942 re-run: 0 editors / 2 editors | 7ee9ae0 lookdev, 3 runs |
|---|---|---|---|
| Frame time avg | 7.3–9.4 ms | 6.19 / 6.16 ms | 5.8–6.2 ms |
| Frame time p95 | 10.7–12.9 ms | 8.8 / 8.4 ms | 7.9–9.0 ms |
| Frame time p99 | 23.5–33.3 ms | 18.3 / 18.0 ms | 16.8–17.8 ms |
| 1% low FPS | 13.7–23.6 | **41.5** / 23.4 | 23.4 / 26.8 / **39.7** |
| Max frame | 148–294 ms | 40 / 329 ms | 333 / 217 / 49 ms |
| CPU / GPU frame avg | 7.3–9.3 / 5.6–5.9 ms | 6.2 / 4.9 · 6.1 / 4.5 ms | 5.8–6.2 / 4.4–4.8 ms |
| Draw calls avg / max | 138 / 272 | 138 / — | **192 / 392–404** |
| SetPass avg / max | 37 / 72 | 37 / — | 38 / 82 |
| Triangles max | 20.3 k | — | 28–30 k |
| Gfx memory max | 782 MB | 782 MB | 782 MB |
| VRAM peak (nvidia-smi) | 802 MB | — | 813–815 MB |
| Load | 5.2 s | 6.4 s / 49.8 s (stalled while unfocused) | 4.2–4.3 s |
| Shift | 12/12, $265.20 | same | same (all 3) |

Counts and memory repeat exactly across runs. Frame-time tails depend on what else is running on the machine; see REVIEW-W4J §3.

## Re-measure triggers
After W4F (ART-003/004), GAME-005 (jar fill meshes), PROC-003, and any lighting/quality-setting change.
