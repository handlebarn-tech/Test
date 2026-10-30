# PROC-005 fix wave: glass_door_cooler, janitor_props, wire_shelving (citations)

Worker notes for the PROC-005 worker / Hub. Nothing is committed. Status: **PASS**. All 14 assets pass validation, reruns are byte-identical, and the contact sheets were inspected.

## What changed, per review finding

### #1 Visual bar (DEC-084)
- **Cooler_GlassDoor_2Door** is rebuilt as a real merchandiser:
  - sheet-metal sides with rounded front edges, a header with screws, and a top panel;
  - a kick panel with an angled-louvre grille and dark plenum, a centre mullion, and 4 levellers (pad, stem, nut);
  - an interior liner, slotted shelf pilasters, LED strips with diffuser lips, and 5 wire shelves per bay (tube frame, deck wires, support bars, clips, price-tag channel).
  - Doors: an extruded frame with rounded edges (taller bottom rail), a double-glazed unit (two panes + spacer, so the glazing edge shows), a glazing bead, a magnetic gasket, top/bottom hinge covers, a torque-closer housing and a long pull handle. Hinge axes and moving-part groups are unchanged.
- **Fridge_TopFreezer / Fridge_Magnets** are rebuilt as appliances:
  - a wrap shell with rounded vertical edges, a top cap and a back coil panel;
  - pillowed doors (rounded on all front edges) with bulb gaskets, plus door liners and shelf ledges inside the doors (LOD0);
  - pulls on the latch side, hinge covers (top cap, middle bracket, bottom), a framed louvred kick grille, and 4 levellers.
- **Magnets** are no longer uniform squares. A seeded assortment (GAP-PROC-28) of paper sheets pinned by domed disc magnets, slightly rotated photo cards, round discs and rounded tiles, all with varied thicknesses (no z-fight). One full-thickness disc pins the side bound.
  - The contact-sheet cameras never see the +X side. I checked a side render myself (`C:\Users\handl\AppData\Local\Temp\claude\C--Users-handl-Downloads-Dispo-Game--claude-worktrees-task-ref-003-e34c4b\34d782d7-4c37-4646-92d4-c2e9e4c40b1d\scratchpad\mag_ab.png`, taken before the contrast bump).
- **Janitor:**
  - Mop sink: moulded basin lofted with a bullnose rim, drafted walls with a plinth recess, and a cavity sloping to a sump with a barred strainer. Splash guards are rounded/hemmed panels with screws.
  - Mops/brooms:
    - a holder rail with bracket arms and spring-grip rollers, plus hang caps;
    - the mop: clamp head with jaw plate and wing screw, headband, and 64 curved splayed strands;
    - the broom: block, ferrule, and 3 x 18 bristle tufts.
  - Bucket: drafted tub with a bumper band and rolled rim, 4 swivel casters (plate, race, fork, treaded wheel, axle), a side-press wringer with press plate, pivot and lever with grip sleeve, and a bail handle with rivets.
- Shared helpers live in `glass_door_cooler.py` (`rpanel`, `rframe`, `prism_x`, `loop_tube`, `leveller`, `louvres`), and `janitor_props.py` imports `rpanel` from it. No proclib/proctex/run_generator edits.

### #5 Mop bucket and janitor colours/materials
- What the sources say:
  - DEC-062 lists only "a drainage (mop) sink, mops and brooms, a small rack of cleaning supplies".
  - RF `MopSink_JC` says only "square mop sink …, A011 only (no imagery, GAP-109); FRP to 4 ft".
  - RF `Mops_Brooms_JC` gives "mops and brooms standing on the JC east wall".
  - None of them gives a colour or material. DEC-079 is removed from the citations.
- `MopBucket_Wringer` is now a labelled placeholder: `rf` = "none (GAP-PROC-30 placeholder …)", `gap: GAP-PROC-30` (also emitted into the manifest entry), and a `_note`.
- Every janitor colour key is a neutral grey named for its part: Sink_Grey, Guard_Grey, Handle_Grey, MopHead_Grey, Bristle_Grey, Holder_Grey, Bucket_Grey, Wringer_Grey, Lever_Grey, Caster_Grey, Fastener_Grey. All cite GAP-PROC-30 in `_sources`.
  - Removed: Bucket_Yellow, Bristle_Red, Handle_Wood, Mop_Cotton, Moulded_Stone, Stainless and Chrome.
  - The finishes (stone, brushed_metal, cotton, plastic, rubber) are explicit `finishes` overrides, labelled as GAP-PROC-30 render placeholders.

### #7 Citations
- **Cooler:**
  - `_sources` is now a per-key map.
  - Shelf count moved from GAP-PROC-17 to **GAP-PROC-28**. The value changed from 4 to 5, estimated from the FOH still through the left door (Low).
  - `Fridge_Magnets` white is replaced by `Appliance_Grey` (GAP-PROC-28). RF says only "full-size fridge", and R3C5 shows only the covered side.
  - `Fridge_TopFreezer` white is cited to RF ("white top-freezer apartment fridge") and the FOH still.
  - Black frame: RF, RI §2.3 row 230, and the FOH still. Glass/LED: RF "lit merchandiser … two glass doors".
  - Hardware, wire, gasket, liner, grille and handle colours are GAP-PROC-28 greys (cooler handles were black before; that was uncited).
  - The blank header label plate is dropped, because it was unsourced.
- **Wire shelving** (params only; generator untouched). Every variant has a `_src` map, there is a top-level `_shelf_src`, and `gaps` gains GAP-PROC-29.
  - Shelf counts: East_Wall 5, South_Wall 5, Chrome_Cartons 5, Bags_Tools 4, CleaningSupplies_JC 4, and the default 5 are all GAP-PROC-29. West_Run cites RF "4-5 shelves"; Rolling cites DEC-088.
  - `Rack_Rolling.bottom_shelf_z_m` and the default bottom/top heights: GAP-PROC-29.
  - `Desk_WireRack_Computer.shelf_z_m`: GAP-PROC-29. RF gives only "monitor on an upper shelf, keyboard shelf at desk height"; the keyboard level is the 29 in convention.
  - South_Wall stays one 5.3 ft section, labelled GAP-PROC-29. An unequal 4 + 1.3 ft split needs new generator code, because sections split evenly. See question 2.
  - Rerun once: **all 8 FBX `export_sha256` are identical to before**. `params_sha256` changed from 69dd09971ea62805 to 8aa4a90d87f1ffae, so the manifest/validation sha fields change. Git lists the wire FBX as modified, but `git diff --stat` on them is empty (stat-dirty only).
  - The wire contact sheet (.png, non-PBR) was regenerated as is.

## Assets (LOD0 / LOD1 / LOD2 / LOD3 tris)
| asset | LOD0 | LOD1 | LOD2 | LOD3 | export_sha256 |
|---|---|---|---|---|---|
| PROC_Cooler_GlassDoor_2Door | 15160 | 6892 | 900 | 24 | e054fe81133800f6 |
| PROC_Fridge_TopFreezer | 3740 | 1876 | 408 | 24 | 37ef60dccb46c2d5 |
| PROC_Fridge_Magnets | 7172 | 2848 | 420 | 36 | 5b13167a2adece39 |
| PROC_MopSink_JC | 1536 | 540 | 84 | 24 | 3a819d51875b3ae5 |
| PROC_Mops_Brooms_JC | 8712 | 2728 | 396 | 12 | 304598427e44796f |
| PROC_MopBucket_Wringer | 2772 | 1940 | 228 | 36 | 18e19bd2e8ab9da0 |
| wire_shelving (8 assets) | 27.9k–71.2k | unchanged | | | unchanged |

- Validation passes on all assets, and two consecutive runs of each generator gave identical shas.
- Remaining warnings are DEC-084 lower-guide warnings (LOD0 under 30k/20k/5k) on the cooler, fridges, sink and bucket. The bucket also gets a LOD1 > 50 % warning.
- Under DEC-114 the visual read decides, and on the sheets they read as manufactured objects. The sink (1.5k) is a simple moulded form by nature; its detail is in the rim, drain and guards.
- Contact sheets: `Docs/Assets/Specs/PROC_glass_door_cooler_contact_sheet.jpg` and `PROC_janitor_props_contact_sheet.jpg` are new. The old `.png` sheets are `git rm`-ed (staged deletion).
- No assets were renamed or removed, so there is no manifest pruning.

## New GAP rows (for KNOWN_GAPS.md; PROC-005 worker merges)
- GAP-PROC-28 | asset | Cooler/fridge details not resolved in the FOH still or R3C5. Covers:
  - cooler shelf count (5, estimated from the FOH still, Low);
  - colours of cooler hardware/handles, wire shelves, tag rails, gaskets and levellers;
  - fridge handle, seal, liner, grille and coil colours;
  - leveller heights;
  - the Fridge_Magnets body colour (neutral grey; RF says only "full-size fridge") and its door layout (top-freezer and right hinge copied from the FOH fridge);
  - the Fridge_Magnets magnet/sticker assortment. R3C5 shows the side densely covered, but the items can't be resolved, so a seeded neutral-grey set of generic cards, discs, tiles and paper sheets stands in, with no artwork.

  | params (neutral greys) | Nolan photo / closer still
- GAP-PROC-29 | asset | Wire-shelving shelf counts and heights not in any source. Covers:
  - shelf counts for Rack_East_Wall, Rack_South_Wall, Rack_Chrome_Cartons, Rack_Bags_Tools and Rack_CleaningSupplies_JC (West_Run is RF 4–5; Rolling is DEC-088);
  - bottom-shelf / top-drop heights, including Rack_Rolling's 10 in;
  - all Desk_WireRack_Computer shelf heights (keyboard level = 29 in desk-height convention);
  - Rack_South_Wall's 5.3 ft RF width against DEC-088 4-ft sections (kept as one section).

  | toolkit defaults | Nolan / REF run-length pass
- GAP-PROC-30 | asset | Janitor closet items and looks beyond DEC-062. Covers:
  - the mop bucket with wringer: not in DEC-062's closet list or RF, so it is a placeholder asset only;
  - splash guards on the mop sink;
  - every colour and material of the mop sink, guards, mops, brooms, holder and bucket (GAP-109: no imagery). All are neutral greys; the PBR finishes are render placeholders.

  | placeholder | Nolan (does a bucket exist; colours/materials)

## Checklist note (replacement "PROC-005 done:" lines for IMP-003_PROC_FIX_CHECKLIST.md)
- **Cooler §7** (line ~133): **PROC-005 done:**
  - The fix wave rebuilt it as a real merchandiser and appliances. Cooler: wrap sides, header, louvred kick, mullion, levellers, liner with slotted pilasters, LED strips, and 5 wire shelves/bay with clips and tag channels. Its doors have rounded extruded frames, double glazing with spacer and bead, gaskets, hinge covers, a closer and pulls.
  - Fridges: pillowed doors with gaskets and liners, hinge covers, louvred kick grille and levellers.
  - Fridge_Magnets: a seeded mixed assortment of cards, discs, tiles and papers (GAP-PROC-28).
  - All colours are cited (RF / FOH still) or GAP-PROC-28 greys; the shelf count is GAP-PROC-28.
  - LOD0 3.7–15.2k (lower-guide warning; reads as real under DEC-114). Byte-identical reruns.
- **Janitor §11** (line 198): **PROC-005 done:**
  - The fix wave rebuilt it. Moulded mop sink with bullnose rim, sloped cavity, barred strainer and hemmed, screwed guards. Holder rail with bracket arms and grip rollers. String mop with clamp, headband and 64 curved strands. Broom with ferrule and 54 tufts.
  - The bucket is a GAP-PROC-30 placeholder (not in DEC-062/RF): drafted tub, swivel casters, side-press wringer and lever. DEC-079 citation removed.
  - All colours and materials are GAP-PROC-30 neutral greys. Collision boxes kept (J3).
  - LOD0 1.5–8.7k (warning). Byte-identical reruns.
- **Wire shelving** (line 74): append "Fix wave: shelf counts/heights and the South_Wall section cited or GAP-PROC-29 (`_src` per variant); FBX byte-identical, params sha changed."

## Questions for Nolan (through the Hub)
1. **Cooler shelf count.**
   - Source: `References/CCTV FOH Desk Racks 2026-10-29.webp`, crop x 600–1150, y 0–480 (cooler behind the fridge).
   - What I see: through the left door, about 4–5 lit shelf levels in the visible upper half, at a regular pitch.
   - Candidates: 5 shelves (used), 6, or 4. GAP-PROC-28 meanwhile.
2. **FOR NOLAN: BOH south rack sections.**
   - Source: RF `Rack_South_Wall` (5.3 ft, "shortened to clear the ex-register-1 desk") vs DEC-088 "BOH chrome runs: 4-ft sections".
   - What I see: 5.3 ft isn't a multiple of 4 ft.
   - Candidates: (a) one 4-ft section, with the RF width cut to 4.0; (b) one 4-ft + one ~1.5-ft unit (needs a generator change for unequal sections); (c) a 5-ft or 6-ft single unit.
   - The same mismatch affects `Rack_East_Wall` (8.7 ft as 2 × 4.35), which was outside this finding.
3. **Janitor closet bucket.**
   - Source: DEC-062 JC list; GAP-109.
   - What I see: no bucket is mentioned, and there is no imagery.
   - Candidates: (a) there is a wringer bucket, so keep it and supply its colour; (b) none, so drop `PROC_MopBucket_Wringer`.
   - The same question covers the sink material (moulded stone vs plastic vs stainless) and the mop, broom and holder colours.
4. **Break-room fridge.**
   - Source: wall2_R3C5.
   - What I see: the side is covered in magnets/stickers. Body colour and door layout are not visible.
   - Candidates: white top-freezer (like FOH), white bottom-freezer, or a black/stainless single door. Also: which side faces the camera, +X (south) as modelled?

## Not done / risks
- Glass reads frosty and the LED strips don't visibly glow in the Eevee preview. Both come from the shared proctex glass/emissive maps (infra), not this generator.
- `PROC_PIPELINE.md` and other families' files were already modified in the worktree by other workers; I did not touch them.
- Unity import is not checked.
