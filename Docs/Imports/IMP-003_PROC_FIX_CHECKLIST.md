# IMP-003 → PROC integration checklist (ChatGPT Blender toolkit, drops 1–4)

**For:** the studio PROC worker who integrates the ChatGPT packages after review and Nolan's approval (DEC-083). The findings are not going back to ChatGPT; this worker fixes every item.
**Evidence for each item:** `Docs/Imports/IMP-003_BLENDER_TOOLKIT_AUDIT.md` (IDs in brackets, e.g. [R1]).
**Sources:**
- RF = `Docs/Reference/ROOM_FIXTURES.json`, sizes `[w, d, h]` ft;
- RI = `Docs/REFERENCES_INDEX.md`;
- TI = RI §6 (2022 TI set, valid for heights, materials and types, DEC-037);
- PP = `Docs/Assets/Specs/PROC_PIPELINE.md`.

**Source files** (read-only, DEC-070; copy into your worktree, never edit in place):
- `C:/Users/handl/Downloads/Dispo Game Imports/blender_proc_vNext/` (drop 1);
- `…/Dispo_Game_Blender_Workstream_Master/packages/*.zip` (drop 2; zip 1 = drop 1);
- `…/Fixture_Toolkit_Full_Package/` (drop 3);
- `…/Dispo_Game_Round2_Workstream/` (drop 4).
- Never open the `__pycache__/*.pyc`.

**Rules for every item:** metres in params; one params file per family; real values from the cited source; anything unsourced stays a named param with a GAP id. Re-run the generator and contact sheet, and commit the manifest diff.

**Done means:**
- every generator passes `blender.ps1` validation;
- two runs are byte-identical;
- existing assets' FBX `export_sha256` are unchanged;
- PP updated (files, budgets, GAP table);
- Unity import is checked.

Round 3 will arrive as more deltas; IMP-003 will append items here.

**Quality bar (DEC-084, overrides DEC-069/074 caps and "generic" wording):** realistic, store-specific LOD0; 2K–4K PBR; LOD0–LOD3 chains. Every family below fails this bar today (§Q), so each family's fix list = its dimension items + its §Q detail items.

## 0. Apply order
1. Core `run_generator.py` + `proclib.py` (§1).
2. Shared params rules (§2).
3. Families in order: wire racks → register station + register L run → jar walls + deli counter → cooler/fridges → office → break room → restroom → janitor → architecture + exterior → ladder → clutter → labels → materials → display cases → ID stand / bags / signs.
4. Arranger (§17; with the GAME-004 owner).
5. Unity import check.

## 1. Core: `Tools/Blender/run_generator.py`, `Tools/Blender/proclib.py`
Start from drop 1's copies; they are ours plus additions only. Do **not** use any `.patch` file: they are whole-file CRLF→LF rewrites, drop 2's is 0 bytes, and drop 3's don't apply to `main`. [R5, T1]

- [ ] **C1 collision** (`run_generator.py`, every generator's `COL_*`). Unity has no postprocessor, so `COL_` meshes would render as blue boxes. Implement the Hub's choice (decision pending):
  - **(a) recommended:** generators return `collision_boxes` (Unity centre + size) in `extra`; the Unity builder adds `BoxCollider`s; delete the `COL_` meshes and `require_collision`;
  - **(b)** keep `COL_` and add a Unity `AssetPostprocessor` (`*_COL_*` → MeshCollider, renderer removed; non-convex, so not on moving rigidbodies).
  - [R1, S4]
- [ ] **C2 manifest churn** (`run_generator.py`). Add `collision` to the entry only when non-empty, and don't add a `validation` key to existing assets. Check: rerun `deli_jar` and expect a byte-identical manifest entry. [R2]
- [ ] **C3 validation JSON.** It is written only after a pass, so `errors` is always empty. Implement the Hub's choice: write it before the `raise` with the error list, or remove it. [R3]
- [ ] **C4 `mesh_stats()`** (drop 3 / round-2 snapshot change). Take the empty-mesh `raise`. Bounds, material slots and non-manifold/degenerate counts only on the Hub's OK, and **never gate on non-manifold**: touching boxes and the jar's open label quads trip it. Make it one deliberate manifest re-baseline commit. [T2]
- [ ] **C5 opt-in checks** (claimed by ChatGPT, not delivered). If wanted, add params-flagged checks in `generate_asset`: `check_origin_bottom_centre` (min Blender z = 0, x/y bbox centred), `fail_on_degenerate`, `check_material_slots`. Default off, with the existing generators' output unchanged. Test them on planted bad meshes: an open quad, a zero-area face, an off-origin object. [A2]
- [ ] **C6 helpers:** add `add_box`, `add_cylinder_between`, `add_vertical_cylinder` (drop 1) and `add_beveled_box` (drop 3 snapshot). Move `from mathutils import …` to the top imports. Fix the missing blank lines at the function seams. Remove the "existing PROC helpers unchanged" comment if C4 lands. [P1, T1]
- [ ] **C7 alpha patch:** apply `Round2/patches/proclib_preserve_rgba_alpha.patch` (`material()` alpha defaults to `rgba[3]`). Verified: no existing caller changes.
- [ ] **C8 drop 3 helpers** (`add_wire_grid`, `add_door_panel`, `add_drawer_box`, `add_cabinet_carcass`, `add_handle_pull`, …): add **only** the ones the families use after their refactor (§3–§10 use them). Leave the rest out until needed. [T3]
- [ ] **C9 `add_wire_grid`:** separate `spacing_x` / `spacing_y`. [T4, G1]
- [ ] **C10 hinge/slide metadata helper:** `hinge_axis(x, y0, y1, z_front, side)` / `slide_axis(...)` returning the manifest dict, used by every door/drawer family instead of per-family dicts. [T4]
- [ ] **C11 cylinder extents:** a cylinder that defines an asset's bounds needs an even segment count ≥ 6, because the ring roll is arbitrary on Y-axis cylinders (caster wheel x extent is 0.0951 for 0.1). [B1]
- [ ] **C12 contact sheets:** every new family uses its own sheet (`own_sheet: true`, `contact_sheet <generator>`), or the default sheet breaks its 1 MB cap. [S2]

## 2. Every params file (all families)
- [ ] **P1** `unity_dir` must start with `UnityProject/` (`UnityProject/Assets/_Game/Art/Procedural/...`). [A1, S1]
- [ ] **P2** `own_sheet: true`. [A2, S2]
- [ ] **P3** delete `validation_warnings` (free text); keep the GAP ids in `gaps`. [A3, S8]
- [ ] **P4** `tri_budget` per DEC-084 (replaces the DEC-069 caps and audit S3). Budgets are LOD0 **guides**, not caps:
  - props 5–20k, fixtures/furniture 20–80k, hero items 30–150k;
  - each LOD1–LOD3 ≈ ½, ¼, ≤ 1/10 of LOD0.
  Validation fails only above the guide's upper bound and **warns** below the lower bound (too simple). See §Q.
- [ ] **P5** GAP ids:
  - register `GAP-PROC-13` (wire racks) and `GAP-PROC-14..22` (one per family) **only** for values with no RF/RI/TI source;
  - fold round 2's `GAP-R2-*` into `GAP-PROC-*`;
  - add each to the PP GAP table + KNOWN_GAPS pointer. [S9]
- [ ] **P6** per-variant `require_collision` (or drop it with C1a). [B4]

## 3. Wire shelving: `generators/wire_shelving.py`, `params/wire_shelving.json` (+ janitor supply rack)
- [ ] **W1** `_feet()` crashes on a zero-length bracket when `foot_radius_m == collar_outer_diameter_m/2`: skip the bracket if its length is < 1e-6. [B3]
- [ ] **W2** wire pattern: dense front-to-back wires + a few long wires (C9), not a square grid. Check against tiles `wall2_R4C1`, `BOH_still`. [G1]
- [ ] **W3** floating wires: extend the grid to the rail line and set the rails at the grid plane (or add a truss). [G2]
- [ ] **W4** replace the even spacing with a `shelf_z_m` list param (even is the default). [G3]
- [ ] **W5** `bays` param with shared inner posts (2-bay West run). [G4]
- [ ] **W6** one params entry per RF rack (convert ft → m in params):

  | RF row | w × d × h (ft) | notes |
  |---|---|---|
  | `Rack_Rolling_1–4` | 6.0 × 2.0 × 6.0 | casters, chrome (Low, GAP-127) |
  | `Rack_East_Wall` | 8.7 × 2.0 × 6.0 | Med |
  | `Rack_West_Run` | 8.0 × 2.0 × 6.0 | 2-bay, 4–5 shelves |
  | `Rack_South_Wall` | 5.3 × 1.8 × 6.0 | |
  | `Rack_Chrome_Cartons` | 2.5 × 1.2 × 6.0 | |
  | `Rack_Bags_Tools` | 3.0 × 1.5 × 5.0 | |
  | `Desk_WireRack_Computer` | 3.4 × 1.5 × 6.0 | **black**, keyboard shelf at desk height |
  | `Rack_CleaningSupplies_JC` | 2.0 × 1.2 × 5.0 | janitor supply rack |

  [dimension table drop 1; janitor §7]
- [ ] **W7** shelf count, post/wire/collar/caster/foot sizes: GAP-PROC-13 until Nolan answers (handoff Q1/Q2).

## 4. Register station: `generators/register_station.py`, `params/register_station.json`
- [ ] **R1 remove `CashDrawer`** (variant + `_cash_drawer`): no cash-handling equipment (DEC-051, RI REF-009 rule). [C1]
- [ ] **R2 scale stand per RI §2.2:**
  - footprint 1.6 × 1.3 ft; top 2.5 ft;
  - **one** wire shelf at 0.5–0.8 ft (not two);
  - black top tray with a raised lip;
  - acrylic panel full width on the **counter-side edge**, 0.8–1.2 ft tall (not a 0.54 m back + side panel);
  - **white** scale body, blue LCD, clear round draft-shield bowl; one scale.
- [ ] **R3** scanner variant: a presentation block is fine for the registers. The BOH `Scanner_Barcode` is a **handheld in a stand** (RF 0.4 × 0.7 × 0.6 ft); add it as a variant.
- [ ] **R4** add keyboard (17.5 in convention, RI §2.2) and receipt-printer props. Card terminal: only if the Hub rules it a generic prop.
- [ ] **R5** monitor/stand sizes: GAP-PROC-14.

## 5. Register counter run (round 2): `generators/register_counter_run.py`, `params/register_counter_run.json`
- [ ] **RC1 L layout:** sides from DEC-039 (south 7,2,3,4,5,6; east 12,11; north 10,9,8 = 11 stations), plan bbox 20.0–42.0 × 7.0–19.0 ft (RI §1.5). Generate L segments + a corner. `station_anchors` carry the DEC-039 register numbers.
- [ ] **RC2 counter per TI §6.4:** top ≤ **34 in (0.864)**, top depth **2'-6" (0.762)**, 2 in edge, **4 in base**; white quartz QZ-2 top, walnut veneer WD-1 front, ML-1 black accents; **open black shelves underneath** (R2C3). Currently 0.96 / 0.74, brown, closed.
- [ ] **RC3** station components:
  - remove `cash_drawer`;
  - `scale_stand_slot` on the **floor, staff side, to the staff's right of the monitor** (RI §2.2), not at `y = h`;
  - add keyboard/printer slots (card terminal per the Hub ruling).
- [ ] **RC4** countertop display case slot on the run (plan 1.4 × 1.4 ft at x 38–39.4, RI §1.5; "lit black glass", R3C2), using §15.
- [ ] **RC5** per-station width: GAP.

## 6. Deli jar wall + deli counter (round 2): `generators/deli_counter_jar_wall.py`, `params/deli_counter_jar_wall.json`
- [ ] **D1 jar wall runs** per RI §1.5: north 26.0 × 1.2 ft, south (between arches) 21.2 × 1.2 ft, east 1.4 × 14.0 ft. Run width and sections are params; shelves are **dark-grey metal** (DEC-043) on a teal leaf-pattern backlit back (R2C3, photo 11).
- [ ] **D2 shelf heights:** default to the store display family, a 34 in base then 1'-2" shelf pitch (TI §6.4, Med), instead of an even spread. Wall height: GAP.
- [ ] **D3 slot count from data, not a fixed 7 × 4:** one jar per strain, house deli ×2 (DEC-079); ~77 jars (PP). Expose the slot grid as params; the game assigns strains.
- [ ] **D4** keep slot size = `PROC_DeliJar` (6.0 × 10.25 × 5.5 in, REF-007) and bottom-centre anchors (already correct).
- [ ] **D5 deli counter is an L** (bbox 14.0–34.2 × 18.0–25.2 ft, RI §1.5), "DELI STYLE" **teal/white checker tile front** (R2C1/R2C2; confirm with handoff Q5), with globe pendants at the west end. Replace the clear acrylic front. Height/depth: GAP (not in TI, GAP-113).

## 7. Glass-door cooler + fridges: `generators/glass_door_cooler.py`, `params/glass_door_cooler.json`
- [ ] **K1** 2-door = RF `Cooler_GlassDoor_2Door` **4.0 × 2.5 × 6.5 ft**, black frame, lit. Drop or keep SingleDoor as a demo only.
- [ ] **K2** handles float 46 mm off the door: use `add_handle_pull` (C8) from the door face. [cooler]
- [ ] **K3** moving parts: group `DoorFrame_nn` + `Glass_nn` + `Handle_nn` per door (or merge them into one door object); `hinge_side` per door via C10. [S6]
- [ ] **K4** add a top-freezer fridge variant: RF `Fridge_TopFreezer` 2.2 × 2.3 × 5.5 ft, white (FOH); `Fridge_Magnets` 2.8 × 2.4 × 5.8 ft (break room, magnet-covered side).
- [ ] **K5** shelf anchors exist; contents per DEC-050 (cooler: concentrates + perishable edibles; fridge: drinks).

## 8. Office: `generators/office_fixtures.py`, `params/office_fixtures.json`
- [ ] **O1 handles z-fight** (inside door/drawer fronts, coplanar) on TallStorageCabinet and FilingCabinet: use `add_handle_pull` / proud handles. [S5]
- [ ] **O2** TallStorageCabinet = RF `Cabinet_Tall_Black_A/B` **2.4 × 2.0 × 5.0 ft, black, plain closed box, no hardware** (DEC-051 Q9): add `doors: false`.
- [ ] **O3** FilingCabinet = RF `FileCabinets_UnderDesk`: several **black** cabinets under the standing desk, run 3.4 × 1.8 × **2.4 ft**, so each is ≤ 0.73 m tall with ~2 drawers.
- [ ] **O4** StandingDesk = RF `Desk_Standing_East` 3.6 × 2.0 × 3.5 ft.
- [ ] **O5** Desk:
  - add an L/corner variant: `Desk_West_Arm` 4.8 × 2.5 × 2.5 + `Desk_Corner_Dual_Monitor` 4.3 × 2.5 × 2.5, **black laminate**;
  - BOH `Desk_ExRegister1` 4.0 × 2.0 × 2.5, **white top**.
- [ ] **O6** Worktable = RF `Worktable_Stainless` 5.3 × 2.5 × 2.5 ft, stainless top, folding legs.
- [ ] **O7** OfficeChair = RF `Chair_Task_1/2` 2.0 × 2.0 × 3.2 ft, black mesh, 5-star base.
- [ ] **O8** remove DrawerCart (no store evidence). Add the **deli prep cart** instead: RF `Cart_Deli_Prep` 2.5 × 1.6 × 2.9 ft, stainless 2-shelf utility cart; the only certified refill spot (DEC-079). Also `Cart_WireBasket` 1.5 × 1.5 × 2.5, black wire.

## 9. Break room: `generators/break_room.py`, `params/break_room.json`
- [ ] **B1** lockers = RF `Lockers_Staff` **one unit 2.0 × 1.5 × 6.0 ft** (DEC-047/051 Q5, High), grey top. Door grid: GAP-126 until Nolan answers (handoff Q3). Hinge metadata must be LOD-independent (claimed fix, not delivered).
- [ ] **B2** bench = RF `Bench_Wood` 5.0 × 1.3 × 1.5 ft, wood plank on **black steel legs**.
- [ ] **B3** board variants: `Board_Bulletin_West` 3.0 × 2.5 ft; `Board_Cork` (hall, wood frame) 1.8 × 2.6; `Whiteboard_West` 4.0 × 3.0 (red/white frame); office `Board_West_BlackFrame` 2.5 × 2.0; `Board_North_Fabric` 5.0 × 3.0 (grey fabric).
- [ ] **B4** LunchTable and FirstAidBox: sizes already match RF; keep them.
- [ ] **B5 missing:**
  - base cabinets + black counter (34 in, TI) `Counter_North_Run` 4.4 × 2.0 and `Counter_East_Return` 5.9 × 2.0;
  - uppers 4.4 × 1.1 × 2.5;
  - double sink 2.7 × 1.6;
  - microwave, coffee maker;
  - mini hoop, coat hooks (RF BreakRoom rows).

## 10. Restroom: `generators/restroom.py`, `params/restroom.json`
- [ ] **T1 sink:**
  - **wall-hung**, no pedestal (27 in knee clearance, TI §6.4/6.6);
  - RF `Lavatory_WallHung` 1.7 × 1.5 ft, rim 34 in;
  - **fix the bowl**: the lofted bowl is a capped solid whose top is coplanar with `BasinTop`, so it shows no basin and z-fights. Make an open recessed loft with no top cap.
- [ ] **T2** mirror = TI **1'-8" × 3'-6"**, bottom 3'-4" AFF (High).
- [ ] **T3** toilet = RF 1.6 × 2.4 × 2.5 ft.
- [ ] **T4** paper-towel dispenser: **silver/stainless**, old manual (DEC-062); RF `Accessories` 1.1 × 0.4 × 1.5.
- [ ] **T5** tool chest = RF `ToolChest_Black` 2.2 × 1.5 × **2.75 ft**, kept below the 33 in grab bar; handles fixed as O1.
- [ ] **T6** large storage cabinet: its own params variant of the office cabinet kind, RF `Cabinet_Storage_Large` 4.0 × 1.5 × 7.0 ft (GAP-109).
- [ ] **T7** add grab bars: 42 in, 36 in and 18 in vertical at 33–36 in AFF (TI, High). Add TP + soap dispensers and the sconce (TI types).

## 11. Janitor closet: `generators/janitor_props.py`, `params/janitor_props.json`, `params/janitor_supply_rack.json`
- [ ] **J1** mop sink = RF `MopSink_JC` **1.6 × 1.5 × 1.0 ft**.
- [ ] **J2** supply rack = RF `Rack_CleaningSupplies_JC` 2.0 × 1.2 × 5.0 ft (fails until W1).
- [ ] **J3** collision on mop/broom/bucket (claimed fix, not delivered): add per C1, or set `require_collision: false` for those variants.

## 12. Architecture kit: `generators/architecture_kit.py`, `params/architecture_kit.json`
- [ ] **A1 door size:** `width_m`/`height_m` are the **leaf**, **3'-0" × 7'-0" × 1¾"** (TI §6.2); add the frame outside. The current leaf comes out 0.816 × 2.08. JC door 2'-8".
- [ ] **A2 door finishes per RF:** black HM (hall-office, break, JC, vestibule doors), white (office→HUB 2). The SE exit door is green with a round logo (DEC-030): leave the logo blank.
- [ ] **A3 arch** = gypsum cased opening **3'-0" × 7'-0"** (TI §6.2, RI §6.4), gypsum/slat finish, not 1.52 × 2.44 metal trim.
- [ ] **A4** baseboard height 4 in (0.1016), grey vinyl VB-1 (TI §6.5).
- [ ] **A5** strip light lengths 2 ft / 4 ft (0.6096 / 1.2192), L2 (TI §6.7). Ceiling tile + troffer 2 × 2: keep (TI).
- [ ] **A6** AccessPanel params variant for the hall `Panel_Blank` 1.0 × 1.5 ft (DEC-062).
- [ ] **A7** SoffitTrim and CornerGuard: no source; drop unless ART asks.

## 13. Exterior (round 2): `generators/building_shell_exterior.py`, `params/building_shell_exterior.json`
- [ ] **E1 remove `EntryVestibule`:** no exterior vestibule exists in any source (the A011 vestibule is the interior FOH/BOH lobby). Add a **storefront door pair** module: **6'-0" × 7'-0", two 3'-0" leaves, out-swinging aluminium** (TI E101, RI §1.4, High).
- [ ] **E2** storefront glass = **GL-1 green-tinted** (TI §6.5). Glazing collision must cover the glass (currently only sill and header).
- [ ] **E3** exterior look per night CCTV (R1C1–R1C5, R3C1): light flat-roof walls, wood fascia, hedge, sidewalk, yellow curb, white/yellow striping, dark green fence/gate. Sizes: GAP.

## 14. Fixed ladder: `generators/fixed_ladder.py`, `params/fixed_ladder.json`
- [ ] **L1** LOD1 fails bounds (5 segments): use even `tube_segments` ≥ 6 (C11). (Claimed fix, not delivered.)
- [ ] **L2** size = RF `Ladder_FireEscape` 1.5 × 0.6 × 9.0 ft, black. REF note: the TI ceiling here is 8'-0"; flagged to the Hub.

## 15. Display cases (round 2): `generators/display_cases.py`, `params/display_cases.json`
- [ ] **V1** add top glass (counter case); back optional.
- [ ] **V2** collision must enclose the glass.
- [ ] **V3** countertop case footprint = 1.4 × 1.4 ft (RI §1.5), lit black glass (R3C2). Height: GAP. TallCase: GAP / optional.

## 16. Clutter kit: `generators/clutter_kit.py`, `params/clutter_kit.json`
- [ ] **X1 box fan:** blades rotate in the XZ plane inside the frame (they poke out now; LOD0 fails). Store fan = RF `Fan_Portable` **white, 1.0 × 0.8 × 1.0 ft**. (Claimed fix, not delivered.)
- [ ] **X2** open carton: keep the flaps on every LOD (no silhouette pop). (Claimed fix, not delivered.)
- [ ] **X3** paper stack: no collision, so set per-variant `require_collision: false` (P6). (Claimed fix, not delivered.)
- [ ] **X4** trash: RF `Trash_Aluminium` 1.5 × 1.5 × 2.5 ft with a round rim; add `Trash_StepCan` stainless 1.0 × 1.0 × 2.0.
- [ ] **X5** tote **yellow** (RF `Props_Floor`, R4C1); bins: **clear** sorted bins + **black** trays (RF `Rack_Rolling_*`).

## 17. Arrangement helpers: `arrangers/placement.py` (with the GAME-004 owner)
- [ ] **H1** placement `y` = shelf top / layer bottom (bottom-centre origin, PP), not `+ h/2`.
- [ ] **H2** shelf anchors use the inner usable area (inside rails/posts) in `wire_shelving` and `register_station`.
- [ ] **H3** decor only: real stock comes from inventory data (DATA-002 / GAME-004). `category_mix` per fixture from DEC-050.
- [ ] **H4** write a real test (determinism + no overlap); `TEST_RESULT.json` ships without test code.

## 18. Labels / decals (round 2): `generators/label_decals.py`, both label params
- [ ] **N1** add **"The Flower Mine"** (DEC-081) to `APPROVED_BRANDS`. Move the whitelist into one shared data file that BRAND-001 also reads.
- [ ] **N2** drop the jar `Band`/`JarCard`/`THCTag` meshes: `PROC_DeliJar` already has those parts with `UVMap_Label` (PP). Keep package-front/price-tag only where no target part exists.
- [ ] **N3** output **PNG textures** at the label's aspect ratio (not 512² SVG), rasterised with an OFL font (not Arial). Card 100 × 80 mm, tag 45 × 28 mm, band 150 × 55 mm (GAP-PROC-03/09).
- [ ] **N4** text from data at runtime (strain, THC %); never invented product data.

## 19. Materials (round 2): `materials/cc0_pbr.py`, `generators/material_library.py`, `params/material_library.json`
- [ ] **M1 no network at build:**
  - remove `_request_json`/`_download` from the build path;
  - add the 7 provider assets to the DEC-023 fetch list (`Tools/Assets/fetch_assets.py`: Poly Haven + url sources) with sha256 + `LICENSE_LEDGER.md` IDs;
  - `build_material` reads only manifest-verified cache files and fails if one is missing.
- [ ] **M2** reuse cached assets: `PH-smooth_concrete_floor` already exists. Prefer the cached `oak_veneer_05` over `oak_veneer_01` unless ART wants the new one.
- [ ] **M3** floors per TI §6.5: sales floor **TL-1 marble-look 12 × 24** + **TL-2 8 × 8 patterned**; CONC-1 concrete only in storage. Retarget/rename `M_Proc_Floor_PolishedConcrete`. ART-003's generated TL-1/TL-2/QZ-2 maps already exist (`lookdev_textures.py`).
- [ ] **M4** keep the `M_Proc_*` names as the Unity naming contract. Real HDRP materials are built in Unity, since the FBX carries names only.

## 20. ID-check stand, bag racks, sign blanks (round 2; low priority)
- [ ] **I1** `id_check_stand`: validation fails (height 1.119 ≠ 1.08). Declare `height_m` as the top including the scanner, or exclude the scanner from the expected size. Location/size: GAP (handoff Q4).
- [ ] **I2** `bag_racks` ToolCaddy fails (handle tube radius above `h + handle_h`): add `handle_radius` to the expected height. The wall bag rack / exit dispenser have no store evidence; keep them optional. The real fixture is RF `Rack_Bags_Tools` (§3).
- [ ] **I3** `sign_blanks` AFrame fails (legs splay past depth and height): clamp the leg endpoints inside `d/2` and `h`. The store uses a 3 × 3 video wall + menu screen 6.6 × 1.0 ft (RI §1.5); screen content is out of scope.

## Q. Quality bar (DEC-084): every family is below it
Measured LOD0 tris (IMP-003 sandbox runs) vs the DEC-084 LOD0 guides:

| Family | LOD0 now | Guide | Gap |
|---|---|---|---|
| wire shelving | ~3,000 | fixture 20–80k | 7–25× |
| cooler 2-door | ~3,000 | hero 30–150k (lit merchandiser, customer-facing via budtender) | 10×+ |
| register scale stand | ~1,200 | fixture 20–80k | 15×+ |
| register counter run (11 stations) | 248 | hero 30–150k per segment | 100×+ |
| deli counter / jar wall | 152 / 84 | hero 30–150k | 200×+ |
| office pieces | 160–830 | furniture 20–80k | 25–100× |
| lockers | ~1,950 | fixture 20–80k | 10×+ |
| restroom pieces | 100–460 | fixture 20–80k | 50×+ |
| janitor props, clutter, labels | 60–470 | props 5–20k | 10–100× |
| architecture kit, exterior | 12–550 | fixture 20–80k (doors), modules per ART | large |
| display cases | 230–260 | fixture/hero 20–150k | 100×+ |

### Q0. Pipeline items (all families)
- [ ] **Q0.1 LOD0–LOD3** in every params `lods`:
  - LOD0 full detail;
  - LOD1 drops micro-detail (screws, wire ends, chamfers below ~3 mm);
  - LOD2 merges parts;
  - LOD3 one silhouette block per part group (as `packaged_goods` LOD2 "far").
  - Unity's LODGroup is built from the `_LOD<n>` suffix (PP), so no extra wiring is needed.
- [ ] **Q0.2 UVs:** replace the 1 UV = 1 m box projection (`UVMap_Main`) on hero/fixture parts with proper unwraps or a **trim-sheet** layout at a stated texel density. ART sets the target (GAP until set). Keep `UVMap_Label` for label regions.
- [ ] **Q0.3 PBR textures:** 2K for props, 4K for hero fixtures/jars/counters (DEC-084). They come from the DEC-023 cache (§19 M1), upgraded from the round-2 `1k` to 2K/4K, or are baked from the procedural detail (normal/AO/curvature) in the pipeline. Record each texture's source in `LICENSE_LEDGER.md`.
- [ ] **Q0.4 wear:**
  - seeded per-instance variation params: edge wear, scuffs, fingerprints on glass and acrylic, sticker residue, floor-tape wear;
  - deterministic from `seed`, which most families record but never use.
- [ ] **Q0.5 validation:**
  - per-family LOD0 guide range in params;
  - fail above the upper bound; warn below the lower bound;
  - check that every LOD1–3 exists and decreases.
- [ ] **Q0.6 frame budget:** check each room against PERF-001 (≤ 3 M tris on screen, ≤ 2000 draw calls, GPU ≤ 12 ms on the 6 GB card). Use GPU instancing and shared materials for repeated racks, jars and ceiling tiles.

### Q1. Per-family detail to add at LOD0 (store-specific; sources as in §3–§20)
- [ ] **Wire racks:**
  - round wires (not 3 mm square boxes) with welded joints;
  - truss edge and split-sleeve collars on grooved posts (1 in pitch grooves);
  - leveller feet with threads; swivel casters with brake, fork and bearing;
  - BOH/FOH contents bins (clear) and trays (black) as separate props.
- [ ] **Register station:**
  - **Scale stand:** tube frame with welded corners; black tray with formed lip; wire shelf of round wire; white scale with LCD, keypad and round draft-shield bowl with lid; acrylic panel with polished edges and stand-offs.
  - **Monitor:** bezel, rear vents, VESA stand.
  - **Scanner:** cable, trigger, window.
- [ ] **Register counter:**
  - QZ-2 quartz top with 2 in eased edge and waterfall end (TI §6.4);
  - walnut-veneer front panels with reveals; ML-1 black accents; HW-2 brass edge pulls;
  - open black under-shelves with supports; toe kick;
  - cable grommets at each station.
- [ ] **Jar wall / deli counter:**
  - arched wood frames; dark-grey metal shelves with front lip;
  - teal leaf-pattern backlit panel (emissive + pattern texture) and LED strips;
  - checker-tile counter front (TL-type tile, real grout lines); stainless tong cups;
  - jars are `PROC_DeliJar` (hero, see PP; its budget is reviewed under DEC-084 by PROC separately).
- [ ] **Cooler/fridge:**
  - door gaskets, hinges and closers; real pull handles;
  - interior LED strips (emissive); wire shelves with clips and price-tag rails; louvred base grille; label plate (blank);
  - fridge door seals, handles, freezer split, hinge caps, magnets layer for `Fridge_Magnets`.
- [ ] **Office:**
  - edge banding and laminate seams; desk grommets and leg levellers; L-desk corner joinery;
  - mesh chair: mesh back texture, gas lift, 5-star base with twin-wheel casters, armrests;
  - filing cabinets: drawer pulls, label holders, lock cylinder (generic), lap-joint carcass;
  - stainless worktable: folding leg mechanism; deli prep cart: stainless shelves with rolled edges, swivel casters.
- [ ] **Lockers:** louvre vents (real slots, not 4 strips), latch handles, number plates (blank), hinge knuckles, sloped/flat top per tile R3C5, base.
- [ ] **Restroom:**
  - wall-hung lavatory: real basin cavity, overflow, faucet, drain, brackets;
  - toilet: proper bowl/trap sculpt, seat + lid with hinges, flush lever;
  - framed mirror; stainless grab bars with flanges; silver manual towel dispenser with lever + window;
  - tool chest: hinges and pulls.
- [ ] **Janitor:** mop sink with drain grate and splash guard; string mop head (alpha cards or strands); broom bristles; bucket with handle and wringer (hollow); rack contents (cleaning bottles, rags) per DEC-079 list.
- [ ] **Architecture:**
  - HM door with frame stop, hinges (3), lever handle at 3'-4"–3'-6" (TI §6.2), kick plate (break/restroom), closer arm;
  - storefront pair with aluminium stiles, push/pull hardware, threshold;
  - ACT tile with fissured texture and grid tees; troffer with louvre/lens detail;
  - arch with gypsum corner bead and slat-wall returns.
- [ ] **Exterior:**
  - storefront mullions with caps and GL-1 tint; parapet coping; curb with chamfer and paint wear; asphalt striping texture;
  - wall packs (blank housings only; no camera hardware);
  - fence/gate per R1C3.
- [ ] **Display cases:** glass with polished edges, black frame with corner joints, LED strips, glass shelves on clips, lock-free sliding back doors.
- [ ] **Clutter:**
  - corrugated cartons with flap creases, tape, a generic shipping-label texture (blank, no carrier marks);
  - yellow tote with ribbed walls and handles;
  - aluminium trash can with rolled rim;
  - portable fan with grille and blades;
  - paper stack with sheet edges.
- [ ] **Labels:**
  - "unbranded ≠ plain" (DEC-084): labels must look like real retail labels (layout, typography hierarchy, barcode/QR-style placeholder, compliance-panel look) using **approved brands only** (DEC-071/081) or fictional BRAND-001 names;
  - no unapproved marks; text from data.
- [ ] **Materials:** 2K/4K sets (Q0.3). Floors TL-1/TL-2 at real tile sizes (12 × 24 in, 8 × 8 in) with grout; QZ-2 quartz, WD-1 walnut, ML-1 black-patina laminate (TI §6.5).

Not in IMP-003 scope, flagged for PROC: the **existing** jar, fill and packaged-goods budgets in PP (jar 1000, packaged 120–600 tris) predate DEC-084. Re-baselining them is a PROC task, not a toolkit fix.
