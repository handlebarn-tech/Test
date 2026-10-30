# CHARACTERS — customers (and later staff)

**Task:** ASSET-004 (2026-10-30), rewrite of the ASSET-003 spec. **Status:** MPFB2 pipeline built; 58 of 60 roster customers exported to the cache with 0 validation errors. Nothing is imported into Unity yet (GAME-CHR-002).
**Governing decisions:** DEC-075 (≥ 10 distinct customers first, **≥ 50 by the end**). **DEC-084 (quality bar): realistic humans with realistic proportions, PBR skin and clothing and facial detail; never low-poly or stylised; performance comes from LODs, not from low-poly bases.** **DEC-087: MPFB2 (CC0, our generator) is the main customer path; Rocketbox (MIT) is the interim/PS2 crowd and background set; MIT is on the DEC-023 allow-list.** DEC-089 (staff uniform). DEC-023 (licences and cache). DEC-033/098 (questions go up the chain, never to Nolan directly).
**Rules kept:** $0, no account, **no real person's likeness** (no scans of real people; MPFB bodies are morph blends of the CC0 base mesh, faces are seeded target mixes, §3), no customer PII, adults only (21+ store).
**Licence record:** `Docs/Assets/LICENSE_LEDGER.md` §1d (MPFB2), §1c (Rocketbox). **Downloads:** `Docs/Assets/fetch_list_mpfb.json`, sha256 in `ASSET_CACHE_MANIFEST.json` (fetched packs + derived customers), files in `C:/Users/handl/Downloads/Dispo Game Assets Cache/mpfb/`.

> **Superseded:** Quaternius stylised packs (DEC-084) and the Rocketbox-first plan of the ASSET-003 spec (DEC-087). Rocketbox stays as the interim crowd (§8). Quaternius stays in the cache and ledger marked SUPERSEDED, unused.

## 1. Sources and licence gate
- **Tool:** MPFB 2.0.18 (Blender extension, GPL; a tool only, nothing GPL ships). sha256 matches extensions.blender.org. Installed into an **isolated Blender profile** at `<cache>/mpfb/blender_user` (`BLENDER_USER_RESOURCES`, set by `blender.ps1 character`). The user's own Blender profile is never touched.
- **Assets:** 17 MakeHuman CC0 packs (base mesh, targets, skins, eyes, brows, lashes, teeth, hair, clothes, proxies) listed in `fetch_list_mpfb.json`.
- **Per-asset licence index:** `install_mpfb.py` extracts the packs and reads every unit's own licence header (`.mhclo`/`.mhmat`/`.mhskel`/`.target` "license" lines). A unit is **allowed only if every file in it is CC0**. Result: **106 units refused**, because several packs labelled `_cc0` contain AGPL- or CC-BY-headed files (some skins, alternative hair and suit materials, and community hair, beards, glasses, a cap and pants whose MakeClothes header says `# license AGPL3`; the first audit missed that header form and was fixed on the ASSET-004 resume). Refused units stay refused; the roster self-check and every export re-audit against the index (`dispo_licence_index.json` in the profile's data dir).
- **Curated pools** (`Tools/Blender/params/customers_mpfb.json`): realistic modern adults only (DEC-084). Costume, novelty, political, historical and "crude" items are left out on purpose. 34 skins, 12 men's and 11 women's outfits, 5 men's hairstyles + shaved and 9 women's hairstyles, 1 hat (fedora), 4 glasses, **no beards** (both CC0-labelled beards are AGPL-headed, GAP-CHR-9). `toigo_stiletto_booties` (44.7k tris) and `toigo_flats` (57.6k) are out of every outfit for the tri budget (replaced by ankle boots / ballet flats). The men's height macro is capped at 0.65 (0.66–0.75 gave 2.04–2.10 m bodies). Height is measured over the body and clothes, without hair or hat (clothing masks delete the covered body vertices, so the body alone is not measurable).

## 2. Pipeline
| Step | Tool | Output |
|---|---|---|
| 1. Install | `python -I Tools/Blender/characters/install_mpfb.py` | add-on + CC0 data in the isolated profile; licence index |
| 2. Roster | `python -I Tools/Blender/characters/roster.py` | `Docs/Assets/Specs/customer_roster_mpfb.json` (60 customers). Self-check: quotas, Rule D, CC0 audit, unique faces, determinism. Exits non-zero on any error |
| 3. Build + export | `Tools/Blender/blender.ps1 character Tools/Blender/params/customers_mpfb.json [C001,C002]` (headless, ~11 s per customer) | `<cache>/mpfb/derived/<id>/`: `<id>.fbx`, `textures/`, `<id>.validation.json`, previews `<id>_head/_lod0/_lod3.png`; `summary.validation.json` |
| 4. Contact sheet | `python -I Tools/Blender/characters/contact_sheet.py` | `Docs/Assets/Specs/customers_mpfb_contact_sheet.jpg` (register framing, all exported customers) |

**Per customer (`customer_gen.py`):** MPFB `HumanService` builds the human from the roster entry (phenotype macros: sex, age, weight, muscle, height, proportions, cup size, firmness, ancestry blend; ~30 seeded face targets; skin; eyes; brows; lashes; teeth; hair; outfit items; hat/glasses/beard as proxies). Shape keys and masks are baked; the Armature modifier stays. MPFB's Blender-only node trees are replaced by a **Principled BSDF on the asset's own textures** (copied next to the FBX, not embedded). Hair, brows and beard are **recoloured to the roster's hair tint** (§3.2). LODs are built (§4), the `game_engine` rig is kept, and one FBX is exported (Y-up, -Z forward, metres, no leaf bones, deform bones only). Any validation error makes Blender exit 10.

**Validation JSON** per customer: identity, CC0 audit of every asset unit, tris per LOD vs budget, LOD1 tris per part, bones and Humanoid-required bones, height vs the sex's range, materials with texture files and pixel sizes, gaps, FBX sha256, pipeline versions.

**Determinism:** the roster is seeded (`seed` 20261030). A rebuild gives the same people; FBX bytes can differ by timestamps, so compare the validation tris/heights, not the sha256, across runs.

## 3. Variation system: 60 customers, readable at register distance
At the register the player looks across the counter at head and torso from about 1.2–2 m, so every customer is a **different person** (body, face, skin, hair, outfit), never a recolour of another.

### 3.1 Roster quotas (enforced by `roster.py`)
- **Size 60** (DEC-075 end target ≥ 50). Sex 30/30. Age bands young 21–29 / adult 30–54 / older 55–80 = 15/30/15 (MPFB age 0.42–0.53 / 0.54–0.72 / 0.73–0.92).
- **Ancestry ~12 × 5** (African, East Asian, Caucasian, South Asian, Eurasian; current roster 12/12/13/11/12), balanced within what each sex and age band has CC0 skins for. Skin tone is never tied to a role, outfit or behaviour. Phenotype ancestry blends: `ancestry_race` in params.
- **Builds** slim / average / heavy (weight and muscle macro ranges). Height per sex 1.45–1.85 m (f), 1.60–1.95 m (m), checked on export.
- **Formal ≤ 20 %** (suits and elegant dress read as staff/office; W5P m3). Hats 10 %, glasses 30 %, beards ~30 % of non-young men once a CC0 beard exists (pool empty now, GAP-CHR-9). Current roster: 6 hats, 21 glasses, 0 beards, 6 shaved heads; builds 21 slim / 19 average / 20 heavy.
- Eyes: mostly brown for non-Caucasian skins (85 %), otherwise from the 8 CC0 eye materials.

### 3.2 Hair tint
Tints: black, dark brown, brown, auburn, blond, grey, white. Older customers are grey or white; non-Caucasian skins are black or dark brown 85 % of the time. Current roster: dark brown 24, black 12, white 11, brown 5, grey 4, blond 3, auburn 1.
**How:** `customer_gen.tint_texture` recolours the hair, eyebrow and beard diffuse in Blender: it keeps the texture's luminance pattern and alpha and moves its mean colour to the tint's sRGB value (`hair_tint_srgb` in params). The tinted copy is written as `<texture>_<tint>.png` and the material is named `M_<asset>_<tint>`, so Unity's by-name material extraction never merges two tints. Eyelashes keep their own texture. No runtime tint shader is needed.

### 3.3 Readability rule (Rule D, register distance)
Register cues: sex, age band, skin, head (hair or hat), top outfit, glasses, beard, build. Shape cues: head, outfit, glasses, beard, build.
**Rule D:** every pair of customers differs in **≥ 3 register cues, at least one of them a shape cue.** On top of that, every face is a different seeded target mix (the self-check rejects duplicate faces).
**QA:** the committed contact sheet (§2 step 4) shows every exported customer at register framing (head and shoulders). Pass = a reviewer confuses no pair. A greyscale pass in store lighting belongs to GAME-CHR-002.

## 4. Budgets
| Item | Budget | Measured (58 customers) |
|---|---|---|
| LOD0 (served customer, ≤ 3 m) | ≤ 150k tris; body subdivided once, all parts | 81–127k (mean 100k) |
| LOD1 (3–8 m) | ≤ 60k; MPFB base resolution, teeth dropped | 26–60k (mean 38k) |
| LOD2 (8–15 m) | ≤ 20k; Decimate 0.32, brows/lashes/teeth dropped | 8.3–18.9k (mean 12k) |
| LOD3 (> 15 m) | ≤ 6k; Decimate 0.10, eyes/glasses/mouth parts dropped | 2.4–5.4k (mean 3.5k) |
| Rig | MPFB `game_engine`, 53 bones, Unity Humanoid-compatible names (`pelvis`, `spine_01…`, `upperarm_l…`) | 53 bones each; all 17 Humanoid-required bones present |
| Height | f 1.45–1.85 m, m 1.60–1.95 m | f 1.50–1.75 m, m 1.61–1.95 m (C028/C054 at 1.59 m deferred) |
| Materials | one per part (skin, eyes, brows, lashes, teeth, hair, each clothing item, proxies) | 7–11 per customer |
| Textures | target ≥ 2K for skin, hair and clothes colour/normal | see §5 gaps |

**On screen (PERF-001: ≤ 3 M tris, ≤ 2000 draws, GPU ≤ 12 ms):** 12 customers with the served one at LOD0, 3 at LOD1 and 8 at LOD2 ≈ 110k + 135k + 120k ≈ 365k tris (12 %). Worst case, all 12 at LOD1 ≈ 540k. Draws ≈ materials per customer (~8–11) × 12 ≈ 130 plus shadows. LOD0 is used only for the served customer.
**VRAM:** per customer a 2K skin (≈ 5.3 MB BC7 with mips), clothes 2K–4K colour + normals, hair/eyes/brows ≤ 1K: ≈ 20–40 MB per distinct person. Texture mip streaming on (DEC-084).

## 5. Texture gaps (candidates are CC0 or our own work; nothing invented)
- **GAP-CHR-4 Skin normals.** Most CC0 skins are a 2K diffuse with no normal, specular or SSS map. Candidates: (a) a tiling skin-pore **detail normal** made in Blender from procedural noise (our own, CC0 by construction), applied as the HDRP detail map; (b) a CC0 tiling skin/leather-pore normal from ambientCG or Poly Haven if one fits (not yet checked); (c) HDRP diffusion profile "Skin" for SSS, no texture needed.
- **GAP-CHR-5 Eyes 1K.** The CC0 eye materials are 1K. At register distance an iris covers a few dozen pixels, so 1K is likely enough. Candidate if not: a procedural iris baked at 2K in Blender, plus HDRP eye wetness.
- **GAP-CHR-6 Brows and lashes 512 px.** Candidates: other CC0 eyebrow/eyelash units already in the licence index (to be compared), or our own alpha cards painted in Blender at 1K.
- **GAP-CHR-7 Shoes, keyhole tank top and fedora normal are 1K** (measured on the 58 exports; all hair in the licence-clean pool is ≥ 2K). Shoes are rarely visible across the counter (low priority); candidate for the tank top: our own 2K repaint. Upscaling is not a fix. Glasses lenses are a flat blue colour texture: HDRP should render them as transparent glass, not textured.
- **GAP-CHR-8 No South-Asian male skin** in the CC0 set (and only one Eurasian male skin). The roster's 12 South-Asian customers are therefore all women. Candidates: (a) a hue/value-shifted derivative of a CC0 male skin, made by us (still CC0, recorded as derived); (b) another CC0 MakeHuman community skin if one exists (not yet found). Needs a likeness-neutral review either way.
- **GAP-CHR-9 No CC0 beard.** Both beards in the packs (`wdg_scruffy_beard`, `grinsegold_beard_sigmund_wip`) and the moustaches are AGPL- or CC-BY-headed. Candidates: (a) our own beard/stubble made in Blender (alpha cards or a stubble skin overlay, CC0 by construction); (b) a CC0 beard from another MakeHuman pack, if one exists (not yet found). Until then no customer has a beard.
- **GAP-CHR-10 MakeHuman logo prints.** Some CC0 system casual suits carry the MakeHuman logo on the tee (seen on the contact sheet). Legal (CC0), but it is a real project's logo in the store. Candidate: paint the logo out in our derived copy of the texture (an `edit` step in `customer_gen.py`).
- **Hairstyle pool is thin** (5 men's after the licence fix), so some customers share hair and tint; Rule D still holds through other cues. Candidate: our own CC0 hair cards, or more CC0 packs.
- GAP-CHR-1 (medical vs adult-use, no visual cue → UI-only MED badge) stays open. GAP-CHR-2 is closed by DEC-089. GAP-CHR-3 (Rocketbox per-bone build scale) is moot for MPFB: build is a body morph.

## 6. Unity import (GAME-CHR-002; nobody does these yet)
1. **Copy to local:** a DEC-023 cache→project script copies each `<cache>/mpfb/derived/<id>/` (FBX + `textures/`) into `UnityProject/Assets/_LocalThirdParty/MPFB/<id>/` (or into git: every unit is CC0, so redistribution is allowed; size decides). The validation JSON goes with it.
2. **Model import:** Rig → **Humanoid**, *Create From This Model* on the `game_engine` rig (map `pelvis`/`spine_01…`/`upperarm_l…`; leave face bones unmapped). Scale: metres, check against the validation height. Read/Write off. Blend shapes: none (baked).
3. **LODs:** the FBX has `<id>_LOD0…LOD3` meshes, so Unity's LODGroup auto-setup applies. Screen heights about 0.45 / 0.15 / 0.05 / 0.01 (tune in PERF capture).
4. **Materials (HDRP Lit):** remap each `M_*` from the copied textures: base colour, normal where present, AO/specular to the mask map. Skin: diffusion profile "Skin" (SSS) + detail normal (GAP-CHR-4). Hair, brows, lashes, beard (`alpha_cutout: true` in the validation JSON): alpha clip, double-sided; HDRP Hair shader later if needed. Tints are already in the textures (§3.2).
5. **Animation:** the Rocketbox MIT clips (§7) retarget through Humanoid. Root motion: in-place walks, NavMeshAgent drives position.
6. **Data, not 60 prefabs:** one `PF_Customer` (Animator + LODGroup + NavMeshAgent + `CustomerLook`); `CustomerIdentity` assets generated from `customer_roster_mpfb.json`. Presentation only; state stays in the simulation.
7. **Checks:** EditMode test that every identity has a valid Humanoid avatar, 4 LODs, tris within §4, Rule D on the roster. PlayMode capture with 12 customers vs the PERF-001 baseline.

## 7. Animation map (Rocketbox, MIT, retargeted via Humanoid)
Idles, talk and props come from `all_animations_max_motextr_static` (ANM-RB-STATIC, 32 files); walks, starts/stops and turns from the motion-extracted folders (ANM-RB-MOTION, 18 files). GAP-ANM-2: how their extracted root motion imports (root motion vs Bake Into Pose) is checked on import.
| Need | Clip (`f_`/`m_` prefix) |
|---|---|
| idle | `idle_neutral_01/02/03`, `idle_breathe_01` |
| shift weight | `idle_move_leg_01` (f), `idle_shake_leg_01` (m) |
| look around | `idle_look_around_01/02`, plus look-at IK toward shelves / menu board |
| wait / impatient | `idle_waiting_01` (+ `m_idle_waiting_02`) → `idle_nervous_01` as patience drops |
| phone | `cell_phone_textmessage` |
| talk at counter | `gestic_talk_neutral_01/02` |
| hand over (ID / cash) and receive (bag) | `documents_take` + right-hand IK to the counter point; prop on the right hand |
| leave with bag | `walk_neutral_01` + upper-body mask layer `hold_bag_idle` (m) / `hold_bag_idle_01` (f) |
| walk | `walk_neutral_01`, `walk_slow_01` (older), `walk_start/stop`, `turn_left/right_60/120_to_walk` |
| queue shuffle | `waiting_walk` |
| greet | `wave_01` |

## 8. Rocketbox interim set (DEC-087)
16 Rocketbox avatars are fetched (MIT, 6.7k–9.3k tris, 2K TGA colour/normal/specular, 80-bone Biped, ledger §1c, fetch list `fetch_list_characters.json`); 64 more adults are in the fetch list as `blocked: P1`. They serve as the PS2 crowd and background set until MPFB customers are imported. MIT notice goes into the build's third-party notices; Rocketbox's `FixRocketboxMaxImport.cs` may be ported with its notice (DEC-087). Excluded categories stay excluded (children, fire, military, pilot, police, swimwear).

## 9. Staff (later)
- **Budtenders/managers (DEC-089):** black pants and a green t-shirt with "The Flower Shop" printed on the **wearer's left chest** (viewer's top-right; DEC-113, closes GAP-CHR-PRINT-SIDE). Built with the same MPFB pipeline from a separate staff roster: a CC0 tee and trousers recoloured, plus a chest print decal made by us from the approved brand (DEC-071). Not built yet.
- **Security / door:** MPFB or Rocketbox `Security_*` (MIT), later.

## 10. Open questions (lead/Hub, within DEC-087 authority; see `Docs/Handoffs/ASSET-004.md`)
- Licence reading of MakeClothes `# license AGPL3` headers on assets whose pack pages say CC0 (refused for now).
- GAP-CHR-8: is a derived (hue-shifted) CC0 skin acceptable for South-Asian men?
- Derived customers in git or local: CC0 is allowed in git (DEC-023), so this is a size call for GAME-CHR-002.
