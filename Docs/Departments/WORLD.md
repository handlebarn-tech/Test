# World department

Rules for every department: `Docs/STUDIO_OS.md` §0. This file is the World lead's resume and domain state; the lead owns it. Lead session and capacity: `Docs/PROJECT_STATE.md` → "Studio roster".

## Charter
- **Prefixes:** REF, ART.
- **Owns:** `Docs/REFERENCES_INDEX.md`, `Docs/Reference/ROOM_FIXTURES.json`, `Docs/KNOWN_GAPS.md` entries for store facts (GAP-1xx), `Docs/Research/` (store-fact research, DEC-031 read-only), `UnityProject/Assets/_Game/Code/Editor/{Graybox,Lookdev}/`, `_Game/Art/{Graybox,Lookdev}/`, the graybox/lookdev scenes, `_Game/Prefabs/` placement, `Tools/Studio/{graybox_qa,room_fixtures_layout}.py`, `References/`.
- **Does not own:** generators/FBX/imported art (Assets), gameplay code and the Slice scene logic (Gameplay).

## Contracts
- **Provides:** `ROOM_FIXTURES.json` and `REFERENCES_INDEX.md` (real dimensions and placements every generator uses; Assets never guesses a store size), scene anchor/object names that code references (referenced by name/anchor only; fileIDs churn).
- **Consumes:** prefab/FBX names and the asset manifest (Assets); gameplay anchor needs (Gameplay).

## Domain reading (on demand, by §)
`REFERENCES_INDEX.md` (by §), `ROOM_FIXTURES.json`, `ASSET_PRODUCTION_PLAN.md` (realism rule), `Docs/Handoffs/REF-008.md` (CCTV tile map and Nolan's answers). Raw CCTV stills/photos never ship in a build; crop people, network gear and security labels (DEC-006/031).

## Domain rules (pointers)
No invented store facts: labelled placeholder + GAP id (DEC-047); quality bar DEC-084; real-store answers DEC-051/062/068/076/079/088/090.

## Status for Hub
_Lead keeps this ≤15 lines._ 2026-10-30, World lead `local_d19eda58…` live.
- Reconciled: ART-006 (W5A) and REF-010 (W5C, DEC-068 restroom cabinet) are merged; BACKLOG rows fixed. Queue item "DEC-068 into ROOM_FIXTURES" was already done by REF-010.
- Now: REF-011 sales-floor layout audit (registers DEC-039 L + operator access, HUB, deli walls, shelf fill) and REF-012 office walkability + door geometry audit, run in parallel (2 workers, no Unity). ART-007 graybox rebuild follows both (1 Unity slot).
- Door contract with Gameplay: World proposes door object/pivot/swing names in REF-012; Gameplay builds interaction against the committed version.
- Risks: ROOM_FIXTURES so far covers back rooms only; the sales floor lives in graybox_layout + REFERENCES_INDEX §1.5, so REF-011 adds sales-floor rows (contract change Assets consumes).

## In flight
| Task | Worker | Branch | State |
|---|---|---|---|
| — | — | — | — |

## Queue (lead re-orders within DEC-096)
1. **Reconcile BACKLOG rows** for REF/ART (ART-006 shows Active but has a handoff).
2. Playtest 1 layout audit against the references, room by room, before more dressing:
   - **register run:** the south-side registers can't be reached or worked; re-audit the whole layout against TI + CCTV (DEC-039 L shape);
   - **HUB** mapped wrong in places;
   - **office** almost unwalkable at current placeholder density: plan real walking/work space before final assets land;
   - **deli walls:** Nolan believes there are about three, not one; check references; shelving also looks unrealistically full (fill density with Assets' stocking arranger);
   - **doors:** geometry and swing so walking through the store feels natural (interaction with Gameplay).
   - DEC-068 restroom cabinet (by the door) into `ROOM_FIXTURES`.
3. Lived-in pass once final assets are in: slight placement variation, partly used supplies, uneven stocking, cleaning and personal items in believable places.
4. Later: livelier exterior and neighbourhood, occupied break room (with Gameplay/Assets).

## Blockers / Questions for Nolan
- None open. Ask through the Hub only what the references cannot settle (e.g. the deli wall count if CCTV is unclear).
