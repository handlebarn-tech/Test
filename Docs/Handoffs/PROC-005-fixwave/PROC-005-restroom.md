# PROC-005 fix wave: restroom family (13 assets)

Status: **PASS**. All 13 assets validate at LOD0..3.
- Determinism: two full runs gave identical `export_sha256` for all 13 assets.
- Contact sheet: `Docs/Assets/Specs/PROC_restroom_contact_sheet.jpg`. The old `.png` sheet is `git rm`'d.
- Nothing is committed.

Files changed:
- `Tools/Blender/generators/restroom.py`
- `Tools/Blender/params/restroom.json`
- the generated FBX files, Unity copies and Validation JSON for the 13 assets.

No asset was renamed or dropped, so no manifest pruning is needed.

## What changed, per finding

### #1 Visual bar: LOD0 rebuilt as manufactured fixtures
- **Dispensers** (towel, TP, soap, napkin) share one sheet-metal construction:
  - a chamfered wall back plate;
  - a cover with a rolled hem bead at the rear edge, a 2 mm reveal to the plate, and a front edge rolled over with radius 12–14 mm;
  - piano-hinge knuckles along the bottom front edge (LOD0/1);
  - a key lock (barrel, recessed core, keyway) set to the front bound.
- Per dispenser type:
  - **Towel (DEC-062 manual):** level window in a proud bezel, dispensing slot under the cover, and a pull lever (hub plus paddle).
  - **TP:** twin-roll hood with the roll bottoms exposed, hollow-core rolls and chrome spindles.
  - **Soap:** level window, push plate, nozzle.
  - **Napkin disposal:** hinged top flap with a barrel (declared as a moving part), lock low on the front.
- **Mirror:** channel frame of 4 separate mitred bars with 0.4 mm hairline joints, an 8-point J-section, glass seated in the channel, and 4 corner screw fixings.
- **Cabinets** (tool chest and storage cabinet):
  - carcass built from panels: sides to the floor, top, bottom and back;
  - recessed toe kick;
  - overlay doors with reveals, a chamfered edge and a pressed recessed panel (flat support rings keep the Wear attribute on the real edges);
  - 2 or 3 split-knuckle barrel hinges per door;
  - bent pulls with roses and a cam lock;
  - inside: lipped shelves on shelf pins.
- **Grab bars:** 3-screw flanges with a boss and filleted return bends (a swept tube instead of capped cylinders).
- **Toilet:**
  - foot flange with closet-bolt caps;
  - rim lip with an undercut;
  - tank body inset under an overhanging, bevelled lid;
  - flush lever with an escutcheon, hub and arm;
  - supply escutcheon, angle stop and riser;
  - 8 corner segments, so the bowl and seat are no longer faceted.
- **Lavatory:**
  - chrome overflow ring with a dark insert;
  - aerator housing and screen;
  - lever hub and paddle;
  - wall escutcheons on the trap arm and both supplies, angle stops with oval handles;
  - 8 corner segments.
- **Sconce:** chamfered back plate with 2 screws, top and bottom metal caps on arms, and a bellied cylinder diffuser (emissive part `Shade`).
- LOD0 lathes now use 24 segments (16 before).

### #7 Citations
- Params now carry a `_sources` map naming every colour and finish key, plus a per-variant `_src` for every size, count, type and finish. The old one-sentence `_sources` is replaced.
- Accessory finishes beyond DEC-062's silver towel dispenser are now neutral mid-grey GAP placeholders:
  - `Accessory_Metal`: grab bars, mirror frame, TP, napkin and sconce;
  - `Accessory_Plastic`: soap body.
  - Both are GAP-PROC-37 (new). The towel dispenser keeps silver, now its own key `Silver_Towel`, cited to DEC-062. The `Stainless` key is gone.
- Chrome, Black_Trim, Brushed_Steel, Glass_Dark, Glass_Frosted and Paper_White are cited to GAP-PROC-37 or GAP-PROC-20.
- Vitreous_White, Flat_Black and Mirror are cited to DEC-062.
- `Cabinet_Storage_Large` shelf count (4) and door count are GAP-PROC-38 (new).
- Accessory configurations are GAP-PROC-39 (new): twin-roll TP, towel window/lever layout, soap push plate, napkin flap, sconce form, channel-frame mirror, 3-screw flange and 2-door tool chest.
- The `gaps` list is now: GAP-109, GAP-127, GAP-PROC-20, GAP-PROC-37, GAP-PROC-38, GAP-PROC-39.

### #8 Grab-bar depth and GAP-107
- **Grab-bar depth:** kept at 0.0762 m, with a `_note` on all 3 bars.
  - RF's 0.15 ft (0.046 m) is a schematic outline.
  - A 1.25 in bar with the 1.5 in wall clearance (ADA convention, GAP-PROC-20) needs about 3 in from the wall to the bar face. At 0.046 m the clearance would be about 0.4 in.
  - The `_src` for `depth_m` says explicitly that RF is not matched.
- **GAP-107:** the restroom generator and params never cited it (grep of both files). The only hit in `Tools/Blender` is `Tools/Blender/params/register_counter_run.json:10`, which is the register family's file, so I left it alone. The Hub should route that to the register worker.

## Asset table (tris)

| Asset | LOD0 | LOD1 | LOD2 | LOD3 |
|---|---|---|---|---|
| Lavatory_WallHung | 2572 | 1396 | 124 | 36 |
| Mirror | 700 | 412 | 268 | 12 |
| Toilet | 2156 | 920 | 96 | 24 |
| ToolChest_Black | 3172 | 1468 | 344 | 24 |
| Cabinet_Storage_Large | 4292 | 1884 | 344 | 24 |
| GrabBar_42 / _36 / _18V | 1340 | 428 | 156 | 12 |
| Dispenser_PaperTowel | 1496 | 728 | 312 | 12 |
| Dispenser_TP | 1628 | 772 | 356 | 12 |
| Dispenser_Soap | 1436 | 692 | 284 | 12 |
| NapkinDisposal | 1264 | 584 | 208 | 12 |
| Sconce_L6 | 1068 | 548 | 220 | 12 |

- Every asset is below the `lod0_min` guide, so validation warns (it does not fail). Under DEC-114 those guides apply in both directions and the contact-sheet read decides. These are small wall props and casework whose detail comes from construction, not tri count.
- Mirror LOD1 and LOD2 are above the 75% and 40% ratio guides: the frame must keep its bound-setting screws and channel, and LOD0 is only 700 tris. They still strictly decrease.

## New GAP rows (for the PROC-005 worker to merge into KNOWN_GAPS)

- GAP-PROC-37 | asset | Restroom accessory and hardware finishes beyond DEC-062's silver manual towel dispenser: TP dispenser, soap dispenser, napkin disposal, sconce body, grab bars and mirror frame (neutral mid-grey placeholders, brushed_metal finish placeholder on the metal); faucet/lock chrome, cabinet hinges, dispenser windows/bezels/levers/push plate, sconce diffuser, TP paper, toilet seat shade; cabinet pull stand-off | params | Nolan (what colour/finish are the TP, soap and napkin units and the grab bars) / a photo
- GAP-PROC-38 | asset | Restroom large storage cabinet (`Cabinet_Storage_Large`): shelf count (placeholder 4, evenly spaced) and door count/arrangement (placeholder 2 swing doors); finish stays GAP-PROC-20 | params | Nolan
- GAP-PROC-39 | asset | Restroom accessory configurations beyond the TI §6.6 / DEC-062 types: twin-roll hood TP dispenser, towel dispenser window/lock/lever/slot layout (DEC-062 "manual" overrides the TI "semi-recessed with waste"), soap push plate + window, napkin disposal top flap, L6 sconce as a cylinder diffuser between caps, mirror as a channel frame with corner fixings, 3-screw exposed grab-bar flanges, 2-door tool chest | params | Nolan / a photo

## Checklist note (replacement line for `Docs/Imports/IMP-003_PROC_FIX_CHECKLIST.md`)

PROC-005 done: restroom (13 assets).
- LOD0 rebuilt as manufactured fixtures:
  - sheet-metal dispensers with hem bead, rolled front, hinge line, key lock and window/slot/lever/push plate/lid;
  - mitred channel-frame mirror with corner fixings;
  - panel-built cabinets with toe kick, overlay pressed-panel doors, barrel hinges, pulls, cam lock and lipped shelves on pins;
  - 3-screw grab-bar flanges with filleted returns;
  - toilet with bolt caps, rim lip, overhanging tank lid and flush lever;
  - lavatory with overflow ring, aerator, lever, escutcheons and angle stops;
  - sconce with plate, caps and diffuser.
- Every size, count, colour and finish is cited per key (`_sources` / `_src`), with new GAP-PROC-37/38/39.
- Grab-bar depth stays 3 in, with a `_note` (RF 0.15 ft is the outline; 1.5 in clearance is under GAP-PROC-20).
- Validation, determinism and the Eevee contact sheet `PROC_restroom_contact_sheet.jpg` pass.
- LOD0 is 700–4292 tris.

## Questions for Nolan (through the Hub), DEC-047 format

1. **Accessory finishes (GAP-PROC-37).**
   - Source: DEC-062, which names only the old silver manual paper-towel dispenser; the restroom has no photos (GAP-109).
   - What I see: no evidence for the TP dispenser, soap dispenser, napkin disposal or grab bars.
   - Candidates: (a) all stainless/silver like the towel unit; (b) white or black plastic TP and soap units with stainless bars; (c) mixed.
2. **Storage cabinet interior (GAP-PROC-38).**
   - Source: DEC-062 / DEC-068 and RF `Cabinet_Storage_Large` (3.2 × 1.5 × 7.0 ft).
   - What I see: nothing on shelf or door count.
   - Candidates: 2 doors with 4 shelves (placeholder), 2 doors with 5 shelves, or 1 door.
3. **TP dispenser form (GAP-PROC-39).**
   - Source: TI §6.6 "surface toilet-paper dispenser".
   - Candidates: twin-roll hood (placeholder), single-roll, or jumbo-roll.
4. **Toilet seat colour.**
   - Source: DEC-062 "standard white toilet".
   - Placeholder: white seat and lid. Candidates: white or black (an open-front black seat is common in commercial restrooms).

## Infra observation (not fixed; for the PROC-005 worker)
- `proclib._wear_attr` writes wear per vertex, so a large flat face whose vertices all sit on convex edges reads as fully worn across its whole area.
- Example: the door border band between the chamfer and the pressed panel showed as a light "glass" pane on the flat-black tool chest.
- I worked around it in my generator with flat support rings.
- Other families' bevelled boxes (`add_beveled_box`) have the same pattern on their big faces.
