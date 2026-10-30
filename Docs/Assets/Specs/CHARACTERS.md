# CHARACTERS — customers (and later staff)

**Task:** ASSET-003 (2026-10-30). **Status:** sourcing + plan only; nothing imported into Unity yet.
**Licence record:** `Docs/Assets/LICENSE_LEDGER.md` §1c. **Downloads:** `Docs/Assets/fetch_list_characters.json`, sha256 in `ASSET_CACHE_MANIFEST.json`, files in `C:/Users/handl/Downloads/Dispo Game Assets Cache/quaternius/<ledger-id>/`.
**Rules kept:** $0, no account, no real person's likeness (all faces are generic stylised Quaternius heads), no customer PII (customers are visual archetypes only).

## 1. What we have (P0, fetched)
| Ledger ID | What | Rig | Tris (measured) | Notes |
|---|---|---|---|---|
| CHR-QUA-UMM | Ultimate Modular **Men**: 11 outfits, each split into Head / Body / Legs / Feet meshes, Humanoid-Rig FBX + master .blend | 62 bones, Humanoid-mappable (Hips…Head, Shoulder/UpperArm/LowerArm/Hand + fingers, UpperLeg/LowerLeg/Foot; no toes) | 5.2k–11.1k (modern outfits 5.2k–6.6k) | 4–11 flat-colour materials per outfit, no textures |
| CHR-QUA-UMW | Ultimate Modular **Women**: 10 outfits, same split, Humanoid-Rig FBX + modular master FBX | 51 bones, same naming | 6.0k–7.9k | 5–9 flat-colour materials |
| ANM-QUA-UAL1 | Universal Animation Library (free tier), 43 clips | 65-joint UE-mannequin-style skeleton | — | FBX for Unity, with and without root motion (`_RM`) |
| ANM-QUA-UAL2 | Universal Animation Library 2 (free tier), 43 clips + female mannequin | same 65-joint skeleton | — | adds folded-arms, phone, yes/no, carry walk |

The two body packs and the animation library use **different skeletons**. That is fine in Unity: every model and clip gets a Humanoid avatar, and Mecanim retargets between them. No Blender retargeting is needed.

**Licence caveat:** pack pages and the bundled `License.txt` say CC0, but `quaternius.com/license.html` now claims QAL for everything. Until the Hub rules on it, import these files only into `_LocalThirdParty/` and never commit the raw FBX (ledger §1c).

## 2. Shortlist considered
| Candidate | Licence | Verdict |
|---|---|---|
| Quaternius Ultimate Modular Men + Women | CC0 (pack) / QAL conflict | **P0, fetched**: the only CC0 set found with rigged, modular, *modern* clothes and both sexes |
| Quaternius Universal Animation Library 1 + 2 (free tiers) | CC0 (pack) / QAL conflict | **P0, fetched**: covers idle, walk, talk, phone, folded arms, interact, pick-up, carry, yes/no |
| Quaternius Universal Base Characters (free: 2 bodies, 5 hair, ~13k tris, UAL skeleton) | CC0 (pack) | P1: better anatomy, but no clothes. The only outfits for this rig are fantasy. Use it only if we model our own modern clothes |
| Kenney Animated Characters (Protagonists / Survivors / Retro) | CC0 | Fallback: one blocky mesh with texture skins; too toy-like for HDRP retail |
| MakeHuman / MPFB2 (Blender add-on) | core assets CC0; exported-model terms unverified (LIB-MH) | P2 path to realistic humans from our own Blender generator; needs a separate licence check of MPFB's clothes/skins |
| KayKit Adventurers (Kay Lousberg) | CC0 | Rejected: fantasy, chibi proportions |
| Mixamo (Adobe) | royalty-free in games, **not CC0**, raw redistribution barred, Adobe ID needed | **Not used** (ledger ANM-MIXAMO). The no-account rule blocks the download. If ever approved: `_LocalThirdParty/` only |
| Sketchfab CC BY rigged people (plan §16 #7–10) | CC BY 4.0 | Not needed now: one-off individuals and attribution overhead. Possible hero NPCs later |

## 3. Variation plan (target: 10+ distinct customers; plan gives 16 presets)
**Usable modern outfits** (fantasy/costume outfits excluded from customers):
- Men (8): Casual, Casual2, Suit, Worker, Farmer (overalls + hat), Punk, Beach, Adventurer (backpack hiker). **Excluded:** King, Spacesuit, Swat (reads as police, which is confusing in a store with ID checks).
- Women (6): Casual, Formal, Suit, Worker, Punk, Adventurer (shorts + pack). **Excluded:** Medieval, Witch, SciFi, Soldier.

**Axes** (mix only within one pack, because men and women use different skeletons):
1. **Part swap**: Head × Body × Legs × Feet from different outfits of the same pack. Men: 8⁴ = 4096 raw, women: 6⁴ = 1296. Most combinations are nonsense, so presets are curated.
2. **Colour**: every material is a named flat colour, so each clothing slot is recoloured from a curated palette per slot (tops 10, bottoms 8, shoes 6). **Skin** comes from a fixed set of 6 natural skin tones that is independent of outfit or archetype. **Hair** colour comes from 6 natural shades plus 2 dyed (punk only).
3. **Hair / hats**: hair and hats are baked into the Head meshes (cowboy hat on Farmer, hard hat on Worker, mohawk on Punk). Swapping heads therefore swaps hair and hat together. Hat-less variants of Farmer and Worker need a small Blender pass that deletes the hat polygons and saves a new head mesh (P1, see the packet).
4. **Scale**: height ±4 % and width ±3 % per preset.

**16 presets** (archetypes only, no names or PII):
| # | Pack | Head | Body | Legs | Feet | Reads as |
|---|---|---|---|---|---|---|
| C01 | M | Casual | Casual | Casual | Casual | everyday regular |
| C02 | M | Casual2 | Casual2 | Casual | Casual2 | young casual |
| C03 | M | Suit | Suit | Suit | Suit | office worker on lunch |
| C04 | M | Worker (hat-less, P1) | Worker | Worker | Worker | trades, after shift |
| C05 | M | Farmer | Casual | Farmer | Farmer | older, overalls + hat |
| C06 | M | Punk | Punk | Punk | Punk | alt / punk |
| C07 | M | Beach | Beach | Beach | Casual | summer / beach |
| C08 | M | Adventurer | Casual2 | Adventurer | Adventurer | hiker with pack |
| C09 | M | Casual | Suit | Casual | Casual2 | smart-casual |
| C10 | F | Casual | Casual | Casual | Casual | everyday regular |
| C11 | F | Formal | Formal | Formal | Formal | professional |
| C12 | F | Suit | Suit | Suit | Formal | business |
| C13 | F | Worker (hat-less, P1) | Worker | Worker | Worker | trades / scrubs-like |
| C14 | F | Punk | Punk | Punk | Punk | alt / punk |
| C15 | F | Adventurer | Adventurer | Adventurer | Adventurer | outdoorsy |
| C16 | F | Casual | Formal | Casual | Casual | smart-casual |

With 3 palette rolls per preset this gives 48 looks. Rule: the same preset never appears twice on screen with the same palette roll.
GAP-CHR-1: the medical-patient vs adult-use split (GAME-009) has no visual cue yet. Keep it gameplay-only (MED badge in the UI), not clothing.

## 4. Animation map (customers)
| Need | Clip (pack) | Notes |
|---|---|---|
| idle | `Idle_Loop` (UAL1) | base layer |
| walk | `Walk_Loop` (UAL1), `Walk_Formal_Loop` (UAL1) for Suit/Formal presets | non-RM file; NavMeshAgent drives position |
| wait / impatient | `Idle_FoldArms_Loop` (UAL2), `Idle_TalkingPhone_Loop` (UAL2) | patience-driven: phone first, folded arms when patience is low |
| talk at counter | `Idle_Talking_Loop` (UAL1) | while the request bubble is shown |
| shift-weight | **GAP-ANM-1**: no clip in either free tier | candidates: (a) blend `Idle_Loop` with a 2–3° pelvis-sway additive clip authored in Blender (tiny, project-original); (b) the paid UAL Pro may have one, which breaks $0; (c) CMU mocap is UNVERIFIED in the ledger. Recommend (a) |
| look-around | **procedural**: Humanoid `Animator.SetLookAtPosition` in `OnAnimatorIK` toward shelf / menu-board / jar-wall points | no clip needed; no package needed |
| hand-over (give ID / cash) | `Interact` (UAL1) + right-hand IK (`SetIKPosition(AvatarIKGoal.RightHand, counterPoint)`) | ID card / cash prop parented to the hand bone during the clip |
| receive (take bag) | `PickUp_Table` (UAL1) + hand IK to the bag | then `Walk_Carry_Loop` (UAL2) on exit |
| reactions | `Yes` (UAL2), `Idle_No_Loop` (UAL2) | accept / decline a recommendation |
| sit (lobby bench, later) | `Sitting_Enter / Idle_Loop / Exit` (UAL1) | only if a bench exists (REF) |

Not used: combat, pistol, sword, spell, death, zombie, `Consume` (no consumption in store), `Driving_Loop`.

## 5. Budget: 6 GB VRAM, up to ~12 on screen
VRAM is not the limit here. 12 skinned meshes at ~6k tris are about 2 MB of vertex data, and the palette textures are tiny. The real costs are **draw calls, skinning, and shadow passes**.
| Item | Budget |
|---|---|
| LOD0 (≤ 4 m from camera: counter, queue head) | ≤ 7k tris, **1 skinned mesh, 1 material** |
| LOD1 (4–10 m: queue, browsing) | ≤ 3k tris |
| LOD2 (> 10 m: lobby, door) | ≤ 1.2k tris, no shadows, 2-bone skin weights |
| All characters on screen | ≤ 50k tris at once (e.g. 3 × LOD0 + 5 × LOD1 + 4 × LOD2 ≈ 21k + 15k + 5k = 41k) |
| Draw calls | 1 per character + 1 per shadow cascade for LOD0/1 only |
| Bones | ≤ 62 (packs ship 51/62); finger bones untouched |
| Textures | one 256×64 palette texture shared by all characters; colour variation comes from a per-renderer `MaterialPropertyBlock` palette row, so no material copies |

**Merge step (needed for the budget):** the outfits ship as 4 meshes with 4–11 materials each, which would be ~30 draw calls per character. A Blender batch script (our pipeline, `Tools/Blender/`) joins the chosen Head/Body/Legs/Feet parts into one skinned mesh per preset. It also bakes each named flat-colour material into UVs on a shared palette strip (slot → palette column) and writes LOD1/LOD2 with Decimate (collapse, keeping UV seams).

## 6. Crowd LOD plan
- `LODGroup` per character with the 3 LODs above. Screen-relative transition heights: 0.35 / 0.15 / 0.03, then cull.
- Animator: `cullingMode = CullUpdateTransforms`. Agents beyond LOD1 tick their Animator at half rate (drive `Animator.Update` manually, or enable/disable on alternating frames).
- Shadows: `ShadowCastingMode.Off` on LOD2. LOD0/1 use HDRP's normal shadow, with contact shadows off for characters.
- IK (look-at, hand) only on the customer currently being served and the next 2 in the queue.
- GPU skinning: Unity 6 default (Player Settings → GPU Skinning = GPU / Batched). Confirm on the perf-scene check (PERF-001 method).
- Hard cap: the spawner never exceeds 12 active customers. Extra arrivals wait off-screen outside the door (gameplay already caps the queue).

## 7. Staff (later)
Use the same packs: Men Casual/Suit and Women Casual/Formal bodies recoloured to the store uniform. **GAP-CHR-2:** the real store's staff uniform (colour, logo shirt, lanyard?) is not in any reference. Use a neutral black top + dark trousers placeholder until Nolan says. No store logo invented.

## 8. Unity import steps (for the integration packet; nobody does these yet)
1. **Copy to local:** write a DEC-023 cache→project copy script following `Tools/Assets/lookdev_textures.py` `import_cache()` to copy the merged preset FBXs (output of the §5 Blender step) and `UAL1_Standard.fbx`, `UAL2_Standard.fbx` (non-RM) from the cache into `UnityProject/Assets/_LocalThirdParty/Quaternius/` (gitignored). Never into `_Game/Art/ThirdParty/` while the QAL question is open.
2. **Model import (each preset FBX):** Model → Scale Factor 1, check that height ≈ 1.6–1.85 m in a test scene (Quaternius FBX can arrive at 100×; fix with Convert Units, not a transform scale). Read/Write off. Blend shapes off. Rig → **Humanoid**, Avatar Definition: *Create From This Model*. Configure: map Hips…Head and the limbs (auto-map should work with these bone names; no toes). Enforce T-pose. Materials → *Use External Materials (Legacy)* off, then remap the single palette material to `M_CharacterPalette` (HDRP/Lit, base map = palette texture, smoothness 0.2).
3. **Animation import (UAL1/UAL2 non-RM FBX):** Rig → Humanoid, *Create From This Model* (the mannequin skeleton). Animation tab: keep only the clips in §4. Set *Loop Time* on every `*_Loop` clip. Root Transform Rotation/Position(Y)/Position(XZ): *Bake Into Pose* = on, based on Original. `Interact`, `PickUp_Table`, `Yes`: loop off.
4. **Controller:** `AC_Customer` (Base: Idle / Walk blend by speed, Wait substate (phone ↔ folded arms by patience), Talk, HandOver, Receive, Yes/No). Upper-body Avatar Mask layer for HandOver/Receive so they can play while weight-shifting. IK Pass on for the base layer.
5. **Prefab:** `PF_Customer_Cxx` = model + Animator(AC_Customer) + LODGroup + NavMeshAgent (radius 0.25, speed 1.2 m/s) + a `CustomerLook` component (palette row, height/width scale). Pure presentation: simulation state stays in `Simulation/Slice` (CustomerState, PatienceState) and the view reads it.
6. **Check:** EditMode test that every preset prefab has a valid Humanoid avatar, a LODGroup with 3 LODs, tris under the §5 budget, and exactly 1 material. PlayMode capture of 12 customers in the slice scene, with frame time compared to the PERF-001 baseline.

## 9. Open questions (forwarded through the Hub, see handoff)
- Q1 (licence): accept Quaternius as CC0 (the per-pack grant plus the bundled License.txt) or as QAL (local import only)? This plan assumes QAL handling either way.
- Q2 (art direction): the Quaternius people are low-poly and flat-shaded. Next to HDRP lookdev they read as stylised. Is that acceptable for customers, or do we invest in UBC bodies plus our own modern clothes (P1) or MPFB2 (P2)?
- Q3 (staff uniform): GAP-CHR-2.
