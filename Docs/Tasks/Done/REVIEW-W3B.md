# REVIEW-W3B — Review ART-002 (graybox update) + REF-003 (scale stand stills)

**Role:** REVIEW · **Priority:** P0 · **Branch:** worktree off `main`; local branch `review/wave-3b`. Start only after ART-002's follow-up commit (REF-003 stand sizes + DEC-037 heights) lands.

## Setup
`git merge --no-ff claude/task-ref-003-e34c4b`, then `git merge --no-ff claude/task-art-002-5e7777` onto `review/wave-3b`.

## Checks
1. **REF-003:** stand spec in REFERENCES_INDEX §2.2 matches the stills (view them yourself); every derived crop has people removed (PII); DEC-030 SE exit row present.
2. **ART-002** (`Docs/Tasks/Active/ART-002.md`): `unity-graybox` twice → no scene diff; `unity-compile`, `unity-test-edit`, `unity-test-play` (incl. the SLICE_DESIGN §7 anchor test) pass; `unity-capture` contact sheet; overlay ≤0.5 ft.
3. Evidence: HUB/HUB 2 swapped per DEC-024; scale stands per REF-003 §2.2 and DEC-021/026; heights per DEC-037 (retail 9'-0", soffits 7'-6", back rooms 8'–9', doors 3'-0"×7'-0", storefront 6'-0"×7'-0"); SE emergency exit per DEC-030; every remaining placeholder carries a GAP id.
4. DEC-029: graybox scenes regenerate deterministically; nothing in `Gameplay_Slice.unity` or `Code/Simulation|Presentation/` touched.
5. DEC-013 Unity gate.

## Owns
`Docs/Reviews/REVIEW-W3B.md`; trivial doc fixes.

## Done when
`review/wave-3b` holds both merges and the review with a verdict. Report the verdict and a ≤12-line summary to the Studio Hub (never ask Nolan; DEC-033).
