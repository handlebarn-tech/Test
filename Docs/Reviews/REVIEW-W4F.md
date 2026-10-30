# REVIEW-W4F — ART-003 (retail lookdev, DEC-039..043) + ART-004 (GAP-120 HUB mirror)

**Verdict: GO with two minor ART follow-ups.** Neither blocks the merge. Branch `review/wave-4f` = `main` (489ea33) + a `--no-ff` merge of `claude/task-art-003-7cdbdc` (tip 27e6d66, clean, no conflicts) + this review. I made no data or code changes.

## 1. Validation (this worktree, DEC-013 gate via studio.ps1; 0 other editors at start)
| Check | Result |
|---|---|
| unity-graybox ×2 | both `unchangedScenes=4 lookdev unchanged`; `git status` clean after both |
| **Forced rebuild** (`-grayboxForce`, run directly) | `walls=19 fixtures=74 cameras=23 anchors=137; lookdev lights=69 millwork=12 panels=8`. The rebuilt scenes are **content-identical** to the committed ones: I compared every YAML object block with fileIDs masked and found 0 differing blocks in all 5 scenes. Only the random fileIDs change. Reverted. |
| unity-compile | OK, 0 CS errors |
| unity-test-edit | 149/149 |
| unity-test-play | 7 passed, 1 skipped (GAME's opt-in `Capture_EachScreen`). Includes the anchor tests, `ElevenRegisters_EachWithAnchorAndScaleStand`, `LookdevTests` and the slice bot's full shift |
| unity-capture | 24 shots, QA 23 views, **max 0.22 ft ≤ 0.5, PASS**. The slice capture passed (10 shots). Output is in `Artifacts/Screenshots/ae0d1ac` |

## 2. DEC-029 (data-driven, no hand edits) — PASS
The stamp skip by itself only proves the stamps match their inputs. The forced rebuild above proves the committed `Retail/BackRooms/Hub/Exterior/Retail_Lookdev.unity` are exactly the builders' output. Lookdev is driven by `Art/Lookdev/retail_lookdev.json`. The textures come from `Tools/Assets/lookdev_textures.py`, which sha-checks them. The CC0 oak veneer is in LFS under `Art/ThirdParty/PolyHaven` (DEC-023). The `graybox_qa.py` change is narrow: the one V5 scan that is known to be wrong (HUB partition) is now checked against A011's 18.995, and every other scan still compares with the plan raster.

## 3. HUB / HUB 2 vs A011 and REVIEW-W4C §1.4 — PASS
| Item | A011 / W4C | `graybox_layout.json` |
|---|---|---|
| HUB 2 (541.34 SF) | west, 18'-9¼" | x 0–18.79 ✔ |
| Partition | ≈x 19 | `W_HUB_HUB2` x 18.995, t 0.41 ✔ (capture 0.02 ft off; ≈18.9 ft in the top-down) |
| HUB (818.53 SF) | east, 28'-3¼", ≈3" residual here | x 19.2–47.19 ✔ |
| Connecting door | north end of the partition | y 48.1–51.1 ✔ |
| Office → HUB 2 door | x ≈7.5–10.5 | 7.5–10.5 ✔ (id kept) |
| West delivery door | y ≈49.5–52.8, into HUB 2 | 49.5–52.8 ✔ |
| SE exit | HUB SE corner, south wall, ≈44.5–47.5 | 43.99–46.99 (clamped to the inner face) ✔ |

- The 12 fixtures and the 6 CCTV poses are mirrored correctly: I spot-checked x → 47.19 − x and yaw → 360 − yaw on 6 items. No fixture crosses the partition or blocks a door. The tightest clearances are the HUB 2 cabinets, 0.3 ft from the office door, and the HUB north rack run, 2.2 ft from the connecting door.
- The HUB contents are still the Low GAP-110 guesses, mirrored rather than re-derived from CCTV, as ART says. Door swings are not modelled.

## 4. Lookdev vs REFERENCES_INDEX §6, DEC-037 and the photos — PASS with notes
- **These match the TI:**
  - Ceiling: PT-1 at 9'-0", with a 7'-6" soffit.
  - Floor: TL-1 12×24 field and TL-2 8×8 zones.
  - Ceiling panels: CLG-1 walnut panels on cable.
  - Lighting: 3500 K L4 downlights.
  - Neon: bottom at 72".
  - Counter: 34" max with a 4" toe and walnut fronts.

  Positions and extents are labelled layout choices (DEC-037: positions come from the plan/A011, not the TI).
- **The jar wall matches DEC-043:** teal leaf skin, dark-grey shelves, and a black top over walnut on the lowest row. There are no tong cups, the slot anchors are unchanged, and the wall-wash spots answer REVIEW-W3D's "too dark".
- **DEC-039/040/041:** 11 stations, each with a monitor, scale stand and anchor, and the slice keeps POS_08. FOH/BOH each have a desk, computer and chair with an anchor. The compass mapping is a stated Low assumption and is already a Hub question.

**m1 (minor, ART): the counter top uses 1½", but it should be 2".** `retail_lookdev.json` `millwork.top` = 0.125 ft, and the note says "REF-005 render: … 1-1/2" top; the A940 text said 2"". REVIEW-W4A corrected this the other way round. A940 detail 11 (the POS cabinet) has a **2" quartz edge**, and the 1½" belongs to detail 12 (4D). §6.4 row 348 says so. Fix: set `top` to 0.167 on the register counter, fix the note and rebuild. This is a one-value data change.

**m2 (minor, ART): CCTV view R2C3 is blind.** The camera (x 24, y 13.5, 8.5 ft) sits inside CLG-1 panel (x 23–31, y 10.5–14.5, bottom 8.25 ft), so `REF_R2C3_Retail.png` shows only walnut. The QA overlay doesn't catch it because the top-down hides the lookdev. Fix: shift the panel grid (a layout choice, Low) so no panel covers a camera, or add a builder check that panels avoid camera points.

**n1:** The `_comment`/`note` strings in `retail_lookdev.json` have mojibake (`Â§` ×9, double-encoded UTF-8). This is cosmetic: the scene object names use a correct §. Re-save the file as UTF-8 on the next ART touch.

**n2:** The Retail captures read very bright (near-white floor). That is consistent with the white TL-1 and EV 9.5, but the exposure should be checked against photos 01/05/10 in the next lookdev pass (there is no baked GI yet, a labelled shortcut).

## 5. PROC-002 canister on the jar wall (Hub's ask)
**Not used.** ART-003 builds jar-wall skins and slot anchors only. Main has PROC-002's `PROC_JarFill_*.fbx`, which only the slice uses (`SliceSceneBuilder`/`SliceGame`), and no `PROC_DeliJar` shell is imported into Unity. Follow-up, not a blocker: an ART/PROC task to import the canister and spawn jar + fill at the `jarSlots` anchors (the PROC-002 handoff gives the spawn rule).

## For the Hub
1. Merge `review/wave-4f`. Then a small ART follow-up for m1 (2" top) and m2 (R2C3 panel clash). These can go together with the jar-spawn follow-up in §5.
2. ART's open questions stand and are not mine to settle: Retail_Lookdev in `SceneBootstrap.AdditiveScenes`, the register compass mapping, brand fonts, the Low layout choices, and the capture-folder suffix.
3. Not checked: the ART-003 before/after sheet itself. I reviewed my own fresh capture instead, and I compared it with the photos by eye only.
