# REVIEW-W4E — Review PROC-002 (deli canister + bud fill generator)

**Role:** REVIEW · **Priority:** P1 · **Branch:** worktree off `main`; local branch `review/wave-4e`.

## Setup
`git merge --no-ff claude/task-proc-002-99e871` (8102f0d or later). Read `Docs/Tasks/Active/PROC-002.md` and `Docs/Handoffs/PROC-002.md`.

## Checks
1. Design matches DEC-042/043: a square clear acrylic canister, white pop-top lid, coloured base band per brand, label card and THC % tag; no tong cups; capacity 454 g (DEC-019). Sizes are labelled photo estimates until REF-007 merges.
2. Determinism: run the generator twice and get identical output (or the documented tolerance). View the render contact sheet yourself.
3. Unity: compile + EditMode tests; budgets/LODs per ASSET_PRODUCTION_PLAN; no edits to `Code/Simulation|Presentation` or graybox scenes; licences per DEC-023.
4. The fill interface matches GAME-002's grams/start fraction; the handoff describes the slice hook.
5. DEC-013 two-editor gate.

## Owns
`Docs/Reviews/REVIEW-W4E.md`; trivial fixes.

## Done when
`review/wave-4e` holds the merge and the review with a verdict. ≤10-line summary to the Studio Hub (never ask Nolan; DEC-033).
