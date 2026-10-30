# IMP-003 — ChatGPT Blender toolkit audit (rolling)

Scope: DEC-069 brief. Source folder: `C:/Users/handl/Downloads/Dispo Game Imports/` (untouched, DEC-070). Our pipeline: `Tools/Blender/` at main 33e57a1, `Docs/Assets/Specs/PROC_PIPELINE.md`.
Verdicts: **adopt** = take as is; **adapt** = take after the listed fixes; **reject** = do not take.

> **Process update (2026-10-30):**
> - **DEC-083:** findings go to the studio PROC integration worker, not back to ChatGPT. The actionable list is `Docs/Imports/IMP-003_PROC_FIX_CHECKLIST.md`, which supersedes the "ask ChatGPT for the fixed files" advice below (drop 4 §A2); the worker fixes those items from the current files.
> - **DEC-084 quality bar** (realistic store-specific LOD0, 2K–4K PBR, LOD0–LOD3, LOD0 guides of props 5–20k / fixtures 20–80k / hero 30–150k) **withdraws** the tri caps used below: drop 1 budgets and drop 2 S3 "props ≤ 1k". By that bar every audited generator is too simple; the per-family missing detail is checklist §Q.

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

---

## Delta check 1 — ChatGPT "fixed" claims relayed by the Hub (2026-10-30 03:42)

**Claimed fixes:**
- ladder bounds; open-carton LOD mismatch; box-fan blade orientation; missing paper-stack collision;
- incomplete moving-part groupings; janitor prop collisions; LOD-dependent locker metadata;
- opt-in validation checks for non-manifold geometry, degenerate faces, material slots, aggregate bounds and bottom-centre origins.

**Finding: none of it is in the Imports folder.**
- **Folder contents:** still only `blender_proc_vNext/` (03:11), `Dispo_Game_Blender_Workstream_Master/` (03:27) and `Fixture_Toolkit_Full_Package/` (03:37). No file is newer than drop 3.
- **Zip contents:** re-extracting all 11 zips gives a tree **identical** to the one audited in drop 2 (`diff -rq`, `.pyc` excluded). Drop 3's snapshot is unchanged too (867 lines).
- **Nothing elsewhere:** nothing newer turned up in `Downloads/` (depth 2).

So every claim is **unverified**, and the drop 1–3 findings stand as written. B1 (ladder), B2 (fan), B4 (paper stack), S6 (cooler moving parts) and the open-carton LOD pop are still present in the files we have.

**Partial overlap with what exists:**
- **Overlap:** the "validation layer upgrade" (non-manifold / degenerate / material slots / bounds) matches drop 3's undeclared `mesh_stats()` change (T2). That version is **not opt-in**: it adds fields to every asset's manifest entry and is report-only, not a check.
- **Not in drop 3:** a bottom-centre origin check.

**When the updated package arrives, verify:**
1. **Behaviour:** each fix by a sandboxed run, re-running the four failing assets;
2. **Opt-in:**
   - the new checks are opt-in via params, with byte-identical manifest + FBX for an existing generator (`deli_jar`, as in drop 1);
   - the checks actually fail on a planted bad mesh: an open quad, a zero-area face, an off-origin object.
3. **Janitor collision:** janitor props gaining `COL_` (drop 2 S4 applies);
4. **Locker metadata:** it no longer differs per LOD.

---

## Drop 4 — round 2 (`Dispo_Game_Round2_Workstream/`, 2026-10-30 03:50), section A: packages, apply order, round-1 claims

### A1. What is in the Imports folder now, and what supersedes what
| Package | Date | Status | Supersedes |
|---|---|---|---|
| `blender_proc_vNext/` | 03:11 | unchanged (drop 1) | — |
| `Dispo_Game_Blender_Workstream_Master/` | 03:27 | unchanged: all 11 zips re-extracted and `diff -rq` identical to drop 2 | its zip 1 = `blender_proc_vNext/` (identical), so the loose folder is redundant |
| `Fixture_Toolkit_Full_Package/` | 03:37 | unchanged (drop 3) | its snapshot supersedes drop 2's `proclib_reference_after_patch.py` (adds 20 helpers + the `mesh_stats` change) |
| `Dispo_Game_Round2_Workstream/` | 03:50 | **new**: 9 generators, `materials/cc0_pbr.py`, 10 params, 2 `proclib` reference copies, 1 patch, 4 docs, 12 `.pyc` (not opened) | nothing; it is additive |

**`proclib.py` lineage:**
- Round 2's `proclib_reference.py` = drop 2 snapshot + drop 3's `mesh_stats()` change, **without** drop 3's 20 helpers.
- `…_after_round2_patch.py` adds only `patches/proclib_preserve_rgba_alpha.patch`: `material()` alpha defaults to `rgba[3]`.
- Round-2 generators import only `add_box`, `add_beveled_box`, `add_cylinder_between`, `finish_object`, `material`, so they need **drop 1 + `add_beveled_box`**, not drop 3.

**Recommended apply order** (into a PROC worktree, never `main` directly):
1. Drop 1 runner/proclib, with fixes R1–R5 and P1.
2. `add_beveled_box` (taken from the drop 3 snapshot).
3. The round-2 alpha patch.
4. Drop 3 helpers only together with the family refactor (T3).
5. Families in the order of the integration list in the summary.

**Alpha patch check:** no existing generator passes a 4-component colour without an explicit alpha. `deli_jar`'s glass passes 0.25 explicitly, and `packaged_goods` unpacks `rgba()`. So **existing output is unchanged; adopt**.

### A2. Round-1 fix claims (relayed by the Hub, 2026-10-30)
Every round-1 file is byte-identical to the drop 2 audit, and no newer runner or generator exists anywhere in the folder. So:

| Claim | In the files? | Evidence |
|---|---|---|
| Ladder bounds (B1) | **no** | `fixed_ladder.json` LOD1 `tube_segments` is still 5 |
| Open-carton LOD mismatch | **no** | `clutter_kit._carton` still adds flaps only when `detail` is set |
| Box-fan blade orientation (B2) | **no** | blades still `_rotated_box` about Z |
| Paper-stack collision (B4) | **no** | still a family-wide `require_collision`, and no `COL_` on PaperStack |
| Moving-part groupings (S6) | **no** | cooler `moving_parts` still lists only `DoorFrame_nn` |
| Janitor prop collisions | **no** | Mop/Broom/Bucket still emit no `COL_` |
| LOD-dependent locker metadata | **no** | same `break_room.py` |
| Opt-in validation: non-manifold, degenerate, material slots, aggregate bounds, bottom-centre origin | **partly, not as claimed** | Only `mesh_stats()` gains non-manifold/degenerate counts, material slots and per-object bounds (drop 3 T2, repeated in round 2's `proclib_reference.py`). It is **always on, report-only** (never fails), and changes every manifest entry. There is **no origin check**, no aggregate-bounds check and no opt-in flag. No updated `run_generator.py` was shipped |

**Conclusion:** the fixes ChatGPT describes are probably in its own workspace but were **not delivered**. All drop 1–3 findings stand.

## Drop 4 section B: round-2 generators, materials, dimensions

### B1. How it was checked
- Every `.py`/`.json` was read; the 12 `.pyc` were not opened.
- Sandbox as before: copies only, `ROOT` redirected, drop 1 runner + `proclib_reference_after_round2_patch.py`, Blender 5.2.3 `--factory-startup`, deleted afterwards.
- **No network:** `material_library` ran with `download_sources: false` (a sandbox-only params edit), so no provider API or download was touched.
- Winding check (drop 2 script) on all exported FBX: **54 meshes, all outward, no inconsistent edges**.
- Determinism: a second run gave **38/38 FBX + SVG byte-identical**.

| Family (DEC-074 item) | Assets | Result (LOD0 tris) | Verdict |
|---|---|---|---|
| `deli_counter_jar_wall` (deli counter + jar wall) | Counter, JarWall | pass (152, 84) | **adapt**: wrong shapes (B2) |
| `register_counter_run` (×11 + POS frame) | RegisterCounterRun | pass (248) | **adapt**: straight run vs the real L; references the rejected CashDrawer (B2) |
| `id_check_stand` | IDCheckStand | **fail**: height 1.119 ≠ 1.08 (scanner and lens sit above the declared `height_m`) | **adapt** |
| `display_cases` | CountertopCase, TallCase | pass (228, 264) | **adapt**: no top glass; glass has no collision |
| `bag_racks` (bag racks / exit-bag station) | WallRack, ExitDispenser, ToolCaddy | WallRack and Dispenser pass; **ToolCaddy fails**: height 0.259 ≠ 0.25 (handle tube radius above `h + handle_h`) | **adapt**; no store source for these forms |
| `sign_blanks` | WallPoster, AFrame, MenuBoard | Poster and MenuBoard pass (separate probe); **AFrame fails**: legs splay past depth and height (0.541 × 0.923 vs 0.52 × 0.92) | **adapt** |
| `material_library` (CC0 library) | PROC_MaterialLibrary swatches + `provenance.json` | pass offline (828) | **adapt**: loader must use our DEC-023 cache (B3) |
| `label_decals` (generic + approved) | 5 generic + 6 approved labels, SVG per label | pass (84 each) | **adapt** (B4) |
| `building_shell_exterior` | StorefrontGlazing, EntryVestibule, Parapet_1m, ParkingCurb, ParkingStripe_1m, BlankSignBand | pass | **adapt**: entry is wrong (B2) |
| first-person hands | omitted ("no people" read conservatively) | — | OK: DEC-074 made it optional; ASSET-003 owns characters |

**Shared fixes** (as drop 2): `unity_dir` lacks `UnityProject/` in all 10 params (S1); no `own_sheet` (S2); `COL_` decision (S4); free-text `validation_warnings` (S8).
- GAP ids are `GAP-R2-01..09`, a new scheme. Fold them into `GAP-PROC-*` on registration, and only for values that have no source (B5).
- Round-2 budgets respect ≤5k fixtures / ≤1k props.

### B2. Generators vs DEC-074, our contract and the store
- **No brands, people, cameras or security detail** in any round-2 geometry. The ID-check stand's scanner is an age-check pad, not access control: OK.
- **Deli counter:**
  - The real deli counter is an **L** (plan bbox 14.0–34.2 × 18.0–25.2 ft, RI §1.5) with a **teal/white checker tile front** ("DELI STYLE", R2C1/R2C2, Med) and globe pendants at its west end.
  - Theirs is a straight 2.4 m counter with a clear acrylic front. Make L segments + a corner piece, tile-front material.
  - Its height and depth are **not in the TI** (GAP-113): keep as a GAP.
- **Jar wall:**
  - Slots match `PROC_DeliJar` exactly (0.1524 × 0.2604 × 0.1397 = 6.0 × 10.25 × 5.5 in, REF-007). Slot anchors use the bottom-centre origin ✓.
  - The real walls are long runs: **north 26.0 × 1.2 ft, south 21.2 × 1.2 ft, east 1.4 × 14.0 ft** (RI §1.5). The shelves are **dark-grey metal** (DEC-043) on a **teal leaf-pattern backlit** back (R2C3, photo 11), in arched wood frames (photo 11).
  - Make the width/sections params per run.
  - **Slot count must not be a fixed 7 × 4.** It comes from the catalog: one jar per strain, house deli doubled (DEC-079); the ~77 jars noted in PROC_PIPELINE.
  - Shelf heights: the TI "special wall display" (glass showcase shelves at 1'-2" on a 34" base, RI §6.4) is the same store-standard family (Med). Use it as the default instead of an even spread.
- **Register counter run:**
  - The store has **11 stations on an L** (DEC-039: south side 7,2,3,4,5,6; east side 12,11; north side 10,9,8), plan L bbox 20–42 × 7–19 ft (RI §1.5). Theirs is one straight 8.2 m box.
  - Counter per TI: **34 in (0.864) max, 2'-6" (0.762) deep white quartz top (QZ-2), walnut-veneer front, 4 in base, open black shelves underneath** (RI §6.4, R2C3). Theirs: 0.96 tall, 0.74 deep, brown laminate, closed.
  - **Station components:**
    - drop `cash_drawer` (rejected under DEC-051, drop 2 C1);
    - put `scale_stand_slot` **on the floor on the staff side, to the staff's right of each monitor** (RI §2.2), not on the counter top (`y = h`);
    - add keyboard, receipt printer and card-terminal slots (card terminal pending the Hub ruling).
  - The countertop display case (1.4 × 1.4 ft at x 38–39.4, RI §1.5, "lit black glass", R3C2) belongs on this run.
- **ID-check stand:**
  - Where ID is checked is a store fact we don't have (GAME-008 models ID events, not a place). Entry stanchions/queue exist (R2C1, 4 lanes RI §1.5).
  - Keep it as GAP and add a Nolan question.
  - Fix the height: either declare `height_m` as the top including the scanner, or exclude the scanner from the expected size.
- **Display cases:**
  - Front + 2 side glass, but **no top glass and no back**. A counter case needs a top. Collision covers only the base and the side posts, so a player can walk into the glass. Add glass to the collision box.
  - Sizes: countertop case ≈ **0.43 × 0.43 m** (1.4 × 1.4 ft plan, Med); theirs is 1.22 × 0.56.
  - The tall case has no store row; the retail display shelving family (RI §6.4) is the closest.
- **Bag racks:**
  - Store fact: one small FOH rack holds deli bags, exit bags, misc tools and vape batteries (`Rack_Bags_Tools`, 3.0 × 1.5 × 5.0 ft, DEC-051 Q2). Kraft order bags sit on the open shelves under the register counter (RI §2.2).
  - The wall bag-slot rack and exit-bag dispenser **have no store evidence**. Keep them only as optional dressing; the tool caddy is generic.
- **Sign blanks:**
  - The real store uses a **3 × 3 video wall** and wall TVs (menu screen 6.6 × 1.0 ft on the north wall, RI §1.5), a "THURSDAY" deals sheet (photo 10), a "Fine Cannabis" white neon (photo 05) and licenses on the west wall.
  - The hanging menu board and A-frame have no store source. The poster blank is fine.
  - Screen content stays out of scope (REF rule).
- **Building shell / exterior:**
  - The entry is a **6'-0" × 7'-0" out-swinging aluminium storefront pair, two 3'-0" leaves** (TI E101, DEC-037, RI §1.4, High).
  - Theirs is a single 0.91 m door in a glass **entry vestibule**. There is **no exterior vestibule** in any source; the A011 vestibule is the interior FOH/BOH lobby. Reject the vestibule; make a storefront-pair door module.
  - Storefront glass is **GL-1 green-tinted** (TI §6.5). The glazing COL covers only sill and header, so players walk through the glass: add glass collision.
  - Exterior evidence is night CCTV only (R1C1–R1C5, R3C1): light flat-roof walls, wood fascia, hedge, sidewalk, yellow curb, striping, a dark green fence/gate (Med/Low).
  - Parapet, curb and stripe sizes: GAP; stripe colour yellow/white per R1C3/R1C2.

### B3. Materials loader (`materials/cc0_pbr.py` + `material_library`)
| Requirement | Finding |
|---|---|
| CC0 sources only | ✓ Poly Haven and ambientCG (both CC0) plus one project-procedural acrylic. Every entry has `provider`, `asset_id`, `source_url`, `license`, `license_url` |
| Licenses recorded | ✓ in params, on the Blender material (custom props) and in `provenance.json`. **But** not in our `Docs/Assets/LICENSE_LEDGER.md` / `ASSET_CACHE_MANIFEST.json` (DEC-023), which is where `fetch_assets.py --verify` looks |
| No download at import/build time without a manifest | **✗ fails.** `download_sources: true` by default: a cold cache calls `api.polyhaven.com` / the ambientCG `full_json` API **during the Blender build** and downloads whatever map URLs the response lists. There is **no sha256 or version pin**, so a provider-side update silently changes inputs. The ambientCG zip is `extractall`ed unchecked. Provider **API** terms are separate from the asset licence, which is one more reason to fetch once by hand/tool and pin it |
| Determinism | Geometry is deterministic (verified offline); the texture inputs are not, for the reason above |
| Map picking | heuristic substring match (`"color"`, `"rough"`, `"nor_gl"`…) over the API JSON. It works for the standard names but is fragile, and on Poly Haven it can pick a map from a `blend`/`gltf` include entry |
| Unity value | the FBX carries only material **names**: Blender node trees and image links don't survive FBX into HDRP. The game's materials are built in Unity (ART-003 lookdev already imports cache textures via `Tools/Assets/lookdev_textures.py`) |

- **Fix (adapt):**
  - Drop the build-time downloader.
  - Add the 7 provider assets as rows to our fetch list. `fetch_assets.py` already supports Poly Haven and URL sources, and writes sha256 + ledger IDs. `smooth_concrete_floor` is already cached (`PH-smooth_concrete_floor`), and we hold `oak_veneer_05` where they picked `oak_veneer_01`.
  - Let `cc0_pbr.build_material` read **only** cached, manifest-verified files, failing if one is missing (no network).
  - Keep the name list (`M_Proc_*`) as the shared naming contract with Unity.
- **Name collision:** three names point at one source (Stainless, Chrome, BlackPowderCoat all use `Metal011`), which is fine given recorded overrides. `M_Proc_Floor_PolishedConcrete` vs the store: the sales floor is **TL-1 marble-look 12 × 24 and TL-2 8 × 8 tile**; concrete (CONC-1) is the storage-room floor (TI §6.5). Rename or retarget per room.

### B4. Labels / decals
- The whitelist is enforced in code (`ValueError` on unknown brands), and the default params are generic-only ✓.
- **Missing "The Flower Mine"** (approved by DEC-081 after the brief). Add it, and keep the list in one shared data file that BRAND-001 also reads, so it can't drift.
- **Duplicate geometry:** `PROC_DeliJar` already has `Band`, `Label` and `ThcTag` parts with `UVMap_Label` 0..1 (PROC_PIPELINE). Separate label meshes for the jar are redundant. The useful deliverable is the **label texture**, rendered at the label's aspect ratio.
- The SVGs are all 512 × 512 square, so 100 × 80 mm cards and 150 × 55 mm bands stretch. SVG text names `Arial`, which is not ours to ship: use an OFL font when rasterising.
- Unity doesn't use SVG textures without an extra package, so rasterise to PNG in the pipeline.
- Label content must stay generic or from the catalog (strain name and THC % from data at runtime), never invented product data.

### B5. Round-2 guessed dimensions → source
| Param (theirs) | Guess | Source we have | Status |
|---|---|---|---|
| deli counter `width/depth/height` 2.4 × 0.78 × 0.97 | straight | L, bbox 20.2 × 7.2 ft (RI §1.5 vector, Med); height/depth not in TI | footprint: RI; height: GAP (was GAP-113) |
| jar wall `width` 1.55, `height` 2.05, `shelf_rows` 4, `jar_columns` 7 | — | runs N 26.0 / S 21.2 / E 14.0 ft × 1.2 ft deep (RI §1.5); shelf pitch 1'-2" on a 34" base (TI display family, Med); slot = PROC_DeliJar (REF-007); count from catalog (DEC-079) | sourced, except wall height: GAP |
| register `station_count` 11 | — | 11 stations, numbering DEC-039 | ✓ |
| register `height` 0.96, `depth` 0.74, finish | — | 0.864 max, 0.762 top, QZ-2 / WD-1 / open shelves (TI §6.4, High) | **wrong**: TI |
| register `station_width` 0.72, straight layout | — | L bbox 22 × 12 ft (RI §1.5); stations per side DEC-039 | layout: RI; per-station width: GAP |
| scale-stand slot on counter top | — | floor, staff side, right of monitor (RI §2.2) | **wrong** |
| ID stand 0.62 × 0.52 × 1.08 | — | none; location unknown | GAP + Nolan Q |
| countertop case 1.22 × 0.56 × 0.62 | — | 1.4 × 1.4 ft on the register counter, lit black glass (RI §1.5, R3C2) | footprint: RI; height: GAP |
| tall case 0.92 × 0.48 × 1.92 | — | no store row | GAP (optional) |
| bag rack / dispenser / caddy | — | `Rack_Bags_Tools` 3.0 × 1.5 × 5.0 ft (ROOM_FIXTURES) is the only bag fixture | forms unsourced |
| sign blanks | — | video wall 3 × 3, menu screen 6.6 × 1.0 ft (RI §1.5) | blanks: GAP |
| storefront `height` 2.7, `bays` 4, `sill` 0.25 | — | retail ceiling 9'-0" (TI §6.1); GL-1 glass; widths from the A011 west wall | heights partly TI; bays: GAP |
| entry door 0.91 × 2.13 single, vestibule 2.2 × 1.8 | — | **pair 6'-0" × 7'-0"**, no vestibule (TI E101, High) | **wrong** |
| parapet 0.72, curb 0.1 × 0.15, stripe 0.1 wide | — | night CCTV only | GAP |
| labels: card 100 × 80 mm, THC tag 45 × 28, band 150 × 55 | — | identical to GAP-PROC-03/09 (PROC_PIPELINE) | already GAP-PROC-03/09 |

### B6. Questions for Nolan (via the Hub; also in the handoff)
1. **ID check** (GAME-008): where are IDs checked in the store, and on what? Candidates: (a) at the door/queue entrance by a greeter at a podium; (b) at the register by the budtender; (c) both. Best guess: (b).
2. **Deli counter front:** is the "DELI STYLE" counter front teal/white checker tile all the way along, with a glass/acrylic case on top? Source: R2C1/R2C2 tiles. Best guess: a tile front, a black counter top, and no display glass.

### Drop 4 summary
| Package | Verdict |
|---|---|
| Round-1 fix claims | **not delivered**: request the updated round-1 files from ChatGPT before integrating drop 2 |
| `proclib_preserve_rgba_alpha.patch` | **adopt** (existing output unchanged) |
| deli counter / jar wall, register run, display cases, exterior | **adapt**: right idea, wrong shapes; real sizes/finishes exist in RI/TI (B2/B5). Exterior: **reject** the vestibule, make the storefront pair |
| ID-check stand, bag racks, sign blanks | **adapt** (3 validation fails); low priority, mostly unsourced forms |
| material library | **adapt**: no build-time downloads; route through `fetch_assets.py` + ledger |
| labels/decals | **adapt**: add The Flower Mine; textures, not meshes |
| hands | n/a (omitted) |

---

## Drop 5 — round 3 (`Dispo_Game_Blender_PROC_Round3_HQ/`, 2026-10-30 04:15)

**Brief:** DEC-083 round 3. **Rules applied:** DEC-084 quality, DEC-071/081 brands, DEC-079 refill/HUB facts, DEC-086 rulings, DEC-088/090.
**Contents:** 10 generators, the shared `round3_quality.py`, 10 params, `state_presets/interaction_states_round3.json`, `Materials/ROUND3_PBR_BINDINGS.json`, 4 docs, 12 `.pyc` (not opened). The package is additive: no `proclib`/runner replacement, and earlier drops are unchanged.

### How it was checked
- Static read of every `.py`/`.json`.
- Sandbox run: drop 1 runner + round-2 `proclib` + `round3_quality.py`, Blender 5.2.3 `--factory-startup`, `PYTHONDONTWRITEBYTECODE`, deleted afterwards.
- Winding check on 222 LOD0 meshes.
- Determinism re-run of 5 families: 43/43 FBX byte-identical.
- Fix items: checklist §R3.

| Family | Assets | LOD0 tris (measured) | DEC-084 guide | Verdict |
|---|---|---|---|---|
| `office_refill_station` | 1 (cart + scale + bowl + wall shelf + supplies) | 8,504 | fixture 20–80k | **adapt** |
| `hub_storage` | CabinetLoaded, DeliBagFull/Partial, ShipmentCartonClosed/Open, StorageTote | 384–6,412 | props 5–20k / fixture 20–80k | **adapt** |
| `queue_stanchions` | Stanchion, PairExtended | 1,612–1,680 | props 5–20k | **adapt** |
| `back_room_lighting` | Troffer_2x4, Strip_4ft, WallPack | 592–1,704 | props 5–20k | **adapt** (troffer must be 2 × 2, TI) |
| `interaction_state_details` | CashDrawerTray, JarResidue | 3,596 / 836 | — | **reject** the till tray; **adapt** the residue |
| `customer_accessories` | Cap, Beanie, Glasses, Backpack, Purse, Phone, Wallet, BlankID, ExitBag | 324–6,932 | props 5–20k | **adapt** (fit to MPFB2, DEC-087/091 R4) |
| `exterior_vehicles` | Sedan, Hatchback, Crossover | 8,568 each, **body inside-out** | hero 30–150k | **reject** (rebuild, or a CC0 source via DEC-023) |
| `seasonal_decor` | Garland, StringLights, WindowClings | 364–9,784 | props 5–20k | **adapt** (no store source; optional) |
| `counter_props` | ReceiptPrinter, ScaleDigits, CardTerminal, PenCup, StickyNotes | 1,160–5,304; **StickyNotes fails** (12,780 > its 12,000 budget) | props 5–20k | **adapt** |
| `packaged_product_variety` | 10 `PROC_Pkg_*_R3` | 2,296–4,304 | props 5–20k (hero shelf items) | **adapt**: brand/category assignments invented (below) |

### Cross-cutting findings
- **Validation is turned off by design.** Every generator returns `actual_unity_size(objs)` as the expected size, so the runner's size check compares the mesh with itself and can never fail.
  - It hides real errors, e.g. door, flap or shelf parts sticking out.
  - Return the authored envelope from params, and let the validation layer (C5) allow a stated tolerance for segment extrema.
- **"High quality" is not met.** The README claims props 12–30k / fixtures 26–80k / vehicles to 130k, but measured LOD0 is 0.3k–9.8k, below every DEC-084 guide. The params budgets are only ceilings. Segment counts went up, but construction detail did not:
  - cabinet bags are bevelled boxes;
  - the vehicle is one 6-section loft with box windows;
  - no wear, no UV unwraps (box projection only).
- **Collision:** every family emits `COL_*` meshes, which conflicts with DEC-086 (manifest boxes). Convert them.
- **Params keys:** `require_manifold`, `require_material_slots` and `validate_origin_bottom_center` assume runner checks that do not exist; C5 is checklist work. `validate_origin_bottom_center` is `false` everywhere. `require_manifold: true` would fail many assets (touching boxes, open shelves) if implemented as written.
- **Shared files / PROC-005 overlap:**
  - Round 3 needs only `proclib` names that PROC-005 keeps (`add_box`, `add_beveled_box`, `add_cylinder_between`, `finish_object`, `material` with the round-2 alpha default, `rounded_rect`, `loft`).
  - The new `round3_quality.py` duplicates drop 3 helpers (lathe, rotated box, torus) under other names. Fold it into `proclib` when PROC-005 lands its helper set; no second helper module.
  - `unity_dir` lacks `UnityProject/` (S1). No `own_sheet` (S2).
  - PROC-005 had no commits when checked (`claude/clever-lamport-837e7f` = main), so there are no conflicting edits yet.
- **Family overlaps with rounds 1–2** (pick one each, do not ship both):
  - lighting: `back_room_lighting` vs drop 2 architecture kit `LEDTroffer_2x2`/`StripLight`;
  - receipt printer + card terminal: `counter_props` vs checklist R4/RC3;
  - deli prep cart: `office_refill_station` vs checklist O8;
  - cartons/totes: `hub_storage` vs `clutter_kit`;
  - package shapes: `packaged_product_variety` vs `packaged_goods` (+ R5 brief);
  - cooler door preset `Door_##` vs cooler generator names `DoorFrame_nn`.

### Family findings (facts → source)
- **Refill station (DEC-079, RF `Cart_Deli_Prep` 2.5 × 1.6 × 2.9 ft, `Shelf_Deli_Canisters` 3.5 × 0.9 ft at ~4.8 ft AFF, RI §2.4):**
  - Correct: cart (0.72 × 0.50 × 0.92 ≈ RF), shelf (1.02 × 0.27 at 1.48 m ≈ RF) and the DEC-079 supply list.
  - Fix:
    - the deli scale is **light-grey with LCD and coloured keys**, carrying a **clear glass mixing bowl ≈ 8 in Ø** (RI §2.4), not a dark scale with a 0.34 m stainless bowl;
    - add the "FOR DELI USE ONLY" placard (store text) and **spray bottles hung on the rail** (RF);
    - the cart is **2-shelf**;
    - split the wall shelf into its own asset (it is placed on the wall, not on the cart);
    - jar anchors: ~5 empties (RF), house jars per DEC-079.
- **HUB storage (DEC-079: 1 lb bags in storage cabinets against the office wall; ~10 lb shipments of one strain):**
  - Cabinet type, size and colour: **no source** (GAP), so ask REF.
  - Doors are **baked open at 96°**. Ship closed geometry with door parts + hinge metadata (C10) and let Unity animate them.
  - Bags: 1 lb resealable bag shape and size have no source (GAP); fullness states are good.
  - The shipment carton is the ~10 lb case; size GAP.
- **Queue stanchions (DEC-079 one line; R2C1 black belts; RI §1.5 4 lanes):** fine as a form. Sizes are commercial-standard (GAP). Belt colour black ✓.
- **Lighting:**
  - TI §6.7: back-room ACT rooms use **L1 2 × 2 troffers** (not 2 × 4), storage L2 2 ft/4 ft strips; BOH `Light_Strip_Pendant` (RF).
  - The wall pack matches exterior CCTV R1C3; generic housing only ✓.
- **Interaction states:**
  - **CashDrawerTray rejected:** a till tray with bill/coin wells is cash-handling equipment (DEC-051/086), and the cash-drawer asset itself is rejected. Remove the `cash_drawer` state preset.
  - Jar residue: OK; check its colour and look against the real jar photos (DEC-042/043).
  - The cooler preset must use the cooler's real group names.
- **Customer accessories:** sized to a 1.75 m reference. They must fit the **MPFB2** bodies (DEC-087) and belong with the R4 wardrobe library (DEC-091).
  - The ID card is blank ✓.
  - The exit-bag label area carries an approved-brand whitelist ✓.
  - The phone camera island is a consumer phone, not security ✓.
- **Vehicles:**
  - Inside-out body shell (negative volume on all 3).
  - The render reads as a flat blob with a floating box cabin and windshield planes sticking out.
  - All 3 variants are the same topology.
  - **Reject.** Rebuild with real body panels, wheel arches and glazing, or source CC0 vehicles through DEC-023. Exterior CCTV shows parked SUVs/cars (R1C1/R1C2).
- **Counter props:**
  - The receipt printer and card terminal are wanted (RI §2.2, DEC-086).
  - Scale digits must be **blue LCD** (register bench scale, RI §2.2), not green 7-segment.
  - StickyNotes: 45 bevelled sheets break their own budget; use a block + top-sheet detail.
- **Packaged variety: brand misuse.** DEC-071 approves names **for their real lines only**: TFS / Dr Greenthumb / Rebel Grown (house **deli flower**), The Flower Mine (TFS house line, DEC-081), **High Variety = cartridges**, **Tok = disposable vapes**. Round 3 invents product lines for real brands:
  - High Variety preroll tin and beverage can;
  - Rebel Grown jar;
  - Dr Greenthumb edible;
  - TFS topical;
  - Flower Mine extract.

  That is fabricated product data (CLAUDE.md rule). Use fictional BRAND-001 names for non-matching categories. Also: the category `flower_or_edible` is not a catalog category; `unity_dir` writes into the existing `Packaged` folder without the `UnityProject/` prefix.
- **Seasonal decor:** no store evidence of decorations. Keep it as an optional kit; no IP ✓.

### Drop 5 summary
**Adapt overall.** Round 3 hits the briefed families and the DEC-079 refill facts mostly right, and its geometry is deterministic and wound correctly (except the vehicles).

**Fix before integration:**
- the always-pass size validation;
- `COL_` → manifest boxes;
- below-guide detail everywhere;
- brand/category misuse in packaged variety;
- the cash-drawer tray;
- the 2 × 4 troffer;
- duplicate families with rounds 1–2.

**Reject:** vehicles and the cash tray.

> **Superseded (DEC-095):** drop 5 is replaced by the rebuilt round 3 (drop 6 below); its fix list §R3 is replaced by checklist §R3b.

---

## Drop 6 — round 3 rebuilt (`Dispo_Game_Blender_PROC_Round3_Rebuild/`, 2026-10-30 05:53)

**Brief:** DEC-095 (re-audit from scratch; supersedes drop 5 and checklist §R3).
**Judged against:**
- RF; RI §1.5, §2.1, §2.2, §2.4, §6.7;
- DEC-051/079/084/086/091/093;
- `packaged_catalog.json` (DATA-002);
- the canonical PROC-005 core (`claude/clever-lamport-837e7f` @ 87807ad).

Never against the drop's own docs.

**Contents:**
- 10 generators + `round3_common.py`;
- 10 params (30 assets);
- `Data/` (reuse map, interaction states, licences, manifest);
- 4 docs;
- a runner patch (`Patches/run_generator_required_uv_maps.diff`);
- `Audit/audit_round3.py` + `static_audit.json` (121/121 static checks, `blender_runtime_validated: false`).

No `.pyc`. ChatGPT had our drop-5 audit this time (`ROUND3_REBUILD_CLAUDE_AUDIT_CORRECTIONS.md`), but still not RF or RI (DEC-095). So the facts that only RF/RI hold are again missing or wrong.

### How it was checked
- Static read of every `.py`/`.json`/`.md`. `audit_round3.py` was **not run**: it `py_compile`s into the tree (writes `.pyc`) and `rmtree`s every `__pycache__` under its root.
- **Sandbox:** `_sbx_imp003/` inside the worktree holds canonical core 87807ad (`git archive`) plus the drop's generators and params. ROOT = the sandbox (the runner resolves it from its own path). Blender 5.2.3 `--factory-startup`, `sys.dont_write_bytecode`. Sandbox deleted afterwards.
- **(a) Canonical runner as is:** every asset fails (`UV maps [Main, Label, Lightmap]`; the runner wants exactly 2).
- **(b) Runner with the drop's UV patch:** each family stops at its first failing asset.
- **(c) Measuring script:** builds every asset × LOD without the runner and records:
  - tris;
  - the Unity-space bbox vs the returned `expected`;
  - the signed volume of every closed part (inside-out check);
  - open and non-manifold edges;
  - a geometry hash.

  Run twice, plus Workbench renders with back-face culling.

| Family (assets) | LOD0 tris measured | Own `quality_floor_lod0` | DEC-084 guide | Runner (patched) | Verdict |
|---|---|---|---|---|---|
| `refill_station` (1) | 6,328 | 12,000 | fixture 20–80k | fail: LOD3 size (casters dropped) | **adapt** (dims/colour regressions) |
| `hub_storage` (1) | 836 | 12,000 | fixture 20–80k | pass | **adapt** (colour; detail) |
| `queue_stanchions` (1) | 3,116 | 5,000 | props 5–20k | pass | **adopt** form; detail per §R3b |
| `customer_held_props` (4) | 128–608 | 2,500 | props 5–20k | fail: LOD chain, size | **adapt** (optional) |
| `cash_drawer_tray` (1) | 832 | 5,000 | — | fail: LOD chain | **reject** (DEC-051/086) |
| `backroom_lighting` (1) | 164 | 2,500 | props 5–20k | fail: LOD chain | **adapt** (diffuser hidden) |
| `parked_vehicles` (3) | 8,816 each | 12,000 | hero 30–150k | fail: LOD3 size | **reject as built** |
| `seasonal_decor` (3) | 424–1,456 | 3,000 | props 5–20k | Pumpkin pass; others LOD chain | **adapt** (optional, no evidence) |
| `counter_workstation_props` (10) | 116–1,644 | 2,500 | props 5–20k | fail: LOD chain, size | **adapt** |
| `product_variety` (5) | 56–952 | 3,000 | props 5–20k | fail: size | **adapt** (into `packaged_goods`) |

### Cross-cutting findings (measured)
- **X1 Size validation can fail again ✓** (drop-5 R3.0.1 fixed). Every generator returns `expected_from_dims(p)`, and the check now catches real drift: **14/30 assets fail size** in ≥ 1 LOD. Causes:
  - envelope parts dropped at `detail 0`: refill casters (1.72 vs 1.85 m), receipt-printer paper, label tail, weigh-boat sides;
  - cylinders whose segment count is not divisible by 4 miss the radius: water bottle, cup, tincture at LOD2/3;
  - the vehicle roof is under-sampled at LOD3 (1.42 vs 1.46 m);
  - parts that stick out by design: wallet seam −0.001, cone-tube cap 0.52 w, edible-tin lid 0.51 w, the sticky-note sheet offset.
- **X2 LOD chains do not decrease:** 18/30 assets have LODn ≥ LODn−1. LOD1 and LOD2 both use `detail 1`, which only changes round segments. The canonical `check_lod_chain` (Q0.5) fails them.
- **X3 Below every bar:** LOD0 is 56–8,816 tris, **below the drop's own `quality_floor_lod0` on 30/30 assets** and below the DEC-084 guide on 30/30.
  - The README's "manufacturing/construction detail at LOD0" is not met: the 2 × 2 troffer is 164 tris and the rolling papers 56.
  - Nothing reads `quality_floor_lod0`; the canonical key is `tri_guide.lod0_min`.
  - Budgets (18k–150k) are guide maxima only.
- **X4 Runner patch:** the canonical runner (87807ad) still requires exactly `[UVMap_Main, UVMap_Label]`, so 30/30 fail unpatched. The patch (params-driven `required_uv_maps`) is small and correct, but it accepts the drops' order `[Main, Label, Lightmap]`. **DEC-097** fixes the order as channel 0 = Main, **1 = Blender lightmap UV**, **2 = Label**, so the label currently lands where the lightmap should be. Adapt the patch to enforce the DEC-097 order (PROC-007).
- **X5 Lightmap UV is unusable as built:** `_assign_uvs` gives **every triangle its own grid cell** (n = ⌈√faces⌉, 8 % padding). The UVs do not overlap, but every edge is a seam and texel use is tiny, so lightmaps will bleed and show seams.
  - Per DEC-097, Blender exports a dedicated lightmap UV (a real unwrap + pack, PROC-007), and Unity's "Generate Lightmap UVs" stays off.
- **X6 Winding:** **0 inside-out** closed parts across 30 assets × 4 LODs (`recalc_face_normals` in `finish`). The drop-5 vehicle inside-out defect is fixed. One open part remains: `ScaleBowl` (a single surface with a hole in the bottom).
- **X7 Determinism:** geometry hashes are identical across two runs for 30/30 assets × 4 LODs. FBX byte-identity was checked only for the 2 assets the runner exported (hub cabinet, stanchion pair); the canonical exporter pins time and UUIDs.
- **X8 Collision:** no `COL_*` meshes ✓ (DEC-086); boxes come from params. But `parked_vehicles`, `counter_workstation_props`, `customer_held_props` and `product_variety` declare **none**. Vehicles need at least a body box.
- **X9 Params contract:**
  - no `unity_dir`/`own_sheet` (S1/S2); 30 rows would also break the default sheet's 1 MB cap;
  - no `checks` block, so the origin, degenerate and material checks stay off;
  - new `GAP-R3-*` ids instead of `GAP-PROC-*` (P5);
  - material names `M_R3_*` (M4 naming).
- **X10 Helper module again:** `round3_common.py` is renamed, not removed. It duplicates canonical `proclib`:
  - `finish` = `finish_object` + `recalc_face_normals` + lightmap UV;
  - `box` → `add_box`;
  - `cylinder`/`tube` → `add_vertical_cylinder`/`add_cylinder_between`;
  - `rounded_prism` → `rounded_rect` + `loft`/`add_beveled_box`;
  - `pbr` → `material`.

  Only `torus` and `wedge` are new. Its `cylinder` uses `max(8, segments)`, which ignores C11's even-segment rule.
- **X11 The reuse map points at things we do not have.** `Data/canonical_reuse_map.json` and `ROUND3_REBUILD_INTEGRATION.md` call round 4/5/6 families "accepted". They reuse `PROC_Register_CashDrawer`, `_POSMonitor`, `_BarcodeScanner` and `_ScaleStand` plus cooler, carton and tote families.
  - None of these is on main or in PROC-005 (87807ad has the jar, fill, packaged goods and wire-shelving WIP).
  - Rounds 4–6 are not audited yet, and the cash drawer was rejected in drop 2 (DEC-086).
  - Treat the map as a wish list.
- **X12 DEC-093 wording ✓:** the integration doc says live project files win, and calls the package "not an instruction to overwrite". No round-3 file has the name of a canonical file. But `product_variety` again runs parallel to `packaged_goods` in the same `PROC_*Pkg_*` namespace.

### Family findings (facts → source)
- **Refill station:** worse than drop 5 on sourced facts.
  - **Correct:** grey scale ✓ and 8 in (0.2032 m) glass bowl ✓ (RI §2.4).
  - **Scale too big:** the body is 0.285 × 0.265 × 0.105 m vs RI §2.4 ≈ 6–7 × 8 × 3 in (≈ 0.17 × 0.20 × 0.08), about 1.5× too big. It also has no LCD, coloured keys or chrome scoop.
  - **Sizes called unsourced, but RF has them:** the drop's `GAP-R3-REFILL-DIMS` says cart and shelf sizes are unknown.
    - RF `Cart_Deli_Prep`: 2.5 × 1.6 × 2.9 ft (0.76 × 0.49 × 0.88 m), Med.
    - RF `Shelf_Deli_Canisters`: 3.5 × 0.9 ft, wood on black brackets at ~4.8 ft (1.46 m) AFF, Med.
  - **What the drop builds:** cart 0.84 × 0.65 m with its top hard-coded at 0.94 m; shelf 1.20 m wide at 1.85 m; **dark** metal (0.16 grey); **3 tiers**.
  - **The real cart** is **stainless/silver** ("silver rolling cart", DEC-079) with a **flat top + lower shelf** (RI §2.4; RF "2-shelf"), a tubular push handle, a "FOR DELI USE ONLY" label and spray bottles on the rail. All of these are missing.
  - The casters float 6 cm below the legs (render). Cart and wall shelf are again one asset.
  - Supplies are 3 identical bottles. DEC-079 lists isopropyl, rags, scraper, bins and tongs, kept *under* the cart.
- **HUB storage:**
  - **Doors:** closed, with hinge metadata (the drop-5 fix was delivered). The hinge metadata is now moot under the Q6 ruling below.
  - **Colour wrong:** grey steel, but RI §2.1 (HUB 2, R2C1) shows **black cabinets, 2+**, Med.
  - **Presence is sourced:** DEC-079 puts them "in the HUB against the office wall", and HUB 2 is the room that shares the office door (RI §1.4). The drop's GAP says presence is not established; only type, size and shelf count are GAPs.
  - **Lead ruling (Q6):** the backstock cabinets follow the DEC-051 Q9 precedent: **plain black closed cabinets**, with no interior, no stock anchors and no openable doors. So the drop's shelves, anchors and hinge metadata are dropped. Reopen only if Gameplay files a restocking need.
  - **Detail:** 836 tris of plain boxes.
- **Queue stanchions:** black ✓ (R2C1); layout left to placement ✓ (RI §1.5 4 lanes; DEC-079 one line). Sizes are commercial defaults (GAP). Missing detail: no cassette, end clip or rubber foot, and the belt is a plain slab.
- **Back-room lighting:**
  - 2 × 2 ✓ (TI §6.7 L1).
  - **The diffuser is invisible.** The dark `Recess` box (z 0–0.35 h) has the same footprint as the diffuser (z ≈ 0.42–0.54 h) and hides it from below; the render from below shows only the dark recess. So the visible face of the ceiling light is dark grey, and there is no emissive part.
  - **Removed:** the L2 2 ft/4 ft strips (TI §6.7 "storage"), the BOH `Light_Strip_Pendant` (RF, 4.0 × 0.5 × 0.3 ft, Low) and the exterior wall pack (CCTV R1C3), all deferred to "Round 6". All three are sourced, so they must exist somewhere: check round 6.
- **Cash-drawer tray: reject.**
  - The drop says the drop-5 rejection was "quality-related". It was not: DEC-086 rejects the cash-drawer variant, and DEC-051 excludes cash-handling equipment. Bill and coin wells are exactly that.
  - Its parent `PROC_Register_CashDrawer` does not exist (X11).
  - Also remove the `PROC_Register_CashDrawer` target in `Data/interaction_states.json`.
- **Parked vehicles:** inside-out fixed ✓, unbranded ✓, but **reject as built**.
  - **Scope is sourced:** RI §2 R1C1 parked SUV, R1C2 parked cars; DEC-091 R6 has parking in scope.
  - **Shape:** the render is still a capsule, one elliptical loft with no greenhouse/hood/trunk break and no wheel arches.
  - **Glazing inside the body:** side glass at x = 0.405 w vs body half-width 0.446 w; the roof glass sits under the roof surface. Wheels and bumpers stand outside the shell.
  - **Detail:** 8,816 tris vs the 30–150k hero guide.
  - **Fix:** prefer CC0 vehicles through DEC-023, ledgered.
- **Interaction states (`Data/interaction_states.json`):**
  - Deli-jar lid states ✓ (RI §2.4: lids off, laid flat). Add "laid flat" as the rest pose.
  - Carton and cooler entries are metadata only ✓. Bind the cooler after K3 (its group names).
  - The drop-5 jar-residue variant is gone. Fine: no cannabis geometry is needed.
- **Customer held props:** phone, water bottle, cup and wallet. Wearables moved to round 4 ✓ (DEC-091 R4). The item mix has no evidence (GAP, optional). The code has a key-ring branch that no params row uses.
- **Counter / workstation props:**
  - **Sourced:**
    - receipt printer, card terminal and keyboard (RI §2.2: "each POS has a monitor, keyboard, receipt printer and a customer-facing card terminal/tablet", Med);
    - the card terminal is also DEC-086;
    - label/tape items (RI §2.2, Low).
  - **Also sourced:** the mouse and label printer (DEC-096 register workstation kit, which also asks for a spray bottle on the scale shelf and a rag; neither is in the drop).
  - **Unsourced:** glove box, weigh boat, pen and sticky notes. Keep them as generic clutter with a GAP.
  - The drop-5 "blue LCD scale digits" item has lost its home. It belongs on the register scale (RI §2.2: white bench scale, blue LCD) and the refill scale (RI §2.4: LCD).
  - StickyNotes no longer breaks its budget ✓, but now fails its size check.
- **Product variety:**
  - Brand fix delivered ✓: all names are fictional, and no real brand string remains.
  - The **categories are catalog-backed** (`packaged_catalog.json`): DROPPER ×4, BATTERY ×6, ROLLING PAPERS ×7, GUMMY ×158 (the tin), PREROLL (the cone tube).
  - Pack sizes are GAP (`GAP-PROC-10`).
  - Still a parallel generator: port the shapes into `packaged_goods` (R3.0.5).
  - Its `nonduplicate_baseline` metadata lists the very shapes it adds (cosmetic).
- **Seasonal decor:** pumpkin, wreath, garland, plus an unused snowflake branch. No store evidence (GAP); optional; no IP ✓.

### Research gaps, round 3 (our docs lack the evidence too)
- **RG3-1 HUB cabinets:** door count and shelves.
  - **Measured (DEC-110):** graybox `FX_HUB2_Cabinets` = 2 black cabinets on the HUB 2 back wall, a 6.0 × 1.5 ft footprint (x 1.19–7.19, y 47.0–48.5) at the "tall" class of 7.0 ft (Low; GAP-110/120). So the placeholder per cabinet is **3.0 × 1.5 × 7.0 ft** (0.914 × 0.457 × 2.134 m), not the drop's 1.80 × 0.55 × 2.00 m single unit.
  - RF has no HUB entry. CCTV R2C1 (RI §2.1) gives colour and count only.
  - Still open: doors and shelves (R2C1 full resolution).
- **RG3-2 Refill-cart supplies:** bottle, bin and tongs sizes and colours. Look at the lower shelf in `References/Index/photos/deli_jars_scale_cart_crop.webp`; otherwise through the lead/Hub, after the DEC-105/110 search.
- **RG3-3 Stanchion model** (base Ø, post Ø).
  - **Measured (DEC-110):** graybox `stanchion` height class = **3.0 ft** (0.914 m, GAP-002) vs the drop's 1.05 m. The lanes (`FX_QueueLane_1..4`, RI §1.5 vector) run x ≈ 6/9/12/15 ft, so they are **3 ft apart**, each 8.71 ft long (y 11.0–19.71).
  - Use 3.0 ft posts and belt runs fitted to the 8.71 ft lanes, not the drop's fixed 2.0 m pair.
  - Base and post Ø: no source in TI, RF or the game files (CCTV R2C1 is too far).
- **RG3-4 Parked-vehicle mix:** only classes are visible (R1C1/R1C2, night IR). Make and colour cannot be resolved, and need not be: stay generic.
- **RG3-5 Register device sizes** (printer, terminal, keyboard): RI §2.2 gives presence only. The register crops (`References/Index/register/`) may give ratios against the 17.5 in keyboard convention.
- **RG3-6 Package sizes** for dropper, battery, papers, tin and cone (GAP-PROC-10): measure real SKUs, or use the DATA-002 source pages if they list sizes.
- **RG3-7 Troffer recess depth and diffuser type:** the TI E-sheet luminaire schedule (RI §6.7) may name a model; recheck it.

### Drop 6 summary
**Adapt overall:** 1 adopt (stanchion form), 7 adapt, 2 reject (cash tray; vehicles as built).
- **Delivered from §R3:**
  - size validation can fail;
  - no `COL_` meshes;
  - 2 × 2 troffer;
  - no real brands;
  - closed cabinet doors;
  - vehicle winding;
  - StickyNotes budget;
  - wearables moved to round 4.
- **Not delivered:**
  - DEC-084 detail (30/30 below its own floor);
  - usable lightmap UVs;
  - sourced refill sizes and colour (regressed);
  - HUB cabinet colour;
  - the cash tray is back.
- **New defects:**
  - non-decreasing LODs (18/30);
  - size failures (14/30);
  - hidden troffer diffuser;
  - floating casters.

Fix items: checklist §R3b.

---

## Drop 7 — round 4 v2 (`Dispo_Game_Blender_PROC_Round4_HQ_v2_EvidenceDriven/`, 2026-10-30)

**Brief:** DEC-091 R4 (wardrobe, hair and accessory libraries for MPFB2 bodies; staff uniform per DEC-089; crowd LOD baker; ASSET-004 owns the bodies).
**Judged against:** DEC-084/087/089/091/093/096, RI §3 (BAND attire column), DEC-023 (licences), canonical core 87807ad.

**Contents (65 files, 49 MB):**
- 5 generators + `round4_quality.py`, 9 params;
- tools: `mpfb2_fit_adapter.py`, `mpfb2_glove_overlay.py`, `crowd_lod_baker.py`;
- arranger `outfit_variation.py` and its baked outputs `OUTFIT_VARIATIONS_64.json` / `STAFF_STYLE_VARIATIONS_12.json`;
- 30 PBR PNGs (10 materials × BaseColor/Normal/Roughness, 2048²);
- a 4096² TFS chest decal;
- `EVIDENCE_REGISTER.json`, `LOCAL_STYLE_RESEARCH.md`, a UV2 runner patch, `STATIC_AUDIT.json`.

It says it supersedes an earlier `…Round4_HQ.zip`, which is not in the Imports folder.

### How it was checked
- Static read of every `.py`, params and doc; 2 textures and the decal viewed.
- The same sandbox method as drop 6: canonical core 87807ad plus the drop's `Tools/Blender`, Blender 5.2.3 `--factory-startup`, no `.pyc`. The measuring script built all 36 assets × 4 LODs, twice. Renders were made, and the sandbox was deleted.
- The tools and arranger were read, not run: they need an MPFB2 body we do not have in a sandbox.

| Family (assets) | LOD0 tris measured | Budget (LOD0) | DEC-084 guide | Build result | Verdict |
|---|---|---|---|---|---|
| `wardrobe_library` (11) | 1,044–2,632 | 42–80k | close-up character clothing | builds; deterministic | **reject as built** (block garments) |
| `hair_library` (9) | — | — | — | **crashes on every asset and LOD** (`face already exists`) | **reject as built** |
| `headwear_library` (6) | 4,916–13,824 | 39–52k | props 5–20k | builds; **TopButton not deterministic** on 3 caps | **adapt** (best family) |
| `staff_uniform` (4) | 1,384–2,344 | 56–68k | — | builds | **adapt** green tee + pants; **reject** black tee and blue polo as uniform |
| `accessory_extensions` (6) | 668–1,960 (2 that build) | 24–30k | props 5–20k | **Watch, Lanyard, PinLanyard, CrossbodyStrap crash** | **adapt** sunglasses/tote; rest broken |
| tools (fit, glove, crowd LOD) | — | — | — | not run | **adapt** fit/crowd; **reject** glove as built |
| `outfit_variation` + baked tables | — | — | — | not run | **adapt** (dangling assets, staff mix) |
| PBR textures + decal | — | — | 2K–4K | viewed | **adapt** (placeholder-grade; ledger) |

### Cross-cutting findings (measured)
- **X1 Always-pass size check is back.** Every generator returns `actual_unity_size(objs)` (measured from the mesh); this is the exact drop-5 R3.0.1 defect. All 23 assets that build therefore "pass" size trivially.
- **X2 13 of 36 assets crash:**
  - `round4_quality.ribbon_obj` makes "two-sided" cards by adding a second face over the same 4 verts in reverse order, which bmesh rejects. That breaks all 9 hair styles, Lanyard, PinLanyard and CrossbodyStrap.
  - `torus_obj` calls `bmesh.ops.create_torus`, which does not exist in Blender 5.2.3. That breaks Watch.
  - The drop's static audit could not see either (no Blender at ChatGPT).
- **X3 Far below every budget:** the garments are 1–2.6k tris against their own 42–80k budgets. The renders show a **closed box torso with capped cylinder sleeves**: no neck, arm or waist openings, no shell thickness, no folds, seams or hems. These are mannequin blocks, not garments, and cannot be skinned to a rig.
- **X4 No rigging path:** nothing transfers MPFB2 armature weights to garments, hair or accessories. The MPFB2 fit contract lists rig deformation as a local check, but no tool does it. `mpfb2_fit_adapter.fit_garment` shrinkwraps the whole garment to the nearest body surface, which collapses relaxed or oversized fits (hoodie, relaxed tee) onto the skin and removes the variation the drop claims. Add a ease/offset per region plus a Data Transfer of vertex weights.
- **X5 Glove overlay copies the whole body:** `build_glove_from_hand` copies the "hand object" and solidifies it. MPFB2's basemesh is one mesh (hands are not separate objects), so the "glove" is a full-body shell. It needs a hand vertex-group mask, or a CC0 glove proxy.
- **X6 Determinism:** 20/23 building assets are identical across runs. `TopButton` (`bmesh.ops.create_uvsphere` + `finish_object` remove_doubles) differs between runs on StructuredFitted, MeshBackTrucker and CurvedBrimCap. Cause not traced; the canonical "two runs byte-identical" gate will fail.
- **X7 Lightmap UV:** the same per-polygon cell scheme as round 3 (`round4_quality.add_lightmap_uv`). Its own comment says production repacking is left to the local pass. Same decision as R3b.0.4. The UV2 patch is identical in intent to round 3's.
- **X8 Params contract:**
  - `unity_dir: Assets/_Game/...` lacks `UnityProject/` (S1);
  - `validation_warnings` (P3);
  - `GAP-R4-*` ids (P5);
  - `round4_quality.py` is a third helper module (C6/C8, DEC-093).

  Collision: none, owned by the body (`COLLISION_POLICY.md`), which is correct for wearables ✓.
- **X9 Textures:** 2048² as claimed, but placeholder-grade. `knit_basecolor` is plain sine stripes (63 KB), not a knit.
  - They are self-authored and declared CC0 ✓, but there is no sha256 manifest entry in our `LICENSE_LEDGER.md` (DEC-023).
  - Several normal maps are 4–6 MB each; 49 MB for 10 materials.
  - Route them through DEC-023 + the ledger, or replace them with ambientCG/Poly Haven CC0 fabric sets (real scans, the same $0 cost).
- **X10 Dangling references:**
  - `OUTFIT_VARIATIONS_64.json`/`STAFF_STYLE_VARIATIONS_12.json` reference `PROC_R3_Accessory_Glasses` ×6, `_Backpack` ×10 and `_Beanie` ×1. Those were in the rejected drop 5, and the round-3 rebuild removed them ("Round 4 owns wearables"). So **nothing supplies glasses, backpack, beanie or purse**.
  - Every outfit also uses a hair asset that crashes (X2).

### Store / decision findings
- **Staff uniform conflicts with DEC-089:**
  - DEC-089: the real store has no dress code; *for the game*, budtenders wear **black pants + a green tee with "The Flower Shop" at the top right of the chest**.
  - The drop labels that "brief-directed, not footage-confirmed" and adds `ObservedBlackTee` and `ObservedLightBluePolo` as staff variants. **10 of 12 staff presets** use them (7 polo, 3 black tee); only 2 use the DEC-089 uniform.
  - Its evidence is real (RI §3 BAND 05/12: black TFS tee + lanyard; 01/03/07: polo), but DEC-089 is the decision. The black tee and polo may be **customer/off-shift wardrobe**. As staff presets: reject.
  - RI §3 says BAND 01's polo is **teal**, not light blue.
- **Decal side:**
  - `staff_uniform._add_decal(side='right')` puts the decal at +X. With the asset facing −Y (label faces −Y, PROC contract), +X is the **wearer's left** (the viewer's right), while the metadata says `decal_side_wearer: right`. One of the two is wrong.
  - DEC-089's "top right of the chest" does not say whose right. **Pending a World REF look at BAND 05/12** (handoff Q8). Placeholder `GAP-CHR-PRINT-SIDE`: wearer's left chest.
  - The decal box also gets no `UVMap_Label` mapping (no `label_rect`), so the 4096² texture would not land on it.
  - The decal is white DejaVu-style bold text on a square canvas, with the text filling ~10 % of the height. The font licence is not recorded; DEC-023 allows OFL/CC0/MIT.
- **Brands:** the only real brand is The Flower Shop text on staff tees (DEC-071/089 ✓). Headwear and other wear are unbranded ✓ (fictional patch carriers).
- **Local-style research:** the anti-stereotype rules are good and match DEC-087(4) (no behaviour or stats tied to appearance) ✓.
  - The "rougher neighborhood" premise is attributed to "the user". Our docs have no such statement, so it is ChatGPT-chat context, not a repo fact.
  - The web pages (Manor PHX, NWS) are reference-only and nothing is bundled ✓. The store address on the TFS site is public.
  - Keep the weights as art direction only; never as a demographic model.
- **Privacy:** the evidence register lists BAND photo observations of identifiable staff (hair types, eyewear). RI §3 already records attire categories at the same level, and no likeness is built ✓. Do not copy the per-photo, per-person notes ("long locs visible on second worker") into game data.
- **DEC-084:** headwear is the only family near the props guide (5–14k): crown panels, visor, closures, button. Everything else needs real garment construction, or (recommended) **MPFB2/MakeHuman system clothes and hair**: CC0 assets that already fit and rig to the MPFB2 basemesh (verify each asset's licence through DEC-023). Our own procedural garments should then only add the DEC-089 uniform print and the store-specific items.

### Research gaps, round 4
- **RG4-1 Uniform print side and size:** DEC-089 "top right of the chest" (wearer or viewer?). Look at BAND 05/12 (black TFS tee) for the real print position, size and font. That is evidence for the print only, not the colour.
- **RG4-2 Garment source:** which MPFB2/MakeHuman system clothes and hair are CC0 and rig-compatible with ASSET-004's bodies. Check the MPFB2 asset packs' licence files (ASSET-004 owner).
- **RG4-3 Uniform font:** TFS brand typeface. Look at TFS signage in RI (BAND 05 neon, the logo living wall R2C2). Otherwise use an OFL stand-in.
- **RG4-4 Polo colour:** teal (RI §3 BAND 01) vs light blue (drop). Only matters if it is kept as customer wardrobe.

### Drop 7 summary
**Adapt overall, weakest drop so far on execution:** 13/36 assets crash, the size check is always-pass again, and the garments are blocks.
- **Adopt:** the anti-stereotype rules; headwear forms; the evidence-category approach; the deterministic outfit arranger pattern (seeded, hashed).
- **Adapt:** headwear (determinism, collision n/a); green tee + black pants (DEC-089; fix the decal side and UV); sunglasses and tote; the fit adapter (weights, per-region ease) and crowd baker; textures (ledger or replace).
- **Reject as built:** wardrobe blocks, hair (crash), ribbon accessories and watch (crash), glove overlay, and staff black tee / blue polo as uniform presets.
- **Counts:** adopt 1 (arranger pattern + rules) · adapt 6 · reject 5. Fix items: checklist §R4.

---

## Drop 8 — round 5 (`Dispo_Game_Blender_PROC_Round5_HQ/`, 2026-10-30)

**Brief:** DEC-091 R5 (packaging families, 1 lb deli bags, exit bags, label art system, stocking arrangers).
**Judged against:**
- `packaged_catalog.json` (DATA-002);
- DEC-071/079/081/084/093/096;
- `Docs/Research/AZ_COMPLIANCE.md` §D5/E1;
- canonical core 87807ad + `packaged_goods` on main.

**Contents (106 files, 9 MB):**
- 2 generators (`round5_packaging` 14 assets, `deli_supplies` 4) + `round5_common.py`;
- tools: `label_art.py` (Pillow renderer), `stocking_arranger.py`, `generate_round5_textures.py`;
- 3 label PNGs (4096²) and ~80 PBR PNGs;
- a UV2 patch (the same as round 3/4);
- `validation/static_audit.py` + outputs.

The README says the stocking sample is synthetic and must not be read as store evidence ✓.

### How it was checked
- Static read; the Tok label and a bag render viewed.
- Sandbox as for drops 6–7: 87807ad core + `Tools/Blender` + `Art/Source/Procedural/Round5` (textures load by relative path). All 18 assets × 4 LODs measured twice; sandbox deleted.
- `label_art.py`, `stocking_arranger.py` and `static_audit.py` were read, not run.

| Family (assets) | LOD0 tris | Budget | DEC-084 guide | Build | Verdict |
|---|---|---|---|---|---|
| `round5_packaging` (14) | 228–1,496 | 60k | props 5–20k (hero items) | all build; deterministic; 0 inside-out; size fail 6/14 at LOD1–3; LOD3 not lower on 7 | **adapt** (port into `packaged_goods`) |
| `deli_supplies` (4) | 72–420 | 32k | props 5–20k | all build; deterministic | **adapt** |
| `label_art.py` + label PNGs | — | — | 2K–4K | viewed | **adapt** (data from catalog, AZ fields) |
| `stocking_arranger.py` | — | — | — | read | **adapt** (anchors from RF/arranger contract) |
| PBR textures | — | — | 2K | listed | **adapt** (ledger, DEC-023) |

### Findings
- **X1 Size check is real again ✓, with one exception.** Generators return authored dimensions. Exceptions: `deli_supplies._bag` returns the measured profile depth `actual_d`, and the bottle returns `diameter * 1.02`, a fudge.
  - Failures: can, concentrate jar and topical jar at LOD1–3; bottle at LOD2; preroll tube at LOD3. The lathe profiles lose their widest ring at low detail.
  - Also: the exit bag's measured depth 0.085 m vs its `size_m` depth 0.1016 m passes only because of `actual_d`.
- **X2 Collision key mismatch:** boxes are emitted under `extra["collision"]["boxes"]`. The canonical runner reads `collision_boxes` (DEC-086 C1), so **no collider reaches the manifest**. Rename the key.
- **X3 Far below DEC-084:** LOD0 is 72–1,496 tris against a 60k budget. The cartons are 228-tri bevelled boxes with no glue flap or tuck detail, and the bags are gusseted boxes. The `detail` float scales segments only, so 7/14 LOD3 = LOD2 (cartons/pouches at 64 or 112 tris).
- **X4 Bag states:**
  - Full vs partial are different meshes ✓, but both keep the full 13 × 15 in envelope. "Partial" should drop the fill line and slump the top.
  - The 1 lb size is a market reference (13 × 15 + 6 in gusset), flagged provisional ✓; DEC-079 gives no size (RG5-2).
  - `contains_flower_geometry: false` ✓.
- **X5 Brands/categories vs the catalog ✓** (better than every earlier round):
  - High Variety 1 g 510 cart = catalog HIGH VARIETY / VAPE / 510 THREAD (14 rows);
  - Tok 2 g AIO = catalog ToK / VAPE / READY TO USE (9 rows, all "… AIO 2G");
  - everything else is fictional ("Copper Mesa Labs": not found in our docs or the catalog).
  - The strain names on the labels ("ATHEN'S HAZE", "ATOMIC POP") **are real catalog rows**.
  - But High Variety also has 11 READY TO USE (AIO 2G) rows that are not covered. Display spelling "TŌK" vs catalog "ToK" (use the catalog form unless DEC-071 says otherwise).
- **X6 Invented label data** (CLAUDE.md: never invent inventory data):
  - "THC 90.0 %", "THC 78.4 %", "LIQUID DIAMONDS", "CURED RESIN", "DUAL MODE" are not in the catalog. The catalog has `thcMg`/`cbdMg`/`sizeG`, not %.
  - The fictional edible label prints "THC 72.6 %" on a "10 servings" edible. Edibles are labelled in mg, ≤ 10 mg/serving, ≤ 100 mg/package (AZ_COMPLIANCE E1).
  - `label_art.py` must take every field from a catalog row (DATA-002); nothing hard-coded.
- **X7 AZ label content:** AZ_COMPLIANCE §D5 (R9-18-310) lists licence #, strain, batch, form, weight, total THC/CBD, the warning, ingredients and a QR code. The template has strain, batch, form, weight and a warning, but **no licence #, CBD, ingredients or QR placeholder**, and its warning wording is its own. The universal symbol is not in §D5 as quoted (check the full row).
- **X8 Label art:**
  - DejaVu Sans via Pillow (system path `/usr/share/fonts/...`, else `load_default`), so the output depends on the machine's fonts and is not reproducible on Windows. Bundle an OFL font and record it (DEC-023).
  - Labels are 4096² squares, while the label rects are 0.037 × 0.071 m etc.: stretched, unless rendered at the rect aspect (the round-2 B4 finding again).
- **X9 Stocking arranger:**
  - Placement-only ✓, seeded ✓, AABB clipping ✓.
  - Anchors must come from RF fixtures and the per-room jar/shelf counts (DEC-079 jars per strain).
  - Density must follow DEC-096 playtest feedback ("over-full shelving"), and stock must come from DATA-002 (arranger H3: no random fill as inventory).
- **X10 Params/helpers:**
  - no `unity_dir`/`own_sheet`/`checks`; `GAP-R5-*` ids;
  - `round5_common.py` is the 4th helper module;
  - `upgrade_target` names (`PROC_Pkg_VapeCartBox`, `…EdibleBag`, `…ExtractJar` …) must be checked against the canonical `packaged_goods` variants (DEC-093: port into it, one family).
- **X11 Textures:** ~80 self-authored PNGs, 2K, CC0 claimed. As in round 4, register them in `LICENSE_LEDGER.md` with sha256 or replace them with CC0 scans. The label PNGs carry real brand names (approved) and must be regenerated from data anyway (X6).

### Research gaps, round 5
- **RG5-1 Product sizes:** the Tok 2 g AIO envelope 76 × 38 × 13 mm is marked "authoritative" by the drop, but our docs have no source for it. Verify on the ToK product page or a physical unit; likewise the HV cart and cartons (GAP-PROC-10).
- **RG5-2 1 lb backstock bag:** type, size and closure (DEC-079 gives only "1 lb bags"). Look at RI §2.1 HUB 2 (black bags on shelves) and the office crop; or ask in the next batched question round.
- **RG5-3 Exit bag:** RI §3 BAND 05 ("kraft bags hung on the shelf") and DEC-043 ("branded paper bags") say **paper/kraft**. The drop's exit bag is an opaque resealable pouch: check which bag is the exit bag (child-resistant exit bag vs kraft carry bag).
- **RG5-4 AZ label layout:** the full R9-18-310 field list and the universal symbol; AZ_COMPLIANCE §D5 is the start.

### Drop 8 summary
**Adapt overall: the best-aligned drop on facts.** Real brands sit only on their catalog categories, real catalog strain names are used, the synthetic-anchor warning is explicit, and every asset builds deterministically.
- **Open:** DEC-084 detail (72–1.5k tris); the collision key; low-LOD size failures; invented THC %/product-line text; missing AZ label fields; the system-font dependency; the exit-bag material.
- **Counts:** adopt 0 · adapt 5 · reject 0. Fix items: checklist §R5.

---

## Drop 9 — round 6 (`Dispo_Game_Blender_PROC_Round6_HQ/`, evidence-revised, 2026-10-30)

**Brief:** DEC-091 R6 (architectural detail kit, retail/back-room light fixtures, UV2 readiness, wear decals, signage, exterior storefront/parking/desert landscaping as params).
**Judged against:** RI §2 (CCTV wall), §6.1 ceilings, §6.2 doors, §6.5 finishes, §6.7 lighting, §6.8 A011/A012; RF; canonical core 87807ad.

**Contents (149 files, 7.6 MB):**
- 5 generators (37 assets) + `round6_common.py`;
- ~130 self-authored PNGs (textures, 4 wear decals, 4 sign arts incl. `Sign_TFS.png`);
- `generate_round6_art.py`;
- `validation/STORE_EVIDENCE.json` + static audit.

This time ChatGPT had **A012** and two camera stills. It adopts an "evidence-first" rule: every item carries `store_evidence_status`, and unproven items default to `disabled_reference` ✓ (the right idea).

### How it was checked
- Static read.
- Sandbox as for drops 6–8: 87807ad + `Tools/Blender` + `Art/Source/Procedural/Round6`. All 37 assets × 4 LODs measured twice; sandbox deleted.

| Family (assets) | LOD0 tris | Budget | Build / size | Verdict |
|---|---|---|---|---|
| `architectural_detail` (10) | 20–704 | 80k | builds; **size check fails 10/10** (axis order); CornerGuard **inside-out** | **adapt** |
| `lighting_fixtures` (10) | 72–16,168 | 90k | size fails 10/10; CheckoutCluster and Pendant **not deterministic** | **adapt** |
| `signage` (4) | 220–396 | 60k | size fails 4/4; LOD0 = LOD3 | **adapt** (optional) |
| `exterior_site` (9) | 28–308 | 120k | size fails 9/9; LOD0 = LOD3 on most | **adapt** (sourced sizes below) |
| `desert_landscaping` (4) | 608–7,948 | 150k | size fails 4/4 (real mismatches) | **adapt** (presence GAP) |
| textures/decals/sign art | — | — | listed | **adapt** (ledger) |

### Findings (measured)
- **X1 Axis-order bug: 37/37 fail the canonical size check.**
  - Generators return `(w, d, h)` (Blender X/Y/Z); the runner compares against the Unity-ordered bbox `(w, h, d)`.
  - After swapping, **20/37 match** and **17/37 still miss** their declared dims: the agave is 0.45 m wide vs 1.05; the pendant globe 0.096 vs 0.2; the checkout cluster 0.50 × 0.47 × 0.51 vs 0.62 × 0.72 × 0.62; the door lever 0.15 vs 0.20; the downlight and recessed can are short; the A-frame depth 0.32 vs 0.62; and so on.
- **X2 Determinism:** CheckoutCluster and Pendant_Globe differ between runs. Both use `bmesh.ops.create_uvsphere`, the same primitive as round 4's non-deterministic TopButton.
  - Conclusion across drops 7 and 9: **avoid `create_uvsphere` in generators**; use a lathe (`add_lathe`) for spheres.
- **X3 Winding:** `CornerGuard_90` (20 tris) is inside-out. All other closed parts are fine.
- **X4 Below DEC-084:**
  - LOD0 is 20–704 tris for everything except the checkout cluster (16k), palo verde (5.6k), shrub (3.6k) and gravel (7.9k).
  - Many assets have LOD0 = LOD3 (signage, storefront, stall, stripe, sidewalk), so the canonical LOD chain fails.
  - The 2 × 2 ACT light is 136 tris, the 2 × 4 troffer 196.
- **X5 Collision key:** `collision.boxes` again (as round 5), so nothing reaches `collision_boxes`.
- **X6 Helper module 5** (`round6_common.py`, also seeded `random`), `GAP`/params gaps as before, and UV2 per R3b.0.4.

### Store-evidence findings (our docs vs the drop's evidence reading)
- **Floors contradict the TI (High) and CCTV:**
  - The drop reads both stills as **wood-look plank flooring**, a **dark blue accent wall** and **light** counters/casework.
  - Our sources:
    - retail floor TL-1 marble-look porcelain + TL-2 "Madrid" patterned tile;
    - back rooms VCT-1 12 × 12 in; storage CONC-1 sealed concrete (RI §6.5);
    - CCTV R2C1 "white marble-look tile + black/white geometric cement tile";
    - HUB "gray square floor tile / dark floor" (RI §2.1);
    - counters **black** (RI §2.4, DEC-043);
    - wall behind displays **teal** WC-1 (RI §2.4/§6.5).
  - Either the drop's stills are not this store (compare RI §6.9: a "Flower Shop" TI set that is *not this store*), or they are mis-read. **Its finish observations must not be used.** Use RI §6.5.
- **Items it disables that our docs confirm:**

  | Drop item (`disabled_reference`) | Our evidence |
  |---|---|
  | Strip 4 ft | TI §6.7 **L2 2 ft/4 ft strip (storage)**, High; RF `Light_Strip_Pendant` BOH |
  | Wall pack | CCTV **R1C3 "wall packs"** (RI §2) |
  | Ceiling grid (2 × 4 module) | ACT-1 **2 × 2 lay-in** in 102–107 at 8'-0" (RI §6.1, High), so **2 × 2**, not 2 × 4 |
  | Outlet/switch plates | RI §6.5: white on white walls, **matte black on finished walls**; switches 3'-6" AFF (§6.2) |
  | Door lever | TI A310 lever hardware, centreline 3'-4"–3'-6" (RI §6.2), on HM doors (no lock or access-control detail, DEC-051) |
  | Storefront glazing + entry door | E101 **6'-0" × 7'-0" aluminium full-glass storefront pair** (RI §6.2/§6.8, High). The drop's door is a 1.02 × 2.13 single leaf: use two 3'-0" × 7'-0" leaves (0.914 × 2.134) |
  | Parking stall / stripe / curb | CCTV R1C2 "parked cars, striping"; R1C3 "**yellow curb**", dark-green privacy fence/gate (RI §2) |
  | Exit sign | ✓ already enabled (R2C1 exit sign) |

- **Door kit vs DEC-110** (World contract `Docs/Reference/DOORS.json` + CF §7.1):
  - **No push bar / exit device at all.** Three doors need one: DOORS.json `Emergency_RetailE`, `Ext_Emergency_SE` and `Ext_Delivery`.
  - **The entry door's `PullHandle`** (`exterior_site.py` l.24) is correct: DOORS.json `Entry` has `hardware: storefrontPull`.
  - The only lever is `DoorLever_Commercial`; its size misses its dims (X1).
  - **Caution:** main's DOORS.json still has the `JC` and `Ext_Delivery` hardware swapped (the World fix is pending), so bind to the corrected ids.
- **Missing TI lighting types:** L3 linear LED (recessed in millwork), L5 small flush mount, L6 bathroom sconce, L7 task, L8 18 in under-cabinet (TI §6.7). Also missing: the retail **CLG-1 suspended 4 × 8 ft dark-walnut acoustic panels** on stainless cable (RI §6.1), the "dark baffle ceiling" in BAND 01/05/10. Retail ceiling: painted gypsum at 9'-0", soffits at 7'-6" (RI §6.1).
- **Pendants:** the globe-pendant cluster matches CCTV R2C2 "globe pendant cluster" ✓; checkout counter light is a plan type ✓ (A012). Counts and sizes are GAP.
- **Baseboard:** 0.102 m (4 in) matches VB-1 **grey vinyl base 4 in** ✓; set the colour to grey (VB-1).
- **Signage:**
  - `Sign_TFS.png` carries the approved brand ✓ (DEC-071).
  - Store signage we know: the "Fine Cannabis" white neon (BAND 05); the logo living wall (R2C2); the "THURSDAY" daily-deals sheet (BAND 10); the 3 × 3 video wall (R2C2); the required licence and pregnancy-warning signage at entry (AZ_COMPLIANCE G2). Use those instead of a generic A-frame and menu board.
- **Landscaping:** the agave, palo verde and shrub are generic Phoenix species. Exterior CCTV (R1C1–R1C3) shows a sidewalk, curb, lot and fence; no planting is recorded (RG6-3).
- **A012 room areas** in the drop match RI §1.3/§6.8 (e.g. HUB 818.53, HUB 2 541.34) ✓. The plan's "access controlled door" label is recorded without modelling any hardware ✓ (DEC-031).

### Research gaps, round 6
- **RG6-1 The drop's two camera stills:** identify them (file names are not in the package); if they are this store, reconcile them with RI §6.5.
- **RG6-2 Light counts and sizes:** pendants, checkout cluster, L4A/L4B downlights. RCP A101 positions (RI §6.1) could give counts.
- **RG6-3 Exterior planting and storefront sign band:** exterior CCTV R1C1–R1C3 at full resolution; a public street view is not in our sources and should not be used without a ruling.
- **RG6-4 HVAC diffusers/returns, sprinklers:** the TI M/FP sheets are not indexed (RI §6 covers A/E only).

### Drop 9 summary
**Adapt overall.** The evidence-first metadata is a real improvement.
- **But:** every asset fails the size check (axis order), 17 also miss their dims, 2 are non-deterministic, 1 is inside-out, and most are 20–700 tris.
- **Its evidence reading of floors and finishes contradicts our TI (High) and CCTV.**
- **It disables 8 families our docs confirm**, including the round-3 strips and wall pack (R3b.4).
- **Counts:** adopt 1 (evidence-status metadata pattern) · adapt 6 · reject 0. Fix items: checklist §R6.
