# PROC-013 handoff: door family (glass storefront + every DOORS.json door), Blender

**Worker:** PROC-013 (replacement; the first worker, an in-Hub agent, died mid-task) · **Reports to:** Studio Hub · **Branch:** `claude/nervous-williams-4af82b`, based on `main` @ 751b85a · No Unity.

## Salvage
- The dead worker's files were all uncommitted in `.claude/worktrees/agent-a83016d0b10c940eb`. I copied all 58 of them, plus its manifest, into this worktree. I did not touch that worktree (DEC-123). It can be retired once this branch merges, because everything in it is here.
- I audited its `doors.py` and `params/doors.json` against the packet. Then I regenerated everything on current `main`. The first re-run gave FBX `export_sha256` values byte-identical to the salvaged exports for all 28 assets, which also re-confirms determinism.
- After that I changed one params value (the Entry evidence crop, see below), so every door row's `params_sha256` changed. The FBX geometry is unchanged.

## Done
- **One parametric generator:** `Tools/Blender/generators/doors.py` with `Tools/Blender/params/doors.json`.
  - It reads every door fact live from `Docs/Reference/DOORS.json`: type, leaves, leaf size, hinge/swing (`closedRotation`, `openAngle`), hardware, `selfClosing`, lock and defaultState. None of these are copied into params.
  - All 15 rows are covered, giving 28 assets: 1 storefrontPair (Frame + LeafL + LeafR), 11 swing doors (Frame + Leaf), 2 openings (Frame) and 1 foldingGrille.
  - Wall thickness comes from the graybox wall `t` (graybox_layout.json, GAP-104), with each frame family's minimum depth as the floor.
- **Glass storefront entry (PT2 #1):**
  - Aluminium stile-and-rail leaves: 3.5 in stiles and top rail, 10 in bottom rail. 1/4 in GL-1 green-tinted glass in **its own material slot**, `M_Proc_Door_Glass_GL1` with alpha 0.22 and BLENDED, listed in the manifest as `door.transparent_slots`.
  - Snap-in glazing beads on both faces, an astragal on the L leaf, and a threshold.
  - Hardware per DOORS.json `storefrontPull` (DEC-115 (2)): back-to-back vertical bar pulls at 42 in.
  - Three butt hinges per leaf, each leaf hinged at its outer jamb.
- **Hollow-metal swing doors:** 1-3/4 in flush leaf, a pressed frame with a swept stop, a strike plate and three rubber silencers. Hardware follows each record:
  - `lever`: lever trim on both faces with roses, and a latch faceplate.
  - `pushBar`: rim exit device (bracket, rail, touch bar, mechanism case). Ext_Delivery also gets an outside pull (GAP-DOOR-7).
  - Closer: a parallel-arm surface closer when `selfClosing` is true. When it is `unknown`, the closer is kept as a GAP-138 placeholder.
  - Kick plate on Hall_Restroom (A310 103 hardware).
- **Arches:** a cased gypsum lining with rounded head corners (r 0.6 ft, measured on BAND 06), corner beads, and spandrel fill out to the square rough opening.
- **Grille 101B:** pickets, crossed lattice links and the top track. Not placed (DEC-037).
- **Pivots:**
  - Every leaf's origin is its hinge axis at floor level, which is the DOORS.json `<object>_Hinge` pivot. The leaf runs along Unity local +X and rotates about +Y by `openAngle`.
  - The frame's origin is the opening centre on the wall centreline. The manifest gives each leaf's pivot in frame-local Unity coordinates (`hinge_pivots_unity_xyz`), plus `yaw_deg` and `swing_side_unity_local`.
- **For ART-013's wall cut:** `rough_opening_m` (width, height, depth) is in every Frame's manifest row, alongside `soffit_opening_m` and `wall_t_graybox_m`. Swing doors: 1.022 × 2.207 m (JC 0.922). Entry: 1.924 × 2.197 m. Arches: 0.946 × 2.149 m.
- **Collision:** DEC-086 manifest boxes (jambs and head; leaf; grille).
- **LODs:** LOD0–LOD3, all strictly decreasing.
- **Sheets.** This is new code: the dead worker had none. Run `doors.py -- sheets [ids]`. Everything renders in EEVEE, so the glass reads as glass. Each door is shown hung in a grey wall stub cut to its rough opening, with the leaf drawn at 40% of `openAngle`. Labels carry the type, size, RO, hinge, swing, hardware, closer, lock, defaultState and GAPs.
  - `Docs/Assets/Specs/PROC_doors_contact_sheet.png` (2800 × 1680): LOD0 of every door, 5 per row.
  - `Docs/Assets/Specs/PROC_doors_lod_sheet.png` (1200 × 4500): one row per door, LOD0 to LOD3 with tri counts.
  - `Docs/Assets/Specs/PROC_doors_<id>.png` (2240 × 560, 15 files): push-side 3/4 view, swing-side 3/4 view, ortho elevation, and the evidence crop with its caption beside it. Doors with no still get a labelled "no still" tile.
  - I fixed the Entry evidence crop. It had been on the queue area; it is now on the glass entry pair with the exit sign (CCTV wall 2 R2C1 top-left).

## Validation
- `Tools/Blender/blender.ps1 doors Tools/Blender/params/doors.json` exits 0, and 28/28 assets pass: transforms, UV maps, degenerate faces, material slots, tri budget, LOD chain and size.
- The generator's own self-checks raise on failure, and all pass:
  - Each leaf's width and height match DOORS.json `leafWidth_ft`/`leafHeight_ft` within `size_tol_m` 0.005. Leaves come out exactly 0.9144 × 2.1336 m (JC 0.81382). The grille is 16.4 × 7.5 ft.
  - The hinge edge sits on the pivot axis (±0.1 mm), and the hinge barrels are centred on the origin axis.
  - Closed leaves fit inside the jambs and clear the head.
  - Arch RO width matches.
- I checked the swing direction numerically. With the leaf assembled at 40% open, its world y lies on the `sw` (swing) side: Vest_FOH +y, Hall_Restroom and Entry −y.
- `Tools/Blender/tests/test_validation.py`: `[SELFTEST] all passed`.
- Manifest: only the 28 new `PROC_Door_*` rows were added. Every existing row is unchanged (checked with a JSON diff against HEAD).
- I inspected the sheets visually. Every leaf reads open on the correct side, the glass is transparent, and the hardware is visible.

## Not done / known limits
- **UV ch1 lightmap (DEC-097) is not done.** The shared `proclib.finish_object` writes only `UVMap_Main` and `UVMap_Label`. The runner also rejects any other UV list, and no generator in the repo has a lightmap UV. Both files are outside my Owns ("use as-is"), so this needs a pipeline task; see For the Hub.
- **Export folder.** The runner hard-codes `Art/Exports/Procedural/` (`EXPORT_DIR`), so the FBX and validation JSON sit there as `PROC_Door_*`, not under the packet's `Art/Exports/Procedural/Doors/**`. I kept the runner as-is.
- **2K PBR:** materials are the preview PBR finish values in params (`finishes`). The slot names are the contract for the PROC-010 materials pass. Wear amounts are placeholders (GAP-DOOR-9).
- **Tri guide:** LOD0 HM leaves are 2.9k–3.6k and storefront leaves 3.3k. That triggers the runner's DEC-084 "below 5000" warning. A flush HM leaf with real hardware is honestly this light (DEC-114: the figures are guides), and I did not pad it.
- Decals (fire label, "EMPLOYEES ONLY", leaf print, SE round logo) are left to the signage pass (GAP-DOOR-8).
- No Unity import (out of scope).

## For the Hub
- **Pipeline task needed (DEC-097):** add a lightmap UV (UV ch1) to `proclib.finish_object` and the runner's UV check, then re-export every PROC family, doors included. This blocks the lightmap part of PROC-013 only.
- **Packet path fix:** amend the PROC-013 and ART-013 references from `Art/Exports/Procedural/Doors/**` to `Art/Exports/Procedural/PROC_Door_*.fbx`. The alternative is a runner `export_dir` param in that same pipeline task.
- **Proposed `KNOWN_GAPS.md` entries** (format `GAP-### | area | unknown | confidence | replacement path`; values in `Tools/Blender/params/doors.json`):
  - GAP-DOOR-1 | asset | HM frame face/stop/rabbet/undercut, hinge layout, lever/rose/exit-device/closer sizes (only the 1-3/4 in leaf and the 3'-4"–3'-6" hardware band are on A310) | none (commercial conventions) | site measure / closer still
  - GAP-DOOR-2 | asset | storefront stile/rail widths, frame section, glass thickness, pull size, threshold, hinge vs pivot type; frame finish dark bronze vs black anodized | Low | site photo of the entry
  - GAP-DOOR-3 | asset | arch: is 7'-0" the crown or the spring line (crown used); whether Arch_E also has a rounded head | Low | still of each arch with a scale reference
  - GAP-DOOR-4 | asset | 101B grille picket pitch/section, lattice, track; 18 in access door not modelled | none (convention) | site photo
  - GAP-DOOR-5 | asset | hardware/closer finishes (satin stainless, black lever, sprayed aluminium closer) | Low | closer stills
  - GAP-DOOR-6 | asset | leaf/frame colour of doors no still shows (Emergency_RetailE, Hall_Restroom, Office_HUB2 frame, HUB2_HUB, Ext_Delivery) and the SE green shade | Low | stills / site photo
  - GAP-DOOR-7 | asset | exterior side of the exterior doors (pull trim on Ext_Delivery, threshold type) | none | exterior photo
  - GAP-DOOR-8 | asset | door decals: fire labels, "EMPLOYEES ONLY", office leaf print, SE round logo | Med (seen, not modelled) | signage pass
  - GAP-DOOR-9 | asset | wear amounts (edge chip, low scuff, hand grime) | none | PROC-010 materials pass
- The salvaged worktree `.claude/worktrees/agent-a83016d0b10c940eb` can be retired after merge. All of its content is on this branch (DEC-123: positively identified).
- **FOR NOLAN:** nothing blocking. GAP-DOOR-2 (what the storefront frame looks like) and GAP-DOOR-6 (colours of the unseen doors) would be closed by one phone photo each of the entry and the back doors.
