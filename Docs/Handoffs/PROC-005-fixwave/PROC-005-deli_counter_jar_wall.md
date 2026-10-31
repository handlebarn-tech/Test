# PROC-005 fix wave: deli_counter_jar_wall (REVIEW-PROC5 #1, #3, #4, #7)

Status: **validation PASS** on all 3 assets, **deterministic** (two runs, identical `export_sha256`). Not committed.
Files: `Tools/Blender/generators/deli_counter_jar_wall.py`, `Tools/Blender/params/deli_counter_jar_wall.json`, FBX + Unity copies + Validation JSON for the 3 jar walls, `Docs/Assets/Specs/PROC_deli_counter_jar_wall_contact_sheet.jpg` (the old `.png` sheet was `git rm`'d).

## What changed

### #3 Phantom deli counter: dropped
- Removed ids: **`PROC_Deli_DeliCounter_LegA`, `PROC_Deli_DeliCounter_LegB`**.
- Reason: RI §1.5 row 101 and §8.1 (REF-011) say the plan's "DELI COUNTER" L is the south register run, which belongs to register_counter_run.
- What was deleted:
  - both variants and the `deli_counter` code;
  - the FBX in `Art/Exports/Procedural/` and the Unity copies in `Fixtures/Deli/` (`git rm`);
  - the Validation JSON (`git rm`);
  - their renders.
- Manifest: I removed both entries from `Art/Exports/Procedural/manifest.json` under the manifest lock. `contact_sheet` crashed on their missing renders, so I could not leave them for the merge. No other entry was touched.
- Unused colours removed: `Wrap_DeliChecker`, `Plywood_Edge`, `Glass_Clear`.

### #4 Depth, RF ids and fittings
- **Sizes now come from the RF rows** (expected = RF; validation enforces it):

  | Wall | RF row | Size (ft) | Size (m) |
  |---|---|---|---|
  | North | `DeliJarWall_North` | 25.9 × 2.1 × 7.0 | 7.894 × 0.640 × 2.134 |
  | South | `DeliJarWall_South` | 21.2 × 2.1 × 7.0 | 6.462 × 0.640 × 2.134 |
  | East | `DeliJarWall_East` | 14.0 × 2.09 × 7.0 | 4.267 × 0.637 × 2.134 |

  North was 26.0 ft (an RI plan string) before. Depth includes the back counter, per the RF notes.
- **`rf` fields** hold the RF fixture ids. The manifest gets a new `rf_fixture` field.
- **`shelf_pitch_m` 0.3556 (14 in)** is re-cited to RI §2.4 "Jar-wall shelves" (≈14–16 in, Low) + GAP-PROC-16. It no longer cites TI §6.4. I used the lower bound so the East top board clears the arch spring.
  - `shelf_depth_m` 11 in: RI §2.4 (10–12 in).
  - 2 jar tiers per wall: RI §8.3 and RF North/South.
- **Per-wall fittings**, each from its own RF note:

  | Wall | Base | Shelving | Wall finish |
  |---|---|---|---|
  | North (DEC-043 photo, "probably this wall", Low) | black carcass, **walnut** fronts in 2 rows, silver cup pulls | dark-grey sheet-metal shelves on slotted black standards + knife brackets | teal wallcovering, green/black **checker tile band** on top |
  | South (RF South, BAND_10, BAND_01) | black back counter with **open hopper bins** on 2 open-bay levels | **black** shelves (BAND_01); 3rd top display board with no jar slots (BAND_01) | teal wallcovering, no checker band |
  | East (RF East, BAND_11) | black counter over black open cubbies | 4 **arched wood U-frames** (swept, rounded arch corners), light shelf boards with LED channel + warm diffuser + cleats; 3 boards per bay (top one has no slots) | backlit teal panel |

  Walnut is on North only. On the South base I modelled the plastic open bins. The "wire bins" in BAND_10 look like the separate chrome wire rack beside the counter (wire_shelving family), not part of this fixture (question 4).
- **Colour split:** North and South use a new `Teal_Wall` key (paper/wallcovering finish).
  - Its tint is the median of the teal wall in the DEC-043 crop (sRGB 55/82/78).
  - That photo shows printed WC-1 with no backlight. The old emissive teal rendered washed out.
  - Only East keeps the emissive `Teal_Backlit` + LED (`emissive_parts` is per wall now).

### #1 Visual bar (LOD0 rebuilt as joinery and metalwork)
- **Carcass:** gables with real toe-kick notches; 4 in kick with a 2 in recess (TI §6.4); deck, back and dividers; bevelled black top with 1 in overhang.
- **North drawers:** walnut fronts with 4 mm reveals over a black face backer. Hollow crescent cup pulls with a back plate and 2 screw heads.
- **South bins:** hopper sides, floor, back, a low front lip and a label slot. Edge banding on shelf noses and divider fronts.
- **Standards:** twin-flange slotted standards with real slot openings at 1 in pitch, a black backer behind the slots, and screw heads through the slots.
- **Brackets and shelves:** knife brackets hooked into the standards. Bent-sheet shelves with a hemmed front lip and rear up-flange, split per standard bay with seams.
- **Panels:** in a black trim frame, with trim battens at the panel seams.
- **Checker band:** individual bevelled 2 in tiles with a recessed grout bed.
- **East:** swept wood U-frames with rounded arch corners; bevelled boards with LED channel, diffuser and cleats.
- Jar slots stay game anchors: North 126, South 102, East 60 (East slots sit inside the bays).

### #7 Citations
- Every size, count, colour and finish key is cited, or carries a GAP id, in `_src`, `_src_colors` or the per-variant `_src`.
- I checked the GAPs I cite: GAP-113 (jar wall not in TI), GAP-133 (east tier count, per-wall depth), GAP-PROC-16 (shelf/standard/pull sizes, jar pitch).
- GAP-106 is no longer cited.

## Assets

| Asset | LOD0 | LOD1 | LOD2 | LOD3 | Slots |
|---|---|---|---|---|---|
| PROC_Deli_JarWall_North | 64,076 | 33,396 | 636 | 84 | 126 |
| PROC_Deli_JarWall_South | 24,168 | 4,668 | 804 | 72 | 102 |
| PROC_Deli_JarWall_East | 8,062 | 4,138 | 474 | 180 | 60 |

- Validation warnings: South and East are under the 30k `lod0_min` guide. Under DEC-114 that is a guide only; on the sheet they read as built fixtures (East is few large swept members).
- The LOD1/LOD2 drops are steeper than the 50/25 % guide (for example South LOD1 is 19 %), but the chain strictly decreases.

## New GAP rows (for KNOWN_GAPS.md, PROC-005 worker to merge)
- GAP-PROC-25 | asset | Deli South jar wall base: the open bins under the black back counter (RF DeliJarWall_South, BAND_10). Bin size, colour (grey-blue by eye), bins per bay (2), bay width (24 in) and level count (2) are placeholders; whether "wire bins" means bins in the counter or the separate chrome wire rack beside it is open | Low | params | site photo / Nolan
- GAP-PROC-26 | asset | Deli East jar wall arched bays (RF DeliJarWall_East, BAND_11). Placeholders: bay count 4 (≈36 in clear ≈ 6 jar widths by eye), frame member 2 in, arch corner radius 0.14 m, shelf board 19 mm thick and light colour, the cubbies under the counter following the bays | Low | params | site measure / Nolan
- GAP-PROC-27 | asset | Deli jar-wall construction placeholders: drawer module width 24 in (North), counter-top overhang 1 in, backlit/wall panel build-up 20 mm, black panel trim and grout, checker band height 6 in and tile 2 in (RI §2.4 gives colours only), and the top display board on South/East (BAND_01/BAND_11) | Low | params | site measure / Nolan

## Replacement checklist line (IMP-003_PROC_FIX_CHECKLIST.md)
- [ ] deli_counter_jar_wall: **PROC-005 done:**
  - 3 RF jar walls: North 25.9 / South 21.2 / East 14.0 × 2.1 × 7.0 ft, `rf` = RF ids.
  - Fittings per wall: North walnut drawers + grey bracket shelves + checker band; South open bins + black shelves; East arched wood bays + backlit teal + LED.
  - LOD0 rebuilt as joinery (toe kick, reveals, cup pulls, slotted standards, knife brackets, hemmed shelves, tiles).
  - DeliCounter_LegA/LegB dropped (= south register run, RI §1.5 row 101): prune the manifest entries (already removed in this worktree).
  - LOD0 8k–64k tris, deterministic.
  - GAP-PROC-25..27.
  - Unity import check still owed.

## Questions for Nolan (through the Hub)
1. **South: third shelf board.**
   - Source: BAND_01 (right half, south wall beside the arch).
   - What I see: above the top jar tier there is another black shelf holding decor (a red bottle, small items).
   - Candidates: (a) a fixed top display shelf on the whole wall (modelled); (b) a short shelf only near the arch.
2. **East: tier count** (GAP-133).
   - Source: BAND_11.
   - What I see: each arched bay has three lit boards. Jars stand on the middle two levels, and a plant sits on the top board.
   - Candidates: (a) 2 jar tiers + a top display board (modelled); (b) 3 jar tiers.
3. **Are North/South backlit?**
   - Sources: the DEC-043 photo shows a matte printed teal wall with no visible glow. RI §2.2 calls the walls in the wide still "teal-backlit jar walls"; BAND_01 looks evenly lit.
   - Candidates: (a) printed wallcovering, unlit (modelled); (b) backlit like East.
4. **South "wire bins".**
   - Source: RF South note, BAND_10.
   - What I see: grey-blue plastic open bins under the counter, and a separate chrome wire rack with a trash can at the end of the run.
   - Candidates: (a) plastic bins in the counter plus a freestanding wire rack (modelled: bins only); (b) wire baskets in the counter.
5. **Does the walnut-drawer photo show North?**
   - Source: DEC-043 photo; RF North note says "probably".
   - Candidates: North (modelled); East or South would swap bases.

## Not done / notes
- Kraft bags, the South daily-deals sheet and the jars are not modelled: they are product, signage or other families' assets.
- The leaf pattern on the teal wall is texture work. The emissive and paper finishes show a flat tint.
- No infra bugs found. `contact_sheet` does fail hard when a manifest entry has no renders (seen with the dropped legs). That is expected behaviour, but it is worth knowing for other families that drop assets.
