# CHARACTERS — customers (and later staff)

**Task:** ASSET-003 (2026-10-30). **Status:** sourcing + plan only; nothing imported into Unity yet.
**Governing decisions:** DEC-075 (≥ 10 distinct customers first, **≥ 50 by the end**). **DEC-084 (quality bar): realistic humans with realistic proportions, PBR skin and clothing and facial detail; never low-poly or stylised; performance comes from LODs, not from low-poly bases.** DEC-023 (licences and cache). DEC-033 (no questions to Nolan).
**Licence record:** `Docs/Assets/LICENSE_LEDGER.md` §1c. **Downloads:** `Docs/Assets/fetch_list_characters.json`, sha256 in `ASSET_CACHE_MANIFEST.json`, files in `C:/Users/handl/Downloads/Dispo Game Assets Cache/<source>/<ledger-id>/`.
**Rules kept:** $0, no account, **no real person's likeness** (so no photogrammetry scans of real people, §2), no customer PII, adults only (21+ store; Rocketbox's Children folder is never fetched).

> **Superseded (DEC-084):** the first version of this spec used Quaternius stylised low-poly packs (CHR-QUA-*, ANM-QUA-*). They stay in the cache and ledger, marked SUPERSEDED, and are **not used for customers or staff**.

## 1. Primary source: Microsoft Rocketbox Avatar Library (MIT)
- **What:** 115 hand-modelled, realistic, fully rigged avatars plus 417 mocap animations, made by the Rocketbox studio over 10 years. Microsoft released them under **MIT** (Nov 2020). The repository is archived (last push 2022-10-02); it is read-only but still downloadable.
- **Licence:** MIT ("Copyright (c) 2020 Microsoft"). Commercial use, modification and redistribution are allowed **as long as the copyright and permission notice ship with the copies**, so the game's third-party notices must include it. **Git:** DEC-023 admits only CC0/OFL into git, so Rocketbox files import into `_LocalThirdParty/` from the cache. The Hub may later extend the allow-list to MIT (handoff Q1).
- **Measured** (all 16 fetched, Blender 5.2): one skinned mesh each, **6.7k–9.3k tris** (women 8.3k–9.3k, men 6.7k–8.7k), 3 materials (body, head, hair-opacity). Real-world scale: women 1.73–1.77 m, men 1.81–1.87 m. **80-bone 3ds Max Biped** (`Bip01 …`), including eye, jaw, lip, cheek and eyebrow bones, so it maps to Unity Humanoid. Textures: **2K TGA** colour + normal + specular for head and body, plus a 2K RGBA hair/eyelash opacity map: 7 maps, ~93 MB per avatar uncompressed. A `_facial.fbx` variant adds blendshapes (15 visemes, 48 FACS, ARKit set). It is not fetched now; it is the hero-face upgrade (§5).
- **Usable pool for customers:** 80 adults after exclusions: Adults 40 (Female 17 + Party 2, Male 21) and Professions 40 (Business 11, Construction 9, Medical 8, Chef, Delivery, Gardener, Wood, Security 2, Sports 4). **Excluded:** Children (4), Fire (10), Military (8), Pilot (5), Police (8) (uniforms that confuse a store with ID checks), and swimwear (Sports_Female_01, Sports_Male_01). Security_* are kept for **staff**.
- **Fetched now (P0, 16 avatars, ~1.5 GB):** Female_Adult_01/03/04/08/12/14/17, Business_Female_03; Male_Adult_01/02/03/04/05/06/09/13, plus 50 animation files (§4) and the repo's LICENSE, README and `FixRocketboxMaxImport.cs`. The other 64 are in the fetch list as `blocked: P1` entries; a re-run fetches them once the roster grows.

**Honest gap vs DEC-084:** Rocketbox is realistic in proportions, faces and PBR-style 2K textures, but its geometry is last-generation (~8k tris, hair cards). Hands, ears and clothing silhouettes are visibly simpler than a modern hero character at the 1.5 m register distance. §2 lists the best higher-detail realistic sources and why none of them can replace Rocketbox for 50+ people today. §5 gives the upgrade path for the register close-up.

## 2. Shortlist (realistic first; exact licences)
| Candidate | Licence (exact) | Realism | Verdict |
|---|---|---|---|
| **Microsoft Rocketbox** (115 avatars + 417 anims) | MIT; notice required in copies | hand-modelled realistic, 2K PBR-style maps, ~8k tris | **P0 (fetched, 16)**; P1 = 64 more. The only free source with 50+ distinct realistic rigged adults |
| **MakeHuman / MPFB2** (Blender add-on, our own generator) | core/system assets (base mesh, targets, skins 01–03, system hair, eyebrows, clothes materials) **CC0**; some community packs **CC-BY** (e.g. eye materials 02/03, some beards): check per asset; MPFB code GPL (tool only) | realistic proportions, morphs for age/weight/height; skins up to 2K; clothing library weaker | **P1 upgrade path**: unlimited body variety plus true age and weight morphs; dress with CC0 MPFB clothes or our own Blender clothes. Use CC0 assets only, so no attribution |
| **CharMorph** Vitruvian base | **CC0** (Antonia, Reom: CC-BY; MB-Lab: AGPL, which propagates to outputs → reject) | realistic base, unclothed | P2: alternative base to MPFB; clothes and hair are our job |
| Sketchfab "Just man" (vrimen, uid e77a2677…) | CC BY 4.0 (CC Attribution) | modelled, 44.8k tris, 2K maps, rigged | P1 hero candidate: credit "Just man by vrimen (CC BY 4.0)" |
| Sketchfab "Joe – Realistic Human" (plan §16 #7) | CC BY 4.0 | modelled, game-ready | P1 hero candidate; same credit rule |
| Sketchfab Renderpeople free (Eric, Carla, Claudia, Nathan, Sophia), in3D iPhone scan, "Rigged T-Pose Human Male" (Mike Alger self-scan) | CC BY 4.0 on Sketchfab | photogrammetry, 16k–55k tris, very realistic | **REJECT: scans of real people**, which breaks the no-likeness rule. Renderpeople's own site terms are proprietary anyway |
| Sketchfab "Realistic Old Russian Guy" | CC BY 4.0 | realistic | **REJECT**: the author says it resembles a real named person |
| Mixamo | royalty-free in games, **not CC0**, Adobe ID required | mixed | Not used (ANM-MIXAMO) |
| Quaternius (all packs), Kenney, KayKit | CC0 / QAL conflict | stylised low-poly | **SUPERSEDED by DEC-084** |
| Unity Asset Store free realistic humans | Unity EULA (local-only) | varies | Not checked: needs an editor slot and Package Manager sign-in. A possible later supplement |

**Conclusion:** no free source provides 50+ distinct, realistic, modern, rigged adults under CC0. **Rocketbox (MIT) is the realistic option that reaches 50+ out of the box.** CC0-only realism means building our own people with MPFB2 (P1). CC BY can supply individual hero characters under DEC-023's existing CC BY handling (local import plus credits).

## 3. Variation system: 60 customers, readable at register distance

### 3.1 Base identities (the strongest cue is a different person)
At the register the player looks across the counter at head and torso from about 1.2–2 m. A different realistic face, hairstyle and outfit is by far the most readable difference, so the system is built on **distinct authored people first, variations second**.
- Rocketbox usable customer bases: **78** (the 80 adults minus the 2 security avatars kept for staff).
- **PS2 start: 16 bases = 16 customers**, no reuse (fetched now).
- **End target: 60 customers from ≥ 50 different bases.** Each base is used at most twice. A reused base must get a different colourway family **and** a different headwear-or-accessory, and the spawner never has both variants in the store at the same time.

### 3.2 Variation layers on top of a base
| Layer | Values | How (realistic, DEC-084) |
|---|---|---|
| Clothing colourway | 3 per base (original + 2) | Hue/value shift of the clothing regions of `body_color` only. A per-avatar clothing mask is painted from UV islands in a Blender batch script (skin, hair and face untouched). Normal and specular maps are kept, so fabric detail survives |
| Headwear | none, cap, beanie, bucket hat, hard hat (construction bases only) | Project-made **realistic** PBR props (2K, bevelled, stitched seams), rigid on `Bip01 Head` with a per-base offset table; hair cards trimmed or hidden under hats via a per-base hair-mask variant |
| Face/upper accessory | none, glasses, sunglasses, earbuds, crossbody bag, backpack, tote | Same: realistic project props on Head / Spine2 sockets |
| Build | slim / average / broad | Per-bone scale on `Bip01 Spine1/Spine2/Pelvis/UpperArm/Thigh` (Humanoid clips write no scale), with inverse compensation on `Neck/Head/Hand`. GAP-CHR-3: verify on the first prefab |
| Height | 0.95–1.05 of authored height | Root scale |
| Age read | the base decides (Rocketbox has young to older adults); older bases use `walk_slow_01` and speed 0.9 m/s | data |
| Behaviour | idle clip choice, phone vs look-around preference, anim speed 0.9–1.1 | data |

**Combinatorics:** 78 bases × 3 colourways × 5 headwear × 7 accessories × 3 builds ≈ 24,500 looks, but only distinctness at the register counts.

### 3.3 Readability rule (Rule D, register distance)
Register cue vector: **R0 base person** (face, hair, body; 78 values), R1 headwear (5), R2 top colourway family (10), R3 face/upper accessory (7), R4 build (3).
- Two roster entries with **different bases** are distinct by construction: different realistic face, hair and outfit cut.
- Two entries with the **same base** must differ in R2 **and** in R1 or R3, and may never be in the store at the same time.
- Roster quota for 60: ≥ 50 different bases, ≤ 10 reused once, 50/50 women/men, a spread of age reads (Rocketbox includes older adults: e.g. Male_Adult_03 grey-haired). Skin tones come from the bases' own authored variety, never tied to a role, outfit or behaviour. The pool includes bases in religious or cultural dress (Female_Adult_06/10/16, Male_Adult_15/19/21). They are ordinary customers, and no stat or behaviour is tied to appearance (handoff Q4).
- **Capacity:** 78 bases already exceed 60, so the target is met without any reuse. Colourways and accessories add headroom (to ~200 roster-legal identities) and stop the regulars looking cloned during a long shift.
- **Roster generator (DATA-CHR-001):** a seeded Python script → `customer_roster.json` (`C001…C060`: base, colourway, headwear, accessory, build, height, behaviour). It asserts Rule D and the quotas and exits non-zero on failure. The PS2 16 are its fixed prefix.
- **QA:** colour and **greyscale** contact sheets of all identities at the register framing (first-person camera, 1.5 m, store lighting). Pass = a reviewer confuses no pair.

### 3.4 First 16 (PS2) = the 16 fetched bases, each its own person
| # | Base | Reads as (from the library preview) |
|---|---|---|
| C01 | Female_Adult_01 | pink shirt, jeans |
| C02 | Female_Adult_03 | purple top, dark trousers |
| C03 | Female_Adult_04 | brown jacket, cargo trousers |
| C04 | Female_Adult_08 | grey tee, jeans |
| C05 | Female_Adult_12 | dark hoodie, shorts |
| C06 | Female_Adult_14 | grey cardigan |
| C07 | Female_Adult_17 | green tee, light jeans |
| C08 | Business_Female_03 | business skirt suit |
| C09 | Male_Adult_01 | tee, shorts |
| C10 | Male_Adult_02 | beige sweater |
| C11 | Male_Adult_03 | older, grey jacket |
| C12 | Male_Adult_04 | hoodie, jeans |
| C13 | Male_Adult_05 | utility vest |
| C14 | Male_Adult_06 | red long-sleeve |
| C15 | Male_Adult_09 | dark tee, jeans |
| C16 | Male_Adult_13 | argyle sweater |
The descriptions come from 200-px library thumbnails. The import task confirms them from the models.
GAP-CHR-1: medical vs adult-use customers have no visual cue. Keep it UI-only (MED badge).

## 4. Animation map (Rocketbox, MIT)
Idles, talk and props come from `all_animations_max_motextr_static` (in place: ANM-RB-STATIC, 32 files). Walks, starts/stops and turns exist only in the motion-extracted folders `…_xy` / `…_xyz` (ANM-RB-MOTION, 18 files). GAP-ANM-2: how their extracted root motion imports into Unity (root motion vs Bake Into Pose) must be checked on import (§8 step 4).
Every need is covered. f_/m_ variants exist for each and play on any avatar via Humanoid; use the matching sex for natural motion.
| Need | Clip (`f_`/`m_` prefix) |
|---|---|
| idle | `idle_neutral_01/02/03`, `idle_breathe_01` |
| shift weight | `idle_move_leg_01` (f), `idle_shake_leg_01` (m) |
| look around | `idle_look_around_01/02`, plus look-at IK toward shelves / menu board when browsing |
| wait / impatient | `idle_waiting_01` (+ `m_idle_waiting_02`) → `idle_nervous_01` as patience drops |
| phone | `cell_phone_textmessage` |
| talk at counter | `gestic_talk_neutral_01/02` |
| hand over (ID / cash) and receive (bag) | `documents_take` + right-hand IK to the counter point; prop parented to `Bip01 R Hand` |
| leave with bag | `walk_neutral_01` base + upper-body mask layer `hold_bag_idle` (m) / `hold_bag_idle_01` (f) |
| walk | `walk_neutral_01`, `walk_slow_01` (older), `walk_start/stop`, `turn_left/right_60/120_to_walk` |
| queue shuffle | `waiting_walk` |
| greet | `wave_01` |
GAP-ANM-1 (old) is closed: Rocketbox has weight-shift clips. The Quaternius UAL is superseded.

## 5. Budget (6 GB VRAM, ~12 on screen; PERF-001 frame budget ≤ 3 M tris, ≤ 2000 draws, GPU ≤ 12 ms)
| Item | Plan |
|---|---|
| LOD0 (≤ 5 m) | authored Rocketbox mesh, ~7.8k tris, 3 materials (+ ≤ 2 accessory props ≤ 6k tris each) |
| LOD1 (5–12 m) | Blender Decimate (planar + collapse, UV-seam safe) to ~4k; textures at 1K mip |
| LOD2 (> 12 m) | ~1.5k, shadows off, 2-bone skin weights, accessories hidden |
| Tris on screen | 12 × LOD0 worst case ≈ 12 × 12k = 144k: under 5 % of the 3 M budget. Geometry is not the constraint |
| Draw calls | ≈ 3 materials + 2 props = 5 per character → ~60 for 12, plus shadows; SRP Batcher compatible (per-identity material instances, **no MaterialPropertyBlock**) |
| VRAM | 7 maps × 2K per base, BC7 (colour, hair RGBA) / BC5 (normal) / BC4 (spec→smoothness): ≈ 25 MB per base with mips → 12 different people ≈ 300 MB. Texture mip streaming on (DEC-084), so LOD1/2 characters hold the 1K mip |
| Skin / hair shading | HDRP Lit **Specular Color** mode, using the authored specular maps. Skin regions get **subsurface scattering** (HDRP diffusion profile "Skin") via a skin mask from the same Blender batch. Hair cards: alpha-clip on opacity, HDRP Hair shader later if needed |
| **Register close-up upgrade (DEC-084)** | For the customer being served (≤ 2 m): load the `_facial.fbx` variant (blendshapes for blinks and visemes), a tiling skin-pore **detail normal** on the head (CC0, ambientCG/Poly Haven) instead of upscaling the 2K maps, and eye wetness/refraction. Optional P1: Blender Subdivision + Shrinkwrap on head and hands only for a ~15k-tri hero LOD |

## 6. Crowd LOD plan
- `LODGroup` per character (LOD0/1/2 + cull), screen heights 0.35 / 0.12 / 0.02.
- Animator `CullUpdateTransforms`. Beyond LOD1, update at half rate. IK and blendshapes only on the served customer and the next 2.
- Shadows off at LOD2; contact shadows only for LOD0.
- Spawner cap 12, no duplicate base in the store at the same time (78 bases ≫ 12).

## 7. Staff (later)
- **Security / door:** `Security_Male_01`, `Security_Female_01` (Rocketbox, realistic, P1 fetch).
- **Budtenders/managers:** Rocketbox Adults recoloured to the store uniform via the clothing mask. GAP-CHR-2: the real uniform is unknown; placeholder plain black top. No logo invented.

## 8. Unity import steps (integration packet; nobody does these yet)
1. **Copy to local:** a DEC-023 cache→project script (pattern: `Tools/Assets/lookdev_textures.py` `import_cache()`) copies each roster base (FBX + 7 TGA) and the animation FBXs into `UnityProject/Assets/_LocalThirdParty/Rocketbox/` (gitignored). The MIT `LICENSE.md` goes into the build's third-party notices.
2. **Materials:** port the logic of Rocketbox's `FixRocketboxMaxImport.cs` (cached under `rocketbox/LIC-RB-MIT/Editor/`, MIT): 3ds Max materials import with tint × texture and glassy hair, so remap to HDRP Lit (Specular Color, skin diffusion profile, hair alpha-clip). Write it as our own `Editor/Characters/RocketboxImport.cs` (HDRP, not Built-in).
3. **Model import:** Rig → **Humanoid**, *Create From This Model*. Unity auto-maps 3ds Max Biped; map eyes and jaw; leave facial bones unmapped. Enforce T-pose (the fix script does this). Scale: authored metres, check 1.55–1.95 m. Read/Write off.
4. **Animations:** Humanoid, *Create From This Model* (Bip01). Keep the §4 clips. Loop the idles and walks. Static set: Bake Into Pose (rotation, Y, XZ). `_xy`/`_xyz` walks and turns: first test whether the forward motion is on `Bip01` or on `MotionExtractionHelper` (GAP-ANM-2). Target: in-place walk cycle with the NavMeshAgent driving position, and speed matched to the clip so feet don't slide. `Footsteps` nodes are ignored.
5. **Controller** `AC_Customer` (Idle variants by random, Wait substate by patience, Talk, HandOver/Receive with upper-body mask, Walk blend, Turn-to-walk, LeaveWithBag layer; IK Pass on).
6. **Data, not 60 prefabs:** one `PF_Customer` (Animator + LODGroup + NavMeshAgent r 0.25, 1.2 m/s + `CustomerLook`). `CustomerIdentity` ScriptableObjects are generated from `customer_roster.json` (base, colourway material, props, build, behaviour). Presentation only: state stays in `Simulation/Slice`.
7. **Checks:** EditMode test that every identity has a valid Humanoid avatar, 3 LODs, ≤ 5 renderers, Rule D on the roster, and the MIT notice present in the notices file. PlayMode capture with 12 customers vs the PERF-001 baseline, plus the §3.3 contact sheets.

## 9. Open questions (through the Hub, see handoff)
- Q1 MIT into git? DEC-023 allows only CC0/OFL in git; Rocketbox stays local unless the Hub extends the allow-list (MIT is redistributable with its notice).
- Q2 Geometry gap: is Rocketbox's ~8k-tri realism (good textures, last-gen meshes) acceptable for PS2 customers, with the §5 close-up upgrade, or should MPFB2 (CC0, our generator) be started now as the main path?
- Q3 Staff uniform (GAP-CHR-2).
