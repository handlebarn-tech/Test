# REVIEW-W4E — PROC-002 (deli canister + bud fill generator)

**Verdict: PASS** (no blockers; minors and notes below go to the Hub/GAME, none need a PROC rework before merge).
**Branch:** `review/wave-4e` = main (ba81722) + `--no-ff` merge of `claude/task-proc-002-99e871` (8102f0d). Clean merge, no conflicts. Reviewer: REVIEW-W4E, 2026-10-29.

## 1. Design vs DEC-042/043/019 — OK
- `deli_jar.json`/`deli_jar.py`: tall square clear acrylic body (0.15 × 0.15 × 0.28 m), white pop-top lid with recessed button, coloured base band (`band.rgba`, per-brand runtime param, `UVMap_Label` on the front), front label card, THC % tag. No tong cups. 776/216 tris (budget 1000/250).
- Capacity: fill = grams / 454 (DEC-019); jar `_note` and GAP-PROC-01/02/03/09 label every size as a photo estimate pending REF-007. Bud looks/colours flagged [GDD] (GAP-PROC-07), fill height linear (GAP-PROC-08). No invented store facts.
- Contact sheets viewed: `PROC_contact_sheet.png` (jar reads as the photo design: band, lid, label + tag) and `PROC_jar_fill_contact_sheet.png` (6 looks × F000…F100 + LOD1/LOD2; steps rise monotonically, F000 = crumbs, buds stay inside the glass, looks are distinguishable). 628 KB / 822 KB (≤1 MB).

## 2. Determinism — OK
All four generator runs (deli_jar, package_base ×2, jar_fill) + both contact sheets, run twice from clean shells: sha256 identical between runs **and** identical to the committed files (FBX in `Art/Exports` and the Unity copies, manifest, both sheets). Only diff seen was LF/CRLF working-copy noise on `manifest.json` (content equal; reverted).

## 3. Unity / budgets / scope / licences
- Unity: see Validation below.
- Budgets: per visible step LOD0 4560/5000, LOD1 1140/1400, LOD2 28/40, enforced in `jar_fill.build()` and in the EditMode test. Fits ASSET_PRODUCTION_PLAN §8 (distant filler = very low poly) and §22 (no huge per-jar bud meshes). ~77 jars × 4560 is the worst case only if every jar is LOD0 and full.
- Scope: no edits to `Code/Simulation|Presentation`, graybox scenes or `studio.ps1` (checked with `git diff --name-only`). `run_generator.py`/`blender.ps1` changes are the minimal extensions the packet allowed; PROC-001 outputs regenerate byte-identically.
- Licences (DEC-023): all assets are procedural from repo code; no third-party content, nothing for the cache/LFS.

## 4. Fill interface vs GAME-002 — OK
`InventoryService.Fill = Grams / startGramsPerBatch` (454), `IsSoldOut` at ≤0 g, `IsLow` < 0.25, `Sold` event — all match the handoff hook (F000 on sold out, else nearest of 10/20/40/70/100 ties up, update on `Sold` for `e.BatchId`, stable non-salted hash for batch → look). Hook is described, not built (correct: Presentation not owned).

## 5. DEC-013 — OK
Before the Unity run: 1 editor (build-002) + its AssetImportWorker + the Hub `serve` process; this run made 2 editors.

## Findings
**Blockers:** none.
**Minor (Hub to route, not PROC rework):**
- m1 **F010 invisible from the front.** The 55 mm band hides the 10 % step; DEC-027 starts jars as low as 0.05, which maps to F010, so a jar at 5–14 % looks empty from the front while it is not SOLD OUT. The LOW label still shows. Hub/DES decision (handoff asks it too): accept, or give F010 a minimum visible pile above the band.
- m2 **GAME follow-up contract.** `SliceBotTests` (PlayMode) asserts `JarFillShown == grams/454` linearly; when the GAME task swaps the cylinder for stepped meshes that test must change to the step mapping. Also `PROC_DeliJar` itself has no `unity_dir`, so the GAME task needs the jar FBX copied into Unity (or a `unity_dir` added to `deli_jar.json`) before the fill can be parented to it.
- m3 **Binary churn.** ~4.5 MB of fill FBX are committed twice (Art/Exports + Unity copy), not in LFS. Allowed by DEC-023 (LFS rule is for ThirdParty) and deterministic, but every param tweak re-adds ~9 MB to history. Hub: consider an LFS rule for `Art/Exports/**/*.fbx` + `_Game/Art/Procedural/**/*.fbx`.
**Notes:**
- n1 Full jars read as 3 neat vertical columns (3×3 lattice, 10 mm jitter). Fine as a GAP-PROC-07 placeholder; the §22 scan buds or more jitter fix it.
- n2 Packet names the sheet `PROC_JarFill_contact_sheet.png`; delivered as `PROC_jar_fill_contact_sheet.png` (the generic sheet naming). Docs and handoff use the delivered name; no change.
- n3 LOD0 total over all steps is 11600 / 12000; adding a seventh step would trip the total budget.
- n4 Register GAP-PROC-07/08/09 in `KNOWN_GAPS.md` and move the PROC-002 packet to Done (Hub, per handoff).

## Validation
- Blender 5.2 headless: two full runs, sha256 identical (§2).
- `studio.ps1 unity-compile`: pass (csErrors=0, CompileCheck OK).
- `studio.ps1 unity-test-edit`: pass, 147/147 (incl. the 6 `JarFillImportTests` cases; main now has more tests than the 30 in the PROC handoff).
