# GRAYBOX spec (ART-001, updated ART-002)

Measured graybox of the whole building, generated from data. Source of truth: `UnityProject/Assets/_Game/Art/Graybox/graybox_layout.json`, transcribed from `Docs/REFERENCES_INDEX.md` §1.3–1.5 and §2.

## Pipeline
| Step | Command | Output |
|---|---|---|
| Rebuild scenes from the JSON | `studio.ps1 unity-graybox` (`Dispo.Editor.Graybox.GrayboxBuilder.Build`, or menu *Dispo › Graybox › Rebuild From Layout*) | `Graybox_<Zone>` root in Retail / BackRooms / Hub / Exterior |
| PlayMode tests | `studio.ps1 unity-test-play` | `Artifacts/TestResults/<stamp>-playmode.xml` |
| Reference captures + QA | `studio.ps1 unity-capture` (Unity with a GPU, then `Tools/Studio/graybox_qa.py`) | `Artifacts/Screenshots/<commit>/`: `REF_*.png`, `TOPDOWN_Plan.png`, `captures.json`, `contact_sheet.png`, `overlay_topdown.png`, `overlay_report.json` |

Edit the JSON and rerun `unity-graybox`. Never hand-edit the `Graybox_*` roots, because each rebuild deletes and regenerates them.

**Deterministic rebuild (ART-002, REVIEW-W2C m1).** Each root has a `_BuildStamp <hash>` child (hash of the JSON + `GrayboxBuilder.cs` + `GrayboxLayout.cs`, CR-stripped). The batch build skips a scene whose stamp matches, so an unchanged rebuild leaves no diff (`unchangedScenes=4`). Pass `-grayboxForce` (or use the menu, which always forces) to regenerate anyway. A changed input still regenerates the whole scene with new fileIDs, so the DEC-029 commit rule stays: commit scenes only with a layout/builder change.

## Conventions
- Plan frame in feet (origin = Retail NW outer corner, +x east, +y south). Unity: **X = x·0.3048, Z = −y·0.3048**, Y up, so north = +Z.
- Walls are axis-aligned segments centred on the plan's drawn wall gaps, with the gap width as thickness. Exterior walls are 0.2 ft and sit inside the outline (fixtures start at 0.2 ft). Openings split a wall, and a header fills from the opening height to the ceiling.
- Object names carry their placeholder: `W_Retail_S_seg0 [h=10ft GAP-001] [t GAP-104]`, `…_ARCH_E_header [opening 3ft x 8ft GAP-113] [conf Med]`, `FX_RegisterCounter_L [conf Med] [h=3.5ft GAP-108] part1`.
- Fixture colour: green = Med, orange = Low confidence. Walls are light grey; floor slabs are dark grey; exterior ground is darker.
- Room trigger volumes are `Room_<id>` (plan rects) and are used by tests.
- **Anchors** (`Graybox_Retail/Anchors`, empty GameObjects, exact SLICE_DESIGN §7 names, no tags in the name): `Anchor_CustomerSpawn`, `Anchor_CustomerExit`, `Anchor_QueueSlot_0..3` (lane x 13.5, y 12→18 ft, slot 0 nearest the registers), `Anchor_ServiceCustomer` / `Anchor_ServicePlayer` / `Interact_Terminal` / `Interact_Scale` at station R1 (x 23 ft), `Anchor_JarSlot_000..113` (north jar wall 3 rows × 26, then east jar wall 3 rows × 12; bottom row first). Anchor forward = the way a customer/budtender/jar faces. All positions Low (layout choice). `GrayboxAnchorTests` (PlayMode) fails if any is missing or duplicated.
- **Register stations** (`stations` in the JSON): 4 POS monitors on the north leg at x 23/27/31/35 (GAP-107, Low). Each has a scale stand 1 ft east of the monitor on the staff side against the counter: 1.5 × 1.5 ft, black top at 3.25 ft, 4 posts, wire shelves at 0.5/1.75 ft, scale 0.9 × 0.9 × 0.3 ft, clear acrylic panel 1.5 × 1.5 ft on the counter edge (DEC-021/026, REF-002 §2.2; sizes Low until REF-003). One invisible box collider per stand; parts have none. Material `GB_Acrylic` is HDRP transparent.
- **Jar walls** (north, east) are a 0.3-ft back panel plus open shelves (`FX_JarShelf_*`) over the rest of the plan footprint, so jars at the slots are visible. Rows at 3.0/4.25/5.5 ft, 1 ft pitch (GAP-002 placeholders).
- Reference cameras: `REF_<tile>_<room>` (TOOLCHAIN §17). Each camera component is disabled and renders only on capture. Pose, FOV, confidence and note are in the JSON.

## Placeholder heights (none measured, all tagged)
| Key | ft | Gap | Used for |
|---|---:|---|---|
| ceiling | 10.0 | GAP-001 | wall height, columns, JC volume |
| door | 7.0 | GAP-104 | all doors (3'-0"×7'-0" convention) |
| arch | 8.0 | GAP-113 | both arches (rectangular; curve not modelled) |
| counter | 3.5 | GAP-108 | register/deli counters, kitchen, sink |
| tall / mid / desk / low / case / stanchion | 7 / 5 / 2.5 / 1.5 / 1.5 / 3 | GAP-002 | fixtures |
| pendant | 8.0 | GAP-113 | globe pendants (spheres, no collider) |
| camera | 9.5 | GAP-001 | CCTV mounts |
| pallet / totes | 4 / 4 | GAP-002 | HUB / HUB 2 pallets, tote stack |
| stand top | 3.25 | GAP-107 | register scale stand (in `stations.stand`) |

## Deviations from the plan (flagged, not invented)
- **Vestibule doors** (to FOH and BOH) use the full 2.2-ft vestibule side, because a 3'-0" door does not fit the drawn vestibule (GAP-104).
- **Interior doors** are 3'-0" wide and centred on the schematic 1.2–1.8 ft symbols. The HUB→HUB 2 door is also 3'-0" (2.0 ft drawn).
- **JC** is a closed ceiling-height volume at its drawn 3×3 position (GAP-103/109). The Restroom is an empty shell (GAP-109).
- **L counters** (register, deli, office desk, kitchen) are two rects each. Arm widths are read off the plan raster.
- **Queue stanchions** are thin, non-solid markers. Med since ART-002: vector fill bbox x 5.95–15.07, y 11.0–19.71 (REVIEW-W1 m3); the inner lines at x≈9/12 stay raster-read.
- **HUB / HUB 2 (ART-002, DEC-024).** Room shells unchanged (HUB = west 818 SF, HUB 2 = east 541 SF). HUB: west and north chrome-rack perimeter runs, a 16 × 6 ft central rack island (≈4 × 3 bays), the plan's desk strip, 2 pallets. HUB 2: the plan's wire-shelving strip, copier, tote stack, 2 pallets, work table, 2 cabinets, merch rack. Types Med (REF-002 §2.1); **every position is a Low guess** (GAP-110). The HUB wall's long bench and colored carts are not placed (no position evidence). **HUB emergency exit** (`EXT_EMERGENCY_HUB`, DEC-030): the green logo door is the building's furthest SE door; the plan shows none, so a 3'-0" opening sits at x 24.8–27.8 on the HUB south wall (Low). The unrecognized black door with yellow sign is not added.
- **No ceilings** (GAP-001; keeps the top-down check simple). Lighting is a temporary sun `Graybox_TempSun (move to Lighting_Day)` in the Exterior scene at 20000 lux. Captures use a temporary fixed-exposure volume at EV 13.
- **CCTV poses** are approximate. The 6 exterior tiles are **Low guesses** (building side unknown). The 6 storage tiles follow DEC-024: R4C3/R4C4/R5C3/R5C4 in HUB, R5C1/R5C2 in HUB 2 (rooms Med, poses Low). The new HUB-wall view R1C4 has no main-wall tile and gets no camera. R4C5 and R5C5 are repeats and get no camera.
- Exterior has no site plan: there is a flat ground slab only.

## Overlay check (top-down ortho vs `References/Index/floor_plan_grid_1ft.png`)
Method: `graybox_qa.py` compares wall centrelines (12 interior samples) and building outer edges (8 samples) along off-grid scanlines, capture vs plan, in feet. Tolerance is 0.5 ft.

**Result (commit base 99379df, 2026-10-29): max deviation 0.22 ft, PASS.**
- Interior wall centrelines: max 0.12 ft (Hall/Break wall at y=33.3; the plan's door arc shifts the drawn gap). All others are ≤0.08 ft.
- Outer edges: 0.13–0.22 ft. The plan's outline stroke is drawn about 0.15 ft outside the 0/47.19/76.03 lines, and the graybox sits exactly on those lines.
- This verifies the generator and the transcription against the vector plan. It does **not** verify the plan against the real building (GAP-101).
