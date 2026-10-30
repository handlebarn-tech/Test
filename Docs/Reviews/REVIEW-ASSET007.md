# REVIEW-ASSET007: studio-built nitrile glove overlay

- **Reviewed:** `claude/task-asset-007` @ `dba3961`
- **Merge base:** `36be358` (merged `--no-ff` onto `main` @ `f0300b1` on `review/asset007`, clean)
- **Sources read:** `Docs/Tasks/Active/ASSET-007.md`; `git diff main...dba3961`; `Docs/Handoffs/ASSET-007.md` (Proof, Known limits, Gaps); `Docs/DECISIONS.md` DEC-023, DEC-047, DEC-079, DEC-084, DEC-087, DEC-111, DEC-114, DEC-122; `Docs/Imports/IMP-003_PROC_FIX_CHECKLIST.md` R4.4/R4.7; `Docs/REFERENCES_INDEX.md` §3 BAND 01/07/11; `Docs/Research/OFFICE_FINDINGS.md` O7; `Tools/Blender/characters/customer_gen.py` (`make_lod`); `Docs/Assets/Specs/gloves_contact_sheet.jpg` and the full-res 640 px tiles in `<cache>/mpfb/derived_gloves/`.

## Verdict: PASS with minors

## Checks
| Check | Result |
|---|---|
| DEC-047 store values | Pass. Glove colour is the labelled placeholder GAP-GLV-1 (`BASE_SRGB`, also in the validation JSON `gaps`). Who wears gloves is GAP-GLV-2, an opt-in per-entry flag. Citations verified: BAND 01 ("nitrile gloves; teal polo + gloves"), BAND 07 ("polo + gloves"), BAND 11 ("gloves"), DEC-079 (managers do deli refills), O7 (deli handling training includes gloves). The worker's claim that IMP-003 R4.7 "Black nitrile ✓ (RI §3)" has no source is correct: no BAND row gives a colour. Cuff length, offsets and texture size are asset-design values, not store facts. |
| R4.7 rejection fixed (no full-body shell) | Pass. Hand vertex-group mask (`lowerarm_*` chain plus a plane cut 7.5 cm above the wrist). `_check` fails the build on verts above the cuff, a missing side or unskinned verts. It returned `[]` for all 3 characters. |
| Packet validation: demo `glove_overlay.py -- customers_mpfb.json C003,C004,C006` (headless Blender 5.2, isolated MPFB profile) | Exit 0, 0 errors. Tris LOD0/1/2/3: C003 99408/34520/10862/3107; C004 89750/30286/9506/2764; C006 83832/29024/9103/2637. Glove at LOD1 is 6.8–7.0k tris. These match the handoff exactly. The regenerated contact sheet is byte-identical to the committed one (`git status` clean), so the build is deterministic. |
| Regression: plain customer C001 through the imported `customer_gen.main` (output to scratch) | 127254/58058/18392/5213 tris, 1.629 m, 0 errors, `gloves: false`. Identical to the cached `derived/summary.validation.json`. The `if __name__ == "__main__"` guard is safe. |
| Export | `GLV_C004.fbx` references `T_nitrile_glove_normal.png`. Both 2K maps are in `textures/`, and the validation JSON lists the material, maps and GAP. |
| LOD chain | Uses the existing `make_lod`. The glove is subdivided at LOD0 only when listed in `subdiv_parts`. |
| Licensing (DEC-023) | Textures are procedural from a fixed seed. No third-party input, so no ledger row is needed. |
| Scope | No ASSET-005/006 files edited; `customers_mpfb.json` untouched. |
| **Visual (DEC-084/114/122)** | It reads clearly as a black nitrile exam glove at every LOD and in the full-body view. Fit is tight to the MPFB hand: the finger and knuckle form carries through and the offset shows no visible bulk. The cuff sits a believable ~7.5 cm up the forearm with a clean edge, and there is no skin poke-through at LOD0–2. On C006 the long sleeve correctly covers the cuff. Proportion and silhouette are right. Material is acceptable but not at the bar yet (minor 1). |

## MAJOR
None.

## minor
1. **Material micro-texture reads as blotchy mottling, not fine nitrile.** At close-up register distance (the 640 px LOD0 tiles), the normal/roughness noise shows as centimetre-scale dark and light patches across the back of the hand and the cuff. It looks like stained or crumpled rubber, not the even satin of a nitrile glove. The code intends 2–3 px pebbles, but the glove's uniform 0–1 UV rescale leaves the texel density too low for that. Acceptance item: DEC-084/122 material quality.
2. **LOD3 cuff sawtooth.** Decimation leaves a visible zigzag notch at the cuff on C003 and C004. Disclosed, and LOD3 is used beyond 15 m only, but it still reads as torn.
3. **Thumbnail reads as bare nail at LOD0/1.** On C003 and C004 the thumbnail shows as a pale grey patch, which reads as a hole more than a nail bump under the film. Disclosed as intentional. It needs a look together with minor 1.
4. **Rest pose only.** The proof shows the A-pose only. There is no posed-finger or fist check of the glove deforming with the hand. Copied weights make it likely fine, but it is unproven.
5. **`subdiv_parts` dependency is silent.** A staff params file that sets `"gloves": true` but leaves out `nitrile_gloves` from LOD0 `subdiv_parts` gets an unsubdivided glove over a subdivided body, and no error or warning appears. Only the handoff records the requirement.
6. **2× 2K glove maps written per character.** Each gloved staff member gets an identical copy of `T_nitrile_glove_{normal,roughness}.png`.
7. **Merge-order risk with ASSET-005.** That packet (Active) owns generators under `Tools/Blender/characters/`, and this branch edits `customer_gen.py` (import, export hook, `__main__` guard). Whichever merges second must re-run the C001 regression.
8. **Handoff format.** There are no `Validation`, `Not-done` or `## For the Hub` sections (the equivalents are Proof, Known limits, Gaps and Follow-ups). GAP-GLV-1/2 and the IMP-003 R4.7 "Black nitrile ✓" correction are not proposed as KNOWN_GAPS/registry entries for the Hub.
