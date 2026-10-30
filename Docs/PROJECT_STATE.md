# PROJECT STATE

Hub-owned; the **only live state record** (DEC-117). A fresh Hub resumes from `Docs/HUB_RESUME.md` + this file + the newest DECs, then reconciles the table below with `list_sessions` and `git branch` (STUDIO_OS §0.9). Plan and milestones: `Docs/Design/ROADMAP_POST_SLICE.md`. Registry: `Docs/BACKLOG.md`. Workers and reviewers do not read this file.

**Updated:** 2026-10-30 (STATE-001, Hub restart prep). **Milestone:** PS1 done; Nolan has played `playtest2-741bb43` (findings `Docs/Design/PLAYTEST2_2026-10-30.md`). **Current milestone: M-B Believable store** (roadmap §2), including the PT2 overhaul (REF-016 → ART-013, PROC-013, GAME-027). Exit = BUILD-008 candidate **plus QA-004 PASS on every PT1 + PT2 requirement in the build before Nolan gets it** (DEC-120). PS1b starts as soon as GAME-026 merges (GAME-017a).
**Hub session:** the fresh Hub started after this clear. Workers below were started by the old Hub `local_c6267ff5`, so SendMessage by name fails: use `send_message` with the `local_…` id.
**Hub clear plan (Nolan 2026-10-30): EXECUTED** (STATE-001). Keep old Hub `local_c6267ff5` unarchived until its children (GAME-026, PROC-005, ASSET-005, ART-008) merge (archiving cascades). `local_5c45166e` ("Random BS", live Remote Control client) is for Nolan to archive from the sidebar.
**Structure (DEC-128/132: dispatch-only Hub, all task work in sessions):** Nolan → Hub → workers → fresh per-review reviewers → integrator sessions merge (DEC-116/117/132). Nolan is cost-sensitive: no FYI messages, lean briefs (DEC-107).

## In flight
| Session | Task | Branch @ sha | State → next Hub action |
|---|---|---|---|
| worker `local_9bc94fb7-d677-4076-81be-83317f26bbf8` (done); reviewer `local_b61cea37-9aa2-44ff-889d-5d08606db651` | **GAME-026** customer flow | `task/GAME-026` @ 54c929d; review → `review/game026` | Reviewer is running its test runs. On PASS: INTEG session (DEC-132), then GAME-017a + GAME-027 unlock. |
| worker `local_335db39d-0968-49fa-846c-808a2abb2158` (done); reviewer `local_9c427f1e-9856-4143-b55f-62862d551e04` | **PROC-005** fixture families fix round | `claude/elated-satoshi-3a4844` @ ddc3112; review → `review/proc005b` | Reviewer running. On PASS: INTEG session. The Hub decides whether the "Left, in order" list closes PROC-005 or moves to PROC-010. |
| worker `local_738af4a0-c26e-49b9-bd35-43c6dacd5b3f` | **PROC-009** parked vehicles | `claude/jovial-meninsky-908c0a` @ 2495e6c; reviewer FAIL (2 MAJOR) at `review/proc009` @ a8cfb3d | Worker is in its fix round. When it reports ready: fresh reviewer. |
| `dispo-art008` `local_77fd945b-ecaf-4432-8c51-54b18ed9dc50` | **ART-008** graybox final pass (Unity slot) | `claude/festive-hamilton-c0ced4` @ a8f4bd4 | In progress. Wait for ready-for-review. |
| `dispo-asset005` `local_1bb17d9a-7584-4a8b-af68-d01479714d05` | **ASSET-005/006** wardrobe + hair (Blender) | `claude/sweet-shirley-002b17` @ 0f3fba5 (uncommitted WIP in worktree) | In progress. At merge the reviewer re-runs the C001 regression (ASSET-007 also edits `customer_gen.py`); then add the staff-gloves line to CHARACTERS.md §9. |
| **none: Agent worker died with the old Hub chat** | **REF-016** store-evidence matrix (docs/data) | `worktree-agent-a9f9579ab68e3b5d2` @ 14332c3 (committed, 1 ahead of main; worktree `.claude/worktrees/agent-a9f9579ab68e3b5d2`) | Start a fresh session that continues from that branch (`source_branch`), per `Docs/Tasks/Active/REF-016.md`. Its work may already be complete: check the packet's deliverables first. Review = fresh **evidence** reviewer (DEC-120 (3)). |
| **none: Agent worker died with the old Hub chat** | **PROC-013** door family incl. glass storefront (Blender) | `worktree-agent-a83016d0b10c940eb` @ 4e1b088 (= main base, no commits). **58 uncommitted files** in the (locked) worktree `.claude/worktrees/agent-a83016d0b10c940eb`: door FBX exports + `manifest.json`. | Start a fresh session continuing from that branch/worktree (`source_branch`; keep the uncommitted files, do not clean the worktree), per `Docs/Tasks/Active/PROC-013.md`. Strong visual review (DEC-122). |
| `dispo-doc005` `local_b83a44f9-f817-45bc-ad86-bf67124cc602` | **DOC-005** rewriting HUB_RESUME / STUDIO_OS / CLAUDE.md | its own branch | Merge when it reports. |
| STATE-001 | this file | `claude/inspiring-volhard-934e33` | Merge, then clear the old Hub chat. |

Worktrees/branches are retired only when positively identified as integrated or obsolete (DEC-123); no broad cleanup.

## Pending for the next Hub
- On each reviewer PASS, start an **integrator session** (DEC-132); **only one integrator at a time**.
- Relaunch REF-016 and PROC-013 as sessions (table above).
- Archive old Hub `local_c6267ff5` once GAME-026, PROC-005, ASSET-005, ART-008 have merged.

## Unity slots (max 2, DEC-013)
ART-008 holds one; GAME-026 reviewer may hold the other. A PROC-005/006b reviewer needing Unity import checks waits for a free slot or borrows GAME-026's while that session is idle.

## Queue (next packets, in order; prerequisites in BACKLOG)
1. (PROC-009 launched, see In flight.)
2. **GAME-017a** (Ready, waits for GAME-026 merge): first playable recommendation depth; the packet carries DEC-118 and the REVIEW-DES6/UX6 minors.
3. **PROC-007** UV layout (Ready, waits for PROC-005 merge) + **ART-011** label-shader cut-over (Later, same wave; packet to write from DEC-097).
4. **ART-013** layout overhaul (Unity; packet when REF-016 PASS + ART-008 + PROC-013 merge) with a fresh Unity implementation reviewer in the assembled scene, independent of the REF-016 evidence review. **GAME-027** after GAME-026 (drop if GAME-026 proves the register ID check in a build).
5. **BUILD-008** candidate → **QA-004** PT1+PT2 validation in the player → only on PASS does Nolan get playtest 3 (DEC-120). Do not hand Nolan a build before that.
6. **GAME-CHR-002** Unity import of the customers (Later; after ASSET-005/006/007), then **NPC-001** bodies in the flow (after GAME-026).
7. PS1b chain GAME-017 → 018 → 019 → 020 (Ready packets, each waits for the previous merge), then PS2 per the roadmap.
Everything else registered in BACKLOG as Later with its dependencies; the Hub writes a packet only when those are Done.

## Priorities (DEC-096, playtest 1)
Controls (done) → store/layout accuracy → believable customer flow → recommendation depth → asset integration that unblocks these.

## Blocked / open with Nolan
Questions go to the PO session `local_0e722850-d68d-43e0-85af-b280cf2337c4` (DEC-125); blockers and "please type so I can start session X" requests by push notification (DEC-129).
- World follow-ups from PROC-006b (small-bin size, POS monitor y): in REF-016 deliverable 4.
- **DATA-004** (PS3 gate): needs Nolan's Dutchie/LeafLogix catalog export (GAP-PKG-01). Asked before (RES-001 O14); ask once more only when PS2 is in sight, batched.
- **DATA-005:** waits for TFS v7.11.5 to ship (GAP-210); external.
- Playtest-2 feedback received 2026-10-30 and taken in (DEC-120, `PLAYTEST2_2026-10-30.md` mapping). Nolan's imports `Bender & Asset new plan.md` → IMP-004; the older import subfolders appear to be the IMP-003 rounds (IMP-004 confirms). Archive the imports after his approval (DEC-070). **Archived 2026-10-30 (Nolan OK):** `Bender & Asset new plan.md` → `C:/Users/handl/Downloads/Dispo Game Imports Archive/2026-10-30_Bender_Asset_new_plan/` (the archive folder was empty before this; the earlier archives PT1/DESIGN_V2 cite are not there, so leave them alone per DEC-123).
- Never re-ask: W6 self-closing doors, emergency exit alarm, drum kit, staff-tee print side (answered: wearer's left, DEC-113) (DEC-105).

## Risks
- Unity editors: max 2 (DEC-013). `studio.ps1 slots`.
- Older worker briefs (all sessions above except ART-008/ASSET-007) still name leads or pool reviewers; the resume line tells them to report to the Hub.
- ChatGPT toolkit drops need full audit before use (DEC-095).
- PROC-005 WireShelving FBX `.meta` files missing on main (fix rides with PROC-007).

## Builds
- Played: `slice-38b9e5c/` (playtest 1). **Playtest 2 = `Dispo Game Builds/playtest2-741bb43/DispoGame.exe`** (doors need `Dispo Game Builds/Docs/Reference/DOORS.json` until the GAME-026 TextAsset fix). Older playtest2-08758c1 has no doors.
