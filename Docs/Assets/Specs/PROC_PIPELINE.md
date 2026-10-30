# PROC_PIPELINE — headless procedural props (PROC-001)

Blender 5.2.3 LTS, headless only (DEC-007). Parameter JSON in, Unity-ready FBX + manifest out.

## Run
```powershell
Tools/Blender/blender.ps1 deli_jar      Tools/Blender/params/deli_jar.json
Tools/Blender/blender.ps1 package_base  Tools/Blender/params/package_box.json
Tools/Blender/blender.ps1 package_base  Tools/Blender/params/package_pouch.json
Tools/Blender/blender.ps1 contact_sheet   # after the generators; reads the manifest + renders
```
The wrapper calls `blender --background --factory-startup --python-exit-code 10 --python Tools/Blender/run_generator.py -- <args>`.
Any generator or validation failure exits non-zero. Override the exe with `$env:BLENDER_EXE`.

## Files
| Path | Role |
|---|---|
| `Tools/Blender/run_generator.py` | entry point: build each LOD, validate, export FBX, update manifest, render previews, contact sheet |
| `Tools/Blender/proclib.py` | rounded-rect loops, ring lofting, UV maps, stats/geometry hash |
| `Tools/Blender/generators/<name>.py` | `build(params, lod) -> (objects, expected_size, extra_manifest_fields)` |
| `Tools/Blender/params/*.json` | the only place dimensions live, one file per asset, each placeholder tagged with a GAP id |
| `Art/Exports/Procedural/<asset_id>.fbx` | one FBX per asset, all LODs inside |
| `Art/Exports/Procedural/manifest.json` | per asset: tris per object and LOD, sizes, UV maps, geometry and export hashes, params hash, GAPs |
| `Artifacts/Renders/<asset>_<LOD>_<view>.png` | previews (gitignored) |
| `Docs/Assets/Specs/PROC_contact_sheet.png` | committed sheet. Rows top to bottom: DeliJar, PackageBox, PackagePouch. Columns: LOD0 front, LOD0 side, LOD1 front. The grey cube is 10 cm |

Deli jar parts (DEC-042/043): `Glass`, `Lid` (pop-top with recessed button), `Band` (coloured base sleeve; its front face has `UVMap_Label` 0..1 for the brand print; colour is a per-brand material param at runtime), `Label` (strain/brand card) and `ThcTag`, each a quad with `UVMap_Label` 0..1. Every part has an `enabled` flag, so a second jar type (house smalls, DEC-042a, REF-007) is just another params file for `deli_jar`; point `jar_fill.json` `jar_params` at it for its fill.

New generator: add `generators/<name>.py` with `build()`, add a params file, run. Nothing else to register.

## Export conventions
- Meters, 1 Blender unit = 1 Unity unit (`FBX_SCALE_ALL`). +Y up and transforms baked (`bake_space_transform`), so objects import with identity rotation/scale. A Blender re-import shows meshes Y-up at scale 1.
- Origin = bottom centre of the asset (sits on a shelf at y=0).
- The front/label side is Blender -Y, which should land on **Unity +Z** (object forward). Check this on the first Unity import (the import task).
- Object names are `<asset_id>_<Part>_LOD<n>`. Unity's FBX importer builds the LODGroup from the `_LOD<n>` suffix.
- UV maps on every mesh: `UVMap_Main` (UV0) is a box projection where 1 UV unit = 1 m, for tiling materials. `UVMap_Label` (UV1) maps the params label rectangle on the front face to 0..1. Every other face gets (-8,-8), so a clamped/masked label shader shows nothing there. The jar label is its own card mesh (`Label`, 0..1).
- Triangulated, flat/smooth split at 40°, one material slot per part (`M_Proc_*`, preview colours only).
- Deli jar manifest `interior` gives the cavity (floor y, top y, inner x/z) for the inventory fill-level system (ASSET_PRODUCTION_PLAN §8 DeliJar `FlowerVolume`).

## Triangle budgets (whole asset per LOD; validation fails above these)
| Asset | LOD0 budget / actual | LOD1 budget / actual | Why |
|---|---|---|---|
| PROC_DeliJar (glass+lid+band+label+THC tag) | 1000 / 776 | 250 / 216 | 200+ jars on the walls; the visual cost belongs to the bud fill, not the container (raised from 800/200 for the DEC-042 band + pop-top button) |
| PROC_PackageBox (body+lid) | 300 / 88 | 60 / 24 | hundreds of SKUs on racks; silhouette is a box |
| PROC_PackagePouch | 500 / 476 | 120 / 116 | the curved gusset needs rings; raise `around`/`rings` only together with the budget |

## Determinism
Two full runs give byte-identical FBX, manifest and contact sheet (sha256 checked). The stock FBX exporter writes `now()` into the header and makes node UUIDs from Python's salted `hash()`. `export_fbx()` pins both: a fixed 2026-01-01 timestamp and a sha256-based hash. This is marked as a shortcut in the code.

## Placeholders (no measured dimensions exist; tracked in the params files)
| GAP | What | Evidence |
|---|---|---|
| GAP-PROC-01 | deli canister 0.15 × 0.15 × 0.28 m body, r 18 mm, 4 mm wall | shape: DEC-042/043 photos (tall square clear acrylic, white pop-top, coloured base band, label card + THC % tag). Size estimated from the photos (height ≈ 2× width) and 454 g; REF-007 will measure |
| GAP-PROC-02 | pop-top lid 35 mm, 2 mm overhang, white, 90 mm recessed button | DEC-042/043 photos, no measurement |
| GAP-PROC-03 | label card 100 × 80 mm at 65 mm; THC % tag 45 × 28 mm | DEC-043 retail photo, no measurement |
| GAP-PROC-09 | base band 55 mm tall, 2.5 mm proud; colour per brand (default green) | DEC-043 retail photo, no measurement |
| GAP-PROC-04 | box 65 × 25 × 100 mm, 20 mm lid | none: conventional carton |
| GAP-PROC-05 | pouch 100 × 150 mm, 40 mm gusset, 15 mm seal | none: conventional stand-up pouch |
| GAP-PROC-06 | package label rectangles | none |

Replacing a placeholder: edit the params JSON, rerun, and the manifest hashes show what changed.

## Jar fill / buds (PROC-002)
```powershell
Tools/Blender/blender.ps1 jar_fill Tools/Blender/params/jar_fill.json   # 6 FBX, also copied to Unity
Tools/Blender/blender.ps1 contact_sheet jar_fill                         # Docs/Assets/Specs/PROC_jar_fill_contact_sheet.png
```
- One params file, many assets: a generator may expose `variants(p)` (asset id, params) and `run_generator` builds each. `unity_dir` in params copies the FBX into the Unity project. `preview_context(p)` adds render-only scenery (the jar glass); `preview_groups` renders one tile per part.
- Assets `PROC_JarFill_<Look>.fbx`, looks = ASSET_PRODUCTION_PLAN §8: GreenDense, GreenAiry, PurpleHeavy, OrangePistil, Frosty, DarkCompact. Unity copy: `Assets/_Game/Art/Procedural/JarFill/`.
- Objects `PROC_JarFill_<Look>_F<pct>_LOD<n>`, pct ∈ 0, 10, 20, 40, 70, 100. Same origin as `PROC_DeliJar` (bottom centre), so the fill drops into the jar at identity. F000 (SOLD OUT) is a few shake crumbs at LOD0 only. Unity builds one LODGroup over all steps; the game enables one step's renderers.
- The opaque base band hides the bottom 55 mm from the front, so F010 reads as empty from the front and shows only from above (realistic).
- Cavity comes from `deli_jar.json`; every vertex is ≥1 mm inside the glass (the generator fails otherwise). Buds sit on a 3×3 lattice, 7 layers; a step holds round(pct × 63) buds in seeded order, so lower steps are subsets of higher ones. Centre-column buds with a bud above are culled (hidden).
- LOD0: icosphere-2 buds (80 tris) + shake; LOD1: icosphere-1 buds (20 tris); LOD2: one rounded column (28 tris). Two material slots: `M_Proc_Bud_<Look>` + `M_Proc_BudAccent_<Look>` (pistils/purple/frost). LOD2 has only the first slot.
- Contact sheet rows (top→bottom): DarkCompact, Frosty, GreenAiry, GreenDense, OrangePistil, PurpleHeavy. Columns: F000…F100 LOD0, then F100 LOD1, F100 LOD2. Tiles at half size.

| Budget (per visible step) | LOD0 | LOD1 | LOD2 |
|---|---|---|---|
| step budget / worst actual (F100) | 5000 / 4560 | 1400 / 1140 | 40 / 28 |
Why: ~77 jars on the wall; buds are procedural stand-ins for the §22 scan-baked buds, which can replace the blob in `jar_fill.blob()` later at the same budgets.

| GAP | What |
|---|---|
| GAP-PROC-07 | bud size/shape/colour per look: procedural placeholders; the catalog has no per-strain look data |
| GAP-PROC-08 | fill height is linear in grams (full = 7 layers ≈ 0.25 m); no measured fill height of a real 1 lb jar |
