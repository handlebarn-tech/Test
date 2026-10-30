# PROC-003 handoff — F010 visible pile, natural packing, REF-007 jar size, house-smalls jar

**Status:** done; validation passes. Branch `claude/task-proc-003` (off main a245942). Packet `Docs/Tasks/Active/PROC-003.md`. Not touched: `Code/Simulation|Presentation`, scenes, `studio.ps1`, the ART-003/004 branch.

## Delivered
- **DEC-046:** `jar_fill.json` `buds.mound` is a 5-bud front heap: 4 on the floor's front/centre plus 1 on top. It fills first, so F010 (5 of 54 buds) shows a pile above the 55 mm band in every look. LOD2 blocks are raised to the same minimum.
  - `jar_fill.build()` fails any step above 0 g whose top is less than 12 mm above the band. The Unity test checks the same thing on every step and LOD.
  - Lower steps stay subsets of higher ones, and tops still rise monotonically.
- **Packing (W4E n1):** seeded per-layer offsets (±¼ pitch), 14 mm x/y and 6 mm z jitter, bud size 0.8–1.15×. Full jars no longer read as 3 columns. Every step stays inside the per-step budgets (LOD0 5000, LOD1 1400, LOD2 40), which the generator enforces; all steps of one look total LOD0 ≈10.1k (budget 12k).
- **Canister size (REF-007, Low–Med):** 6.0 × 5.5 in footprint, 10.25 in overall (body 235 mm + 1 in lid), ~4.3 L cavity. The fill uses 6 layers (was 7) to fit the shorter jar.
- **House-smalls jar (DEC-042a):** `params/deli_jar_smalls.json` gives `PROC_DeliJar_Smalls`, the published POP 4 L size 6.1 × 5.3 × 10.4 in (High).
  - It has no brand band. The label card and THC % tag are kept as the shop convention (Low).
  - The lid split and corner radius are not published: **GAP-PROC-12** (new; renumbered by REVIEW-W4P, GAP-PROC-10 is PROC-004's).
- **W4E m2:** both jar FBXs now copy to `Assets/_Game/Art/Procedural/DeliJar/` (folder kept from GAME-005 in the W4P re-merge), so GAME can parent the fill to the jar.
- Updated: `JarFillImportTests` (new cavity + DEC-046 check), `PROC_PIPELINE.md` (PROC-003 section), both contact sheets.

## Validation (this machine)
- All 5 generator runs (package box/pouch, deli jar, smalls jar, jar fill) and both contact sheets ran twice: sha256 identical on all 22 outputs.
- The package FBXs are unchanged from main.
- Contact sheets are 855 KB and 888 KB (≤1 MB).
- `unity-compile` OK; `unity-test-edit` 149/149.

## For the Hub (DEC-033)
1. **[NEEDS-HUB] Smalls fill:** the smalls jar has no fill set yet. Its cavity is nearly the canister's, so GAME can reuse `PROC_JarFill_*` inside it (fit checked by eye, not by the test). Alternatively, a `jar_fill_smalls.json` with smaller buds would add ~4.5 MB of FBX, given the churn noted in W4E m3. Which do you want?
2. **[NEEDS-HUB] Register GAP-PROC-12:** smalls lid/corner/label, not published.
3. **Unchanged / still open:** the GAME hook from the PROC-002 handoff; the canister size is still an estimate (GAP-PROC-01); the LFS rule for procedural FBX (W4E m3).
