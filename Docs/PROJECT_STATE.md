# PROJECT STATE

Hub-owned, the **only live state record** (DEC-117). A fresh Hub reads `PROJECT_BRIEF.md` → `HUB_RESUME.md` → this file, then reconciles the tables below with `list_sessions` (linked and unlinked), `git branch --no-merged main` and dirty worktrees (STUDIO_OS §0.9). Plan: `Design/ROADMAP_POST_SLICE.md`. Registry: `BACKLOG.md`. Workers and reviewers do not read this file.

**Updated:** 2026-10-31 early morning (Phoenix) by the post-cutover Hub (Fable) just before Nolan cleared it for a fresh Hub (DEC-156 handover; see "Hub handover" below). **Milestone:** PS1 done; Nolan has played `playtest2-741bb43` (findings `Design/PLAYTEST2_2026-10-30.md`). **Current milestone: M-B Believable store** (roadmap §2). Exit = BUILD-008 candidate **plus QA-004 PASS on every PT1 + PT2 requirement in the build before Nolan gets it** (DEC-120). PS1b starts when GAME-026 merges (GAME-017a).
**Studio structure:** Nolan → Hub (project manager, integrates) → workers → fresh reviewers (DEC-138..156; `Docs/Audits/RECOVERY-001.md`). **Caps:** 6 concurrent worker/reviewer sessions or Agents plus the Hub (hard maximum, not a target, DEC-154), 2 Unity editors. **Model routing (DEC-155):** Hub Fable; workers/reviewers Opus by default; Sonnet only for clearly simple bounded deterministic work; Fable outside the Hub only when Opus is specifically inadequate. Rulings on record: DEC-145 jar fill is visual, DEC-146 POS_05 clearance 3.2 ft, DEC-147 lot cap 15, DEC-148 Hub sync merges / check 0 against a named sha, DEC-150/153 pause and un-pause, DEC-154 cap 6, DEC-155 routing, DEC-156 Hub lifecycle.
**Account:** Pro plan. At this update `get_usage` still shows weekly all-models 100 % (reset 2026-10-31 18:59 Phoenix), weekly Fable 38 %, 5-hour 0 %, extra usage on ($54 of $100 at the fresh Hub's start ritual, 2026-10-31 ~10:40 Phoenix; it confirmed: nothing running, no dirty worktrees, resume branches at the recorded shas). Nolan said usage has reset and to resume; usage is his call (DEC-100). The five sessions started 2026-10-30 18:40–19:00 all died at the weekly limit within ~20 minutes; the Hub committed their uncommitted work on their branches (ART-013 @ 87b89b3, PROC-017 @ 3605d42) and restarted fresh sessions from those branches.

## Recovery: work stranded by the 2026-10-30 usage limit (fresh worker from the branch; never resume a dead session)
Integrated so far: **DOC-004**, **PROC-013b**, **DOC-006**. *queued* = waits for a free unit; *parked* = off the critical path.
| Task | Branch @ sha (committed WIP) | State | Next Hub action |
|---|---|---|---|
| **GAME-026** customer flow (P0) | worker `claude/game026-r4-fa0e50` @ a1225dd (round 4 reported ready: compile, EditMode 801/803, PlayMode 11/12); the dead r4 reviewer's merge branch `claude/review-game026-r4-ddc2f6` holds no verdict | awaiting review | **Started:** fresh Unity reviewer (see In flight). |
| **ART-013** layout overhaul (P0) | `claude/art013-r3-19355d` @ 87b89b3 (= rev9 converter + door frames in the converter, `--matrix` 60 → 4 open rows, GAP-134 pair, DEC-146 applied 114/114, GrayboxBuilder places PROC doors, DEC-145 display jars, capture views, Graybox EditMode tests, plus the killed session's uncommitted edits to the three reference JSONs and §9.3) | deep WIP, no handoff, Unity validation state unknown | **Started:** fresh Unity worker (see In flight); it first inspects the WIP commit and runs the validation. |
| **PROC-017** entry queue kit | `claude/proc017-r2-c7e5be` @ 3605d42 (generator + belt/stand/scanner/stanchion/bag exports and validation JSONs captured uncommitted) | WIP, no handoff | *queued*: next free unit (Opus, Blender). |
| **PROC-007** UV layout (P1; ART-011 waits on it) | `claude/hopeful-mendeleev-39bba2` @ 1947e0e (packet → Active only) | not started | *queued*: needs a Unity slot (both held). ART-011 follows in the same wave. |
| **GAME-017a** first playable rec depth (P0) | `claude/adoring-bell-224eaa` @ db1b48b (packet → Active only) | not started; shares Slice files with GAME-026 | after GAME-026 merges. |
| **ASSET-005/006** wardrobe + hair | `claude/asset005-r2-4273a0` @ 382e835 (WIP + `main` incl. ASSET-007 merged) | WIP, no handoff | **Started** (see In flight). |
| **REF-015** exterior envelope (+REF-016a) | `claude/ref015-r2-e5330b` @ ffa2914 (partial handoff + `main` merged) | rows/§10 not written | **Started** (see In flight). |
| **PROC-014** QA renders + fault tests | `claude/sleepy-keller-7875af` @ d8cf4b3 | partial handoff | *queued* (P1, Blender). |
| **PROC-018** HUB storage + refill | `claude/adoring-nash-8593f0` @ 448e9b1 | hub_storage done; refill params only | *queued* (P1, Blender). |
| **PROC-009b** vehicle look | `claude/jovial-sutherland-c52674` @ aefadfc | WIP, unreviewed | *parked* (P3). |
| **PROC-015** architecture kit research | `claude/elegant-nash-3c26bb` @ 4dbfc2d | research WIP | *parked*. |
| **UX-003** shift-day UX spec | `claude/determined-elgamal-c29f29` @ 0125c2e | nothing written | *parked* (PS2). |
| Verified already on `main` | `claude/audit-001-b559c2`, `claude/xenodochial-bell-85575c`, `claude/gifted-kapitsa-91bb28`, `worktree-agent-ad1cfeade6bad8b2d`, `art013-r2`, `task/GAME-026-r4`, `review/proc013b`, `review/doc006`, `claude/intelligent-lumiere-b0fd09`, `claude/brave-boyd-7af7b5`, `claude/infallible-bhaskara-f98714`, `review/doc004` | — | retire when convenient (DEC-123) |
| Captured, superseded | `worktree-agent-a83016d0b10c940eb` @ 788046a (PROC-013 originals); `claude/clever-lamport-837e7f`; `review/game026*` (r1–r3 verdicts are on `main`; r4 empty); the stopped agents' clean worktrees `.claude/worktrees/agent-*` | preserved | retire when convenient (DEC-123) |

## In flight: NONE. HOLD (Nolan, DEC-157/159): nothing starts until Nolan writes "Resume"; the 19:02 cron (DEC-158) was cancelled; no background Agents for this resume (DEC-159).
The five sessions started at this update (`art013-2`, `rev-game026-r4-2`, `asset005-2`, `ref015-2`, `imp005`) were stopped minutes after launch; they hold nothing beyond their source branches (Recovery table). On resume, start fresh from those branches: ART-013 from `claude/art013-r3-19355d` @ 87b89b3 (Opus, Unity), GAME-026 r4 reviewer against `claude/game026-r4-fa0e50` @ a1225dd (Opus, Unity), ASSET-005 from `claude/asset005-r2-4273a0` @ 382e835, REF-015 from `claude/ref015-r2-e5330b` @ ffa2914, IMP-005 from `main` (packet `Tasks/Ready/IMP-005.md`), then PROC-017 from `claude/proc017-r2-c7e5be` @ 3605d42. The 2026-10-30 dead sessions `art013`, `rev-game026-r4`, `proc017`, `asset005` refused archiving ("live work"); `ref015` is archived. Nolan can archive them from the sidebar; their WIP is on the branches.

## Queue (next packets, in order; 6 is a hard maximum, not a target)
1. Reviewers as deliverables land (ART-013 Unity reviewer; REF-015, ASSET-005, IMP-005 doc/visual reviewers), within the cap.
2. **PROC-017** at the next free unit; **PROC-007** when a Unity slot frees (then **ART-011** in the same wave); **PROC-018**, **PROC-014** as units free (Blender, no Unity); **OPS-004** (Unity build gates on `main`; needs a Unity slot) and **OPS-005** (brief review) when units are free.
3. On GAME-026 PASS: integrate → **GAME-017a** (same Slice files) → PS1b chain GAME-017 → 018 → 019 → 020.
4. **BUILD-008** candidate (packet when ART-013 + GAME-026 merge) → **QA-004** PT1+PT2 gate → only on PASS does Nolan get playtest 3 (DEC-120).
5. **GAME-CHR-002** after ASSET-005/006; **NPC-001** after GAME-026; **GAME-028** (DEC-145 jar binding) after GAME-017a + ART-013. PROC-009b, PROC-015, UX-003 parked.

## Unity slots (max 2, DEC-013)
ART-013 and the GAME-026 reviewer hold both (PROC-007 and OPS-004 wait). A stale `unity.exe` from before the cutover may still be running; workers check `slots` before batchmode and report a blocked slot rather than killing anything.

## Hub handover 2026-10-31 (DEC-156; the previous Hub was cleared by Nolan at ~320k context)
Fresh Hub: do the HUB_RESUME start ritual, then nothing else until Nolan says resume (HOLD, DEC-157). On resume, in this order, within the cap of 6 and 2 Unity slots, Opus by default (DEC-155):
1. Reviewer for GAME-026 r4 against `claude/game026-r4-fa0e50` @ a1225dd (check 0 vs 818598a, DEC-148; Unity). Then ART-013 worker from `claude/art013-r3-19355d` @ 87b89b3 (Unity; its last commit is unvalidated WIP: the worker runs `--matrix`, `--check`, graybox, compile and EditMode first). Then ASSET-005 from `claude/asset005-r2-4273a0` @ 382e835, REF-015 from `claude/ref015-r2-e5330b` @ ffa2914, IMP-005 from `main` (`Tasks/Ready/IMP-005.md`; the drop sits in `<repo>/Nolan Import/`, untracked, never commit it), PROC-017 from `claude/proc017-r2-c7e5be` @ 3605d42. Briefs: STUDIO_OS §0.5 standard text plus the per-task notes in the Recovery table; every brief says "never SendMessage the Hub; end your turn with the one line" (DEC-152).
2. On Nolan's own turn use `start_session`; on a child-completion turn too (DEC-152); after a refusal only, a background Agent (DEC-151).
3. Four 2026-10-30 sessions (`art013` local_62f68467, `rev-game026-r4` local_f1d0ffe8, `proc017` local_7bf91d96, `asset005` local_2795f19a) are "failed" and refused archiving; their work is on the branches above; archive when the app allows, one attempt each. The five sessions started and stopped on 2026-10-31 are archived.
4. Leftover clean worktrees: `.claude/worktrees/agent-*` (stopped agents) and the dead sessions' worktrees (`modest-khorana-945a3b` = ART-013 branch, `hopeful-mendeleev-39bba2` = PROC-017 branch, `inspiring-volhard-934e33` = ASSET-005 branch, `determined-elgamal-c29f29` = REF-015 branch, `adoring-bell-224eaa` = dead GAME-026 review merge); retire only after their branches are integrated (DEC-123).
5. Open DEC numbering: next is DEC-160. BACKLOG rows for ART-013/REF-015/PROC-017/IMP-005 mirror their packet folders at integration (ART-013, REF-015, PROC-017 packets are already in `Active/` on their branches; IMP-005 is in `Ready/` on `main`).
Shared notes for the Hub family: `C:/Users/handl/AppData/Local/Claude-Data/claude_pzs8sxrjxfjjc/side-session-notes/local_69cad76a-59bd-41dd-a4e9-ba5efc0795dc/`.

## Open with Nolan (batched in the Hub's `FOR NOLAN` reply block, DEC-144)
- **HOLD (DEC-157/159):** nothing starts until Nolan writes "Resume"; then sidebar sessions, no Agents.
- **Usage reading:** `get_usage` still reports the weekly all-models window at 100 % until 18:59 Phoenix today while Nolan reports a reset; the Hub proceeded on his word (DEC-100). If sessions die again with "weekly limit", that reading was right and the reset is 18:59.
- **Nolan's design drop** (`Nolan Import/`, 7 files) is in audit as IMP-005; nothing from it is adopted until the audit and review land (DEC-095). It was dropped outside `Dispo Game Imports/` (DEC-070); the worker archives it to the Imports Archive.
- **DATA-004** (PS3 gate): needs Nolan's Dutchie/LeafLogix catalog export (GAP-PKG-01). Asked once (RES-001 O14); ask again only when PS2 is in sight.
- **DATA-005:** waits for TFS v7.11.5 (GAP-210); external.
- PROC-005 open sizes/finishes GAP-PROC-14..42 (`Handoffs/PROC-005.md` "Questions for Nolan", DEC-105 search done). Low priority; batch.
- **Never re-ask** (DEC-105): W6 self-closing doors, emergency exit alarm, drum kit, staff-tee print side (DEC-113), W1/W2 layout (measured, DEC-110), register numbering (DEC-079), cash tray (DEC-051/086), jar count (DEC-145), POS_05 clearance (DEC-146), lot overflow (DEC-147), pacing (DEC-150/153), cap (DEC-154), routing (DEC-155).

## Risks
- Branches older than today's `main` carry stale copies of `ROOM_FIXTURES`/`DOORS`/`SCENE_ANCHORS`: every worker merges `main` before handoff (§0.5); reviewers fast-fail otherwise (DEC-142/148). ART-013 and REF-015 both edit ROOM_FIXTURES (different rows); the second to merge re-merges.
- If the weekly limit is in fact still active, sessions die again before 18:59 Phoenix; workers commit as they go, so this table is the resume point.
- The `Dispo Game Builds|Imports|Imports Archive|Assets Cache` folders exist **only inside the repo root** (gitignored). 52 worktrees exist, max 3 Unity worktrees for disk (MACHINE_PROFILE). Retire positively-integrated ones gradually (DEC-123).
- ChatGPT/outside design drops need a full audit before use (DEC-095): IMP-005.

## Builds
- Played: `<repo>/Dispo Game Builds/slice-38b9e5c/` (playtest 1), **`playtest2-741bb43/DispoGame.exe`** (playtest 2; doors need `Dispo Game Builds/Docs/Reference/DOORS.json` until the GAME-026 TextAsset fix). Next: BUILD-008 after ART-013 + GAME-026, gated by QA-004.
