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
Quality bar DEC-084 (never low-poly/generic; LOD chains; 2K–4K PBR) in every brief; $0 and the license allow-list DEC-023/087; brands DEC-071/078/081; toolkit intake and fix ownership DEC-069/070/083/092; no-overwrite rule DEC-093; **ChatGPT context limits DEC-095**.

## Status for Hub
_Lead keeps this ≤15 lines._ 2026-10-30 (Assets lead `local_172b2109-6384-4914-800b-6dc37226e046`): BACKLOG reconciled (added ASSET-003/004, AUDIO-001, BRAND-001/001b/002, IMP-003, PROC-005/006). 3 of 3 worker slots in use, all Agent subagents in worktrees: PROC-005 resumed from `claude/clever-lamport-837e7f`; IMP-003 re-auditing the rebuilt round 3 (then 4–6) on top of `claude/brave-brattain-30c797`, folding in the REVIEW-W5T follow-ups; PROC-006 phase 1 = register workstation kit evidence spec (DEC-096 #5, no counter geometry until World's register re-audit lands). ASSET-004 paused until a slot frees. Old worker sessions archived by the Hub. DEC-097 (UV layout) approved → PROC-007 queued after PROC-005; World does the label-shader cut-over in the same wave. DEC-098: anything important for Nolan goes to the Hub marked FOR NOLAN.

## In flight
| Task | Worker | Branch | State |
|---|---|---|---|
| PROC-005 toolkit integration + checklist fixes (DEC-092) | Agent subagent (lead) | new worktree; base `claude/clever-lamport-837e7f` | resumed 2026-10-30: wire shelving fix → remaining families |
| IMP-003 rolling toolkit audit | Agent subagent (lead) | new worktree; base `claude/brave-brattain-30c797` | rebuilt round 3 from scratch, then rounds 4–6; old §R3 (REVIEW-W5T partial PASS) superseded |
| PROC-006 register kit spec (phase 1) | Agent subagent (lead) | new worktree off `main` | evidence spec `Docs/Assets/Specs/REGISTER_KIT.md` |
| ASSET-004 MPFB2 customers | — | `claude/task-asset-004` (225ac4a, partial) | paused; next steps in its handoff |

## Queue (lead re-orders within DEC-096)
0. PROC-007 (DEC-097 UV layout + re-export) right after PROC-005 merges; agree the cut-over commit with the World lead.
1. Review/merge path for the three in-flight tasks (Docs reviewer for IMP-003/PROC-006; Unity A for PROC-005 with a borrowed World Unity slot).
2. Each toolkit round after audit: Docs review → Hub → Nolan approval → PROC integration (DEC-095). After rounds 3–6, a research pass of our own where ChatGPT lacked evidence (IMP-003 lists the gaps).
3. PROC-006 phase 2: generators for the register kit once the spec and World's ROOM_FIXTURES rev7 (REF-011: registers + operator zones, deli walls, HUB) land — size from rev7 rows, not the current graybox; World messages when rev7 is on main; then stocking arranger with believable uneven fill; buds/nugs look (low).
4. ASSET-004 resume (CHARACTERS.md rewrite, contact sheet, PROC-CHR-004 scale-to-60, GAME-CHR-002 import with Gameplay).
5. Round 7 (interaction + polish, DEC-091 R7) by this studio after rounds 3–6 are integrated.
6. BRAND-002 name search before any public build (DEC-078). Later (P1): Unity Warehouse/Office packs need a Package Manager download.

## Blockers / Questions for Nolan
- None open (UV layout settled by DEC-097).
- No questions for Nolan.
