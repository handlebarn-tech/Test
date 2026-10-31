# PROJECT STATE

Hub-owned, the **only live state record** (DEC-117). A fresh Hub reads `PROJECT_BRIEF.md` → `HUB_RESUME.md` → this file, then reconciles the tables below with `list_sessions` (linked and unlinked), `git branch --no-merged main` and dirty worktrees (STUDIO_OS §0.9). Plan: `Design/ROADMAP_POST_SLICE.md`. Registry: `BACKLOG.md`. Workers and reviewers do not read this file.

**Updated:** 2026-10-30 evening by RECOVERY-001 (Fable) after the clean cutover (DEC-144): every pre-recovery session archived; all uncommitted work committed; this file is the sole resume point. **Milestone:** PS1 done; Nolan has played `playtest2-741bb43` (findings `Design/PLAYTEST2_2026-10-30.md`). **Current milestone: M-B Believable store** (roadmap §2). Exit = BUILD-008 candidate **plus QA-004 PASS on every PT1 + PT2 requirement in the build before Nolan gets it** (DEC-120). PS1b starts when GAME-026 merges (GAME-017a).
**Studio structure:** Nolan → Hub (project manager, integrates) → workers → fresh reviewers (DEC-138..142; `Docs/Audits/RECOVERY-001.md`). The dispatcher-only Hub, planner/integrator sessions and the spare pool are retired. **Caps:** 4 concurrent worker/reviewer sessions, 2 Unity editors.
**Account:** Pro plan; the weekly limit was hit on 2026-10-30 ~13:30 and resets 2026-10-31 ~19:00 Phoenix. Every session below that says "usage limit" died mid-task; its WIP is committed on the branch named.

## Recovery: work stranded by the usage limit (start a FRESH worker from the branch; never resume the dead session)
| Task | Branch @ sha (committed WIP) | State | Next Hub action |
|---|---|---|---|
| **GAME-026** customer flow | `task/GAME-026` @ 060f4af; `review/game026-r4` @ 16be0c3 holds only a merge of `main`, **no r4 verdict was written** (reviewer died at the limit) | r1–r3 FAIL; r2/r3 MAJOR = stale `Data/Reference` copies vs `main` | Fresh reviewer on `task/GAME-026` @ 060f4af (check 0: contains `main`?). If the stale-copy MAJOR recurs: Hub decision (§0.7). Packet still names a lead/pool: brief the correction. |
| **ASSET-005/006** wardrobe + hair | `claude/sweet-shirley-002b17` @ b42a4ae (worker archived in the cutover; its last state: garment + hair rebuild generators running, 60-customer export, sheets, docs and handoff not done) | WIP, no handoff; `customer_gen.py` shared with ASSET-007 (merged) | Fresh worker from the branch with `Tasks/Active/ASSET-005.md`; reviewer re-runs the C001 regression. |
| **ART-013** layout overhaul (P0, critical path) | `claude/art013` @ 14b3eb3 | converter rev9 south side done; Unity builder, PROC doors, `--matrix`, ID-stand/guard pair, captures, handoff not done; details in `Handoffs/Recovered/ART-013_partial.md` (incl. a POS_05 clearance data conflict and a jar-count ruling for the Hub) | Fresh Unity worker from the branch with `Tasks/Ready/ART-013.md`; merge `main` first; needs a Unity slot and `git lfs pull`. |
| **PROC-007** UV layout | `claude/hopeful-mendeleev-39bba2` @ 1947e0e (packet → Active only) | not started | Fresh worker; base `main` (PROC-005 merged). ART-011 follows in the same wave. |
| **GAME-017a** first playable rec depth | `claude/adoring-bell-224eaa` @ db1b48b (packet → Active only) | not started; shares Slice files with GAME-026 | Start only after GAME-026 merges. |
| **PROC-013b** door follow-ups | `claude/intelligent-lumiere-b0fd09` @ 44999a7 | **ready for review** (reported 13:28) | Fresh reviewer (Sonnet if no Unity needed). |
| **DOC-006** LFS pointer guard in `studio.ps1` | `claude/brave-boyd-7af7b5` @ 8f39d2b | **ready for review**; BACKLOG row to add | Fresh reviewer; add the BACKLOG row at integration. |
| **DOC-004** GSS §28 fast recommendation | worker `claude/infallible-bhaskara-f98714` @ 3e47f69; `review/doc004` **PASS with minors** | awaiting integration (spare-11 died) | Hub integrates (§0.8). |
| **PROC-009b** vehicle look follow-ups | `claude/jovial-sutherland-c52674` @ aefadfc (the 13 uncommitted files were committed by RECOVERY-001; unreviewed) | WIP: re-exported vehicle FBX, params, contact sheet, `Previews/PROC-009b/` | Fresh worker from the branch. |
| **PROC-014** QA review renders + fault tests | `claude/sleepy-keller-7875af` @ d8cf4b3 (partial handoff on branch) | review mode + planted-fault tests pass; PROC_PIPELINE A1 section and review-sheet size fix left | Fresh worker from the branch. |
| **PROC-018** HUB storage + refill station | `claude/adoring-nash-8593f0` @ 448e9b1 | hub_storage done; refill_station params only | Fresh worker from the branch. |
| **PROC-015** architecture kit research | `claude/elegant-nash-3c26bb` @ 3e47f69 | research-only WIP handoff | Fresh worker from the branch. |
| **PROC-017** entry queue kit | `claude/hopeful-engelbart-ed1ea5` @ 7f4f7d6 (packet → Active + the untracked `entry_queue_kit.py`/`.json` committed by RECOVERY-001) | generator started, unreviewed | Fresh worker from the branch. |
| **REF-015** exterior envelope | `claude/dazzling-jennings-baa5c9` @ 0afad5c (partial handoff on branch) | measurements done; rows/§10/n1–n3 not written | Fresh worker (Sonnet) from the branch. |
| **UX-003** shift-day UX spec | `claude/determined-elgamal-c29f29` @ 0125c2e (partial handoff) | nothing written | Fresh worker (Sonnet); low priority (PS2). |
| Verified already on `main`, branches can be retired when convenient | `claude/audit-001-b559c2`, `claude/xenodochial-bell-85575c`, `claude/gifted-kapitsa-91bb28` (content identical to `main`); `worktree-agent-ad1cfeade6bad8b2d` (PROC-009 v1, superseded by the merged fix rounds) | — | none now (DEC-123) |
| Captured, superseded | `worktree-agent-a83016d0b10c940eb` @ 788046a (the 58 PROC-013 originals, 30 differ from the merged relaunch); `claude/clever-lamport-837e7f` (one early PROC-005 validation json) | preserved, unreviewed | retire when convenient (DEC-123) |
All pre-recovery sessions were archived in the cutover (DEC-144): old Hub `local_35b16660`, PO session `local_0e722850`, side chat, spares 6–13, every dead worker and reviewer. Nothing resumes from a conversation; everything above resumes from its branch. Every worktree is clean apart from Unity `.meta` import noise and one HDRP settings asset Unity rewrote.

## In flight (sessions actually working)
| Session | Task | Branch @ sha | State → next Hub action |
|---|---|---|---|
| none | | | The cutover archived everything; the Hub starts fresh workers from the recovery table as tasks are ready and the caps allow. |

## Queue (next packets, in order; prerequisites in BACKLOG; obey the caps)
1. Integrate **DOC-004**; review **PROC-013b** and **DOC-006**.
2. **GAME-026** to a verdict (see Recovery), then **GAME-017a** → PS1b chain GAME-017 → 018 → 019 → 020.
3. **ART-013** (Unity slot 1) and **PROC-007** → **ART-011** (Unity slot 2) in parallel; both are on the M-B critical path. ART-013 re-copies `DOORS/SCENE_ANCHORS` if GAME-026's copies land first.
4. **PROC-009b**, **PROC-014**, **PROC-018**, **PROC-015**, **PROC-017**, **REF-015** as slots free (Blender/doc work; no Unity).
5. **BUILD-008** candidate → **QA-004** PT1+PT2 validation → only on PASS does Nolan get playtest 3 (DEC-120).
6. **GAME-CHR-002** after ASSET-005/006/007; **NPC-001** after GAME-026. **UX-003** and PS2 rows after PS1b.
Everything else is Later in BACKLOG; the Hub writes a packet when dependencies are Done.

## Unity slots (max 2, DEC-013)
Unknown after the limit; run `studio.ps1 slots` before starting a Unity session.

## Open with Nolan (batched in the Hub's `FOR NOLAN` reply block, DEC-144)
- RECOVERY-001 §7 items 1–4: **approved with adjustments, DEC-143** (model by work character; 4 + Hub; early handover; clean cutover done).
- **Hub ruling pending → DEC (Hub decides, not Nolan):** jar count in the slice (77 jars vs ~171 slots, DEC-121; from `Handoffs/Recovered/ART-013_partial.md`) and the POS_05 clearance data conflict (REF-016 row). Also: parked cars when more than 15 customers are inside (lot has 15 spaces; DEC-134; REVIEW-PROC009 r3 m5). Proposed: cap at 15, extra customers arrived on foot (DEC-110 W4 sidewalk arrivals).
- **DATA-004** (PS3 gate): needs Nolan's Dutchie/LeafLogix catalog export (GAP-PKG-01). Asked once (RES-001 O14); ask again only when PS2 is in sight.
- **DATA-005:** waits for TFS v7.11.5 (GAP-210); external.
- PROC-005 open sizes/finishes GAP-PROC-14..42 (`Handoffs/PROC-005.md` "Questions for Nolan", DEC-105 search done). Low priority; batch.
- **Never re-ask** (DEC-105): W6 self-closing doors, emergency exit alarm, drum kit, staff-tee print side (DEC-113), W1/W2 layout (measured, DEC-110), register numbering (DEC-079), cash tray (DEC-051/086).

## Risks
- Branches older than today's `main` carry stale copies of `ROOM_FIXTURES`/`DOORS`/`SCENE_ANCHORS`: every worker merges `main` before handoff (§0.5); reviewers fast-fail otherwise.
- Packets of GAME-026 and ASSET-005 still name leads/pools (not edited while their workers were alive); fresh briefs carry the correction.
- The `Dispo Game Builds|Imports|Imports Archive|Assets Cache` folders exist **only inside the repo root** (no `Downloads/` siblings exist); they are now gitignored and stay where they are. Four worktrees also sit inside the repo under `Dispo Game/Dispo Game/`; retire them only when their sessions are archived (DEC-123).
- Max 3 Unity worktrees for disk (MACHINE_PROFILE); 60 worktrees exist. Retire positively-integrated ones gradually.
- ChatGPT toolkit drops need a full audit before use (DEC-095).

## Builds
- Played: `<repo>/Dispo Game Builds/slice-38b9e5c/` (playtest 1), **`playtest2-741bb43/DispoGame.exe`** (playtest 2; doors need `Dispo Game Builds/Docs/Reference/DOORS.json` until the GAME-026 TextAsset fix). Next: BUILD-008 after ART-013 + GAME-026, gated by QA-004.
