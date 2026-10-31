# PROJECT STATE

Hub-owned, the **only live state record** (DEC-117). A fresh Hub reads `PROJECT_BRIEF.md` → `HUB_RESUME.md` → this file, then reconciles the tables below with `list_sessions` (linked and unlinked), `git branch --no-merged main` and dirty worktrees (STUDIO_OS §0.9). Plan: `Design/ROADMAP_POST_SLICE.md`. Registry: `BACKLOG.md`. Workers and reviewers do not read this file.

**Updated:** 2026-10-30 ~18:00 Phoenix by the first post-cutover Hub (Fable; the Hub is session "Dispo Game studio hub" `local_375fef70`; "Dispo Game recovery architecture" was the RECOVERY-001 session, now finished). **Milestone:** PS1 done; Nolan has played `playtest2-741bb43` (findings `Design/PLAYTEST2_2026-10-30.md`). **Current milestone: M-B Believable store** (roadmap §2). Exit = BUILD-008 candidate **plus QA-004 PASS on every PT1 + PT2 requirement in the build before Nolan gets it** (DEC-120). PS1b starts when GAME-026 merges (GAME-017a).
**Studio structure:** Nolan → Hub (project manager, integrates) → workers → fresh reviewers (DEC-138..144; `Docs/Audits/RECOVERY-001.md`). **Caps:** 4 concurrent worker/reviewer sessions plus the Hub, 2 Unity editors. Rulings this Hub recorded: DEC-145 (jar fill is visual), DEC-146 (POS_05 clearance 3.2 ft), DEC-147 (lot cap 15), DEC-148 (Hub sync merges; check 0 against a named sha).
**Account:** Pro plan. 2026-10-30 18:00 Phoenix: weekly all-models 95 % (resets 2026-10-31 19:00 Phoenix), weekly Fable 28 %, 5-hour 27 %, extra usage on ($32 of $100). Usage is Nolan's call (DEC-100).

## Recovery: work stranded by the 2026-10-30 usage limit (fresh worker in a worktree cut from `main` that first `git merge`s the branch below; never resume a dead session, never cut a worktree from the old branch)
Reprioritised against the critical path (roadmap §3: GAME-026 → 017a; ART-013 → BUILD-008 → QA-004). Integrated: **DOC-004** (merged). Started: see In flight. *queued* = waits for a free slot; *parked* = off the critical path, starts only when nothing above it can run.
| Task | Branch @ sha (committed WIP) | State | Next Hub action |
|---|---|---|---|
| **GAME-026** customer flow (P0) | `task/GAME-026` @ 060f4af (behind `main`); `review/game026-r4` holds no verdict | r1–r3 FAIL; r2/r3 MAJOR = stale `Data/Reference` copies vs `main` | **Started:** fresh sync worker (merge `main`, re-copy DOORS/SCENE_ANCHORS, tests green, report ready) → then a fresh Unity reviewer. Packet names a lead/pool: the brief carries the correction. |
| **ART-013** layout overhaul (P0) | `claude/art013` @ 14b3eb3; `Handoffs/Recovered/ART-013_partial.md` | converter rev9 south side done (113/114 clearance); Unity builder, doors, `--matrix`, stand/guard pair, captures, handoff not done | **Started:** fresh Unity worker; rulings DEC-145/146 in the packet. |
| **PROC-013b** door follow-ups | `claude/intelligent-lumiere-b0fd09` (Hub sync-merged `main`, DEC-148) | ready for review | **Started:** fresh reviewer (Sonnet, Blender sheets only). |
| **DOC-006** LFS pointer guard | `claude/brave-boyd-7af7b5` (Hub sync-merged `main`, DEC-148) | ready for review; BACKLOG row DOC-005 "LFS guard" → DOC-006 at integration | **Started:** fresh reviewer (Sonnet). |
| **PROC-007** UV layout (P1; ART-011 waits on it) | `claude/hopeful-mendeleev-39bba2` @ 1947e0e (packet → Active only) | not started | *queued*: next free slot; needs a Unity slot for the ProcArt tests (after the GAME-026 sync worker finishes). ART-011 follows in the same wave. |
| **GAME-017a** first playable rec depth (P0) | `claude/adoring-bell-224eaa` @ db1b48b (packet → Active only) | not started; shares Slice files with GAME-026 | after GAME-026 merges. |
| **ASSET-005/006** wardrobe + hair | `claude/sweet-shirley-002b17` @ b42a4ae | WIP, no handoff; `customer_gen.py` shared with ASSET-007 (merged) | *queued* after PROC-007 (Blender, no Unity). Packet names leads: the brief carries the correction. |
| **PROC-009b** vehicle look | `claude/jovial-sutherland-c52674` @ aefadfc | WIP, unreviewed | *parked* (P3). DEC-147 lot cap applies to the consumer, not this task. |
| **PROC-014** QA renders + fault tests | `claude/sleepy-keller-7875af` @ d8cf4b3 | partial handoff on branch | *queued* (P1, Blender). |
| **PROC-018** HUB storage + refill | `claude/adoring-nash-8593f0` @ 448e9b1 | hub_storage done; refill params only | *queued* (P1, Blender). |
| **PROC-017** entry queue kit | `claude/hopeful-engelbart-ed1ea5` @ 7f4f7d6 | generator started | *queued* (P1, Blender). |
| **PROC-015** architecture kit research | `claude/elegant-nash-3c26bb` @ 4dbfc2d | research WIP | *parked*. |
| **REF-015** exterior envelope | `claude/dazzling-jennings-baa5c9` @ 0afad5c | measurements done; rows/§10 not written | *queued* (Sonnet, doc only, no Unity: the filler when a slot frees). |
| **UX-003** shift-day UX spec | `claude/determined-elgamal-c29f29` @ 0125c2e | nothing written | *parked* (PS2). |
| Verified already on `main` | `claude/audit-001-b559c2`, `claude/xenodochial-bell-85575c`, `claude/gifted-kapitsa-91bb28`, `worktree-agent-ad1cfeade6bad8b2d` (PROC-009 v1) | — | retire when convenient (DEC-123) |
| Captured, superseded | `worktree-agent-a83016d0b10c940eb` @ 788046a (PROC-013 originals); `claude/clever-lamport-837e7f`; `review/game026*` (r1–r3 verdicts are on `main`; r4 empty) | preserved | retire when convenient (DEC-123) |
All pre-recovery sessions were archived in the cutover (DEC-144). Nothing resumes from a conversation.

## In flight (actually working). `start_session` was refused on this session-triggered turn, so all four run as background worktree Agents of the Hub (DEC-139/143 fallback); they report to the Hub, not to the sidebar. A fresh Hub that finds them gone checks the branches below for committed work.
| Session | Task | Branch @ sha | State → next Hub action |
|---|---|---|---|
| Agent ART-013 (Fable, Unity slot 1) | ART-013 | `art013-r2` cut from `claude/art013` @ 14b3eb3, merges `main` 29da42f | working → fresh Unity reviewer on `ready for review` |
| Agent GAME-026 r4 (Sonnet, Unity slot 2) | GAME-026 | `task/GAME-026-r4` cut from `task/GAME-026` @ 060f4af, merges `main` 29da42f | working → fresh Unity reviewer (r4) on `ready for review`; a repeat of the stale-copy MAJOR is a Hub decision (DEC-142) |
| Agent REVIEW PROC-013b (Sonnet) | PROC-013b review | `claude/intelligent-lumiere-b0fd09` @ 511e9a2 → `review/proc013b` | reviewing → integrate on PASS |
| Agent REVIEW DOC-006 (Sonnet) | DOC-006 review | `claude/brave-boyd-7af7b5` @ 078990a → `review/doc006` | reviewing → integrate on PASS; register the DOC-006 row (DOC-005 "LFS guard" row renamed) |

## Queue (next packets, in order; obey the caps)
1. On PROC-013b / DOC-006 PASS: integrate, archive, and start **PROC-007** (Unity slot once the GAME-026 sync worker is done) and **REF-015** (Sonnet filler).
2. On GAME-026 `ready`: fresh Unity reviewer; on PASS → integrate → **GAME-017a** (same Slice files) → PS1b chain GAME-017 → 018 → 019 → 020.
3. **ART-011** right after PROC-007 (same wave). Then **ASSET-005/006**, **PROC-014**, **PROC-018**, **PROC-017** as Blender slots free.
4. **BUILD-008** candidate (packet when ART-013 + GAME-026 merge) → **QA-004** PT1+PT2 gate → only on PASS does Nolan get playtest 3 (DEC-120).
5. **GAME-CHR-002** after ASSET-005/006; **NPC-001** after GAME-026; **GAME-028** (DEC-145 jar binding) after GAME-017a + ART-013. UX-003 and PS2 rows after PS1b.

## Unity slots (max 2, DEC-013)
At 18:00 a `unity.exe` (8 MB, likely idle) and Unity Hub were running; the Hub cannot run `studio.ps1 slots` (hub_guard). ART-013 and the GAME-026 sync worker hold the two slots; each checks `slots` before batchmode and reports if a stray editor blocks it.

## Open with Nolan (batched in the Hub's `FOR NOLAN` reply block, DEC-144)
- **Usage pacing** (DEC-100): weekly all-models at 95 % with ~25 h to the reset and extra usage on; four sessions started. Nolan decides whether to pace; the Hub does not trim.
- **DATA-004** (PS3 gate): needs Nolan's Dutchie/LeafLogix catalog export (GAP-PKG-01). Asked once (RES-001 O14); ask again only when PS2 is in sight.
- **DATA-005:** waits for TFS v7.11.5 (GAP-210); external.
- PROC-005 open sizes/finishes GAP-PROC-14..42 (`Handoffs/PROC-005.md` "Questions for Nolan", DEC-105 search done). Low priority; batch.
- **Never re-ask** (DEC-105): W6 self-closing doors, emergency exit alarm, drum kit, staff-tee print side (DEC-113), W1/W2 layout (measured, DEC-110), register numbering (DEC-079), cash tray (DEC-051/086), jar count (DEC-145), POS_05 clearance (DEC-146), lot overflow (DEC-147).

## Risks
- Branches older than today's `main` carry stale copies of `ROOM_FIXTURES`/`DOORS`/`SCENE_ANCHORS`: every worker merges `main` before handoff (§0.5); reviewers fast-fail otherwise (DEC-142/148).
- The weekly limit may kill sessions again before 2026-10-31 19:00; workers commit as they go, so the recovery table above is the resume point.
- The `Dispo Game Builds|Imports|Imports Archive|Assets Cache` folders exist **only inside the repo root** (gitignored). The four worktrees that sat under `Dispo Game/Dispo Game/` were removed in the RECOVERY-001 audit (branches kept); 52 worktrees exist, max 3 Unity worktrees for disk (MACHINE_PROFILE). Retire positively-integrated ones gradually (DEC-123).
- ChatGPT toolkit drops need a full audit before use (DEC-095).

## Builds
- Played: `<repo>/Dispo Game Builds/slice-38b9e5c/` (playtest 1), **`playtest2-741bb43/DispoGame.exe`** (playtest 2; doors need `Dispo Game Builds/Docs/Reference/DOORS.json` until the GAME-026 TextAsset fix). Next: BUILD-008 after ART-013 + GAME-026, gated by QA-004.
