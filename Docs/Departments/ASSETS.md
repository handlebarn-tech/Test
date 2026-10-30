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
_Lead keeps this ≤15 lines._ 2026-10-30 (Hub, at handover): three workers paused at the usage limit (PROC-005, ASSET-004, IMP-003). Imports holds ChatGPT round 3 (rebuilt, re-audit) and rounds 4–6; round 7 is ours (DEC-095). No lead session yet.

## In flight
| Task | Worker | Branch | State |
|---|---|---|---|
| PROC-005 toolkit integration + checklist fixes (DEC-092) | session `local_6c216f80-4744-4711-9081-d99ed58eba4f` (idle) | `claude/clever-lamport-837e7f` | stopped mid-task at the usage limit |
| ASSET-004 MPFB2 customers (DEC-087/089) | session `local_d31ad4c5-232b-4628-986c-5d276e71a2a2` (idle) | `claude/objective-archimedes-e3d973` | stopped at the usage limit |
| IMP-003 rolling toolkit audit | session `local_13653ae5-1c1d-43bc-8eaf-e383573d7312` (idle) | `claude/brave-brattain-30c797` | round 3 audited; REVIEW-W5T on `review/wave-5t` (79568f8) partial PASS: needs a follow-up pass (inside-out vehicles, tri counts, §R3 items, DEC-093 wording) + m1 (a real brand only on a category it has in the catalog; TFS EdibleTub and prepack pouch are wrong). Not merged. |

## Queue (lead re-orders within DEC-096)
1. **Reconcile BACKLOG rows** for this department's prefixes.
2. Resume PROC-005 (it unblocks World's final assets).
3. IMP-003: re-audit the **rebuilt round 3** (`Dispo_Game_Blender_PROC_Round3_Rebuild/`) from scratch, then rounds 4 (`…Round4_HQ_v2_EvidenceDriven`), 5, 6. Expect gaps against our research and rooms (DEC-095); after the audits, consider a research pass of our own where ChatGPT lacked evidence. Each round: audit → Docs review → Hub → Nolan approval → PROC integration.
4. **Round 7 (interaction + polish, DEC-091 R7) is done by this studio**, not ChatGPT: plan it after rounds 3–6 are integrated.
5. Playtest 1 (DEC-096): full register workstation kit (label printer, receipt printer, scanner, mouse, keyboard, under-counter storage with bags/boxes/personal/cleaning items, spray bottle hanging from a scale shelf, rag); stocking arranger with believable uneven fill; buds/nugs look (low priority).
6. ASSET-004 MPFB2 customers; BRAND name search of all fictional names before any public build (DEC-078).
7. Later (P1): Unity Warehouse/Office packs (claimed) still need a Package Manager download.

## Blockers / Questions for Nolan
- None open.
