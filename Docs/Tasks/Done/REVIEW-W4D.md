# REVIEW-W4D — Review GAME-002b (slice polish)

**Role:** REVIEW · **Priority:** P1 · **Branch:** worktree off `main`; local branch `review/wave-4d`.

## Setup
`git merge --no-ff claude/task-game-002b` (154f235 or later). Read `Docs/Handoffs/GAME-002b.md` and `Docs/Reviews/REVIEW-W3D.md` §Notes.

## Checks
1. Gates: compile, EditMode tests, PlayMode tests, and the SliceCapture run with graphics. View shot 9 yourself: LOW/SOLD OUT labels sit over their own jars, and Kush Cake shows SOLD OUT.
2. **N1 was not checked by eye in a windowed editor (handoff):** do a windowed PlayMode check, or argue from the capture setup that panel and camera sizes now match, and state which you did.
3. DEC-044: `PriceFit` uses the POS total; tests updated.
4. Nits: Results Back/More options overlap, toast over the report, `MoreOptions()` guard.
5. No graybox scene edits (DEC-029); Domain untouched beyond DEC-028. DEC-013 two-editor gate.

## Owns
`Docs/Reviews/REVIEW-W4D.md`; trivial fixes.

## Done when
`review/wave-4d` holds the merge and the review with a verdict. ≤10-line summary to the Studio Hub (never ask Nolan; DEC-033).
