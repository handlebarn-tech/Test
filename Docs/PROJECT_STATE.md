# PROJECT STATE

**Milestone:** M0/M1 done pending review → next M2 graybox + M3 domain engine (in parallel)
**Known-good commit:** `main` (docs only). Wave 1 work is on branch `review/wave-1` (commit 667ebd1), unreviewed.
**Build health:** on `review/wave-1`: Unity 6000.6.7f1 HDRP project compiles; 1/1 EditMode tests pass; Windows dev build + smoke launch OK (BUILD-001).
**Updated:** 2026-10-29 by Hub (session 2, wave 2 launched)

## Wave 1 results (all complete, awaiting REVIEW-W1)
- **REF-001** (handoff `Docs/Handoffs/REF-001.md`): 10 rooms with high-confidence shells in feet from the vector PDF; 17 CCTV feeds mapped; 13 photos indexed. There are no heights anywhere. HUB/HUB2, restroom and JC are visually blind.
- **MIG-001** (handoff `Docs/Handoffs/MIG-001.md`): full engine contract with line refs; 63 features triaged; 39 executed golden cases; slice subset defined.
- **BUILD-001** (handoff `Docs/Handoffs/BUILD-001.md`): Unity project, 5 asmdefs, 10 additive scenes, `Tools/Studio/studio.ps1` (doctor / compile / test-edit / build / status).

## Wave 2 (running, started 2026-10-29, all off `base/wave-2` per DEC-012)
| Task | Session name | Branch prefix |
|---|---|---|
| REVIEW-W1 | dispo-review-w1 | review-w1 (commits land on `review/wave-1`) |
| ART-001 | dispo-art-001 | task-ART-001 (Unity) |
| GAME-001 | dispo-game-001 | task-GAME-001 (Unity) |
| PROC-001 | dispo-proc-001 | task-PROC-001 (Blender) |
| DES-001 | dispo-des-001 | task-DES-001 (docs) |
| UX-001 | dispo-ux-001 | task-UX-001 (docs) |
| ASSET-001 | dispo-asset-001 | task-ASSET-001 (docs, Sonnet) |
Unity concurrency: max 2 editors (DEC-013).

## NEXT ACTIONS (in order) — fresh Hub starts here
1. Check linked sessions (`list_sessions {"linked": true}`) and new handoffs on their branches.
2. REVIEW-W1 GO → merge `review/wave-1` into `main` (first move aside the untracked `UnityProject/` in the main checkout, which would block the merge; it came from BUILD-001 runs). NO-GO → relay findings to affected wave-2 sessions.
3. As wave-2 tasks finish: start a REVIEW-W2 session over their branches; merge reviewed branches one at a time (Unity ones: re-run compile + tests after each).
4. Then finalize GAME-002 from DES-001's draft + UX-001; candidates for wave 3: GAME-002, GAME-003, PERF-001, BUILD-002 (wires PROC `blender` command into studio.ps1), asset import from ASSET-001.

## Cross-project
- GAP-206 "sleeping" defect relayed to the TFS tool project hub session on 2026-10-29 (no reply needed).
- When TFS ships v7.11.5, regenerate the goldens and diff them (GAP-210).

## Blockers
- None.

## Decisions requiring user input
- None open. Possible later item: tax rounding (floor vs round, GAP-204). That is the TFS tool's open question with Nolan; the game mirrors v7.11.4 until decided.
