# PROJECT STATE

**Milestone:** M0/M1 done pending review → next M2 graybox + M3 domain engine (in parallel)
**Known-good commit:** `main` (docs only). Wave 1 work is on branch `review/wave-1` (commit 667ebd1), unreviewed.
**Build health:** on `review/wave-1`: Unity 6000.6.7f1 HDRP project compiles; 1/1 EditMode tests pass; Windows dev build + smoke launch OK (BUILD-001).
**Updated:** 2026-10-29 by Hub (session 1, end)

## Wave 1 results (all complete, awaiting REVIEW-W1)
- **REF-001** (handoff `Docs/Handoffs/REF-001.md`): 10 rooms with high-confidence shells in feet from the vector PDF; 17 CCTV feeds mapped; 13 photos indexed. There are no heights anywhere. HUB/HUB2, restroom and JC are visually blind.
- **MIG-001** (handoff `Docs/Handoffs/MIG-001.md`): full engine contract with line refs; 63 features triaged; 39 executed golden cases; slice subset defined.
- **BUILD-001** (handoff `Docs/Handoffs/BUILD-001.md`): Unity project, 5 asmdefs, 10 additive scenes, `Tools/Studio/studio.ps1` (doctor / compile / test-edit / build / status).

## NEXT ACTIONS (in order) — fresh Hub starts here
1. Start one session for `Docs/Tasks/Ready/REVIEW-W1.md` (worktree on `review/wave-1`).
2. On GO: `git merge --no-ff review/wave-1` into `main`. Move REF/MIG/BUILD packets Review → Done; delete the branch.
3. Then start **two sessions in parallel**, each in its own worktree off `main`:
   - Unity / art: `Docs/Tasks/Ready/ART-001.md` (graybox + QA harness)
   - Data / engine: `Docs/Tasks/Ready/GAME-001.md` (importer + C# engine + goldens)
   - Both touch `UnityProject/`, but in disjoint folders. Merge one at a time, re-running compile and tests after each merge.
4. After both: GAME-002, the vertical-slice shift loop (write that packet then).

## Cross-project
- GAP-206 "sleeping" defect relayed to the TFS tool project hub session on 2026-10-29 (no reply needed).
- When TFS ships v7.11.5, regenerate the goldens and diff them (GAP-210).

## Blockers
- None.

## Decisions requiring user input
- None open. Possible later item: tax rounding (floor vs round, GAP-204). That is the TFS tool's open question with Nolan; the game mirrors v7.11.4 until decided.
