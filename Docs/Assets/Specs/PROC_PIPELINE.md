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
| PROC_DeliJar (glass+lid+label) | 800 / 442 | 200 / 122 | 200+ jars on the walls; the visual cost belongs to the bud fill, not the container |
| PROC_PackageBox (body+lid) | 300 / 88 | 60 / 24 | hundreds of SKUs on racks; silhouette is a box |
| PROC_PackagePouch | 500 / 476 | 120 / 116 | the curved gusset needs rings; raise `around`/`rings` only together with the budget |

## Determinism
Two full runs give byte-identical FBX, manifest and contact sheet (sha256 checked). The stock FBX exporter writes `now()` into the header and makes node UUIDs from Python's salted `hash()`. `export_fbx()` pins both: a fixed 2026-01-01 timestamp and a sha256-based hash. This is marked as a shortcut in the code.

## Placeholders (no measured dimensions exist; tracked in the params files)
| GAP | What | Evidence |
|---|---|---|
| GAP-PROC-01 | deli jar 0.15 × 0.15 × 0.28 m, r 18 mm, 4 mm wall | shape only: REFERENCES_INDEX photos 01/07/11 (square clear acrylic, lidded). Photo 07 is the only size cue (Low) |
| GAP-PROC-02 | jar lid 30 mm, 4 mm overhang, black | lids visible on the shelves, no measurement |
| GAP-PROC-03 | jar label card 100 × 120 mm, 30 mm up | white card on the front in photo 07 |
| GAP-PROC-04 | box 65 × 25 × 100 mm, 20 mm lid | none: conventional carton |
| GAP-PROC-05 | pouch 100 × 150 mm, 40 mm gusset, 15 mm seal | none: conventional stand-up pouch |
| GAP-PROC-06 | package label rectangles | none |

Replacing a placeholder: edit the params JSON, rerun, and the manifest hashes show what changed.
