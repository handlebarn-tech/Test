# BACKLOG

Priority P0 = critical path of the current milestone (`Design/ROADMAP_POST_SLICE.md` §2). States: **Ready** (packet in `Tasks/Ready`, prerequisites met) · **Active** (packet in `Tasks/Active`, worker launched) · **Done** (merged; packet in `Tasks/Done`) · **Blocked** (named blocker) · **Later** (registered, planned, no packet yet; the Hub writes the packet when its dependencies are Done) · **Dropped/Rejected** (reason). Milestone of each row: the roadmap §2 table. New legitimate work found in a handoff or review gets a row here (Later or Ready) before anything else happens to it.

The task registry: IDs, titles, dependencies (DEC-117). Hub-owned. **A task's state is its packet folder** (`Docs/Tasks/Ready|Active|Done`); the State column mirrors it and changes only in the same commit as the packet move. Live in-flight detail (session, branch, next step) is in `PROJECT_STATE.md`, not here. The ID prefix is a role label (REF, ART, GAME, PROC, …), not an owner.

| ID | P | Title | Depends on | State |
|---|---|---|---|---|
| REF-001 | P0 | Canonical reference index | — | Done |
| MIG-001 | P0 | Budtender reconstruction contract + triage | — | Done |
| BUILD-001 | P0 | Unity HDRP project, scenes, studio.ps1 | — | Done |
| REVIEW-W1 | P0 | Independent review of wave 1 | wave 1 | Done (GO with notes) |
| ART-001 | P0 | Measured graybox + QA-001 capture/PlayMode harness + test player | wave 1 (DEC-012) | Done |
| GAME-001 | P0 | DATA-001 importer + C# domain engine slice + golden tests | wave 1 (DEC-012) | Done |
| DES-001 | P0 | Vertical-slice design spec + GAME-002 draft packet | wave 1 | Done |
| UX-001 | P1 | Slice UX spec + wireframes (terminal, HUD, dialogue) | wave 1 | Done |
| ASSET-001 | P1 | $0 asset license ledger + acquisition list | — | Done |
| GAME-002 | P0 | Vertical-slice shift loop: customer intent → recommend UI → sale → inventory/visual change | ART-001, GAME-001, DES-001, UX-001 | Done |
| GAME-003 | P1 | Full NL parser port (all RC goldens), exclusions, compare, Similar | GAME-001 | Done |
| PERF-001 | P2 | Machine performance baseline in graybox | ART-001 | Done (W4J, 023f4b2) |
| PROC-001 | P1 | Blender headless wrapper + first generators (deli jar / package base) | — | Done |
| REVIEW-W2A | P0 | Review GAME-001 + PROC-001 | GAME-001, PROC-001 | Done (GO with notes) |
| REVIEW-W2B | P0 | Review DES-001 + UX-001 + ASSET-001 | DES/UX reconcile | Done (GO with notes) |
| REVIEW-W2C | P0 | Review ART-001 + commit HDRP-normalized ProjectSettings | ART-001 | Done (GO with notes) |
| ASSET-002 | P1 | Fetch P0 assets into shared cache (DEC-023) + LFS setup | ASSET-001 | Done |
| REF-002 | P0 | HUB CCTV evidence + register scale stand (DEC-019..022) | — | Done |
| REVIEW-W2D | P0 | Review REF-002 | REF-002 | Done (GO with notes) |
| REF-003 | P0 | Index back-of-register CCTV stills (scale stand) | — | Done |
| ART-002 | P1 | Graybox update: HUB rooms + register scale stands from REF-002 | REF-002, ART-001 merge | Done |
| RES-001 | P1 | Read-only research in Nolan's M365 (Outlook, OneDrive) for store facts | — | Done |
| COMP-001 | P0 | Arizona cannabis compliance review → gameplay changes (overselling etc.) | — | Done |
| REVIEW-W3A | P0 | Review GAME-003 + BUILD-002 | — | Done (GO with notes) |
| REVIEW-W3B | P0 | Review ART-002 + REF-003 (after ART-002 height/stand follow-up) | — | Done |
| REVIEW-W3C | P0 | Review COMP-001 + RES-001 + ASSET-002 | — | Done |
| REF-004 | P1 | Import TI drawing set + extract heights/counters (DEC-037) | RES-001 | Done |
| BUILD-002 | P2 | Build manifest (TOOLCHAIN §14) + fuller result schema (§8) | BUILD-001 | Done |
| REVIEW-W3D | P0 | Review GAME-002 slice (+ integrate GAME-003, ART-002 anchors) | GAME-002 | Done (GO with notes) |
| REVIEW-W3E | P1 | Review REF-004 | REF-004 | Done (PASS) |
| REF-005 | P1 | Deli case/counter/jar sizes + import TI PDFs, render-check counter | REF-004 | Done (W4A) |
| ART-003 | P1 | Hero retail lookdev: TI finishes (DEC-037, REFERENCES_INDEX §6), ASSET-002 cache, brand fonts | ART-002, REF-004, ASSET-002 | Done (W4F) |
| PROC-002 | P1 | Jar fill / bud system (Blender generators, 454 g jar, fill levels driving GAME-002 visuals) | PROC-001 | Done (W4E) |
| BUILD-003 | P2 | `studio.ps1`: SliceCapture in unity-capture; W3A n2 ms/PID stamp, n3 lock re-check, n5 dirtyPathCount | BUILD-002 merge | Done (W4B) |
| COMP-002 | P2 | Post-slice compliance mechanics: limit meter, ID-check events, medical customers (COMP-001 backlog) | slice merged | Later |
| GAME-004 | P2 | Packaged assortment (DEC-034): prepacks, prerolls, vapes, edibles | slice merged, PROC package gen | Later |
| GAME-002b | P1 | Slice polish: W3D N1 jar-label placement (windowed check), DEC-044 PriceFit on POS total, Results/Esc overlap, toast over report, MoreOptions guard | GAME-002 | Done (W4D) |
| GAME-005 | P1 | (Done, W4K) Hook PROC-002 fill meshes into slice jars: copy the jar FBX into Unity (or `unity_dir`), switch SliceBotTests to the step mapping (W4E m2), DEC-046 min pile | PROC-002, ART-003/004 merge | Done (W4K) |
| PROC-003 | P2 | DEC-046 F010 minimum visible pile; more bud jitter (W4E n1); smalls jar type once REF-007 values land | PROC-002 | Done (W4P, re-merged onto GAME-005, d1f2fe7) |
| BUILD-005 | P2 | (Review W4G) LFS rule for `Art/Exports/**/*.fbx` + `_Game/Art/Procedural/**/*.fbx` (W4E m3) | — | Done (W4G) |
| DES-002 | P1 | Post-slice roadmap + COMP-002/GAME-004 specs + next packets | slice merged | Done (W4H) |
| PROC-004 | P1 | Packaged-product generator family (DEC-034), generic labels | PROC-002 | Done (W4I) |
| REF-008 | P1 | Tile-by-tile CCTV map of Office, FOH, BOH (+ Break, Restroom/JC, halls) → ROOM_FIXTURES.json | — | Done (W4N) |
| ART-005 | P2 | W4F m1 2" top + m2 R2C3 panel clash; Retail_Lookdev in AdditiveScenes | ART-003/004 | Done (W4M) |
| DATA-002 | P1 | Packaged catalog importer from Nolan's Dutchie export (whitelist, PII-free, DEC-048/050) | DES-002 | Done (W4O) |
| DES-003 | P1 | Integrate Nolan's decision-pressure spec | — | Done (W4Q) |
| QA-002 | P1 | Gate A TFS parity gate + DP scenario harness (EditMode, new `Tests/EditMode/Gates/`) | DES-003 | Done (W4T) |
| QA-002b | P1 | Gate A pass with `ParserOptions.Game` + game003 defect queries (REVIEW-W4T m1, DEC-067) | QA-002 | Done |
| UX-005 | P1 | PS1b UX extension of `UX_PS1.md` (doc-only) | UX-002 | Done (W4S) |
| GAME-006 | P1 | Cart | GAME-005 | Done (W4W) |
| GAME-017 | P1 | KNOWN profile, questions, query composer → QueryParser | GAME-006/007/010 | Ready (waits) |
| GAME-018 | P1 | Similar/Compare/Details at the counter | GAME-017 | Ready (waits) |
| GAME-019 | P1 | ServiceEvaluator, DecisionQuality, no-sales (DEC-052) | GAME-018 | Ready (waits) |
| GAME-020 | P1 | Telemetry, debug explanation, star gate | GAME-019 | Ready (waits) |
| REVIEW-PS1b | P1 | Review of PS1b | GAME-017..020 | Later |
| GAME-021 | P2 | Repeat-customer memory | PS1b | Ready (waits) |
| GAME-022 | P2 | Difficulty profiles | PS1b | Ready (waits) |
| GAME-023 | P2 | Spec §133 acceptance shift | GAME-011/012 | Blocked (DEC-059: needs GAME-011/012 on main) |
| GAME-024 | P2 | Career + save v1 | PS1b | Ready (waits) |
| DES-004 | P2 | PS2 design (was "DES-003" in ROADMAP); 004b+c door lock + manager refill | PS1 | Done (W5L, merged d79e103) |
| IMP-001 | P1 | Audit DISPO_GAME_DESIGN_V2 import | — | Done (REVIEW-IMP1) |
| UX-002 | P1 | PS1 UX spec (`UX_PS1.md`) | DES-002 | Done (W4L) |
| ART-004 | P1 | HUB/HUB 2 mirror fix (with ART-003) | ART-003 | Done (W4F) |
| BUILD-004 | P1 | Hub guard hook (`Tools/Studio/hub_guard.py`, DEC-045) | — | Done (W4B) |
| REF-006 | P1 | Desks, SE exit, GAP-120 (with REF-007) | — | Done (W4C) |
| REF-007 | P1 | Deli jar spec / house-smalls jar dimensions | — | Done (W4C) |
| REF-009 | P1 | Apply DEC-051 to `ROOM_FIXTURES.json` | REF-008 | Done (W4R) |
| REF-009b | P1 | W4R m1–m5 + DEC-062 into `ROOM_FIXTURES.json` | REF-009 | Done (W4U) |
| REF-010 | P1 | Restroom storage cabinet placement (DEC-068) into `ROOM_FIXTURES` | ART-006 | Done (W5C) |
| REF-011 | P0 | Sales-floor layout audit: registers + operator access, HUB, deli walls, shelf fill (DEC-096) | — | Done (115292c) |
| REF-012 | P0 | Office walkability + door geometry audit; DOORS.json contract for Gameplay (DEC-096) | — | Done (115292c) |
| REF-013 | P0 | Settle GAP-129/130/132/134 from TI/floor-plan vectors; apply DEC-110 to DOORS | REF-011, REF-012 | Done (REVIEW-REF013b PASS; minors m1 schema note, m2 stale bulletin-board note → REF-015) |
| ART-007 | P0 | Graybox/lookdev rebuild from REF-011/012 (registers, HUB, deli walls, office, doors) | REF-011, REF-012 | Done (741bb43) |
| ART-008 | P0 | Graybox final pass on the REF-013 fix (rev8, DEC-115 hinges, clearance failures) | REF-013 fix (Done) | Done (REVIEW-ART008 PASS with minors; 108/114 clearance, 6 FAILs = GAP-131 data → REF-017; frame ruling DEC-136) |
| GAME-007 | P1 | Purchase-limit meter + over-limit asks + strike ledger (COMP-002 §2) | GAME-006 | Done |
| GAME-008 | P1 | ID-check events (COMP-002 §3) | GAME-007 | Done (W5N) |
| GAME-009 | P2 | Medical customers (COMP-002 §4) + W5N m2 queue strip | GAME-007, GAME-008 | Done (REVIEW-PS1, 054e159) |
| GAME-010 | P1 | Retune for tension + QA bot personas | GAME-005 (merge after GAME-006: both edit SliceConfig and Slice tests) | Done (W5M; 010b W5S) |
| UX-003 | P2 | Shift-day UX: phase banners, opening/closing task list, restock prompts, report v2 layout (SPEC_SHIFT_DAY) | DES-004 | Ready (waits PS1b, DEC-096) |
| GAME-011 | P1 | Shift phases + traffic curve + compressed clock | DES-004 | Ready (waits PS1b, DEC-096) |
| GAME-012 | P1 | Deli restock loop (re-scoped DEC-080) | DES-004, ART-005 (ROADMAP ID, see DOC-002), DEC-055 | Ready (waits PS1b, DEC-096) |
| GAME-013 | P2 | Opening/closing tasks + report v2 (GSS, SPEC_SHIFT_DAY §10; Income/Tax/Category/Rec-Med sections) | GAME-011, GAME-020 | Later |
| GAME-014 | P1 | Packaged sales: shelf stock authority, FOH fetch, cart lines, 5 g concentrate sub-cap + edible validator (SPEC_GAME004, COMP-002 §5) | GAME-007, DATA-004, ART-006 | Later (PS3) |
| GAME-015 | P1 | Non-flower recommendation: strain-linked items via the engine (parity), constraint match for the rest [GDD] (SPEC_GAME004 §4) | GAME-014, DEC-054 | Later (PS3) |
| GAME-016 | P2 | Deals v1: weekday category deals excluding deli (RES-001 P7/P8), values GAP; DP-025/026 acceptance | GAME-014 | Later (PS3) |
| DES-005 | P0 | Playtest 1 intake (DEC-096): controls + customer-flow spec, GAME-025/026 packets, World door/entry contract needs, long-term ideas proposal | — | Done (W5U, 5ab7aeb) |
| DES-006 | P0 | Recommendation depth audit: PS1b (GAME-017..020) vs the TFS tool, packet amendments | — | Done (REVIEW-DES6, 97ee06f) |
| DES-005b | P0 | Fold DEC-103 into CONTROLS_FLOW_PS1 + GAME-025/026; REVIEW-W5U m1–m3 (KNOWN_GAPS GAP-CF rows, GAP-DAY-04 basis) | DES-005 | Done (REVIEW-DES5b, abede71) |
| DES-007 | P2 | DEC-101: long-term rows into `ROADMAP_POST_SLICE.md` (Hub-delegated) + deadpan tone note for dialogue/event writers | DES-005 merge | Done (in DES-005b, abede71) |
| GAME-017a | P0 | First playable recommendation depth (+ PT2 #13: natural-language intent, modifiers/negations, no rigid menu) (cut from GAME-017, DES-006 §5): needs, read-it-as picker, parser route, Q9, reject→re-search | DES-006, DATA-003, UX-006, GAME-009, GAME-025 (same Presentation/Slice files), QA-002b Gate A | Ready (waits: GAME-026 merge; shared Slice files) |
| DATA-003 | P0 | Customer needs catalog + golden parses from the TFS tool (GAME-017a data) | DES-006 | Done (db43b6d) |
| UX-006 | P0 | Counter UX addendum: read-it-as picker, said cards, query preview | DES-006, DES-005 | Done (REVIEW-UX6, 5920ab2) |
| BUILD-007 | P0 | Playtest build 2 (PS1 complete) into `Downloads/Dispo Game Builds/` | GAME-009 | Done (playtest2-741bb43) |
| GAME-025 | P0 | Controls: camera/look feel, Esc pause menu, door interaction  | DES-005, GAME-009 merge, World REF-012 `DOORS.json` | Done (08758c1) |
| GAME-026 | P0 | Customer flow: guard ID check-in at entry, one line, player calls next  | DES-005, GAME-025, World REF-011 `SCENE_ANCHORS.json` | Active |
| GAME-027 | P0 | PT2 #11: budtender ID verification at the register works in the playable build (did GAME-008's events ever reach the player?); defect fix + PlayMode proof | GAME-026 (same Slice files) | Later (drop if GAME-026 proves it in a build) |
| ART-006 | P1 | Back rooms graybox + lookdev from ROOM_FIXTURES rev3 + HDRP bud materials | REF-009, PROC-003 | Done (W5A) |
| IMP-002 | P1 | Integrate the approved DISPO_GAME_DESIGN_V2 pack (DEC-063) into `Docs/Design/DESIGN_V2/` | IMP-001 | Done (W4V, DEC-066) |
| ASSET-003 | P1 | Customer characters + animations sourcing (CHARACTERS.md, DEC-084/087) | ASSET-001 | Done (W5P) |
| ASSET-004 | P1 | MPFB2 customer pipeline (DEC-087/089): 60-customer roster, generator, LODs | ASSET-003 | Done (976af6e, 18b66d1) |
| AUDIO-001 | P1 | Audio plan + CC0 sourcing (no Unity) | ASSET-001 | Done |
| BRAND-001 | P1 | Only approved brands ship (DEC-071) | DATA-002 | Done |
| BRAND-001b | P1 | Fictional-brand collision pass (DEC-078) | BRAND-001 | Done |
| BRAND-002 | P1 | Name search of all fictional names before any public build (DEC-078) | BRAND-001b | Later |
| IMP-003 | P1 | Rolling ChatGPT toolkit audit (DEC-070/083/095): drops 1–5, rebuilt round 3, rounds 4–6 | — | Done (e0fc82c, DEC-111); a future drop gets a new IMP task |
| PROC-005 | P1 | Integrate the approved toolkit + fix every checklist item (DEC-092) | IMP-003 | Done (REVIEW-PROC005d r4 PASS with minors; SWR facing DEC-137; GAP-PROC-14..42; m1/m5 → PROC-005b, m4 → PROC-007) |
| PROC-005b | P2 | PROC-005 follow-ups: R7 `components.scale_stand_slot` exports inside the South run; give SouthWestReturn a per-station dx override so the stand lands at the operator's **left** per RF POS_07 `stand_rect` (x 17.78–19.08, y 24.0–25.6; REVIEW-PROC005d m1), before ART-011/013 place stands from the manifest; also the still-owed HDRP material builder reading `finishes` and the `to_unity`/BoxCollider EditMode test (m5) | PROC-005 | Later (ART-013 reads POS_07 `stand_rect`, not the manifest slot, until this lands) |
| PROC-006 | P1 | Register workstation kit: evidence spec (DEC-096) | — | Done (6af8906); generators = PROC-006b |
| PROC-006b | P1 | Register kit generators + seeded per-station variation (DEC-104) | PROC-006 | Done (e1e8a68; REVIEW-PROC006b PASS, 7 minors → PROC-006c / PROC-010 / PROC-007) |
| PROC-006c | P2 | Register kit review follow-ups (REVIEW-PROC006b m2–m6: contact sheet, hanging ISO spray, keyboard GAP tags, stale anchor strings, GAP ids for KNOWN_GAPS) | PROC-006b | Done (REVIEW-PROC006c PASS @ 53de5ff; m2 stations-sheet labels + m3 colour-true previews → PROC-010) |
| PROC-007 | P1 | DEC-097 UV layout (lightmap ch1, label ch2) + re-export jars/packaged goods, with World's label-shader cut-over | PROC-005 | Ready, dispatch now (PROC-005 merged; also: RegisterKit FBX `.meta`/first import, REVIEW-PROC006b m7; PROC-005 texture `.meta` import settings: `_Normal` as normal map, `_Mask` sRGB off, REVIEW-PROC005d m4) |
| PROC-008 | P2 | Cash-drawer tray (R3b.6) | — | Rejected (Hub ruling: DEC-051/086 win; cash equipment is never modelled) |
| PROC-009 | P2 | Studio-built parked vehicles (DEC-111; R3b.7 rejected as built): CC0 source (DEC-023) or a rebuild per checklist R3b.7 | PROC-005 core (merged) | Done (REVIEW-PROC009 r3 PASS with minors; count rule DEC-134, class rule DEC-135; minors → PROC-009b, textures/lightmap UV → PROC-016) |
| PROC-009b | P3 | Parked-vehicle look follow-ups (REVIEW-PROC009 r3 m1–m4): carry the sedan dark headlamp housing to LOD2; make the wrapped lamp lens read at 3/4; hatchback mesh grille cells readable at LOD0 (not a solid black block); Hub to confirm the shared `run_generator.py` preview-camera change (r1 m4) | PROC-009 | Later |
| PROC-016 | P1 | Shared unwrap + texture-bake pipeline (Q0.2/Q0.3): DEC-084 2K–4K PBR maps and DEC-097 lightmap UV ch1 for studio-built PROC assets; first users the parked vehicles and the PROC-013 doors (lightmap UV not delivered: `proclib.finish_object` and the runner UV check allow only `UVMap_Main`/`UVMap_Label`; re-export all `PROC_Door_*`, REVIEW-PROC013 m1) (tread/sidewall normals, dust/grime, GAP-PROC-24; REVIEW-PROC009 r1 m1/m2) | PROC-007 | Later |
| ASSET-005 | P1 | Studio-built customer wardrobe (DEC-111; R4.1 rejected as built): MPFB2 CC0 clothes, or procedural shells per R4.1, keeping the drop's garment list and colourways | ASSET-004 | Active (with ASSET-006, one session) |
| ASSET-006 | P1 | Studio-built hair (DEC-111; R4.2 rejected as built): MPFB2 CC0 hair or alpha card clumps per R4.2, keeping the 9-style list | ASSET-004 | Active (in the ASSET-005 packet and session) |
| ASSET-007 | P2 | Studio-built nitrile glove overlay (DEC-111; R4.7 rejected as built): hand vertex-group mask or a CC0 glove proxy | ASSET-004 | Done (REVIEW-ASSET007 PASS, 8 minors → ASSET-007b; colour/wear DEC-126/127) |
| ASSET-007b | P1 | Glove look follow-ups (REVIEW-ASSET007 m1–m6): fine nitrile micro-texture instead of mottling, LOD3 cuff, thumbnail read, posed-hand deformation proof, warn when `gloves` lacks `nitrile_gloves` in subdiv_parts, share the glove maps. Strong visual review (DEC-122: player-facing at the register) | ASSET-007, ASSET-005 | Later (before ASSET-008) |
| AUDIT-001 | P1 | Read-only .md audit + approval sheet (`Docs/Audits/`) | DES-003 | Done (DEC-064) |
| DOC-001 | P1 | Apply AUDIT-001 batches A–C (DEC-064), 2 phases | AUDIT-001; phase 2 after IMP-002 | Done (W4X) |
| DOC-002 | P2 | AUDIT-001 batch D (risky: ART renumber, CLAUDE.md read list, REFERENCES_INDEX split, branch naming) | DOC-001; between waves only | Later |
| DOC-003 | P3 | AUDIT-001 batch E (Medium/Low cleanup) | DOC-001 | Done (W4Z) |
| BUILD-008 | P0 | Playtest build 3 (M-B exit): candidate build for QA-004; reaches Nolan only after QA-004 PASS (DEC-120) | GAME-026, ART-008, ART-013, PROC-013, PROC-006b (Done) | Later (packet when those merge) |
| ART-011 | P1 | Lookdev label shader reads Unity `uv3` (DEC-097); lands in the same wave as PROC-007 | PROC-007 | Ready to dispatch (packet `Tasks/Ready/ART-011.md`; PROC-005 merged; builds on PROC-007's accepted commit; integrated in one wave with PROC-007) |
| GAME-CHR-002 | P1 | Import the 60 MPFB customers into Unity: prefabs, LODs, Humanoid retarget of the Rocketbox animation map (CHARACTERS.md §6–7) | ASSET-005, ASSET-006, ASSET-007 | Later (PS1b) |
| NPC-001 | P1 | Customers walk the GAME-026 flow with bodies: NavMesh (AI Navigation), entry → guard → queue → counter → exit, idle/wait/talk animation states | GAME-026, GAME-CHR-002 | Later (PS1b) |
| BUILD-008b | P0 | Playtest build 4 (PS1b exit) | GAME-020, NPC-001 | Later |
| ART-009 | P1 | BOH/HUB stock dressing + restock anchors for the manager refill (racks per DEC-041, backstock GAP-DAY-02); was ROADMAP "ART-005" (renumbered, DOC-002) | ART-007, PROC-005 | Later (PS2, before GAME-012) |
| NPC-002 | P1 | Ambient staff NPCs: guard at the stand, GM assigning registers (DEC-079), second budtender; SPEC_SHIFT_DAY §5 | ASSET-008, NPC-001, GAME-011 | Later (PS2) |
| ASSET-008 | P1 | Staff characters: separate MPFB roster in the DEC-089/113 uniform (green tee, print wearer's left chest), guard set (CHARACTERS.md §9) | ASSET-005, ASSET-006, ASSET-007b | Later (PS2) |
| AUDIO-002 | P1 | Unity integration of the AUDIO-001 plan: mixer groups, ducking, slice/PS1 cues, PS2 rush layers | AUDIO-001, GAME-011 | Later (PS2) |
| UI-001 | P2 | Settings menu off the Esc pause: four mixer volumes, mouse sensitivity, invert, key hints (AUDIO_PLAN §1, GAME-025) | AUDIO-002 | Later (PS2) |
| PERF-002 | P2 | Perf pass with a full-day NPC count against PERF_BASELINE budgets | GAME-011, NPC-002 | Later (PS2) |
| DATA-004 | P1 | Real packaged catalog from Nolan's Dutchie/LeafLogix export through the DATA-002 importer (PII-free, DEC-048/050); replaces every PLACEHOLDER SKU (GAP-PKG-01) | Nolan provides the export | Blocked (FOR NOLAN, asked once; PS3 gate) |
| UX-004 | P2 | Packaged UX: category tabs, format/dose filter, packaged cards, cart lines (SPEC_GAME004) | DATA-004 | Later (PS3) |
| PROC-010 | P1 | Toolkit families phase 2 (+ IMP-004 A3: thermostat, wet-floor sign, black fire-extinguisher cabinets; A4: state variants, rigged moving parts) = PROC-005 handoff "Left, in order": architecture kit, exterior, ladder, display cases, clutter (incl. playtest-1 register details: spray bottle, rag, bins), stocking arranger with uneven fill, labels, materials (incl. register-kit 2K PBR and colour-true, labelled sheets, REVIEW-PROC006b m1 / REVIEW-PROC006c m2–m3; REF-016: kit wire-bin width ≈0.35 m, height 0.36 m kept, to match ROOM_FIXTURES `Trash_Small_POS_*`), ID stand/bags/signs | PROC-005 PASS, PROC-007 | Later (split into packets at PROC-005 review; carved out already: PROC-013 doors, PROC-017 entry/queue kit, PROC-018 HUB 2 cabinets + refill station) |
| PROC-012 | P2 | Bud/nug look pass (playtest 1: "nugs still look off"): PROC-003 follow-up at DEC-084 | PROC-007 | Later (M-F) |
| REF-015 | P2 | Exterior envelope, parking, fence and approach evidence from A011/A012, CCTV R1C1–C5/R3C1 and BAND photos → REFERENCES_INDEX §9 + ROOM_FIXTURES exterior rows; GAPs for what no source shows; the stale bulletin-board note (REVIEW-REF013b m2) was fixed in REF-016. Carries REF-016a | — | Ready (pulled forward: no deps, no Unity) |
| REF-016 | P0 | Canonical store-evidence matrix (DEC-120 (2)): every fixture/zone row has source, confidence, dims/placement/orientation, served side, current implementation, gaps. It settles the south-side register count, Register 7, register-area facing and the emergency-exit wall (PT2 #3, 4, 6, 8, 9) | REF-013 | Done (REVIEW-REF016 FAIL → fix round; REVIEW-REF016-r2 PASS with minors n1–n3 → REF-016a) |
| ART-013 | P0 | Store layout overhaul in Unity from REF-016: register count/positions, facing and served side, placeholder footprints, jar density (DEC-121), door audit + wall sealing incl. emergency exit, glass storefront (PT2 #1, 3–9). Work list = REFERENCES_INDEX §9.3 (REF-016 handoff "ART-013 must also": remove the rev7 south north arm, rebuild the south run and west return per rev8/rev9, move stations and anchors, sink to the south wall, seal the exit (hinge N, rough opening + jambs), entry and ID stand to A011, printers on the staff half, outstanding REF-013 items). Unity implementation review in the assembled scene (DEC-120 (3)) | REF-016 (Done), ART-008, PROC-013 (Done) | Ready (packet `Tasks/Ready/ART-013.md`; ART-008 merged, ready to dispatch; route note REVIEW-ART008 m2; door geometry from the manifest `PROC_Door_*` rows, FBX at `Art/Exports/Procedural/PROC_Door_*.fbx`) |
| REF-016a | P3 | REVIEW-REF016-r2 minors: n1 align row-level `confidence` (POS_02..07 still Med) with `matrix.conf.position` Low; n2 reword §9.1 so CCTV is the deciding source for south x and the run-length shift only supporting; n3 R2C5 view direction "NW" (§2) vs "W" (§9.1) | REF-016 | Ready (rides in the REF-015 packet) |
| REF-017 | P1 | South POS REF data from ART-008 (REVIEW-ART008 m3, GAP-131): narrow the POS_07/02/03/04/05 operator zones (3.4 ft) to the station pitch (3.2 ft) or re-measure the pitch; POS_02 `behind_stand` 5.2 → 3.2 ft (south back counter under the stand), or move the stand 0.22 ft east if a drawing supports it. Clears the last 6 `--check` FAILs | REF-016 (Done) | Later (fold into ART-013 if its worker reaches it first) |
| REF-018 | P2 | Re-base the retail frame to the 30.5 ft A011 depth (DEC-136): y +1.5 ft for everything south of the retail mid-floor in ROOM_FIXTURES/DOORS/SCENE_ANCHORS, back rooms and HUB; then re-run `room_fixtures_layout.py`. Moves Gameplay anchors by name | ART-013, GAME-026 | Later |
| GAME-026b | P2 | Lift the REVIEW-ART7 m3 rule keeping NPCs off `Anchor_Door_JC_*` (both JC anchors reachable since ART-008); re-check routes that assumed a direct floor-to-arch path (rev8 SW return closes it; REVIEW-ART008 m2) | GAME-026, ART-008 (Done) | Later |
| DOC-005 | P3 | LFS guard (REVIEW-ART008 m1): `studio.ps1 doctor` (or every unity-* command) fails on LFS pointer files under `Assets`. Also commit the untracked register-kit `.meta` files from the Unity import (REVIEW-ART7 m4; the PROC-005 Fixtures metas landed with PROC-005) | — | Later |
| PROC-013 | P1 | Door family at DEC-084: transparent glass aluminium storefront pair, interior/hall/emergency doors with frames and hardware per DOORS.json (PT2 #1, #7); carved out of the PROC-010 architecture kit | REF-013, PROC-005 core | Done (REVIEW-PROC013 PASS with minors; GAP-DOOR-1..9 registered; lightmap UV ch1 → PROC-016; minors → PROC-013b) |
| PROC-013b | P3 | Door follow-ups (REVIEW-PROC013 m2/m4/m5): the ART-013 packet export path (done in the packet: `Art/Exports/Procedural/PROC_Door_*.fbx`; a runner `export_dir` param stays optional for PROC-016); revisit the Hall_Break closer mount side with the hardware pass (GAP-DOOR-1); add a closed-state elevation tile to the door sheets (Entry meeting stile/astragal). m6 (LOD0 leaf tris below the DEC-084 guide) accepted under DEC-114 | PROC-013 | Later |
| PROC-014 | P1 | DEC-091 R7 QA tooling (DEC-095, studio-built): labelled review-render set per asset class in `run_generator` (orthos + 3/4 clay, 3/4 material, optional wire; DEC-122) + planted-fault tests in `test_validation.py` (axis order, collision key, runtime error in `build()`); also add the PROC_PIPELINE "Authoring order and script rules" section (IMP-004 audit §4 A1) | PROC-005 | Later |
| PROC-015 | P1 | North/east-wall sales-floor anchors at DEC-084: living-wall backing + foliage clusters, TFS lettering (DEC-071), rounded merch rack, deli hand-wash sink, generic closed ATM shell (DEC-131); sizes from RI §1.5 / REF-016; strong visual review | REF-016, PROC-005 (core merged; new generator file only, rebases onto the fix round) | Ready |
| PROC-017 | P1 | Entry and queue kit at DEC-084: ID-check stand + guard scanner (checklist §20 I1), queue stanchions (R3b.3), kraft exit bag (R5.3); carved out of PROC-010 | PROC-005 core (merged) | Ready |
| PROC-018 | P1 | HUB 2 black storage cabinets (R3b.2) + deli refill station: prep cart, canister shelf, refill scale (R3b.1, DEC-079); carved out of PROC-010 | PROC-005 core (merged) | Ready |
| QA-004 | P0 | Playtest-3 gate (DEC-120 (1)): requirement list from PT1 + PT2, each PASS/FAIL in the BUILD-008 candidate player, with evidence (captures, steps). A major FAIL blocks Nolan's build | BUILD-008 candidate | Later |
| IMP-004 | P1 | Audit the new import `Downloads/Dispo Game Imports/Bender & Asset new plan.md` (and confirm the older subfolders are the IMP-003 rounds already audited) against canonical state; propose adopt/reject per item into existing tasks/DECs/GAPs (DEC-070/095) | — | Done (REVIEW-IMP004 PASS; adoptions per DEC-131; imports archive awaits Nolan OK, DEC-070) |
| ART-012 | P2 | Exterior and parking lot from REF-015: façade, lot striping, fence/gate, HVAC, vegetation, night wall packs (M-9) | REF-015, PROC-009, PROC-010 | Later (M-F) |
| ART-010 | P1 | Lived-in pass (DEC-096/104, playtest 1): placement variation, partly used supplies, uneven stocking, cleaning and personal items in believable places, restroom-cabinet supplies | PROC-010, ART-008 | Later (M-F) |
| LIGHT-001 | P1 | Final lighting/lookdev: day and night looks, BOH look, glass/reflections/decals, material consistency (M-7) | ART-010, ART-012 | Later (M-F) |
| PERF-003 | P1 | (+ IMP-004 A4: LOD/impostor + atlas pack) Final optimisation pass: LODs, batching, lightmaps, memory; performance report (M-10) | LIGHT-001 | Later (M-G) |
| QA-003 | P1 | Final regression: every gate, every DP test, scene load, no missing references; final issue list (M-10) | PERF-003 | Later (M-G) |
| BUILD-009 | P1 | Release packaging: build settings, version, clean state docs (M-10) | QA-003, BRAND-002 | Later (M-G) |
| DATA-005 | P2 | Re-import the TFS tool at v7.11.5, regenerate goldens, diff parity (GAP-210) | TFS ships v7.11.5 | Blocked (external) |
| LT-1a | P3 | Presentation-only parking lot: cars come and go with arrivals (LT §1) | ART-012, PROC-009, GAME-011 | Later (M-F) |
| LT-1b | P3 | Parking-lot throughput as pressure (LT §1) | LT-1a, PS4 | Later (PS4) |
| LT-2a | P2 | Start screen: difficulty select (LT §2) | GAME-022 | Later (PS2) |
| LT-2b | P3 | Start screen: character customisation / role select (LT §2) | GAME-CHR-002, ASSET-008 | Later (M-F) |
| LT-3 | P2 | Store condition over the day: per-zone mess state, closing looks different from opening (LT §3) | GAME-011, GAME-013, PROC-010 | Later (PS2) |
| LT-4 | P3 | Coworker personality traits (LT §4) | NPC-002, PS4 | Later (PS4) |
| LT-5 | P2 | TV ad wall: render-texture slideshow, approved/fictional brands, no effect claims (LT §5) | TV-wall fixture (PROC-010) | Later (M-F) |
| LT-6a | P3 | Break room ambient props (LT §6) | ART-010 | Later (M-F) |
| LT-6b | P3 | Break room NPC use and breaks (LT §6) | NPC-002, PS4 | Later (PS4) |
| LT-7 | P3 | Neighbourhood activity: traffic, pedestrians, deliveries, weather (LT §7) | ART-012, LT-1a | Later (M-F) |
| LT-8 | — | Tone pillar adopted (`Design/TONE.md`, DEC-101) | — | Done (DES-005b) |
| DOC-004 | P3 | Put "fast recommendation" back in GSS §28 (DEC-059 n1, REVIEW-W4Q); rides with the next GSS edit | — | Done |
