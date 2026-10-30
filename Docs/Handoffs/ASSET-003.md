# Handoff — ASSET-003 (2026-10-30): customer characters + animations sourcing

**Deliverables:** `Docs/Assets/Specs/CHARACTERS.md` (sources, 60-customer variation system, readability rule, budget, crowd LOD, Unity import steps), `Docs/Assets/fetch_list_characters.json`, ledger §1c, manifest (515 rows, 0 bad). No Unity work, no binaries in git. Commits: be746d4 (v1), a320a38 (DEC-075 scaling), this one (DEC-084 realism).

## History of scope (from the Hub)
1. v1: CC0 stylised packs (Quaternius) → fetched.
2. DEC-075: ≥ 10 distinct customers at first, ≥ 50 by the end → variation system for 60.
3. **DEC-084: realistic humans, never low-poly or stylised; performance via LODs.** The primary source is now **Microsoft Rocketbox (MIT)**. All Quaternius rows are marked SUPERSEDED in the ledger (files stay in the cache, unused).

## Fetched for DEC-084 (cache `…/Dispo Game Assets Cache/rocketbox/`, 1.5 GB)
- **16 Rocketbox avatars** (8 women, 8 men; everyday clothes; one older man): FBX + 2K TGA colour/normal/specular (head, body) + 2K RGBA hair opacity. Measured in Blender 5.2: 1 mesh, **6.7k–9.3k tris**, 3 materials, 80-bone 3ds Max Biped (facial bones included), real scale 1.73–1.87 m. All FBX are binary and import cleanly; 112 TGA are present at full size.
- **50 Rocketbox mocap clips** (MIT): 32 in-place (idles, weight shift, look-around, waiting, nervous, phone, talk, `documents_take` for hand-over/receive, hold-bag, wave) + 18 motion-extracted (walk neutral/slow, start/stop, waiting-walk, turns). Every P0 animation need is covered; the old GAP-ANM-1 (weight shift) is closed.
- **LIC-RB-MIT:** the repo's LICENSE.md, README.md and `FixRocketboxMaxImport.cs`.
- The other **64 usable Rocketbox adults** are in the fetch list as `blocked: P1` entries. Drop the key and re-run to fetch (~93 MB each). Excluded for good: Children, Fire, Military, Pilot, Police, swimwear. Security_* is reserved for staff.

## Realistic-source findings (exact licences in ledger §1c)
- **Rocketbox (MIT):** the only free source with 50+ distinct, realistic, rigged, modern adults (80 usable). Not CC0: MIT requires the notice in shipped copies. Under DEC-023 it stays out of git (local import).
- **MPFB2 / MakeHuman:** system assets CC0 (base mesh, targets, skins, hair); some community packs CC-BY. This is the best **CC0** realistic route: our own generator with real age and weight morphs. It needs clothing work. P1.
- **CharMorph Vitruvian:** CC0 base, unclothed; P2. MB-Lab is AGPL, which propagates to outputs → never use.
- **Sketchfab CC BY modelled heroes:** "Just man" (vrimen, 44.8k tris), "Joe" (plan §16). These are P1 hero candidates with credits.
- **Rejected:** photogrammetry scans (Renderpeople free, in3D, a self-scan) and a model the author says resembles a named real person. They break the no-likeness rule.
- **Gap:** no CC0 source gives realistic, clothed, rigged modern adults at scale. Rocketbox geometry is last-gen (~8k tris) next to DEC-084's detail bar; its 2K textures and faces are realistic. The spec §5 close-up upgrade covers the register: facial blendshapes variant, skin detail normal, SSS, eyes, optional hero subdivision.

## Variation (spec §3)
78 customer bases → 60 customers from ≥ 50 distinct people, each base reused at most once. Layers on top: clothing colourways via Blender clothing masks, realistic project-made headwear and accessories, bone-scale builds, height, behaviour. Rule D: a different base = distinct. A same-base pair must differ in colourway family plus headwear or accessory, and is never in the store together. PS2 uses the 16 fetched bases, one person each.

## Validation
- `python -I Tools/Assets/fetch_assets.py --list Docs/Assets/fetch_list_characters.json` → `{'cached': 24, 'fetched': 1, 'blocked': 64, 'failed': 0}` on the last run (all P0 fetched).
- `python -I Tools/Assets/fetch_assets.py --verify` → 515 rows, 0 bad.
- Blender 5.2 headless import of all 16 avatars plus a sample clip: mesh, rig, tris and height recorded above.

## Gaps (placeholders in the spec)
- GAP-ANM-2: `_xy`/`_xyz` walk clips. How their extracted root motion maps into Unity has to be checked at import.
- GAP-CHR-3: bone-scale builds need a visual check on the first prefab.
- GAP-CHR-1: no visual medical cue (UI-only MED badge).
- Library thumbnails were only 200 px, so the outfit descriptions in spec §3.4 need confirming from the models at import.

## Questions for Nolan (through the Hub)
1. **MIT into git?** DEC-023 admits only CC0/OFL; Rocketbox is MIT (redistributable with notice). Options: (a) keep it local-only (current plan, works); (b) extend the allow-list to MIT with the notice file.
2. **Geometry gap.** Source: any `rocketbox/CHR-RB-*/Export/*.fbx` (6.7k–9.3k tris, 2K maps). Is Rocketbox plus the close-up upgrade acceptable for customers, or should MPFB2 (CC0, our generator, higher-poly bodies, real age/weight morphs) start now as the main path, with Rocketbox as crowd/background? Recommendation: Rocketbox for PS2 (it exists today, 50+ people); run MPFB2 as a P1 R&D packet and compare at the register.
3. **Staff uniform (GAP-CHR-2):** no reference shows what budtenders wear. Placeholder: plain black top.
4. **Cultural garments:** the Rocketbox pool includes women in hijab/niqab/burqa and men in thobe/keffiyeh (Female_Adult_06/10/16, Male_Adult_15/19/21). Plan: they are in the pool as ordinary customers, with no behaviour or stats tied to appearance. The Hub may remove them if it disagrees.

## Proposed packets
- **PROC-CHR-001 (Blender, no Unity slot):** batch script in `Tools/Blender/` over the cached Rocketbox bases. It paints clothing masks and skin masks per base from UV islands/colour (for colourways and SSS), builds LOD1 (~4k) / LOD2 (~1.5k) by Decimate, and makes realistic headwear/accessory props (2K PBR) with a per-base socket-offset table. Output: `rocketbox/derived/` + manifest rows. Validation: per-base LOD tris, mask contact sheet.
- **DATA-CHR-001 (Python, parallel):** seeded roster generator → `customer_roster.json` (60), with Rule D and quota self-check; the PS2 16 as its prefix.
- **GAME-CHR-002 (Unity, 1 editor slot, after PROC-CHR-001):** spec §8 steps 1–7: cache→`_LocalThirdParty` copy, HDRP Rocketbox import script (port of the MIT fix script), Humanoid avatars, `AC_Customer`, `PF_Customer` + `CustomerIdentity` assets, spawner hookup (view only), EditMode tests, perf capture vs PERF-001, register contact sheets, MIT notice in third-party notices.
- **R&D-CHR-003 (Blender, P1):** MPFB2 CC0-only pilot: 4 customers with our own modern clothes, compared at register distance against Rocketbox.

## Notes
- The itch anonymous download recipe and the Quaternius licence conflict are kept in ledger §1c for the superseded rows.
