# PROJECT STATE

**Milestone:** VERTICAL SLICE PLAYABLE on main (0032589, 2026-10-29). Next: slice polish (GAME-002b), wave-4 art/proc, BUILD-003
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
| GAME-002 | dispo-game-002 | REVIEW-W3D GO with notes; MERGED (0032589). EditMode 141/141, bot 12/12 on real anchors. Follow-up GAME-002b: N1 jar labels, DEC-044 PriceFit, nits |
| ART-002 | — | REVIEW-W3B GO with notes; merged to main |
| REF-003 | — | merged via W3B |
| GAME-003, BUILD-002 | — | REVIEW-W3A GO with notes; merged to main (f3e5bc9). n1 cache reset → GAME-002 before its merge; n2/n3/n5 → BUILD-003 |
| COMP-001, RES-001, ASSET-002 | — | REVIEW-W3C PASS; merged to main (32a1ad9) |
| REF-004 | dispo-ref-004 | done (79f648d): TI values indexed §6; PDFs not importable by tools → REVIEW-W3E (`local_632adaa1-403b-4158-b66e-aa1f28011736`); REF-005 sent to the same REF-004 session |
Unity Warehouse/Office packs: still need a Unity editor Package Manager download (P1, later).

### Live session ids (for SendMessage / archive)
- dispo-art-003 `local_392adc04-9603-4cc9-959c-6e3e2d792743` · dispo-proc-002 `local_1b8fb899-d1dc-49d4-8384-8bc73da3e85a` (wave 4, write their own packets first)
- dispo-review-w3d `local_57aeb17a-1d55-496c-8328-51721cfc125a` · dispo-game-002 `local_e574024b-b42a-4f12-b5db-6b6d66ac34bc` (W3A n1 fix)
- dispo-review-w4a `local_92c0cff8-fdfb-4ee5-9c24-1b6e713cb793` (REF-005) · dispo-build-003 `local_be1d6c10-aea5-4f5d-9fae-be727feb85cf` · dispo-ref-004 `local_8e643693-f039-47b6-8392-365947ed9efc` (idle; archive after W4A)
- dispo-game-002 `local_e574024b-b42a-4f12-b5db-6b6d66ac34bc` (working)
- dispo-review-w3b `local_53273c02-a00e-46fb-9407-96ecfc4855ad` (started by Hub session 3)
- dispo-art-002 `local_6681ee58-dbed-4e39-adda-192aa4a576fb` (idle; archive after W3B merges)
- dispo-review-w3a `local_d40fcd21-be35-4d84-bf4f-90fb27eac376` · dispo-review-w3c `local_819f11d1-8aac-40d4-b6d8-c2435445b1ee` · dispo-ref-004 `local_8e643693-f039-47b6-8392-365947ed9efc` (working)
- Idle, archive after their reviews merge: game-003 `local_23577d66-0fd6-4bfb-831e-6950d9ff3e3d`, build-002 `local_e58e2c77-01ad-4ef6-b560-9da96488af50`, ref-003 `local_c3b522a0-283d-45c1-af1d-8e0ec1bfca4f`, res-001 `local_f19e4a49-5f05-4f20-a0ca-c56f31e4a50e`, comp-001 `local_7f7a77b4-e098-4fd1-b838-399ac35df20f`, asset-002 `local_4921e361-4a37-4b68-a853-961b622160da`.

## NEXT ACTIONS (in order) — fresh Hub starts here (handover 2026-10-29 23:20, usage limit; auto-resume 02:00)
1. **Review queue, ready now (start sessions):**
   - REVIEW-W4B: BUILD-003 + BUILD-004 hub guard (`claude/task-build-003-0837ba`). Wait for BUILD-004's commit. **Before merging, delete the untracked prototype `.claude/settings.json` and `Tools/Studio/hub_guard.py` in the main checkout** (git won't overwrite untracked files).
   - BUILD-PLAY (`local_599eaab4-f54f-4421-bdf9-b3729caf654f`): Windows build of the slice for Nolan → `C:/Users/handl/Downloads/Dispo Game Builds/`.
   - **Merged 00:10:** W4E (PROC-002) cb1f8f5; W4B (BUILD-003/004, hardened hub guard live) 489ea33. **Running:** REVIEW-W4F (ART-003+004) in session `local_c8cbad4e…`. **Dispatched by message:** PROC-003 → ART-003 session (fresh branch, after any W4F fixes); BUILD-005 → `local_fa1d4222…`. PERF-001 started (`local_a0a92385-d051-4974-84b8-22bfa01d709e`). **01:05:** W4G merged (c2a2400, BUILD-005 LFS). DEC-047 (workers raise uncertainty questions) is in CLAUDE.md. DES-002 is done (a8b8993) → REVIEW-W4H in the W4G session `local_0dd63bac…`. DES-002's 7 questions were forwarded to Nolan (rec/med share, packaged limits, out-of-state med, daily limit, ID desk location, PII-free inventory export, packaged placement).
   - **00:50:** W4F merged (592086c, ART-003+004: retail lookdev, HUB/HUB 2 match A011). Started REF-008 CCTV deep map Office/FOH/BOH `local_3bc3be53-eb4d-477e-8a99-02d950744ef4` and GAME-005 real jars in slice `local_65e98573-c33d-4c96-bef4-961578ada020`. ART-005 (W4F m1/m2) queued to the ART session after PROC-003. Nolan played the slice: "good progress". Also started 00:35 (Nolan: "run as many sessions as needed"): REVIEW-W4G BUILD-005 `local_0dd63bac-df1d-448d-9203-641ead6b6837`, DES-002 roadmap + COMP-002/GAME-004 specs `local_33047f9d-d771-457c-8dbd-4b07a7a41d2e`, PROC-004 packaged generator `local_ffb38222-b25a-4efb-9910-d97897bbe8b9`. **Next to start:** GAME-005 (after W4F merges).
   - **Merged 23:55:** W4C (REF-006/007, GAP-120 confirmed) d186fea; W4D (GAME-002b) dc4f83c. BUILD-PLAY done: `C:/Users/handl/Downloads/Dispo Game Builds/slice-c867cd5/DispoGame.exe`.
   - **Dispatched by message (notice turn):** REVIEW-W4B (BUILD-003+004) → idle W4D session `local_fa1d4222…`; ART-004 GAP-120 fix → ART-003 session `local_392adc04…`; then the W4C session `local_c8cbad4e…` reviews ART-003+004 together (W4F). W4E (PROC-002) is still finishing.
   - **Earlier:** REVIEW-W4C `local_c8cbad4e-a459-40bf-8475-597c8ec94b75` (REF-006/007), REVIEW-W4D `local_fa1d4222-cd8c-4df7-b9ab-799c6519e8b9` (GAME-002b), REVIEW-W4E `local_c4b9cab4-e039-4ea5-b9d8-a90655ae6797` (PROC-002 at 8102f0d). Merge each on GO.
   - (was queued) REVIEW-W4C: REF-006 + REF-007 (`claude/task-ref-006`, through cf527fe): FOH/BOH desk stills, jar spec (Amazon smalls + acrylic canister), crops (no people, network rack, thermostat or security drawer), SE exit from A011. Doc review. **Key finding: GAP-120, Working Plan V5 and the graybox have HUB and HUB 2 swapped east–west.** After merge ART fixes it (the SE exit goes on the furthest-east room, DEC-042c).
2. **Still working at handover** (read their handoffs/branches when they finish; they report to whoever is Hub):
   - GAME-002b slice polish (session `local_e574024b-b42a-4f12-b5db-6b6d66ac34bc`, fresh branch from main)
   - ART-003 retail lookdev (`local_392adc04-9603-4cc9-959c-6e3e2d792743`): also DEC-039/040/041/043 registers, desks, jar wall, lighting
   - PROC-002 jar canister + fill (`local_1b8fb899-d1dc-49d4-8384-8bc73da3e85a`): DEC-042/043 canister design
   - REF session `local_8e643693-f039-47b6-8392-365947ed9efc` (REF-004..007), idle once REF-007 is done; archive after W4C merges.
   Each finished task → its own REVIEW session → merge → archive.
3. Then: PERF-001 (unblocked; start once ≤2 Unity users), COMP-002, GAME-004 packaged assortment, a GAME task to hook PROC-002 fill into the slice jars, ART HUB/HUB 2 swap fix (GAP-120).
4. Nolan is away from the PC (23:40): contact him only if urgent. Otherwise brief him at milestones in the end-of-turn notes. The slice is playable on main (0032589).

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
- W3B notes: m1 reference graybox objects by name/anchor only (fileIDs churn on rebuild); m2 register count settled by DEC-039; m5 SE exit room (HUB vs HUB 2) open; m6 raw CCTV stills never ship in a build.
- Next REF follow-up (REF-005): read `COMPILED_Flower Shop_Int Set.pdf` for deli case/counter/jar sizes (GAP-108/113).
- Hub ruling: entry storefront width = 6'-0" per TI E101 / DEC-037 (door types/sizes from TI); ART follows it.
- Follow-up for BUILD: add the SliceCapture test to `studio.ps1 unity-capture` (GAME-002 open item).
- Done 2026-10-29: Nolan put the 3 TI/A011/A012 PDFs in Downloads; REF-005 imports them to `References/TI/` and render-checks the counter height.
- Batch for Nolan (store fact): a photo of a real receipt's tax lines would settle Phoenix TPT rate (OPEN-4); game keeps 25.1 % (DEC-001) meanwhile.
