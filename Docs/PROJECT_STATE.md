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

## Wave 3 status (2026-10-29)
| Task | Session | State |
|---|---|---|
| GAME-002 | dispo-game-002 | building; got DEC-033..036 must-fixes |
| ART-002 | dispo-art-002 | done; follow-up: REF-003 stand sizes + DEC-037 heights → then REVIEW-W3B |
| REF-003 | dispo-ref-003 | done → REVIEW-W3B (with ART-002) |
| GAME-003, BUILD-002 | — | done → REVIEW-W3A (dispo-review-w3a) |
| COMP-001, RES-001, ASSET-002 | — | done → REVIEW-W3C (dispo-review-w3c) |
| REF-004 | dispo-ref-004 | importing TI drawings (read-only M365) |
Unity Warehouse/Office packs: still need a Unity editor Package Manager download (P1, later).

## NEXT ACTIONS (in order) — fresh Hub starts here
1. ART-002 follow-up done → start REVIEW-W3B (packet still to write: ART-002 + REF-003, Unity gates, overlay, anchors test).
2. Merge W3A/W3B/W3C as they pass; Unity merges re-run compile + tests.
3. GAME-002 done → REVIEW of the slice (play it via the PlayMode bot + captures) → merge → the vertical slice is playable; brief Nolan.
4. Then: PERF-001; ART-003 hero retail lookdev (TI finishes DEC-037 + ASSET-002 cache, Montserrat/Crimson Pro brand fonts); PROC-002 jar fill/bud system; COMP later mechanics (limit meter, ID events, medical); packaged assortment (DEC-034).
5. Archive finished sessions after merge.

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
