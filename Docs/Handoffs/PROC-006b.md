# PROC-006b handoff — register workstation kit (generators + per-station arranger)

**Worker:** PROC-006b (resumed from the unreviewed WIP d30bb73 after DEC-112). **Reports to:** Studio Hub. **Branch:** `claude/proc-006b-92b9a0`, merged with main @ 1b72b81.

## Done
- **Spec** `Docs/Assets/Specs/REGISTER_KIT.md`: DEC-104 answers were already applied (6f4c445). This task added the anchor binding to ROOM_FIXTURES rev7 (now merged).
- **Generator** `Tools/Blender/generators/register_kit.py` + `params/register_kit.json` (WIP kept). Fixes made here, because the WIP never completed a full run:
  - `PaperStock_Open` LOD3 keeps its walls and flaps (it was a closed box that broke the size envelope);
  - the `Tumbler` straw is kept at LOD2 and LOD3;
  - `SprayBottle_ISO` `size_m` now matches what its own profile builds (0.094 × 0.0985 × 0.265 m; was 0.096 × 0.11 × 0.282);
  - `WipesPack` and `TrashBin_Wire` size tolerance raised to 0.011 m, because the soft-pack bulge and the wire rim drop out at LOD2–3 (1 cm);
  - manifest rows now name the rev7 anchor ids instead of "pending".
- **Arranger** `Tools/Blender/generators/register_arranger.py` (pure Python): it reads rev7 `POS_02..12` (`operator_zone`, `stand_rect`, `staff_side`) and `Trash_Small_POS_xx`, then writes `Art/Exports/Procedural/RegisterStations/POS_xx.json`. There is one seed per station (`61*100 + reg`).
  - Fixed at every station: keyboard, mouse (always right), scanner, receipt printer, label printer (its slot varies: 7 stations left, 4 right).
  - Optional per station, with weights: bags, tape, paper stock open or closed, tumbler, wipes, ISO spray, rag draped or folded, trash bin wire or solid.
  - Condition varies per station: `wear_scale`, `fill_level` and yaw.
  - Placements are collision-checked per anchor. Items that don't fit go into `not_fitted` and are never forced.
  - Frame and citations: `arranger` block in the params.
- **Self-test** `Tools/Blender/tests/test_register_arranger.py`, all asserts pass:
  - same seed gives identical JSON, and it equals the committed files;
  - 11 stations;
  - each fixed item appears exactly once, on TOP;
  - the mouse is right of the keyboard edge;
  - optional sets differ: 11 distinct of 11.
- **Exports:** 16 `PROC_RK_*` FBX (LFS) + Unity copies + validation JSON + manifest rows (only `PROC_RK_*` rows changed). **All 16 pass.**
- **Sheets:**
  - `Docs/Assets/Specs/PROC_register_kit_contact_sheet.png` (all props: LOD0 front/side, LOD3);
  - `Docs/Assets/Specs/PROC_register_kit_stations_sheet.png` (POS_02/06/07/09 dressed; context slabs are preview only). Built with `register_stations_sheet.py`.

## Validation
- `blender -b --factory-startup --python-exit-code 10 -P Tools/Blender/run_generator.py -- register_kit <abs params>` exits 0, and 16/16 pass.
- **Deterministic:** two consecutive full runs gave identical sha256 for all 49 outputs (FBX, Unity copies, validation, manifest).
- `python Tools/Blender/tests/test_register_arranger.py` passes; the PROC-005 `tests/test_validation.py` still passes.
- One run hit a transient Windows `OSError 22` opening an FBX for write (a file lock); the rerun was clean. This is not generator logic.

**Tris vs DEC-084 (guides, not caps, DEC-114).** LOD0 / LOD1 / LOD2 / LOD3:

| Prop | LOD0 | LOD1 | LOD2 | LOD3 |
|---|---|---|---|---|
| Keyboard | 17012 | 4808 | 264 | 24 |
| TrashBin_Wire | 16448 | 5292 | 240 | 32 |
| Rag_Folded | 6236 | 1556 | 156 | 12 |
| Rag_Draped | 5980 | 1492 | 156 | 24 |
| PaperStock_Open | 4728 | 1272 | 312 | 108 |
| Scanner | 4704 | 1528 | 352 | 56 |
| Mouse | 4660 | 1252 | 340 | 40 |
| LabelPrinter | 4444 | 1496 | 128 | 36 |
| SprayBottle_ISO | 4124 | 964 | 240 | 24 |
| TrashBin_Solid | 3936 | 924 | 348 | 32 |
| BagBundle | 3332 | 212 | 80 | 12 |
| ReceiptPrinter | 3036 | 1388 | 96 | 24 |
| Tumbler | 2492 | 668 | 212 | 52 |
| TapeRoll | 1948 | 508 | 240 | 32 |
| WipesPack | 1860 | 524 | 96 | 12 |
| PaperStock_Closed | 144 | 112 | 28 | 12 |

12 props are under the 5k guide (validation warns only). Per DEC-114, judge the contact sheet. The weakest read is **PaperStock_Closed**: a bevelled box with a tape strip, seam and label, but nothing more.

## Not done / limits
- **Materials:** preview colours only. The 2K PBR set is still pending PROC-005 Q0.2/Q0.3, as the WIP already noted in the manifest.
- **No Unity work** (Hub: no editor). The new Unity FBX copies have no `.meta` files and no `Props/`/`RegisterKit/` folder metas. Unity creates them on first import, and whoever opens the editor commits them.
- The WIP's `checks`/LOD pattern is unchanged. The spec's per-row LOD0 ranges (e.g. 6–12k) are guides only.

## For the Hub (World / evidence, not Nolan)
1. **Small-bin size conflict.** Rev7 `Trash_Small_POS_xx` is 0.9 × 0.9 × 1.5 ft (0.27 × 0.27 × 0.46 m, Low). The kit uses an office-bin convention: wire 0.30 × 0.36 m, solid 0.28 × 0.25 m (GAP-REG-10). Both are placeholders; World should pick one. The arranger clamps the bin against the stand back, so the larger kit bin sits 1–3 cm further into the aisle than rev7's centre.
2. **Monitor depth position.** Rev7 POS_xx pos is the graybox monitor; it sits 0.22 ft inside the counter staff edge, which leaves no room for the keyboard in front of it. The arranger reserves the monitor footprint (rev7 1.6 × 0.25 ft) at the **back** of the 2'-6" POS top (`GAP-RK-LAYOUT`). World should confirm that the rev7 y is only graybox.

## Questions for Nolan (through the Hub)
Searched first (DEC-105): `DECISIONS.md` (DEC-021/096/103/104), `KNOWN_GAPS.md`, `Handoffs/REF-008.md`, `Research/*.md`, `REFERENCES_INDEX.md` §2.2/§6.4 for "under-shelf / under-counter". Nothing answers this.

1. **What is under the register counter on the staff side: open shelves or drawers, and how many levels?**
   - Sources: CCTV CEN (155,490)–(300,530) and EAST (1540,380)–(1615,435) show open black shelves holding bag bundles and boxes. TI A940 detail 11 (REFERENCES_INDEX §6.4, High) calls the POS cabinet a "two-drawer POS cabinet".
   - Candidates: (a) open shelves on the staff side with the drawers on another part of the run; (b) two open shelf levels per station, no drawers; (c) a drawer row above open shelves.
   - Placeholder meanwhile: two open shelves (UNDER_UPPER z 0.45 m, UNDER_LOWER z 0.12 m, 0.5 m deep), labelled GAP in params.
