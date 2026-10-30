# PROC-005 handoff (in progress)

**Branch:** `worktree-agent-ac7414483b9f8bb4a`. It merges `claude/clever-lamport-837e7f`, which holds the core slice 4ef04ae and the WIP commit 87807ad.

## Commits
1. **Core slice (4ef04ae):** C1–C11 and Q0.5.
2. **Wire shelving (102f126):** fixed the caster fork sweep, whose profile axes were swapped (plate width landed on X), and the LOD3 shelf extents. The swivel race is now no wider than the collar. V-grooves and 6-sided truss wires keep the 2-section runs under the 80k guide. 8 RF racks.
3. **Register station (c1fdf71):** 7 unbranded POS props, no cash drawer (R1–R5).
4. **Register counter run (4070f60):** TI §6.4 POS counter as two L legs with DEC-039 anchors (RC1–RC5).
5. **Deli (3c4119e):** jar walls N/S/E plus the deli counter as two L legs (D1–D5).

Each family has its own contact sheet: `Docs/Assets/Specs/PROC_<generator>_contact_sheet.png`. The checklist `Docs/Imports/IMP-003_PROC_FIX_CHECKLIST.md` is ticked per item, with a "PROC-005 done" note per family.

## Validation (every family)
- `blender.ps1` validation passes, with the opt-in checks on (origin, degenerate faces, material slots).
- Two runs give byte-identical FBX (sha256 compared).
- The existing manifest entries are unchanged: jars, fill and packaged goods have the same `export_sha256`. Only new assets were added.
- The FBX files are copied to `UnityProject/Assets/_Game/Art/Procedural/Fixtures/{WireShelving,Register,Deli}/`. They have no `.meta` yet, because Unity has not been run.

## LOD0 tris vs the DEC-084 guide
- **Wire shelving (20–80k):** within the guide.
  - Rolling 36.5k, East Wall 71.2k, West Run 68.8k, South Wall 44.4k.
  - Chrome Cartons 35.2k, Bags/Tools 30.6k, WireRack desk 38.2k, JC rack 27.9k.
  - LOD1 is about ½, LOD2 about ⅙, LOD3 under 300.
- **Register station:** below the guide; validation warns.
  - ScaleStand 3.8k (guide 20k), Keyboard 7.3k.
  - Monitor 2.0k, CardTerminal 1.1k, scanners 0.5k, ReceiptPrinter 0.4k (guide 5k).
- **Register counter:** LegA 4.5k, LegB 1.8k (hero guide 30k); validation warns.
- **Deli:** jar walls 4.6k / 3.9k / 2.6k, counter legs 0.3k / 0.2k (guide 30k); validation warns.

## Left (not started)
- **Families, in this order:**
  - §7 cooler/fridges;
  - §8 office;
  - §9 break room;
  - §10 restroom;
  - §11 janitor (J1, J3; J2 is done);
  - §12 architecture;
  - §13 exterior;
  - §14 ladder;
  - §15 display cases (the countertop case is referenced by the register run as `PROC_DisplayCase_Countertop`);
  - §16 clutter (rack bins/trays moved here from Q1 wire racks);
  - §17 arranger;
  - §18 labels;
  - §19 materials;
  - §20 ID stand / bags / signs.
- **Cross-family items:**
  - Q0.2 UVs: blocked on ART's texel target. The UV layout is kept as is (UVMap_Label on channel 1, per the lead).
  - Q0.3 PBR textures, including the leaf, checker and wrap patterns.
  - Q0.4 wear: params are recorded, and the Unity builder must consume them.
  - Q0.6 frame budget.
  - P5: register GAP-PROC-13..16 in the PP GAP table and KNOWN_GAPS.
  - PP doc update.
- **Unity import check** (no editor slot this session):
  - verify the `to_unity` X negation with an EditMode test;
  - generate the `.meta` files;
  - check that the BoxColliders from `collision_boxes` line up.

## GAP ids used
- GAP-PROC-13: wire racks.
- GAP-PROC-14: register station.
- GAP-PROC-15: register counter.
- GAP-PROC-16: deli. The checklist's D5 named GAP-PROC-14 for the deli case placeholder, but 14 is the register station's, so the deli uses 16.
- None of these is in the PP GAP table yet (P5 open).

## Questions for the lead (pipeline/ART, not for Nolan)
1. **DEC-084 lower guide on small props and flat fixtures.** A receipt printer at 5k, or a plywood-front counter at 30k, would need invented geometry. I added only real detail and left the warnings standing.
   - Options: lower the per-family `tri_guide.lod0_min` (for example 1k for countertop electronics), or have the PBR/normal-map work (Q0.3) carry the detail.
   - Placeholder meanwhile: the current tris, with the warnings.
2. **Register leg mapping (ART, DEC-039 / GAP-106).**
   - Draft: LegA (22 ft run) holds 7,2,3,4,5,6 then 12,11 toward the outer corner; LegB (9.5 ft return) holds 10,9,8.
   - It lives in the params `registers` lists, so it is a params edit if ART maps it differently.
   - The deli L split is also a draft: LegA 20.2 ft, LegB 4.7 ft at the west end, depth 2.5 ft (GAP-PROC-16).
3. **Drops out of IMP-003 scope.** The imports folder now also holds `Dispo_Game_Blender_PROC_Round3_Rebuild` and Round4–6. They are not in this checklist and were not opened. Does an audit/IMP task cover them?

## Questions for Nolan (through the Hub)
- None. Per DEC-105 I checked DECISIONS.md (DEC-039/043/050/079/084/086/088/090), REFERENCES_INDEX §1.5/§2.2/§2.4/§6.4 and the IMP-003 handoff. Every open size is a GAP param, and the open mappings are ART's.
