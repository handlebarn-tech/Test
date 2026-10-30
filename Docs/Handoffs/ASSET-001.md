# Handoff — ASSET-001 (2026-10-29)
**Deliverables:** `Docs/Assets/LICENSE_LEDGER.md` (≈108 verified rows + 69 Sketchfab, 52 Poly Haven), `Docs/Assets/ACQUISITION_LIST.md`. No assets downloaded; `UnityProject/` untouched.

## Method
Poly Haven license page + public API; Sketchfab public model API (license, author, tris) for every Sketchfab URL in ASSET_PRODUCTION_PLAN.md; license pages for Unity, Quaternius, MakeHuman, Sonniss, Pixabay, Kenney, ambientCG, BigSoundBank, Google Fonts OFL. Visit date 2026-10-29.

## Findings that change the plan
- **Poly Haven covers more than the plan used:** `CashRegister_01` (CC0) replaces the CC BY registers; also cardboard box, crates, carts, extinguisher, microwave, trash, cleaning bottles, electrical box.
- **Rejected:** Niclas basemesh (404), BlueOxel A/C (CC BY-SA), hdyeah register (Sketchfab "Free Standard"), 7 over-heavy models (≤3.3M tris).
- **Unverified:** plaggy "CC0 Jar" on Fab (403, no listing found) → use Yusuf jar or model custom; CMU mocap (not checked).
- **Quaternius is QAL v1.0, not CC0** (no redistribution as assets).
- **Redistribution:** Unity EULA, Sonniss v2.0, Quaternius QAL, Pixabay forbid redistributing raw files → keep raws out of git. Only CC0 sources are safe to commit.
- Unity Warehouse: 936.8 MB, built for 2022.3, HDRP-only → test on Unity 6000.6. UnityJapanOffice: 3.3 GB → extract prefabs only.
- Door chime: only a CC0 subway bell found (poor match); consider synthesizing.

## Limits
Sketchfab sizes unknown until download (tris recorded); Sketchfab provenance = uploader-declared license only — do a visual provenance/brand-mark check at import. Unity EULA text not re-read.

## Needs Nolan
Unity Asset Store EULA/My Assets (Warehouse, Office), Sketchfab login for downloads (see ACQUISITION_LIST "Human-only steps").
## Next
Fetch task (P0 list), then Blender normalize per plan §73.
