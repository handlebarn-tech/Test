# PROC-005 fix wave: register families (register_station + register_counter_run)

Worker notes for the PROC-005 worker. Not committed. Files touched: `Tools/Blender/generators/register_station.py`, `Tools/Blender/generators/register_counter_run.py`, `Tools/Blender/params/register_station.json`, `Tools/Blender/params/register_counter_run.json`, the generated FBX (Art/Exports/Procedural + the Unity copies under `Fixtures/Register/`), Validation JSON, and the two contact sheets (`Docs/Assets/Specs/PROC_register_station_contact_sheet.jpg`, `PROC_register_counter_run_contact_sheet.jpg`; old `.png` sheets `git rm`-ed).

**Result: PASS.** All 11 assets validate and both reruns gave byte-identical FBX (every `export_sha256` matched). LOD0 runs from 0.5k to 11k tris. Validation warns that LOD0 is under the DEC-084 lower guide on 9 assets; under DEC-114 that is a guide, not a fail, and the contact sheets show the read.

## What changed, per finding
- **#1 visual bar (station).** POS props rebuilt as unbranded manufactured electronics:
  - **Monitor:** tapered rear cover with slotted vents and a recessed I/O block (power, 2 video, USB). The bezel lip steps into an inset screen recess with a glass sheet. Also: menu buttons under the bezel, power LED, VESA-100 plate with 4 screws, tilt hinge barrel, neck with a cable cut-out, chamfered base on 4 rubber feet.
  - **Keyboard:** chamfered case with a recessed key well. Tapered caps with gaps sit in the well. Lock LEDs, rubber feet.
  - **Receipt printer:** chamfered body on rubber feet. The clamshell lid is stepped in with a dark seam line. Paper exit slot with a paper tongue and a serrated tear bar. Feed button and 2 status LEDs on the front ledge, cover-open lever on one side, power rocker on the other.
  - **Card terminal:** swept body, screen glass a hair proud of it, 4×3 keypad plus a function row of rounded caps, chip slot in the lower end face, magstripe groove on the side, status LED. Stand: swivel collar, tilt hinge barrel with cradle cheeks and screws, base on a rubber ring.
  - **Presentation scanner:** rubber foot ring, chamfered weighted base, tilt hinge with side caps, lofted head, raised window bezel with a recessed red window, LED, cable with filleted bends.
  - **Scale stand and handheld scanner:** they already had tube frame, welds, wire shelf, formed tray, scale, trigger and cable, so they are unchanged.
- **#1 visual bar (counters).** Real cabinet construction:
  - **Top:** 2 in quartz slab with an eased edge and waterfall ends.
  - **Carcass:** 2'-1" deep, black melamine interior with a back panel and a bottom deck. Gables carry black edge banding. Toe kicks are 4 in high with a 2 in recess, on both faces.
  - **Staff side:** one two-drawer POS cabinet under each monitor (TI detail 11). Walnut fronts sit proud of the gables, with reveals and HW-2 brass edge pulls clipped over the top edge. Every other bay is an open shelf bay (≤ 36 in) with a banded adjustable shelf on 4 shelf pins, plus back-rail screws.
  - **Customer face:** plywood sheets (4 ft) with hairline seams over a dark backer, carrying the DELI STYLE wrap colour, with an ML-1 band under the top.
  - **Grommets:** a cable grommet with a cap behind every monitor.
  - **Frame flip:** the asset is now exported **staff side front (-Y)** so the contact sheet shows the construction. The customer face is +Y (see `_about`).
- **#2 register mapping.** `LegA_Run` and `LegB_Return` are dropped and replaced by one asset per RF rev7 row:

  | asset | RF row | size ft (L × D × H) | registers (RF POS_xx) | ends |
  |---|---|---|---|---|
  | `PROC_RegisterCounter_North` | Counter_Register_North | 20.6 × 2.2 × 2.833 | 10, 9, 8 (x 36.0/30.0/24.0) | waterfall both; display-case slot (RI §1.5 row 99) |
  | `PROC_RegisterCounter_EastReturn` | Counter_Register_EastReturn (GAP-130) | 9.8 × 2.2 × 2.833 | 12, 11 (y 12.0/16.0) | north end butts the North customer face; south end waterfall |
  | `PROC_RegisterCounter_South` | Counter_Register_South (GAP-129, order GAP-131) | 20.2 × 2.2 × 2.833 | 7, 2, 3, 4, 5, 6 (x 31.0/27.8/24.6/21.4/17.8/14.8) | waterfall both |
  | `PROC_RegisterCounter_SouthReturn` | Counter_Register_SouthReturn (GAP-129) | 2.4 × 2.0 × 2.833 | none | south end butts the South customer face; black ML-1 end panel and faces (R2C5 "black cabinet end") |

  - `station_anchors` per station:
    - register number, `rf_fixture` (POS_xx) and `local_x_m` (RF POS pos minus the counter centre along `plan_axis_x`);
    - the monitor position (RF POS: 0.22 ft inside the staff edge);
    - `scene_anchors` with `Anchor_Register_NN_Operator` (1.0 ft off the staff edge) and `_Call` (1.2 ft off the customer face), matching SCENE_ANCHORS / RI §8.1;
    - component slots, with the scale-stand slot at dx −1.8 ft / dy +0.65 ft from the RF `stand_rect`.
  - I checked the anchors numerically for station 08: local 6.3 ft west of the centre at x 30.3 = plan x 24.0.
- **#6.** GAP-106 (and the closed GAP-107) are removed from both families' params and docstrings. Per-variant `gaps` now cite GAP-129/130/131 where RF does.
- **#7/#8 cites.**
  - Every size, colour and finish in both params is in a per-key `_sources` map, cited to RF/TI/RI/DEC/REGISTER_KIT or labelled GAP-PROC-14/15/22/23/24. Construction detail is named as such.
  - The card-terminal colour had no source, so it is now a mid-grey GAP placeholder (`Plastic_Terminal`, GAP-PROC-14).
  - The "4 in backsplash" is **not in my files**: it is in `break_room.json` (lines ~434/465). The register counter has no backsplash. That fix belongs to the break-room worker (GAP-PROC-19).
  - ExRegister1 is left to the office family, as briefed.
  - The walnut value is darkened to a real walnut tone and labelled as such.
- **No cash equipment** (DEC-051/086) and **no brand marks** (DEC-071/081): nothing added.

## Removed asset ids (prune from the manifest; FBX, Unity copy and Validation JSON already deleted with `git rm`)
- `PROC_RegisterCounter_LegA_Run`
- `PROC_RegisterCounter_LegB_Return`

I also removed those two keys from `Art/Exports/Procedural/manifest.json`, taking the same `.lock` file. `contact_sheet register_counter_run` crashes on manifest entries whose renders are gone, so it could not run without this; no other entry was touched. The manifest diff is large because other families are regenerating at the same time.

Other references to the old ids are outside my ownership and need a follow-up: `Docs/Assets/Specs/GRAYBOX.md`, `Docs/Handoffs/ART-007.md`, `Docs/Handoffs/IMP-003.md`, `Docs/Imports/IMP-003_BLENDER_TOOLKIT_AUDIT.md`, `Docs/Reviews/REVIEW-IMP3B.md`, `Tools/Studio/room_fixtures_layout.py`, `UnityProject/.../graybox_layout.json`, `retail_lookdev.json` (they may mean the graybox, not these FBX).

## Assets (tris)
| asset | LOD0 | LOD1 | LOD2 | LOD3 |
|---|---|---|---|---|
| PROC_RegisterCounter_North | 8616 | 3108 | 564 | 84 |
| PROC_RegisterCounter_EastReturn | 4644 | 1740 | 348 | 60 |
| PROC_RegisterCounter_South | 11032 | 3984 | 768 | 120 |
| PROC_RegisterCounter_SouthReturn | 1156 | 516 | 132 | 24 |
| PROC_Register_ScaleStand | 3784 | 2328 | 848 | 96 |
| PROC_Register_POSMonitor | 2288 | 740 | 124 | 36 |
| PROC_Register_Scanner_Presentation | 1032 | 728 | 148 | 24 |
| PROC_Register_Scanner_Barcode | 536 | 344 | 156 | 36 |
| PROC_Register_Keyboard | 7296 | 1472 | 280 | 12 |
| PROC_Register_ReceiptPrinter | 1172 | 692 | 96 | 24 |
| PROC_Register_CardTerminal | 1496 | 1088 | 180 | 24 |

## New GAP rows (full text, for KNOWN_GAPS)
- GAP-PROC-40 | asset | Register counter construction values not in RF/TI: 3/4 in carcass and plywood face thickness, 4 ft wrap-sheet width, ≤36 in open-bay width and shelf height, 15 in two-drawer POS cabinet width, 1 in top overhang past the staff-side drawer fronts, the SouthReturn carcass depth (22.5 in, so it fits the RF 2.0 ft row), the grommet colour, the walnut shade; DELI STYLE wrap shown as a flat teal average until a checker print texture exists (DEC-090) | params | REF/measure; texture task for the wrap print
- GAP-PROC-41 | asset | Register counter top: TI §6.4 says QZ-2 white quartz on a 2'-6" deep POS top, but the REF-003 stills (RI §2.2) read the top as black stone-look with light veining, and RF rev7 rows are 2.2 ft deep. The generator uses RF depth and TI colour | Low | Nolan (top colour); REF (depth)
- GAP-PROC-42 | asset | Customer-face finish of the two returns: EastReturn carries the North/South DELI STYLE wrap by continuity (no still shows its west face); SouthReturn is black ML-1 from R2C5 "black cabinet end" (Low) | Low | Nolan / a still of the returns

Proposed replacement text for GAP-PROC-15 (drop the GAP-106 cite; review #6):
- GAP-PROC-15 | asset | Register counter ML-1 band height, drawer reveal, pull width, grommet size/inset, and the countertop component offsets (keyboard, printer, scanner, card terminal, monitor dy); station x, monitor inset, scale-stand slot and operator/call anchors come from ROOM_FIXTURES POS_xx / SCENE_ANCHORS | draft params | ART/REF

## Checklist line (IMP-003_PROC_FIX_CHECKLIST, replace both "PROC-005 done:" lines)
- §4 register station: **PROC-005 done (fix wave):** POS props rebuilt as unbranded electronics. Monitor: tapered rear cover, vents, I/O block, inset screen in a stepped bezel, buttons, LED, VESA plate + screws, tilt hinge, base on rubber feet. Keyboard: key well, gapped tapered caps, LEDs, feet. Receipt printer: clamshell seam, serrated tear bar, paper tongue, feed button, LEDs, lever, rocker, feet. Card terminal: proud screen, 4×3 + function caps, chip slot, magstripe groove, swivel/tilt stand. Presentation scanner: hinge, window bezel, foot ring, cable. Every params value cited or GAP-PROC-14. Byte-identical reruns. LOD0 0.5–7.3k tris (DEC-114).
- §5 register counter: **PROC-005 done (fix wave):** re-mapped to RF rev7 rows North (10/9/8), EastReturn (12/11, GAP-130), South (7,2,3,4,5,6, GAP-129/131) and SouthReturn (no register); LegA/LegB dropped. TI §6.4 construction: slab top + waterfalls, banded gables, two-drawer POS cabinet with HW-2 pulls under each monitor, open banded shelf bays on pins, toe kicks, wrap sheets with seams (DEC-090), grommets. Exported staff side front. `station_anchors` carry RF POS x, SCENE_ANCHORS operator/call anchors and component slots. GAP-106 removed. LOD0 1.2–11k tris.

## Questions for Nolan (through the Hub), DEC-047 format
1. **Counter-top colour.**
   - Source: TI A940 detail 11 (RI §6.4 "QZ-2 white quartz") vs REF-003 stills `References/Index/register/east_stand.jpg`, `wide_stand_A.jpg` (RI §2.2 "counter top is black stone-look with light veining").
   - What I see: the two sources disagree.
   - Candidates: (a) white quartz per TI (modelled now); (b) black veined stone-look (a later change).
   - GAP-PROC-41.
2. **Keyboard room in front of the monitor.**
   - Source: RF POS_08..POS_12 `pos_ft`, monitor centre 0.22 ft inside the staff edge (RI §8.1 "monitor centre on the staff edge").
   - What I see: a monitor base there leaves no counter-top for the keyboard on the staff side.
   - Candidates: (a) the RF point is the station anchor and the monitor really sits further toward the customer (component slot dy −0.30 m now, GAP-PROC-15); (b) the keyboard sits on a tray or shelf below the top.
   - Answerable by the Hub/REF from the R2C3/R2C4 stills.
3. **East and south return faces.**
   - Source: R2C5 tile (`References/Index/cctv/wall2_R2C5.jpg`, "black cabinet end"); no still shows the east return's west (customer) face.
   - Candidates: (a) wrap continues on both returns; (b) the returns are plain black ML-1.
   - GAP-PROC-42.

## Infra notes (not fixed, per the brief)
- `contact_sheet <gen>` raises if a manifest entry's renders are missing (dropped or renamed assets). A skip-missing guard in `run_generator.contact_sheet` would avoid hand-pruning the manifest.
- The acrylic scale-stand panel and draft-shield bowl render as near-opaque grey in the Eevee sheet. Either the `glass` finish's alpha is not applied in the preview or the colour alpha (0.25) is ignored. Worth a look in proctex/preview.
