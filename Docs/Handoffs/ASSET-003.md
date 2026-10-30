# Handoff — ASSET-003 (2026-10-30): customer characters + animations sourcing

**Deliverables:** `Docs/Assets/Specs/CHARACTERS.md` (variation plan, tri budget, crowd LOD, Unity import steps), `Docs/Assets/fetch_list_characters.json`, ledger §1c (7 rows), 31 new manifest rows. No Unity work, no binaries in git.

## Fetched (cache `C:/Users/handl/Downloads/Dispo Game Assets Cache/quaternius/`, 56 MB)
- **CHR-QUA-UMM** Ultimate Modular Men (11 outfits, Humanoid-Rig FBX each + master .blend) and **CHR-QUA-UMW** Ultimate Modular Women (10 outfits + modular master FBX). Source: the pack page's Google Drive "Just give me the Download" links.
- **ANM-QUA-UAL1 / UAL2** Universal Animation Library 1 + 2, free Standard tiers (43 clips each, FBX + GLB, RM and non-RM). Source: itch's anonymous "No thanks, just take me to the downloads" flow. The link is signed and expiring, so these are `local` entries in the fetch list.
- Measured in Blender 5.2 (headless): men 5.2k–11.1k tris (modern outfits 5.2k–6.6k), 62 bones. Women 6.0k–7.9k tris, 51 bones. 4 meshes and 4–11 flat-colour materials per outfit. UAL: 65-joint UE-style skeleton. Every model has Humanoid-mappable bone names. Archives contain `License.txt` = CC0 1.0.
- 14 modern outfits (8 men, 6 women) → 16 curated presets × 3 palette rolls (spec §3).

## Mixamo verdict
The Adobe FAQ (updated 2021-09-14) says it is royalty-free for commercial video games, but it is **not CC0**. Raw redistribution is barred under Adobe's terms, and download needs an **Adobe ID**, which this task forbids. Under DEC-023 it would be `_LocalThirdParty/`-only, like the Unity EULA rows. **Not used**: ledger ANM-MIXAMO = REJECT for now. The CC0 UAL clips cover the P0 list.

## Validation
- `python -I Tools/Assets/fetch_assets.py --list Docs/Assets/fetch_list_characters.json` → 4 fetched. A re-run gives `cached: 4`.
- `python -I Tools/Assets/fetch_assets.py --verify` → 297 rows, 0 bad.
- FBX headers checked (`Kaydara FBX Binary`, `.blend` header). All 21 FBX import cleanly in Blender 5.2.

## Gaps (placeholders in the spec)
- GAP-ANM-1: there is no weight-shift idle in the free tiers. Recommendation: a tiny project-original additive pelvis-sway clip authored in Blender.
- Look-around is done procedurally with Humanoid look-at IK. Hand-over/receive = `Interact` / `PickUp_Table` + hand IK. No clip gap.
- Hats are baked into the Head meshes. Hat-less Worker/Farmer heads need a Blender delete pass.
- GAP-CHR-1: no visual cue for medical vs adult-use customers. Keep it UI-only.

## Questions for Nolan (through the Hub)
1. **Quaternius licence.** Source: `quaternius.com/license.html` (QAL v1.0, "regardless of the specific site or platform") vs each pack page, itch "License" field and bundled `License.txt` (all CC0 1.0). Options: (a) treat as CC0, so the files may enter git via LFS; (b) treat as QAL, import into `_LocalThirdParty/` only. The ledger and spec assume (b) for now. It is safe either way.
2. **Art direction.** Source: `CHR-QUA-UMM/Preview.jpg`, `CHR-QUA-UMW/Preview.jpg` in the cache. The people are low-poly and flat-shaded, which is stylised next to HDRP lookdev. Options: (a) accept for customers; (b) UBC realistic bodies (CC0, free tier unclothed) plus our own modern clothes in Blender (P1); (c) MPFB2/MakeHuman pipeline (P2, licence check needed).
3. **Staff uniform (GAP-CHR-2).** No reference shows what budtenders wear. Candidates: black/dark store tee, logo polo, lanyard. Placeholder: plain black top + dark trousers.

## Proposed packets
- **PROC-CHR-001 (Blender, no Unity slot):** batch script in `Tools/Blender/` that reads the cache FBXs and, for each §3 preset, joins Head/Body/Legs/Feet into one skinned mesh. It bakes the flat-colour materials onto a shared 256×64 palette strip, makes hat-less Worker/Farmer heads, generates LOD1 (≤3k) and LOD2 (≤1.2k) by Decimate, and exports `PF_Cxx.fbx` to the cache under `quaternius/derived/` with manifest rows. It also authors the GAP-ANM-1 sway clip. Validation: tri/material/bone counts per preset vs spec §5, plus a contact sheet.
- **GAME-CHR-002 (Unity, 1 editor slot, after PROC-CHR-001):** spec §8 steps 1–6: the cache→`_LocalThirdParty` copy script, Humanoid import, `AC_Customer` with look-at/hand IK, `PF_Customer_Cxx` prefabs with LODGroup, the spawner wired to the existing `CustomerState`/`PatienceState` (view only), the EditMode budget test, and a 12-customer perf capture vs PERF-001.

## Notes
- Itch anonymous download recipe (no account): GET the page → POST `/<slug>/download_url` (csrf) → GET the returned page → POST `/<slug>/file/<upload_id>?source=game_download` (csrf from that page, **no key param**) → JSON `url` (signed R2 link).
- The ledger's older LIB-QUA row (DEFER, QAL) is left as written. §1c explains the conflict.
