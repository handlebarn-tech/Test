# PROJECT STATE

Hub-owned; the **only live state record** (DEC-117). A fresh Hub resumes from `Docs/HUB_RESUME.md` + this file + the newest DECs, then reconciles the table below with `list_sessions` and `git branch` (STUDIO_OS §0.9). Plan and milestones: `Docs/Design/ROADMAP_POST_SLICE.md`. Registry: `Docs/BACKLOG.md`. Workers and reviewers do not read this file.

**Updated:** 2026-10-30 (INTEG PROC-009: parked vehicles merged, PASS r3 with minors; DEC-134/135; minors → PROC-009b, textures → PROC-016). **Milestone:** PS1 done; Nolan has played `playtest2-741bb43` (findings `Docs/Design/PLAYTEST2_2026-10-30.md`). **Current milestone: M-B Believable store** (roadmap §2), including the PT2 overhaul (REF-016 → ART-013, PROC-013, GAME-027). Exit = BUILD-008 candidate **plus QA-004 PASS on every PT1 + PT2 requirement in the build before Nolan gets it** (DEC-120). PS1b starts as soon as GAME-026 merges (GAME-017a).
**Hub session:** the fresh Hub is running; old Hub `local_c6267ff5` is retired and its four children are being detached so it can be archived. Workers below were started by the old Hub `local_c6267ff5`, so SendMessage by name fails: use `send_message` with the `local_…` id.
**Hub clear plan (Nolan 2026-10-30): EXECUTED** (STATE-001). Keep old Hub `local_c6267ff5` unarchived until its children (GAME-026, PROC-005, ASSET-005, ART-008) merge (archiving cascades). `local_5c45166e` ("Random BS", live Remote Control client) is for Nolan to archive from the sidebar.
**Structure (DEC-128/132: dispatch-only Hub, all task work in sessions):** Nolan → Hub → workers → fresh per-review reviewers → integrator sessions merge (DEC-116/117/132). Nolan is cost-sensitive: no FYI messages, lean briefs (DEC-107).

## In flight
| Session | Task | Branch @ sha | State → next Hub action |
|---|---|---|---|
| worker `local_9bc94fb7-d677-4076-81be-83317f26bbf8` (fix round) | **GAME-026** customer flow | `task/GAME-026`; r2 review FAIL → `review/game026-r2` @ 9e0b299 | Fixing M1 (stale DOORS/SCENE_ANCHORS build copies). #11(2) not build-proven, so GAME-027 stays. Seed-1 report changes need QA sign-off. When ready: fresh reviewer. |
| worker `local_335db39d-0968-49fa-846c-808a2abb2158` (fix round) | **PROC-005** fixture families | `claude/elated-satoshi-3a4844`; review FAIL → `review/proc005b` @ 35c47b2 | Register run/jar walls vs REF-013 ROOM_FIXTURES; regenerating nine families. When ready: fresh reviewer. |
| worker `local_77fd945b-ecaf-4432-8c51-54b18ed9dc50`; reviewer `local_f6623b7b-9a38-4980-a8c3-e8b2f2277967` (running) | **ART-008** graybox final pass (Unity slot) | `claude/festive-hamilton-c0ced4` @ 1440ff6 | Under review: 108/114 clearance; the 6 failures come from GAP-131 data. On PASS: INTEG session. |
| `dispo-proc013` `local_6b501011-a377-4a18-8f78-90c75f433ede` (running) | **PROC-013** door family incl. glass storefront (Blender) | continues `worktree-agent-a83016d0b10c940eb` @ 4e1b088 + uncommitted files (locked worktree) | Relaunch running. When ready: strong visual review (DEC-122). |
| `dispo-asset005` `local_1bb17d9a-7584-4a8b-af68-d01479714d05` (running) | **ASSET-005/006** wardrobe + hair (Blender) | `claude/sweet-shirley-002b17` @ 0f3fba5 | Generators running; no commit/handoff yet. At merge the reviewer re-runs the C001 regression (ASSET-007 also edits `customer_gen.py`); then add the staff-gloves line to CHARACTERS.md §9. |

Worktrees/branches are retired only when positively identified as integrated or obsolete (DEC-123); no broad cleanup.

## Pending for the next Hub
- On each reviewer PASS, start an **integrator session** (DEC-132); **only one integrator at a time**.
- **Hub ruling needed (REVIEW-PROC009 r3 m5):** parked cars when more than 15 customers are inside (lot has 15 spaces; DEC-134), e.g. cap at 15. Record it as a DEC via a planner.
- Fresh reviewers when the GAME-026 and PROC-005 fix rounds report ready.
- Finish detaching old Hub `local_c6267ff5`'s four children, then archive it.
- App limits: `start_session` is refused on peer-triggered turns (post a card + PO line instead); archiving needs Remote Control off and no background monitors.

## Unity slots (max 2, DEC-013)
ART-008 reviewer holds one; GAME-026 reviewer (idle) may still hold the other. PROC-005 reviewer (idle) may also have used Unity. Check `studio.ps1 slots` before starting a Unity session.

## Queue (next packets, in order; prerequisites in BACKLOG)
1. **GAME-017a** (Ready, waits for GAME-026 merge): first playable recommendation depth; the packet carries DEC-118 and the REVIEW-DES6/UX6 minors.
2. **PROC-007** UV layout (Ready, waits for PROC-005 merge) + **ART-011** label-shader cut-over (Later, same wave; packet to write from DEC-097).
3. **ART-013** layout overhaul (Unity; packet when ART-008 + PROC-013 merge; REF-016 prerequisite met: PASS r2, integrated via `integrate/ref016`; work list REFERENCES_INDEX §9.3) with a fresh Unity implementation reviewer in the assembled scene, independent of the REF-016 evidence review. **GAME-027** after GAME-026 (drop if GAME-026 proves the register ID check in a build).
4. **BUILD-008** candidate → **QA-004** PT1+PT2 validation in the player → only on PASS does Nolan get playtest 3 (DEC-120). Do not hand Nolan a build before that.
5. **GAME-CHR-002** Unity import of the customers (Later; after ASSET-005/006/007), then **NPC-001** bodies in the flow (after GAME-026).
6. PS1b chain GAME-017 → 018 → 019 → 020 (Ready packets, each waits for the previous merge), then PS2 per the roadmap.
Everything else registered in BACKLOG as Later with its dependencies; the Hub writes a packet only when those are Done.

## Priorities (DEC-096, playtest 1)
Controls (done) → store/layout accuracy → believable customer flow → recommendation depth → asset integration that unblocks these.

## Blocked / open with Nolan
Questions go to the PO session `local_0e722850-d68d-43e0-85af-b280cf2337c4` (DEC-125); blockers and "please type so I can start session X" requests by push notification (DEC-129).
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
