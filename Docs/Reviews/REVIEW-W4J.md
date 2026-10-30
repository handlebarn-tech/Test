# REVIEW-W4J — PERF-001 (player perf capture, `studio.ps1 perf`, baseline)

**Branch:** `review/wave-4j` = `main` (b52c60b) + `--no-ff` merge of `claude/task-perf-001-dcc05b` (da1a4a3) → 7ee9ae0.
- The only conflict was the task packet: main no longer has `Docs/Tasks/Active/`, and git's directory-rename detection put `PERF-001.md` in `Docs/Tasks/Done/`.
- Main has since moved to 377e086. I didn't re-merge, because the review is about the perf tooling, not about newer content.

**Final verdict: GO with notes.** I made one fix in review: `-perf` runs no longer stall when the player window is unfocused (§1).
The failing metric (1% low) is mostly measurement noise from other work on the machine (§3). The one real, repeatable cost is the Results→POS frame.

## 1. Capture and `studio.ps1 perf`: deterministic, and no effect on normal play
- **Normal play** is unchanged:
  - `PerfCapture` is only added when `-perf <json>` is on the command line.
  - The one global change is `enableFrameTimingStats: 1`. It costs a little CPU in every build, including release, but it's needed for CPU/GPU frame time. Fine.
- **Determinism:** all 3 lookdev runs and the a245942 re-run end with served=12, 0 walkouts, $265.20, 3★.
  - Draw calls, SetPass and memory repeat almost exactly: draw-call average 191.72/191.72/191.77, gfx memory 781.89 MB.
  - Only frame time varies.
- **Fixed in review: unfocused-start stall.** `runInBackground` is 0 in ProjectSettings, and `PerfCapture.Begin` only turns it on after all 9–10 scenes have loaded.
  - One of my three runs of the a245942 exe stopped during scene load and never resumed; I killed it. A second one paused and only finished after 49.8 s. The process was responding, the log ended after input init, and no frames were captured.
  - A stalled run waits until `studio.ps1`'s 15-minute kill.
  - Fix: `SceneBootstrap.Start` sets `Application.runInBackground = true` before loading when `-perf` is present. It's one line and affects `-perf` runs only.
  - My lookdev runs were built before the fix, and they happened to keep focus.
- **Minor (not fixed):** `perf` reads `BUILD_MANIFEST.json` under `$ErrorActionPreference = 'Stop'`. A build folder without the manifest crashes the command without a result JSON. A `Test-Path` guard would fix it.
- **Duplicated code:** `PerfCapture.Step` copies `SliceBotTests.Step` (PERF-001 handoff). That's acceptable for now; keep both in sync.

## 2. Is PERF_BASELINE reproducible? Yes for counts and memory; no for frame-time tails unless the machine is quiet
I added a 2026-10-30 section with a lookdev column to `Docs/PERF_BASELINE.md`.
- **Counts and memory reproduce exactly.** a245942 re-run: draw calls 137.8, SetPass 36.6, gfx memory 782 MB, the same as PERF-001.
- **Frame time does not reproduce.** The same a245942 exe gave **1% low 41.5 FPS / max 40 ms with 0 other editors** and **23.4 FPS / max 329 ms with 2**. Avg (6.2 ms) and p99 (18 ms) were the same in both runs. PERF-001, with 2–3 editors open, got 7.3–9.4 ms, p99 23–33 ms, 1% low 14–24 FPS and max 148–294 ms.
- **Lookdev (7ee9ae0) cost:**
  - Draw calls average 138 → **192** (max 272 → ~400). Triangles max 20 k → 29 k.
  - CPU, GPU and memory: no measurable change (CPU 5.8–6.2 ms, GPU 4.4–4.8 ms, VRAM peak 815 MB).
  - Load time 4.3 s.
- **6 GB VRAM:** we use 0.8 GB of the 5 GB ceiling. The lookdev did not move gfx memory. The proposed 3.5 GB gfx budget leaves about 1.5 GB for the OS, the browser and a second editor, which is sensible.

## 3. The failing metric: 1% low 14–24 FPS
To find which frames are slow, I added temporary per-frame logging in a local build: screen transition, GC0 delta and sale state for every frame. It is not committed. 3 lookdev runs, about 3,000 frames each. A 1% low is the average of the slowest ~30 frames.
- **Mostly noise.** The worst frames are bursts of 3–5 consecutive 80–333 ms frames on the idle World screen.
  - They have no GC, no customer and no screen change, and they land at different frames in each run: 5, 3 and 0 frames over 50 ms in the three runs.
  - When the run with no burst happens (run 3), the 1% low is **39.7 FPS**. The same a245942 exe gives **41.5 FPS with 0 other editors and 23.4 with 2**. Content doesn't change between those two runs, so contention alone moves the metric by 18 FPS.
  - These bursts are OS or GPU contention from the other Unity editors and builds. PERF-001's 2–3 editors explain its low numbers.
- **Real and repeatable:** the **Results→POS** frame costs 22.6–26 ms on average (max 40–45 ms) in every run, for every customer. That's 4–5× a 5.2 ms median frame.
  - That frame runs `Sim.Present` (Fit/PriceFit scoring) and a full UI Toolkit POS rebuild (`SliceView.Render` clears and rebuilds the screen).
  - Smaller, also repeatable: 25–35 ms frames around customer spawn on the World screen.
- **Likely top causes, in order (not fixed):**
  1. The full-screen UI Toolkit rebuild and layout on each screen change (the POS screen especially).
  2. The `Present` scoring work on the same frame.
  3. Customer spawn/despawn (NPC `CreatePrimitive`/`Destroy`) and first-use shader/PSO compiles after the 60-frame warm-up.
- **The measurement inflates the cost.** At timeScale 20 a shift lasts about 3,000 frames, so the 12 POS frames are 0.4 % of all frames, close to half the 1% bucket. At real speed (1×) a shift lasts about 20× more frames, so these frames would barely reach the 1% low.
  - Recommendation for PERF-002: report p99.9 and per-transition max frame time, not only the 1% low.

## 4. Gates (DEC-013 through `studio.ps1`)
| Gate | Result |
|---|---|
| `unity-build` (7ee9ae0) | pass, smoke scenes=10 |
| `perf` ×3 (7ee9ae0) | all completed; numbers in §2 |
| `unity-compile` | pass, csErrors=0 (includes the SceneBootstrap fix) |
| `unity-test-edit` | **149/149** |

`unity-build` rewrote `HDRenderPipelineGlobalSettings.asset` (+21 lines, W2C n2). I reverted it, so it is not in this commit.

## Budget recommendation for the Hub
Adopt PERF-001's proposed budgets as the binding ones in MACHINE_PROFILE, with these changes:
- Frame time avg ≤ 16.7 ms and p95 ≤ 16.7 ms: keep.
- **1% low ≥ 30 FPS: keep as the target, but only gate on it when measured with ≤ 1 other Unity editor (best of 2 runs).** Under contention it's not a valid gate.
  - Also add **POS transition frame ≤ 33 ms** (it is 40–45 ms now; the owner is GAME/UX in PERF-002).
- CPU ≤ 12 ms, GPU ≤ 12 ms: keep. Today 6 / 4.5 ms.
- Draw calls ≤ 2,000 and SetPass ≤ 300: keep. Lookdev raised draw calls by 40 %, so re-check after the PROC jar fills and GAME-005.
- Gfx memory ≤ 3.5 GB and VRAM peak ≤ 5 GB: keep. Today 0.8 GB.
- Load ≤ 15 s: keep. Today 4–6 s.
- Triangles: report only. The counter undercounts under HDRP.

## Notes for the Hub
- n1: PERF-002 should take a Profiler deep capture of the Results→POS frame and of customer spawn, and add p99.9 and transition-frame metrics.
- n2: run `perf` with ≤ 1 other editor for any gate decision. DEC-013 allows two editors, so the Hub needs to schedule perf runs.
- n3: `perf` manifest guard (§1, minor).
