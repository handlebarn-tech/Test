# PROC-006c handoff: register kit follow-ups (REVIEW-PROC006b minors 2–6)

**Worker:** PROC-006c · **Reports to:** Studio Hub · **Branch:** `claude/zealous-kalam-4192dd`, based on `main` @ d207f31 · No Unity.

## Done
- **m2 contact sheet.** New `Docs/Assets/Previews/PROC_register_kit_contact_sheet.png`, 1500 × 4800 px, about 1 MB. It has one row per prop (16 rows).
  - Five 300 px tiles per row: LOD0 3/4, LOD0 side, LOD1, LOD2, LOD3.
  - Each tile is labelled with the prop, LOD, tri count and frame width in cm. The camera is orthographic and framed to the prop.
  - LOD3 now renders as solid shapes, not ghost boxes.
  - It comes from a new `contact` mode in `Tools/Blender/generators/register_stations_sheet.py`. To keep the PNG small, colours are reduced to 32 levels per channel; this causes no visible banding.
  - The stations sheet moved to `Docs/Assets/Previews/PROC_register_kit_stations_sheet.png` and was re-rendered. I removed the two old `Docs/Assets/Specs/PROC_register_kit_*` PNGs and updated the spec link.
- **m3 the ISO spray hangs.** `build_spray` now adds a wire S-hook (`RK_Metal`, all LODs). It has a ring round the trigger neck, an arm that rises behind the head, and a hook over the rail.
  - The attach point is the inside top of the hook, recorded as manifest `attach_point_unity_xyz` with a `hangs` note.
  - `STAND_RAIL` now uses `yaw_base_deg` -90. The hook sits over the stand-top edge, and the bottle hangs below it on the operator side with the nozzle facing the operator (spec RK-07: "hung by the trigger neck over a wire-frame edge"; DEC-104 R3).
  - New params `sb_hook_*` are tagged GAP-REG-8. `size_m` is now 0.094 × 0.1258 × 0.2918.
  - Checked in the POS_09 stations render: the bottle hangs off the stand edge.
- **m4.** The keyboard gets `gaps: ["GAP-REG-11"]` and a `_src` naming `kb_d_m`, `case_h_m` and `key_h_m` as full-size keyboard convention. I added a GAP-REG-11 row to the spec's GAP register.
- **m5.** The `UNDER_UPPER`, `UNDER_LOWER` and `UNDER_UPPER_EDGE` gap strings now name the real open item: under-counter shelf heights and depth. The TI calls it a "two-drawer POS cabinet" but the CCTV shows open shelves; the question is open with Nolan through the Hub (PROC-006b Q1). Tagged `GAP-RK-LAYOUT`. The spec's Anchors paragraph has the same wording.
- **m6:** see For the Hub below.
- **Re-export.** All 16 `PROC_RK_*` props were re-exported and all pass.
  - Only the `SprayBottle_ISO` FBX content changed (in both the Art export and the Unity copy).
  - The other props differ only in `params_sha256` (plus the keyboard's `gaps`).
  - In the manifest, only `PROC_RK_*` rows changed (checked with a JSON diff).
- **Station JSONs regenerated.** Every POS JSON on main was stale: its `frame.origin` came from ROOM_FIXTURES before REF-013, and main's fixtures have moved since. The new JSONs use main's fixtures.
  - Item counts and `not_fitted` are unchanged at all 11 stations (02 still drops TapeRoll and PaperStock_Open; 05 drops PaperStock_Closed).
  - The other changes: the spray's yaw and the new gap strings.

## Validation
- `Tools/Blender/blender.ps1 register_kit Tools/Blender/params/register_kit.json` exits 0, and 16/16 pass. SprayBottle_ISO tris are now 5160 / 1380 / 476 / 48 (was 4124 / 964 / 240 / 24); the other props are unchanged.
- `python Tools/Blender/tests/test_register_arranger.py`: passed, 11 stations, 11 distinct optional sets.
- `blender -b ... -P Tools/Blender/tests/test_validation.py`: `[SELFTEST] all passed`.
- Sheets: run `register_stations_sheet.py -- contact` and `register_stations_sheet.py` (POS_02/06/07/09). I inspected both visually.

## Not done
- m1 (2K PBR) belongs to PROC-010, and m7 (Unity `.meta` / first import) rides with PROC-007, as the packet says.
- Not run: a second full run to recheck byte determinism. The spray FBX was not re-hashed against a second run.

## For the Hub
**m6: proposed `KNOWN_GAPS.md` entries.** Format: `GAP-### | area | unknown | confidence | replacement path`. Suggested new section: `## PROC-006 register kit (see Docs/Assets/Specs/REGISTER_KIT.md GAP register; values in Tools/Blender/params/register_kit.json)`. Each entry's source is the spec's GAP register and DEC-104.
- GAP-REG-1 | asset | receipt printer depth/height (width ≈ 5.8 in measured in CEN, Low; top exit per DEC-104 R6; 80 mm paper per OFFICE_FINDINGS F3) | Low (80 mm thermal class convention) | closer register still / site measure
- GAP-REG-2 | asset | label printer depth/height and lid colour (width ≈ 7.4 in measured in WIDE; orange lid per R2C3; at every register, placement varies per DEC-104 R2) | Low | closer still / site measure
- GAP-REG-3 | asset | mouse type/colour/size (right of the keyboard at every register, DEC-104 R1; not visible in any still) | none (black wired optical, convention size) | closer still
- GAP-REG-4 | asset | folded bag bundle and tape roll sizes | Low | DEC-091 R5 bag dimensions
- GAP-REG-5 | asset | paper-stock box sizes (contents: receipt/label stock per DEC-104 R4, Med) | Low | site measure
- GAP-REG-6 | asset | personal items set at registers (only a CEN tumbler identifiable) | Low | more stills
- GAP-REG-7 | asset | wipes pack size (sparse at registers per DEC-104 R5; DEC-021 wipes on stand shelves) | Low | site measure
- GAP-REG-8 | asset | ISO spray bottle and S-hook size, and the section of the stand-top edge it hangs on (bottle type from the deli cart, Med; hanging per DEC-104 R3) | Low | site measure / closer still of a scale stand
- GAP-REG-9 | asset | rag size and where it lies (blue per DEC-104 R5) | Low | more stills
- GAP-REG-10 | asset | small register bin size and type per station (DEC-104 R7; office-bin convention 11.5 × 14 in vs rev7 `Trash_Small_POS_xx` 0.9 × 0.9 × 1.5 ft; see the PROC-006b World item 1) | Low | World picks one / site measure
- GAP-REG-11 | asset | keyboard depth, case and key heights (17.5 in width is the only cited value) | none (full-size keyboard convention) | closer still
- GAP-RK-LAYOUT | store | cm-level arrangement on the POS top (keyboard/printer slots, monitor depth position) and the under-counter shelf heights/depth (placeholder z 0.45/0.12 m, 0.5 m deep; TI A940 det. 11 "two-drawer POS cabinet" vs CCTV open shelves) | Low | the PROC-006b FOR NOLAN under-counter question; World's monitor-depth answer
- GAP-RK-WEIGHTS | store | per-station presence weights of the optional dressing items (DEC-104 non-uniform rule gives no rates) | none (designer weights) | playtest tuning

**DEC proposal:** none. The meaning of hanging-anchor placements (`pos_m` = the item's attach point on the edge) is in the `STAND_RAIL` `_src`. World should read it when it places items.
