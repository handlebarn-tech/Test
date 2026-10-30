# ACQUISITION LIST — ASSET-001

Prepared 2026-10-29. Every row's license is in `LICENSE_LEDGER.md` (IDs match). **Nothing downloaded yet** (ASSET-001 snapshot, 2026-10-29; downloads since are in `ASSET_CACHE_MANIFEST.json`, licenses in `LICENSE_LEDGER.md`; AUDIT-001 E4). Ordered: P0 slice + M5 hero retail → P1 M6 stock/BOH → P2 later. Fetch rule: one asset → record SHA-256 → ledger "Downloaded" → Blender normalize (plan §73). Raws go in gitignored `ThirdParty/`, never committed (ledger "Repo policy").
Sizes: Poly Haven = 2k glTF+textures from API; Sketchfab = tris (MB unknown until download).

## Human-only steps (agent must not do these)
1. Unity Asset Store: sign in, accept EULA, add **Unity Warehouse** (936.8 MB) and **UnityJapanOffice** (3.3 GB) to My Assets. Needs Nolan.
2. Sketchfab: free account login needed to download any model (agent cannot create accounts).
3. Sonniss GDC bundle: email/registration download (7.47 GB+) — optional, only after P0 audio gaps are confirmed.
4. Test-import Warehouse (built for 2022.3, HDRP) into Unity 6000.6 before relying on it.

## P0 — slice + M5 (hero retail)
| # | Ledger ID | Asset | Why | Notes |
|---|---|---|---|---|
| 1 | LIB-PH materials: PH-marble_01 / marble_tiles / marble_mosaic_tiles | Retail floor | Light marble-pattern floor (plan §2 row 2) | Pick 1 after look-dev; ~4–14 MB each |
| 2 | PH-fine_grained_wood, PH-oak_veneer_05 | Wood cabinets/counters | | |
| 3 | PH-concrete_floor_01 (+ smooth_concrete_floor) | BOH/shell floor | | |
| 4 | PH-CashRegister_01 | Register POS hero | CC0, 2.4 MB, no attribution; beats Sketchfab register rows | |
| 5 | SK-344514 Cashier Machine (untextured), SK-dd3b0f POS Terminal | Register hardware | Donor for monitor/terminal; retopo dd3b0f | CC BY credit |
| 6 | SK-a73f64 Digital Scale | Deli scale | 5.8k tris | CC BY |
| 7 | SK-da8bc0 Free Jar Pack + SK-bfeabe Weed Bud | Deli jar wall | Jar usable; bud needs retopo (250k) → custom Blender | CC BY; plaggy CC0 jar is **unverified** |
| 8 | SK-a4216f ATM | Entry ATM | Strip bank logos | CC BY |
| 9 | SK-938a9b Display cabinet (+ custom glass case, plan §19) | Merch wall | | |
| 10 | PH-security_camera_01/02, SK-ab8d2a dome, SK-2273be CCTV monitor | Security | CCTV composite feeds | |
| 11 | SK-79370d exit sign, SK-4324a9 emergency light, SK-7fbd47 or PH-korean_fire_extinguisher_01, SK-976c3f pull station, SK-caa8b3 smoke detector | Life safety (east exit, hall) | | |
| 12 | PH-potted_plant_04, PH-fern_02, SK-e9832f pothos, SK-8013c4 bush+ivy | Living wall / plants | Avoid 96k-tri PH plants unless LOD'd | |
| 13 | FNT-BAR Barlow, FNT-INT Inter | Signage / POS UI | OFL; bundle OFL.txt | |
| 14 | PH HDRIs: kloofendal_overcast_puresky (day), courtyard_night (night) | Exterior lighting | 2k HDR | |
| 15 | Audio: LIB-KEN-IF (Interface Sounds), LIB-KEN-DA, AUD-BSB door bell | POS beeps, scan, entry chime | CC0; audition door bell, may need a synthesized 2-note chime | |
| 16 | PH exterior: exterior_aircon_unit, modular_chainlink_fence, utility_box_01/02, security_light, asphalt_01 | Exterior shell dressing | | |

## P1 — M6 stock / BOH
| # | Ledger ID | Asset | Notes |
|---|---|---|---|
| 17 | PH-plastic_crate_02 (+01/03, plastic_container) | Totes (blue, yellow lids via material) | 4–9 MB each |
| 18 | SK-b9f45d Cardboard Boxes Pack, PH-cardboard_box_01 | Case stacks | CC BY / CC0 |
| 19 | SK-ef69cb Metal Wire Shelf, SK-fb263b rack, PH-worn_metal_rack | Chrome wire racks | |
| 20 | PH-hand_truck, PH-industrial_storage_cart | Carts | |
| 21 | PH-mounted_fluorescent_lights, PH-caged_hanging_light | BOH lighting | |
| 22 | LIB-UWH Unity Warehouse (selected prefabs only) | HUB pallets/cargo/racking | 936.8 MB, HDRP, version risk; SK-17cf3c racking is the fallback |
| 23 | Office: PH-metal_office_desk, PH-modern_arm_chair_01, SK-d492f8 desk, SK-c144d8 server rack, SK-6fc5ea safe, SK-c9f6e2 access reader, paper/folder/clipboard (SK-e8b337, 113901, 865023, PH-office_notepads) | Office + IT | |
| 24 | Break room: SK-9ccda2 coffee maker, SK-0b01a3 appliances, PH-wall_clock, PH-vintage_microwave (retro look; verify), PH-metal_trash_can | | |
| 25 | Restroom/janitor: SK-ef9e5c supplies, SK-e6f440 toilet, SK-0c5dce mop+bucket, PH-WetFloorSign_01, PH-multi_cleaner_bottle, PH-bleach_bottle | | |
| 26 | LIB-UJO UnityJapanOffice (extract prefabs only) | Optional; 3.3 GB | Skip if PH/Sketchfab suffice |
| 27 | Audio ambience from LIB-BSB (per-sound CC0 check) / Sonniss | HVAC hum, room tone | |

## P2 — later
Characters/animation (MakeHuman, KinemIQ CC0 subset, Kevin Iglesias), vehicles (SK-20f9af, aeb269, edc994), street pack (SK-f3eb47), Quaternius.

## Rejected (do not fetch) — details in ledger
Removed listing: Niclas basemesh (404). CC BY-SA: BlueOxel A/C. "Free Standard": hdyeah register. Too heavy: Rosenthal bud 3.3M, Weed Jar 1.1M, Ivy 767k, barcode scanner 508k, Display Case 216k, Garage Shelf 150k, ghostnoface grinder 86k. Unverified: plaggy Fab jar, CMU mocap.

## Gaps (not available free & verified → custom model in Blender, plan §19/§41)
Deli flower jar wall final look, store glass case, queue stanchions, register counter, menu screen, product packaging, barcode scanner, shipping totes with exact markings.
