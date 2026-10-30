# PROC-007 — DEC-097 UV layout: lightmap UV on channel 1, label UV on channel 2

**Dept:** Assets · **Role:** PROC · **Priority:** P1 · **Owner:** — (launch after PROC-005 merges; both edit the shared exporter) · **Reviewer:** Unity A from the pool · **Touches:** none · **Interfaces:** DEC-097, agreed with the World lead 2026-10-30: Unity `uv` = base, `uv2` = lightmap, `uv3` = label; `generateSecondaryUV` stays 0. Assets sends World the accepted PROC-007 commit; World's ART shader task reads `uv3` against it; the Hub merges both in one wave. Unity slot: borrowed from World when ART-007 is not in Unity (ask first)

## Goal
Every generated mesh exports UV0 = base, UV1 = a dedicated non-overlapping lightmap UV (DEC-084 "UV2"), UV2 = `UVMap_Label` where it exists. Re-export jars, jar fill and packaged goods in the same wave.

## Rules
- Change the shared export path once (`Tools/Blender/` runner/proclib), not per generator. Lightmap UV: no overlaps, padding suited to 1–2K lightmaps; add a validation check (exists, in 0–1, no overlap).
- Unity import keeps "Generate Lightmap UVs" off (`generateSecondaryUV: 0` in the `.meta` files under `_Game/Art/Procedural/`).
- Only the UV layout and the export hashes may change; geometry, materials and names stay the same (diff vertex counts and bounds against the old FBX).
- Update `Code/Tests/EditMode/ProcArt/PackagedGoodsImportTests.cs` (label is now Unity `uv3`; add a check that `uv2` is the lightmap UV), plus the JarFill tests where relevant.

## Deliverables
Exporter change + validation check; re-exported FBX (LFS) + manifest; updated tests; `Docs/Handoffs/PROC-007.md` naming the commit World's shader cut-over must land with.

## Validation
Blender validation passes for every family; ProcArt EditMode tests green via `studio.ps1` (needs one Unity slot, borrowed from World).
