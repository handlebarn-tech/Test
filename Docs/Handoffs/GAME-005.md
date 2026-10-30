# Handoff: GAME-005 (real deli canister + stepped bud fill in the slice)

**Status:** done, all gates pass. Branch `claude/task-game-005-972696` (off `main` 592086c). Packet `Docs/Tasks/Active/GAME-005.md` (written by this workcell).

## Changes
- **Jar import:** `Tools/Blender/params/deli_jar.json` gets `unity_dir` → `Assets/_Game/Art/Procedural/DeliJar/PROC_DeliJar.fbx` (+ .meta, default importer). Regenerated in Blender 5.2: the FBX is byte-identical (sha `b3dd1043…`); only the manifest's `params_sha256` and `unity_copy` changed. BUILD-005 is not on main, so the FBX is a plain binary (76 KB).
- **Spawn:** `SliceGame.SpawnJars` instantiates the canister at each `Anchor_JarSlot_###` (found by name, W3B m1; TEMP fallbacks unchanged). The jar's +Z label face follows the anchor forward, which faces into the room (N run yaw 180, E run yaw 270). The fill FBX is a child at identity. Glass gets `Slice_JarGlass` (HDRP Lit transparent); band gets a per-jar property block colour.
- **Fill step:** new `Simulation/Slice/JarFillStep.For(fill, steps, minVisiblePct)`: 0 g → F000 (SOLD OUT crumbs), else the nearest step ≥ min, ties up. The steps are read from the fill renderers' names (`_F<pct>_`), and `SliceSceneBuilder` picks up every `PROC_JarFill_*` model in the folder, so PROC-003 can change steps or looks without code changes. Only that step's LOD renderers are enabled; the LODGroups stay as imported. Updated on `InventoryService.Sold` for that batch.
- **DEC-046:** `SliceConfig.jarMinVisibleStepPct = 20` [GDD]. The 55 mm band hides F010 from the front (F010 top ≈ 35 mm), so any jar above 0 g shows at least F020 until PROC-003 raises F010; then set it to 10 (data only).
- **Brand band + label:** band colour = stable FNV-1a hash of `batch.Brand` into an 8-hue generic palette ([GDD] placeholder: no brand colours are recorded). Label = TextMesh (built-in font, HDRP Unlit alpha-clip `Slice_JarLabelText`) with strain (wrapped at 14 chars) + brand from `batches.json`, fitted inside the label card below the THC tag. The THC % tag stays blank: the catalog has no THC data. Bud look per batch = the same hash of the batch id mod the look count ([GDD], as the PROC-002 handoff says).
- **LOW / SOLD OUT labels:** `JarTops` now use the canister's real top (renderer bounds + 5 cm), so labels sit over the new taller jars.
- **Tests:** `SliceBotTests` asserts the step mapping (independent nearest-step LINQ, min step, F000 for every sold-out jar) instead of linear `grams/454` (W4E m2). EditMode `JarFillStep_NearestStep_TiesUp_MinVisible`. `SliceCaptureTests` adds shot `Jars_Closeup` (0.7 m from the sold-out jar).
- Removed the unused `Slice_JarFill.mat`.

## Validation (2026-10-30)
- Blender 5.2 `deli_jar` regen: FBX sha unchanged; LOD0 776 / LOD1 216 tris.
- `studio.ps1 unity-compile`: csErrors=0, CompileCheck OK. `unity-test-edit`: **150/150** (incl. the new mapping test). `unity-test-play`: 7 passed + 1 skipped (GPU capture under `-nographics`); bot seed 1 still 12/12, $265.20, Kush Cake sold out, 0 fallback anchors, 77 jars.
- `studio.ps1 unity-capture`: graybox QA PASS (max dev 0.22 ft); SliceCapture passed, **11 shots** incl. the new `SLICE_10_Jars_Closeup` and the SOLD OUT label-placement assertion. Contact sheet `Docs/Assets/Specs/SLICE_contact_sheet.png` refreshed (full PNGs in `Artifacts/Screenshots/592086c/slice/`). The DEC-013 gate waited once (2 editors running) and then ran.
- Checked by eye: the canisters stand on ART's shelves facing the room, band hues differ per brand, label text reads correctly, SOLD OUT shows F000 crumbs, LOW jars show the F020 pile above the band.

## For the Hub
- `Docs/Specs/SLICE_DESIGN.md` §4 still says "Jar fill level = grams / startGrams (linear)". The data is still linear; the visual is now stepped. DES owns the doc: please update it (not edited here).
- PROC-003: when F010 clears the band, set `jarMinVisibleStepPct` to 10 in `SliceConfig.json`.
- Brand band colours and the label layout are placeholders until ART/REF have real brand data (DEC-043). No logos.
- **Buds render white/grey:** the fill FBX colours do not survive Unity's HDRP material import, so every look is the same white. Bud materials were already ART's (PROC-002 handoff); flagging it as the most visible gap now.
- LOW labels for a lower-row jar sit just under the shelf above (the jar's real top); unchanged behaviour, just more visible with taller jars.
- Editor runs in this worktree rewrite `Art/Lookdev/Materials/LD_WD1_Walnut.mat` `_MainTex` to fileID 0 (texture guid 7bd7bec1… not resolved here). Reverted, not mine (ART); worth an ART check.
- Not done: random 90° yaw per jar, HDRP bud materials (ART), graybox/lookdev scenes (DEC-029).
