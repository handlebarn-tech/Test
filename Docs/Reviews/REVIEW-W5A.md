# REVIEW-W5A — ART-006 (HDRP bud materials + back rooms from ROOM_FIXTURES rev5)

**Verdict: PASS with minors (GO to merge).** `claude/task-art-006` @ c1ad023 merged `--no-ff` into `review/wave-5a` off main 33e57a1; clean merge. Code changes are Editor-only (`GrayboxBuilder.cs`, `GrayboxLayout.cs`, new `BudMaterials.cs`) plus the converter `Tools/Studio/room_fixtures_layout.py`, `graybox_layout.json`, four scenes, six bud material pairs and six FBX `.meta` remaps. No `Code/Domain/` or runtime edits.

## Gates (single editor via `studio.ps1`, DEC-013)
- `unity-compile` csErrors=0. `unity-graybox` on the merged tree: `unchangedScenes=4`, `bud materials: looks=6 remapped=0`, so the committed scenes and materials equal what the generator produces (idempotent).
- `unity-test-edit` **185/185**, which includes QA-002's `TfsParityGateTests` (Gate A, DEC-058/067) and the golden tests. `unity-test-play` 8 passed, 1 skipped (GPU capture). `unity-capture` graybox QA PASS (23 views, max deviation 0.22 ft), slice 11 shots.

## Checks
- **Positions vs ROOM_FIXTURES — PASS.** I compared the 72 converted fixture rects (centre and size) against `pos_ft` / `size_ft` in rev5: all match to 0.06 ft except two documented overrides: `Mops_Brooms_JC` at x 22.4 (the W4U m1 ruling; data still says 22.9) and the restroom storage cabinet at x 6.5–8.0, y 29.7–32.9, beside the door against the east wall (DEC-068). The cabinet clears the door span (y 33.1–36.1) and is Low under GAP-109. Skipped on purpose: `Lockers_Staff` (no position, GAP-126), `FOH_Props_Floor`, and the vestibule shell (a wall change). Door openings moved to the A011 spans.
- **Reproducible:** running the converter again produced the committed `graybox_layout.json` (a line-ending difference only).
- **Security/brands — PASS.** No keypad, safe or camera detail: `Panel_Blank` and the IT rack are plain boxes, and the legacy `FX_Office_Safe` box is removed. No brand names or logos. The bud materials are flat HDRP Lit colours from `jar_fill.json`, with no textures or downloaded assets ($0).
- **Bud looks — PASS.** In `SLICE_10_Jars_Closeup` the fills now render in colour (dark and light greens, purple, orange pistils) instead of the earlier white. Greens vs the dark compact look differ mainly by shade and bud shape, so all six are distinguishable but the three green looks are close.
- **Back-room captures — viewed, limited.** Office, Hall, Break room, FOH, BOH and HUB frames in the contact sheet show the new boxes at the CCTV camera positions, but the back rooms are unlit and very dark, and the FOH frame is dominated by one close brown block, so layout correctness rests on the data comparison above rather than on the images.

## Minors
- m1 Back-room readability: no room lighting yet (ART-003 lighting covers retail). A lit room sheet or top-down fixture overlay would let a reviewer check layouts by eye. `TOPDOWN_Plan.png` shows walls only.
- m2 REF must record DEC-068 in ROOM_FIXTURES (it still has `pos_ft: null` and the old "back wall" note) and the 22.4 mop x; the build overrides live in the converter script. The cabinet is 3.2 ft wide against 4 ft in the data (only 3.2 ft of wall).
- m3 No restroom CCTV exists, so the cabinet placement was checked in the layout, not against an image.
- m4 The standing desk is a full-height solid row (contains the file cabinets), fine for graybox; a leg/top split needs a REF size.
- m5 I ran the converter once by accident while reviewing; the file was restored, and the tree is clean.
