# REVIEW-PROC5: PROC-005 slice 1 (toolkit core, wire shelving, 8 fixture families)

**Reviewer:** Unity pool · **Requested by:** Assets lead · **Verdict to:** Hub (DEC-112) · **Date:** 2026-10-30
**Reviewed:** `worktree-agent-ac7414483b9f8bb4a` @ e9f8173, merged onto `review/proc5` from main db43b6d with no conflicts.
**Sources:** `Docs/Tasks/Active/PROC-005.md`, `Docs/Handoffs/PROC-005.md`, the diff, IMP-003 checklist, DEC-084, REFERENCES_INDEX §1.5/§6.4/§6.6, ROOM_FIXTURES, KNOWN_GAPS, DEC-043/062/079/088.

## Verdict: FAIL

The pipeline core is sound and can be merged on its own. It fails on two counts:
- the visual quality bar (DEC-084);
- citations under the Hub rule: in two families, store values contradict the sources they cite.

## Passed
1. **Determinism.** I reran `janitor_props` headless (`blender.ps1`). The 3 FBX are byte-identical (git shows no change on the LFS objects). Manifest and validation JSON differ only in CRLF/LF line endings.
2. **Existing exports unchanged.** The manifest diff covers all 24 existing entries (jar, fill, packaged goods). `export_sha256`, `params_sha256` and every old field are equal. The only change in `lods.*` is new fields (bounds, geometry checks, material_slots). 68 new assets were added.
3. **Validation self-test.** `Tools/Blender/tests/test_validation.py` passes: all cases, including open quad, zero area, off-origin, no material and LOD-up.
4. **GAP ids and RF dims.** Every cited GAP id exists. RF ids match their ft rows except in the findings below. register_station checks out against RI §2.2. TI §6.4/§6.6, DEC-088 and DEC-090 spot-checks hold up.

## Findings
1. **MAJOR: DEC-084 visual bar.** The contact sheets for every family except wire shelving read as graybox or generic, not realistic:
   - flat untextured slabs: restroom mirror, dispensers and cabinets; office cabinets; deli counter legs (a translucent box);
   - simple extruded shapes: register props, fridges;
   - square "magnets" on a fridge;
   - no visible PBR surface detail.
   LOD0 tris sit at 0.1–7k against guides of 5–20k for props and 20–80k for fixtures. These would not pass as finished assets. Wire racks (28–71k) read as real fixtures. The fix needs real detail or the Q0.3 normal maps, not invented geometry. The handoff's question 1 on a per-family minimum is the Hub's call. I take no position on lowering DEC-084.
2. **MAJOR: register mapping contradicts its source.** `register_counter_run` LegA holds registers [7,2,3,4,5,6,12,11] on `plan_rect_ft` [20,42,7,9.5]. RI §1.5 row 98 (REF-011) says this L holds only 10/9/8 (north) and 12/11 (east). The params ignore RF `Counter_Register_North`/`_EastReturn`/`_South` and GAP-129/130.
3. **MAJOR: phantom deli counter.** `deli_counter_jar_wall` `DeliCounter_LegA`/`LegB` model the plan's "DELI COUNTER" L. RI §1.5 row 101 and §8.1 (REF-011) say that L is the south register run, so these assets duplicate it.
4. **MAJOR: jar-wall depth and fittings.** Jar-wall `depth_m` is 0.366/0.427 m against RF `DeliJarWall_*` 2.1 ft (0.64 m), with no `_note`. The `rf` fields hold RI plan strings instead of RF ids. `shelf_pitch_m` 0.3556 is cited to TI §6.4, but that pitch belongs to the showcase row, and RI says the jar wall is not in TI (GAP-113). Walnut drawers on all three walls contradict RF South ("open bins / wire bins"). DEC-043's photo is probably the north wall only.
5. **MAJOR: janitor closet.** `MopBucket_Wringer` cites DEC-079, which is about deli restock and has no janitor's-closet list. DEC-062's closet list has no bucket. The colours and materials (Bucket_Yellow, Bristle_Red, Handle_Wood, Mop_Cotton, Moulded_Stone, stainless guards) have no source. GAP-109 says there is no imagery, so the bucket's existence is unsourced and the colours and materials need a GAP marker, not plausible defaults.
6. **MAJOR: wrong GAP cited.** GAP-106 is cited for the leg/register mapping (register_counter_run, deli notes, GAP-PROC-15 text). GAP-106 is about the north-wall video-wall/living-wall order.
7. **Minor: uncited values; cite them or name a GAP.**
   - wire-shelving shelf counts (5 or 4) except West_Run and Rolling; `Rack_Rolling.bottom_shelf_z_m`; `Desk_WireRack_Computer` shelf heights; South_Wall as one 5.3 ft section against DEC-088's 4-ft sections;
   - `Hooks_Coats` hook count of 5;
   - break-room finishes: bulletin/fabric board frames, table top, black appliances;
   - office standing-desk and ExRegister1 finishes, where `_sources` claims "from RF";
   - restroom accessory finishes beyond DEC-062's silver towel dispenser;
   - restroom `Cabinet_Storage_Large` shelf count;
   - `Fridge_Magnets` white finish;
   - cooler shelf count of 4, attributed to GAP-PROC-17 although that row doesn't cover it.
8. **Minor: wrong source or missing note.** The "4 in backsplash" is cited to TI §6.4, which only says "with backsplash"; the height belongs to GAP-PROC-19. Grab-bar depth is 0.076 m against RF 0.046 m with no note. GAP-107 is cited but is closed.
9. **Not run: Unity import check and EditMode.** No editor slot was assigned to this review, and the FBX have no `.meta`. It is still owed before merge, together with the handoff's remaining item 12 (to_unity X negation and BoxCollider test).

## Required to pass
- Remodel the non-wire families to DEC-084, or get a Hub decision on per-family minimums.
- Re-map the register and deli fixtures to the REF-011 RF rows (North 20.6 / EastReturn 9.8 / South). Drop or retarget the deli counter legs.
- Fix every MAJOR citation: cite a source or name a GAP.
- Run the Unity import check and EditMode through `studio.ps1`.

## Partial merge option
The core (4ef04ae: proclib, run_generator, validation, manifest collision boxes) and wire shelving (102f126) pass on their own. Wire shelving still needs the minor shelf-count citations from finding 7. They can be split off if the Hub wants the core on main early.
