# PROJECT STATE

Hub-owned; the **only live state record** (DEC-117). A fresh Hub resumes from `Docs/HUB_RESUME.md` + this file + the newest DECs, then reconciles the table below with `list_sessions` and `git branch` (STUDIO_OS §0.9). Plan and milestones: `Docs/Design/ROADMAP_POST_SLICE.md`. Registry: `Docs/BACKLOG.md`. Workers and reviewers do not read this file.

**Updated:** 2026-10-30 12:30 (playtest-2 intake, DEC-120..123). **Milestone:** PS1 done; Nolan has played `playtest2-741bb43` (findings `Docs/Design/PLAYTEST2_2026-10-30.md`). **Current milestone: M-B Believable store** (roadmap §2), now including the PT2 overhaul (REF-016 → ART-013, PROC-013, GAME-027). Exit = BUILD-008 candidate **plus QA-004 PASS on every PT1 + PT2 requirement in the build before Nolan gets it** (DEC-120). PS1b starts as soon as GAME-026 merges (GAME-017a).
**Hub session:** the Hub Nolan started 2026-10-30 ~19:30 (main checkout; workers reply to it via the "From" link of its resume message). Earlier Hubs `local_c6267ff5`, `local_5c45166e`, `local_3dbae2f5` are idle and superseded (archive when convenient). Workers below were started by `local_c6267ff5`, so SendMessage by name fails: use `send_message` with the `local_…` id.
**Structure:** Nolan → Hub → workers → fresh per-review reviewers → Hub merges (DEC-116/117). Nolan is cost-sensitive: no FYI messages, lean briefs (DEC-107).

## In flight
| Session | Task | Branch @ sha | State → next Hub action |
|---|---|---|---|
| `dispo-art008` `local_77fd945b-ecaf-4432-8c51-54b18ed9dc50` | **ART-008** graybox final pass (Unity slot) | `claude/festive-hamilton-c0ced4` @ 3890936 (no work yet; based on the REF-013 fix) | **Resumed** after REF-013 merged (REVIEW-REF013b PASS). Rebase/merge main first. |
| `dispo-game026` `local_9bc94fb7-d677-4076-81be-83317f26bbf8` | **GAME-026** customer flow (Unity slot) | `task/GAME-026` @ 5d7e543 (WIP, 22 files, "uncompiled"; includes GAME-009 m3/m4 and the GAME-025 M1 SliceDoor fallback) | **Resumed 19:40.** compile, finish CF §4–5 deliverables, handoff, `ready for review`. Owns the Slice files until merged (GAME-017a waits). |
| `dispo-proc-005-fixture-f` `local_335db39d-0968-49fa-846c-808a2abb2158` | **PROC-005** fixture families fix round (REVIEW-PROC5 FAIL: DEC-084 look, citation conflicts) | `claude/elated-satoshi-3a4844` @ 0adfba7 (PBR finish library, Eevee contact sheets, manifest lock) | **Resumed 19:40;** `ready for review` when the eight families pass the packet's own checklist. At review: the Hub decides whether the "Left, in order" list closes PROC-005 or moves to PROC-010 (registered Later). |
| `dispo-asset005` `local_1bb17d9a-7584-4a8b-af68-d01479714d05` | **ASSET-005/006** wardrobe + hair (Blender) | `claude/sweet-shirley-002b17` @ 0f3fba5 (packet only, now also on main `Tasks/Active/ASSET-005.md`) | **Resumed (GO) 19:40;** uncommitted wardrobe WIP in worktree. |
| `dispo-asset007` `local_d3aad36e-a494-47b7-a5c7-2cd0a58efe19` (idle, done) | **ASSET-007** glove overlay (Blender) | `claude/task-asset-007` @ dba3961 | **In review** (Agent reviewer → `REVIEW-ASSET007.md` on `review/asset007`). Gloves answered (DEC-126: black; on while weighing deli flower). At merge: tick IMP-003 checklist R4.7; after ASSET-005/006 merge add the staff-gloves line to CHARACTERS.md §9 (handoff Follow-ups). |
| `dispo-proc009` `local_738af4a0-c26e-49b9-bd35-43c6dacd5b3f` | **PROC-009** parked vehicles (Blender) | `claude/jovial-meninsky-908c0a` off main @ 3ab683b | First turn died on the plan usage limit (reset 12pm); re-sent 12:05. Await `ready for review`. |
| `dispo-proc006c` `local_796c7c2a-33dc-4897-9a85-ec441c8a9961` | **PROC-006c** register kit review follow-ups (Blender) | `claude/zealous-kalam-4192dd` | Launched 12:05. |
| Agent worker (Hub-spawned, worktree; dies if the Hub restarts: then relaunch as a session) | **REF-016** store-evidence matrix (docs/data) | worktree off main | Launched 12:30. Review = fresh **evidence** reviewer (DEC-120 (3)). |
| Agent worker (Hub-spawned, worktree) | **PROC-013** door family incl. glass storefront (Blender) | worktree off main | Launched 12:30. Strong visual review (DEC-122). |
| Agent worker (Hub-spawned, worktree) | **IMP-004** audit of `Bender & Asset new plan.md` (docs) | worktree off main | Launched 12:30. Hub applies the adoptions after review. |

Dead Agent runs from the old Hub, nothing to recover: the REF-013 M1 fix on `worktree-agent-a8683a438ebc5cbe4` (superseded by 3890936), the first PROC-009 run, REVIEW-REF13-FIX and the first REVIEW-PROC006b (no verdicts). Worktrees/branches are retired only when positively identified as integrated or obsolete (DEC-123); no broad cleanup.

## Unity slots (max 2, DEC-013)
GAME-026 holds one; ART-008 takes the other when unblocked. A PROC-005/006b reviewer needing Unity import checks waits for a free slot or borrows GAME-026's while that session is idle.

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
Questions go to the PO session `local_0e722850-d68d-43e0-85af-b280cf2337c4` (DEC-125); blockers by push notification.
- World follow-ups from PROC-006b (small-bin size, POS monitor y): in REF-016 deliverable 4.
- **DATA-004** (PS3 gate): needs Nolan's Dutchie/LeafLogix catalog export (GAP-PKG-01). Asked before (RES-001 O14); ask once more only when PS2 is in sight, batched.
- **DATA-005:** waits for TFS v7.11.5 to ship (GAP-210); external.
- Playtest-2 feedback received 2026-10-30 and taken in (DEC-120, `PLAYTEST2_2026-10-30.md` mapping). Nolan's imports `Bender & Asset new plan.md` → IMP-004; the older import subfolders appear to be the IMP-003 rounds (IMP-004 confirms). Archive the imports after his approval (DEC-070).
- Never re-ask: W6 self-closing doors, emergency exit alarm, drum kit, staff-tee print side (answered: wearer's left, DEC-113) (DEC-105).

## Risks
- Unity editors: max 2 (DEC-013). `studio.ps1 slots`.
- Older worker briefs (all sessions above except ART-008/ASSET-007) still name leads or pool reviewers; the resume line tells them to report to the Hub.
- ChatGPT toolkit drops need full audit before use (DEC-095).
- PROC-005 WireShelving FBX `.meta` files missing on main (fix rides with PROC-007).

## Builds
- Played: `slice-38b9e5c/` (playtest 1). **Playtest 2 = `Dispo Game Builds/playtest2-741bb43/DispoGame.exe`** (doors need `Dispo Game Builds/Docs/Reference/DOORS.json` until the GAME-026 TextAsset fix). Older playtest2-08758c1 has no doors.
