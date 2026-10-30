# Handoff — ASSET-002 (2026-10-29)
**Deliverables:** `Tools/Assets/fetch_assets.py`, `Tools/Assets/make_chime.py`, `Docs/Assets/fetch_list_p0.json` (41 entries), `Docs/Assets/ASSET_CACHE_MANIFEST.json` (249 files, ~650 MB), LFS patterns in `.gitattributes`, `_LocalThirdParty/` in `.gitignore`, one ledger row `ORIG-CHIME`. Cache: `C:/Users/handl/Downloads/Dispo Game Assets Cache/<source>/<ledger-id>/`. No binaries in git.

## Fetched (41/41 P0 entries)
- **Poly Haven (20, CC0, 2k glTF / 2k HDR, md5-checked vs API):** marble_01, marble_tiles, fine_grained_wood, oak_veneer_05, concrete_floor_01, smooth_concrete_floor, asphalt_01, CashRegister_01, security_camera_01/02, korean_fire_extinguisher_01, potted_plant_04, fern_02, exterior_aircon_unit, modular_chainlink_fence, utility_box_01/02, security_light, HDRIs kloofendal_overcast_puresky + courtyard_night.
- **Kenney (CC0):** interface-sounds.zip (100 ogg), digital-audio.zip (60 ogg). Kept zipped.
- **Fonts (OFL, google/fonts raw):** Barlow 18 TTF + OFL.txt; Inter variable + italic + OFL.txt.
- **BigSoundBank (CC0):** AUD-BSB 2153.wav (metro 3-tone, weak match).
- **Sketchfab (15, CC BY 4.0, `redistributable: false`, glTF + license.txt):** 344514, dd3b0f, a73f64, da8bc0, bfeabe, a4216f, 938a9b, ab8d2a, 2273be, 79370d, 4324a9, 976c3f, caa8b3, e9832f, 8013c4 (485 MB; jar pack 236 MB, weed bud 135 MB). Fetched via the signed-in pane: `fetch('/i/archives/latest?archiveType=gltf&model=<uid>')` -> S3 link valid ~5 min -> download + unzip into `cache/sketchfab/<SK-id>/`. Rate limit: ~15 calls then 429 for ~2 min.
- **Brand-mark check** (all baseColor/diffuse/emissive viewed; result in `brand_check` per fetch-list entry): **SK-a4216f ATM `Screen2` has an "MTA" logo -> retexture before use**; **SK-a73f64 scale label reads "TrapoTron-600" + quick-guide text -> replace label**; the rest are clean (POS panel is generic UI, exit sign generic).
- **ORIG-CHIME:** project-original 2-note chime (E5->C5, 2.75 s), generated deterministically by `make_chime.py` (same sha256 on re-run). Ledger row added.

## Skipped (why)
- PH-marble_mosaic_tiles: in ACQUISITION_LIST but no ledger row -> not fetched.
- SK-7fbd47 extinguisher: list says "or"; took the CC0 PH extinguisher.
- PH material Displacement/EXR maps: the 2k glTF bundle only (diff, nor_gl, arm/rough); fetch others later if look-dev needs them.

## Blockers
1. Sketchfab: resolved 2026-10-29 (Hub signed the pane in).
2. **Unity Warehouse / UnityJapanOffice (P1 per ACQUISITION_LIST, packet item 3):** both owned (store says "You purchased this item on Oct 29"), signed in, but the store only offers **Open in Unity**; no browser download link, and `%APPDATA%/Unity/Asset Store-5.x/` does not exist yet. Needs the editor: Unity 6000.6.7f1 -> Window > Package Manager > My Assets -> Download (no Import) for each. Files then land in `%APPDATA%/Unity/Asset Store-5.x/Unity Technologies Japan/...`; add `local` entries pointing there (or copy into cache) and re-run. An agent can do this with computer-use only if the editor's Unity ID is signed in; counts against the 2-editor cap.

## Validation
- `python -I Tools/Assets/fetch_assets.py` re-run: `{'cached': 41, 'fetched': 0, 'blocked': 0, 'failed': 0}`, manifest byte-identical, no network for cached entries.
- `python -I Tools/Assets/fetch_assets.py --verify`: 249 rows, 0 bad (every row's file hash matches and its ledger ID exists in LICENSE_LEDGER.md).
- `git check-attr filter` -> lfs only under `UnityProject/Assets/_Game/Art/ThirdParty/`; `git lfs install --local` done.

## Notes
- Manifest `path` values are absolute cache paths; Sketchfab rows are `redistributable: false` (CC BY, DEC-023 -> `_LocalThirdParty/`). CC BY credits needed in game credits (author per ledger row).
- `.gitignore` edit is outside the packet's file list but is what DEC-023 requires; flag for review.
