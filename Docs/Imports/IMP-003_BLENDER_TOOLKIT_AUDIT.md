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
