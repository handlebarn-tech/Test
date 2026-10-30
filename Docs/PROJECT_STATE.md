# PROJECT STATE

**Milestone:** M0/M1 done pending review → next M2 graybox + M3 domain engine (in parallel)
**Known-good commit:** `main` (docs only). Wave 1 work is on branch `review/wave-1` (commit 667ebd1), unreviewed.
**Build health:** on `review/wave-1`: Unity 6000.6.7f1 HDRP project compiles; 1/1 EditMode tests pass; Windows dev build + smoke launch OK (BUILD-001).
**Updated:** 2026-10-29 by Hub (session 2, wave 2 launched)

## Wave 1 results (all complete, awaiting REVIEW-W1)
- **REF-001** (handoff `Docs/Handoffs/REF-001.md`): 10 rooms with high-confidence shells in feet from the vector PDF; 17 CCTV feeds mapped; 13 photos indexed. There are no heights anywhere. HUB/HUB2, restroom and JC are visually blind.
- **MIG-001** (handoff `Docs/Handoffs/MIG-001.md`): full engine contract with line refs; 63 features triaged; 39 executed golden cases; slice subset defined.
- **BUILD-001** (handoff `Docs/Handoffs/BUILD-001.md`): Unity project, 5 asmdefs, 10 additive scenes, `Tools/Studio/studio.ps1` (doctor / compile / test-edit / build / status).

## Wave 1: DONE, merged to main (e5c476d), REVIEW-W1 GO with notes.

## Wave 2 status (2026-10-29)
| Task | Session | State |
|---|---|---|
| ART-001 | dispo-art-001 | working (Unity) |
| GAME-001 | dispo-game-001 | MERGED to main (6f8eafe) |
| PROC-001 | dispo-proc-001 | MERGED to main (6f8eafe) |
| DES-001 | dispo-des-001 | done; reconciling UX-001 questions + ENGINE.md names (claude/task-des-001-635c15) |
| UX-001 | dispo-ux-001 | done → REVIEW-W2B (claude/task-ux-001-1115a2) |
| ASSET-001 | dispo-asset-001 | done → REVIEW-W2B (claude/task-asset-001-9856c0) |
| REVIEW-W2A | dispo-review-w2a | running (branch review/wave-2a) |
| REVIEW-W2B | not started | start when DES-001 reconcile finishes |

## NEXT ACTIONS (in order) — fresh Hub starts here
1. DES-001 reconcile done → start REVIEW-W2B session (packet in Active).
2. REVIEW-W2A / W2B GO → merge `review/wave-2a`, `review/wave-2b` into main one at a time (Unity: re-run compile + tests). Move packets to Done.
3. ART-001 done → its own review (REVIEW-W2C) → merge.
4. Then finalize GAME-002 from DES-001's draft; start GAME-002 (+ GAME-003 parser port, PERF-001, BUILD-002 incl. `studio.ps1 blender`, ASSET-002 fetch) as wave 3.
5. Retire finished sessions (archive on Nolan's OK).

## Cross-project
- GAP-206 "sleeping" defect relayed to the TFS tool project hub session on 2026-10-29 (no reply needed).
- When TFS ships v7.11.5, regenerate the goldens and diff them (GAP-210).

## Blockers
- None.

## Decisions requiring user input
- Answered 2026-10-29: jars 454 g (DEC-019), deli only (DEC-020), weighed at a register stand (DEC-021), HUB CCTV image supplied (DEC-022).
- Open: human-only sign-ins for ASSET-002 (Unity Asset Store claims for Warehouse/Office; Sketchfab login). Nolan may also send a photo of the register scale stand.
- Open (before any public build): real brand names (Cookies, Alien Labs, ...) ship in `batches.json`; allowed by DATA_SCHEMA §5 and not PII, but a trademark/IP call for Nolan (REVIEW-W2A m2).
- Later: tax rounding (GAP-204), the TFS tool's open question.
