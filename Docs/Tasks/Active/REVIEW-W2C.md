# REVIEW-W2C — Review ART-001 (graybox + QA harness)

**Role:** REVIEW · **Priority:** P0 · **Branch:** worktree off `main`; local branch `review/wave-2c`.

## Goal
GO / NO-GO for merging ART-001 into `main`. Independent read against `Docs/Tasks/Active/ART-001.md`, `Docs/REFERENCES_INDEX.md` and `References/Floor Plan.pdf`, not the worker's summary.

## Setup
`git merge --no-ff claude/task-art-001-e39b67` onto `review/wave-2c`. Copy `Tools/Studio/studio.config.example.json` to `studio.config.json` (gitignored).

## Checks
1. `studio.ps1 doctor`, `unity-graybox`, `unity-compile`, `unity-test-edit`, `unity-test-play`, `unity-capture` all pass (DEC-013: max 2 Unity editors; REVIEW-W2A also runs Unity).
2. Overlay: re-check the top-down vs `References/Index/floor_plan_grid_1ft.png`; confirm max deviation ≤0.5 ft and spot-check 4 room dimensions in `graybox_layout.json` against REFERENCES_INDEX.
3. Every placeholder height and Low-confidence fixture carries its GAP id; nothing invented. HUB interior treated as low confidence (DEC-018). Register the new GAP-104 fact (vestibule doors use the full 2.2 ft side) in `Docs/KNOWN_GAPS.md`.
4. `studio.ps1` additions: the DEC-013 wait gate works and doesn't break existing commands.
5. **ProjectSettings normalization:** Unity/HDRP re-serializes `GraphicsSettings.asset`, `QualitySettings.asset` and `HDRenderPipelineGlobalSettings.asset` on open. Decide whether the normalized values are the correct HDRP defaults; if yes, commit them once as a separate commit on `review/wave-2c` ("BUILD: commit HDRP-normalized ProjectSettings") and note any behaviour change (e.g. lodBias 2→1).
6. Hygiene: no files over 10 MB, no Library/Temp/UserSettings tracked, no PII.

## Owns
`Docs/Reviews/REVIEW-W2C.md`; the GAP-104 row in `Docs/KNOWN_GAPS.md`; the ProjectSettings commit; trivial doc fixes.

## Done when
`review/wave-2c` holds the merge and the review file with a verdict. Report the verdict and a ≤15-line summary to the Studio Hub. The Hub merges.
