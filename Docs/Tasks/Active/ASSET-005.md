# ASSET-005 / ASSET-006 — Studio-built customer wardrobe and hair

**Role:** Worker (DEC-116) · **Priority:** P1 · **Reports to:** Hub · **Reviewer:** fresh reviewer the Hub picks · **Depends on:** ASSET-004 (done, 60/60 exported) · **Starts on:** Hub GO.

## Why
DEC-111: the ChatGPT R4 wardrobe and hair are rejected as built (IMP-003 checklist R4.1 block garments, R4.2 all 9 styles crash), but the assets still get made. Bar: DEC-084 (realistic close-up at the register, LODs carry performance), DEC-114 (tri guides, judged by the visual read).

## Scope
1. **Wardrobe (ASSET-005, R4.1).** Keep the drop's garment list as the spec: `TeeClassic, TeeRelaxed, TankClassic, HoodiePullover, JeansStraight, ShortsCasual, WorkPolo, ScrubTop, ScrubPants, BusinessShirt, BusinessTrousers` (drop `Tools/Blender/params/wardrobe_library.json` `variants`). Keep colourways (tops: black, white, charcoal, sage, navy, sand, rust; bottoms: black, indigo, khaki, charcoal, navy, olive), material variants (jersey, fleece, denim, scrub, woven) and material states (clean, washed, sun_faded, workworn_subtle) from drop `Docs/Round4/COLOR_MATERIAL_VARIANTS.json`. Drop root: `Dispo Game Imports/Dispo_Game_Blender_PROC_Round4_HQ_v2_EvidenceDriven/`.
   - Preferred: map each garment to an **allowed** MPFB2/MakeHuman system garment (already fitted and rigged). Colourways via the ASSET-004 `tint_texture` approach (baked, per-tint material names).
   - Only where no allowed CC0 garment exists: our own procedural shell (openings, 2–4 mm solidify, hems, seams, collars; fit and weights per R4.0.4/R4.6 via MPFB2 proxy fitting + weight transfer). Fabric textures CC0 (ambientCG/Poly Haven) or our own, registered in `LICENSE_LEDGER.md` (R4.0.7).
   - Wear states are subtle material treatments, never socioeconomic coding (drop note; DEC-087(4)).
   - Fixes ASSET-004 GAP-CHR-10 (MakeHuman logo tee) where a garment replaces it.
2. **Hair (ASSET-006, R4.2).** Keep the 9-style list: cropped, side part, bob, shoulder wavy, long straight, long curly, curly halo, locs, ponytail. Map each to allowed MPFB2 CC0 hair; build alpha-tested card clumps (double-sided material or separate back-face verts, R4.0.2) for styles with no allowed hair. Widen the thin men's pool (5 + shaved, CHARACTERS.md §5). Hair tint stays `tint_texture`.
3. Update `Tools/Blender/params/customers_mpfb.json` pools, re-bake the roster (`roster.py`, quotas and Rule D unchanged), re-export all 60.

## Out of scope
Staff uniform (R4.4/DEC-089/113), headwear (R4.3), glove (ASSET-007), beards (GAP-CHR-9, PROC-CHR-004), Unity import (GAME-CHR-002), skin textures.

## Rules
- Licences: CC0/MIT only (DEC-023/087). Use the ASSET-004 per-unit licence index; AGPL/CC-BY-headed units stay refused even inside `_cc0` packs (ASSET-004 lead ruling 1). New studio-made assets are CC0 by construction and get ledger rows.
- Every value cites its source (drop file, MPFB unit, CHARACTERS.md, DEC) or is a labelled `GAP-CHR-<n>`.
- Binaries stay in the cache (`<cache>/mpfb/derived/`), never in git; contact sheet JPG ≤ 1 MB is fine.
- No real-person likeness. Isolated Blender profile only.

## Acceptance
- **Licence audit clean:** every unit in every customer allowed by the index; 0 AGPL/CC-BY slips (re-run the widened header regex over any new pack).
- **60/60 customers re-export with 0 validation errors**, tris within the CHARACTERS.md §4 budgets, roster self-check 0 errors and deterministic.
- **Contact sheets read as real people** (DEC-084/114): regenerate `customers_mpfb_contact_sheet.jpg`, plus one wardrobe sheet (11 garments × colourways) and one hair sheet (9 styles).
- Each of the 11 garments and 9 styles is either covered (named unit or studio asset) or a labelled GAP with candidates.

## Deliverables
Params/generator changes, any procedural garment/hair generators under `Tools/Blender/characters/`, updated `CHARACTERS.md`, ledger + manifest rows, contact sheets, `Docs/Handoffs/ASSET-005.md` (covers ASSET-006).
