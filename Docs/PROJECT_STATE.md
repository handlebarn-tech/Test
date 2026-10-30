# PROJECT STATE

**Milestone:** M0/M1 done pending review → next M2 graybox + M3 domain engine (in parallel)
**Known-good commit:** `main` (docs only). Wave 1 work is on branch `review/wave-1` (commit 667ebd1), unreviewed.
**Build health:** on `review/wave-1`: Unity 6000.6.7f1 HDRP project compiles; 1/1 EditMode tests pass; Windows dev build + smoke launch OK (BUILD-001).
**Updated:** 2026-10-29 by Hub (session 2, end; handover for a cleared hub)

## Wave 1 results (all complete, awaiting REVIEW-W1)
- **REF-001** (handoff `Docs/Handoffs/REF-001.md`): 10 rooms with high-confidence shells in feet from the vector PDF; 17 CCTV feeds mapped; 13 photos indexed. There are no heights anywhere. HUB/HUB2, restroom and JC are visually blind.
- **MIG-001** (handoff `Docs/Handoffs/MIG-001.md`): full engine contract with line refs; 63 features triaged; 39 executed golden cases; slice subset defined.
- **BUILD-001** (handoff `Docs/Handoffs/BUILD-001.md`): Unity project, 5 asmdefs, 10 additive scenes, `Tools/Studio/studio.ps1` (doctor / compile / test-edit / build / status).

## Waves 1 and 2: DONE, all merged to main (latest 93f8b47). Every review GO with notes.

## Wave 3 status (2026-10-29)
| Task | Session | State |
|---|---|---|
| GAME-002 | dispo-game-002 | done (8df0a82, 41/41 EditMode, bot 12/12) → REVIEW-W3D (packet in Active; proposed, waiting on start) |
| ART-002 | dispo-art-002 | done incl. follow-up 6788cca → REVIEW-W3B (dispo-review-w3b) |
| REF-003 | dispo-ref-003 | done → REVIEW-W3B (with ART-002) |
| GAME-003, BUILD-002 | — | done → REVIEW-W3A (dispo-review-w3a) |
| COMP-001, RES-001, ASSET-002 | — | REVIEW-W3C PASS; merged to main (32a1ad9) |
| REF-004 | dispo-ref-004 | importing TI drawings (read-only M365) |
Unity Warehouse/Office packs: still need a Unity editor Package Manager download (P1, later).

### Live session ids (for SendMessage / archive)
- dispo-game-002 `local_e574024b-b42a-4f12-b5db-6b6d66ac34bc` (working)
- dispo-review-w3b `local_53273c02-a00e-46fb-9407-96ecfc4855ad` (started by Hub session 3)
- dispo-art-002 `local_6681ee58-dbed-4e39-adda-192aa4a576fb` (idle; archive after W3B merges)
- dispo-review-w3a `local_d40fcd21-be35-4d84-bf4f-90fb27eac376` · dispo-review-w3c `local_819f11d1-8aac-40d4-b6d8-c2435445b1ee` · dispo-ref-004 `local_8e643693-f039-47b6-8392-365947ed9efc` (working)
- Idle, archive after their reviews merge: game-003 `local_23577d66-0fd6-4bfb-831e-6950d9ff3e3d`, build-002 `local_e58e2c77-01ad-4ef6-b560-9da96488af50`, ref-003 `local_c3b522a0-283d-45c1-af1d-8e0ec1bfca4f`, res-001 `local_f19e4a49-5f05-4f20-a0ca-c56f31e4a50e`, comp-001 `local_7f7a77b4-e098-4fd1-b838-399ac35df20f`, asset-002 `local_4921e361-4a37-4b68-a853-961b622160da`.

## NEXT ACTIONS (in order) — fresh Hub starts here
1. ~~Start REVIEW-W3B~~ started 2026-10-29 by Hub session 3.
2. Merge W3A/W3B as they pass (W3C merged); Unity merges re-run compile + tests.
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
- Follow-up for BUILD: add the SliceCapture test to `studio.ps1 unity-capture` (GAME-002 open item).
- Batch for Nolan (store fact): a photo of a real receipt's tax lines would settle Phoenix TPT rate (OPEN-4); game keeps 25.1 % (DEC-001) meanwhile.
