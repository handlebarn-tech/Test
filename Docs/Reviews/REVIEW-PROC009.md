# REVIEW-PROC009: studio-built parked vehicles

# Round 2 (fix round 1)

**Reviewed:** `claude/jovial-meninsky-908c0a` @ `429872f` · **Review branch:** `review/proc009-r2` (`review/proc009` @ `a8cfb3d` + worker branch, `--no-ff` merge `dbbaf57`) · **Reviewer:** fresh, Hub-spawned (STUDIO_OS §0.7)
**Sources read:** the packet; the diff `2495e6c..429872f`; `Docs/Handoffs/PROC-009.md` (fix round 1, Validation, Not done); round 1 of this review (below).

## Verdict: FAIL (1 MAJOR)

## Checks
1. **Blender validation.** `blender.ps1 parked_vehicles Tools/Blender/params/parked_vehicles.json` exited 0. All 3 validation JSONs show `passed: true` with no errors and no warnings. The tri counts match the handoff exactly: Sedan 88458/29054/6900/1382, Hatchback 87732/28732/6992/1400, SUV 89050/29852/7462/1536.
2. **Determinism.** After my rerun all 3 FBX are sha256-identical to the commit, and the Unity copies are byte-identical to the Art exports. The JSONs differ only in line endings. Rerunning `parked_vehicles_sheet.py` reproduced the committed sheet byte for byte (sha256 `8f850e2d…`).
3. **Toolkit self-test.** `[SELFTEST] all passed`.
4. **Old Specs PNGs removed.** Nothing outside Handoffs/Reviews still points at them.
5. **Visual review (DEC-122/DEC-114), judged myself.** I looked at the committed sheet and at LOD0 front/rear 3/4 tiles that I re-rendered at 1500 × 1000 with the worker's own sheet code (scratch only, not committed).

## Round-1 findings
- **MAJOR 2 (contact sheet): FIXED.** The sheet is 2520 × 840 and 527 KB. It has one row per class and six tiles per row: LOD0 front 3/4, rear 3/4 and side, plus LOD1, LOD2 and LOD3. Every tile is labelled with asset, LOD/view, tris and frame width. The LOD steps can be judged: the silhouette holds through LOD2, and LOD3 is a hull with boxes, which is acceptable at that range.
- **MAJOR 1 (visual read): mostly fixed, one new defect (see MAJOR below).**
  - Sedan A-pillar wedge: fixed (black sail panel).
  - Per-class fascia: the hatch gets two lamps and a mesh grille, the SUV a two-bar chrome grille with blunt lamps and vertical tails, the sedan wide tail lamps. They now differ. The sedan front is still weak, though (MAJOR, item b).
  - Hatchback: the short hood and sloped hatch glass now read as a compact 5-door hatch. Fixed.
  - SUV: the greenhouse now runs to the tail; the tailgate glass is framed and raked; there is no deck ledge. It reads as a boxy compact SUV/wagon, which is acceptable for the generic class. Fixed.
  - Mirrors: tapered rounded housings. Fixed.
  - Raked ends: visible and they help.
  - "Clay" paint: deferred to the texture dependency, as round 1 ruled.
- **minor 1 + 2 (texture maps, lightmap UV):** raised in the handoff as FOR THE HUB dependencies. Done as ruled.
- **minor 3 (plate rule):** now cited, A.R.S. 28-2354(A)(1), in params `_sources` and PROC_PIPELINE. Fixed.
- **minor 4 (`run_generator.py`):** unchanged; still the Hub's call.

## MAJOR
1. **The front end still breaks the DEC-084 read (R3b.7 "never low-poly or generic-looking").**
   - **a. New in this round: the undertray shows as a black brick under the front bumper on all three classes.** It is visible in every front 3/4 tile from LOD0 to LOD2 and in the LOD0 side views. The cause is in `parked_vehicles.py` `bumpers()`, lines ~477–481. The intake/undertray is a square-edged box, `intake_m` wide (the full width at the rear), hung *below* the bumper bottom (`z0 - ih/2`). Its front face sits 1 cm behind the bumper's furthest point. But the bumper is rounded and raked, so the box's front face and lower edge stand proud of the curved cover and read as a separate block hanging under the car. **Fix:** put the intake *inside* the bumper cover as a recessed opening, or tuck the box behind the cover's curve and above its lowest line. Any lip should follow the bumper plan curve, not be a straight box.
   - **b. The sedan fascia still reads as a blank slab.** The "slim wide" headlamps render as small amber dots at the corners. The slatted grille reads as a black licence-plate rectangle. So at 3/4 the sedan's front still has no lamps and the bumper looks like a box, which is round 1's complaint. **Fix:** headlamps big enough to read at parking-lot distance (they should wrap into the fender, as the handoff's own round-0 "Look" note proposed), and a grille whose slats are visible.

## minor
- None new. (Observation, not a blocker: overall the set still reads late-1990s/2000s rather than 2020s. Rounder plan-view corners and wrapped lamps would help most. Texture maps will remove the clay read.)

## Not checked
- Unity import (packet: not needed); in-scene placement in the lot.

---

# Round 1

**Reviewed:** `claude/jovial-meninsky-908c0a` @ `2495e6c` · **Merge base:** `3ab683b` · **Review branch:** `review/proc009` (main @ `8081e5e` + worker branch, `--no-ff` merge `643483e`) · **Reviewer:** fresh, Hub-spawned (STUDIO_OS §0.7)
**Sources read:** `Docs/Tasks/Active/PROC-009.md`; the full diff `3ab683b..2495e6c`; `Docs/Handoffs/PROC-009.md` (Done, Validation, Not done, For the Hub); DEC-023, DEC-032, DEC-071, DEC-084, DEC-087, DEC-097, DEC-111, DEC-114, DEC-122 in `Docs/DECISIONS.md`; `Docs/Imports/IMP-003_PROC_FIX_CHECKLIST.md` R3b.7; `Docs/Reviews/REVIEW-PROC006c.md` (contact-sheet precedent).

## Verdict: FAIL

## Checks
1. **Blender validation.** `Tools/Blender/blender.ps1 parked_vehicles Tools/Blender/params/parked_vehicles.json` exited 0. All 3 validation JSONs: `passed: true`, `errors: []`, `warnings: []`, 6 collision boxes each. The tri counts match the handoff exactly (Sedan 86134/27914/6644/1382, Hatchback 83876/27260/6694/1400, SUV 86422/28682/7164/1536).
2. **Determinism.** After my rerun all 3 FBX are sha256-identical to the commit, and each Unity copy is byte-identical to its Art export. The validation JSONs and `manifest.json` differ only in line endings (`git diff --ignore-cr-at-eol` empty). `contact_sheet parked_vehicles` reproduced the committed PNG byte for byte.
3. **Toolkit self-test.** `blender -b --factory-startup -P Tools/Blender/tests/test_validation.py` prints `[SELFTEST] all passed`.
4. **Citations (DEC-047).** `parked_vehicles.json` carries `_sources`, a `_class` per entry and GAP-PROC-23/24 for every dimension and colour; the class choice cites CCTV R1C1/R1C2 and RG3-4. No uncited store value found. (The Arizona rear-plate rule is a legal fact "from memory": minor 3.)
5. **Licensing (DEC-023/087).** Scripted rebuild, no third-party source, so no LICENSE_LEDGER row is needed. Pass.
6. **Unbranded / trade dress (DEC-071).** No badges, no wordmarks, blank plates. The grille, lamp and greenhouse shapes do not copy any real model's signature elements; the three bodies read as generic classes. Pass.
7. **R3b.7 mechanics.** Wheels sit inside the arches, glazing is flush (faces of the greenhouse), shut-line grooves exist, LOD0 is inside the 30–150k guide, LOD0–LOD3 chain present. Pass mechanically.
8. **Visual review (DEC-122/DEC-114), judged myself** on `PROC_parked_vehicles_review_3q.png` (1200 × 1050, zoomed crops) and `PROC_parked_vehicles_contact_sheet.png` (480 × 480). Fails: see MAJOR 1 and 2.
9. **Texture deferral (asked by the Hub).** See minor 1 for the ruling.

## MAJOR
1. **The visual read fails DEC-084 and R3b.7 ("real panels", "never low-poly or generic-looking").** Triangle count is not the problem (DEC-114); the shapes are. In the 3/4 sheet:
   - **Sedan:** at the base of the near A-pillar the greenhouse does not close onto the cowl; a grey wedge shows between pillar, glass and hood. The hood sits like a lid over a flat vertical fascia, and the bumper reads as a box (the handoff's Not-done admits the fascia).
   - **All three:** the same fascia (rectangular grille, square lamps, slab bumper) and the same rear lamp blocks, so the classes differ only in greenhouse and length.
   - **Hatchback:** it has a sedan-length hood and a separate ledge above the tail lamps, so it reads as a long-hood wagon, not a compact hatch.
   - **SUV:** the rear has no tailgate shape. A thin-pillared glass box sits inset behind a flat deck ledge, which reads as a pickup with a glass cap; ride height and body side read as a wagon, not an SUV.
   - **Mirrors** on all three are rectangular boxes on stubs.
   - No wear and no surface detail (see minor 1), so the paint reads as clay.
   Together these give a boxy 1980s kit-car read, not "real products" that belong in a 2020s Phoenix lot. This is the R3b.7 rejection reason restated, so the asset has not yet replaced the rejected R3b vehicles (DEC-111).
2. **The contact sheet cannot carry the DEC-122/DEC-114 visual review.** The packet's deliverable is a contact sheet; DEC-122 asks for readable, labelled sheets. `PROC_parked_vehicles_contact_sheet.png` is 480 × 480 with 9 unlabelled tiles (about 60–130 px per car), LOD0 front/side and LOD3 only. LOD1 and LOD2 never appear, so the LOD steps cannot be judged visually, and nothing names the class, LOD or tris. The 3/4 review sheet helps for LOD0 but is unlabelled and LOD0-only. (Precedent: REVIEW-PROC006c accepted a 1500 × 4800 sheet with labelled LOD0 3/4, side, LOD1, LOD2, LOD3 tiles.)

## minor
1. **Texture maps deferred (Hub question).** Ruling: **acceptable as a blocked dependency, not as Done.** DEC-084 requires 2K–4K PBR texture sets and proper UVs, and the packet lists "PBR textures"; nothing in DECISIONS rules texture maps optional. But the unwrap/bake pipeline (Q0.2/Q0.3) does not exist on `main` and no PROC asset merged so far has maps, so one packet cannot be expected to build it. The worker should have raised it to the Hub as a blocked dependency (CLAUDE.md) instead of only listing it under Not done. Hub: register GAP-PROC-24 and make the shared texture pipeline a tracked dependency; the vehicles are not DEC-084-complete until maps (tread/sidewall normals, dust/grime) are applied. Note that much of MAJOR 1's "clay" read is geometry, so maps alone will not fix it.
2. **No lightmap UV (DEC-097 channel 1).** Same shared pipeline gap as PROC-007; static parked cars need it before baking. Track with minor 1.
3. **Arizona rear-plate rule cited "from memory".** Not a store value, but cite A.R.S. 28-2354 properly in `_sources` or label it.
4. **Shared `run_generator.py` changed** (preview camera moved outside the bounds). Harmless for orthographic renders and correctly reasoned, but it is a shared file outside the new generator; the packet has no `Owns` list, so the Hub should confirm it.

## Not checked
- Unity import (packet: not needed); the FBX copies have no `.meta` and no material builder binds `materials_pbr`.
- In-scene placement in the lot.
