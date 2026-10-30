# PROC-007 — DEC-097 UV layout: lightmap UV on channel 1, label UV on channel 2

**Role:** PROC · **Priority:** P1 · **Owner:** — (launch after PROC-005 merges; both edit the shared exporter) · **Reviewer:** fresh, Hub-spawned (STUDIO_OS §0.7) · **Touches:** none · **Interfaces:** DEC-097, agreed 2026-10-30 (DEC-097): Unity `uv` = base, `uv2` = lightmap, `uv3` = label; `generateSecondaryUV` stays 0. the ART label-shader task reads `uv3` against the accepted PROC-007 commit; the Hub merges both in one wave. Unity slot per DEC-013

## Goal
Every generated mesh exports UV0 = base, UV1 = a dedicated non-overlapping lightmap UV (DEC-084 "UV2"), UV2 = `UVMap_Label` where it exists. Re-export jars, jar fill and packaged goods in the same wave.

## Rules
- The ChatGPT drops (rounds 3–6) order UV maps base, label, lightmap, which is the reverse of DEC-097. The runner check must enforce the DEC-097 order and fail anything else (IMP-003 R3b.0.4).
- Change the shared export path once (`Tools/Blender/` runner/proclib), not per generator. Lightmap UV: no overlaps, padding suited to 1–2K lightmaps; add a validation check (exists, in 0–1, no overlap).
- Unity import keeps "Generate Lightmap UVs" off (`generateSecondaryUV: 0` in the `.meta` files under `_Game/Art/Procedural/`).
- Only the UV layout and the export hashes may change; geometry, materials and names stay the same (diff vertex counts and bounds against the old FBX).
- Update `Code/Tests/EditMode/ProcArt/PackagedGoodsImportTests.cs` (label is now Unity `uv3`; add a check that `uv2` is the lightmap UV), plus the JarFill tests where relevant.

## Deliverables
Exporter change + validation check; re-exported FBX (LFS) + manifest; updated tests; `Docs/Handoffs/PROC-007.md` naming the commit World's shader cut-over must land with.

## Validation
Blender validation passes for every family; ProcArt EditMode tests green via `studio.ps1` (needs one Unity slot, borrowed from World).

## Read
`CLAUDE.md` → this packet, then only: `Docs/DECISIONS.md` DEC-084/097; `Docs/Assets/Specs/PROC_PIPELINE.md` (export path, validation layer); `Docs/Imports/IMP-003_PROC_FIX_CHECKLIST.md` R3b.0.4; `Docs/Handoffs/PROC-005.md` (families and manifest on main).

## Owns
`Tools/Blender/` runner/proclib export + validation code and params; `Art/Exports/Procedural/**` re-exports + manifest; `UnityProject/Assets/_Game/Art/Procedural/**/*.meta` (`generateSecondaryUV` only); `Code/Tests/EditMode/ProcArt/`; `Docs/Handoffs/PROC-007.md`. Not the Lookdev shader (ART-011).

## Handoff
`Docs/Handoffs/PROC-007.md` (≤40 lines): the commit ART-011 must land with, per-family vertex/bounds diff result, validation output paths. Uncertainty: STUDIO_OS §0.6 first; one line to the Hub when done.
