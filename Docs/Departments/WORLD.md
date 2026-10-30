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
_Lead keeps this ≤15 lines._ 2026-10-30, World lead `local_d19eda58…`; reports to Hub `local_78db2735…`.
- **Merge-ready:** `review/world-1` @ b30d72c = REF-011 (sales floor, ROOM_FIXTURES rev7, SCENE_ANCHORS.json) + REF-012 (office walkability, DOORS.json), both PASS with minors fixed (REVIEW-REF11/REF12). Merges clean with main.
- Findings: south counter +2.6 ft north for a 3 ft staff aisle; 3 deli walls (N/E/S); HUB desk at the north end; office meets the 3.0/2.5 ft clearances; 15 doors, entry is a pair.
- Now: ART-007 rebuilds graybox/lookdev from these (World Unity slot).
- DEC-110 answered W5–W7; W1–W4 rejected → REF-013 settles them from the TI/floor-plan vectors, then joins `review/world-1` and ART-007. Rule: no layout question without a floor-plan/TI measurement attempt.

## In flight
| Task | Worker | Branch | State |
|---|---|---|---|
| REF-011 sales-floor audit | subagent (done) | `worktree-agent-a3e83b7d768da38d0` 2731c1a | PASS (REVIEW-REF11) → on `review/world-1` |
| REF-013 drawings measure + DEC-110 | subagent (worktree) | off `review/world-1` | running |
| ART-007 graybox rebuild | subagent (worktree, Unity slot) | off `review/world-1` b30d72c | running |
| REF-012 office + doors audit | subagent (done) | `worktree-agent-a2f71eef653a08c1c` e798f88 | PASS (REVIEW-REF12) → on `review/world-1` a452259 |

## Queue (lead re-orders within DEC-096)
2. Playtest 1 layout audit against the references, room by room, before more dressing:
   - **register run:** the south-side registers can't be reached or worked; re-audit the whole layout against TI + CCTV (DEC-039 L shape);
   - **HUB** mapped wrong in places;
   - **office** almost unwalkable at current placeholder density: plan real walking/work space before final assets land;
   - **deli walls:** Nolan believes there are about three, not one; check references; shelving also looks unrealistically full (fill density with Assets' stocking arranger);
   - **doors:** geometry and swing so walking through the store feels natural (interaction with Gameplay).
2b. **DEC-097 label UV cut-over:** Lookdev label shader reads UV channel 2 (lightmap UV on channel 1); agree timing with the Assets lead, then do it in ART-007 or a small ART task.
2c. **Assets ask (low):** staff tee (DEC-089) logo chest side from BAND 05/12; reply to the Assets lead with side + crop, or "not shown → GAP". Not started; DEC-112 retired departments, so it is left for the Hub (Assets lead was told it was queued).
3. Lived-in pass once final assets are in (DEC-104: small items never uniform between stations; small bins per register, big bins spread out; main cleaning supplies in the restroom cabinet `Cabinet_Storage_Large`, note to add in ART-007/next REF): slight placement variation, partly used supplies, uneven stocking, cleaning and personal items in believable places.
4. Later: livelier exterior and neighbourhood, occupied break room (with Gameplay/Assets).

## Blockers / Questions for Nolan
- REF-012 Qs after DEC-105 filter (searched DECISIONS, KNOWN_GAPS, Handoffs/REF-008, Research). **Forward (batch with REF-011):** hinge side of 7 doors (GAP-137); lever vs push bar on office/JC doors + do entry/HUB/office doors self-close (GAP-138); can customers use the restroom (GAP-139). **Not forwarded:** Q1 standing desk vs deli cart: lead ruling, the cart rolls out, placeholder stands; Q2 "drum kit" = REF-008 Q11, skipped by Nolan in DEC-051, so never re-asked, and plant/wire cart stay GAP-127 placeholders; Q3 "does the retail east exit exist": answered by `Research/OFFICE_FINDINGS.md` B9 (a permit added an east retail door).
- None open. Ask through the Hub only what the references cannot settle (e.g. the deli wall count if CCTV is unclear).
