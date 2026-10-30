# Handoff — BUILD-003 (studio.ps1 W3A notes + SliceCapture in unity-capture)

**Status:** done; all validation passes. Branch `claude/task-build-003-0837ba` off main a6e230c, not merged. Only `Tools/Studio/studio.ps1` changed (no C#).

## Changed (`Tools/Studio/studio.ps1`)
1. **n2:** `$Stamp` = `yyyyMMdd-HHmmss-fff-<PID>`. Logs, results, test XMLs and the player log all use it. `status` now strips either stamp form to group by command, so old result files still show.
2. **n3:** `Assert-UnityReady` re-checks `Test-ProjectLocked` after `Wait-UnitySlot`. If another run on the worktree launched meanwhile, the result is `blocked` (exit 2), not `fail`.
3. **n5:** `BUILD_MANIFEST.json` `dirtyPaths` → `dirtyPathCount` (still a count). No other reader in the repo; BUILD-002 handoff left as history.
4. **SliceCapture:** after GrayboxCapture + QA, `unity-capture` greps `Assets/**/*.cs` for `Category("SliceCapture")`.
   - Found: re-acquires the DEC-013 slot and runs `-runTests -testPlatform PlayMode -testCategory SliceCapture -testResults <xml> -sliceCaptureDir <screenshots>/<commit>/slice` with graphics.
     Pass needs passed ≥ 1 and failed = 0. Summary gains `slice: passed=… failed=… skipped=… shots=N`; outputs list the slice dir, XML and `<stamp>-unity-capture-slice.log`.
   - Not found: `slice: skipped (no SliceCapture test category)`, and the status is decided by graybox capture alone.

## Validation (this machine)
- main a6e230c: doctor pass (lfsPatterns 9/9) · status pass · compile 260 s, csErrors=0 · edit 123/123 · capture 130 s: 24 shots, QA PASS 0.22 ft, slice skipped.
- Same-second runs: two concurrent `status` runs wrote `20261029-230327-467-44636-status.json` and `…-230327-469-34952-status.json`.
- Run path: throwaway worktree at `claude/task-game-002-7f57d6` (d878b6c, fast-forward of main) + this script → capture pass in 218 s, graybox QA PASS, `slice: passed=1 failed=0 skipped=0 shots=10` (SLICE_01…10; Results shot checked visually). Throwaway removed.
- n3: held the slot lock so `unity-compile` passed the first lock check and queued, then opened `Temp/UnityLockfile` and released the slot. After the DEC-013 wait the result was `status: blocked`, exit 2, and no editor was launched.

## Notes for the Hub
- If the project-lock re-check fires on the slice step, the graybox shots are already written but the run reports `blocked`. Re-running is safe.
- Two same-second `unity-capture` runs still share `<screenshots>/<commit>/`, which is keyed by commit (unchanged; out of scope).
