# IMP-003 — ChatGPT Blender toolkit audit (rolling)

Scope: DEC-069 brief. Source folder: `C:/Users/handl/Downloads/Dispo Game Imports/` (untouched, DEC-070). Our pipeline: `Tools/Blender/` at main 33e57a1, `Docs/Assets/Specs/PROC_PIPELINE.md`.
Verdicts: **adopt** = take as is; **adapt** = take after the listed fixes; **reject** = do not take.

---

## Drop 1 — `blender_proc_vNext/` (files dated 2026-10-30 03:11)

### Contents
| File | What | Verdict |
|---|---|---|
| `proclib.py` | our `proclib.py` + 3 helpers (`add_box`, `add_cylinder_between`, `add_vertical_cylinder`) | **adopt** (fix P1) |
| `run_generator.py` | our runner + opt-in `COL_` collision parts + per-asset `Validation/<asset>.json` | **adapt** (R1–R4) |
| `patches/*.patch` | same changes as the two copies | **reject** as an apply route (R5); the copies are the deliverable |
| `generators/wire_shelving.py` | chrome wire rack family: `Stationary` (feet) + `Rolling` (casters), LOD0/LOD1, shelf anchors, `COL_Rack` | **adapt** (G1–G6) |
| `params/wire_shelving.json` | 48 × 18 × 72 in, 5 shelves, all tagged `GAP-PROC-13` | **adapt** (A1–A3 + dimension table) |
| `README.md`, `docs/PIPELINE_AUDIT_AND_WIRE_SHELVING.md` | notes; honest that nothing was run in Blender | reference only |
| `__pycache__/*.pyc` (3) | compiled bytecode | **reject**: never imported or copied |

### How it was checked
- Static read of every line of the generator, params and both diffs. `diff --strip-trailing-cr` against ours: the two copies are **our current files plus additions only**. Nothing of ours was removed or changed.
- Patches: both are whole-file `@@ -1,N +1,M` hunks (our working copy is CRLF, theirs LF). `patch --binary` on our files reproduces the copies byte for byte.
- Behaviour check, sandboxed: I copied only the `.py`/`.json` files to `_imp003_sandbox/` in this worktree, so `ROOT` resolved to the sandbox, and ran our `blender.ps1` with Blender 5.2.3, `--factory-startup` and `PYTHONDONTWRITEBYTECODE=1`. The sandbox was deleted afterwards. Nothing ran on the host tree or the Imports folder.

| Check | Result |
|---|---|
| Headless 5.2.3 run, validation | **pass** both variants (size, UV maps, identity transforms, budgets) |
| Tris (Stationary / Rolling) | LOD0 3012 / 3044 (budget 5000), LOD1 1424 / 1456 (budget 1800); `COL_Rack` 108, not counted. Matches my hand count. DEC-069 ≤~5k fixture: **pass** |
| Size (Unity xyz) | 1.2192 × 1.8288 × 0.4572 on both LODs = params |
| Determinism | 2 runs: identical FBX and validation JSON sha256. `seed` is recorded but unused (no randomness): honest, no issue |
| Existing generators through the patched runner | `deli_jar` FBX `export_sha256` and every `geometry_sha256` **unchanged** vs committed manifest; entry gains `collision: {objects:{}}` + `validation` keys (R2) |
| Brands / people / cameras / security detail | none |
| $0 / CC0 | own code, no assets |

### Runner (`run_generator.py`) fixes
- **R1 — collision has no Unity side (blocker for `COL_`).** The `COL_Rack` mesh exports into the FBX as an ordinary mesh with UV maps and an `M_Proc_Collision` material. No `AssetPostprocessor` exists in `UnityProject/` (grep), so Unity would **render a blue box around every rack**. Pick one:
  - (a) *Recommended, smaller:* drop the `COL_` mesh. The generator writes `collision_boxes` (Unity centre + size) into the manifest, and the Unity builder adds `BoxCollider`s, as GrayboxBuilder/LookdevBuilder already do. No UV, material or tri cost, and the rolling racks (DEC-062, they slide) get cheap convex colliders.
  - (b) Keep `COL_` and add a Unity `AssetPostprocessor`: `*_COL_*` → `MeshCollider` and strip its renderer. Note: a compound of disjoint boxes in one mesh is non-convex, so it can't sit on a moving rigidbody.
  - Hub decision; see the handoff.
- **R2 — manifest churn.** `entry.setdefault("collision", …)` and `entry["validation"]` are written for **every** asset, so the next rerun of jars, fill and packaged goods rewrites all 24 existing manifest entries and adds 24 `Validation/*.json` files with no geometry change. Write `collision` only when non-empty (or drop it with R1a).
- **R3 — validation JSON adds nothing yet.** It is written only after validation passes, so `errors` is always `[]`. It repeats manifest fields, and `warnings` is free text copied from params. To meet DEC-069's "per-asset validation JSON" usefully, write it **before** the `raise` with the error list too (a failed run then leaves evidence), or drop it and treat the manifest entry as the validation record. Hub call; I lean to the second (less code).
- **R4 — `require_collision`**: keep only if R1b is chosen.
- **R5 — apply route.** Don't use the `.patch` files: they rewrite whole files and flip line endings. Copy the `.py` files in and review `git diff` (the index is LF, so git shows only the additions).

### `proclib.py` fix
- **P1** — move `from mathutils import Matrix, Vector` to the top imports. `add_cylinder_between` uses `to_track_quat("Z","Y")`, which is degenerate when the axis is parallel to Y (side rails, wheel axles). In 5.2.3 it still produces a valid cylinder (sizes validated), but the ring's start angle is arbitrary. Fine for round parts. The helpers are generic and reusable for P2/P3 (register, fridge frames, lockers, ladder): adopt.

### Generator (`wire_shelving.py`) fixes
- **G1 — wire pattern.** Shelves are a square grid at the same pitch both ways (`wire_spacing_m` × `wire_stride`). Generic chrome wire shelves have dense front-to-back wires, a few long wires and a truss edge. Give the two axes separate pitches; that also saves tris. This is a product-type look, not a store fact, so check it against the CCTV tiles listed in `ROOM_FIXTURES` (`wall2_R4C1`, `BOH_still`).
- **G2 — floating wires.** The grid stops `1.6 × post_d` (≈4 cm) short of the side rails, and the rails sit `edge − rail_r` (≈2 cm) above the grid. At close range the wires touch neither the rails nor the posts. Extend the grid to the rail line and drop the rails to the grid plane (or add the truss).
- **G3 — shelf heights.** Levels are evenly spaced between `bottom_shelf_z_m` and `height − top_margin_m`. Real racks are adjustable, and BOH shows a lower stacked section (`Rack_East_Wall` notes). Replace with an explicit `shelf_z_m` list (keep even spacing as the default).
- **G4 — multi-bay runs.** `Rack_East_Wall` (8.7 ft) and `Rack_West_Run` ("2-bay", 8.0 ft) are runs, not one unit. Add `bays` (shared inner posts), or let ART place N units; the shared-post version avoids doubled posts.
- **G5 — black finish.** `Desk_WireRack_Computer` is a **black** wire unit used as a desk (DEC-040/041). That is a params variant (`colors.chrome` → black, plus a keyboard-shelf height), not new code. Note it for P2's desk work.
- **G6 — minor.** Rolling `COL_Rack` starts at the post bottom (0.14 m), so casters have no collision. Fine for the player; mention if R1a is chosen. Only LOD0/LOD1 exist; add a far LOD (one frame box) only if PERF asks.

### Params fixes
- **A1 — `unity_dir` is wrong:** `Assets/_Game/Art/Procedural/Fixtures/WireShelving` lacks the `UnityProject/` prefix every other params file uses. The FBX copy would land in `<repo>/Assets/…` (confirmed in the sandbox). Use `UnityProject/Assets/_Game/Art/Procedural/Fixtures/WireShelving`.
- **A2 — contact sheet:** no `own_sheet: true`, so a run adds two rack rows to the committed default `PROC_contact_sheet.png` (jar/box/pouch scale). Set `own_sheet` and use `contact_sheet wire_shelving`.
- **A3 — `validation_warnings`** free text: drop it. `gaps` already carries the IDs, and the warnings repeat this audit.
- `GAP-PROC-13` is free (highest used is GAP-PROC-12). Register it in PROC_PIPELINE's GAP table on integration.

### Guessed dimensions → real source or GAP
ROOM_FIXTURES = `Docs/Reference/ROOM_FIXTURES.json` (REF-009b rev5); sizes there are `[w, d, h]` ft. Every value below is a named param already, so a real value is a params-only edit.

| Param (theirs) | Guess | Our source | Status |
|---|---|---|---|
| `width_m` | 1.2192 (48 in) | Rack_Rolling_1–4: **6.0 ft** (Low, GAP-127); Rack_East_Wall **8.7 ft** run (Med); Rack_West_Run **8.0 ft**, 2-bay (Med); Rack_South_Wall **5.3 ft** (Low); Rack_Chrome_Cartons **2.5 ft** (Low, GAP-127); Rack_Bags_Tools **3.0 ft** (Low placeholder); Desk_WireRack_Computer **3.4 ft** black (Med) | **wrong for every placement**: per-placement params from ROOM_FIXTURES |
| `depth_m` | 0.4572 (18 in) | Rolling 1–4 **2.0 ft**; East/West run **2.0 ft**; South **1.8 ft**; Cartons **1.2 ft**; Bags/Tools **1.5 ft**; Desk **1.5 ft** | **wrong**: ROOM_FIXTURES |
| `height_m` | 1.8288 (72 in) | **6.0 ft** on all racks above; Bags/Tools **5.0 ft** | matches (Low/Med) |
| `shelf_count` | 5 | Rack_West_Run "4–5 shelves" (Med); others none | GAP-PROC-13 (West run: ROOM_FIXTURES) |
| `bottom_shelf_z_m`, `top_margin_m`, even spacing | 6 in / 4 in | none | GAP-PROC-13 (+ G3) |
| `post_diameter_m`, `collar_*` | 1 in; 1.25 × 1.63 in | none | GAP-PROC-13 |
| `wire_diameter_m`, `wire_spacing_m`, `shelf_perimeter_diameter_m`, `shelf_edge_height_m` | 3.2 mm, 1 in, 9.5 mm, 1 in | none (CCTV can't resolve wire) | GAP-PROC-13 |
| `caster_radius_m`, `caster_width_m`, `caster_stem_*` | 4 in wheel, 1 in, 1.5 in | Rolling racks are "on rollers" (DEC-051/062); no size | GAP-PROC-13 |
| `foot_*` | 1.75 in dia, 3/8 in, 1.5 in stem | none | GAP-PROC-13 |
| `colors.chrome` | grey 0.72 | "chrome" in ROOM_FIXTURES notes; Desk_WireRack_Computer black | ok; black variant (G5) |
| `collision_*_thickness_m` | 35 / 25 mm | gameplay values, not store facts | ok (moot with R1a) |

### Drop 1 summary
**Adapt.** The plumbing is sound: deterministic, inside budget, contract-compatible, and our existing assets' FBX bytes are unchanged. Before PROC integrates:
- R1 collision decision, then R2 (no churn) and R3 (validation JSON on failure, or drop it);
- params A1 (`unity_dir`, a real bug) and A2 (`own_sheet`);
- real sizes per placement from ROOM_FIXTURES;
- G1–G4 for a believable rack.

The proclib helpers can be adopted now.

---

## Drop 2 — `Dispo_Game_Blender_Workstream_Master/` (files dated 2026-10-30 03:27)

`README_FIRST.md` plus 11 zips in `packages/`. I extracted them to my scratchpad, deleted the `.pyc` files unread, and read every `.py` and `.json`.

| # | Package | Assets | Verdict |
|---|---|---|---|
| 1 | `Blender_PROC_vNext_WireShelving` | = drop 1, byte-identical (6 files compared) | see drop 1 |
| 2 | `Register_Station` | POSMonitor, MonitorStand, CashDrawer, BarcodeScanner, ScaleStand + `add_beveled_box` | **adapt**; **reject CashDrawer** (C1) |
| 3 | `Glass_Door_Cooler` | Cooler_SingleDoor, Cooler_DoubleDoor | **adapt** |
| 4 | `Office_Fixtures` | Desk, OfficeChair, StandingDesk, FilingCabinet, TallStorageCabinet, DrawerCart, Worktable | **adapt** (DrawerCart: no store evidence, drop) |
| 5 | `Break_Room` | LockerBank, WoodBench, LunchTable, BulletinBoard, FirstAidBox | **adapt** |
| 6 | `Restroom` | Sink, Mirror, Toilet, PaperTowelDispenser, ToolChest | **adapt** |
| 7 | `Janitor_Closet` | MopSink, Mop, Broom, Bucket + `janitor_supply_rack.json` (reuses `wire_shelving`) | **adapt**; the supply rack crashes (B3) |
| 8 | `Architecture_Kit` | InteriorDoor_3x7, EmergencyExitDoor, DoorFrameKit, ArchOpening, CeilingTile_2x2, SoffitTrim, LEDTroffer_2x2, StripLight, Baseboard, CornerGuard, BlankWallPlate, AccessPanel | **adapt** (SoffitTrim, CornerGuard: no source, optional) |
| 9 | `Fixed_Ladder` | FixedLadder_BlackSteel | **adapt** (B1); dimensions already match ROOM_FIXTURES |
| 10 | `Clutter_Kit` | 3 cartons, PlasticTote, PlasticBin, PaperStack, AluminiumTrashCan, BoxFan | **adapt** (B2, B4) |
| 11 | `Arrangement_Helpers_v2` | `arrangers/placement.py`: `shelf_fill()`, `carton_stack()`, overlap check; 2 params; `tests/TEST_RESULT.json` | **adapt** (H1–H3) |

### How it was checked
- Sandbox as in drop 1: copies only, `ROOT` redirected, Blender 5.2.3 `--factory-startup`, `PYTHONDONTWRITEBYTECODE=1`, deleted afterwards. `proclib.py` = package 2's `proclib_reference_after_patch.py`, which is drop 1's `proclib.py` + `add_beveled_box` (diffed). Package 2's `patches/proclib_add_beveled_box.patch` is **0 bytes**, so the reference file is the only copy of the helper.
- Every generator and param file was run. A clutter re-run used a sandbox-only copy of the params with `require_collision: false` on PaperStack, so BoxFan could be reached.
- Winding/normal check (my own script, run on the exported FBX): signed volume plus inconsistent-edge count on all **146 LOD0 meshes**, including the hand-built arch faces. **All outward, no inconsistent edges.**
- Determinism: a second run of 7 generators + clutter gave **47/47 FBX byte-identical**. Seeded `random.Random` in the clutter kit is per asset and per LOD, so carton dimensions match across LODs.
- `placement.py` (pure Python, no bpy) was **read, not executed**. `TEST_RESULT.json` is a result file with no test code, so it is unverifiable.

| Result | Assets |
|---|---|
| **pass** (validation, budget, size) | 46 of 50 as shipped, 47 with PaperStack relaxed: every register, cooler, office, break-room, restroom, janitor-prop and architecture asset; 3 cartons, tote, bin, trash can; PaperStack once its collision flag was relaxed |
| **fail B1** | `FixedLadder` LOD1: size x 0.4783 ≠ 0.48. With 5 cylinder segments no vertex reaches −x, so the rails fall short of the declared width. The same hazard exists wherever a cylinder defines an extent with an odd segment count |
| **fail B2** | `Clutter_BoxFan` LOD0: depth 0.202 ≠ 0.12. Blades are rotated in the XY plane, so they stick out of the front and back of the frame. The comment in the code admits it |
| **fail B3** | `Janitor_SupplyRack`: `ValueError: cylinder endpoints must differ`. With `foot_radius_m` = `collar_outer_diameter_m`/2, the foot-to-post bracket has zero length. That is a `wire_shelving._feet` bug, so skip a zero-length bracket |
| **fail B4** | `Clutter_PaperStack`: `require_collision: true` is set for the whole family, but paper stack emits no `COL_`. Set it per variant |
| Tris | all far below their params budgets (largest: Cooler_DoubleDoor 2996 LOD0, LockerBank 1948, ScaleStand 1192; props ≤ 260) |

### Shared fixes (all packages)
- **S1 `unity_dir`**: every params file lacks the `UnityProject/` prefix (drop 1 A1). In the sandbox, 47 FBX copies landed in `<root>/Assets/…`.
- **S2 `own_sheet`**: absent everywhere. All 50 new assets would join the default `PROC_contact_sheet.png`, and at 3 tiles × 320 px per row the sheet passes the 1 MB limit, so `contact_sheet` raises. Set `own_sheet: true`, or render one sheet per generator.
- **S3 prop budgets**: DEC-069 caps props at ≤~1k tris, but params budget mop/broom 1200, bucket 1400, carton up to 2200, tote 1800, trash 1800, fan 2600, cash drawer 1100. Actuals are ≤ 260, so set prop budgets to ≤ 1000. The fixture budgets (≤ 5000) are fine.
- **S4 collision**: same decision as drop 1 R1. Every family emits `COL_*` meshes with UVs and a material, and the repo has no Unity postprocessor. If the Hub picks R1a (manifest boxes), every `COL_*` builder becomes a box list; they are all boxes already.
- **S5 handles inside doors (z-fighting)**:
  - Affected: `Office_TallStorageCabinet`, `Office_FilingCabinet` and `Restroom_ToolChest`. The handle box spans `-d/2 … -d/2 + handle_depth`, which lies entirely inside the door or drawer front (`-d/2 … -d/2 + door_t`). The front faces are coplanar, so handles flicker or vanish.
  - Lockers do it right: the door is recessed by `handle_d`. Do the same.
- **S6 moving parts**: the cooler lists only `DoorFrame_nn` as moving, but `Glass_nn` and `Handle_nn` must swing with it. Group them, or merge glass + handle into the door object. Every hinge is `left`; give a `hinge_side` param per door.
- **S7 wall-mount origin**: keep our bottom-centre rule (PROC_PIPELINE outranks the brief). ChatGPT kept it and flagged the conflict; no change needed.
- **S8 `validation_warnings`** free text in every params file: drop (drop 1 A3).
- **S9 GAP ids**: GAP-PROC-14..22 are ChatGPT's proposals, free in our repo (highest used is GAP-PROC-13 from drop 1). Register them only for values with no source; the table below assigns the sourced ones.

### Package fixes and guessed dimensions → source
ROOM_FIXTURES sizes are `[w, d, h]` ft; RI = `Docs/REFERENCES_INDEX.md`. Anything not listed keeps the package's GAP.

**2 Register station (GAP-PROC-14)**
- **C1 reject `CashDrawer`**: REF rules (RI back-room section "Excluded by rule", DEC-051) say no cash-handling equipment, generic props only.
- **Scale stand vs RI §2.2:**
  - Footprint 0.62 × 0.46 m → **0.49 × 0.40 m** (1.6 × 1.3 ft, Low-Med).
  - Top 0.91 m → **0.76 m** (2.5 ft, Low).
  - Levels: two wire shelves (0.28/0.52 m) → **one** wire shelf at **0.15–0.24 m** (0.5–0.8 ft, Med).
  - Top: grey painted slab → **black tray with a raised lip** (Med).
  - Acrylic: tall 0.54 m back panel + side panel → **full-width panel on the counter-side edge, 0.24–0.37 m** (0.8–1.2 ft; Med position, Low size). In the wide view it may be a 3-sided riser.
  - Scale: black → **white body, blue LCD, clear round draft-shield bowl** (Med). One scale (a second is Low).
- Monitor/stand/scanner: generic sizes, no measurement (GAP-PROC-14). The BOH `Scanner_Barcode` is a **handheld scanner in its stand**, 0.4 × 0.7 × 0.6 ft; ChatGPT's scanner is a presentation-style block, which is a different object.
- Missing vs the brief: the POS counter itself. The TI gives it (RI §6.4: 34 in max, 2'-6" deep quartz top, 4 in base, walnut front). Also keyboard, receipt printer and card terminal (RI §2.2 "Other counter facts", Med presence). Whether a card terminal counts as cash equipment is a Hub call.

**3 Cooler (GAP-PROC-15)**
- `Cooler_GlassDoor_2Door` = **4.0 × 2.5 × 6.5 ft → 1.22 × 0.76 × 1.98 m**, black frame, lit (Med; RI §2.3 Low). Theirs: 1.38 × 0.76 × 2.02. Use ROOM_FIXTURES.
- The SingleDoor variant has no store instance; keep it as the param demo or drop it.
- Handles float 46 mm in front of the door with no standoffs (`handle_y = -d/2 + r` vs door at `-d/2 + 0.055`). Add standoffs or move the handle to the door.
- Glass sits behind the frame bars, which is fine.
- The FOH `Fridge_TopFreezer` (white apartment fridge, 2.2 × 2.3 × 5.5 ft) and the break-room `Fridge_Magnets` (2.8 × 2.4 × 5.8 ft) are **not covered**; a top-freezer variant is missing.
- Shelf contents are DEC-050 facts: the cooler holds concentrates and perishable edibles, the fridge drinks (see H3).

**4 Office (GAP-PROC-16)**, against ROOM_FIXTURES Office rows:

| Asset | Theirs (m) | Store | Fix |
|---|---|---|---|
| Desk | 1.45 × 0.72 × 0.75, wood straight | `Desk_West_Arm` 4.8 × 2.5 × 2.5 ft + `Desk_Corner_Dual_Monitor` 4.3 × 2.5 × 2.5, **black laminate L**; BOH `Desk_ExRegister1` **white top** 4.0 × 2.0 × 2.5 | L/corner variant, colours black/white, sizes from ROOM_FIXTURES |
| StandingDesk | 1.35 × 0.70 × 1.12 | `Desk_Standing_East` 3.6 × 2.0 × 3.5 ft (Low) | 1.10 × 0.61 × 1.07 |
| FilingCabinet | 0.47 × 0.62 × **1.32**, 4 drawers | `FileCabinets_UnderDesk` **several black** cabinets under the standing desk, run 3.4 × 1.8 × **2.4 ft** (count Low) | must fit under the desk: ≤ 0.73 m tall, black, ~2 drawers |
| TallStorageCabinet | 0.92 × 0.46 × 1.85, grey, 2 doors + chrome handles | `Cabinet_Tall_Black_A/B` 2.4 × 2.0 × 5.0 ft, **plain black closed box, no hardware detail** (DEC-051 Q9) | 0.73 × 0.61 × 1.52, black, a `doors: false` option |
| Worktable | 1.52 × 0.76 × **0.91**, grey | `Worktable_Stainless` 5.3 × 2.5 × 2.5 ft, **stainless top, folding legs** | 1.62 × 0.76 × 0.76 |
| OfficeChair | 0.68 × 0.68 × 1.08, 4-arm base | `Chair_Task_1/2` 2.0 × 2.0 × 3.2 ft, **black mesh** task chair | 0.61 × 0.61 × 0.98; a 5-star base is the commercial norm (visual, not a store fact) |
| DrawerCart | 0.52 cube-ish | no store row; the office has `Cart_Deli_Prep` (stainless 2-shelf utility cart) and `Cart_WireBasket` (black wire) | drop; the deli prep cart is the needed one |

**5 Break room (GAP-PROC-17)**
- **LockerBank: store fact (DEC-047/051 Q5, High) = one unit about 2 × 6 ft** (`Lockers_Staff` 2.0 × 1.5 × 6.0 ft, GAP-126). Theirs is a 4 × 2 bank of 8, 1.22 m wide, so it is **wrong**. Use `columns`/`rows` to fit 0.61 × 0.46 × 1.83 m, grey top. The locker count per unit is a Nolan question (below).
- WoodBench: `Bench_Wood` 5.0 × 1.3 × 1.5 ft = **1.52 × 0.40 × 0.46** with **black steel legs** (theirs 1.22 wide, wood legs). Note: RI §1.5 vector says bench 1.0 × 7.0 ft; ROOM_FIXTURES (REF-009b) is the newer source.
- LunchTable 1.22 × 0.76 × 0.75 ≈ `Table_Lunch` 4.0 × 2.5 × 2.5 ft (Low): ok.
- BulletinBoard 0.91 × 0.61: `Board_Bulletin_West` 3.0 × 2.5 ft → **0.91 × 0.76**. The same generator covers `Board_Cork` (hall, wood frame, 1.8 × 2.6 ft), the office boards and `Whiteboard_West` (4.0 × 3.0 ft, red/white frame) as params variants.
- FirstAidBox 0.33 × 0.12 × 0.45 ≈ `FirstAid_Kit` 1.0 × 0.4 × 1.3 ft (Med): ok. The green ISO cross is fine (no red-cross emblem).
- Missing vs the room: base cabinets + black counter (34 in, TI), uppers, double sink, magnet fridge, whiteboard, microwave, coffee maker, mini hoop, coat hooks (ROOM_FIXTURES BreakRoom rows).

**6 Restroom (GAP-PROC-18)**
- Sink: **pedestal** sink, but the store has `Lavatory_WallHung` with **27 in knee clearance** (TI §6.4/§6.6, High). Remove the pedestal and use brackets or none. 1.7 × 1.5 ft → **0.52 × 0.46 m**, rim 0.864 (theirs matches). **Bowl bug:** the lofted "bowl" is a capped solid whose top cap is coplanar with `BasinTop` at z = h, so there is no visible basin and the faces z-fight. Use an open loft (no top cap), recessed.
- Mirror 0.61 × 0.81 → TI **1'-8" × 3'-6" = 0.51 × 1.07 m**, bottom 3'-4" AFF (High; ROOM_FIXTURES keeps it).
- Toilet 0.39 × 0.72 × 0.78 vs `Toilet` 1.6 × 2.4 × 2.5 ft (0.49 × 0.73 × 0.76, Med): widen.
- PaperTowelDispenser: **white plastic**, but DEC-062 says **old silver manual**. Use a chrome/stainless colour. Size ≈ `Accessories` 1.1 × 0.4 × 1.5 ft: ok.
- ToolChest 0.82 × 0.46 × **0.91**: `ToolChest_Black` 2.2 × 1.5 × 2.75 ft = 0.67 × 0.46 × **0.84**, which must stay **below the 33 in grab bar**. Theirs is too tall. Two shelves inside are not modelled (closed doors, fine).
- Reusing `PROC_Office_TallStorageCabinet` for `Cabinet_Storage_Large` (4.0 × 1.5 × 7.0 ft, GAP-109) needs its **own params variant**; the office cabinet is 2.4 × 2.0 × 5.0.
- Missing: grab bars 42 / 36 / 18 in at 33–36 in AFF (TI, High), TP and soap dispensers, sconce (TI types).

**7 Janitor closet (GAP-PROC-19)**
- MopSink 0.61 × 0.61 × 0.30 → `MopSink_JC` 1.6 × 1.5 × 1.0 ft = **0.49 × 0.46 × 0.30** (A011, Med). FRP to 4 ft is wall finish, not this asset.
- Supply rack 0.76 × 0.36 × 1.22 → `Rack_CleaningSupplies_JC` 2.0 × 1.2 × 5.0 ft = **0.61 × 0.37 × 1.52** (Low), plus B3.
- Mop/broom 1.45/1.40 m ≈ `Mops_Brooms_JC` 5.0 ft (1.52): ok. The bucket is a closed top; fine at this distance.

**8 Architecture kit (GAP-PROC-20)**
- **Doors:** the TI door is a **3'-0" × 7'-0" × 1¾" leaf** (RI §6.2, High). The generator puts the frame *inside* `width_m`/`height_m`, so the leaf comes out **0.816 × 2.08 m**. Make `width_m`/`height_m` the leaf (or opening) and add the frame outside; the 1¾" leaf thickness (0.044) is right.
- Door finishes/colours per ROOM_FIXTURES: black HM (hall/office, break, JC, vestibule) and white (office→HUB 2). JC is **2'-8"**. The SE exit door is green with a round logo (DEC-030). The logo is store branding, so leave it blank for the brand/IP question.
- Push bar + closer only: OK under DEC-051/062 (no access-control hardware).
- **Arch:** retail arches are **3'-0" × 7'-0" gypsum cased openings** (RI §6.2/§6.4, High; vestibule arch A011 ≈ 3.1 ft). Theirs: 1.52 × 2.44, painted metal trim. Use width 0.914 clear, top 2.134, gypsum/slat finish.
- CeilingTile 2 × 2 and LEDTroffer 2 × 2: **match TI** (ACT-1 at 8'-0"/9'-0", L1 troffer, High). StripLight 1.2 m ≈ L2 4 ft (1.219); use 1.2192, and the 2 ft too. `Light_Strip_Pendant` is Low.
- Baseboard: TI **VB-1 grey vinyl 4 in** → height 0.1016 (theirs 0.1).
- Wall plate 70 × 115 mm = standard single-gang: ok. White or matte black per TI §6.5.
- AccessPanel: no source, but it can serve as the hall `Panel_Blank` (1.0 × 1.5 ft, DEC-062) via params.
- SoffitTrim, CornerGuard: no source; optional.

**9 Fixed ladder (GAP-PROC-21)**
- Matches `Ladder_FireEscape` (1.5 × 0.6 × 9.0 ft = 0.46 × 0.18 × 2.74; theirs 0.48 × 0.197 × 2.75), black. Use the ROOM_FIXTURES values, so no new GAP is needed (ROOM_FIXTURES Low/Med).
- Fix B1: even segment counts (≥ 6), or compute the extent from the vertices.
- Note for REF, not ChatGPT: TI gives FOH (107 Fulfillment) an ACT ceiling at 8'-0", but the ladder row is 9 ft "full height". Check whether it passes a ceiling hatch.

**10 Clutter kit (GAP-PROC-22)**
- B2 fan blades: rotate them in the XZ plane inside the frame. The store fan is `Fan_Portable` **white, 1.0 × 0.8 × 1.0 ft (0.30 × 0.24 × 0.30)**, not a 0.52 box fan.
- Trash can 0.42 Ø × 0.58 → `Trash_Aluminium` 1.5 × 1.5 × 2.5 ft = **0.46 × 0.76 tall**. The office `Trash_StepCan` (stainless, 1.0 × 1.0 × 2.0 ft) is a second variant. The rim is a rounded-square bevel box on a round body; make it a ring.
- Tote: FOH totes are **yellow** (`Props_Floor`, R4C1); theirs is blue-grey.
- Bin: FOH racks use **clear** sorted bins and **black** trays (`Rack_Rolling_*`); add both variants.
- Open-carton LOD0 includes flaps (wider than LOD1), so the silhouette pops at the LOD switch. Acceptable, or keep the flaps in LOD1.
- B4: per-variant `require_collision`.

**11 Arrangement helpers**
- **H1 origin bug:** placements set `y = shelf_y + item_h/2` (and `layer_bottom + h/2` for cartons), i.e. the item *centre*. Our assets' origin is the **bottom centre** (PROC_PIPELINE), so every item floats by half its height. Use `y = shelf_y` / `layer_bottom`.
- **H2 anchor size:** wire-shelf anchors give the outer `w × d`, so items can sit over the rails/posts. Use the inner usable area, or keep `gap` ≥ post inset.
- **H3 product truth:** a random `category_mix` fill is decor only. The FOH racks, fridge and cooler hold DEC-050 categories (racks: vapes, edibles, some infused prerolls; fridge: drinks; cooler: concentrates + perishable edibles). Real stock must come from inventory data (DATA-002 / GAME-004), never invented. Use the arranger only for non-interactive dressing (BOH cases, decor), with `category_mix` from DEC-050.
- `category` exists on our packaged-goods manifest entries, so the mix does work. There is no runner hook, as ChatGPT says; it belongs with whoever owns population (GAME-004).

### Drop 2 summary
**Adapt overall.** The code is clean, deterministic and correctly wound, and almost everything fits our contract.
- **Bugs:** 4 crash/validation bugs (B1–B4), handles buried in doors (S5), a bowl-less sink, and floating cooler handles.
- **Params:** `unity_dir`/`own_sheet` are wrong in every params file.
- **Accuracy:** most sizes are generic guesses where ROOM_FIXTURES/TI already had the answer. The worst: the lockers (1 unit, not 8), the office cabinets (black plain boxes), the file cabinets (under-desk), the scale stand (RI §2.2 spec), the pedestal vs wall-hung sink, the mirror (TI), the door leaf (3'-0" × 7'-0") and the arch (3'-0" × 7'-0").
- **Reject:** CashDrawer (DEC-051). DrawerCart, SoffitTrim and CornerGuard have no store evidence (optional).
- **Not covered:** POS counter, top-freezer/magnet fridges, break-room millwork, grab bars, deli prep cart.

---

## Drop 3 — `Fixture_Toolkit_Full_Package/` (files dated 2026-10-30 03:37)

Shared-library work only: no generator, params or asset.

| File | What | Verdict |
|---|---|---|
| `patches/01_…foundations.patch` | +316 lines to `proclib.py`: `ft`/`inch`/`feet_inches`, prism/square tube, sheet panel, countertop slab, panel frame, wire grid, adjustable foot, caster assembly, cabinet carcass, door panel, drawer box | **adapt** (T1–T5) |
| `patches/02_…completion.patch` | +346 lines: hollow enclosure, bent-sheet lip, slotted panel, shelf clip, panel inset, shelf, U-pull, commercial leg/base, trim profile | **adapt** (T1–T5) |
| `proclib_reference_after_both_patches.py` (867 lines) | the snapshot; **also changes `mesh_stats()`** (T2) | reference only |
| `docs/*.md`, `tests/*.json` | coverage claim "27/27 Priority-1 capabilities", syntax-only checks | info |
| `__pycache__` (1 `.pyc`) | — | **reject** |

### How it was checked
- **Patch chain:** both patches apply in order (patch 01 at offset −18) on drop 2's `proclib_reference_after_patch.py` (= ours + drop 1 + `add_beveled_box`). **Not on our current `proclib.py`.**
- **Patches vs snapshot:** the result is **not** equal to the reference snapshot. The snapshot additionally rewrites `mesh_stats()` (T2), which neither patch contains.
- **Diff:** apart from `mesh_stats`, the snapshot vs drop 2 is additions only.
- **Smoke test** (my own driver on a sandbox copy of the snapshot, Blender 5.2.3 headless, sandbox deleted): all 20 new geometry helpers (plus the 3 unit functions) were called once, then `finish_object` + `mesh_stats`.
  - All run, with no exceptions.
  - Every size check passes: square tube/prism along Y and X keep their cross-section (no roll problem), carcass/drawer/enclosure/slotted/inset/shelf/legs/trim at the requested sizes, and the U-pull stands off the face by its `stand_off`.
  - Unit checks: `ft(3)` = 0.9144, `feet_inches(2, 6)` = 0.762.

### Fixes
- **T1 apply route:**
  - The patches assume drops 1 + 2 are already applied, and the snapshot carries an extra change. Integrate from the snapshot, minus or plus T2 by Hub decision, after the drop 1 R/P fixes. Don't apply the patches to `main`.
  - Style: three function seams have no blank lines (after `add_vertical_cylinder`, `add_beveled_box`, `add_drawer_box`).
  - The `proclib.py` comment from drop 1, "existing PROC helpers unchanged", becomes false once T2 lands.
- **T2 undeclared `mesh_stats()` change:**
  - Adds `empty mesh` → raise (good), `bounds_m_blender_xyz`, `material_slots`, and `geometry.non_manifold_edges` / `degenerate_faces`.
  - Every manifest entry (all 24 existing assets) changes on the next rerun. FBX bytes are not affected, since stats don't touch the export.
  - The non-manifold count is **noisy**: touching boxes merged by `remove_doubles` count as non-manifold (carcass 6, drawer 6, frame 4, slotted 4…), and our card meshes (jar `Label`, `ThcTag`) are open quads by design. Keep it informational and never gate on it.
  - Adopt the empty-mesh raise. Take the rest only if the Hub wants it, and fold it into the same single re-baseline commit as drop 1 R2.
- **T3 dead code:**
  - None of the ~650 new lines is used by any generator (drops 1–3).
  - Meanwhile the drop 2 families re-implement the same things: three private wire grids (`wire_shelving`, `register_station._wire_shelf`, cooler `_shelves`), five door/drawer/carcass builders, and handles.
  - Adopt the helpers **together with** refactoring the integrated families onto them, with one implementation each: `add_wire_grid`, `add_door_panel`/`add_drawer_box`/`add_cabinet_carcass`, and `add_handle_pull`. `add_handle_pull` stands off the face, which fixes drop 2 S5.
  - Helpers still unused after that refactor (slotted panel, bent lip, shelf clip, panel inset, trim profile, leg base, hollow enclosure) wait until a generator needs them. This matches our "nothing to register / no code for later" pipeline style.
- **T4 helper gaps:**
  - `add_wire_grid` has one `spacing` for both axes; drop 1 G1 needs separate X/Y pitches (`spacing_x`, `spacing_y`).
  - The caster wheel's ring roll is arbitrary when the axle is along Y: the wheel's x extent is 0.0951 for a 0.1 diameter. That's harmless for floor contact, but don't let it define asset bounds (drop 2 B1 class).
  - "hinge-ready part / hinged door / sliding drawer" map to plain geometry helpers. There is **no** hinge/slide metadata helper, so drop 2's per-family hinge dicts stay duplicated. A small `hinge_axis(...)` / `slide_axis(...)` helper returning the manifest dict would close that.
- **T5 units:** params JSON stays in meters (PROC_PIPELINE: params are the only place dimensions live). `ft()`/`inch()` are for generator code converting ROOM_FIXTURES/TI values, not for literal store sizes in code.

### Drop 3 summary
**Adapt.** The helpers are correct in Blender 5.2.3 and generic (no store dimensions, brands or security detail). Take them through the snapshot, with T2 as a Hub decision, and only alongside a refactor that makes the drop 2 families use them. Then add separate wire pitches and a hinge/slide metadata helper.
