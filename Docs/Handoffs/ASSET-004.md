# Handoff — ASSET-004 (2026-10-30): MPFB2 customer pipeline — DONE (60/60 exported)

Branch `worktree-agent-ae6487dd8e469d31b` (merges `claude/task-asset-004` 225ac4a). Reviewer: Docs reviewer (pipeline/spec); Unity A later for import.

## Done
- **First session (225ac4a):** MPFB 2.0.18 in an isolated Blender profile (`<cache>/mpfb/blender_user`), 17 CC0 packs fetched, `install_mpfb.py` per-asset licence index, `roster.py` (60, quotas, Rule D, CC0 audit), `customer_gen.py` + `blender.ps1 character`, C001–C003 samples.
- **Licence-audit fix (important):** the AGPL header regex missed the MakeClothes form `# license AGPL3`, so AGPL-headed units inside `_cc0` packs were marked allowed (found when `jujube_newsboy_cap` failed). Regex widened; index rebuilt: **106 refused** (was 58). Pools pruned in `customers_mpfb.json`: 7 hairstyles, 2 glasses, the newsboy cap, both beards, cortu cargo pants/jeans shorts (shorts outfits dropped, cargo → `toigo_wool_pants`). The first session's C001–C003 used AGPL-headed hair (`littleright_bobcut_hair`) and are superseded by this run. Ledger §1d updated.
- **Budget fixes from the first 60-run (21 failures):** `toigo_stiletto_booties` (44.7k tris) → `toigo_ankle_boots_female`; `toigo_flats` (57.6k) → `toigo_ballet_flats`. Men's height macro capped 0.75 → 0.65 (4 men measured 2.04–2.10 m); height is now measured over body + clothes without hair/hat. A body-only measure was tried and dropped, because clothing masks delete the covered body vertices. LOD2 decimate 0.35 → 0.32 (C001 was 20.1k against the 20k budget).
- **Hair tint:** `customer_gen.tint_texture` recolours hair, brow and beard diffuse to the roster tint (`hair_tint_srgb` in params), keeping luminance and alpha; per-tint texture and material names. No runtime shader needed.
- **Roster** regenerated: 60, self-check 0 errors, deterministic.
- **Why the export ran 3 times:** run 1 hit the AGPL-hat licence bug. Run 2 found 2 heavy shoes and over-tall men (21 failures). Run 3 had a body-only height measure that the clothing masks break. Each run surfaced a different root cause, not the same customers failing again. Run 4 (all fixes): 58/60 pass, and the 2 that fail are deferred (below) rather than looped. A final 13-customer re-export only fixed the previews: the Workbench preview showed the hair normal map instead of the colour, and FBX wiring was unaffected.
- **Export:** **60 of 60** (C028/C054 re-exported after the lead ruling lowered the men's height floor to 1.55 m; the height check runs inside the export, so a re-export was needed) in `<cache>/mpfb/derived/<id>/`, each with 0 validation errors and a CC0 audit that passes (every asset unit allowed). FBX 329 MB + textures 1.43 GB in total (~30 MB per customer; textures are copied per customer, so dedupe on import).
- **Batch robustness:** one failing customer no longer stops the batch; `summary.validation.json` merges partial re-runs and lists failures; exit is still non-zero on any failure.
- **CHARACTERS.md** rewritten for MPFB: sources/licence gate, pipeline, variation (quotas, hair tint, Rule D), budgets with measured figures, texture gaps, Unity import, animation map, Rocketbox interim, staff (DEC-089).
- **Manifest:** 60 `MPFB-DERIVED-<id>` rows in `ASSET_CACHE_MANIFEST.json`, reproducible with `python -I Tools/Blender/characters/manifest_rows.py` (replaces only MPFB-DERIVED rows, checks sha256 against each validation JSON).
- **Contact sheet:** `Docs/Assets/Specs/customers_mpfb_contact_sheet.jpg` (`contact_sheet.py`, register framing, row-major C001…, 10 per row, 60 tiles, 295 KB).

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
- (done) The manifest-row logic is now `Tools/Blender/characters/manifest_rows.py`.
- Greyscale/store-lighting contact sheet → GAME-CHR-002.
- (done) C028/C054: resolved by the lead ruling (men's floor 1.55 m), both pass.
- Contact-sheet observations: the MakeHuman logo tee is very common (GAP-CHR-10); glasses lenses are an opaque flat blue in the preview (needs HDRP glass).

## Questions for Nolan (through the Hub)
None for Nolan. DEC-105 search done (`Docs/DECISIONS.md`, `Docs/KNOWN_GAPS.md`, `Docs/Handoffs/REF-008.md`, `Docs/Research/**`; terms AGPL, MakeClothes, South Asian, GAP-CHR, beard, MPFB, LocalThirdParty, allow-list). None of the questions below was asked before. They are licensing/technical calls that DEC-087 puts within Hub authority, so they go to the lead/Hub, not to Nolan. GAP-CHR-2 is closed by DEC-089 and is not re-asked. DEC-110: none of the questions is about physical size, distance or placement. REVIEW-ASSET4 fixes: the register distance now cites SCENE_ANCHORS Call↔Operator 1.34 m (REF-011, Low, GAP-129). That file is not in this worktree, so the value is quoted from the review, not re-measured. LOD bands and roster quotas are marked [GDD]. GAP-CHR-4..10 are in KNOWN_GAPS.md. GAP-CHR-9 names the two allowed jartur69 bearded skins.

## Lead rulings applied (2026-10-30)
1. AGPL/CC-BY-headed files stay refused even inside packs labelled CC0; the stricter audit stays.
2. Men's height floor 1.55 m (params `height_m_range`); C028/C054 pass.
3. No hue-shifted skins: GAP-CHR-8 stays open as a sourcing task, roster unchanged.
4. Derived customers stay in the local cache, never in git; GAME-CHR-002 copies them at import (CHARACTERS.md §6).
5. Manifest rows reproducible via `manifest_rows.py`.

## Open
- None blocking. Gaps GAP-CHR-4..10 are for PROC-CHR-004.
