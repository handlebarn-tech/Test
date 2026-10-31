# PROC-005 fix wave: office_fixtures (worker notes)

Status: **PASS** (validation for all 10 assets; FBX sha256 identical across two runs). Nothing committed.
Files: `Tools/Blender/generators/office_fixtures.py` (rewritten), `Tools/Blender/params/office_fixtures.json`, the 10 FBX + Unity copies + Validation JSON, `Docs/Assets/Specs/PROC_office_fixtures_contact_sheet.jpg` (new). The old `.png` sheet is `git rm`'d (staged). No assets were renamed or dropped.

## Finding 1: visual bar (LOD0 rebuilt as real furniture)
- **Desks** (West_Arm, Corner_Dual_Monitor, ExRegister1):
  - laminate top on a 25 mm core, inset 1.5 mm, with PVC edge banding on all four edges;
  - 2 rear cable grommets (flange with a cap tab);
  - rect-tube four-leg steel frame with apron rails, corner gussets and screws into the top;
  - leg end caps and levelling glides;
  - steel modesty panel with rolled top and bottom hems, on brackets, with screws.
- **Standing desk:**
  - banded top with grommets;
  - two 3-stage rectangular columns with plastic collars;
  - T feet with end caps and levellers;
  - side brackets with screws, crossbar with a telescoping sleeve, motor housing;
  - control box with cable stubs, and an up/down paddle under the front edge.
- **File cabinets** (3 units × 2 drawers):
  - each unit has a carcass (side sheets, top with a rolled front hem, back, recessed kick);
  - drawer fronts with 4 mm gaps and bevelled pan edges;
  - bar pulls, label-holder frames with cards, and a lock cylinder with keyway on each top drawer;
  - drawer boxes on inner/outer telescoping slide members, visible when a drawer opens (the slide_axis moving parts are kept).
- **Tall cabinets:**
  - recessed toe kick on levellers, face frame;
  - a single inset front panel with a 3 mm reveal and a pressed stiffener field;
  - top cap with a hemmed front edge, louvre banks on both sides, back and kick screws.
  - Still no handle, lock or hinge (DEC-051 Q9, RF "no hardware detail").
- **Task chair:**
  - five-star base with hub, socket bosses and twin-wheel casters (hood + stem);
  - chrome gas lift under a ribbed shroud and lift collar;
  - mechanism with tension knob and height lever;
  - crowned waterfall seat cushion (loft) on a pan;
  - T armrests (post, height button, soft pad);
  - spine, closed tube frame on the mesh back with woven weft strands, lumbar band.
- **Stainless worktable:**
  - 4 mm top sheet with down-turned edges and rolled hems underneath, and hat-channel stiffeners;
  - two folding leg frames (tube legs, top bar, cross bar, hinge plates with screws);
  - two-link folding brace with knuckle and bracket;
  - adjustable bullet feet.
  - **No undershelf:** RF says folding legs and tile wall2_R3C3 shows an open frame (GAP-PROC-33, question below).
- **Carts:**
  - plate-mount swivel casters: plate with bolts, swivel race, fork cheeks and crown, axle bolt, profiled tyre;
  - deli cart: pressed trays with marine lip, rolled rim and stiffeners, post collars, U push handle, rail label;
  - wire cart: real welded wire baskets (floor frame and grid, vertical side wires, mid rail, heavy rim), post collars and domed post caps.
- **LOD1** drops screws, slides, louvres, weave and knobs. **LOD2** uses plain parts. **LOD3** is blocks. The tri counts strictly decrease.

Contact-sheet read: every asset now reads as manufactured furniture, with seams, hems, casters and hardware visible in the detail tiles. The GAP grey frames and the grey standing desk are deliberate placeholders.

## Finding 7: citations
- `_sources` is now a map. It cites every colour key and finish override. Each variant has a `_src` map that cites its size (RF fixture id + size_ft), its counts and its part params.
- **Standing desk:** RF `Desk_Standing_East` notes give no colour or finish, so the top, edge and frame are now mid-grey GAP-PROC-31 placeholders. The old black laminate was uncited.
- **Desk_ExRegister1:** RF `Desk_ExRegister1` says "white-top desk". That cites the white top colour only. The laminate finish, the edge colour and the frame colour are GAP-PROC-31, and the edge and frame are now mid grey.
- **Other finishes:**
  - Desk_West_Arm "black laminate" is cited for both colour and finish.
  - Corner piece "black" is cited for colour only; its laminate finish is GAP.
  - Worktable "stainless top" is cited. Its leg colour comes from wall2_R3C3 (light grey, Low); the leg finish is GAP.
  - Cabinets and file cabinets "black" are cited for colour; the steel finish is GAP.
  - Chair "black mesh" is cited. The gas lift, seat fabric finish and plastics are GAP.
  - Deli cart stainless, 2 shelves and handle are cited to RF and RI §2.4; the label colour is GAP.
  - Wire cart "black wire" is cited.
  - Casters, levellers, grommets, controller and hardware are mid-grey GAP-PROC-31.
- GAP greys are linear 0.21 (sRGB mid grey).
- **Counts:** the file-cabinet count of 3 (RF "several") and 2 drawers per unit, the basket count of 3, and the grommet count are GAP-PROC-32. The deli cart's 2 shelves are cited (RF "2-shelf", RI §2.4).
- **Part sizes** (legs, pulls, kick, chair parts, shelf heights, basket depth, wire pitch, caster height) stay GAP-PROC-18, as that row already says. Deli top shelf 0.84 m is noted against RI §2.4's ≈34–36 in (Low).
- `gaps` list: GAP-127, GAP-135, GAP-136, GAP-PROC-18, GAP-PROC-31, GAP-PROC-32, GAP-PROC-33. I checked that GAP-127, 135, 136 and PROC-18 say what the params cite.

## Assets (tris)
| Asset | LOD0 | LOD1 | LOD2 | LOD3 |
|---|---|---|---|---|
| PROC_Cabinet_Tall_Black | 5236 | 1200 | 96 | 12 |
| PROC_FileCabinets_UnderDesk | 6376 | 3052 | 1180 | 24 |
| PROC_Desk_Standing_East | 4828 | 2408 | 144 | 36 |
| PROC_Desk_West_Arm | 4072 | 2040 | 120 | 36 |
| PROC_Desk_Corner_Dual_Monitor | 4072 | 2040 | 120 | 36 |
| PROC_Desk_ExRegister1 | 4072 | 2040 | 120 | 36 |
| PROC_Worktable_Stainless | 3484 | 1948 | 316 | 24 |
| PROC_Chair_Task | 5084 | 2800 | 908 | 36 |
| PROC_Cart_Deli_Prep | 4880 | 2928 | 652 | 72 |
| PROC_Cart_WireBasket | 10576 | 5648 | 2720 | 84 |

- All LOD0 counts are below `tri_guide.lod0_min` 20000, which is a warning only. Under DEC-114 these are furniture pieces that read real at 3.5–10.6k, and I added no filler geometry to reach the guide.
- Determinism: run 1 and run 2 produced the same `export_sha256` for all 10 assets (e.g. Cabinet b8de213faad2333f, Chair 9db99bb93205f250, WireBasket d35d07fe1bab4477).

## New GAP rows (full text, for KNOWN_GAPS)
- GAP-PROC-31 | asset | Office furniture finishes/colours not given by RF/RI:
  - tall-cabinet material (steel powder coat assumed; could be laminate) and file-cabinet finish;
  - file-cabinet pull/lock/label-holder colour;
  - desk frame/leg colour and type for all four desks;
  - Desk_Corner_Dual_Monitor laminate (RF says only "black");
  - Desk_Standing_East top/edge/frame colour and finish (RF gives none);
  - Desk_ExRegister1 laminate finish, edge and frame colour (RF gives only "white top");
  - worktable leg finish (colour Low from wall2_R3C3);
  - chair seat upholstery, plastics finish and gas-lift finish;
  - caster, leveller, grommet and standing-desk controller colours;
  - label colours (deli-cart rail label, file cards).

  Placeholders are mid grey (linear 0.21) | `Tools/Blender/params/office_fixtures.json` `_sources` | REF closer still / Nolan
- GAP-PROC-32 | asset | Office counts and hardware types not stated by RF/RI:
  - file-cabinet unit count (RF "several", 3 used), 2 drawers per unit, pull and lock type;
  - standing-desk column type (3-stage rectangular) and controller;
  - desk frame type (four-leg tube frame + modesty panel), grommet count and position;
  - tall-cabinet front (single inset panel; door count unknown; no hardware per DEC-051 Q9);
  - task-chair construction beyond "black mesh";
  - wire-cart basket count (3) and caster type (plate-mount swivel) on both carts.

  | params `_src` | REF/Nolan
- GAP-PROC-33 | asset | Worktable undershelf: REVIEW-PROC5 asked for an undershelf. RF `Worktable_Stainless` says "stainless top on folding legs", and tile wall2_R3C3 shows an open folding-leg frame with no shelf, so the model has no undershelf | params `Worktable_Stainless._src` | Nolan / closer still

## Checklist line (IMP-003_PROC_FIX_CHECKLIST)
PROC-005 done: office_fixtures. LOD0 is rebuilt as real furniture:
- banded laminate tops with grommets, tube frames and modesty panels;
- a 3-stage standing desk;
- file cabinets with gapped fronts, pulls, locks and slides;
- steel tall cabinets with an inset front and no hardware (DEC-051 Q9);
- a five-star mesh chair;
- a hemmed stainless folding worktable on bullet feet;
- swivel-caster carts with marine-lip trays or welded wire baskets.

Every colour, finish, count and size is cited (RF ids, RI §2.4, wall2_R3C3) or labelled GAP-PROC-18/31/32/33. LOD0 is 3.5–10.6k tris (DEC-114), LODs strictly decrease, the build is deterministic, and the contact sheet is `PROC_office_fixtures_contact_sheet.jpg`.

## Questions for Nolan (through the Hub)
1. **Worktable undershelf.**
   - Source: RF `Worktable_Stainless`; tile wall2_R3C3 (worktable under the floating shelves, centre).
   - What I see: an open frame of light-grey splayed folding legs with no shelf. The review asked for an undershelf.
   - Candidates: (a) folding-leg table with no shelf (modelled); (b) fixed-leg stainless table with an undershelf.
2. **Standing-desk colour.**
   - Source: RF `Desk_Standing_East` (tiles wall2_R3C3, wall1_R3C3, wall1_R3C4); the east wall is at the right edge of R3C3, mostly hidden.
   - What I see: nothing that shows the top colour.
   - Candidates: black, white or wood-look top; black or white frame. Placeholder: mid grey.
3. **Tall cabinet construction.**
   - Source: RF `Cabinet_Tall_Black_A/B`, chat_office_L (not in repo).
   - What I know: black plain boxes (DEC-051 Q9).
   - Candidates: (a) steel storage cabinet with 1 or 2 doors (modelled as a single inset front, no hardware); (b) laminate wardrobe. The door count is unknown.
4. **Desk frames.**
   - Source: RF `Desk_West_Arm` / `Desk_Corner_Dual_Monitor` (wall2_R3C3 left).
   - What I see: the leg colour under the black L desk can't be read.
   - Candidates: black or silver steel legs, or laminate panel ends. Placeholder: grey four-leg frame.

## Infra notes
None. I had to use 8 tube segments at every LOD where a tube sets a bounding extent (6 segments break the exact-size check). This is by design (C11), not a bug.
