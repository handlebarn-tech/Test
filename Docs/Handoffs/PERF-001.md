# Handoff — PERF-001 (machine performance baseline)

**Branch:** `claude/task-perf-001-dcc05b` · **Measured build:** `a245942` (main) + capture hook · **Packet:** `Docs/Tasks/Active/PERF-001.md`

## Done
- `-perf <json>` player arg: `Presentation/Perf/PerfCapture.cs`, started from `SceneBootstrap` after all scenes load. Bot plays the
  seed-1 shift (copy of `SliceBotTests.Step` without asserts), vsync off, runInBackground on, timeScale 20, 60 warm-up frames
  skipped, 600 s timeout writes `completed:false`. Writes frame-time avg/p50/p95/p99/max, 1% low, CPU/GPU frame time, draw calls,
  SetPass, batches, tris, verts, Unity memory counters, load time, shift result; quits with exit 0/1.
- `ProjectSettings`: `enableFrameTimingStats: 1` (needed for CPU/GPU frame time).
- `studio.ps1 perf`: runs the existing dev build at 1920×1080 windowed, samples peak VRAM with nvidia-smi, writes
  `Artifacts/Perf/<commit7>-<stamp>.json` and the usual result JSON. Needs `unity-build` first (else blocked, exit 2). No DEC-013 slot.
- `Docs/PERF_BASELINE.md`: budgets vs 2 runs, top 3 costs, re-measure triggers.

## Results (2 runs)
avg 7.3–9.4 ms, p95 10.7–12.9, p99 23–33, **1% low 14–24 FPS (only failing metric)**, CPU 7.3–9.3 ms vs GPU 5.6–5.9 ms (CPU-bound),
138 draw calls / 37 SetPass, 782 MB gfx, 802 MB VRAM peak, load 5.2 s, shift 12/12 served. Counts/memory repeat exactly.

## Validation
`unity-compile` OK (0 CS errors) · `unity-build` OK + smoke · `perf` ×2 completed · `unity-test-edit` 149/149 (waited 4 min on DEC-013).

## Notes / questions for the Hub
- Budgets marked *proposed* in PERF_BASELINE (1% low ≥ 30, CPU/GPU ≤ 12 ms, draw calls ≤ 2000, SetPass ≤ 300, tris ≤ 3 M,
  gfx ≤ 3.5 GB, load ≤ 15 s) need a Hub decision; MACHINE_PROFILE still says "provisional".
- `Batches Count` reads 0 under HDRP/SRP Batcher and the triangle counter likely undercounts; use draw calls/SetPass instead.
- Bot step is duplicated in `PerfCapture` (Presentation can't reference the test asmdef). If GAME changes the bot, update both,
  or move `Step` into Presentation in a GAME task.
- Frame-time noise is ~25 % with other editors running; measure with ≤1 other editor for gate decisions.
- Suggested follow-up (PERF-002): Profiler deep capture of the hitches (top cost 1); re-run `perf` after W4F/GAME-005.
- Not a PlayMode test: the editor's Game view isn't representative of the player, so the capture is player-only.
