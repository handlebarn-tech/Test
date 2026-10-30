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

- [ ] **C1 collision** (`run_generator.py`, every generator's `COL_*`). Unity has no postprocessor, so `COL_` meshes would render as blue boxes. **Decided (DEC-086): option (a), manifest boxes.** No `COL_*` render meshes in the FBX:
  - **(a) recommended:** generators return `collision_boxes` (Unity centre + size) in `extra`; the Unity builder adds `BoxCollider`s; delete the `COL_` meshes and `require_collision`;
  - **(b)** keep `COL_` and add a Unity `AssetPostprocessor` (`*_COL_*` → MeshCollider, renderer removed; non-convex, so not on moving rigidbodies).
  - [R1, S4]
- [ ] **C2 manifest churn** (`run_generator.py`). Add `collision` to the entry only when non-empty, and don't add a `validation` key to existing assets. Check: rerun `deli_jar` and expect a byte-identical manifest entry. [R2]
- [ ] **C3 validation JSON.** It is written only after a pass, so `errors` is always empty. **Decided (DEC-086):** write it **on failure** too, before the `raise`, with the error list; keep it as the PROC gate. [R3]
- [ ] **C4 `mesh_stats()`** (drop 3 / round-2 snapshot change). Take the empty-mesh `raise`. Bounds, material slots and non-manifold/degenerate counts are **accepted as diagnostics (DEC-086)**; **never gate on non-manifold**: touching boxes and the jar's open label quads trip it. Make it one deliberate manifest re-baseline commit. [T2]
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
- [ ] **W7 real values (DEC-088, closes GAP-PROC-13 for these):**
  - **FOH rolling racks** (`Rack_Rolling_1–4`): **3 shelves including the top**; **small wheels**, **4 casters**, 2 per side at the ends.
  - **BOH chrome runs**: **4-ft sections** (`bays`, W5). The **middle sections also roll** (casters); end sections are fixed (feet). This needs per-section `caster_enabled`.
  - Post, wire, collar and caster/foot dimensions stay GAP-PROC-13.
- [ ] **W8 REF follow-up for the PROC worker (do not guess; Hub-confirmed open item):** RF `Rack_East_Wall` is 8.7 ft and `Rack_West_Run` 8.0 ft (2-bay). In 4-ft sections that is 2 sections, which leaves no "middle" section to roll, and 8.7 is not a multiple of 4. Model 2 fixed sections for now and list the run lengths/section counts for the next REF pass (GAP-127).

## 4. Register station: `generators/register_station.py`, `params/register_station.json`
- [ ] **R1 remove `CashDrawer`** (variant + `_cash_drawer`): no cash-handling equipment (DEC-051, RI REF-009 rule). [C1]
- [ ] **R2 scale stand per RI §2.2:**
  - footprint 1.6 × 1.3 ft; top 2.5 ft;
  - **one** wire shelf at 0.5–0.8 ft (not two);
  - black top tray with a raised lip;
  - acrylic panel full width on the **counter-side edge**, 0.8–1.2 ft tall (not a 0.54 m back + side panel);
  - **white** scale body, blue LCD, clear round draft-shield bowl; one scale.
- [ ] **R3** scanner variant: a presentation block is fine for the registers. The BOH `Scanner_Barcode` is a **handheld in a stand** (RF 0.4 × 0.7 × 0.6 ft); add it as a variant.
- [ ] **R4** add keyboard (17.5 in convention, RI §2.2) and receipt-printer props. **Card terminal included** as a realistic unbranded prop (DEC-086, DEC-084).
- [ ] **R5** monitor/stand sizes: GAP-PROC-14.

## 5. Register counter run (round 2): `generators/register_counter_run.py`, `params/register_counter_run.json`
- [ ] **RC1 L layout:** sides from DEC-039 (south 7,2,3,4,5,6; east 12,11; north 10,9,8 = 11 stations), plan bbox 20.0–42.0 × 7.0–19.0 ft (RI §1.5). Generate L segments + a corner. `station_anchors` carry the DEC-039 register numbers.
- [ ] **RC2 counter per TI §6.4:** top ≤ **34 in (0.864)**, top depth **2'-6" (0.762)**, 2 in edge, **4 in base**; white quartz QZ-2 top, walnut veneer WD-1 front, ML-1 black accents; **open black shelves underneath** (R2C3). Currently 0.96 / 0.74, brown, closed.
- [ ] **RC3** station components:
  - remove `cash_drawer`;
  - `scale_stand_slot` on the **floor, staff side, to the staff's right of the monitor** (RI §2.2), not at `y = h`;
  - add keyboard, receipt-printer and **card-terminal** slots (DEC-086).
- [ ] **RC4** countertop display case slot on the run (plan 1.4 × 1.4 ft at x 38–39.4, RI §1.5; "lit black glass", R3C2), using §15.
- [ ] **RC5** per-station width: GAP.

## 6. Deli jar wall + deli counter (round 2): `generators/deli_counter_jar_wall.py`, `params/deli_counter_jar_wall.json`
- [ ] **D1 jar wall runs** per RI §1.5: north 26.0 × 1.2 ft, south (between arches) 21.2 × 1.2 ft, east 1.4 × 14.0 ft. Run width and sections are params; shelves are **dark-grey metal** (DEC-043) on a teal leaf-pattern backlit back (R2C3, photo 11).
- [ ] **D2 shelf heights:** default to the store display family, a 34 in base then 1'-2" shelf pitch (TI §6.4, Med), instead of an even spread. Wall height: GAP.
- [ ] **D3 slot count from data, not a fixed 7 × 4:** one jar per strain, house deli ×2 (DEC-079); ~77 jars (PP). Expose the slot grid as params; the game assigns strains.
- [ ] **D4** keep slot size = `PROC_DeliJar` (6.0 × 10.25 × 5.5 in, REF-007) and bottom-centre anchors (already correct).
- [ ] **D5 deli counter is an L** (bbox 14.0–34.2 × 18.0–25.2 ft, RI §1.5), "DELI STYLE" front = **plywood with a decorative wrap** (DEC-090, Med); the teal/white checker in R2C1/R2C2 is the **wrap print** (a texture on the plywood front, not real tile), with globe pendants at the west end. Replace the clear acrylic front. **No glass case on top is stated**: keep it as an optional placeholder param (GAP-PROC-14). Height/depth: GAP (not in TI, GAP-113).

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
- [ ] **B1** lockers = RF `Lockers_Staff` **one unit 2.0 × 1.5 × 6.0 ft** (DEC-047/051 Q5, High), grey top. Door grid **2 columns × 6 rows = 12 small doors** (DEC-088, Med; narrows GAP-126): `columns: 2`, `rows: 6`, each door ≈ 0.30 × 0.30 m in the 2.0 × 6.0 ft unit. Hinge metadata must be LOD-independent (claimed fix, not delivered).
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
- [ ] **I1** `id_check_stand`: validation fails (height 1.119 ≠ 1.08). Declare `height_m` as the top including the scanner, or exclude the scanner from the expected size. Location: **entrance check-in ID stand** (DEC-086, from canon DEC-036 M2 / RES-001 O2/O3); the counter never re-checks. Size: GAP.
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
  - plywood counter front with the printed teal/white checker wrap as a texture (DEC-090/D5): plywood edge and seam detail, wrap edges and wear, no tile or grout geometry; stainless tong cups;
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

## R3b. Round 3 rebuilt (`Dispo_Game_Blender_PROC_Round3_Rebuild/`): fix items (audit "Drop 6")
Replaces §R3 (drop 5 `…Round3_HQ/` is superseded, DEC-095). Integrate after rounds 1–2 (PROC-005), as **new** families on top of the canonical core (DEC-093). Never copy a drop file over a canonical one. Measured on canonical core 87807ad: 30 assets; with the UV patch only **3/30 pass** (HUB cabinet, stanchion pair, pumpkin).

**Package verdicts:**

| Family | Verdict |
|---|---|
| `queue_stanchions` | adopt (form) |
| `refill_station` | adapt |
| `hub_storage` | adapt |
| `backroom_lighting` | adapt |
| `counter_workstation_props` | adapt |
| `product_variety` | adapt (into `packaged_goods`) |
| `customer_held_props` | adapt (optional) |
| `seasonal_decor` | adapt (optional) |
| `cash_drawer_tray` | **reject** |
| `parked_vehicles` | **reject as built** |
| `round3_common.py` | reject as a module; map onto `proclib` |
| runner UV patch | adapt to the DEC-097 channel order (PROC-007; R3b.0.4) |

**Status of the drop-5 items (§R3, item by item):**
| §R3 item | Status in the rebuild |
|---|---|
| R3.0.1 size validation | **fixed** (now fails on real drift: R3b.0.1) |
| R3.0.2 collision | **fixed** (no `COL_*`); 4 families declare no boxes (R3b.0.5) |
| R3.0.3 params | **open**: no `unity_dir`/`own_sheet`/`checks`; `GAP-R3-*` ids; `quality_floor_lod0` (non-canonical) |
| R3.0.4 DEC-084 detail | **open**: 30/30 below the drop's own floor |
| R3.0.5 one family per object | **partly**: the reuse map exists but names non-existent assets; `product_variety` is still parallel; strips/pendant/wall pack dropped |
| R3.0.6 materials | **open**: `M_R3_*` infix; no textures (binding deferred, acceptable) |
| R3.1 refill station | **regressed**: sourced dims replaced by a GAP; dark 3-tier cart; scale oversize; no placard/bottles/handle/scoop; shelf merged |
| R3.2 HUB storage | **partly**: closed doors + hinge ✓; colour wrong (black, RI §2.1); bags/carton moved to reuse |
| R3.3 stanchions | **kept**; detail still missing |
| R3.4 lighting | **partly**: 2 × 2 ✓; diffuser hidden; strips/pendant/wall pack removed |
| R3.5 interaction states | **regressed**: the cash tray is back; residue dropped (fine); cooler metadata generic ✓ |
| R3.6 customer accessories | **moved** to round 4 (DEC-091) ✓; held props are new |
| R3.7 vehicles | **partly**: inside-out fixed; still rejected on quality |
| R3.8 seasonal | unchanged (optional) |
| R3.9 counter props | **partly**: StickyNotes budget fixed; blue-LCD digits item dropped |
| R3.10 packaged variety | **fixed** brands (fictional; catalog-backed categories); still parallel |
| R3.11 DEC-093 | **open**: `round3_common.py` is a second helper module again |

### R3b.0 Shared
- [ ] **R3b.0.1 size failures (14/30)** [X1]: keep `expected_from_dims(p)`, and make every LOD hit the envelope:
  - keep envelope-defining parts at every `detail`: refill casters, receipt paper, label tail, weigh-boat sides;
  - use cylinder segments that are multiples of 4 (also C11: even ≥ 6);
  - stop parts poking out: wallet seam, cone-tube cap 0.52 w, edible-tin lid 0.51 w, sticky-note offsets;
  - sample the vehicle roof peak at every LOD.
  - Source: canonical runner size check (C5).
- [ ] **R3b.0.2 LOD chains (18/30 non-decreasing)** [X2]: give LOD1 and LOD2 different `detail` levels, or reduce segments on flat parts. Target ½ / ¼ / ≤ 1⁄10 (Q0.5 `check_lod_chain`).
- [ ] **R3b.0.3 DEC-084 detail** [X3]: LOD0 is 56–8,816 tris; every family needs its real construction (per family below) and the Q0 items (unwrapped UVs/trim sheets, 2K–4K PBR via DEC-023, seeded `wear(p)`). Replace `quality_floor_lod0` with `tri_guide.lod0_min` (Q0.5).
- [ ] **R3b.0.4 lightmap UV** [X4, X5]: **settled by DEC-097; implement via PROC-007.** The layout is:
  - channel 0 = `UVMap_Main`;
  - **channel 1 = a dedicated lightmap UV exported from Blender**;
  - **channel 2 = `UVMap_Label`**;
  - Unity "Generate Lightmap UVs" stays **off**.

  Fixes against the drops:
  - **Do not port** `_assign_uvs`/`add_lightmap_uv`'s per-triangle cells: they do not overlap, but every edge is a seam. Build the lightmap UV with a real unwrap + pack per PROC-007.
  - **Channel order:** every round-3–6 drop creates `[Main, Label, Lightmap]`, which puts the label on channel 1 and the lightmap on channel 2: the reverse of DEC-097.
  - The drops' `required_uv_maps` runner patch is only a candidate. The runner check must enforce the DEC-097 order (PROC-007).
- [ ] **R3b.0.5 collision** [X8]: add manifest boxes for `parked_vehicles` (body + wheels), the counter props and product shapes (one box each, or let Unity skip pickups by rule). Source: DEC-086 C1.
- [ ] **R3b.0.6 params** [X9]: `unity_dir: UnityProject/Assets/_Game/Art/Procedural/...` (P1); `own_sheet: true` for multi-variant families (P2); a canonical `checks` block (`fail_on_degenerate`, `material_slots`, `origin_bottom_centre: true`); `GAP-R3-*` → `GAP-PROC-*` (P5); `M_R3_*` → M4 names.
- [ ] **R3b.0.7 helpers** [X10]: do not add `round3_common.py`. Map `finish`→`finish_object`, `box`→`add_box`, `cylinder`/`tube`→`add_vertical_cylinder`/`add_cylinder_between`, `rounded_prism`→`rounded_rect`+`loft` or `add_beveled_box`, `pbr`→`material`. Port `torus` into `proclib` only if a kept family uses it (wheels, wreath, tape). Hinges/slides via `hinge_axis()`/`slide_axis()` (C10). Source: DEC-093, R3.11.
- [ ] **R3b.0.8 reuse map** [X11]: ignore `Data/canonical_reuse_map.json`'s "accepted round 4/5/6" and `PROC_Register_*` targets. Wire reuse only to assets that exist in PROC at integration time; list the rest as dependencies.

### R3b.1 Refill station (`refill_station`; RF `Cart_Deli_Prep`, `Shelf_Deli_Canisters`; RI §2.4; DEC-079)
- [ ] **Split** into `PROC_Office_DeliPrepCart` and `PROC_Office_DeliCanisterShelf` (RF lists them as two fixtures).
- [ ] **Cart dims:** RF 2.5 × 1.6 × 2.9 ft (0.762 × 0.488 × 0.884 m), Med. Remove the hard-coded `top_z = 0.94` and `cart_w = 0.7 w`. Delete `GAP-R3-REFILL-DIMS` (it is sourced).
- [ ] **Cart construction:**
  - **stainless/silver** (DEC-079 "silver rolling cart"), not 0.16 dark;
  - **2 levels**, flat top + lower shelf (RF/RI §2.4), not 3;
  - a tubular push handle;
  - casters touching the legs (they float 6 cm below now);
  - a "FOR DELI USE ONLY" label on the rail (store text, RI §2.4);
  - spray bottles hung on the rail (RF notes).
- [ ] **Shelf:** RF 3.5 × 0.9 ft (1.067 × 0.274 m), **wood** board on **black** brackets, top at ~4.8 ft (1.46 m) AFF, Med. Anchors for ~5 empty canisters (RF); house jars per DEC-079.
- [ ] **Scale:** light grey ✓ and bowl 0.2032 m clear glass ✓ (RI §2.4).
  - Body ≈ 6–7 × 8 × 3 in (≈ 0.17 × 0.20 × 0.08 m), Low; currently 0.285 × 0.265 × 0.105.
  - Add the LCD, coloured keys and a small chrome scoop (RI §2.4).
  - Give the bowl a closed bottom and wall thickness (it is open now).
- [ ] **Supplies** (DEC-079): isopropyl bottle, rags, scraper, bins and tongs as distinct shapes, **under** the cart on the lower shelf. Currently 3 identical bottles.

### R3b.2 HUB storage (`hub_storage`; DEC-079; RI §2.1)
- [ ] **Colour black** (RI §2.1 HUB 2 R2C1 "black cabinets, 2+", Med), not grey steel.
- [ ] **Size:** **2 cabinets, 3.0 × 1.5 × 7.0 ft each** (graybox `FX_HUB2_Cabinets`, a 6.0 × 1.5 ft footprint on the HUB 2 back wall, "tall" 7.0 ft; Low, GAP-110), not one 1.80 × 0.55 × 2.00 m unit.
- [ ] **Evidence text:** placement "HUB against the office wall" (DEC-079) = HUB 2, which shares the office door (RI §1.4). The `evidence` and GAP text must say presence is sourced. Type, size and shelves stay GAP (RG3-1).
- [ ] **Lead ruling (Q6, following the DEC-051 Q9 precedent):** build them as **plain black closed cabinets**:
  - **remove** the interior shelves (`shelf_count`), the `stock_anchors` and the door/hinge `moving_parts`;
  - no openable doors; no lock or hardware detail.

  If Gameplay later needs restocking from these cabinets, Gameplay files it and this item is reopened.
- [ ] **Detail (exterior only):** folded-steel edges, door-panel reveal lines, plinth/levelling feet, and seeded `wear(p)` on the black finish. No interior.

### R3b.3 Queue stanchions (`queue_stanchions`)
- [ ] **Keep:** black ✓ (R2C1), no layout ✓ (RI §1.5 4 lanes, DEC-079 one line).
- [ ] **Detail:** weighted lathe base with a rubber ring, a cassette head with an end clip and receiver slot, belt webbing texture.
- [ ] **Post height 3.0 ft** (0.914 m; graybox `stanchion` class, GAP-002), not 1.05 m. Belt length fits the graybox lanes: 8.71 ft long, 3 ft apart (RI §1.5; RG3-3).

### R3b.4 Back-room lighting (`backroom_lighting`; TI §6.7; RF `Light_Strip_Pendant`)
- [ ] **Diffuser hidden:** the `Recess` box covers the diffuser from below. Put the diffuser (emissive material) at the bottom face, z = 0, with the housing above it.
- [ ] **Removed sourced fixtures:** restore the L2 strips 2 ft/4 ft (TI §6.7 "storage"), the BOH pendant strip (RF 4.0 × 0.5 × 0.3 ft, Low) and the exterior wall pack (CCTV R1C3, generic housing, no camera). Restore them here, or confirm round 6 delivers them; do not lose them.
- [ ] **Detail:** T-bar lay-in flange, louver/lens pattern, rear housing (RG3-7).

### R3b.5 Interaction states (`Data/interaction_states.json`)
- [ ] **Remove** the `PROC_Register_CashDrawer` target (DEC-051/086).
- [ ] **Deli-jar lid:** add a "laid flat" rest pose (RI §2.4); bind pivots on canonical `PROC_DeliJar`.
- [ ] **Cooler/carton:** bind to real group names after K3 / the chosen carton family.

### R3b.6 Cash-drawer tray (`cash_drawer_tray`): **reject**
- [ ] Do not integrate (DEC-051 cash-handling exclusion; DEC-086 rejects the cash-drawer variant). The drop's "quality-only rejection" claim is wrong.

### R3b.7 Parked vehicles (`parked_vehicles`): **reject as built**
- [ ] Source CC0 vehicles through DEC-023 + `LICENSE_LEDGER.md` (preferred). Or rebuild with:
  - real panels, a greenhouse/hood/trunk break and wheel arches;
  - glazing set flush into the body (it sits inside now);
  - wheels inside the arches;
  - LOD0 at 30–150k.

  Keep classes generic (RI R1C1 SUV, R1C2 cars; RG3-4).
- [ ] If any loft is kept: winding is fixed (0 inside-out); add body collision (R3b.0.5).

### R3b.8 Customer held props (`customer_held_props`; optional)
- [ ] GAP item mix. Size failures: wallet seam; bottle/cup radius at LOD2/3 (R3b.0.1). Drop the unused key-ring branch, or add a params row for it. Detail: phone camera island, bottle threads, cup lid tab.

### R3b.9 Counter / workstation props (`counter_workstation_props`)
- [ ] **Keep and detail:** receipt printer, card terminal, keyboard (RI §2.2, DEC-086). Add a paper roll and cutter, terminal keypad legends as a texture, and a full key grid. Sizes via RG3-5.
- [ ] **Label/tape items** (RI §2.2, Low): keep.
- [ ] **DEC-096 register workstation kit:** label/receipt printer, scanner, mouse, keyboard, under-counter storage, spray bottle on a scale shelf, rag. So the mouse and label printer are **sourced** (DEC-096).
- [ ] **Add:** the spray bottle and rag; the scanner is not in this drop.
- [ ] Glove box, weigh boat, pen, sticky notes: generic clutter, GAP.
- [ ] **Blue LCD scale display:** a texture/emissive item on the register scale (RI §2.2) and the refill scale LCD (RI §2.4); the drop-5 item was dropped.

### R3b.10 Product variety (`product_variety`)
- [ ] **Port** the 5 shapes into `packaged_goods` (R3.0.5); no parallel generator.
- [ ] **Brands:** fictional ✓. **Categories** are catalog-backed (DROPPER, BATTERY, ROLLING PAPERS, GUMMY/EDIBLE, PREROLL in `packaged_catalog.json`). Bind each shape to its catalog subcategory, and use a real approved brand only where the catalog row has one (REVIEW-W5T m1).
- [ ] **Sizes:** GAP-PROC-10 (RG3-6). Fix the cap/lid overhang size failures (R3b.0.1).

### R3b.11 Seasonal decor (`seasonal_decor`; optional)
- [ ] No store evidence (GAP). Keep unbranded. Detail: pumpkin ribs as one lathe, wreath needle cards, garland pennant cord. Drop the unused snowflake branch, or add a params row for it.

**Genuine improvements worth porting (DEC-093):**
- the `expected_from_dims` pattern;
- `recalc_face_normals` in finishing;
- `torus`;
- the separate-door-part construction (useful elsewhere; the HUB cabinet itself stays closed per Q6);
- the stanchion form;
- the catalog-matching product shapes;
- the params-driven `required_uv_maps` patch idea, enforcing the DEC-097 channel order (PROC-007).

## R4. Round 4 v2 (`Dispo_Game_Blender_PROC_Round4_HQ_v2_EvidenceDriven/`): fix items (audit "Drop 7")
**Owner split:** ASSET-004 owns the MPFB2 bodies and the rig (DEC-093). PROC integrates the wearables on top, after ASSET-004 delivers a body. Measured on core 87807ad: 36 assets, **13 crash**, 23 build (always-pass size check).

**Package verdicts:**

| Package | Verdict |
|---|---|
| `outfit_variation` (pattern + anti-stereotype rules) | adopt |
| `headwear_library` | adapt |
| `staff_uniform`: BriefGreenTee + BlackPants | adapt |
| `accessory_extensions`: Sunglasses + Tote | adapt |
| `mpfb2_fit_adapter` | adapt |
| `crowd_lod_baker` | adapt |
| PBR textures + decal | adapt |
| `wardrobe_library` | **reject as built** |
| `hair_library` | **reject as built** |
| Watch, Lanyard, PinLanyard, CrossbodyStrap | **reject as built** |
| `mpfb2_glove_overlay` | **reject as built** |
| ObservedBlackTee / ObservedLightBluePolo as staff | **reject** |
| `round4_quality.py` as a module | **reject** |

### R4.0 Shared
- [ ] **R4.0.1 always-pass size check** [X1]: replace every `actual_unity_size(objs)` return (5 generators) with the authored envelope from params (`body_profile` + ease), as R3.0.1 did.
- [ ] **R4.0.2 crashes** [X2]:
  - `round4_quality.ribbon_obj`: build two-sided cards with separate back-face verts, or one-sided cards + a double-sided material (hair/strap). Today 12 assets fail on `face already exists`.
  - `torus_obj`: `bmesh.ops.create_torus` does not exist in 5.2.3. Use the round-3 `torus` loop (R3b.0.7) once in `proclib`.
- [ ] **R4.0.3 determinism** [X6]: `headwear_library._button`'s TopButton differs between runs on 3 caps. Rebuild it with a closed lathe (`add_lathe`) instead of `create_uvsphere` + remove_doubles, then re-check two runs.
- [ ] **R4.0.4 rigging** [X4]: no asset is skinned. Add a Data Transfer of vertex weights from the ASSET-004 MPFB2 body (or use MPFB2's clothes/proxy system) and test deformation in the ASSET-004 rig poses.
- [ ] **R4.0.5 params** [X8]: `unity_dir` → `UnityProject/Assets/_Game/Art/Procedural/Characters/...` (S1); drop `validation_warnings` (P3); `GAP-R4-*` → `GAP-PROC-*`/`GAP-CHR-*` (P5); a `checks` block; lightmap UV per R3b.0.4.
- [ ] **R4.0.6 helpers:** do not add `round4_quality.py`. Map `box_obj`/`cyl_obj`/`lathe_obj`/`rotbox_obj` onto `proclib`; keep one `torus`/`ribbon` in `proclib` (DEC-093).
- [ ] **R4.0.7 textures** [X9]: either register the 30 PNG + decal in `LICENSE_LEDGER.md` with sha256 (DEC-023), or replace them with ambientCG/Poly Haven CC0 fabric scans (preferred; the knit map is sine stripes). Keep 2K, and use the decal at 4K only if the print is legible at close-up.

### R4.1 Wardrobe (`wardrobe_library`): **reject as built**
- [ ] The 11 garments are closed box/cylinder blocks (1–2.6k tris vs 42–80k budgets), with no openings, thickness, seams or folds.
- [ ] **Preferred:** MPFB2/MakeHuman system clothes (CC0, already fitted and rigged to the basemesh; verify licences, RG4-2) for the customer wardrobe. Keep the drop's garment list, colourways and material states (`COLOR_MATERIAL_VARIANTS.json`) as the variation spec.
- [ ] **If procedural:** shell garments with neck/arm/waist openings, 2–4 mm solidify, hems, seams and collars at the DEC-084 close-up bar; fit per R4.0.4.

### R4.2 Hair (`hair_library`): **reject as built**
- [ ] All 9 styles crash (R4.0.2). After the fix they would be single-strip cards around a radial or ponytail path. Use MPFB2/MakeHuman CC0 hair (RG4-2), or rebuild proper card clumps with an alpha-tested material (`hair_basecolor_alpha_2048` exists).
- [ ] Keep the style list (cropped, side part, bob, shoulder wavy, long straight, long curly, curly halo, locs, ponytail): it matches the RI §3 categories without likeness.

### R4.3 Headwear (`headwear_library`): **adapt**
- [ ] Fix TopButton determinism (R4.0.3).
- [ ] Close the crown underside or give it thickness: the open `Crown`/`Brim` is single-sided and vanishes from inside under back-face culling.
- [ ] Fit to the MPFB2 head anchor (`head_anchor_z_m` comes from the 1.75 m profile; GAP until ASSET-004).
- [ ] Patches stay blank or fictional (no team marks) ✓. Forward/backward orientation stays (RI §3 BAND 04/12).

### R4.4 Staff uniform (`staff_uniform`; DEC-089)
- [ ] **Keep only** BriefGreenTee + BlackPants as the staff uniform (DEC-089, also for managers). Rename them `PROC_Chr_Staff_Tee_Green` / `_Pants_Black`, and drop "brief-directed, not footage-confirmed": DEC-089 is the decision.
- [ ] **Remove** ObservedBlackTee and ObservedLightBluePolo from the staff set. Move them to the customer/off-shift wardrobe only if wanted; the polo is teal per RI §3 BAND 01 (RG4-4). Rewrite `STAFF_STYLE_VARIATIONS_12.json`: today 10/12 presets use them.
- [ ] **Decal side:** the code puts it at +X = **wearer's left** while the metadata says "wearer right". **Pending a World REF look at BAND 05/12** (handoff Q8). Placeholder `GAP-CHR-PRINT-SIDE`: wearer's left chest, i.e. the viewer's top-right, the usual left-chest print.
- [ ] **Decal UVs:** give the decal patch a `label_rect` so `UVMap_Label` maps the texture. Crop the decal to the text's aspect (it is 4096² with the text at ~10 % height). Record the font licence, or use an OFL font (RG4-3).
- [ ] **Gloves** (DEC-079: managers refill and clean jars; RI §3 nitrile gloves) are fine as an optional staff accessory once R4.7 is fixed.

### R4.5 Accessories (`accessory_extensions`)
- [ ] Sunglasses and tote: adapt (detail: hinges and temples; tote handles and gusset).
- [ ] Watch, Lanyard, PinLanyard, CrossbodyStrap: fix the crashes (R4.0.2).
- [ ] **Lanyard:** a plain or pin lanyard only, with a **blank** badge card (no access-control or ID detail; DEC-051/DEC-031).
- [ ] **Missing wearables:** glasses (prescription), backpack, beanie and purse were dropped between rounds 3 and 4. Add them here (RI §3 BAND 05/07: glasses; crossbody seen).

### R4.6 MPFB2 fit adapter (`tools/mpfb2_fit_adapter.py`)
- [ ] Shrinkwrap NEAREST_SURFACEPOINT on the whole garment collapses loose fits. Use per-region ease (vertex groups) or MPFB2 proxy fitting, then a weight transfer (R4.0.4). Body object name stays a param (`GAP_REPLACE_…`) until ASSET-004.

### R4.7 Glove overlay (`tools/mpfb2_glove_overlay.py`): **reject as built**
- [ ] It copies the whole "hand object". MPFB2's basemesh is one mesh, so the result is a full-body shell. Mask by a hand vertex group (delete the rest), or use a CC0 glove proxy. Black nitrile material ✓ (RI §3).

### R4.8 Crowd LOD baker (`tools/crowd_lod_baker.py`)
- [ ] Decimate COLLAPSE breaks hair cards and seams. Exclude alpha cards, and preserve UV seams (`use_symmetry` off, `vertex_group` for silhouettes). PROC's own LOD chain may make it redundant: keep it for background crowds only (DEC-087 Rocketbox is the interim crowd).

### R4.9 Outfit arranger (`arrangers/outfit_variation.py` + baked tables)
- [ ] **Adopt** the seeded, hashed pattern and the anti-stereotype rules. Re-bake after R4.1/R4.2/R4.5 so no outfit references a crashing or missing asset (today 17 `PROC_R3_Accessory_*` refs + all hair).
- [ ] The "rougher neighborhood" weighting comes from ChatGPT chat, not our docs. Keep the weights as art direction; DEC-087(4): no behaviour or stats tied to appearance.

## R5. Round 5 (`Dispo_Game_Blender_PROC_Round5_HQ/`): fix items (audit "Drop 8")
Measured on core 87807ad: 18 assets; all build; deterministic; 0 inside-out.

**Package verdicts:**

| Package | Verdict |
|---|---|
| `round5_packaging` | adapt → port into `packaged_goods` |
| `deli_supplies` | adapt |
| `label_art.py` | adapt |
| `stocking_arranger.py` | adapt (GAME-004 owner) |
| textures | adapt |
| UV2 patch | per R3b.0.4 |
| `round5_common.py` as a module | reject (map onto `proclib`) |

### R5.0 Shared
- [ ] **R5.0.1 collision key** [X2]: emit `collision_boxes` (canonical C1), not `collision.boxes`. Today no collider reaches the manifest.
- [ ] **R5.0.2 size** [X1]:
  - return the authored size everywhere: drop `actual_d` in `deli_supplies._bag` and the bottle's `* 1.02`;
  - keep the widest lathe ring at every LOD: can, jars, bottle, tube;
  - fix the exit-bag depth (0.085 measured vs 0.1016 declared).
- [ ] **R5.0.3 LOD chain** [X3]: LOD3 must drop below LOD2 (7/14 equal). Use per-LOD bevel/segment tables, not one `detail` float.
- [ ] **R5.0.4 DEC-084 detail** [X3]:
  - cartons: tuck flaps, glue seam, crease bevels, window/foil areas;
  - pouches: crimped seals, tear notch, zipper bead;
  - jars: threads, CR lid ribs;
  - cart: mouthpiece, window and 510 thread;
  - Tok: screen, button and USB-C.

  Target: props 5–20k at LOD0.
- [ ] **R5.0.5 port** (DEC-093): map each `upgrade_target` onto an existing `packaged_goods` variant and port the shape there. Never ship `PROC_R5_*` next to `PROC_Pkg_*` for the same slot. Params: `unity_dir`/`own_sheet`/`checks`, `GAP-R5-*` → `GAP-PROC-10`/`-*`.

### R5.1 Brand / catalog data (`round5_packaging.json`, `label_templates.json`)
- [ ] **Keep:** High Variety → 510 cart (catalog HIGH VARIETY / VAPE / 510 THREAD) and Tok → 2 g AIO (catalog ToK / VAPE / READY TO USE) ✓.
- [ ] **Add:** a High Variety AIO 2G form (11 catalog READY TO USE rows).
- [ ] **Spell** the brand as the catalog does ("ToK"), unless DEC-071 rules otherwise.
- [ ] **No hard-coded label data** [X6]: strain, potency, weight and form come from a `packaged_catalog.json` row (DATA-002).
  - Potency in **mg** (`thcMg`/`cbdMg`), never an invented %.
  - Remove "LIQUID DIAMONDS", "CURED RESIN", "DUAL MODE" and the fictional edible's "72.6 %".
  - Edibles follow ≤ 10 mg/serving, ≤ 100 mg/package (AZ_COMPLIANCE E1).
- [ ] **AZ label fields** [X7, AZ_COMPLIANCE §D5]: add licence # (placeholder, not real), batch, form, weight, total THC/CBD, the warning, an ingredients line and a non-scannable QR placeholder. Check the universal-symbol requirement (RG5-4).

### R5.2 Label renderer (`tools/label_art.py`)
- [ ] Bundle an OFL font in the repo and record it in `LICENSE_LEDGER.md`. Never resolve `/usr/share/fonts` or `load_default`; the output must be byte-identical across machines.
- [ ] Render at each label rect's aspect (e.g. 0.037 × 0.071 m → 2134 × 4096), not 4096² (round-2 B4).
- [ ] Whitelist check ✓. Add "a real brand only on a catalog category it has" (REVIEW-W5T m1) as a hard check against `packaged_catalog.json`.

### R5.3 Deli supplies (`deli_supplies`)
- [ ] **1 lb backstock bag:** keep the full/partial states, but make "partial" actually lower the fill and slump the top. Size: GAP (RG5-2); the market reference is fine as a placeholder.
- [ ] **Exit bag:** our evidence shows **kraft/paper bags** (RI §3 BAND 05; DEC-043 "branded paper bags"). Add a kraft paper exit bag (TFS-branded print OK, DEC-071). Keep the opaque pouch only if RG5-3 confirms a child-resistant exit bag.
- [ ] **Receipt label:** fine; size from the printer stock (RG3-5).

### R5.4 Stocking arranger (`tools/stocking_arranger.py`, with the GAME-004 owner)
- [ ] **Replace** every synthetic `LIVE_*_REFERENCE` anchor with RF fixture anchors (rolling racks DEC-088 3 shelves; jar walls DEC-079 jars per strain, house deli doubled).
- [ ] **Stock** from DATA-002 rows only (H3).
- [ ] **Density** below "full": DEC-096 playtest feedback says over-full shelving. Expose a fill ratio per fixture.

### R5.5 Textures
- [ ] Register the ~80 PNGs (sha256 + CC0 self-authored) in `LICENSE_LEDGER.md` (DEC-023), or replace them with CC0 scans. Regenerate the label PNGs from data (R5.1).

## R6. Round 6 (`Dispo_Game_Blender_PROC_Round6_HQ/`): fix items (audit "Drop 9")
Measured on core 87807ad: 37 assets build; **0/37 pass the size check**.

**Package verdicts:**

| Package | Verdict |
|---|---|
| evidence-status metadata (`store_evidence_status`, `integration_default`) | adopt |
| `architectural_detail` | adapt |
| `lighting_fixtures` | adapt |
| `exterior_site` | adapt |
| `signage` | adapt (optional) |
| `desert_landscaping` | adapt (presence GAP) |
| textures/decals | adapt |
| `round6_common.py` as a module | reject |

### R6.0 Shared
- [ ] **R6.0.1 axis order** [X1]: return `(w, h, d)`, Unity order (`dimensions_m` is `[w, d, h]`). Today 37/37 fail.
- [ ] **R6.0.2 real dims mismatches** [X1]: build to the declared dims, or fix the dims, for 17 assets:
  - Sprinkler, ExitSign, DoorLever, TrackHead, Downlight, WallPack;
  - CheckoutCluster, Pendant, RecessedCan;
  - AFrame, EntryDoor, ParkingStall, WheelStop;
  - Gravel, Agave, PaloVerde, Shrub.
- [ ] **R6.0.3 determinism** [X2]: replace `bmesh.ops.create_uvsphere` (`round6_common.uv_sphere`) with `add_lathe` spheres. The same fix as R4.0.3.
- [ ] **R6.0.4 winding:** `CornerGuard_90` is inside-out. Fix the face order, or call `recalc_face_normals`.
- [ ] **R6.0.5 LOD chain + DEC-084 detail** [X4]: most assets are 20–700 tris with LOD0 = LOD3.
  - Troffer/ACT: real housing + lens (see R3b.4);
  - storefront: mullions, thresholds, closer arm;
  - plates: screws, receptacle faces;
  - exit sign: housing + letters as a texture;
  - curb and wheel stop: chamfers and wear.
- [ ] **R6.0.6 collision key:** `collision_boxes`, not `collision.boxes` (R5.0.1). Params `unity_dir`/`own_sheet`/`checks`; lightmap UV per R3b.0.4.

### R6.1 Evidence status: switch on what our docs confirm (RI)
- [ ] **Do not use** the drop's finish reading (wood-look plank floors, dark-blue wall, light counters). Our finishes come from RI §6.5: TL-1 marble-look porcelain + TL-2 "Madrid" patterned tile (retail), VCT-1 (back rooms), CONC-1 (storage), VB-1 grey 4 in base, black counters (RI §2.4/DEC-043), teal WC-1 behind displays. See RG6-1.
- [ ] **Set to `store_supported_candidate`:**
  - `Light_Strip_4ft` + a 2 ft variant (TI §6.7 L2, storage; RF `Light_Strip_Pendant` BOH): these also close R3b.4;
  - `Light_WallPack` (CCTV R1C3);
  - outlet/switch plates (RI §6.5 white / matte black; switch 3'-6" AFF, §6.2);
  - door lever (TI A310; centreline 3'-4"–3'-6"; no lock or access-control detail);
  - storefront + entry door (E101);
  - parking stall, stripe and curb (R1C2, R1C3 yellow curb).
- [ ] **Ceiling grid:** **2 × 2** ACT-1 module (RI §6.1, rooms 102–107 at 8'-0"), not 2 × 4. Keep 2 × 4 disabled.
- [ ] **Entry:** E101 is a **6'-0" × 7'-0" pair** (two 0.914 × 2.134 m aluminium full-glass leaves), not a 1.02 m single door (RI §6.2/§6.8, High). Exterior entry door per checklist §13 (no vestibule, DEC-086).
- [ ] **Exterior:** add the dark-green privacy fence/gate (R1C3). Keep landscaping disabled until RG6-3.
- [ ] **Door kit (DEC-110):**
  - add a **push bar / exit device** asset, used only on `EMERGENCY_EXIT`, `EXT_EMERGENCY_HUB` and `EXT_DELIVERY` (graybox openings);
  - **levers** on every other door (TI A310 heights): replace `EntryDoor`'s `PullHandle` with a lever per DEC-110, unless the Hub rules a storefront exception;
  - no lock, reader or access-control detail (DEC-051/031).

### R6.2 Missing families (sourced)
- [ ] **TI §6.7:** L3 recessed linear LED (millwork), L5 small flush mount, L6 bathroom sconce, L7 task light, L8 18 in under-cabinet; L4A/L4B 4½ in downlights (retail gypsum). The drop's downlight is 6 in: add a 4½ in size.
- [ ] **RI §6.1 CLG-1:** suspended 4 × 8 ft dark-walnut acoustic panels on stainless cable with end caps (the retail "baffle" ceiling), plus the gypsum soffit at 7'-6".
- [ ] **Signage** (replace the generic A-frame/menu): "Fine Cannabis" white neon (RI §3 BAND 05); daily-deals sheet (BAND 10); entry licence + pregnancy warning signage (AZ_COMPLIANCE G2); TFS logo panel (`Sign_TFS.png`, DEC-071).

### R6.3 Textures, decals, sign art
- [ ] Register the ~130 PNGs in `LICENSE_LEDGER.md` (sha256, self-authored CC0), or replace the surface materials with CC0 scans of the RI §6.5 finishes (marble-look porcelain, VCT, sealed concrete, walnut). Wear decals (scuff, tape line, wall mark, edge wear): keep, and seed them with `wear(p)` (Q0.4).
