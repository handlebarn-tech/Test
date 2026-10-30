# REVIEW-W4B — Review BUILD-003 (studio runner fixes + SliceCapture) + BUILD-004 (hub guard hook)

**Role:** REVIEW · **Priority:** P1 · **Branch:** worktree off `main`; local branch `review/wave-4b`.

## Setup
`git merge --no-ff claude/task-build-003-0837ba` (8738078 or later). Read `Docs/Handoffs/BUILD-003.md` and its BUILD-004 section, and `Docs/Reviews/REVIEW-W3A.md` n2/n3/n5.

## Checks
1. BUILD-003: n2 same-second runs no longer collide; n3 re-checks the lock after taking the slot (`blocked`, not `fail`); n5 `dirtyPathCount`; the studio capture command runs SliceCapture now that the slice is on main (10 shots), and skips cleanly when the category is absent.
2. BUILD-004 / DEC-045: `.claude/settings.json` PreToolUse hook + `Tools/Studio/hub_guard.py`. Run its self-test. Confirm that in the main checkout real engine/build/DCC invocations and edits under `UnityProject/`/`Tools/` are denied, while doc heredocs that merely *mention* those tools, git commands, and anything under `.claude/worktrees/` are allowed. It must fail open on a bad payload, missing python or a missing script. Check it can never block a worker in its worktree.
3. Gates: doctor, status, compile, EditMode; DEC-013 two-editor gate.

## Owns
`Docs/Reviews/REVIEW-W4B.md`; trivial fixes.

## Done when
`review/wave-4b` holds the merge and the review with a verdict. ≤10-line summary to the Studio Hub (never ask Nolan; DEC-033).
