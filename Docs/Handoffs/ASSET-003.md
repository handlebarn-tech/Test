# Handoff — ASSET-003 (2026-10-30): customer characters + animations sourcing

**Deliverables:** `Docs/Assets/Specs/CHARACTERS.md` (variation plan, tri budget, crowd LOD, Unity import steps), `Docs/Assets/fetch_list_characters.json`, ledger §1c (9 rows), 51 new manifest rows. No Unity work, no binaries in git.

## Scope change (DEC-075, Hub message 2026-10-30)
Nolan wants ≥ 10 distinct customers at first and **≥ 50 by the end**. The spec now designs for a 60-identity roster (headroom to 100+). It adds a register-distance readability rule (Rule D, spec §3.4), the combinatorics (354 shape-distinct head-silhouette × top pairs before any colour), and a seeded roster generator with a pairwise self-check. To widen the everyday garments it also fetches **CHR-QUA-AM / CHR-QUA-AW** (Quaternius Animated Men/Women, CC0): tees, long-sleeve, dress, tank top, and an older man.

## Fetched (cache `C:/Users/handl/Downloads/Dispo Game Assets Cache/quaternius/`, 91 MB)
- **CHR-QUA-UMM** Ultimate Modular Men (11 outfits, Humanoid-Rig FBX each + master .blend) and **CHR-QUA-UMW** Ultimate Modular Women (10 outfits + modular master FBX). Source: the pack page's Google Drive "Just give me the Download" links.
- **ANM-QUA-UAL1 / UAL2** Universal Animation Library 1 + 2, free Standard tiers (43 clips each, FBX + GLB, RM and non-RM). Source: itch's anonymous "No thanks, just take me to the downloads" flow. The link is signed and expiring, so these are `local` entries in the fetch list.
- **CHR-QUA-AM / AW** Animated Men (4) / Women (4), flat + Smooth FBX each (Drive links from the pack pages).
- Measured in Blender 5.2 (headless): men 5.2k–11.1k tris (modern outfits 5.2k–6.6k), 62 bones. Women 6.0k–7.9k tris, 51 bones. 4 meshes and 4–11 flat-colour materials per outfit. AM/AW: single mesh, 42 bones, one material per garment, flat 1.8k–2.8k / smooth 6.4k–8.8k tris. UAL: 65-joint UE-style skeleton. No pack has shape keys, so body types use per-bone scale (spec §3.3, GAP-CHR-3). Every model has Humanoid-mappable bone names. Archives contain `License.txt` = CC0 1.0.
- 22 modern top garments (12 men, 10 women) across 4 families. Hair, hats, beards and earrings split out of the head meshes. First 16 identities hand-picked for PS2; 60 generated later (spec §3).

## Mixamo verdict
The Adobe FAQ (updated 2021-09-14) says it is royalty-free for commercial video games, but it is **not CC0**. Raw redistribution is barred under Adobe's terms, and download needs an **Adobe ID**, which this task forbids. Under DEC-023 it would be `_LocalThirdParty/`-only, like the Unity EULA rows. **Not used**: ledger ANM-MIXAMO = REJECT for now. The CC0 UAL clips cover the P0 list.

## Validation
- `python -I Tools/Assets/fetch_assets.py --list Docs/Assets/fetch_list_characters.json` → 6 entries fetched (2 added after DEC-075).
- `python -I Tools/Assets/fetch_assets.py --verify` → 317 rows, 0 bad.
- FBX headers checked (`Kaydara FBX Binary`, `.blend` header). All 37 FBX import cleanly in Blender 5.2. Part and material names for the hair split were read from the modular masters.

## Gaps (placeholders in the spec)
- GAP-ANM-1: there is no weight-shift idle in the free tiers. Recommendation: a tiny project-original additive pelvis-sway clip authored in Blender.
- Look-around is done procedurally with Humanoid look-at IK. Hand-over/receive = `Interact` / `PickUp_Table` + hand IK. No clip gap.
- Hats are baked into the Head meshes. Hat-less Worker/Farmer heads need a Blender delete pass.
- GAP-CHR-3: bone-scale builds need a visual check on the first prefab; fallback is a Blender broad-body variant.
- GAP-CHR-1: no visual cue for medical vs adult-use customers. Keep it UI-only.

## Questions for Nolan (through the Hub)
1. **Quaternius licence.** Source: `quaternius.com/license.html` (QAL v1.0, "regardless of the specific site or platform") vs each pack page, itch "License" field and bundled `License.txt` (all CC0 1.0). Options: (a) treat as CC0, so the files may enter git via LFS; (b) treat as QAL, import into `_LocalThirdParty/` only. The ledger and spec assume (b) for now. It is safe either way.
2. **Art direction** (now also: smooth or flat shading for F3/F4). Source: `CHR-QUA-UMM/Preview.jpg`, `CHR-QUA-UMW/Preview.jpg` in the cache. The people are low-poly and flat-shaded, which is stylised next to HDRP lookdev. Options: (a) accept for customers; (b) UBC realistic bodies (CC0, free tier unclothed) plus our own modern clothes in Blender (P1); (c) MPFB2/MakeHuman pipeline (P2, licence check needed).
3. **Staff uniform (GAP-CHR-2).** No reference shows what budtenders wear. Candidates: black/dark store tee, logo polo, lanyard. Placeholder: plain black top + dark trousers.

## Proposed packets
- **PROC-CHR-001 (Blender, no Unity slot):** batch script in `Tools/Blender/` (spec §3.2). It splits hair, headwear, beard and earrings out of every head and remaps all named materials to palette-strip UVs. It builds the Blender-made accessories (cap, beanie, bucket hat, glasses, sunglasses, tote, shoulder bag, women's earrings; ≤ 400 tris each), Decimate LOD1/LOD2 for F1/F2, the cross-family hair fit table, and the GAP-ANM-1 sway clip. Output goes to `quaternius/derived/` with manifest rows. Validation: per-part tri/material counts vs spec §5, plus a parts contact sheet.
- **DATA-CHR-001 (Python, no Unity slot; can run in parallel):** the seeded roster generator (spec §3.4) → `customer_roster.json` with 60 identities, the PS2 16 as a fixed prefix, and a Rule D pairwise self-check.
- **GAME-CHR-002 (Unity, 1 editor slot, after PROC-CHR-001):** spec §8 steps 1–7: the cache→`_LocalThirdParty` copy script, Humanoid import, `AC_Customer` with look-at/hand IK, 4 family prefabs + `CustomerIdentity` assets from the roster, the spawner wired to the existing `CustomerState`/`PatienceState` (view only, no duplicate identity in the store), the EditMode budget + Rule D test, a 12-customer perf capture vs PERF-001, and colour/greyscale register contact sheets.

## Notes
- Itch anonymous download recipe (no account): GET the page → POST `/<slug>/download_url` (csrf) → GET the returned page → POST `/<slug>/file/<upload_id>?source=game_download` (csrf from that page, **no key param**) → JSON `url` (signed R2 link).
- The ledger's older LIB-QUA row (DEFER, QAL) is left as written. §1c explains the conflict.
