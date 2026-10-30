# ASSET-007 handoff: studio-built nitrile glove overlay

**Status:** done; ready for a fresh review. Blender only, no Unity. Replaces the ChatGPT R4.7 glove tool that was rejected as built (DEC-111, IMP-003 R4.7).

## What was built
- **`Tools/Blender/characters/glove_overlay.py`** uses the **hand vertex-group mask** approach from the packet. It builds the glove from the baked MPFB body:
  1. It copies the body mesh, so the glove keeps the same topology, UVs and skin weights and deforms with the hand.
  2. It keeps only the faces weighted to the forearm chain (`lowerarm_*` and its children).
  3. It cuts each arm with a plane square to the forearm, 7.5 cm above the wrist.
  4. It pushes the result 1.5 mm out along the normals, adds a rolled bead at the cuff, and adds a 2.2 mm lip back toward the skin so the cuff edge has thickness.
  5. It deletes the hand skin under the glove, as MPFB's own clothes masks do, but keeps 2 cm of skin under the cuff so no gap shows. Without this step the decimated skin at LOD2/3 and the fingernails showed through (seen on the first contact sheet).
  - Result: two separate gloves, never a full-body shell. A self-check (`_check`) fails the build if any glove vertex sits above the cuff, a side is missing, or a vertex has no skin weight.
- **Material `M_nitrile_glove`:** Principled BSDF, near-black, non-metal, satin finish (roughness about 0.40). It uses a studio-made **2K tiling micro-texture normal map and roughness map**, generated procedurally, so they are CC0 by construction and need no ledger row. The glove gets its own 0–1 UV layout, scaled uniformly, so the 2K maps are not spent on the skin atlas. The textures are written next to the FBX as `T_nitrile_glove_{normal,roughness}.png` and listed in the validation JSON.
- **`customer_gen.py` (small hook only):**
  - A roster or staff entry with `"gloves": true` gets the glove part `<id>.nitrile_gloves`, added after the MPFB material pass.
  - The validation JSON gains `gloves` and `gloves_check`, and a glove failure is a validation error.
  - The glove is left out of the height measurement.
  - The module-level `main()` now sits under `if __name__ == "__main__"`, so other scripts can import it. Blender's `--python` runs it as `__main__`, so `blender.ps1 character` behaves the same as before.
- **LODs:** the glove goes through the existing `make_lod` chain (LOD0 to LOD3). LOD0 subdivides the glove only if `"nitrile_gloves"` is in `lods.LOD0.subdiv_parts`. The demo adds it in memory. **The future staff params file must list it**, the way it lists `"body"`. I did not edit `customers_mpfb.json` (customers wear no gloves, and ASSET-005/006 may be editing that file).

## Proof
- Demo command (isolated MPFB profile):
  ```
  $env:BLENDER_USER_RESOURCES='<cache>/mpfb/blender_user'
  blender --background --python-exit-code 10 --python Tools/Blender/characters/glove_overlay.py -- Tools/Blender/params/customers_mpfb.json C003,C004,C006
  ```
  It writes to `<cache>/mpfb/derived_gloves/GLV_<id>/`. That is a separate folder, so the customer contact sheet and `summary.validation.json` are untouched.
- **Contact sheet:** `Docs/Assets/Specs/gloves_contact_sheet.jpg` (157 KB). It has one row per character (C003 f heavy, C004 m heavy, C006 m older slim with long sleeves). Each row shows the left-hand close-up at LOD0, LOD1, LOD2 and LOD3, rendered in EEVEE, then a full-body LOD0 view.
- **Results:** 0 validation errors and an empty `gloves_check` for all 3. Triangle counts with gloves (LOD0/1/2/3):

  | Character | LOD0 | LOD1 | LOD2 | LOD3 |
  |---|---|---|---|---|
  | C003 | 99.4k | 34.5k | 10.9k | 3.1k |
  | C004 | 89.8k | 30.3k | 9.5k | 2.8k |
  | C006 | 83.8k | 29.0k | 9.1k | 2.6k |

  For comparison, C004 without gloves is 89.0k / 30.1k / 9.4k / 2.7k. The masked hand skin roughly pays for the glove, which is about 6.9k triangles at LOD1. All counts are well inside the CHARACTERS §4 budgets.
- **Regression:** a normal customer build (C001, no gloves) after the change matches its earlier triangle counts and height exactly (127254 / 58058 / 18392 / 5213, 1.629 m, 0 errors).

## Known limits
- **LOD3:** the decimated cuff can show a small notch (C004 tile). This LOD is used beyond 15 m only.
- **Nails:** the nail bumps read through the glove at LOD0/1, as nails do through real nitrile. Kept on purpose.
- **Removability:** gloves are baked per character, because the skin underneath is masked and `make_lod` joins all parts into one mesh. Gloves that go on and off during play would need a second body variant (not in scope).
- **Long sleeves:** under a long sleeve, MPFB's sleeve mask has already removed the forearm skin, so the glove ends where the skin ends. The sleeve hides it (C006 row).

## Gaps
- **GAP-GLV-1: glove colour.** The REFERENCES_INDEX §3 BAND rows 01, 07 and 11 say "nitrile gloves" or "gloves" with no colour. The "Black nitrile ✓ (RI §3)" in the IMP-003 checklist is not backed by those rows. Placeholder: **black** (`BASE_SRGB` in `glove_overlay.py`, one constant to change). I did not inspect the photos; the packet allows Research, KNOWN_GAPS and CCTV handoffs only.
- **GAP-GLV-2: who wears gloves.** The sources are DEC-079 (managers refill and clean jars) and OFFICE_FINDINGS O7 (deli handling training includes gloves). BAND rows 01/07/11 show budtenders (polo/tee) with gloves on the floor. Working answer: gloves are an optional per-staff flag. The staff roster (CHARACTERS §9, not built yet) decides which staff get them.

## Questions for Nolan (through the Hub)
1. **Glove colour (GAP-GLV-1):** the source is the REFERENCES_INDEX §3 BAND rows 01/07/11, which say gloves but no colour. Candidates: black (current placeholder), blue, purple. What colour are the store's nitrile gloves?
2. **Who wears them (GAP-GLV-2):** do budtenders on the floor wear gloves all the time (BAND rows suggest yes), or only managers doing deli refills (DEC-079)? Candidates: all floor staff / deli handling only / per-person.

## Follow-ups for the Hub
- After ASSET-005/006 merge, add one line to CHARACTERS.md §9 (staff): "Staff gloves: `"gloves": true` per staff entry, `nitrile_gloves` in LOD0 `subdiv_parts`, ASSET-007." I left CHARACTERS.md alone to avoid colliding with that work.
- `IMP-003_PROC_FIX_CHECKLIST.md` R4.7 can be ticked once this merges.
