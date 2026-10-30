# REVIEW-W4P — PROC-003 (F010 visible pile, natural packing, REF-007 jar size, house-smalls jar)

**Verdict: PASS** (one reviewer fix applied; one interface clash for GAME-005 to resolve on its side).
**Branch:** `review/wave-4p` = main (79fdfc9) + `--no-ff` merge of `claude/task-proc-003` (96a8aa0) → 389628d, plus review fix 21d5b14. Reviewer: REVIEW-W4P, 2026-10-30.

## Merge
- PROC-003 branched before BUILD-005 put procedural FBX under LFS, so 13 FBX conflicted (raw binary vs LFS pointer) and 3 new FBX were raw.
- Resolved by taking PROC-003's bytes and re-adding them: all 16 PROC-003 FBX are now LFS pointers, matching `.gitattributes`.
- `PROC_PIPELINE.md`: kept both the PROC-004 and the PROC-003 sections.
- Git's rename detection paired the packet with `Docs/Tasks/Done/PROC-003.md`; kept there (task done).

## 1. Determinism: PASS
Every generator was run twice on the merged tree: deli_jar, deli_jar_smalls, package box/pouch, jar_fill and PROC-004 packaged_goods, plus all three contact sheets.
- The two runs are sha256-identical on all 51 outputs (FBX in `Art/Exports` and the Unity copies, manifest, sheets).
- They are also identical to the committed files. The only difference is LF/CRLF noise in `manifest.json`; the content is equal.
- PROC-004 outputs are unchanged by the merge.

## 2. DEC-046 F010: PASS
`PROC_jar_fill_contact_sheet.png` was viewed (columns F000, F010, F020, F040, F070, F100, LOD1, LOD2).
- F010 shows a pile above the green band from the front in all 6 looks.
- F000 is the only empty-looking step.
- The generator fails any step above 0 g whose top is less than 12 mm above the band, and `JarFillImportTests` checks every step and LOD in Unity.
- Steps rise monotonically.

## 3. Packing (W4E n1): PASS, with a note
- F100 and LOD1 no longer read as 3 neat columns in any look.
- n1: DarkCompact F070 still reads as a fairly regular 3×4 grid of round buds. This is acceptable under GAP-PROC-07 (placeholder buds) and is not a rework item.

## 4. Sizes vs REFERENCES_INDEX §2.4: PASS, labelled
- `PROC_DeliJar` (canister): 0.1524 × 0.1397 m = 6.0 × 5.5 in; body 0.235 m + lid 0.0254 m = 10.25 in. This sits inside §2.4's "≈6 × 5–6 in × ≈10–10.5 in" and is labelled Low–Med under GAP-PROC-01.
- `PROC_DeliJar_Smalls`: 0.1549 × 0.1346 m and 0.2388 + 0.0254 m = 6.1 × 5.3 × 10.4 in. This is the published POP 4 L size (High). The cavity is ≈4.3 L. It has no band (house product); the label and tag are kept as the shop convention (Low).
- The fill is 6 layers to ≈0.23 m; GAP-PROC-08 is updated.
- **Reviewer fix (21d5b14):** PROC-003 named its new gap GAP-PROC-10, but PROC-004 (already on main) uses GAP-PROC-10 and GAP-PROC-11 for packaged sizes and labels. Renumbered to **GAP-PROC-12** in `deli_jar_smalls.json`, the handoff and `PROC_PIPELINE.md`. I also corrected PIPELINE's "7 layers ≈ 0.25 m" row. The regeneration changed only `manifest.json` (the gap key); every FBX and PNG stayed byte-identical.

## 5. LFS: PASS
All procedural FBX on the review branch are LFS pointers (checked with `git cat-file` on the index); the 3 new files included.

## 6. Unity: PASS
`unity-compile` passes (csErrors=0). `unity-test-edit` passes 163/163, including the updated `JarFillImportTests` (cavity + DEC-046 check on every step and LOD).
Scope check: no changes to `Code/Simulation|Presentation`, scenes or `studio.ps1`. The only code change is `Tests/EditMode/ProcArt/JarFillImportTests.cs`.

## 7. Interface for GAME-005: CLASH (must fix on the GAME-005 side)
GAME-005 (`claude/task-game-005-972696`, 3b0dc7e) branched from the PROC-002 state:
- **c1 Jar path.** GAME-005 adds `"unity_dir": ".../Procedural/DeliJar"` to `deli_jar.json`, commits its own `Procedural/DeliJar/PROC_DeliJar.fbx` (the old 0.15 × 0.28 m jar), and loads `{Proc}/DeliJar/PROC_DeliJar.fbx` in `SliceSceneBuilder.cs`. PROC-003 sets `unity_dir` to `.../Procedural/Jars` and ships both jars there. Merging both will conflict in `deli_jar.json` and `manifest.json`, and would leave two jar copies.
  - **Fix:** merge W4P first. GAME-005 then drops its `unity_dir` edit and its `DeliJar/` copy, and loads `{Proc}/Jars/PROC_DeliJar.fbx`.
- **c2 Label depth.** `SliceGame.JarLabel` hard-codes `faceZ = 0.0765` (half of the old 0.15 m depth + offset). The new canister is 0.1397 m deep, so its front face is at ≈0.0699 m and the label card at ≈0.0707 m. The text would float ≈6 mm in front of the jar.
  - **Fix:** set faceZ ≈ 0.0714, or derive it from the jar mesh bounds. `centreY` 0.092 still falls on the card (the label params are unchanged).
- **c3 Fill height.** The full fill is now ≈0.23 m (was ≈0.25 m) and the jar is shorter. GAME-005 should re-check any hard-coded heights; `SliceCaptureTests` uses `jar - up*0.25` for a camera point.
- **c4 Look names** (`PROC_JarFill_*`, 6 looks) and the step names are unchanged, so GAME-005's folder scan still works.

## 8. DEC-013: PASS
Before the run, 2 editors were open on other worktrees (review-w2c, task-game-001). The run waited, polling every 60 s (02:09–02:14), and started when 1 editor remained; this run made 2.

## Findings
**Blockers:** none for PROC-003 itself.
**Minor:**
- m1 GAME-005 interface clash c1–c3 above. The Hub should route it to GAME-005 or REVIEW-W4N(GAME-005) before that merges.
- m2 Hub registers **GAP-PROC-12** (smalls lid/corner/label) in KNOWN_GAPS. Also still unregistered from PROC-004: GAP-PROC-10/11.
**Notes:**
- n1 DarkCompact F070 is somewhat regular (see §3).
- n2 The handoff's [NEEDS-HUB] smalls fill: reusing `PROC_JarFill_*` is fine on volume (4.29 L vs 4.32 L). However, the smalls cavity is 5 mm shallower front to back (0.1266 m vs 0.1317 m inner) and 2.5 mm wider. The canister fill can therefore clip the smalls front/back walls by up to ≈2.5 mm per side. GAME can scale the fill to 0.96 in depth for smalls jars, or the Hub can order a smalls fill set. No test covers that fit.
- n3 The packet moved to `Docs/Tasks/Done/` via the merge.

## Validation
- Blender headless: 2 full runs on the merged tree, plus a third after the fix; sha256 as in §1.
- Contact sheets: 855 KB, 888 KB and 783 KB (≤1 MB).
- `studio.ps1 unity-compile`: pass, at commit 21d5b14.
- `studio.ps1 unity-test-edit`: pass, 163/163 (`Artifacts/TestResults/20261030-021510-863-19100-editmode.xml`).
- Main is not merged by this review. The Hub merges `review/wave-4p` (389628d + 21d5b14 + this file) on PASS.
