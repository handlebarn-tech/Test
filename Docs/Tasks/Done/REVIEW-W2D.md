# REVIEW-W2D — Review REF-002 (HUB CCTV + register scale stand)

**Role:** REVIEW (references) · **Priority:** P0 · **Branch:** worktree off `main`; local branch `review/wave-2d`.

## Goal
GO / NO-GO for merging REF-002. Independent read: look at the images yourself.

## Setup
`git merge --no-ff claude/task-ref-002-77ac90` onto `review/wave-2d`.

## Checks
1. **Tile identity:** REF-002 says 7 of 8 HUB-wall tiles are the same cameras as main-wall R4C3/R4C4/R5C1–C5, HUB R1C4 is new, and HUB R2C4 repeats R2C1. Verify by viewing the crops in `References/Index/hub/` against the main CCTV walls.
2. **Room assignment:** left column = HUB 2, rest = HUB. Check the reasoning against Nolan's words ("First room on left two pictures, the rest are in the bigger side of the hub") and the plan areas (HUB 818 SF, HUB 2 541 SF). Note this reverses REF-001's mapping (DEC-024).
3. **Register scale stand:** confirm it is visible in R2C3, R2C4, R3C2 and BAND 10 (scale in BAND 07); check the size estimate against the plan scale.
4. **Fixtures:** spot-check 6 of the 19 HUB fixture rows against their cited tiles.
5. `Docs/KNOWN_GAPS.md` GAP-105/107 edits are consistent; also update GAP-110 to "CCTV only, Med" (Hub request).
6. PII: no people identification; crop files ≤1 MB each.

## Owns
`Docs/Reviews/REVIEW-W2D.md`; GAP-110 row; trivial doc fixes on `review/wave-2d`.

## Done when
`review/wave-2d` holds the merge and the review file with a verdict. Report the verdict and a ≤10-line summary to the Studio Hub.
