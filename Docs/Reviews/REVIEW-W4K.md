# REVIEW-W4K — GAME-005 (real deli canister + stepped bud fill in the slice)

**Verdict: PASS (GO to merge).** `claude/task-game-005-972696` @ 3b0dc7e merged `--no-ff` into `review/wave-4k` off main. One fix in the merge commit (m1); no blockers.

1. **Spawn by name - PASS.** `SliceGame.SpawnJars` instantiates the canister at `Anchor_JarSlot_###` (ART's `jarSlots` anchors); the hard-coded layout is only a fallback. Capture shows jars on ART's shelves facing the room; the handoff reports 0 fallback anchors and 77 jars.
2. **Fill steps - PASS.** `JarFillStep.For`: 0 g gives F000 (SOLD OUT), otherwise the nearest step at or above `jarMinVisibleStepPct` (20), ties up (DEC-046). Updated on `InventoryService.Sold`. `SliceBotTests` assert the step mapping with an independent LINQ calculation, plus an EditMode `JarFillStep_NearestStep_TiesUp_MinVisible` test. In shot 10 the LOW jars show a pile above the band.
3. **Labels - PASS.** LOW and SOLD OUT labels sit over their jars in SLICE_09/10 (viewed; the capture test also asserts the SOLD OUT placement).
4. **No logos - PASS.** Label = TextMesh strain + brand text from `batches.json`; the band colour is a hash into a generic 8-hue palette.
5. **Gates - PASS.** `unity-compile` csErrors=0; `unity-test-edit` 164/164; `unity-test-play` 7 passed, 1 skipped (the GPU capture test under `-nographics`); `unity-capture` graybox QA PASS (23 views, max deviation 0.22 ft), slice 1 passed, 11 shots. Single editor through the runner; I did not test two editors at once (DEC-013).
6. **Follow-up (not a blocker):** buds render white/grey until ART builds HDRP bud materials.

## Notes
- m1 **LFS fix in the merge.** The branch predates BUILD-005 and added `Art/Procedural/DeliJar/PROC_DeliJar.fbx` as a plain 76 KB blob. The merge commit renormalizes it to an LFS pointer (sha256 b3dd1043…); all tracked FBX are now pointers.
- m2 Labels print real brand names as text from `batches.json`; this touches the open brand-IP question (DEC-043), so decide before any public build.
- m3 `SLICE_DESIGN.md` §4 still says fill = grams / startGrams (linear): update it (Hub/DES, noted in the handoff).
- m4 When PROC-003 clears F010 above the band, set `jarMinVisibleStepPct` to 10.
- m5 Editor runs rewrite `LD_WD1_Walnut.mat` (ART's, noted in the handoff). My runs left the tree clean.
