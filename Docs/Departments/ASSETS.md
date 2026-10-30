# Assets department

Rules for every department: `Docs/STUDIO_OS.md` §0. This file is the Assets lead's resume and domain state; the lead owns it. Lead session and capacity: `Docs/PROJECT_STATE.md` → "Studio roster".

## Charter
- **Prefixes:** PROC, ASSET, IMP, BRAND, AUDIO.
- **Owns:** `Tools/Blender/`, `Tools/Assets/`, `Art/Exports/`, `SourceAssets/`, `UnityProject/Assets/_Game/Art/{Procedural,ThirdParty}/`, `Code/Tests/EditMode/ProcArt/`, `Docs/Assets/`, `Docs/Imports/`, `Docs/ASSET_PRODUCTION_PLAN.md` (domain sections), `Tools/Data/brand_aliases.json` + brand lists (with Gameplay for catalog use); intake of `Downloads/Dispo Game Imports/` art drops and their archiving (DEC-070).
- **Does not own:** real store dimensions (World's `ROOM_FIXTURES`), scene placement (World), gameplay code (Gameplay).

## Contracts
- **Provides:** generator params, FBX/prefab names, the asset manifest, LOD/collision conventions (manifest boxes, DEC-086).
- **Consumes:** `ROOM_FIXTURES.json` / `REFERENCES_INDEX.md` for every real size (named params, never guessed); label text and catalog from Gameplay.

## Domain reading (on demand, by §)
`ASSET_PRODUCTION_PLAN.md` (realism rule), `Docs/Imports/IMP-003_BLENDER_TOOLKIT_AUDIT.md`, `IMP-003_PROC_FIX_CHECKLIST.md`, `Docs/Assets/LICENSE_LEDGER.md`, `Docs/Handoffs/IMP-003.md`.

## Domain rules (pointers)
Quality bar DEC-084 (never low-poly/generic; LOD chains; 2K–4K PBR) in every brief; $0 and the license allow-list DEC-023/087; brands DEC-071/078/081; toolkit intake and fix ownership DEC-069/070/083/092; no-overwrite rule DEC-093; **ChatGPT context limits DEC-095**; **no repeat questions DEC-105** (search DECISIONS, KNOWN_GAPS, Handoffs/REF-008, Research first and list what was searched; answered/skipped questions are never re-asked); pass it in every brief; **measure first DEC-110** (layout/size/clearance questions only after measuring floor plan/TI, CCTV and game files; doors: push bars only on emergency exits + delivery door, levers elsewhere).

## Status for Hub
_Lead keeps this ≤15 lines._ 2026-10-30 (Assets lead `local_172b2109-6384-4914-800b-6dc37226e046`): BACKLOG reconciled (added ASSET-003/004, AUDIO-001, BRAND-001/001b/002, IMP-003, PROC-005/006). 4 of 4 worker slots in use (temporary +1 for ASSET-004 until it is accepted), all Agent subagents in worktrees: PROC-005 resumed from `claude/clever-lamport-837e7f`; IMP-003 re-auditing the rebuilt round 3 (then 4–6) on top of `claude/brave-brattain-30c797`, folding in the REVIEW-W5T follow-ups; PROC-006 phase 1 = register workstation kit evidence spec (DEC-096 #5, no counter geometry until World's register re-audit lands). ASSET-004 resumed (Hub raised capacity). Old worker sessions archived by the Hub. DEC-097 (UV layout) approved → PROC-007 queued after PROC-005; World does the label-shader cut-over in the same wave. DEC-098: anything important for Nolan goes to the Hub marked FOR NOLAN.

## In flight
| Task | Worker | Branch | State |
|---|---|---|---|
| PROC-005 toolkit integration + checklist fixes (DEC-092) | Agent subagent (lead) | new worktree; base `claude/clever-lamport-837e7f` | resumed 2026-10-30: wire shelving fix → remaining families |
| IMP-003 rolling toolkit audit | Agent subagent (lead) | `worktree-agent-aa0d2341e0f4619cc` (4a615d6, 289019d, 02573db, a976d0d) | rounds 3–6 audited (R3b 1/7/2, R4 1/6/5, R5 0/5/0, R6 1/6/0 adopt/adapt/reject); rulings folded in (ecb8132); in review with Docs 2 |
| PROC-006 register kit spec (phase 1) | done (subagent retired) | `worktree-agent-a5f8a932c9a5f07a9` @ 1070e9c | **merged to main (6af8906)**; Nolan answered (DEC-104) → PROC-006b. 13 items, 11 evidenced, GAP-REG-1..10; trash bin RK-09 added |
| ASSET-004 MPFB2 customers | Agent subagent (lead) | new worktree; base `claude/task-asset-004` | resumed 2026-10-30; Docs reviewer `local_99d7e5b7…` |
| PROC-006b register kit generators (DEC-104) | Agent subagent (lead) | new worktree; base main + PROC-005 core | launched 2026-10-30 |

## Queue (lead re-orders within DEC-096)
0. PROC-007 (DEC-097 UV layout + re-export) right after PROC-005 merges; agree the cut-over commit with the World lead.
1. Review/merge path for the three in-flight tasks (Docs reviewer `local_99d7e5b7-ef60-4076-9821-58f16ce3bec0` for IMP-003/PROC-006/ASSET-004; Unity A2 `local_4e865bb8-479c-41c5-8628-7f3e7cb2a4c3` (or B2 `local_041172fa…`) for PROC-005/007 with a borrowed World Unity slot).
2. Each toolkit round after audit: Docs review → Hub → Nolan approval → PROC integration (DEC-095). After rounds 3–6, a research pass of our own where ChatGPT lacked evidence (IMP-003 lists the gaps).
3. PROC-006b running; anchors bind to World's ROOM_FIXTURES rev7 (REF-011: registers + operator zones, deli walls, HUB) land — size from rev7 rows, not the current graybox; World messages when rev7 is on main; then stocking arranger with believable uneven fill; buds/nugs look (low).
4. After ASSET-004: GAME-CHR-002 import with Gameplay (Unity), return the extra slot.
5. Round 7 (interaction + polish, DEC-091 R7) by this studio after rounds 3–6 are integrated.
6. BRAND-002 name search before any public build (DEC-078). Later (P1): Unity Warehouse/Office packs need a Package Manager download.

## Blockers / Questions for Nolan
- None open (UV layout settled by DEC-097).
- No questions for Nolan open (register kit answered by DEC-104).
- Lead rulings 2026-10-30 (IMP-003): Q6, the HUB backstock cabinets, follow the DEC-051 Q9 precedent (plain black closed boxes) until Gameplay files a restock need. Q7 is already settled by DEC-097. Q8, the staff tee print side, is asked of World REF (BAND 05/12) and stays a GAP meanwhile.
