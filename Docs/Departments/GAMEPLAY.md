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
_Lead keeps this ≤15 lines._ 2026-10-30 (Hub, at handover): PS1 is one task from done (GAME-009). Playtest 1 feedback (DEC-096) makes controls, believable customer flow and recommendation depth this department's top priorities. No lead session yet.

## In flight
| Task | Worker | Branch | State |
|---|---|---|---|
| GAME-009 medical (+ W5N m2 queue strip) | session `local_7f8c95e9-933b-4ca0-8d51-0ecbe3d5688a` (idle) | `claude/task-game-009` @ a4806d6 | unfinished: EditMode 215/217, capture-timeout fix not re-run, no handoff yet |
| DES-004b+c (PS2 shift day) review | Docs reviewer `local_b073ffa0…`; DES worker session `local_82d327a2-5b67-4cff-b481-5854a94f6f31` idle | REVIEW-W5L | waiting on the verdict |

## Queue (lead re-orders within DEC-096)
1. **Reconcile BACKLOG rows** for this department's prefixes (several are stale: GAME-007/010, QA-002b, GAME-011/012 now have packets in Ready).
2. Finish GAME-009 → REVIEW-PS1 → playtest build for Nolan (BUILD).
3. Playtest 1 (DEC-096), first copy `Downloads/Dispo Game Imports/GameFeedback10-30.txt` to `Docs/Design/PLAYTEST_2026-10-30.md` and archive the original (DEC-070):
   - controls: camera/look feel, Esc always opens a pause menu;
   - door interaction (World owns the door geometry; agree the contract);
   - customer flow: entry check-in with an ID-checking guard (DEC-086, DEC-036 M2) → one line → **the player calls the next customer**, nobody appears at the register on their own;
   - **recommendation depth (top concern):** customers state needs in different ways, the player interprets them and asks follow-ups, then uses the full TFS recommendation workflow. Bring PS1b (GAME-017..020) forward and check it against the TFS tool's depth before building (DES pass).
4. PS1b chain GAME-017 → 018 → 019 → 020; then GAME-021/022/024; UX-003; GAME-011/012 per DES-004.
5. Long-term ideas from playtest 1 go into the roadmap through a DES proposal to the Hub (scope): parking-lot throughput system, character setup/start screen, store condition over the day, coworker personalities, TV ad wall cycling (5–10 s), grounded deadpan humour as a tone pillar.

## Blockers / Questions for Nolan
- None open.
