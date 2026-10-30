# PROJECT STATE

Hub-owned; the **only live state record** (DEC-117). A fresh Hub resumes from `Docs/HUB_RESUME.md` + this file + the newest DECs, then reconciles the table below with `list_sessions` and `git branch` (STUDIO_OS §0.9). Plan and milestones: `Docs/Design/ROADMAP_POST_SLICE.md`. Registry: `Docs/BACKLOG.md`. Workers and reviewers do not read this file.

**Updated:** 2026-10-30 ~18:30 (full reconciliation, DEC-117/119). **Milestone:** PS1 done (`playtest2-741bb43` is with Nolan). **Current milestone: M-B Believable store** (roadmap §2) → exit = playtest build 3 (BUILD-008). PS1b starts as soon as GAME-026 merges (GAME-017a).
**Hub session:** none active. Both earlier Hubs (`local_c6267ff5` "Dispo · Studio Hub", `local_5c45166e` "Dispo · Random BS") are idle and superseded; the next Hub Nolan starts writes its id here and may archive them. All worker sessions below were started by `local_c6267ff5` and are **idle since ~15:49** (stopped at the Hub reset): each needs one resume line from the Hub ("continue your packet; when done, `<ID> ready for review: <branch> @ <sha>` to the Hub").
**Structure:** Nolan → Hub → workers → fresh per-review reviewers → Hub merges (DEC-116/117). Nolan is cost-sensitive: no FYI messages, lean briefs (DEC-107).

## In flight
| Session (idle) | Task | Branch @ sha | State → next Hub action |
|---|---|---|---|
| — | **REF-013 fix** | `claude/festive-hamilton-c0ced4` = `worktree-agent-ae92283c8f8687a3d` @ 3890936 (handoff `Docs/Handoffs/REF-013.md` on the branch) | **Awaiting review.** REVIEW-REF13 (FAIL, on main) listed 1 major; the fix round answers it. Spawn a fresh reviewer (§0.5 brief, packet `Tasks/Active/REF-013.md`); on PASS merge, close REF-013, unblock ART-008. |
| `dispo-proc006b` `local_cab28702-140d-48df-963a-3cc4b318aa89` | **PROC-006b** register kit generators (Blender) | `claude/proc-006b-92b9a0` @ 9728334 (handoff on branch: validates 16/16, 4-station contact sheet) | **Awaiting review.** The earlier Agent reviewer died with the old Hub; no verdict exists. Spawn a fresh reviewer (Blender validation + DEC-084 look). |
| `dispo-art008` `local_77fd945b-ecaf-4432-8c51-54b18ed9dc50` | **ART-008** graybox final pass (Unity slot) | `claude/festive-hamilton-c0ced4` @ 3890936 (no work yet; based on the REF-013 fix) | **Blocked** on the REF-013 fix verdict (packet: stop if FAIL). Resume after PASS. |
| `dispo-game026` `local_9bc94fb7-d677-4076-81be-83317f26bbf8` | **GAME-026** customer flow (Unity slot) | `task/GAME-026` @ 5d7e543 (WIP, 22 files, "uncompiled"; includes GAME-009 m3/m4 and the GAME-025 M1 SliceDoor fallback) | **Active, mid-task.** Resume: compile, finish CF §4–5 deliverables, handoff, `ready for review`. Owns the Slice files until merged (GAME-017a waits). |
| `dispo-proc-005-fixture-f` `local_335db39d-0968-49fa-846c-808a2abb2158` | **PROC-005** fixture families fix round (REVIEW-PROC5 FAIL: DEC-084 look, citation conflicts) | `claude/elated-satoshi-3a4844` @ 0adfba7 (PBR finish library, Eevee contact sheets, manifest lock) | **Active, mid-task.** Resume; `ready for review` when the eight families pass the packet's own checklist. At review: the Hub decides whether the "Left, in order" list closes PROC-005 or moves to PROC-010 (registered Later). |
| `dispo-asset005` `local_1bb17d9a-7584-4a8b-af68-d01479714d05` | **ASSET-005/006** wardrobe + hair (Blender) | `claude/sweet-shirley-002b17` @ 0f3fba5 (packet only, now also on main `Tasks/Active/ASSET-005.md`) | **Active, not started.** Resume with GO. |
| `dispo-asset007` `local_d3aad36e-a494-47b7-a5c7-2cd0a58efe19` | **ASSET-007** glove overlay (Blender) | `claude/elastic-kilby-04c2ca` @ 36be358 (no work yet) | **Active, not started.** Resume with GO. |

Dead Agent runs from the old Hub, nothing to recover: PROC-009 (no branch; packet back in `Tasks/Ready`), the REF-013 M1 fix on `worktree-agent-a8683a438ebc5cbe4` (superseded by 3890936), REVIEW-REF13-FIX and REVIEW-PROC006b (no verdicts written). Stale worktrees under `.claude/worktrees/` for merged tasks can be removed with `git worktree remove` when convenient.

## Unity slots (max 2, DEC-013)
GAME-026 holds one; ART-008 takes the other when unblocked. A PROC-005/006b reviewer needing Unity import checks waits for a free slot or borrows GAME-026's while that session is idle.

## Queue (next packets, in order; prerequisites in BACKLOG)
1. **PROC-009** vehicles (Ready, packet in `Tasks/Ready`): launch when a Blender worker frees up; no Unity.
2. **GAME-017a** (Ready, waits for GAME-026 merge): first playable recommendation depth; the packet carries DEC-118 and the REVIEW-DES6/UX6 minors.
3. **PROC-007** UV layout (Ready, waits for PROC-005 merge) + **ART-011** label-shader cut-over (Later, same wave; packet to write from DEC-097).
4. **BUILD-008** playtest build 3 (Later; packet when GAME-026, ART-008 and PROC-006b are on main) = M-B exit. Give Nolan the path.
5. **GAME-CHR-002** Unity import of the customers (Later; after ASSET-005/006/007), then **NPC-001** bodies in the flow (after GAME-026).
6. PS1b chain GAME-017 → 018 → 019 → 020 (Ready packets, each waits for the previous merge), then PS2 per the roadmap.
Everything else registered in BACKLOG as Later with its dependencies; the Hub writes a packet only when those are Done.

## Priorities (DEC-096, playtest 1)
Controls (done) → store/layout accuracy → believable customer flow → recommendation depth → asset integration that unblocks these.

## Blocked / open with Nolan
- **DATA-004** (PS3 gate): needs Nolan's Dutchie/LeafLogix catalog export (GAP-PKG-01). Asked before (RES-001 O14); ask once more only when PS2 is in sight, batched.
- **DATA-005:** waits for TFS v7.11.5 to ship (GAP-210); external.
- Playtest build 2 is with Nolan; his feedback becomes the playtest-2 intake (a DES task when it arrives).
- Never re-ask: W6 self-closing doors, emergency exit alarm, drum kit, staff-tee print side (answered: wearer's left, DEC-113) (DEC-105).

## Risks
- Unity editors: max 2 (DEC-013). `studio.ps1 slots`.
- Older worker briefs (all sessions above except ART-008/ASSET-007) still name leads or pool reviewers; the resume line tells them to report to the Hub.
- ChatGPT toolkit drops need full audit before use (DEC-095).
- PROC-005 WireShelving FBX `.meta` files missing on main (fix rides with PROC-007).

## Builds
- Played: `slice-38b9e5c/` (playtest 1). **Playtest 2 = `Dispo Game Builds/playtest2-741bb43/DispoGame.exe`** (doors need `Dispo Game Builds/Docs/Reference/DOORS.json` until the GAME-026 TextAsset fix). Older playtest2-08758c1 has no doors.
