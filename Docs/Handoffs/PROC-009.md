# PROC-009 handoff: studio-built parked vehicles

## Fix round 2 (REVIEW-PROC009 round 2, FAIL: 1 MAJOR, front end)
- **a. Undertray brick, removed.** The square undertray box and lip are gone. The bumper cover is now two sweeps along the same plan curve:
  - a painted upper band, which still sets the exact length;
  - a black lower intake/diffuser band (`bumper.lower_band_m`), recessed 8 mm inside the cover.

  The intake now sits inside the bumper silhouette and follows its curve and wraps; nothing hangs below the car.
- **b. Sedan fascia.** The headlamps had read as dots because the light lens sat on light paint with a chrome inner box behind it. Changes:
  - Headlamps now have a black housing behind the clear lens, with chrome projectors and a DRL strip.
  - Every lamp lens is swept along the body's plan outline round the fender corner (`lamps.head_wrap_m`/`tail_wrap_m`: sedan 0.16/0.12 m, hatch 0.14/0.10 m, SUV 0.10/0.08 m).
  - Sedan headlamp is 0.46 × 0.12 m.
  - Grille slats are chrome, 12 mm, at LOD0–1, so they read.
  - I also fixed a sign bug: lens paths sat 2 mm inside the end face; they are now 2 mm proud.
- **Sheet:** `Docs/Assets/Previews/PROC_parked_vehicles_contact_sheet.png` re-rendered and checked by eye at 2× crops. All three front 3/4 views show wrapped lamps, a visible grille and a black lower band inside the bumper, with no block underneath.
- **Validation:** 3/3 assets pass with 0 warnings; a rerun gives byte-identical FBX; `[SELFTEST] all passed`.

  | LOD | Sedan | Hatchback | SUV |
  |---|---|---|---|
  | LOD0 | 91,790 | 91,064 | 92,382 |
  | LOD1 | 29,394 | 29,024 | 30,144 |
  | LOD2 | 7,252 | 7,344 | 7,814 |
  | LOD3 | 1,438 | 1,456 | 1,592 |
- **Reviewer observation (late-1990s/2000s read), not addressed further:** wrapped lamps help; rounder plan corners and texture maps (blocked dependency) are the remaining levers.

## Fix round 1 (REVIEW-PROC009, FAIL: 2 MAJOR, 4 minor)
- **MAJOR 1 (visual read):**
  - **Raked ends:** a `rake` shear pulls each nose and tail back with height. The fascias now slope (hood edge about 10 cm back) and the SUV tailgate leans. Bumper fronts (shear 0) keep the exact length; the shear is monotone (`front_m`/`rear_m` < `zone_m`), so the mesh cannot fold.
  - **Own fascia per class** (params `lamps`, `grille`, `bumper.intake_m`):
    - sedan: slim wide lamps, slatted grille, wide tail lamps;
    - hatch: taller rounded lamps, mesh grille, deep intake, tall tail lamps;
    - SUV: blunt nose, big two-bar chrome grille, vertical tail lamps.
    All three get a DRL strip and an amber marker in the headlamp, and a lower intake/undertray with a lip. The undertray runs back under the body; a first try floated like a sled.
  - **Sedan A-pillar wedge:** the greenhouse side ahead of the front door glass is now a black sail panel, not paint.
  - **Hatchback:** shorter hood (cowl 1.22 m from the front, was 1.40). The roof breaks at 3.25–3.70 m into a sloped hatch glass that runs to the tail. It now reads as a compact hatch, not a long-hood wagon.
  - **SUV:** the greenhouse runs to the tail, so there is no deck ledge. The tailgate glass is recessed in a thicker paint frame and raked by the shear. Rocker raised to 0.34 m, taller nose.
  - **Mirrors:** tapered rounded housings lofted from the stalk to the cap, glass on the flat rear face.
  - **Paint surface:** a door feature line (3 mm ridge at 68 % of the side height) and rounder bumper covers.
  - **Not fixed: the "clay" read.** That needs texture maps (minor 1, blocked).
- **MAJOR 2 (contact sheet):**
  - New `Tools/Blender/generators/parked_vehicles_sheet.py` writes `Docs/Assets/Previews/PROC_parked_vehicles_contact_sheet.png` (2520 × 840, 527 KB), following the PROC-006c pattern.
  - One row per class; tiles: LOD0 front 3/4, rear 3/4 and side, then LOD1, LOD2, LOD3. Each tile is labelled with asset, LOD/view, tris and the true frame width.
  - The unlabelled runner sheet and the 3/4 review PNG in `Docs/Assets/Specs/` are removed; PROC_PIPELINE points to the new sheet.
- **minor 1 + 2 (texture maps, lightmap UV): blocked dependency, raised.** **FOR THE HUB:** the vehicles are not DEC-084-complete until the shared Q0.2/Q0.3 unwrap + texture pipeline (tread/sidewall normals, dust/grime masks) and the DEC-097 lightmap UV (PROC-007) exist. Please track both as dependencies of PROC-009. GAP-PROC-24 covers the maps.
- **minor 3:** looked up and cited. Under A.R.S. 28-2354(A)(1), a vehicle issued one plate shows it on the rear (azleg.gov/ars/28/02354.htm, read 2026-10-30). The cite is in params `_sources` and PROC_PIPELINE.
- **minor 4:** the 2-line `run_generator.py` camera change stays as is; the Hub to confirm (no `Owns` list in the packet).
- **Validation (this round):** 3/3 assets pass with 0 warnings; a rerun gives byte-identical FBX; `[SELFTEST] all passed`; sheet inspected by eye.

  | LOD | Sedan | Hatchback | SUV |
  |---|---|---|---|
  | LOD0 | 88,458 | 87,732 | 89,050 |
  | LOD1 | 29,054 | 28,732 | 29,852 |
  | LOD2 | 6,900 | 6,992 | 7,462 |
  | LOD3 | 1,382 | 1,400 | 1,536 |

## Original delivery (round 0; superseded where fix round 1 says so)

**Worker:** PROC worker session · **Branch:** `claude/jovial-meninsky-908c0a` (off `main` @ 3ab683b) · **Blender only, no Unity.**

## Done
- **Route: scripted rebuild (R3b.7 option 2), not CC0.** Poly Haven's model API has no vehicle category (checked `api.polyhaven.com/categories/models`). The other DEC-023 libraries offer no vehicle near DEC-084: Kenney and Quaternius are stylised, and Quaternius is DEFER/QAL anyway. So `LICENSE_LEDGER.md` gets no new row: no third-party source is used.
- `Tools/Blender/generators/parked_vehicles.py` + `Tools/Blender/params/parked_vehicles.json` produce 3 assets: `PROC_Vehicle_Sedan`, `PROC_Vehicle_Hatchback` and `PROC_Vehicle_SUV`. The classes stay generic (CCTV R1C1 SUV, R1C2 cars; RG3-4). They are unbranded: no badges, and the plate is blank (DEC-071).
- **R3b.7 items:**
  - Real panels: the body is a closed section loft with shoulder radius, tuck-under and a crowned deck. Shut lines are recessed V grooves at the doors, door bottoms, hood (front, cowl and both sides) and sedan trunk.
  - The greenhouse breaks from hood and trunk: a separate loft with tumblehome, roof-rail radius and a crowned roof.
  - Wheel arches: the side's bottom edge follows the arch circle, with an arch lip (black cladding on the SUV) and well liners.
  - Flush glazing: windows are faces of the greenhouse surface itself. The SUV and hatch tailgate glass is recessed 12 mm inside a paint frame.
  - Wheels sit inside the arches: lathed tyre with shoulder and tread grooves, rim barrel, 5/6/10 spokes, hub, lug nuts, disc and caliper.
- **Other detail:**
  - bumpers swept along the plan curve, with the wrap ends flush to the sides;
  - headlamps with reflector, projectors and amber marker; grille with surround and slats;
  - taillights with a reverse lamp; rear plate (12 × 6 in, rear only for Arizona) with surround;
  - mirrors with arm and glass; door handles (chrome on the sedan); wipers; roof rails on the SUV.
- **Quality bar and tris:**

  | LOD | Sedan | Hatchback | SUV |
  |---|---|---|---|
  | LOD0 | 86,134 | 83,876 | 86,422 |
  | LOD1 | 27,914 | 27,260 | 28,682 |
  | LOD2 | 6,644 | 6,694 | 7,164 |
  | LOD3 | 1,382 | 1,400 | 1,536 |

  LOD0 sits inside DEC-084's 30–150k hero guide; the LOD steps are about ⅓, ¼ and 1/60. LOD3 is the hull, tyre plus disc rim, and boxes.
- **Collision (R3b.0.5):** manifest boxes for the body, cabin and 4 wheels.
- **PBR:** the manifest gets `materials_pbr` (metallic/smoothness/alpha for 16 slots) and `paint_variants` (6 neutral colours for material swaps); wear params come from the seed.
- **Contact sheet:** `Docs/Assets/Specs/PROC_parked_vehicles_contact_sheet.png`. Also a 3/4 workbench review sheet, `PROC_parked_vehicles_review_3q.png` (front-3/4 and rear-3/4 per class).
- **PROC_PIPELINE:** new section "Parked vehicles (PROC-009)" with the run commands and GAP-PROC-23/24.
- **Shared runner fix, outside the new files** (`run_generator.py`, 2 lines): the preview camera stood at a fixed y = −2 m / x = +2 m. That is inside a 4.9 m car, so the "front" render showed the car from inside. It now sits 2 m outside the bounds. The camera is orthographic, so renders of existing assets do not change; they were not regenerated.

## Validation
- `blender.ps1 parked_vehicles …`: 3/3 pass the canonical checks (exact size, origin bottom-centre, UV maps, material slots, no degenerate faces, LOD chain), with **0 warnings**.
- Determinism: a second run gave byte-identical FBX (sha256 diff empty).
- `Tools/Blender/tests/test_validation.py` passes.
- `contact_sheet parked_vehicles` is 141 KB (< 1 MB). Renders were checked by eye.

## Not done
- **Texture maps (Q0.2/Q0.3):** these need a proper unwrap or trim sheet, plus maps baked or sourced from the cache. That is the shared pipeline item PROC-005 left open: proclib still box-projects `UVMap_Main`, and nothing in the repo bakes textures yet. Until then the vehicles have PBR *values* only. The tread blocks and sidewall wait for a normal map. GAP-PROC-24.
- **Lightmap UV (R3b.0.4 / PROC-007):** not in proclib on main. Static parked cars will need it before baking.
- **Unity:** not opened. The FBX are copied to `UnityProject/Assets/_Game/Art/Procedural/Exterior/Vehicles/` without `.meta` files, and no material builder binds `materials_pbr`.
- **Look:** the front fascia is a near-vertical face with lamps and grille on it, so it reads more 2000s than current. The next pass would rake the nose and wrap the lamps. Interior: none; the dark glass hides that.

## For the Hub
- **GAP-PROC-23 (register):** vehicle class dimensions and proportions are generic (midsize sedan 4.88 × 1.84 × 1.44 m, compact hatch 4.37 × 1.80 × 1.45 m, compact SUV 4.60 × 1.86 × 1.70 m). They are not measured. Searched: RI/CCTV (classes only, RG3-4), OFFICE_FINDINGS B20 (15 spaces, 1 accessible; no vehicles), KNOWN_GAPS GAP-134.
- **GAP-PROC-24 (register):** parked-car paint mix (CCTV cannot resolve colour) and the vehicle texture maps.
- "Rear plate only" uses the Arizona rule (A.R.S. 28-2354, Med from memory, not looked up here); the plate is blank.
- **Proposed DEC:** a vehicle family or class is added as a `classes` entry in `parked_vehicles.json`, not as a new generator (pickup and van are likely next if the lot needs them).

## Questions for Nolan (through the Hub)
None. The class mix and colours are unresolvable from CCTV and were already ruled generic (RG3-4).
