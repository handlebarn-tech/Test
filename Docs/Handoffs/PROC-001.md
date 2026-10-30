# PROC-001 handoff — Blender headless pipeline + first generators

**Status:** done, validation passed. Branch `claude/task-proc-001-38ca78`. Nothing written to `UnityProject/` or `Tools/Studio/`.

## Delivered
- `Tools/Blender/blender.ps1 <generator> <params.json>` (+ `contact_sheet`) runs `blender -b --factory-startup --python-exit-code 10 -P`. It exits non-zero on failure; a forced API error was seen to exit 1.
- Generators: `deli_jar` (rounded-square acrylic canister with wall/floor thickness, slip lid, front label card) and `package_base` (`shape: box` with optional telescoping lid, or `shape: pouch`, a stand-up gusseted bag). Both take parameters for dimensions, lid, label rect and LOD segment counts.
- Outputs: `Art/Exports/Procedural/{PROC_DeliJar,PROC_PackageBox,PROC_PackagePouch}.fbx` + `manifest.json`. Committed contact sheet: `Docs/Assets/Specs/PROC_contact_sheet.png` (607 KB).
- Spec: `Docs/Assets/Specs/PROC_PIPELINE.md` covers conventions, budgets, determinism and GAPs.

## Validation (run 2026-10-29)
- All four commands ran headless from a clean `powershell -NoProfile` with exit 0.
- Tris (budget): DeliJar 442 (800) / 122 (200); Box 88 (300) / 24 (60); Pouch 476 (500) / 116 (120). The runner fails the run when a budget is exceeded.
- In-run checks: identity transforms, UV maps exactly `UVMap_Main`,`UVMap_Label`, and bbox matching the params within 0.1 mm.
- Determinism: two full runs gave byte-identical FBX, manifest and contact sheet (sha256). The FBX header timestamp and the salted-`hash()` UUIDs are pinned in `export_fbx()`.
- FBX re-import in Blender: meters, scale 1, Y-up mesh data, both UV maps present.

## Not verified / for the import task
- No Unity import was done (not owned). Still to confirm in Unity: the label side lands on +Z, the `_LOD<n>` LODGroup auto-setup works, and 1 m = 1 unit.
- The jar glass is a single closed shell with no transparency setup. The fill-volume/bud system is not built; the manifest `interior` gives its cavity.
- The contact sheet has no text captions. Row and column order is documented in PROC_PIPELINE.md.

## For the Hub
- **Register GAP-PROC-01…06 in `Docs/KNOWN_GAPS.md`** (not my file). All jar and package dimensions are placeholders. The only evidence is jar shape (photos 01/07/11) and no package sizes exist.
- Pouch LOD0 is at 95% of budget by design. Raise `around`/`rings` only together with `tri_budget`.
- `studio.ps1 blender` wiring: forward to `Tools/Blender/blender.ps1`.
