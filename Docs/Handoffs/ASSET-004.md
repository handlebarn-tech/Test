# Handoff — ASSET-004 (2026-10-30): MPFB2 customer pipeline — PARTIAL (usage limit hit)

## Done
- MPFB 2.0.18 (sha256 matches extensions.blender.org) installed into an isolated Blender profile in the cache (`<cache>/mpfb/blender_user`, via `BLENDER_USER_RESOURCES`); the user's Blender is untouched.
- 17 CC0 MakeHuman packs fetched (`Docs/Assets/fetch_list_mpfb.json`, manifest, ledger §1d). `Tools/Blender/characters/install_mpfb.py` extracts them and writes a per-asset licence index: **58 units refused**. Several `_cc0` packs contain AGPL-headed files (skins, hair/suit alternative materials).
- `roster.py`: seeded 60-customer roster with quotas (sex 30/30; age 15/30/15; ancestry 12×5; formal ≤ 20 %), Rule D, and a CC0 audit self-check → `Docs/Assets/Specs/customer_roster_mpfb.json` (0 errors, deterministic).
- `customer_gen.py` + `blender.ps1 character …`: build via MPFB API (morphs, seeded face targets, skin, eyes, brows, lashes, hair, clothes, glasses/hat/beard), bake, Principled materials on the asset textures (copied), LOD0 (body subdiv) to LOD3 (decimate), game_engine rig, FBX, validation JSON, previews.
- C001–C003 exported to `<cache>/mpfb/derived/` with 0 errors. LOD0 90–109k, LOD1 32–45k, LOD2 11–16k, LOD3 3–4k tris; 53 bones, Humanoid set present; height 1.52–1.78 m.
- W5P m2 (ledger "not scans" claim softened) and m3 (Medical/Business cap, spec) are fixed.

## Not done (next session)
- CHARACTERS.md full rewrite for MPFB (sections: pipeline, budgets, variation, import); spec has a status note only.
- Manifest rows for the derived samples; a committed contact sheet of the previews.
- Gaps found: most skins are 2K diffuse with no normal map; eyes 1K, brows/lashes 512, some hair 1K, shoes 1K. Hair tint is not applied (planned Unity material tint). No South-Asian male skin in the CC0 set.
- Proposed packets: GAME-CHR-002 (Unity import of MPFB FBX: Humanoid from game_engine rig, HDRP Lit + SSS + detail normal, alpha-clip hair, LODGroup from `_LOD0..3`); PROC-CHR-004 (scale to 60, add hair tint, close remaining texture gaps).
- Reviewer (Docs) not yet notified: the work is partial.
