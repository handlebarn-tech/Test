# BACKLOG

Priority P0 = vertical-slice critical path. State: Ready / Active / Review / Done / Blocked.

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
| QA-002b | P1 | Gate A pass with `ParserOptions.Game` + game003 defect queries (REVIEW-W4T m1, DEC-067) | QA-002 | Active |
| UX-005 | P1 | PS1b UX extension of `UX_PS1.md` (doc-only) | UX-002 | Done (W4S) |
| GAME-006 | P1 | Cart | GAME-005 | Review |
| GAME-017 | P1 | KNOWN profile, questions, query composer → QueryParser | GAME-006/007/010 | Ready (waits) |
| GAME-018 | P1 | Similar/Compare/Details at the counter | GAME-017 | Ready (waits) |
| GAME-019 | P1 | ServiceEvaluator, DecisionQuality, no-sales (DEC-052) | GAME-018 | Ready (waits) |
| GAME-020 | P1 | Telemetry, debug explanation, star gate | GAME-019 | Ready (waits) |
| REVIEW-PS1b | P1 | Review of PS1b | GAME-017..020 | Later |
| GAME-021 | P2 | Repeat-customer memory | PS1b | Ready (waits) |
| GAME-022 | P2 | Difficulty profiles | PS1b | Ready (waits) |
| GAME-023 | P2 | Spec §133 acceptance shift | GAME-011/012 (no packets) | Blocked (DEC-059) |
| GAME-024 | P2 | Career + save v1 | PS1b | Ready (waits) |
| DES-004 | P2 | PS2 design (was "DES-003" in ROADMAP) | PS1 | Later |
| IMP-001 | P1 | Audit DISPO_GAME_DESIGN_V2 import | — | Done (REVIEW-IMP1) |
| UX-002 | P1 | PS1 UX spec (`UX_PS1.md`) | DES-002 | Done (W4L) |
| ART-004 | P1 | HUB/HUB 2 mirror fix (with ART-003) | ART-003 | Done (W4F) |
| BUILD-004 | P1 | Hub guard hook (`Tools/Studio/hub_guard.py`, DEC-045) | — | Done (W4B) |
| REF-006 | P1 | Desks, SE exit, GAP-120 (with REF-007) | — | Done (W4C) |
| REF-007 | P1 | Deli jar spec / house-smalls jar dimensions | — | Done (W4C) |
| REF-009 | P1 | Apply DEC-051 to `ROOM_FIXTURES.json` | REF-008 | Done (W4R) |
| REF-009b | P1 | W4R m1–m5 + DEC-062 into `ROOM_FIXTURES.json` | REF-009 | Done (W4U) |
| GAME-007 | P1 | Purchase-limit meter + over-limit asks + strike ledger (COMP-002 §2) | GAME-006 | Ready |
| GAME-008 | P1 | ID-check events (COMP-002 §3) | GAME-007 | Ready |
| GAME-009 | P2 | Medical customers (COMP-002 §4) | GAME-007, **GAME-008** (same files; AUDIT-001 A3) | Ready |
| GAME-010 | P1 | Retune for tension + QA bot personas | GAME-005 (merge after GAME-006: both edit SliceConfig and Slice tests) | Active |
| GAME-011 | P1 | Shift phases + traffic curve + compressed clock (ROADMAP, no packet yet) | DES-004 | Later |
| GAME-012 | P1 | Deli restock loop (ROADMAP, no packet yet) | DES-004, ART-005 (ROADMAP ID, see DOC-002), DEC-055 | Later |
| GAME-013 | P2 | Opening/closing tasks + report v2 (ROADMAP, no packet yet) | GAME-011, GAME-020 | Later |
| GAME-014 | P1 | Packaged sales (ROADMAP, no packet yet) | GAME-007, DATA-002, ART-006 (ROADMAP ID, see DOC-002) | Later |
| GAME-015 | P1 | Non-flower recommendation (ROADMAP, no packet yet) | GAME-014, DEC-054 | Later |
| GAME-016 | P2 | Deals v1 (ROADMAP, no packet yet) | GAME-014 | Later |
| ART-006 | P1 | Back rooms graybox + lookdev from ROOM_FIXTURES rev3 + HDRP bud materials | REF-009, PROC-003 | Active |
| IMP-002 | P1 | Integrate the approved DISPO_GAME_DESIGN_V2 pack (DEC-063) into `Docs/Design/DESIGN_V2/` | IMP-001 | Done (W4V, DEC-066) |
| AUDIT-001 | P1 | Read-only .md audit + approval sheet (`Docs/Audits/`) | DES-003 | Done (DEC-064) |
| DOC-001 | P1 | Apply AUDIT-001 batches A–C (DEC-064), 2 phases | AUDIT-001; phase 2 after IMP-002 | Active |
| DOC-002 | P2 | AUDIT-001 batch D (risky: ART renumber, CLAUDE.md read list, REFERENCES_INDEX split, branch naming) | DOC-001; between waves only | Later |
| DOC-003 | P3 | AUDIT-001 batch E (Medium/Low cleanup) | DOC-001 | Later |
