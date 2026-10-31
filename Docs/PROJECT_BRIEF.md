# PROJECT BRIEF — the stable picture of Dispo Game

Hub-owned, guarded (`hub_guard.py`). The high-level model a fresh Hub needs before it reads live state: what the game is, what exists, what is planned, why the current work is the right work. It changes only when a durable fact changes (milestone, structure, a system's state). Live state is `PROJECT_STATE.md`; rules are `CLAUDE.md` and `STUDIO_OS.md` §0; the plan with task IDs is `Design/ROADMAP_POST_SLICE.md`. Everything here cites where the detail lives; read the detail only when a decision needs it. ~4 minutes to read.

## 1. What game we are building
A **first-person budtender simulation of one real Phoenix dispensary** (The Flower Shop, TFS) in **Unity 6 + HDRP**, assets generated procedurally in **Blender 5.2**, $0 third-party assets. The source of the game's intelligence is the store's real recommendation tool, ported in parity.

**Player fantasy (GSS §3):** "Read a customer, understand what they actually want, find the right product from real current inventory, serve them efficiently, keep the floor stocked, and survive increasingly busy shifts inside a living dispensary." The player starts as a budtender on shift; management responsibility is later progression, never a prerequisite.

**Intended experience:** a customer speaks like a person, not a query; the player interprets, asks the right follow-ups, searches the tool's way, reads the cards, weighs out deli flower, checks ID and limits, rings it up; the queue, the clock and the stock push back; the store visibly changes through the day. Expert play is judgment, prioritisation and foresight, not picking the top card (`Design/SPEC_DECISION_PRESSURE.md` §1). Humour is grounded and deadpan, produced by the simulation and played straight (`Design/TONE.md`, DEC-101).

**Pillars (GSS §4):** fast human interpretation · inventory truth (you can only sell what exists) · batch matters · physical work matters · knowledge helps but does not bury the player · rush pressure changes decisions · the store visibly changes · realism without administrative bloat. **Product thesis to preserve (MASTER_PLAN §4.1):** translate ordinary customer language into a few inventory-specific recommendations using current batch chemistry while hiding complexity; complex backend, simple floor experience; an inference never silently becomes an observed fact.

## 2. Hard constraints (the DECs everyone must know)
- **Tool parity:** the local TFS budtender tool source `C:/Users/handl/Downloads/tfs-budtender` (v7.11.4, read-only, no PII, has its own hub) is the top authority for recommendation logic; the game never changes engine scoring; new logic is game design and lives in Simulation (DEC-001/002/006/060). The old Three.js game source is gone: `NO_SOURCE_RECONSTRUCTION_BASELINE.md`.
- **No invented store facts:** every store value cites a source or is a labelled GAP (DEC-047); layout and size questions are measured from the floor plan / TI drawings / CCTV before anyone asks (DEC-110); Nolan is never asked a question already answered or skipped (DEC-105).
- **Excluded content:** customer PII/CRM, security material (never open the Security folder, P&P manual, credential sheets), cash-handling equipment, real auth (DEC-006/031/051; MASTER_PLAN §6).
- **Quality bar:** realistic, LOD chains, 2K–4K PBR, never low-poly/generic; tri counts are guides not caps; automation checks mechanics, reviewers judge the visual read (DEC-084/114/122). Reality outranks generic dispensary aesthetics.
- **Budget and tools:** $0 assets, licences per DEC-023/087; max 2 Unity editors at once (DEC-013); Unity worktrees max 3 (disk). Concurrency: 4 worker/reviewer sessions or background Agents plus the Hub; model by the character of the work (DEC-140/143/151).
- **Git safety:** no broad branch/worktree cleanup; retire only what is positively integrated or obsolete (DEC-123). Git identity for every commit: `git -c user.name=Nolan_Bradford -c user.email=handlebarn@gmail.com`.
- **Playtest gate:** no playtest build reaches Nolan until QA-004 records PASS for every still-relevant playtest-1 and playtest-2 item in the actual build (DEC-120).
- **Plan usage is Nolan's call:** never trim scope or pause work for usage limits; mention numbers if relevant (DEC-100). Caps exist for review bandwidth and collision risk, not usage.

## 3. Nolan's standing directives (how he wants the studio run)
- The Hub is his **project manager and right hand with ultimate operational authority**: it decides routine technical and process questions itself and records them as DECs; it never asks permission for routine actions (starting/archiving sessions, merging, downloads) and never makes progress depend on his messages (DEC-025/139/149).
- **Escalate only** for: major decisions with substantial consequences; genuinely low confidence; conflicting evidence that cannot be resolved; his subjective product preference; an irreversible boundary (deleting work, public builds, spending, studio structure). Everything else: decide, record, continue.
- **Chain of command** (DEC-033/098): nobody below the Hub contacts Nolan; the chain routes, it never filters: every `FOR NOLAN` item reaches him. Questions reach him batched in the Hub's `FOR NOLAN` reply block until he designates a new PO session (DEC-144); blockers by push notification.
- "Run as a studio": staff dependency-ready work in parallel within the caps; "be smart about how you delegate". Don't ask him about delegation mechanics. Isolated sessions are the normal execution path; background Agents only after the app refuses a session start, inside the same cap (DEC-151).
- **No chatter, no polling:** a message goes out only when the receiver must act; no FYI or acknowledgement messages; no recurring crons or status requests (DEC-107/149).
- **Archive patience:** archive a session only after it has finished and reported; one attempt. Workers nest under the Hub so heavy parents can be archived (DEC-133 items 2–3).
- Imports: `<repo>/Dispo Game Imports/` holds only his fresh drops; after audit and integration a worker moves each to `<repo>/Dispo Game Imports Archive/<date>_<name>/` (DEC-070). ChatGPT drops never get our full context and are always audited (DEC-095); anything he drops is audited → reviewed → his approval before use.
- Microsoft 365 research is read-only (DEC-031). He is signed in to Sketchfab and the Unity Asset Store in the built-in browser pane (Warehouse/Office packs claimed).
- Realism vs fun (DEC-032): a real rule becomes a mechanic, automation, flavour or a cut.
- He plays a build after each milestone (DEC-085) and gives feedback as playtest reports (`Design/PLAYTEST*_2026-10-30.md`); his playtest-1 priorities: controls → store/layout accuracy → believable customer flow → recommendation depth → asset integration that unblocks these (DEC-096).

## 4. Where truth lives
| Need | Authority |
|---|---|
| Live state: in flight, queue, recovery, open Nolan items, builds | `PROJECT_STATE.md` (Hub writes it) |
| The plan: milestones, their task IDs, dependencies, critical path | `Design/ROADMAP_POST_SLICE.md` (DEC-119) |
| Task registry (ID, title, deps, state) | `BACKLOG.md`; a task's state = its packet folder `Tasks/Ready|Active|Done` (mirrored in the same commit) |
| Ratified decisions | `DECISIONS.md` (append-only; newest wins; grep the topic; superseded chains in `HISTORY.md`) |
| Unknowns / placeholders | `KNOWN_GAPS.md` (136 GAP rows) |
| Real-store facts and dimensions | `REFERENCES_INDEX.md`, `Reference/ROOM_FIXTURES.json`, `DOORS.json`, `SCENE_ANCHORS.json`, `References/` (floor plan, TI set, CCTV), `Research/`, Nolan's CCTV answers in `Handoffs/REF-008.md` |
| Recommendation logic | the TFS tool source, then `Reconstruction/` (contract, goldens, data schema) |
| Gameplay design | `GAMEPLAY_SIMULATION_SPEC.md` (GSS, the base) < `Design/SPEC_DECISION_PRESSURE.md` (DP, ratified DEC-057, wins over GSS) < `DECISIONS.md`; `Design/DESIGN_V2/` is an add-on (DP wins, DEC-063/066); `Design/SPEC_SHIFT_DAY.md`, `SPEC_COMP002.md`, `SPEC_GAME004.md` per system; `Specs/` (SLICE_DESIGN, ENGINE, UX_*, CONTROLS_FLOW_PS1) for what is built |
| Asset pipeline | `Assets/Specs/PROC_PIPELINE.md`, `CHARACTERS.md`, `REGISTER_KIT.md`, `ASSET_PRODUCTION_PLAN.md` (realism rule), `Assets/LICENSE_LEDGER.md`, `Imports/IMP-00x_*.md` |
| Toolchain | `TOOLCHAIN_EXECUTION.md`, `Tools/Studio/studio.ps1` (doctor, unity-compile/test/build, slots), `MACHINE_PROFILE.md` |
| History (never edited after the fact) | `Handoffs/`, `Reviews/`, `Audits/`, `HISTORY.md`, git log and the tag `pre-recovery-2026-10-30` |
Nothing is copied between these; packets and briefs cite path + §.

## 5. Systems map and state (what exists, what is partial, planned, deferred, rejected)
"Exists" = merged on `main` and in a played build. Milestone codes are §6. Detail: roadmap §2–§3, BACKLOG rows.
| System | State | Where it stands / next |
|---|---|---|
| **Recommendation engine** (ported TFS parser, scoring, pricing, exclusions, Similar/Compare; `Code/Domain/`) | **Exists**, parity Gate A green (QA-002) | Refine chip port as its own task (DEC-118 B1); re-baseline on TFS v7.11.5 when it ships (DATA-005, blocked external) |
| **Customer intelligence** (hear → interpret → ask → search the tool's way → read cards → react; DP spec) | **Partial**: chip intents + cards in the slice; natural-language intent, needs catalog and 564 golden parses (DATA-003) ready | GAME-017a (first playable depth, PT2 #13) then GAME-017 → 020 = **PS1b**; Nolan's top gameplay concern (DEC-096 #4) |
| **Customer flow** (guard ID scan at the door, one line, "Next guest!", ID again at the register) | **In progress**: GAME-026 (4 review rounds so far); rules DEC-103/109 | GAME-027 only if the register ID check is not proven in a build; bodies and walking come with GAME-CHR-002 + NPC-001 |
| **Counter transaction** (assisted weigh, cart, purchase-limit meter, strikes, ID-check events, medical customers, tax, POS, jar fill/LOW/SOLD OUT, shift report) | **Exists** (PS1, playtest 2) | tuning only; QA bot personas exist (GAME-010) |
| **Controls and doors** (always-on mouse look, Esc pause, Backspace back, doors from `DOORS.json`) | **Exists** (GAME-025) | settings menu UI-001 (PS2); PROC door models placed by ART-013 |
| **Store world** (graybox + lookdev of every room from audited references: registers with operator zones, three deli walls, HUB rooms, office, 15 doors, 42 anchors) | **Exists**; **layout overhaul in progress** (ART-013 on the REF-016 evidence matrix, PT2 #3/4/8/9) | exterior REF-015 partial → ART-012 (M-F); lived-in pass ART-010, final lighting LIGHT-001 (M-F); retail depth re-base REF-018 |
| **Procedural asset pipeline** (`Tools/Blender/`: 19 generators, validation, contact sheets, LFS FBX → Unity) | **Exists**: jars + fill, packaged goods, wire shelving, 8 fixture families, register kit, 28 door parts, parked vehicles | UV cut-over PROC-007 → ART-011; QA render tooling PROC-014 (partial); bake pipeline PROC-016; phase-2 families PROC-010; bud look PROC-012 (M-F) |
| **Characters** (MPFB2 60-customer roster, gloves) | **Partial**: roster exported, gloves done; wardrobe + hair ASSET-005/006 WIP; nothing in Unity yet | GAME-CHR-002 import → NPC-001 customers in the flow; staff ASSET-008 → NPC-002 (PS2) |
| **Shift day** (compressed 08–22 clock, traffic curve, manager refill restock, opening/closing, repeat customers, difficulty, career + save) | **Planned, specified** (DES-004 `SPEC_SHIFT_DAY.md`, DP, V2) | **PS2**: GAME-011/012/013/021/022/024, UX-003, GAME-023 acceptance shift |
| **Packaged floor** (prepacks, prerolls, vapes, edibles; FOH stock, BOH backstock, deals) | **Planned**: generator (PROC-004) and PII-free importer (DATA-002) exist; catalog data missing | **PS3**, gated on Nolan's Dutchie/LeafLogix export (DATA-004, GAP-PKG-01); GAME-014/015/016, UX-004 |
| **Compliance (AZ)** (limits, IDs, medical allotment, tax) | **Exists** in PS1 from COMP-001 research | copy rule H1 (system text never promises an effect) |
| **Audio** | **Planned**: plan + CC0 sourcing done (AUDIO-001) | AUDIO-002 Unity integration (PS2) |
| **Builds / QA / perf** | playtest builds 1 and 2 played; perf baseline exists | BUILD-008 + **QA-004 gate** close M-B; PERF-002 (PS2), PERF-003/QA-003/BUILD-009 (M-G) |
| **Management layer** (ordering, deliveries, receiving, merchandising, staffing) | **Deferred, gated**: PS4 opens only when GSS §104 holds (testers finish several shifts and want to improve) | PS4 decomposition not registered yet; V2 pack holds the design material |
| **Rejected / out of scope** | cash equipment (PROC-008, DEC-051/086), customer PII/CRM, real auth/RLS, invented store facts, ChatGPT drops without audit, parking-lot throughput before PS4 | — |
| **Provisional** (placeholders that stand until evidence) | GAP-labelled store values; emergency-exit alarm (GAP-CF-04, never re-ask); default tuning from V2 `CONFIG/default_tuning.yaml` | replaced only by cited evidence or a DEC |

## 6. Milestones, next target, critical path (roadmap §2–§3)
PS1 Counter Decisions (**done**, playtest 2) → **M-B Believable store (current)** → PS1b Customer Intelligence → PS2 Full Shift Day → PS3 Packaged Floor (gated on the catalog export) → M-F Final look and world → M-G Ship-ready → PS4 Management (gated).

**Next meaningful playable target: playtest 3 = BUILD-008, the M-B exit.** Customers enter through the guard, queue and get called; the layout matches the references; register stations look real; doors are real; fixtures pass the quality bar; and QA-004 records PASS for every still-relevant PT1 + PT2 item in that build before Nolan sees it (DEC-120).

**Critical path today:** GAME-026 → GAME-017a → GAME-017..020 (fun) in parallel with ART-013 (layout + doors) → BUILD-008 → QA-004 (store). PROC-007 → ART-011 (UV/label cut-over) rides alongside; characters join at GAME-CHR-002 once ASSET-005/006 pass.

**Why the current tasks are the right tasks:** every PT2 finding is mapped to a row in `Design/PLAYTEST2_2026-10-30.md` §Mapping: #10–12 → GAME-026; #3/4/8/9 → REF-016 (done) → ART-013; #1/6/7 → PROC-013 (done) → ART-013; #13 → GAME-017a; #5 → DEC-121 in ART-013. GAME-017a waits for GAME-026 only because they share the Slice files (one owner at a time). Ordering rule: shortest path to fun; fidelity work runs in parallel but never ahead of the evidence (DEC-008/047/110).

**Cross-system dependencies that bite:** `ROOM_FIXTURES.json` / `DOORS.json` / `SCENE_ANCHORS.json` are the contract between REF (evidence), ART (scene) and GAME (anchors, door logic): one running task edits them at a time (DEC-142). Generators size from `ROOM_FIXTURES`, never guess. Characters need the wardrobe/hair pass before Unity import. Packaged gameplay needs real catalog data. PS2 needs PS1b first (DEC-096).

## 7. Major unresolved product and design questions
- **Packaged catalog data** (DATA-004, GAP-PKG-01): Nolan's Dutchie/LeafLogix export; asked once, ask again only when PS2 is in sight. Gates PS3.
- **PS4 scope**: the management decomposition is written only when GSS §104 is met after PS2; V2 pack questions GAP-V2-01 (storage zones, deliveries, expiry, staffing titles) wait for that gate.
- **Start screen / role select scope** (LT-2a/2b): difficulty with PS2; customisation after the character pipeline; role select only when a second role exists (DEC-101).
- **Exterior and parking** (REF-015 → ART-012, LT-1a): space layout is being measured; dwell time and throughput are PS4 questions.
- **Placeholders that stand**: emergency-exit alarm (GAP-CF-04), Phoenix TPT rate 25.1% until a receipt settles it (OPEN-4), class mix and paint of parked cars (GAP-PROC-23/24).
- **Register count on the south run** (PT2 #3): settled by REF-016 evidence, implemented by ART-013; verify in playtest 3.

## 8. Glossary
TFS = The Flower Shop (the real store and its budtender tool) · GSS = `GAMEPLAY_SIMULATION_SPEC.md` · DP = decision-pressure spec · CF = `Specs/CONTROLS_FLOW_PS1.md` · RF = `ROOM_FIXTURES.json` · TI = tenant-improvement drawing set (A011/A901/A940…) in `References/TI/` · CCTV wall = Nolan's camera-wall screenshot, tiles `R<row>C<col>` · HUB / HUB 2 = the two back storage rooms (not the Studio Hub) · FOH/BOH = fulfilment and product-storage rooms · JC = janitor closet · PS1/PS1b/PS2… = play-slice milestones, M-B/M-F/M-G = store/look/ship milestones · Gate A = TFS parity test gate (QA-002) · PT1/PT2 = playtests 1 and 2 · [SRC] cited store fact · [GDD] game-design decision.

## 9. People, machine, sessions
Nolan Bradford (owner, handlebarn@gmail.com) talks to the Hub in the Hub chat (the pre-recovery PO communication session was archived in the 2026-10-30 cutover, DEC-144). The TFS tool's own hub is the peer session "TFS tool: project hub (phases 1-7)": relay tool defects there, never edit its files. Machine: Windows 11 laptop, RTX 4050 6 GB, 32 GB RAM; Unity 6000.6.7f1 + HDRP 17.6.0, Blender 5.2.3, Python 3.12, git-lfs; no gh, no pwsh 7 (`MACHINE_PROFILE.md`). The "external" folders `Dispo Game Builds|Imports|Imports Archive|Assets Cache` live inside the repo root, gitignored. Builds played: `slice-38b9e5c` (PT1), `playtest2-741bb43` (PT2).
