# ROADMAP — from the current build to the finished game

**Role (DEC-119):** the one high-level plan: milestones, what each contains (by task ID), dependencies and the critical path. **No task state lives here.** A task's state is its packet folder and `Docs/BACKLOG.md`; live execution is `Docs/PROJECT_STATE.md`. Hub-owned; edited when a milestone opens, closes or changes scope, not per task. History of this file: DES-002 proposal, DES-003 (DP), IMP-002 (V2), DES-005b (LT ideas), rewritten 2026-10-30 as the whole-game roadmap.

**Citation key (DEC-064):** "GSS §n" = `GAMEPLAY_SIMULATION_SPEC.md`; "DP §n" = `Design/SPEC_DECISION_PRESSURE.md`; "V2 <file> §n" = `Design/DESIGN_V2/`; "CF §n" = `Specs/CONTROLS_FLOW_PS1.md`; "LT §n" = `Design/PROPOSAL_PLAYTEST1_LONGTERM.md`; "M-n" = `MASTER_PLAN.md` / `STUDIO_OS.md` §66 production milestones. [SRC] store fact (cited) · [GDD] game-design decision · GAP labelled unknown.

## 0. Where the game stands (2026-10-30)
- **On `main` (playtest build 2, `playtest2-741bb43`):** one register, a 16-customer deli-flower shift. Chip intent → ported TFS engine (parity gate A green) → cards → assisted weigh → cart, purchase-limit meter, strikes, ID-check events, medical customers and tax → POS → jar fill / LOW / SOLD OUT → report. Always-on mouse look, Esc pause, Backspace back, doors from `DOORS.json`. Graybox + lookdev of every room rebuilt from the audited references (REF-011/012, ART-007): registers with operator zones, three deli walls, HUB, office, 15 doors, 42 scene anchors. 60-customer MPFB character pipeline exported (not yet in Unity). Toolkit core + wire shelving generators merged; 8 more fixture families generated but failed review (DEC-084 look).
- **Nolan's playtest-1 verdict (`PLAYTEST_2026-10-30.md`):** positive; wants natural movement and doors (done), a real entry/ID-check/call-next flow (GAME-026), an accurate register run / HUB / office / deli walls (REF-011..013, ART-007/008), register workstation detail (PROC-006b), a lived-in store, a livelier outside, better nugs.
- **Finished game (GSS, MASTER_PLAN):** a first-person budtender sim of this one real store: full shift days with traffic, restock, opening/closing, repeat customers and difficulty; deli flower plus the packaged assortment; customer intelligence over the real recommendation tool (parity); career progression and saves; a fully dressed, lit, populated store with staff, customers, audio and exterior; then the gated management layer (PS4). Not in scope: real PII/CRM, real auth, cash equipment, invented store facts.

## 1. Ordering rule (DEC-008, GSS §104)
"Shortest path to fun" = the most new player decisions per unit of new art and new data. Fidelity work (world, assets) runs in parallel but never ahead of the evidence (DEC-047/110). Management only after testers can play several shifts and want to improve.

## 2. Milestones (each ends in a playtest build, DEC-085; done when STUDIO_OS §91 holds)

| # | Milestone | Playable/valuable state at exit | Contains (task IDs; state in BACKLOG) |
|---|---|---|---|
| **PS1** | Counter Decisions | done: build `playtest2-741bb43` | GAME-006..010, 025, COMP-002, UX-002, DES-005/005b/006, DATA-003, UX-006, BUILD-007 |
| **M-B** | Believable store | Customers enter through the guard, queue, get called; store layout matches the references; register stations look real; fixtures pass the quality bar. Exit test (DEC-120): QA-004 records PASS for every still-relevant PT1 + PT2 requirement in the build-3 candidate, before Nolan gets it. | GAME-026, GAME-027, REF-013 (fix), REF-016, ART-008, ART-013, PROC-013, QA-004, PROC-005 (fixture families), PROC-006b, PROC-007 + ART-011 (UV/label cut-over), ASSET-005/006/007, PROC-009, BUILD-008 |
| **PS1b** | Customer Intelligence | Every sale is hear → interpret → ask → search the tool's way → read cards → react; service is evaluated and scored. Exit: DP §115 tests DP-001..032 that PS1b owns pass; a first-card bot scores below an ask-well bot. | GAME-017a → GAME-017 → GAME-018 → GAME-019 → GAME-020; GAME-CHR-002 + NPC-001 (customers visible and animated in the flow); BUILD-008b |
| **PS2** | Full Shift Day | Compressed 08–22 clock, traffic curve, manager refill restock, opening/closing, repeat customers, difficulty profiles, career + save v1; staff NPCs ambient; audio in. Exit: GAME-023 acceptance shift (DP §133) passes. | DES-004 (done), UX-003, GAME-011, GAME-012, GAME-013, GAME-021, GAME-022, GAME-023, GAME-024, ART-009, NPC-002, ASSET-008, AUDIO-002, LT-2a, LT-3, PERF-002, UI-001 |
| **PS3** | Packaged Floor | Prepacks, prerolls, vapes, edibles on racks/coolers with FOH fetch, format/dose matching, deals v1. **Gated on real catalog data from Nolan (GAP-PKG-01, DATA-004).** | DATA-004, GAME-014, GAME-015, GAME-016, UX-004, PROC-010 (arranger/labels/clutter), ART-006 (done) |
| **M-F** | Final look and world | Final lighting day/night, lived-in dressing, exterior and parking with traffic, bud look, TV wall, break room; every family at DEC-084. | LIGHT-001, ART-010, ART-012, REF-015, PROC-012, LT-1a, LT-5, LT-6a, LT-7, LT-2b |
| **M-G** | Ship-ready | Stable optimised build, regression suite green, no missing references, names cleared, docs clean. | PERF-003, QA-003, BRAND-002, BUILD-009, DOC-002, DATA-005 (when TFS v7.11.5 ships) |
| **PS4** | Management (gated) | Ordering → deliveries → HUB receiving → merchandising → staffing (GSS §61, §75–76; DP §87–100). DES writes the PS4 plan only when the Hub opens the gate (GSS §104 met after PS2). | LT-1b, LT-4, LT-6b and the PS4 decomposition (not registered) |

## 3. Tracks and dependencies (what unlocks what)

**Gameplay (GAME/UX/DATA/QA).** GAME-026 → GAME-017a (shared Slice files, one owner) → 017 → 018 → 019 → 020 → PS2 rows (GAME-011/012 need PS1b per DEC-096; GAME-021/022/024 need GAME-019/020; GAME-023 needs 011/012 and is Blocked by DEC-059 until then; GAME-013 needs 011 + 020). PS3: DATA-004 (Nolan's Dutchie export) → GAME-014 → 015/016; UX-004 after DATA-004. Gate A (QA-002) stays green on every gameplay merge; `Code/Domain/` changes only as faithful ports (DEC-001/002, DEC-118 B1).

**World (REF/ART/LIGHT).** REF-013 fix → ART-008 (graybox final on rev8) → BUILD-008. PROC-007 → ART-011 same wave. ART-009 (BOH/HUB stock dressing + restock anchors) before GAME-012. ART-010 lived-in pass after the final asset families land (PROC-005/010). REF-015 (exterior envelope, parking, fence from A011/A012, CCTV R1C1–C5/R3C1, BAND) → ART-012 exterior → LT-1a/LT-7. LIGHT-001 after ART-010/012. Every store value cites a source or is a GAP (DEC-047); layout questions are measured, never asked (DEC-110).

**Assets (PROC/ASSET/IMP/BRAND/AUDIO).** PROC-005 fixture families (fix round) → PROC-007 → PROC-010 (architecture kit, exterior, ladder, display cases, clutter, arranger, labels, materials, ID stand/bags/signs = PROC-005's "Left, in order") → PROC-012 bud look. PROC-006b register kit (independent). ASSET-004 (done) → ASSET-005/006/007 → GAME-CHR-002 (Unity import, retarget) → NPC-001; ASSET-008 staff (DEC-089/113) → NPC-002. AUDIO-001 plan (done) → AUDIO-002 Unity integration (PS2). Future toolkit drops: new IMP task per DEC-095; BRAND-002 before any public build.

**Build/QA/Perf.** BUILD-008 closes M-B, BUILD-008b closes PS1b (one BUILD row per milestone build). PERF-002 with full-day NPC counts (PS2); PERF-003 + QA-003 + BUILD-009 in M-G.

**Critical path today:** REVIEW of the REF-013 fix → ART-008 → BUILD-008 (store) and GAME-026 → GAME-017a → 017 → 018 → 019 → 020 (fun). Characters join at GAME-CHR-002 once ASSET-005/006 pass. Everything in PS3 waits on Nolan's catalog export.

## 4. Cross-cutting rules
- **Tool parity is the top rule** (DEC-001/002/006): nothing changes engine scoring; new logic is [GDD] and lives in Simulation. Gate A (DP §124) from QA-002 on. The parity oracle is the shipped engine (v7.11.4, DEC-060); DATA-005 re-baselines on v7.11.5.
- **V2 add-on (DEC-063):** DP wins on conflict; V2's 70 exploits are a test plan built in QA-002's harness by the owning packets. TFS input snapshot = parser input (DEC-057); the report never shows TFS scores (DEC-052).
- **Copy rule H1** (COMP-001): system text never promises an effect. **Tone:** `Design/TONE.md` for every dialogue/event writer (DEC-101).
- **Quality bar** DEC-084/114 for every asset; **$0** and licences per DEC-023/087; **no cash equipment, PII or security hardware** (DEC-006/031/051).
- **Brands:** only approved brands ship (DEC-071/078); BRAND-002 before a public build.

## 5. Long-term ideas (DEC-101, LT §n) — registered in BACKLOG as LT-* rows
LT-1a parking lot presentation (M-F) · LT-1b lot throughput (PS4) · LT-2a start screen difficulty (PS2) · LT-2b character/role select (M-F) · LT-3 store condition over the day (PS2) · LT-4 coworker personalities (PS4) · LT-5 TV ad wall (M-F) · LT-6a break-room props (M-F) · LT-6b break-room NPC use (PS4) · LT-7 neighbourhood activity (M-F) · LT-8 tone pillar (done). Values [GDD]; open asks stay in LT §n until a row opens (DEC-105).
