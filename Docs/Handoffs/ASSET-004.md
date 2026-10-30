# Handoff — ASSET-004 (2026-10-30): MPFB2 customer pipeline — DONE (58/60 exported; 2 deferred)

Branch `worktree-agent-ae6487dd8e469d31b` (merges `claude/task-asset-004` 225ac4a). Reviewer: Docs reviewer (pipeline/spec); Unity A later for import.

## Done
- **First session (225ac4a):** MPFB 2.0.18 in an isolated Blender profile (`<cache>/mpfb/blender_user`), 17 CC0 packs fetched, `install_mpfb.py` per-asset licence index, `roster.py` (60, quotas, Rule D, CC0 audit), `customer_gen.py` + `blender.ps1 character`, C001–C003 samples.
- **Licence-audit fix (important):** the AGPL header regex missed the MakeClothes form `# license AGPL3`, so AGPL-headed units inside `_cc0` packs were marked allowed (found when `jujube_newsboy_cap` failed). Regex widened; index rebuilt: **106 refused** (was 58). Pools pruned in `customers_mpfb.json`: 7 hairstyles, 2 glasses, the newsboy cap, both beards, cortu cargo pants/jeans shorts (shorts outfits dropped, cargo → `toigo_wool_pants`). The first session's C001–C003 used AGPL-headed hair (`littleright_bobcut_hair`) and are superseded by this run. Ledger §1d updated.
- **Budget fixes from the first 60-run (21 failures):** `toigo_stiletto_booties` (44.7k tris) → `toigo_ankle_boots_female`; `toigo_flats` (57.6k) → `toigo_ballet_flats`. Men's height macro capped 0.75 → 0.65 (4 men measured 2.04–2.10 m); height is now measured over body + clothes without hair/hat. A body-only measure was tried and dropped, because clothing masks delete the covered body vertices. LOD2 decimate 0.35 → 0.32 (C001 was 20.1k against the 20k budget).
- **Hair tint:** `customer_gen.tint_texture` recolours hair, brow and beard diffuse to the roster tint (`hair_tint_srgb` in params), keeping luminance and alpha; per-tint texture and material names. No runtime shader needed.
- **Roster** regenerated: 60, self-check 0 errors, deterministic.
- **Why the export ran 3 times:** run 1 hit the AGPL-hat licence bug. Run 2 found 2 heavy shoes and over-tall men (21 failures). Run 3 had a body-only height measure that the clothing masks break. Each run surfaced a different root cause, not the same customers failing again. Run 4 (all fixes): 58/60 pass, and the 2 that fail are deferred (below) rather than looped. A final 13-customer re-export only fixed the previews: the Workbench preview showed the hair normal map instead of the colour, and FBX wiring was unaffected.
- **Export:** **58 of 60** in `<cache>/mpfb/derived/<id>/`, each with 0 validation errors and a CC0 audit that passes (every asset unit allowed). FBX 329 MB + textures 1.43 GB in total (~30 MB per customer; textures are copied per customer, so dedupe on import).
- **Batch robustness:** one failing customer no longer stops the batch; `summary.validation.json` merges partial re-runs and lists failures; exit is still non-zero on any failure.
- **CHARACTERS.md** rewritten for MPFB: sources/licence gate, pipeline, variation (quotas, hair tint, Rule D), budgets with measured figures, texture gaps, Unity import, animation map, Rocketbox interim, staff (DEC-089).
- **Manifest:** 58 `MPFB-DERIVED-<id>` rows appended to `ASSET_CACHE_MANIFEST.json` (FBX path, sha256 equal to the validation JSON, CC0, redistributable).
- **Contact sheet:** `Docs/Assets/Specs/customers_mpfb_contact_sheet.jpg` (`contact_sheet.py`, register framing, row-major C001…, 10 per row, 58 tiles, 288 KB).

## Measured (all exported customers)
- Tris LOD0 81–127k (mean 100k, budget 150k); LOD1 26–60k (mean 38k, budget 60k); LOD2 8.3–18.9k (mean 12k, budget 20k); LOD3 2.4–5.4k (mean 3.5k, budget 6k).
- Rig: 53 bones, 0 Humanoid-required bones missing. Height f 1.50–1.75 m, m 1.61–1.95 m. 7–11 materials per customer.
- Roster self-check: 0 errors, deterministic.

## Texture and pool gaps (CHARACTERS.md §5)
GAP-CHR-4 skins 2K diffuse, no normal (procedural pore detail normal / HDRP SSS); GAP-CHR-5 eyes 1K (likely fine); GAP-CHR-6 brows/lashes 512 px; GAP-CHR-7 shoes / keyhole tank top / fedora normal 1K (hair is all ≥ 2K after the licence pruning); GAP-CHR-8 no South-Asian male skin (all 11 South-Asian customers are women); GAP-CHR-9 no CC0 beard; GAP-CHR-10 MakeHuman logo on some system casual tees; thin men's hair pool (5 + shaved).

## Proposed packets
- **GAME-CHR-002 (Unity import):** copy `<cache>/mpfb/derived/<id>/` into the project, FBX → Humanoid from the `game_engine` rig, LODGroup from `<id>_LOD0..3`. Materials → HDRP Lit (skin diffusion profile + detail normal; hair/brows/lashes alpha-clip from `alpha_cutout` in the validation JSON; tints already baked). One `PF_Customer` + `CustomerIdentity` from `customer_roster_mpfb.json`, Rocketbox Humanoid clips; EditMode checks (Humanoid valid, 4 LODs, tris within budget) and a 12-customer PERF capture.
- **PROC-CHR-004 (follow-up):** close GAP-CHR-4/6/9/10 with our own CC0 work (pore detail normal, brow cards, beard/stubble, logo paint-out), widen the hair pool, then re-export.

## Deferred
- Manifest rows were written by a one-off script (logic: one `MPFB-DERIVED-<id>` row per FBX, sha256 checked against the validation JSON); fold it into `customer_gen.py` if re-exports become routine.
- Greyscale/store-lighting contact sheet → GAME-CHR-002.
- **C028, C054** (men; bodies 1.591 m and 1.598 m against the 1.60 m validation floor). Fix options: lower the men's floor to 1.55 m (realistic adult men) or raise the men's height macro floor 0.38 → 0.42. Either changes the params; re-export just those two. Lead's call.
- Contact-sheet observations: the MakeHuman logo tee is very common (GAP-CHR-10); glasses lenses are an opaque flat blue in the preview (needs HDRP glass).

## Questions for Nolan (through the Hub)
None for Nolan. DEC-105 search done (`Docs/DECISIONS.md`, `Docs/KNOWN_GAPS.md`, `Docs/Handoffs/REF-008.md`, `Docs/Research/**`; terms AGPL, MakeClothes, South Asian, GAP-CHR, beard, MPFB, LocalThirdParty, allow-list). None of the questions below was asked before. They are licensing/technical calls that DEC-087 puts within Hub authority, so they go to the lead/Hub, not to Nolan. GAP-CHR-2 is closed by DEC-089 and is not re-asked. DEC-110: none of the questions is about physical size, distance or placement. The register viewing distance (1.2–2 m) and the LOD ranges in CHARACTERS.md are planning figures carried over from ASSET-003, not new measurements; GAME-CHR-002 should check them against the floor plan and the counter in the game files.

## Questions for the lead / Hub
1. **Licence reading.** Many MakeHuman community assets are listed as CC0 on their pack pages but their files carry the MakeClothes header `# license AGPL3`. I treat them as refused (strict reading, DEC-023/087). Source: `<cache>/mpfb/blender_user/extensions/.user/user_default/mpfb/data/clothes/jujube_newsboy_cap/jujube_newsboy_cap.mhclo` line 3. Candidates: (a) keep refusing (current); (b) accept the pack-page CC0 as authoritative. (b) would bring back beards, 7 hairstyles, 2 glasses and a cap.
2. GAP-CHR-8: is a derived (hue-shifted) CC0 skin acceptable for South-Asian men, or does the roster stay with South-Asian women only?
3. Storage of the derived customers: DEC-023 already allows CC0 in git, so this is only a size call (~15–40 MB each with textures). GAME-CHR-002 decides between git (LFS) and a local copy.
