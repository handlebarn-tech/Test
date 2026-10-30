# REVIEW-W3D — Review GAME-002 (playable vertical-slice shift)

**Role:** REVIEW · **Priority:** P0 · **Branch:** worktree off `main`; local branch `review/wave-3d`.

## Setup
`git merge --no-ff claude/task-game-002-7f57d6` onto `review/wave-3d`. Read `Docs/Handoffs/GAME-002.md` (on that branch) and `Docs/Tasks/Active/GAME-002.md`.

## Checks
1. Studio gates: `unity-compile`, `unity-test-edit` (expect 41/41), `unity-test-play` (2 pass + capture skipped). Then run the SliceCapture test with graphics (`-runTests -testPlatform PlayMode -testCategory SliceCapture -sliceCaptureDir <dir>`) and view the 10 shots yourself: HUD, dialogue, query, results, detail, POS (check the 28 g tile no longer overlaps MSRP after the min-height fix), toast, jar wall LOW/SOLD OUT, report. Labels must sit over their jars.
2. Play it: run the PlayMode bot (seed 1) and confirm 12 customers, revenue = Σ sales, a SOLD OUT occurs, report fields per SLICE_DESIGN §1.
3. Domain scope (DEC-028): GAME-002 touches only S1 (`Catalog.SetInStock`), S2 (`Engine/Labels.cs`), S3 (`RepBatchId`). Engine goldens unchanged. Flag overlap with GAME-003 (`review/wave-3a`) for the Hub.
4. Compliance (DEC-035/036): 28.0 g cap blocks Confirm; "21+ ID verified" line; clock 14:00 inside 08–22; POS nearest-$0.05 vs card `priceFloor`.
5. DEC-029: no graybox scene edited; `Gameplay_Slice.unity` regenerates from `SliceSceneBuilder`.
6. Rule on GAME-002's 5 "Decisions taken" (SOLD OUT seeding of rank-1 reps, 3.5 g flooring, service start, metrics, new config keys, screen-space labels): accept, or state the fix.
7. Integration: when `review/wave-3a` (GAME-003) and `review/wave-3b` (ART-002 anchors) have a GO, the Hub will tell you; then merge them into `review/wave-3d`, resolve conflicts, re-run gates and confirm the TEMP_ anchors switch off on ART-002's real anchors. If they are not ready when the GAME-002-only checks finish, report the verdict for GAME-002 alone and wait for the Hub's message.
8. DEC-013 Unity gate.

## Owns
`Docs/Reviews/REVIEW-W3D.md`; trivial fixes (CSS, doc typos). Anything larger: findings to the Hub.

## Done when
`review/wave-3d` holds the merge(s) and the review with a verdict. Report the verdict and a ≤15-line summary to the Studio Hub (never ask Nolan; DEC-033).
