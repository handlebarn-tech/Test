# PROC-005 fix wave: break_room (17 assets)

Worker: break_room family. Files touched: `Tools/Blender/generators/break_room.py`, `Tools/Blender/params/break_room.json`, the 17 FBX (Art/Exports/Procedural + Unity BreakRoom copies), their Validation JSON, `Docs/Assets/Specs/PROC_break_room_contact_sheet.jpg` (new) and `git rm` of the old `.png` sheet (staged). Nothing committed. No assets were renamed or dropped, so no manifest pruning is needed.

**Status: PASS.** Validation passes for all 17 assets on every LOD. LOD1–3 strictly decrease. Two consecutive runs gave identical `export_sha256` for all 17 FBX. Contact sheet and detail renders were inspected.

## What changed

### Finding #1 (DEC-084 visual bar): LOD0 rebuilt as real objects
- **Lockers_Staff (15.0k)**
  - Side panels with a folded front flange run down to the floor around a recessed toe kick.
  - Face-frame rails sit flush with the doors. The mullion and row rails are recessed, so 3 mm reveals show between doors.
  - Compartment floors and a centre divider sit behind the doors.
  - Each of the 12 doors: hemmed (bevelled) panels around a stamped louvre band with 5 angled fins over a real opening.
  - Hardware per door: latch escutcheon, lift handle, padlock hasp staple, and a blank number plate with 2 rivets.
  - Two knuckle hinges per door with pin caps. Rivet rows on the side flanges. Grey cap with an eased front.
  - Hinge metadata is kept on every LOD.
- **Bench_Wood (2.1k)**: 3 eased planks with 6 mm gaps on filleted square-tube U-frames. Cross stretchers, long rails under the planks, a centre stretcher, glides, and countersunk screws in the planks.
- **Boards ×5 (144–536)**
  - Mitred moulded frames: eased outer edge, stepped inner lip with a cove.
  - Recessed face panel and a backer.
  - Whiteboard: red outer frame, white inner trim (RF "red/white frame"), and a marker tray with end caps that stays inside the RF depth.
- **Table_Lunch (1.2k)**: eased top, rounded rect-tube apron and legs, levelling glides, and a corner brace with a screw at each leg.
- **FirstAid_Kit (0.8k)**: box, a door with a 2 mm seam, a moulded door rim, a raised generic cross, a latch tab and a 3-knuckle hinge.
- **Counter_North_Run / Counter_East_Return (1.8k / 2.5k)**
  - Finished end panels to the floor, and a black-melamine carcass seen through 3 mm reveals.
  - TI toe kick: 4 in tall, 2 in recess.
  - Each bay: drawer front over a door, slab fronts with bevels.
  - Black bar pulls: horizontal on drawers, vertical on doors.
  - Eased black top and backsplash. The return keeps the sink cut-out.
- **Uppers_North (1.5k)**: side panels, black interior seen through reveals, 4 narrow paired doors with black bar pulls near the bottom (BAND_03), and hinge metadata.
- **Sink_Double (2.2k)**
  - The deck is a real planar annulus around each bowl: top, underside and edge strip.
  - Coved, tapered bowls have an inner skin and an outer skin (sheet thickness).
  - Strainer baskets with crossbars.
  - Chrome pull-down gooseneck: escutcheon, column, filleted spout, spray head and lever.
- **Microwave (2.6k)**: wrapper behind a full-width fascia. The door has a moulded border and a dark window. The panel holds a display, a 3×4 keypad with gaps, start/stop keys and a door-open button. Side vent ribs and 4 feet.
- **CoffeeMaker_Pod (1.1k)**: base, drip tray with a grate, tower, head with a lid seam, spout, 3 brew buttons, and a rear reservoir with its lid.
- **Hoop_Mini (3.8k)**: wire hamper frame (posts and rings) with a bag, two uprights, a backboard, rim and bracket, a diamond zig-zag net, and a ball with seams.
- **Hooks_Coats (2.7k)**: eased rail with end screws, and 5 cast double-prong hooks on base plates with screws and ball tips.

### Finding #7 (citations)
- `params` now has:
  - a `_sources` map;
  - `_colors_src`, which names a source or GAP for every colour key;
  - a `finishes` override map, with GAP-labelled finishes where they aren't sourced;
  - a per-variant `_src` covering every size and count.
- **`Hooks_Coats` hooks = 5** → GAP-PROC-35 placeholder. The rail-only model is kept and noted: RF 2.5 × 0.8 × 5.5 ft includes the hanging coats and bags. Rail depth and height stay GAP-PROC-19.
- **Board frames.**
  - Bulletin_West frame and face, and the North_Fabric frame (was an uncited aluminium): GAP-PROC-34, neutral greys.
  - BlackFrame face: GAP-PROC-34.
  - Cited from RF: the Cork frame and face (wood/cork), the Whiteboard (red/white), the BlackFrame frame (black) and the North_Fabric face (grey fabric).
- **Table top**: the old uncited pale top is now a worker read of a wall2_R3C5 crop (wood-tone top, dark legs) → GAP-PROC-36 (Low, confirm).
- **Black appliances** are now cited. BAND_03 (in RF `Counter_North_Run` source_tiles, RI §3 row 03) shows a black pod coffee maker and a black microwave with a dark door. Keypad, feet and grate colours are GAP-PROC-34 grey.
- **Other new citations from BAND_03**: black bar pulls; a chrome pull-down faucet; the black speckled top (finish `stone` per TI §6.4 OS3 QZ-1); and the TI §6.4 "black melamine interiors" for the carcass.
- **Finding #8 (backsplash)**: the 4 in height is now GAP-PROC-19, not TI §6.4. TI only says "with backsplash".
- **Neutral greys replace uncited colours**:
  - locker body and hardware;
  - first-aid cross, latch and hinge (red was unsourced);
  - toe kick;
  - hoop frame, backboard, hamper and net;
  - hook rail and hooks.
- Ball orange and the white rim come from a wall2_R3C5 crop read → GAP-PROC-36.
- The top-level `gaps` list adds GAP-127, GAP-PROC-34, GAP-PROC-35 and GAP-PROC-36.
- `Light_Wood` is now a honey/medium wood (0.5/0.3/0.15). It sits between BAND_03, which has a warm cast, and the lighter wall2_R3C5. The citation says white balance is uncertain.

## Asset table (tris)
| Asset | LOD0 | LOD1 | LOD2 | LOD3 | pass |
|---|---|---|---|---|---|
| PROC_Lockers_Staff | 15044 | 5748 | 516 | 24 | ✔ |
| PROC_Bench_Wood | 2136 | 744 | 188 | 36 | ✔ |
| PROC_Board_Bulletin_West | 144 | 96 | 56 | 12 | ✔ |
| PROC_Board_Cork | 144 | 96 | 56 | 12 | ✔ |
| PROC_Whiteboard_West | 536 | 312 | 68 | 12 | ✔ |
| PROC_Board_West_BlackFrame | 144 | 96 | 56 | 12 | ✔ |
| PROC_Board_North_Fabric | 144 | 96 | 56 | 12 | ✔ |
| PROC_Table_Lunch | 1228 | 540 | 108 | 24 | ✔ |
| PROC_FirstAid_Kit | 804 | 436 | 70 | 12 | ✔ |
| PROC_Counter_North_Run | 1768 | 1128 | 96 | 36 | ✔ |
| PROC_Counter_East_Return | 2540 | 1644 | 144 | 36 | ✔ |
| PROC_Uppers_North | 1508 | 996 | 580 | 12 | ✔ |
| PROC_Sink_Double | 2248 | 1196 | 48 | 24 | ✔ |
| PROC_Microwave | 2592 | 1296 | 188 | 12 | ✔ |
| PROC_CoffeeMaker_Pod | 1120 | 624 | 132 | 12 | ✔ |
| PROC_Hoop_Mini | 3820 | 2044 | 532 | 24 | ✔ |
| PROC_Hooks_Coats | 2680 | 1400 | 992 | 12 | ✔ |

**DEC-084 warnings.** Every asset is still under its `lod0_min` guide; per DEC-114 these are warnings only.
- The read is real construction: no slabs, every edge bevelled.
- The flat boards (144 tris) are framed panels whose surface comes from the cork/fabric/enamel maps. Adding geometry would mean inventing content (pinned papers are "not recorded").
- Some LOD1/LOD2 counts sit above the ½ / ¼ guide ratio (warnings). LOD3 stays a block in every case.

## New GAP rows (for KNOWN_GAPS.md, merged by the PROC-005 worker)
- GAP-PROC-34 | asset | Break-room finishes/colours not visible or not recorded, modelled as neutral greys with a placeholder finish:
  - locker body/doors (only the top shows in R3C5) and locker hardware;
  - Board_Bulletin_West frame + face (DEC-062 gives none);
  - Board_North_Fabric frame;
  - Board_West_BlackFrame face and frame material;
  - first-aid cross/latch/hinge;
  - counter toe kick;
  - appliance keypad/feet/drip grate/reservoir;
  - hoop frame/backboard/hamper/net;
  - coat-hook rail + hooks.

  Owner: params | REF / Nolan
- GAP-PROC-35 | asset | Break-room counts and part sizes not covered by GAP-PROC-19 (placeholders):
  - Hooks_Coats hook count (5; hidden under coats);
  - bench plank count/thickness and tube size;
  - locker louvre fin count and number-plate existence;
  - board frame section, face recess and whiteboard tray (not seen);
  - table top/leg/apron sizes;
  - first-aid door depth;
  - microwave keypad layout;
  - coffee-maker button count and reservoir position;
  - mini-hoop hamper height, backboard height, rim and ball radius.

  Owner: params | REF / measure
- GAP-PROC-36 | asset | Break-room colours read by the PROC-005 worker from a wall2_R3C5 crop and not yet in RF notes (Low):
  - Table_Lunch wood-tone top + dark legs (the table's RF row cites DEC-051 only);
  - Hoop_Mini orange ball and light/white rim.

  Confirm, then add them to RF notes. Owner: params | REF / Nolan

## Replacement checklist note (IMP-003_PROC_FIX_CHECKLIST §9, the "PROC-005 done:" line)
**PROC-005 done:** 17 RF assets, rebuilt in the fix wave as real construction (REVIEW-PROC5 #1).
- **Lockers:** flanged sides, recessed kick, 12 hemmed doors with stamped louvres over real openings, lift handle + hasp, blank plate + rivets, knuckle hinges.
- **Bench:** eased planks on filleted tube frames.
- **Boards:** mitred moulded frames; the whiteboard has a red frame, white trim and a tray.
- **Table:** tube apron, legs and glides.
- **First aid:** moulded door, cross and hinge.
- **Counters:** end panels, black-melamine carcass reveals, TI 4 in toe kick with a 2 in recess, drawer-over-door slabs, black bar pulls (BAND_03), eased black top and backsplash.
- **Uppers:** 4 paired doors.
- **Sink:** annulus deck, coved bowls with sheet thickness, strainers, chrome pull-down gooseneck.
- **Microwave / coffee maker:** fascia, keypad, vents, feet, drip grate.
- **Hoop and hooks:** wire hamper, net and ball; cast double-prong hooks.

Every size, count, colour and finish is cited (`_src`, `_colors_src`, `finishes`) or GAP-labelled (GAP-PROC-19/34/35/36). The backsplash height is GAP-PROC-19 (#8). The hook count of 5 is GAP-PROC-35, with a rail-only model (the RF bound includes the coats). Uppers_East is skipped (RF Low). LOD0 tris run 0.14–15k (DEC-114: the visual read passes). The run is deterministic.

## Questions for Nolan (through the Hub), DEC-047 format
1. **Lunch table finish.**
   - Source: `References/Index/cctv/wall2_R3C5.jpg`, crop x 60–240 / y 80–286, under the mini hoop.
   - What I see: a table with a wood-tone (golden) top and dark metal legs, with items on it.
   - Candidates: (a) wood/wood-look laminate top on black legs (modelled); (b) a different table, which would mean the item seen is something else.
2. **Mini hoop colours.**
   - Source: same crop.
   - What I see: an orange basketball sitting in a white/light ring over a dark wire frame. The backboard isn't resolvable.
   - Candidates: an over-the-hamper hoop with a white rim and an orange ball (modelled); hamper colour unknown.
3. **Bulletin board (Board_Bulletin_West, DEC-062).**
   - Source: no imagery.
   - Candidates: cork face with a wood frame (like the hall Board_Cork), or a fabric face with an aluminium frame. Neutral grey for now.
4. **Hook count on the coat rail.**
   - Source: wall2_R3C5, lower-left: coats and bags hide the rail.
   - Candidates: 4–6 hooks; 5 modelled.
5. **Locker body colour.**
   - Source: wall2_R3C5 foreground: only the dark-grey top shows.
   - Candidates: grey like the top (modelled as mid grey), or beige/black.

## Observations for the PROC-005 worker (infra, not fixed here)
- The `wood_light` finish's grain runs horizontally on vertical door fronts: the box projection puts u = x on front faces. It also reads as wavy bands, and the params colour barely shows through the BaseColor map, so the cabinets look pale whatever `Light_Wood` is set to. A per-finish grain rotation, or a v-oriented wood map for vertical faces, would help all the cabinet families.
- Black keys (`Black_Steel`, `Black_Appliance`, `Black_Top`) render mid grey in the Eevee previews (strong spec/rim light). This is the preview lighting, not the data.
