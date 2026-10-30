# REVIEW-W2B — Review DES-001 + UX-001 + ASSET-001

**Role:** REVIEW (docs) · **Priority:** P0 · **Branch:** worktree off `main`; create local branch `review/wave-2b`.

## Goal
GO / NO-GO for merging the slice design, slice UX and asset ledger into `main`, and confirm GAME-002 can be written with no open design questions.

## Setup
`git merge --no-ff` each of `claude/task-des-001-635c15`, `claude/task-ux-001-1115a2`, `claude/task-asset-001-9856c0` onto `review/wave-2b`.

## Checks
1. **DES-001 ↔ UX-001 ↔ GAME-001 consistency:**
   - Every UX question (UX_SLICE §9) is answered in SLICE_DESIGN.md.
   - Every engine name in SLICE_DESIGN §6 and the GAME-002 draft exists in GAME-001's `Docs/Specs/ENGINE.md` (read it with `git show claude/task-game-001-b68d0f:Docs/Specs/ENGINE.md`).
   - Every bound field in UX_SLICE matches.
2. **Source discipline:** spot-check 8 [SRC] rules against their citations; confirm no invented real-store facts (placeholders must be flagged; the 3 open facts for Nolan are listed).
3. **Constants:** SliceConfig §8 complete; recompute the 3 formula sanity rows.
4. **ASSET-001:** re-verify 8 ledger rows (mix of Poly Haven, Sketchfab, audio, font) at their URLs; confirm no assets were committed; confirm redistribution flags.
5. **Hygiene:** no PII, no tfs-budtender content copied, SVG/PNG sizes within packet limits.

## Owns
`Docs/Reviews/REVIEW-W2B.md`; trivial doc fixes on `review/wave-2b`.

## Done when
`review/wave-2b` holds the three merges and the review file with a verdict. Report the verdict and a ≤15-line summary to the Studio Hub. The Hub merges.
