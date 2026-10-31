# PROJECT BRIEF — the stable picture of Dispo Game

Hub-owned, guarded (`hub_guard.py`). This is the knowledge a fresh Hub needs before it reads live state; it changes only when a durable fact changes (milestone, structure, a new system). Live state is `PROJECT_STATE.md`; rules are `CLAUDE.md` and `STUDIO_OS.md` §0; the plan is `Design/ROADMAP_POST_SLICE.md`. Everything here cites where the detail lives; read the detail only when a decision needs it. ~2 minutes to read.

## 1. What we are building
A first-person **budtender simulation of one real Phoenix dispensary** (The Flower Shop, TFS) in **Unity 6000.6.7f1 + HDRP**, with assets generated procedurally in **Blender 5.2** and $0 third-party assets. The player works shifts: hears a customer's need in plain language, uses the store's real recommendation logic to pick deli-flower batches, weighs out, checks IDs and limits, sells, and keeps the store believable and compliant. Later: full shift days, packaged goods, careers, then a gated management layer (`MASTER_PLAN.md` §4, `GAMEPLAY_SIMULATION_SPEC.md`, roadmap §0).

**Core thesis to preserve:** "translate ordinary customer language into a small number of inventory-specific recommendations using current batch chemistry while hiding unnecessary complexity" (MASTER_PLAN §4.1). Complex backend, simple floor experience (§4.2). Observed facts never silently become inferred ones (§4.3).

## 2. Hard constraints (the DECs everyone must know)
- **Tool parity:** the local TFS budtender tool source `C:/Users/handl/Downloads/tfs-budtender` (v7.11.4, read-only, no PII, has its own hub) is the top authority for recommendation logic; the game never changes engine scoring; new logic is game design and lives in Simulation (DEC-001/002/006/060). The old Three.js game source is gone: `NO_SOURCE_RECONSTRUCTION_BASELINE.md`.
- **No invented store facts:** every store value cites a source or is a labelled GAP (DEC-047); layout and size questions are measured from the floor plan / TI drawings / CCTV before anyone asks (DEC-110); Nolan is never asked a question already answered or skipped (DEC-105).
- **Excluded content:** customer PII/CRM, security material (never open the Security folder, P&P manual, credential sheets), cash-handling equipment (DEC-006/031/051).
- **Quality bar:** realistic, LOD chains, 2K–4K PBR, never low-poly/generic; tri counts are guides not caps; automation checks mechanics, humans/reviewers judge the visual read (DEC-084/114/122). Reality outranks generic dispensary aesthetics.
- **Budget and tools:** $0 assets, licences per DEC-023/087; max 2 Unity editors at once (DEC-013); Unity worktrees max 3 (disk).
- **Git safety:** no broad branch/worktree cleanup; retire only what is positively identified as integrated or obsolete (DEC-123). Git identity for every commit: `git -c user.name=Nolan_Bradford -c user.email=handlebarn@gmail.com`.
- **Playtest gate:** no playtest build reaches Nolan until QA-004 records PASS for every still-relevant playtest-1 and playtest-2 item in the actual build (DEC-120).
- **Plan usage is Nolan's call:** never trim scope or pause work for usage limits; mention numbers if relevant (DEC-100). Throughput caps exist for review bandwidth and collision risk, not usage (DEC-140).

## 3. Nolan's standing directives (how he wants the studio run)
- The Hub is his **project manager and right hand with ultimate operational authority**: it decides routine technical and process questions itself and records them as DECs; it never asks permission for routine actions (starting/archiving sessions, merging, downloads) (DEC-025, DEC-139).
- **Escalate only** for: major decisions with substantial consequences; genuinely low confidence; conflicting evidence that cannot be resolved; his subjective product preference; an irreversible boundary (deleting work, public builds, spending, studio structure). Everything else: decide, record, continue.
- **Chain of command** (DEC-033/098): nobody below the Hub contacts Nolan; the chain routes, it never filters: every `FOR NOLAN` item reaches him. Questions go to the PO communication session, batched (DEC-125); blockers by push notification.
- "Run as a studio": staff dependency-ready work in parallel within the caps; "be smart about how you delegate". Don't ask him about delegation mechanics.
- **No chatter:** a message goes out only when the receiver must act; no FYI or acknowledgement messages (DEC-107). Hub replies to Nolan are short and lead with what needs him.
- **Archive patience:** archive a session only after it has finished and reported; one attempt. Workers nest under the Hub so heavy parents can be archived (DEC-133 items 2–3 survive).
- Imports: `<repo>/Dispo Game Imports/` holds only his fresh drops; after audit and integration a worker moves each to `<repo>/Dispo Game Imports Archive/<date>_<name>/` (DEC-070). ChatGPT drops never get our full context and are always audited (DEC-095); anything he drops is audited → reviewed → his approval before use.
- Microsoft 365 research is read-only (DEC-031). He is signed in to Sketchfab and the Unity Asset Store in the built-in browser pane (Warehouse/Office packs claimed).
- Realism vs fun (DEC-032): a real rule becomes a mechanic, automation, flavour or a cut. Tone: grounded deadpan humour played straight (DEC-101, `Design/TONE.md`).
- He plays a build after each milestone (DEC-085) and gives feedback as playtest reports (`Design/PLAYTEST*_2026-10-30.md`).

## 4. Where truth lives
| Need | Authority |
|---|---|
| Live state: in flight, queue, recovery, open Nolan items, builds | `PROJECT_STATE.md` (Hub writes it) |
| The plan: milestones, their task IDs, dependencies, critical path | `Design/ROADMAP_POST_SLICE.md` (DEC-119) |
| Task registry (ID, title, deps, state) | `BACKLOG.md`; a task's state = its packet folder `Tasks/Ready|Active|Done` (mirrored in the same commit) |
| Ratified decisions | `DECISIONS.md` (append-only; newest wins; grep the topic) |
| Unknowns / placeholders | `KNOWN_GAPS.md` (136 GAP rows) |
| Real-store facts and dimensions | `REFERENCES_INDEX.md`, `Reference/ROOM_FIXTURES.json`, `DOORS.json`, `SCENE_ANCHORS.json`, `References/` (floor plan, TI set, CCTV), `Research/`, Nolan's CCTV answers in `Handoffs/REF-008.md` |
| Recommendation logic | the TFS tool source, then `Reconstruction/` (contract, goldens, data schema) |
| Gameplay / UX specs | `Specs/` (SLICE_DESIGN, ENGINE, UX_SLICE, UX_PS1, UX_COUNTER_INTEL, CONTROLS_FLOW_PS1), `Design/SPEC_DECISION_PRESSURE.md` (wins over GSS), `Design/DESIGN_V2/` (add-on, DEC-063/066), `GAMEPLAY_SIMULATION_SPEC.md` |
| Asset pipeline | `Assets/Specs/PROC_PIPELINE.md`, `CHARACTERS.md`, `REGISTER_KIT.md`, `ASSET_PRODUCTION_PLAN.md` (realism rule), `Assets/LICENSE_LEDGER.md`, `Imports/IMP-00x_*.md` |
| Toolchain | `TOOLCHAIN_EXECUTION.md`, `Tools/Studio/studio.ps1` (doctor, unity-compile/test/build, slots), `MACHINE_PROFILE.md` |
| History (never edited after the fact) | `Handoffs/`, `Reviews/`, `Audits/`, `HISTORY.md`, git log |
Nothing is copied between these; packets and briefs cite path + §.

## 5. Systems map (what exists on `main`)
- **Code** `UnityProject/Assets/_Game/Code/`: `Domain/` (ported TFS engine: parser, recommender, pricing, exclusions, goldens; no engine references), `Simulation/` (shift, customers, patience, limits, IDs, jar fill), `Presentation/Slice/` (first-person counter, HUD, doors), `Editor/` (Graybox/Lookdev/Slice builders, StudioCI, ProjectSetup), `Tests/EditMode` (goldens, parser, Gate A parity, ProcArt import tests) and PlayMode.
- **Scenes:** Bootstrap loads Retail, BackRooms, Hub, Exterior, GameplaySystems, NPCs, Audio, Lighting additively. Graybox and lookdev rebuilt from audited references (REF-011/012/013/016, ART-007/008): registers with operator zones, three deli walls, HUB rooms, office, 15 doors, 42 scene anchors.
- **Blender pipeline** `Tools/Blender/`: `run_generator.py` + `proclib.py`/`proctex.py`, 19 generators (`generators/*.py`) driven by `params/*.json`, validation JSON per export, contact sheets in `Docs/Assets/Specs/`, FBX in `Art/Exports/Procedural/` (LFS) copied to `_Game/Art/Procedural/`. UV layout DEC-097 (uv2 lightmap, uv3 label, PROC-007 pending). Characters: MPFB2 pipeline, 60-customer roster (`characters/`).
- **Data:** catalog importer from Nolan's Dutchie export (PII-free whitelist), needs catalog + 564 golden parses (DATA-003); packaged catalog waits on his export (DATA-004, GAP-PKG-01).
- **Builds:** `<repo>/Dispo Game Builds/` (inside the repo root, gitignored; older docs write `Downloads/Dispo Game Builds/`): playtest 1 `slice-38b9e5c`, playtest 2 `playtest2-741bb43`; gates in `BUILD_STATUS.md`, perf in `PERF_BASELINE.md`. Same for `Dispo Game Imports/`, `Dispo Game Imports Archive/` and the 6.6 GB `Dispo Game Assets Cache/`.

## 6. Milestones (roadmap §2; state in BACKLOG)
PS1 Counter Decisions (done, playtest 2) → **M-B Believable store** (current: GAME-026 flow, REF-016 evidence matrix done, ART-013 layout overhaul, PROC-013 doors done, PROC-005 fixtures done, PROC-007/ART-011 UV cut-over, ASSET-005/006/007 characters, PROC-009 vehicles done, QA-004 gate, BUILD-008) → PS1b Customer Intelligence (GAME-017a → 017 → 018 → 019 → 020) → PS2 Full Shift Day → PS3 Packaged Floor (gated on Nolan's catalog export) → M-F Final look → M-G Ship-ready → PS4 Management (gated).
Ordering rule: shortest path to fun; fidelity work in parallel but never ahead of evidence (DEC-008/047/110). Playtest-1 priorities: controls (done) → layout accuracy → believable customer flow → recommendation depth → asset integration that unblocks these (DEC-096).

## 7. Glossary
TFS = The Flower Shop (the real store and its budtender tool) · GSS = `GAMEPLAY_SIMULATION_SPEC.md` · DP = decision-pressure spec · CF = `Specs/CONTROLS_FLOW_PS1.md` · RF = `ROOM_FIXTURES.json` · TI = tenant-improvement drawing set (A011/A901/A940…) in `References/TI/` · CCTV wall = Nolan's camera-wall screenshot, tiles `R<row>C<col>` · HUB / HUB 2 = the two back storage rooms (not the Studio Hub) · FOH/BOH = fulfilment and product-storage rooms · JC = janitor closet · PS1/PS1b/PS2… = play-slice milestones · Gate A = TFS parity test gate (QA-002) · PT1/PT2 = playtests 1 and 2.

## 8. People and sessions
Nolan Bradford (owner, handlebarn@gmail.com) talks to the Hub in the Hub chat and answers questions in the **PO communication session** `local_0e722850-d68d-43e0-85af-b280cf2337c4`. The TFS tool's own hub is the peer session "TFS tool: project hub (phases 1-7)": relay tool defects there, never edit its files. Machine: Windows 11 laptop, RTX 4050 6 GB, 32 GB RAM; Unity, Blender, Python 3.12, git-lfs; no gh, no pwsh 7 (`MACHINE_PROFILE.md`).
