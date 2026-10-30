# Gameplay department

Rules for every department: `Docs/STUDIO_OS.md` §0. This file is the Gameplay lead's resume and domain state; the lead owns it. Lead session and capacity: `Docs/PROJECT_STATE.md` → "Studio roster".

## Charter
- **Prefixes:** GAME, UX, DES, QA, DATA, COMP, BUILD, PERF.
- **Owns:** `UnityProject/Assets/_Game/Code/{Domain,Simulation,Presentation}/`, `Code/Editor/{Slice,CI}/`, `Code/Editor/ProjectSetup.cs`, `Code/Tests/` except `Tests/EditMode/ProcArt/`, `_Game/{Data,UI,Audio}/` wiring, the Slice scene and its builder; `Tools/Data/`; `Docs/Specs/`, `Docs/Design/` except `ROADMAP_POST_SLICE.md` (Hub, scope), `Docs/Reconstruction/`, `Docs/BUILD_STATUS.md`, `Docs/PERF_BASELINE.md`; playtest builds in `Downloads/Dispo Game Builds/`.
- **Does not own:** scene geometry, graybox/lookdev builders and `ROOM_FIXTURES` (World); generators, imported art, characters (Assets).

## Contracts
- **Provides:** catalog/data schema (`Reconstruction/DATA_SCHEMA.md`, `_Game/Data/Catalog`), the gameplay anchor *needs* (World commits the names), the label text set for Assets' label generator.
- **Consumes:** scene anchor/object names (World), prefab/FBX names and manifest (Assets).

## Domain reading (on demand, by §)
`Docs/Design/SPEC_DECISION_PRESSURE.md` (wins over GSS on conflict), `Design/DESIGN_V2/` (DEC-063/066), `Design/ROADMAP_POST_SLICE.md`, `Design/SPEC_COMP002.md`, `SPEC_GAME004.md`, `SPEC_SHIFT_DAY.md`, `TUNING_PS1.md`, `Docs/Specs/*`, `GAMEPLAY_SIMULATION_SPEC.md`, `TOOLCHAIN_EXECUTION.md` (runner/tests). TFS tool source `C:/Users/handl/Downloads/tfs-budtender` is the top authority for recommendation logic (DEC-001/002, read-only, no PII).

## Domain rules (pointers)
Gate A on every gameplay PR (DEC-067); V2 Critical/High exploit tests before a system is complete (DEC-066); exploration tests `[Explicit]` (DEC-072); realism vs fun (DEC-032); approved brands only (DEC-071/081).

## Status for Hub
_Lead keeps this ≤15 lines._ 2026-10-30, lead session started.
- BACKLOG reconciled: GAME-007/008/010, QA-002b Done; GAME-011/012 Ready (wait for PS1b, DEC-096); new rows DES-005/006, GAME-025/026.
- DES-004b+c merged (W5L, d79e103).
- GAME-009 resumed in its own session (Gameplay's Unity slot); then REVIEW-PS1 → playtest build 2.
- DES-005 (playtest intake, controls + customer-flow spec, GAME-025/026 packets) and DES-006 (PS1b vs TFS depth audit) run as doc-only subagents.
- Next code after GAME-009: GAME-025 controls, then GAME-026 flow and the DES-006 "first playable depth" cut.
- Cross-dept: door + entry/guard/queue anchors with World (contract in `Specs/CONTROLS_FLOW_PS1.md` §Contract, from DES-005).

## In flight
| Task | Worker | Branch | State |
|---|---|---|---|
| GAME-009 medical (+ W5N m2 queue strip) | session `local_7f8c95e9-933b-4ca0-8d51-0ecbe3d5688a` | `claude/task-game-009` | over DEC-102 ceiling (506k): told to finish if one run away, else WIP handoff; then archive, continue in a fresh worktree subagent if needed |
| DES-005 playtest intake | done | `worktree-agent-afdc1983fe7bb696c` @ 5c8031b | in review (Docs 2); needs list sent to World; 7 Nolan Qs + proposal sent to Hub |
| DES-006 recommendation depth audit | done | `worktree-agent-aad768800c956f13b` @ caebbd3 | in review (Docs 2) |
| DATA-003 needs catalog + goldens | lead subagent | worktree | running |
| UX-006 counter UX addendum | lead subagent | worktree | running |

## Queue (lead re-orders within DEC-096)
1. GAME-009 → REVIEW-PS1 → playtest build 2 for Nolan (BUILD).
2. GAME-025 controls (after DES-005 + GAME-009 merge; World door contract).
3. GAME-026 customer flow (World entry anchors) and the DES-006 first-depth cut, then PS1b GAME-017 → 018 → 019 → 020 as amended.
4. GAME-021/022/024; UX-003; GAME-011/012 per DES-004.
5. **DES-005b (next free slot, off `review/w5u`)**: fold DEC-103 (Nolan's flow answers: call lines, one line, no 2nd door, guard scans ID back + green light, ID re-shown at register, check-in never backs up, FOH/BOH + north office + HUB connector doors propped open, GM assigns registers per DEC-079; emergency-exit alarm stays GAP) into `CONTROLS_FLOW_PS1.md` + GAME-025/026; REVIEW-W5U m1/m2; KNOWN_GAPS GAP-CF rows + GAP-DAY-04 basis → DEC-096 (m3).
6. DES-007 (after DES-005 merges): DEC-101 accepted the long-term proposal as phased; add its rows to `ROADMAP_POST_SLICE.md` (Hub-delegated) + a deadpan tone note where dialogue/event writers read. Nolan Q1–7 (GAP-CF) are with the Hub; keep placeholders.

## Lead rulings (DES-006 questions, 2026-10-30)
- B1: a faithful add-only port of the tool's Refine chip selection into `Code/Domain/` is allowed (DEC-001/002: the tool is the authority; porting it is not changing logic), as its own task with tool-captured goldens and Gate A; record a DEC when it merges. Until then GAME-018 keeps the Refine placeholder.
- Q2 free typing: not in PS1b; later PC/expert option for the roadmap.
- Q3 New/Experienced toggle: include it in the TFS input snapshot hash if the tool's results depend on it (follow the tool).
- Q4 the UX addendum belongs to Gameplay UX (UX-006).
- Q5 yes: GAME-017a is split out now. Sequence: GAME-009 → GAME-025 → GAME-017a → GAME-026 (shared Slice files, one owner at a time).

## Blockers / Questions for Nolan
- None open.
