# BUILD-003 — studio.ps1 review notes + SliceCapture in unity-capture

**Role:** BUILD · **Priority:** P2 · **Branch:** `claude/task-build-003-0837ba` worktree off `main` (a6e230c)

## Goal
Close REVIEW-W3A notes n2, n3, n5 on `studio.ps1` and make `unity-capture` also take the GAME-002 slice screenshots, so parallel sessions and reviewers get one capture command.

## Read
`Docs/Tasks/Done/BUILD-002.md`, `Docs/Handoffs/BUILD-002.md`, `Docs/Reviews/REVIEW-W3A.md` n2/n3/n5; `Docs/Handoffs/GAME-002.md` (capture hook, on `claude/task-game-002-7f57d6`); DEC-013.

## Owns
`Tools/Studio/` (not `graybox_qa.py`), `Code/Editor/CI/` only if needed, `Docs/Handoffs/BUILD-003.md`.

## Deliverable
1. **n2:** `$Stamp` = `yyyyMMdd-HHmmss-fff-<PID>`, so same-second runs in one worktree get separate logs/results. `status` must still group results by command.
2. **n3:** `Assert-UnityReady` re-checks `Test-ProjectLocked` after taking the DEC-013 slot lock → `blocked` (exit 2), not `fail`.
3. **n5:** `BUILD_MANIFEST.json` `dirtyPaths` → `dirtyPathCount`; update readers.
4. **SliceCapture:** after GrayboxCapture + QA, if a test source declares `Category("SliceCapture")`, `unity-capture` runs `-runTests -testPlatform PlayMode -testCategory SliceCapture -sliceCaptureDir <screenshots>/<commit>/slice` with graphics (slot re-acquired). Pass needs ≥1 passed, 0 failed. If no such category exists, it skips cleanly and says so in the summary.

## Validation
`doctor`, `status`, `unity-compile`, `unity-test-edit`, `unity-capture` (skip path on main); two same-second `status` runs with distinct result files. Optional: run path on a throwaway merge of `claude/task-game-002-7f57d6`. DEC-013 gate (max 2 Unity.exe, 60 s retry).

## Handoff
`Docs/Handoffs/BUILD-003.md` (≤40 lines). Report to the Studio Hub.
