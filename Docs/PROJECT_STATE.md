# PROJECT STATE

**Milestone:** M0/M1 done pending review → next M2 graybox + M3 domain engine (in parallel)
**Known-good commit:** `main` (docs only). Wave 1 work is on branch `review/wave-1` (commit 667ebd1), unreviewed.
**Build health:** on `review/wave-1`: Unity 6000.6.7f1 HDRP project compiles; 1/1 EditMode tests pass; Windows dev build + smoke launch OK (BUILD-001).
**Updated:** 2026-10-29 by Hub (session 2, wave 3 launched)

## Wave 1 results (all complete, awaiting REVIEW-W1)
- **REF-001** (handoff `Docs/Handoffs/REF-001.md`): 10 rooms with high-confidence shells in feet from the vector PDF; 17 CCTV feeds mapped; 13 photos indexed. There are no heights anywhere. HUB/HUB2, restroom and JC are visually blind.
- **MIG-001** (handoff `Docs/Handoffs/MIG-001.md`): full engine contract with line refs; 63 features triaged; 39 executed golden cases; slice subset defined.
- **BUILD-001** (handoff `Docs/Handoffs/BUILD-001.md`): Unity project, 5 asmdefs, 10 additive scenes, `Tools/Studio/studio.ps1` (doctor / compile / test-edit / build / status).

## Waves 1 and 2: DONE, all merged to main (latest 93f8b47). Every review GO with notes.

## Wave 3 (started 2026-10-29)
| Task | Session | Notes |
|---|---|---|
| GAME-002 | dispo-game-002 | vertical-slice shift loop; scoped Domain grant (DEC-028); own additive scene (DEC-029) |
| GAME-003 | dispo-game-003 | parser + full features port |
| ART-002 | dispo-art-002 | HUB swap, scale stands, slice anchors, deterministic scenes |
| REF-003 | dispo-ref-003 | back-of-register stills → stand spec; tell ART-002 when merged |
| BUILD-002 | dispo-build-002 | studio.ps1 hardening, blender/assets commands, build manifest |
| ASSET-002 | dispo-asset-002 | P0 asset fetch into shared cache (DEC-023) |
Unity: max 2 editors (DEC-013), so Unity sessions queue on the gate.

## NEXT ACTIONS (in order) — fresh Hub starts here
1. As each wave-3 task finishes, start a review session for it (group small ones) and merge reviewed branches one at a time; Unity merges re-run compile + tests.
2. REF-003 merged → message ART-002 to update stand sizes.
3. After GAME-002 + ART-002 merge: the vertical slice is playable → PERF-001, then M5 hero retail lookdev (ART-003) from the ASSET-002 cache, PROC-002 jar fill/bud system, and a playtest/QA pass.
4. Archive finished sessions.

## Cross-project
- GAP-206 "sleeping" defect relayed to the TFS tool project hub session on 2026-10-29 (no reply needed).
- When TFS ships v7.11.5, regenerate the goldens and diff them (GAP-210).

## Blockers
- None.

## Decisions requiring user input
- Answered 2026-10-29: jars 454 g (DEC-019), deli only (DEC-020), weighed at a register stand (DEC-021), HUB CCTV image supplied (DEC-022).
- Done 2026-10-29: Nolan signed in to Sketchfab and Unity in the built-in browser pane; Unity Warehouse + UnityJapanOffice are in My Assets (account handlebarn, Personal). ASSET-002 downloads still need one batch OK from Nolan (list with sizes). Nolan may also send a photo of the register scale stand.
- Open (before any public build): real brand names (Cookies, Alien Labs, ...) ship in `batches.json`; allowed by DATA_SCHEMA §5 and not PII, but a trademark/IP call for Nolan (REVIEW-W2A m2).
- Later: tax rounding (GAP-204), the TFS tool's open question.
