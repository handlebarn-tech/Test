# CHARACTERS — customers (and later staff)

**Task:** ASSET-003 (2026-10-30). **Status:** sourcing + plan only; nothing imported into Unity yet.
**Scope (DEC-075, Nolan via Hub):** start with ≥ 10 distinct customers; by the end of the project, **≥ 50 distinct customers**. This spec designs a variation system for **60 (headroom to 100+)**.
**Licence record:** `Docs/Assets/LICENSE_LEDGER.md` §1c. **Downloads:** `Docs/Assets/fetch_list_characters.json`, sha256 in `ASSET_CACHE_MANIFEST.json`, files in `C:/Users/handl/Downloads/Dispo Game Assets Cache/quaternius/<ledger-id>/`.
**Rules kept:** $0, no account, no real person's likeness (generic stylised Quaternius faces), no customer PII (a customer is a visual identity plus gameplay stats, never a name or CRM record). Every customer is an adult (21+ store; no child models).

## 1. What we have (P0, fetched)
| Ledger ID | Family | What | Rig | Tris (measured, Blender 5.2) | Materials |
|---|---|---|---|---|---|
| CHR-QUA-UMM | **F1** men, modular | Ultimate Modular Men: 11 outfits, each split Head / Body / Legs / Feet (+ separate Backpack) | 62 bones, Humanoid-mappable, no toes | 5.2k–11.1k (modern 5.2k–6.6k) | named flat colours, 4–11 |
| CHR-QUA-UMW | **F2** women, modular | Ultimate Modular Women: 10 outfits, same split | 51 bones | 6.0k–7.9k | named flat colours, 5–9 |
| CHR-QUA-AM | **F3** men, whole | Animated Men: Casual (raglan tee), LongSleeve, Shirt (tee + shorts), Suit (older man, white hair + beard); flat + Smooth versions; 11 baked clips | 42 bones (mitten fingers), Humanoid-mappable | flat 1.9k–2.1k / smooth 7.9k–8.8k | one per garment (Shirt, Pants, Shoes, Hair, Skin…) |
| CHR-QUA-AW | **F4** women, whole | Animated Women: Alternative (jacket, two-tone hair), Casual (tee), Dress, TankTop; flat + Smooth | 42 bones | flat 1.8k–2.8k / smooth 6.4k–7.7k | one per garment |
| ANM-QUA-UAL1 | anim | Universal Animation Library (free tier), 43 clips | 65-joint UE-style | — | — |
| ANM-QUA-UAL2 | anim | UAL 2 (free tier), 43 clips + female mannequin | same | — | — |

All six use different skeletons. Unity's **Humanoid** avatar retargets UAL clips onto every family, so no Blender retarget is needed.
**Licence caveat:** pack pages and bundled `License.txt` say CC0, but `quaternius.com/license.html` claims QAL for everything. Until the Hub rules, import only into `_LocalThirdParty/` and never commit raw FBX (ledger §1c).

## 2. Shortlist considered
| Candidate | Licence | Verdict |
|---|---|---|
| Quaternius Ultimate Modular Men + Women (F1/F2) | CC0 (pack) / QAL conflict | **P0, fetched**: modular parts give the combinatorics; most garment types |
| Quaternius Animated Men + Women (F3/F4) | CC0 (pack) / QAL conflict | **P0, fetched**: the most "everyday" clothes (tees, long-sleeve, dress, tank top), an older man, and a cheap flat version that doubles as a crowd LOD |
| Quaternius Universal Animation Library 1 + 2 (free tiers) | CC0 (pack) / QAL conflict | **P0, fetched**: idle, walk, talk, phone, folded arms, interact, pick-up, carry, yes/no |
| Quaternius Universal Base Characters (2 bodies, 5 hair, ~13k tris, UAL skeleton) | CC0 (pack) | P1: better anatomy, but unclothed (only fantasy outfits exist for this rig). Use it only if we model our own modern clothes |
| Kenney Animated Characters | CC0 | Fallback: blocky texture-skinned single mesh; too toy-like |
| MakeHuman / MPFB2 | core assets CC0; exported-model terms unverified (LIB-MH) | P2 path to realistic humans and real age/weight morphs; needs a licence check |
| KayKit Adventurers | CC0 | Rejected: fantasy, chibi |
| Mixamo | royalty-free in games, not CC0, Adobe ID needed | **Not used** (ledger ANM-MIXAMO) |
| Sketchfab CC BY rigged people | CC BY 4.0 | Not now: one-offs plus attribution |

**Why these packs scale to 50+:** F1/F2 are modular, so parts mix freely within a family. Every pack uses **named per-garment materials**, so each garment recolours independently. Hair, hats, beards and earrings are separate materials inside the head meshes, so a Blender pass can **split them into their own parts** (§3.2). Accessories are rigid props on the Head/Spine bones, so they work on all four families.

## 3. Variation system (scales to 60+, target roster = 60)

### 3.1 Axes and pool sizes (modern items only)
Excluded from customers as costume or confusing: King body, Spacesuit, Swat (reads as police), Medieval, Witch, SciFi, Soldier; weapons (Pistol, Sword); Horse_Head.

| Axis | Men (F1 + F3) | Women (F2 + F4) | Source |
|---|---|---|---|
| **Top garment** (register-visible) | 12: F1 Casual sweater, Casual2 tee, Suit, Worker hi-vis vest, Farmer overalls, Punk vest, Beach shirt, Adventurer shirt; F3 raglan tee, long-sleeve, tee, older suit | 10: F2 Casual, Formal, Suit, Worker, Punk, Adventurer; F4 jacket (Alternative), tee, dress, tank top | packs |
| **Legs / feet** (queue-visible only) | F1: 8 legs × 8 feet (mixable); F3 fixed per body | F2: 6 × 6; F4 fixed | packs |
| **Hair style** | 11 + shaved: F1 Casual, Casual2, Suit, Adventurer (long), Beach, Punk (mohawk), King hair (white, crown removed); F3 quiff, short ×2, white | 11: F2 Casual, Formal (updo), Suit, Punk (mohawk), Adventurer (buzz), Worker, Medieval hair (hood removed), SciFi (long); F4 long, two-tone bangs, ponytail, bob | split from Head meshes (§3.2) |
| **Hair colour** | 8: black, dark brown, brown, auburn, blond, grey, white, dyed (pink/blue/green; only on punk/alt styles) | same | palette |
| **Skin tone** | 6 natural tones, independent of every other axis | same | palette |
| **Top colour family** | 10 perceptually spaced families (black, white, grey, navy, red, green, mustard, teal, brown, pink) | same | palette |
| **Headwear** | 6: none, cowboy hat (F1 Farmer), hard hat (F1 Worker), cap, beanie, bucket hat | 5: none, hard hat (F2 Worker), cap, beanie, bucket hat | 2 from packs; cap/beanie/bucket made by `Tools/Blender` (P1) |
| **Face accessory** | 6: none, glasses, sunglasses (on head), beard (F1 King / F3 Suit), moustache (F1 Worker), earrings (F1 Beach/Punk) | 4: none, glasses, sunglasses, earrings | men: split from heads; glasses, sunglasses and women's earrings: Blender-made (no earrings material in F2/F4) |
| **Carry** (queue/walk) | none, backpack (F1), tote, shoulder bag | same | 1 pack + 2 Blender-made |
| **Build** | slim / average / broad (bone-scale preset, §3.3) | same | Unity prefab |
| **Height** | 0.94–1.06 (6 steps) | 0.94–1.06 | Unity prefab |
| **Age read** | young / adult / older (older = grey/white hair, beard or glasses, walk speed 0.9 m/s, `Walk_Formal_Loop`) | same | combination rule |

**Raw combinations:** about 10¹⁰ per sex, if legs/feet are counted at all. That number is meaningless: what matters is how many customers look different **at the register**, so §3.4 counts only register-visible cues.

### 3.2 Making the parts (Blender, project pipeline)
1. **Hair/headwear split.** For each Head mesh, separate faces by material (`Hair*`, `Moustache`, `Earrings`, `Worker_Yellow` hat, `Beige/Red` cowboy hat, `Gold` crown) into their own meshes, weight-painted 100 % to `Head`. What remains is a bald **face** part. F1 alone then yields 8 faces × 7 hair styles instead of 8 fixed heads.
2. **Cross-family hair.** Hair is rigid on `Head`, so a style can be fitted to another family's face with a per-family socket offset and scale. This is allowed only when a fit check shows no visible clipping. Fitted pairs go into a whitelist table.
3. **Blender-made accessories** (cap, beanie, bucket hat, glasses, sunglasses, tote, shoulder bag): primitive-based, ≤ 400 tris each, palette-UV'd, one socket per family (`Head` or `Spine/Chest`). These come from our own generator, so there is no licence question.
4. **LODs:** F3/F4 already ship flat versions (≈ 2k tris), so the flat file is LOD1 of its smooth twin. F1/F2 get Decimate LOD1/LOD2 (§5).
5. **Palette UVs:** every part's named material maps to a column of a shared palette strip. A garment's column is recoloured per identity (§5).

### 3.3 Body types without morph targets
No pack ships shape keys. Builds use **per-bone scale on the prefab**: Humanoid clips write rotations (and hips position), never bone scale, so the scales persist under every UAL clip.
- slim: `Chest/Torso/Spine` X·Z 0.92, `UpperArm/UpperLeg` X·Z 0.92
- average: 1.0
- broad: `Chest/Torso/Spine` X·Z 1.12, `Hips` X 1.08, `UpperArm/UpperLeg` X·Z 1.08
Bone scale propagates to children, so compensate on `Neck` / `Head` / `Hand` with the inverse scale to keep heads and hands normal. GAP-CHR-3: this has to be checked visually on the first prefab. Fallback: a Blender "broad" variant of each Body mesh (shrink/fatten along normals with an armpit mask).

### 3.4 Distinct at register distance (the readability rule)
At the register the player sees the customer **across the counter, head and torso, about 1.2–2 m away, in first person**. Legs and shoes are hidden by the counter, so they never count toward distinctness.

**Register cue vector (one value per cue):**
| # | Cue | Kind | Men | Women |
|---|---|---|---|---|
| R1 | head silhouette = hair style or headwear | shape | 12 + 5 = 17 | 11 + 4 = 15 |
| R2 | top garment type | shape | 12 | 10 |
| R3 | face accessory | shape | 6 | 4 |
| R4 | build / height class | shape | 3 | 3 |
| R5 | top colour family | colour | 10 | 10 |
| R6 | skin tone | colour | 6 | 6 |
| R7 | hair colour | colour | 8 | 8 |

**Rule D (the roster test):** every pair of customers in the roster must differ in **≥ 3 cues, of which ≥ 1 is a shape cue (R1–R4)**. Pure recolours never count as a new customer. In addition, no R1×R2 combination (head silhouette + top) appears more than twice in the roster.

**Capacity:** shape-distinct (R1 × R2) pairs alone give 17 × 12 = **204 men**, 15 × 10 = **150 women**, 354 in total, before any colour axis. Rule D needs only 60 identities, so even if the roster were limited to the 4 most everyday tops per sex, it would still have 17 × 4 + 15 × 4 = 128 shape pairs to pick from. The bottleneck is not combinatorics but **readability of similar faces**. That is why the rule leans on hair, headwear and accessories (the most readable head-and-shoulders cues) rather than faces.

**Roster mix (60):** 30 men / 30 women (F1 + F3 / F2 + F4). Age: ~25 % older, ~25 % young, rest adult. Builds 30/40/30. Skin tones spread evenly; no skin tone is tied to a garment, headwear or archetype. Dyed hair only on alt/punk styles, at most 6 in the roster.

**Roster generator (P1 packet):** a seeded Python script (`Tools/Assets/` or `Tools/Blender/`) greedily draws identities from the pools under Rule D and the mix quotas. It writes `Docs/Assets/Specs/customer_roster.json` (id `C001…C060`, family, part ids, palette indices, headwear, accessory, build, height, age read). It asserts Rule D pairwise and exits non-zero on failure (its self-check). The same seed always produces the same roster.

**Milestones:** PS2 = the 16 hand-picked identities below (subset of the roster, ≥ 10 required). Later = the generated 60. Same pipeline throughout, only the roster grows.

**Readability check (QA):** render a contact sheet of every identity at the register framing (the slice's first-person camera, 1.5 m, store lighting): (1) in colour; (2) in **greyscale**. Pass when no two tiles are confused in the greyscale sheet by a reviewer. Rule D already guarantees ≥ 1 shape difference.

### 3.5 First 16 (PS2 slice, hand-picked, all satisfy Rule D)
| # | Fam | Face / hair | Headwear | Top | Accessory | Build | Reads as |
|---|---|---|---|---|---|---|---|
| C01 | F3 | short brown | — | raglan tee (red/grey) | — | avg | everyday regular |
| C02 | F1 | Casual2 hair | cap | Casual2 tee (green) | — | slim | young casual |
| C03 | F1 | Suit hair | — | Suit (navy) | glasses | avg | office lunch |
| C04 | F1 | Worker face | hard hat | Worker hi-vis vest | moustache | broad | trades after shift |
| C05 | F1 | Farmer face | cowboy hat | overalls (blue) | — | broad | older, rural |
| C06 | F1 | Punk mohawk (dyed) | — | Punk vest (black) | earrings | slim | alt / punk |
| C07 | F3 | white hair | — | older suit (charcoal) | beard | avg | older gentleman |
| C08 | F1 | Adventurer long | — | Adventurer shirt + backpack | — | avg | hiker |
| C09 | F3 | quiff blond | beanie | long-sleeve (mustard) | — | slim | young |
| C10 | F4 | long dark | — | tee (teal) | — | avg | everyday regular |
| C11 | F2 | Formal updo (auburn) | — | Formal (white) | glasses | avg | professional |
| C12 | F2 | Suit hair | — | Suit (black) | sunglasses on head | slim | business |
| C13 | F4 | two-tone bangs | — | jacket (pink/black) | earrings | slim | alt |
| C14 | F4 | ponytail blond | — | dress (red) | — | avg | going out |
| C15 | F2 | Worker hair | hard hat | Worker vest | — | broad | trades |
| C16 | F4 | bob grey | bucket hat | tank top (green) | glasses | avg | older, outdoorsy |

Skin tones and leg/shoe choices are assigned by the generator, evenly spread. This table lists only register cues.
GAP-CHR-1: medical vs adult-use customers have no visual cue. Keep it UI-only (MED badge).

## 4. Animation map (customers)
| Need | Clip (pack) | Notes |
|---|---|---|
| idle | `Idle_Loop` (UAL1) | base layer |
| walk | `Walk_Loop` (UAL1); `Walk_Formal_Loop` (UAL1) for suits and the older age read | non-RM file; NavMeshAgent drives position |
| wait / impatient | `Idle_FoldArms_Loop`, `Idle_TalkingPhone_Loop` (UAL2) | phone first, folded arms when patience is low |
| talk at counter | `Idle_Talking_Loop` (UAL1) | while the request bubble is up |
| shift-weight | **GAP-ANM-1**: none in the free tiers | recommend a tiny project-original additive pelvis-sway clip from Blender |
| look-around | procedural: Humanoid `Animator.SetLookAtPosition` in `OnAnimatorIK` toward shelf / menu board / jar wall | no clip, no package |
| hand-over (ID / cash) | `Interact` (UAL1) + right-hand IK to the counter point | prop parented to the hand bone |
| receive (bag) | `PickUp_Table` (UAL1) + hand IK | then `Walk_Carry_Loop` (UAL2) on exit |
| reactions | `Yes`, `Idle_No_Loop` (UAL2) | accept / decline a recommendation |
| sit (bench, later) | `Sitting_*` (UAL1) | only if a bench exists |

Personality variety at no asset cost: per-identity animation speed 0.9–1.1, idle clip start offset, and the wait-state order (phone vs folded arms) as part of the identity. F3/F4 also ship 11 baked clips of their own. They are not used, because UAL is the one shared set.

## 5. Budget: 6 GB VRAM, up to ~12 on screen
VRAM is not the limit (12 skinned characters ≈ 2–3 MB of vertex data, plus a tiny palette texture). The costs are **draw calls, skinning, and shadows**.

| Item | Budget |
|---|---|
| LOD0 (≤ 4 m: counter, queue head) | ≤ 9k tris per character, all parts included (F3/F4 smooth ≤ 8.8k; F1/F2 ≤ 7k body + hair + ≤ 2 accessories) |
| LOD1 (4–10 m) | ≤ 3k (F3/F4 flat versions; F1/F2 Decimate) |
| LOD2 (> 10 m) | ≤ 1.2k, no shadows, 2-bone skin weights, accessories off |
| All characters on screen | ≤ 60k tris (e.g. 3 × LOD0 + 5 × LOD1 + 4 × LOD2 ≈ 27k + 15k + 5k = 47k) |
| Renderers per character | ≤ 6 at LOD0 (face, hair, body, legs, feet, 1 accessory; F3/F4: 1 body + accessories), ≤ 2 at LOD2 |
| Materials | **one material instance per identity**, all on the same HDRP/Lit shader and the shared palette texture, with the identity's colours in a palette row index. Same shader → **SRP Batcher** keeps 12 × 6 draws cheap. Do **not** use `MaterialPropertyBlock`: it breaks SRP Batcher compatibility |
| Bones | ≤ 62; finger bones untouched |
| Texture | one palette strip (64 columns × N identity rows, e.g. 64 × 64 px for 60 identities): ~16 KB |

## 6. Crowd LOD plan
- `LODGroup` per character, transition heights 0.35 / 0.15 / 0.03, then cull.
- Animator `cullingMode = CullUpdateTransforms`. Characters beyond LOD1 tick at half rate.
- Shadows off at LOD2. Contact shadows off for characters.
- IK (look-at, hand) only on the customer being served and the next 2 in the queue.
- GPU skinning = Unity 6 default. Confirm with the PERF-001 method.
- The spawner never has more than 12 active customers. It picks identities from the roster without repeating any identity currently in the store (60 identities ≫ 12 slots), so no duplicates are ever on screen together.

## 7. Staff (later)
Same packs: F1 Casual/Suit and F2 Casual/Formal tops in the store uniform colour, with no store logo invented. **GAP-CHR-2:** the real staff uniform is unknown. Placeholder: plain black top, dark trousers. Staff identities are excluded from the customer roster.

## 8. Unity import steps (for the integration packet; nobody does these yet)
1. **Copy to local:** a DEC-023 cache→project copy script following `Tools/Assets/lookdev_textures.py` `import_cache()`. It copies the Blender-processed parts (§3.2) and `UAL1_Standard.fbx` / `UAL2_Standard.fbx` (non-RM) into `UnityProject/Assets/_LocalThirdParty/Quaternius/` (gitignored), never into `_Game/Art/ThirdParty/` while the licence question is open.
2. **Model import (per family body/parts FBX):** check that height ≈ 1.6–1.85 m in a test scene (fix the scale with Convert Units, not a transform). Rig → **Humanoid**, *Create From This Model*; auto-map should work (no toes; F3/F4 mitten fingers map thumb + one finger chain or are left unmapped). Enforce T-pose. Read/Write off. Remap materials to the identity material (§5).
3. **Rigid parts** (hair, headwear, accessories): plain MeshRenderers under a `Socket_Head` / `Socket_Chest` child of the bone, positioned with per-family offsets from the §3.2 fit table.
4. **Animation import (UAL1/UAL2 non-RM FBX):** Humanoid, *Create From This Model*. Keep the §4 clips only. *Loop Time* on `*_Loop`. Root transform: Bake Into Pose for rotation, Y and XZ.
5. **Controller:** `AC_Customer` (Idle/Walk blend by speed, Wait substate, Talk, HandOver, Receive, Yes/No; upper-body Avatar Mask layer for HandOver/Receive; IK Pass on).
6. **Data, not 60 prefabs:** 4 family prefabs `PF_Customer_F1..F4` (Animator + LODGroup + NavMeshAgent r 0.25, 1.2 m/s + `CustomerLook`). `CustomerLook` reads one `CustomerIdentity` ScriptableObject per roster entry: part ids, palette row, headwear, accessory, build preset, height, anim speed. An editor importer creates the 60 assets from `customer_roster.json`. Presentation only: simulation state stays in `Simulation/Slice` (CustomerState, PatienceState).
7. **Checks:** an EditMode test that loads every identity and asserts a valid Humanoid avatar, 3 LODs, LOD0 tris ≤ 9k, ≤ 6 renderers, one shared shader, and Rule D on the roster file. A PlayMode capture of 12 customers vs the PERF-001 baseline, plus the §3.4 colour/greyscale contact sheets.

## 9. Open questions (through the Hub, see handoff)
- Q1 licence: CC0 (per-pack grant + bundled License.txt) vs QAL (local import only). This plan works either way.
- Q2 art direction: low-poly stylised people next to HDRP lookdev. Also, which shading for F3/F4: smooth versions (closer to F1/F2 detail) or flat for all?
- Q3 staff uniform (GAP-CHR-2).
