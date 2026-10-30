# REVIEW-W2A — Review GAME-001 + PROC-001

**Role:** REVIEW · **Priority:** P0 · **Branch:** worktree off `main` (wave 1 now merged); create local branch `review/wave-2a`.

## Goal
GO / NO-GO for merging GAME-001 and PROC-001 into `main`. Independent read: check work against packets and sources, not the workers' summaries.

## Setup
In your worktree: `git merge --no-ff claude/task-game-001-b68d0f`, then `git merge --no-ff claude/task-proc-001-38ca78` onto `review/wave-2a`. Resolve trivial conflicts (state/doc files); report anything else.

## Checks
1. **GAME-001** (`Docs/Tasks/Active/GAME-001.md`):
   - `studio.ps1 doctor`, `unity-compile`, `unity-test-edit` all pass on the merged branch (DEC-013: max 2 Unity editors; ART-001 is also running Unity).
   - Re-run `node Tools/Data/import_catalog.js` twice; md5s match the manifest. Run `--check`.
   - PII: grep the generated catalog for any non-allow-listed key, emails, names, ids (DEC-006).
   - Spot-check 5 ported constants/functions against the cited lines in `C:/Users/handl/Downloads/tfs-budtender/deploy/2026-10-30-v7114/site/index.html` (read-only, other live project).
   - Confirm `Dispo.Domain` still has `noEngineReferences: true` and no package refs.
   - REVIEW-W1 M1: confirm RC-04/RC-11 are tested from recorded parses (DEC-017).
2. **PROC-001** (`Docs/Tasks/Active/PROC-001.md`):
   - Run both generators twice via `Tools/Blender/blender.ps1`; confirm byte-identical outputs and tri budgets.
   - Files: no export over 10 MB; nothing under `UnityProject/`.
   - Register GAP-PROC-01…06 (from `Docs/Assets/Specs/PROC_PIPELINE.md`) in `Docs/KNOWN_GAPS.md`.
3. **Hygiene:** no secrets, no PII, no tfs-budtender files copied in, LF/CRLF settings don't break the catalog md5s on a fresh checkout.

## Owns
`Docs/Reviews/REVIEW-W2A.md`; `Docs/KNOWN_GAPS.md` (GAP-PROC rows); trivial doc fixes on `review/wave-2a`.

## Done when
`review/wave-2a` holds both merges and the review file with a verdict. Report the verdict and a ≤15-line summary to the Studio Hub. The Hub merges into `main`.
