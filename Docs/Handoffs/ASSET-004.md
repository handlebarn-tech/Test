# Handoff — ASSET-004 (2026-10-30): MPFB2 customer pipeline — @@STATUS@@

Branch `worktree-agent-ae6487dd8e469d31b` (merges `claude/task-asset-004` 225ac4a). Reviewer: Docs reviewer (pipeline/spec); Unity A later for import.

## Done
- **First session (225ac4a):** MPFB 2.0.18 in an isolated Blender profile (`<cache>/mpfb/blender_user`), 17 CC0 packs fetched, `install_mpfb.py` per-asset licence index, `roster.py` (60, quotas, Rule D, CC0 audit), `customer_gen.py` + `blender.ps1 character`, C001–C003 samples.
- **Licence-audit fix (important):** the AGPL header regex missed the MakeClothes form `# license AGPL3`, so AGPL-headed units inside `_cc0` packs were marked allowed (found when `jujube_newsboy_cap` failed). Regex widened; index rebuilt: **106 refused** (was 58). Pools pruned in `customers_mpfb.json`: 7 hairstyles, 2 glasses, the newsboy cap, both beards, cortu cargo pants/jeans shorts (shorts outfits dropped, cargo → `toigo_wool_pants`). The first session's C001–C003 used AGPL-headed hair (`littleright_bobcut_hair`) and are superseded by this run. Ledger §1d updated.
- **Tri budget fix:** `toigo_stiletto_booties` is 44.7k tris (LOD1 > 60k) → replaced by `toigo_ankle_boots_female`.
- **Hair tint:** `customer_gen.tint_texture` recolours hair, brow and beard diffuse to the roster tint (`hair_tint_srgb` in params), keeping luminance and alpha; per-tint texture and material names. No runtime shader needed.
- **Roster** regenerated: 60, self-check 0 errors, deterministic.
- **Export:** @@EXPORT@@
- **Batch robustness:** one failing customer no longer stops the batch; `summary.validation.json` merges partial re-runs and lists failures; exit is still non-zero on any failure.
- **CHARACTERS.md** rewritten for MPFB: sources/licence gate, pipeline, variation (quotas, hair tint, Rule D), budgets with measured figures, texture gaps, Unity import, animation map, Rocketbox interim, staff (DEC-089).
- **Manifest:** @@MANIFEST@@
- **Contact sheet:** `Docs/Assets/Specs/customers_mpfb_contact_sheet.jpg` (`contact_sheet.py`, register framing, row-major C001…, 10 per row, @@SHEETSIZE@@).

## Measured (all exported customers)
@@MEASURED@@

## Texture and pool gaps (CHARACTERS.md §5)
GAP-CHR-4 skins 2K diffuse, no normal (procedural pore detail normal / HDRP SSS); GAP-CHR-5 eyes 1K (likely fine); GAP-CHR-6 brows/lashes 512 px; GAP-CHR-7 some hair/shoes 1K; GAP-CHR-8 no South-Asian male skin (all 11 South-Asian customers are women); GAP-CHR-9 no CC0 beard; GAP-CHR-10 MakeHuman logo on some system casual tees; thin men's hair pool (5 + shaved).

## Proposed packets
- **GAME-CHR-002 (Unity import):** copy `<cache>/mpfb/derived/<id>/` into the project, FBX → Humanoid from the `game_engine` rig, LODGroup from `<id>_LOD0..3`. Materials → HDRP Lit (skin diffusion profile + detail normal; hair/brows/lashes alpha-clip from `alpha_cutout` in the validation JSON; tints already baked). One `PF_Customer` + `CustomerIdentity` from `customer_roster_mpfb.json`, Rocketbox Humanoid clips; EditMode checks (Humanoid valid, 4 LODs, tris within budget) and a 12-customer PERF capture.
- **PROC-CHR-004 (follow-up):** close GAP-CHR-4/6/9/10 with our own CC0 work (pore detail normal, brow cards, beard/stubble, logo paint-out), widen the hair pool, then re-export.

## Deferred
- Manifest rows were written by a one-off script (logic: one `MPFB-DERIVED-<id>` row per FBX, sha256 checked against the validation JSON); fold it into `customer_gen.py` if re-exports become routine.
- Greyscale/store-lighting contact sheet → GAME-CHR-002.

## Questions for Nolan (through the Hub)
1. **FOR NOLAN — licence reading.** Many MakeHuman community assets are listed as CC0 on their pack pages but their files carry the MakeClothes header `# license AGPL3`. I treat them as refused (strict reading, DEC-023/087). Source: `<cache>/mpfb/blender_user/extensions/.user/user_default/mpfb/data/clothes/jujube_newsboy_cap/jujube_newsboy_cap.mhclo` line 3. Candidates: (a) keep refusing (current); (b) accept the pack-page CC0 as authoritative. (b) would bring back beards, 7 hairstyles, 2 glasses and a cap.
2. GAP-CHR-8: is a derived (hue-shifted) CC0 skin acceptable for South-Asian men, or does the roster stay with South-Asian women only?
3. Do MPFB customers go into git (all CC0, ~15–40 MB each with textures) or stay local in `_LocalThirdParty`?
