# REFERENCES INDEX (REF-001)

Canonical finder for every supplied reference. Originals under `References/` are immutable; derived files live in `References/Index/`.
Confidence: **High** = printed/vector value, **Med** = read from a vector drawing or clear image, **Low** = inference or convention.
Staff are described by attire/role only.

## 0. File inventory

> **Moved images (AUDIT-001 E10, DEC-064):** DEC-041..043 cite the `References/Incoming/` names. The files now are: `CCTV BOH desk + racks 2026-10-29.webp` → `References/CCTV BOH Desk Racks 2026-10-29.webp` (and the FOH still → `CCTV FOH Desk Racks 2026-10-29.webp`); `Photo deli jars + scale (office) 2026-10-29.webp` → `References/Photo Deli Jars Scale Office 2026-10-29.webp`; `Photo deli jar wall (retail) 2026-10-29.jpg` → `References/Photo Deli Jar Wall Retail 2026-10-29.jpg`.

| File | Type | What it is | Index section |
|---|---|---|---|
| `References/Floor Plan.pdf` | PDF, 6 pp (pp5–6 blank), Print-to-PDF, no text layer, vector shapes | "The Flower Shop Phoenix · Floor Plan", **Working Plan V5, not for construction**. Built from the RSP Architects A011 (floor plan) / A012 (lighting plan) sheets, 2026 AZDHS update (read as text only; "A013" was a mislabel, fixed REF-004), cameras and a walkthrough | §1 |
| `References/CCTV Camera Wall.png` | PNG 2048×1137, 5×5 tiles | Camera wall snapshot A (busy floor, overlay timestamps read 2012 = NVR clock, not a real date) | §2 |
| `References/CCTV Camera Wall 2.png` | PNG 2696×1462, 5×5 tiles | Camera wall snapshot B, same tile layout, higher resolution (use this one first) | §2 |
| `References/BAND_TFS Phoenix (NEW)_…/…_01..13.jpeg` | 13 JPEG 1280×960, body-cam style, EXIF 2026-03-16..20 | Eye-level store/staff snapshots | §3 |
| `References/CCTV HUB Wall 2026-10-29.webp` | WEBP 2000×564, 2×4 tiles | HUB/HUB 2 camera wall supplied by Nolan 2026-10-29 (DEC-022). Nolan: "First room on left two pictures, the rest are in the bigger side of the hub... It's mostly misc storage." | §2.1 |
| `References/CCTV Register Back Center East 2026-10-29.webp` | WEBP 1866×755, NVR playback, 2 feeds | "Back Of Register center" (close) + "Back Of Register East", 11:40:16, 1/21/2026. Supplied by Nolan for the scale stand (DEC-026) | §2.2 |
| `References/CCTV Register Back Center Wide 2026-10-29.webp` | WEBP 1134×640, 1 feed | "Back Of Register center", 16:48:53, wide. **Same camera and framing as wall tile R2C4** (DEC-026) | §2.2 |
| `References/CCTV BOH Desk Racks 2026-10-29.webp` | WEBP 2000×1022, 1 feed, no overlay text | BOH overhead still: chrome wire rack island of packaged stock, wall rack of black cases, the ex-register-1 computer on the right (DEC-041). Supplied by Nolan 2026-10-29 | §2.3 |
| `References/CCTV FOH Desk Racks 2026-10-29.webp` | WEBP 2000×1101, 1 feed, no overlay text | FOH overhead still: computer on a black wire rack against the back wall, fridge, glass-door cooler, chrome racks, patterned-tile doorway (DEC-041). Supplied by Nolan 2026-10-29 | §2.3 |
| `References/Photo Deli Jars Scale Office 2026-10-29.webp` | WEBP 952×1269, phone photo, office | Deli canisters (empty and in use, THC % label cards), deli scale with glass bowl, stainless "FOR DELI USE ONLY" prep cart (DEC-042b). **Raw photo: never ships** (network rack, thermostat, security-labelled drawer in frame) | §2.4 |
| `References/Index/photos/deli_jars_scale_cart_crop.webp` | WEBP 570×779, derived crop (330,490)–(900,1269) | Jars + scale + cart only. No network rack, thermostat, security drawer or screen content | §2.4 |
| `References/Photo Deli Jar Wall Retail 2026-10-29.jpg` | JPEG 640×481, phone photo, retail | Retail deli jar wall: uniform canisters with brand card, THC % tag and brand base band, dark-grey metal shelves, teal leaf-pattern wall, black counter with walnut drawers, branded bags (DEC-043). **A shopper is partly visible at the right edge (x ≥ ≈605); the raw photo never ships** | §2.4 |
| `References/Index/photos/deli_jar_wall_retail_crop.jpg` | JPEG 590×481, derived crop (0,0)–(590,481) | People-free crop of the jar wall (the shopper is cut off) | §2.4 |
| `References/TI/Interior TI Approved Set - PHX.pdf` | PDF 37 pp (24"×36"-class sheets, vector + text layer), 9.15 MB, 2022-08/10, City-approved 2022-12 | Retail interior TI drawings: G010 mounting heights, A101 plan + RCP, A310 door/material schedules, A320 partitions, A901 elevations, A940 millwork, I101 finish plan, E-sheets luminaire schedule. Text-read in REF-004; Nolan supplied the file and it was imported in REF-005 (plain git, <10 MB). Every page was checked: no security plan, P&P or credential page (the security mentions are a grille, card-reader hardware lines and spec boilerplate) | §6 |
| `References/TI/A011 Phoenix AZDHS Floor Plan - 2026 Update.pdf`, `References/TI/A012 AZDHS Floor Plan - Lighting - 5.20.26.pdf` | PDF 1 p each, vector, 1/4"=1'-0" (18 pt/ft), sheet date 05/15/23, revs 12/23/22 | Room areas and labels behind Working Plan V5; A012 lighting legend | §6.8 |
| (chat only) 3 CCTV pairs Nolan pasted into the REF-008 session, 2026-10-29 | images in chat, not files | Office (2 views, one new), BOH (= R4C2 + BOH still), FOH (2 views, one new) | §7 |
| `References/LIVE_TFS_BUDTENDER_v7.11.4.md` | MD | Live budtender app behaviour (v7.11.4: Floor Mode, 6 effect domains, tier filters, accessibility). **No visual tokens** (colours/fonts/layout) are recorded in it | UI only (GAP-114) |
| `References/Review_Budtender_Tool_Comprehensive_Chat_Record.md` | MD | Project history of the budtender tool (not in the REF-001 input list; not analysed here, MIG owns it) | — |

Derived files (`References/Index/`):
- `floor_plan_p1..p4_200dpi.png` — page renders.
- `floor_plan_stitched_300dpi.png` — plan drawing stitched across the p1/p2 page break (the pages join exactly: p1 clip ends 584.28 pt, p2 starts 28.44 pt, so offset is 555.84 pt).
- `floor_plan_grid_1ft.png` — stitched plan with a 1-ft grid (bold every 5 ft) in the §1.2 coordinate frame. **ART-001: start here.**
- `cctv/wall1_RrCc.jpg`, `cctv/wall2_RrCc.jpg` — 50 tile crops (row r, column c).
- `hub/hub_RrCc.jpg` — 8 tile crops of the HUB wall (REF-002), 500×282 each.
- `register/` (REF-003, people cropped out): `east_stand.jpg` (East feed: stand + counter back + keyboard), `center_close_stand.jpg` (centre feed: stand with 2 scales + acrylic panel), `wide_stand_A.jpg` / `wide_stand_B.jpg` (wide feed, two stands), `wide_storefront_band.jpg` (video wall, living wall, jar walls above head height).

## 1. Floor plan

### 1.1 Scale basis
- Printed dims: overall width **47'-2¼"**; retail depth **29'-0"**; small-room band **16'-10"**; rear depth **29'-0"**; HUB width **28'-3¼"**; HUB 2 width **18'-9¼"**; overall depth **≈76'-0½"**. High.
- Vector scale: the retail outer rectangle is 264.7 pt wide = 47.1875 ft, so **5.6095 pt/ft**. Checks: retail depth 29.0 ft, band 16.8 ft, HUB 28.29 ft, HUB 2 18.49 ft, overall 76.03 ft. All match the printed dims to within 0.25 ft except HUB 2 (18.49 vs printed 18'-9¼" = 18.77; the printed 541.34 SF ÷ 29.24 ft = 18.51 supports the vector width). **High.**
- Every fixture coordinate below comes from the vector geometry, except the HUB/HUB 2 racks and desks, which exist only in raster form and were read off the 1-ft grid (±0.25 ft).
- The legend says rooms are "sized from architect sheet" but fixtures/doors are "placed from cameras and your notes (approximate)". So room shells are High and fixture positions are **Med at best**. The schematic door arcs are not real door widths (see §5).

### 1.2 Coordinate frame (feet)
Origin is the NW outer corner of Retail. **+x = east, +y = south** (plan is north-up "from camera labels"). Rooms are drawn as filled rects with about 0.4–0.5 ft gaps that stand in for walls. Wall thickness is not specified (GAP-104).

### 1.3 Rooms (names as printed)

| Room (plan label) | Printed SF | x0–x1 | y0–y1 | W × D (ft) | Notes |
|---|---:|---|---|---|---|
| RETAIL (Retail / sales floor) | 1,373.31 | 0–47.19 | 0–29.0 | 47.19 × 29.0 | 47.19×29 = 1,368.5, which matches the printed SF |
| RESTROOM (unisex) | 53.16 | 0–8.0 | 29.5–36.1 | 8.0 × 6.6 | |
| HALL | 35.16 | 8.39–13.70 | 29.5–36.1 | 5.31 × 6.6 | entered via west arch |
| OFFICE | 131.82 | 0–13.70 | 36.5–46.3 | 13.70 × 9.80 | sheet says 13'-8¾" |
| BREAK ROOM | 151.56 | 14.10–23.31 | 29.5–46.3 | 9.20 × 16.80 | contains JC |
| JC (janitor closet, inside break room) | 19.19 | 19.9–22.9 | 42.9–45.9 | 3.0 × 3.0 (drawn) | drawn size and corner both unconfirmed. 3×3 = 9 SF, not 19.19 (GAP-103) |
| FOH (floor restock; A011 "FULFILLMENT") | 180.26 | 23.69–36.49 | 29.5–46.3 | 12.80 × 16.80 | 215 SF drawn. A011 (REF-006) puts FULFILLMENT 180.26 SF in the west room (next to Break), so FOH = 180.26 |
| BOH (backstock; A011 "PRODUCT STORAGE") | 163.44 | 36.90–47.19 | 29.5–46.3 | 10.29 × 16.80 | 173 SF drawn |
| HUB (sheet: Product Storage) | 818.53 | V5: 0–28.29 · **A011: ≈19.2–47.19 (east)** | 46.8–76.03 | 28.29 × 29.24 | general storage, desks; **A011 (REF-007): the east room, reached through the connecting door; the SE emergency exit opens from it.** V5 mirrors the pair |
| HUB 2 (sheet: Product Storage) | 541.34 | V5: 28.70–47.19 · **A011: 0–≈18.8 (west)** | 46.8–76.03 | 18.49 (A011 18'-9¼") × 29.24 | **A011: the west room, entered from the office and the west delivery door ("first room", DEC-022).** No access from FOH/BOH |
| *Arch vestibule (unnamed, "white wall")* | — | 35.2–38.2 | 29.5–31.7 | 3.0 × 2.2 | small lobby behind the east arch, with doors to FOH and BOH. A011 labels it **HALL 35.16 SF** (REF-006); V5 puts that label on the west hall by the restroom |
| Net / gross | 3,467.77 / 3,590 (assessor) | | | | the plan says walls ≈ 122 SF |

### 1.4 Doors / openings (from the vector plan)

| Opening | Location (ft) | Drawn width | Conf. |
|---|---|---|---|
| ENTRY (customer, double door) | west wall x=0, y 11.0–20.0 (position) | drawn 9.0 opening; **use 6'-0" × 7'-0" storefront pair** (TI E101 = A011 vector 6.0 ft, DEC-037, Hub ruling) | High (size) / Med (position) |
| EXIT label (orange = position not confirmed) | west wall, just north of entry | — | Low |
| EMERGENCY EXIT | east wall x=47.19, y 20.5–24.0 | 3.5 (swing drawn orange = unconfirmed) | Low |
| West arch (Retail→Hall) | y≈29.25, x 9.10–12.91 | 3.81 | Med |
| East arch (Retail→vestibule) | y≈29.25, x 35.21–38.21 | 3.0 | Med |
| Hall→Restroom door | x≈8.2, y 31.5–33.3 | 1.8 symbol | Low (schematic) |
| Hall→Break room door | x≈13.7, y 31.5–33.3 | 1.8 symbol | Low |
| Hall→Office door | y≈36.1, x 9.5–11.3 | 1.8 symbol | Low |
| Vestibule→FOH door | arc at x 34.0–35.2, y 30.6 | 1.2 symbol | Low |
| Vestibule→BOH door | arc at x 38.2–39.4, y 30.6 | 1.2 symbol | Low |
| Office→HUB door | V5: y≈46.3, x 4.0–5.8 · **A011 (REVIEW-W4C): at the east end of the office south wall, x≈7.5–10.5, opening into HUB 2 (west room)** | 1.8 symbol; A011 ≈3'-0" | Low (V5) / Med (A011, scaled by eye) |
| EXT. DELIVERY (employees only) | west wall x=0, y 47.8–51.2 (A011 ≈49.5–52.8, scaled by eye, REVIEW-W4C); opens into HUB 2 per A011 | 3.4 | Med |
| Door to HUB 2 | V5: wall x≈28.3–28.7, y 48.6–50.6 · **A011: in the partition's north end (partition x≈18.8–19.2), y≈46.8–49.8, swings into HUB** | 2.0 drawn; A011 ≈3'-0" | Med (V5) / High (A011 location) |
| EMERGENCY EXIT, SE (green door with round logo; DEC-030) | **A011 (REF-007): "access controlled entrance / exit" at the SE corner of the east room (HUB, 818.53 SF), on the south wall at x≈44.4–47.2, y=76.03, swinging out.** HUB is the furthest-east room, so the door opens from **HUB** (DEC-042c: HUB 2 is not furthest east). This agrees with HUB-wall tile R1C4 (HUB) showing the door | ≈3'-0" (A011 vector) | High (room, wall) / Med (exact x) |

### 1.5 Fixtures, counters, registers (vector, ft; Med unless noted)

| Fixture (plan label) | x0–x1 | y0–y1 | Size |
|---|---|---|---|
| living wall (north) | 1.8–11.0 | 0.2–1.4 | 9.2 × 1.2 |
| menu screen (north) | 11.6–18.2 | 0.2–1.2 | 6.6 × 1.0 |
| deli flower jar wall (north) | 19.0–45.0 | 0.2–1.4 | 26.0 × 1.2 |
| jar wall (east) | 45.6–47.0 | 0.2–14.2 | 1.4 × 14.0 |
| "N.E Corner" cam | ≈46.6, 0.5 | — | camera dot |
| licenses (west wall) | 0.2–1.0 | 3.0–8.0 | 0.8 × 5.0 |
| merch (rack, rounded) | 4.0–8.6 | 2.6–4.0 | 4.6 × 1.4 |
| REGISTERS (up to 12) — L counter | 20.0–42.0 | 7.0–19.0 (bbox) | L: north run along y≈7–8.x, return leg down the east side to y=19. **REF-011:** holds registers 10/9/8 (north) and 12/11 (east) only; the east return sits too close to the east jar wall (§8.1, GAP-130) |
| display case (on register counter) | 38.0–39.4 | 7.4–8.8 | 1.4 × 1.4 |
| globe pendants over register run | 6 circles, centres x 23.0, 26.0, 29.0, 32.0, 35.0, 38.0; y 11.0 | Ø0.8 | 3.0 ft pitch |
| DELI COUNTER — L counter | 14.0–34.2 | 18.0–25.2 (bbox) | L. **REF-011: this is the south register run (registers 7,2,3,4,5,6, staff on its south side), not a separate deli counter**; drawn ≈2.6 ft too far south (§8.1, GAP-129) |
| globe pendants, deli west end | centres (15.0, 26.2), (17.0, 26.2) | Ø0.8 | |
| two white columns | x≈19.0 and x≈35.0 | y 19.6–20.4 | ≈0.8 sq |
| queue stanchion lines (dashed, raster-read) | x ≈ 6, 9, 12, 15 | y ≈ 11–19.5 | 4 lanes, Low-Med |
| ATM | 1.2–3.4 | 25.8–27.6 | 2.2 × 1.8 |
| deli flower jar wall (south, between arches) | 13.5–34.7 | 27.6–28.8 | 21.2 × 1.2. **REF-011:** it has a back counter under the shelves (BAND 10); real depth runs to the wall, ≈2.1 ft (§8.3) |
| rack (east wall) | 45.6–47.0 | 15.0–20.0 | 1.4 × 5.0 |
| sink (hand wash, east wall) | 45.6–47.0 | 24.6–26.8 | 1.4 × 2.2 |
| Office: IT rack | 0.6–2.0 | 38.0–42.0 | 1.4 × 4.0 |
| Office: safe | 11.0–13.2 | 37.2–40.2 | 2.2 × 3.0 |
| Office: desk (L) | 9.0–13.2 | 41.0–45.6 (bbox) | L |
| Break: kitchen + sink (L) | 14.7–22.7 | 30.1–33.8 (bbox) | L |
| Break: bench | 14.7–15.7 | 38.5–45.5 | 1.0 × 7.0 |
| FOH: wire racks ×2 | 25.0–33.0 | 32.2–33.6 and 34.4–35.8 | 8.0 × 1.4 each |
| FOH: fridge | 24.3–25.9 | 42.0–45.6 | 1.6 × 3.6 |
| BOH: cases · racks ×2 | 37.6–39.0 and 45.0–46.6 | 33.0–45.6 | 1.4–1.6 × 12.6 |
| HUB: unlabelled storage strip (raster) | ≈1.5–3.0 | ≈56–73 | Low-Med |
| HUB: desks + computers (raster) | ≈15–27 | ≈70–74.4 | Low-Med |
| HUB 2: unlabelled storage strip (raster) | ≈30.5–31.8 | ≈52–73 | Low-Med |

## 2. CCTV camera wall (both snapshots, identical 5×5 layout)

The plan text says the wall carries **17 distinct feeds: 6 exterior, 6 sales floor, 5 BOH**. The 25 tiles break down as those 17, plus 2 apparent repeats, plus 6 storage-room feeds that the plan does not account for (GAP-105); REF-002 maps them to HUB / HUB 2 from Nolan's HUB wall (§2.1).

| Tile | Zone / view | Key fixtures & finishes | Mapped plan room | Conf. |
|---|---|---|---|---|
| R1C1 | Exterior sidewalk along a light building wall, night IR | concrete walk, curb, asphalt, parked SUV | Exterior (side unknown) | Med |
| R1C2 | Exterior rear/side lot | light flat-roof commercial wall, parked cars, striping | Exterior | Med |
| R1C3 | Exterior lot by long wall | dark green privacy fence/gate, yellow curb, wall packs | Exterior (likely delivery/rear) | Low |
| R1C4 | Exterior drive aisle | orange cone, hedge, yellow crosshatch, headlights | Exterior | Med |
| R1C5 | Exterior front/side parking | sidewalk approach, building edge, street | Exterior | Med |
| R2C1 | Sales floor, from register end looking toward entry | glass entry doors + exit sign, queue stanchions (black belts), video-wall TV, living wall, "DELI STYLE" counter, POS monitors, card readers, scales on rolling carts; white marble-look tile + black/white geometric cement tile near counter | Retail (west half) | High |
| R2C2 | Sales floor, high SW-ish view over queue | wall planters + wood bench, 3×3 video wall, "THE FLOWER SHOP" logo living wall, stanchion field, DELI STYLE counter with checker tile front, jar walls, globe pendant cluster | Retail | High |
| R2C3 | Register run close (**REF-011: camera behind the south run, looking north** at the north run) | 3–4 POS stations, black counter with open shelves below, scale carts, jar wall with mint/teal backlit shelving on the side wall, yellow wet-floor sign, "HIGH TIDE" stool/seat back | Retail (registers) | High |
| R2C4 | Register run, wider (camera name "Back Of Register center", REF-003; **REF-011: behind the south run, looking north**) | 3 POS + spare monitor, kraft order bags, globe pendant clusters, DELI STYLE counter behind | Retail (registers) | High |
| R2C5 | Elevated view along register L toward deli/queue (**REF-011: from the SE behind the south run's east end, looking NW**; not the plan's "N.E Corner" cam) | register L end with trash bin, black cabinet end, jar wall on right, entry/queue far left | Retail (NE register L) | Med |
| R3C1 | Exterior sidewalk + hedge against building | narrow walk, hedge, wood fascia | Exterior | Med |
| R3C2 | Register counter from behind, looking across the floor to the back wall | **lit black glass display cabinet on the counter** (matches plan "display case"), 2 POS, scales, arched niche through a vertical wood-slat wall, jar wall, ATM + queue at the far end, merch rack with white garments on the right | Retail | High |
| R3C3 | Office | L desk with 2 monitors, stainless worktable, paper trays, money counter, black file cabinet, trash/recycling cans, wall shelves, posted procedures, green neon glow, black door with cannabis-leaf print, utility cart, plant | Office | High |
| R3C4 | Hall | black "EMPLOYEES ONLY" door with fire-door label, corkboard + taped notices, second black door (open) into the office, black/white geometric tile, arch jamb at left | Hall | High |
| R3C5 | Break room | L wood cabinets + black counter, sink, microwave, coffee maker, labor-law poster, wood/metal bench, coats/bags on hooks, fridge side covered in magnets, mini hoop, floor mats, black door with taped note | Break room | High |
| R4C1 | FOH | chrome wire racks with clear sorted bins, yellow tote on top, white fridge, **two glass-door coolers**, concrete floor with red floor tape, doorway to the tiled vestibule | FOH | High |
| R4C2 | BOH | narrow aisle, stacked "Dr Greenthumbs" black cases, kraft order bags, wire racks of cased product, doorway to the tiled vestibule | BOH | High |
| R4C3 | Large storage room | rows of chrome wire racks, some posts painted orange, cased product, dark floor, black double door at the far wall | **HUB** (= HUB wall R1C2, §2.1) | Med |
| R4C4 | Large storage room | grid of chrome wire racks, pallet of blue cases, yellow tote, dark large-format floor tile, wood-panel wall band with lit strip | **HUB** (= HUB wall R1C3) | Med |
| R4C5 | Office (apparent repeat of R3C3, mean pixel diff 12–16) | same as R3C3 | Office | Med |
| R5C1 | Storage, near a door | shrink-wrapped pallets of blue cases, stacked yellow-lid black totes, large copier/printer, black cabinets, wire merch rack, dark gray tile | **HUB 2** (= HUB wall R1C1) | Med |
| R5C2 | Storage/work area | work table with patterned front, cardboard cases, blue totes, wire carts, copier, black cabinets, white door | **HUB 2** (= HUB wall R2C1) | Med |
| R5C3 | Large storage room | chrome wire racks, stacked yellow tote lids, hand truck, black crates, black cabinet | **HUB** (= HUB wall R2C2) | Med |
| R5C4 | Large storage room | wire racks, 2 pallets of blue cases, black totes, wainscot band with wall signs | **HUB** (= HUB wall R2C3) | Med |
| R5C5 | Apparent repeat of R5C2 (diff 12–19) | same as R5C2 | **HUB 2** (= HUB wall R2C4) | Med |

### 2.1 HUB camera wall (REF-002, `References/CCTV HUB Wall 2026-10-29.webp`)

Tile matching: each tile was compared with the 25 main-wall tiles (128×72 grayscale, mean abs diff). Seven tiles are the same cameras as the main wall's unmapped storage tiles (diff 9–27 vs ≥35 for any other tile); **R1C4 is new** (best diff 46).

**Room decision.** Nolan: "First room on left two pictures, the rest are in the bigger side of the hub."
- "Left two pictures" = the **left column** (R1C1 + R2C1), not the first two of the top row. R1C1/R2C1 show one cluttered room (copier, yellow-lid totes, work table, gray square floor tile); R1C2 shows the same orange-post chrome racks and dark floor as R1C3/R2C2/R2C3, so it belongs with "the rest". R2C4 repeats R2C1, so the left-column room has exactly two distinct views.
- "The bigger side" = **HUB** (818.53 SF vs HUB 2 541.34 SF, printed, High). R1C4's desk + office chair + keyboard matches the plan's HUB "desks + computers" strip (x≈15–27, y≈70–74.4).
- **REF-007 (A011, High):** the office and the west delivery door open into the small west room (541.34 SF = HUB 2), and the bigger east room (818.53 SF = HUB) lies beyond the connecting door. That is the literal "first room", so the naming below holds. Only the V5 geometry is mirrored (§1.3).
- So left column = **HUB 2**, the rest = **HUB**. Conf. **Med** (owner statement + plan areas). "First room" is read as the order Nolan listed them, since the plan says HUB 2 is reached only through HUB. This supersedes the DEC-018 / REF-001 guess (R5C1/R5C2/R5C5 → HUB), which had the rooms swapped.

| HUB-wall tile | = main wall | Room | View / camera pose guess (pose Low) | Key fixtures & finishes | Conf. (room) |
|---|---|---|---|---|---|
| R1C1 | R5C1 | HUB 2 | high corner looking along the room to a doorway at the far left (shelving with black bags beyond: likely the connecting door to HUB) | copier/printer (left foreground), stack of 4 yellow-lid black totes, 3 shrink-wrapped pallets of blue cases, chrome wire merch rack with kraft bags + a green branded panel, gray square floor tile, white walls | Med |
| R1C2 | R4C3 | HUB | down the aisle between two long rack banks toward a white end wall | chrome wire racks, some posts painted orange, orange product cases on the foreground racks, small black bin cart at the aisle end, black door + yellow sign on the far wall, dark floor | Med |
| R1C3 | R4C4 | HUB | high corner looking across the central rack island | island ≈4 bays wide × 3 deep of chrome wire racks (mostly empty), perimeter racks on the left and back, pallet of blue cases + small bins on the right, yellow sign on a rack, dark wood-panel wall band with a lit strip on the back wall, dark large-format floor | Med |
| R1C4 | — (new) | HUB | from above the desk corner, looking across the room past the rack island | light wood desk with keyboard + black office chair (foreground right), long dark counter/bench along the left wall, green door with round logo (far left), blue and red rolling carts, rack island with cased product, pallet of blue cases (right), white walls, dark floor | Med |
| R2C1 | R5C2 | HUB 2 | high corner over the clutter, looking toward the back wall | work table with patterned (geometric) front panel, cardboard cases, blue stackable bins, wire shelving with boxes, stacked black/yellow totes, black cabinets (back right), white door (back right), brown wire display panels (right), yellow tote (foreground) | Med |
| R2C2 | R5C3 | HUB | high corner looking across the rack island | rack island + perimeter racks on the left and back walls, white cases on the racks, black plastic crates (left foreground), black bins/cart (left), stack of yellow totes + hand truck (right) | Med |
| R2C3 | R5C4 | HUB | high corner looking along a wall with racks behind | wire racks, 2 pallets of blue cases, black totes/crates, dark-brown wainscot band with small wall signs (left wall), rack on the left edge | Med |
| R2C4 | R5C5 | HUB 2 | **repeat of R2C1** (diff 26.8; slight crop/time change) | same as R2C1 | Med |

**Fixture list for ART.** Positions on the plan are not derivable from these views; place within the §1.3 shells, using the §1.5 raster strips as the only plan evidence.

| Room | Fixture | Count / size | Evidence | Conf. |
|---|---|---|---|---|
| HUB | chrome wire shelving, central island | ≈4 × 3 bays; bay ≈4 × 2 ft, ≈6–7 ft tall (convention) | HUB R1C3, R1C4, R2C2 | count Low, type Med |
| HUB | chrome wire shelving, perimeter runs | along at least the back and left walls of the R1C3/R2C2 views; two long banks forming an aisle in R1C2 | HUB R1C2, R1C3, R2C2 | Low |
| HUB | orange-painted rack posts on some bays | a few | HUB R1C2 | Med |
| HUB | shrink-wrapped pallets of blue cases | 2–3 | HUB R1C3, R1C4, R2C3 | Med |
| HUB | yellow tote stack + hand truck | 1 stack | HUB R2C2 | Med |
| HUB | black plastic crates / totes | several | HUB R2C2, R2C3 | Med |
| HUB | desk with computer + office chair | 1 desk visible | HUB R1C4 (matches plan "desks + computers") | Med |
| HUB | long counter/bench along a wall | 1 | HUB R1C4 | Low |
| HUB | rolling carts (blue, red) | 2 | HUB R1C4 | Med |
| HUB | doors: green door with round logo = **SE emergency exit** (DEC-030, §1.4); black door with yellow sign = **unconfirmed** (Nolan does not recognize it; no door added) | 2 | HUB R1C4, R1C2 | High (green door = exit) / Low (plan position); black door unconfirmed |
| HUB 2 | copier/printer | 1 | HUB R1C1 | Med |
| HUB 2 | yellow-lid black totes | stack of 4 (+ more in R2C1) | HUB R1C1, R2C1 | Med |
| HUB 2 | shrink-wrapped pallets of blue cases | 2–3 | HUB R1C1 | Med |
| HUB 2 | work table with patterned front | 1 | HUB R2C1 | Med |
| HUB 2 | wire shelving / wire carts with boxes; blue stackable bins | several | HUB R2C1 | Med |
| HUB 2 | black cabinets | 2+ | HUB R2C1 | Med |
| HUB 2 | chrome wire merch rack with bags; brown wire display panels | 1 + several | HUB R1C1, R2C1 | Med |
| HUB 2 | doors: doorway (far left of R1C1), white door (R2C1) | 1–2 (plan shows 1) | HUB R1C1, R2C1 | Low (may be the same door seen twice) |
| both | finishes: white walls; dark large-format floor (HUB) vs gray square tile (HUB 2); dark-brown wood/wainscot band, with a lit strip on some HUB walls; ceiling not visible | — | HUB R1C1, R1C3, R2C3 | Med (finish) / none (sizes) |

Contents: misc storage only (Nolan). Case/box labels are **not** inventory data.

### 2.2 Register scale stand (DEC-021, DEC-026; REF-003 spec)

Sources: REF-002 (wall R2C3, R2C4, R3C2, BAND 07/10) + REF-003 back-of-register stills (§0; crops in `References/Index/register/`). The wide still is the R2C4 camera zoomed in. Size reference: a full-size POS keyboard (≈17.5 in wide, **convention**, not measured) on the counter top in the same frames. Floor-tile size is unknown (GAP-113), so the tiles give no scale.

**ART-002 graybox spec** (feet; +x along the counter, +y away from the counter toward staff):

| Part | Spec | Evidence | Conf. |
|---|---|---|---|
| Type | free-standing chrome wire-frame stand (utility-cart style), 4 chrome corner posts, black top tray with a raised lip | `east_stand`, `center_close_stand`, `wide_stand_A/B` | Med |
| Footprint | **≈1.6 W × 1.3 D ft** (range 1.4–1.8 × 1.1–1.5). Width ≈ 1.0–1.2× the keyboard width in East and wide frames | keyboard ratio, perspective-corrected by eye | Low-Med |
| Top height | **≈2.5 ft** (range 2.2–2.8): the top tray sits clearly **below** the counter top, by ≈0.7–1.2 ft. Absolute value hangs on the 36–42 in counter convention (GAP-108) | all four crops | Low |
| Levels | **2**: the black top tray + **1** open chrome wire shelf in the bottom third (≈0.5–0.8 ft above the floor). No middle shelf seen | `east_stand`, `wide_stand_A`, `wide_stand_B` | Med |
| Top contents | 1 white bench scale (blue LCD, clear round draft-shield bowl with lid). The close centre stand carries **2** white scale bodies side by side (second may be a spare scale; Low). Small items: label/tape, wipes | all crops | Med (1 scale) / Low (2) |
| Lower-shelf contents | white paper bags/boxes, spare supplies (not readable) | `east_stand`, `wide_stand_A/B` | Med (presence) |
| Acrylic panel (DEC-026) | clear acrylic panel, **full stand width, on the counter-side edge of the top tray**, rising from the tray to about the counter top or a few inches above (**≈0.8–1.2 ft tall**). In the wide view it reads as a 3-sided clear box/riser (papers and bags are stacked on top of it). Thickness not visible | `center_close_stand`, `wide_stand_A`, `wide_stand_B` | Med (position) / Low (size, box vs panel) |
| Placement | pushed against the staff side of the register counter, in front of the counter's open under-shelves; **one stand per POS, to the staff's right of that POS monitor** (wide: right of the dark monitor and right of the next one; centre close: right of the centre monitor). A black wire trash bin often sits next to it (`wide_stand_A`) | wide + centre stills, R2C4 | Med |
| Count | 4 POS monitors in the wide/R2C4 view (left one dark/off); stands seen at 2 of them, a third at the frame edge, the fourth hidden behind a foreground seat back. One more stand in the East feed. **≥4 stands**; total = number of POS stations (GAP-107) | wide, East | Low-Med |
| Finish | chrome wire + black top tray; counter top is black stone-look with light veining; staff floor is black/white geometric cement tile, customer floor white marble-look | crops | Med |

Other counter facts in these stills: each POS has a monitor, keyboard, receipt printer and a customer-facing card terminal/tablet on the counter (Med). Open black shelves under the counter hold tape rolls, kraft bags and boxes (Med). Wide still, seen beyond the queue from left to right: video wall (showing a promo panel "HIGH VARIETY · 10 for $75 · 15 for $100"; units not shown, **not pricing data**), "THE FLOWER SHOP" logo living wall, "DELI STYLE FLOWER!!" counter with a teal/white checker front and globe pendant cluster, teal-backlit jar walls (High, same as R2C4; feeds GAP-106).

### 2.3 FOH / BOH desk stills (REF-006, DEC-041)
Both are single fisheye-ish overhead feeds with no timestamp overlay. **No people are visible in either still.** No chair is visible either, but per DEC-041 each desk gets one in the game. Sizes are Low (no scale object except doors, which are 3'-0" × 7'-0" per TI §6.2). Positions are relative to the frame; ART places them on the plan (§1.3 rooms, A011).

| Still | Item | What is seen | Size / height | Conf. |
|---|---|---|---|---|
| FOH | doorway (left of frame) | black-framed door opening into the vestibule; the floor beyond is **white tile with a grey curved/quatrefoil pattern** (TL-2-type 8×8 patterned tile, §6.5), and FOH is concrete. A wall card reader sits beside the jamb, an outlet low on the jamb wall, and red/white floor tape on the concrete | door 3'-0" × 7'-0" (TI) | High (type) |
| FOH | wood/black-metal open shelf unit | seen through the doorway, in the tiled vestibule, holding supplies | ≈2.5 ft wide, ≈4 ft tall | Low |
| FOH | **computer desk** | "in the middle against the wall" (DEC-041): a black wire shelving unit used as a desk on the back wall, with a monitor on an upper shelf and a keyboard shelf at standing/desk height; a white apartment fridge is immediately to its right | ≈3–4 ft wide × ≈1.5 ft deep, ≈6 ft tall unit | Low |
| FOH | fridge | white top-freezer apartment fridge, back wall | ≈2.0 × 2.3 ft, ≈5.5 ft tall | Low |
| FOH | **glass-door cooler** | black-frame, internally lit merchandiser, right of the fridge on the back wall, two lit glass doors visible (matches R4C1 "two glass-door coolers") | ≈4 ft wide (2 doors), ≈6.5 ft tall | Low |
| FOH | chrome wire racks | one free-standing chrome rack (4–5 shelves) in the room centre/right, loaded with clear and black bins of packaged product, mylar bags and cartons; a second chrome rack runs along the right/back wall with boxed product; a yellow tote is on the floor in the foreground | standard chrome-wire bays ≈2 × 4 ft (or 2 × 5), ≈6 ft tall | Low (convention) |
| BOH | chrome wire rack island | large chrome rack of 4–5 shelves seen from above, carrying green "OGeez!" and navy "Baked Bros" case boxes, white cartons and loose product on the lower shelves | ≈2 × 5 ft bay, ≈6 ft tall | Low |
| BOH | wall rack | chrome rack along the right wall, stacked black cases and white cartons on the upper shelves | ≈1.5–2 ft deep | Low |
| BOH | **computer desk** | right edge of frame: a white counter/desk with a black monitor, keyboard and a small device. This is the old register-1 computer (DEC-041) | desk depth ≈2 ft; height not measurable | Low |
| BOH | dark doorway / black panel | top centre of frame beyond the rack, with a small chrome rack above it holding cartons | — | Low |

The HUB-style "wire rack bay ≈4 × 2 ft, ≈6–7 ft tall" in §5 applies here too.

### 2.4 Deli jars, jar wall, scale and prep cart (REF-007, DEC-042, DEC-043)
| Item | Evidence | Size | Conf. |
|---|---|---|---|
| **House deli smalls jar** (DEC-042a) | Amazon B0GX12Q9G8, "USYOGO POP Airtight … Food-Storage Container", sold as a 2-pack with 2 scoops (3.3 oz). Published: **6.1" L × 5.3" W × 10.4" H, 4 L / 4.2 qt**, clear, "food-grade" BPA-free plastic (the resin is not named), one-press airtight pop lid, stackable. Fetched 2026-10-29 | 6.1 × 5.3 × 10.4 in | High (published) |
| **Deli flower canister** (DEC-042b, DEC-043) | office photo and retail jar-wall photo: tall square clear acrylic canister, white push-button lid with a dark gasket, coloured base band (green seen), a THC % label card ("28.57 %", "27.73 % Blue Tint #2") clipped on the front; about 12 empties on the cart, lids off and laid flat | **≈6 × 5–6" footprint × ≈10–10.5" tall** (Low-Med). Office: read against the scale body (≈6–7"). Jar wall: front height:width 1.6–1.9 on four jars, matching the published POP 4 L jar (6.1 × 5.3 × 10.4", ratio 1.7–2.0). Both photos agree with that size class; no direct measurement. The 12×12 / 8×8 floor tile is too oblique to use | Low-Med |
| Deli scale | compact digital bench scale, light-grey body, LCD and coloured keys on the front, a clear glass mixing bowl (≈8" Ø) on the pan; a small chrome scoop beside it | body ≈6–7" W × ≈8" D × ≈3" H | Low |
| Deli prep cart | stainless utility cart, flat top + lower shelf, tubular push handle, casters, "FOR DELI USE ONLY" label on the rail, spray bottles hung from the rail; the lower shelf holds bins, bags and paper | top ≈30" × 18–24", top ≈34–36" AFF (standard utility cart; about 6 jars span the back edge) | Low |
| **Jar design on the wall** (DEC-043) | every tall jar is the same: clear square acrylic body, **white push-button pop lid**; a **white brand label card** on the front lower half (brand + strain name, e.g. "Sanfermade", "Copperstate", "Purple Raspberry"); a **white THC % tag** (large "22.5 %", "24.9 %", "23.1 %", with a small strain line) clipped across the front at about mid-height; and a **coloured base band** ≈20–25 % of the height (≈2–2.5"), one colour per brand (green, red, white, black seen; the band carries the brand name) | band ≈2–2.5"; card ≈½ jar width; tag ≈⅓–½ width | Med (design) / Low (sizes) |
| Shorter jars | a few shorter canisters of the same design stand on the counter at the right, ≈⅔ the height of the tall jars (≈7"). Per DEC-043 the game shelves every jar, so these are out-of-place jars and the short size is not confirmed as a standard | ≈7" tall | Low |
| Jar-wall shelves | wall-mounted **dark-grey sheet-metal shelves** with a front lip on black standards/brackets, one jar deep (≈10–12"); two shelf tiers above the counter, ≈1.3–1.5× jar height apart (≈14–16"), plus jars on the counter top itself; the top shelf runs under a green/black checker tile band | depth ≈10–12", spacing ≈14–16" | Low |
| Wall behind | **teal** with a darker teal **curved-leaf / arc pattern** (matches WC-1 "wall behind displays", §6.5); green-and-black checker tile band above the top shelf | — | Med (finish) |
| Counter | **black** top (dark quartz or laminate), base cabinets with **walnut drawer fronts** (PL-1/WD-1-like) and silver cup pulls, two drawer rows; black lower bins of packaged product at the left end | top height not measurable here (34" max per TI millwork, §6.4) | Med (finish) |
| Bags | branded kraft paper bags with handles, standing in a row on the top shelf at the right end | ≈8–10" wide | Low |
| Stainless tong cups | small stainless cups/trays behind or beside each jar on the shelves | — | **not modelled** (temporary, Nolan, DEC-043) |
| Floor / ceiling | white-and-grey patterned tile at the counter (TL-2 type, §6.5); dark wood-slat accent ceiling at the top right (CLG-1) | — | Med |
Use the derived crops for art reference; never ship the raw photos. The office photo and both crops show no people; the raw jar-wall photo shows a shopper at the right edge.

## 3. BAND photos (`…_NN.jpeg`)

| # | Room / zone | Fixtures | Materials / finishes | Clutter | Signage | Human-scale cues | Staff attire / vibe |
|---|---|---|---|---|---|---|---|
| 01 | Retail, beside the arch | rounded arch through a vertical wood-slat wall, chrome wire accessory racks, deli jar wall (lidded clear canisters with label cards), black display counter | walnut-tone slats, teal swirl-pattern shelf backs, black shelves, dark slatted ceiling baffles, dome camera | dense merch, sticker rolls | brand plaque (round logo) | people stand next to the arch (opening is well above head height) | black graphic tee, crossbody bag, cap, nitrile gloves; teal polo + gloves. Casual, playful |
| 02 | none (face close-up) | — | — | — | — | — | not used for the environment |
| 03 | Break room | upper/lower wood cabinets, black counter, stainless sink + gooseneck faucet, pod coffee maker, microwave | wood-grain laminate, black counter | spray bottles, snacks, notes | handwritten note | person sitting on the counter shows counter height relative to a seated adult | black tee + crossbody + cap; light polo, distressed jeans. Off-shift, relaxed |
| 04 | Office | desk, monitor, corkboard, black "Heritage" safe, cardboard box on top | dark desktop, white wall | papers, bottles, can | corkboard notices | safe is about shoulder height on a seated person | black tee + flat-brim cap; reversed cap. Goofy selfie |
| 05 | Retail, register side | deli jar wall, HP POS, wall-mounted TV, **"Fine Cannabis" white neon**, blue-lit counter fronts, wood bench | teal shelf backs, blue/white patterned cement tile + white marble tile, dark ceiling baffles, globe pendants | kraft bags hung on the shelf | handwritten "TECHNICAL ISSUES / STORE IS CLOSED" sign | person standing in front of the counter | black "The Flower Shop" tee, lanyard with pins, glasses |
| 06 | Retail → arch → Hall | rounded white arch through the wood-slat wall, chrome wire rack, jar wall, black counter with label rolls | wood slats, patterned tile visible through the arch | stocked rack | jar label cards | **person standing inside the arch: best arch-height cue** (Low) | dark tee, cap, jeans |
| 07 | Retail, deli/jar area near arch | large square acrylic deli jar ("THE FLOWER SHOP" label, THC card), scale, stainless step can, framed product display | patterned tile, white wall | — | THC % jar card | **jar held in arms: best jar-size cue** (Low) | black tee, lanyard, glasses; polo + gloves; cap |
| 08 | Retail, by living wall (rotated image) | living-wall greenery, lit wood display shelf, counter | dense foliage, wood, white | boxes on the counter | — | — | white graphic tee, glasses |
| 09 | Office / IT (rotated image) | IT/network rack with open cabling, box fan | metal, white wall | cable mess | — | — | close-up, sunglasses |
| 10 | Retail, along the jar wall (rotated image) | jar wall, wire bins, trash can, globe pendant cluster, scales | brown/white geometric cement tile, dark slat ceiling | dense | "THURSDAY" daily deals sheet | full-height people beside the counter and pendants | black tee + cap; light top + lanyard |
| 11 | Retail, jar wall | backlit jar wall in arched wood frames, glass top counter, pre-roll/vape displays, jar stacks | teal swirl backs, warm LED strips, wood frames | dense product | brand jar cards (no inventory recorded here) | jar vs torso | black graphic tee, crossbody, cap, sunglasses, gloves |
| 12 | Retail, register line | POS monitors in a row, deli jar, stanchions, queue area, black merch display | white floor, black counters | cups, bags | — | standing customers | black "The Flower Shop" tee, pin-covered lanyard, backwards cap |
| 13 | BOH/office corner (Low) | wall shelf, thermostat, IT box, fan | white wall, wood shelf | — | — | — | plaid overshirt, pin lanyard. Selfie |

Product names visible on jar cards or boxes are **not** inventory data and must not be used as such (CLAUDE.md).

## 4. Room × source coverage

| Plan room | Plan | CCTV | BAND photo | Status |
|---|---|---|---|---|
| Retail | ✔ | R2C1–C5, R3C2 + REF-003 register stills (§2.2) | 01, 05, 06, 07, 08, 10, 11, 12 | well covered |
| Hall | ✔ | R3C4 | 06 (through the arch) | covered |
| Office | ✔ | R3C3, R4C5 | 04, 09 (13?) | covered (safe/IT side only in notes + photos) |
| Break room | ✔ | R3C5 | 03 | covered |
| JC | ✔ | door only (R3C5) | — | location and size from A011 (§7.3); interior blind |
| Restroom | ✔ | — | — | **BLIND** on camera; fixtures from A011 (§7.4) |
| FOH | ✔ | R4C1 + FOH still (§2.3) | — | CCTV only, two views |
| BOH | ✔ | R4C2 + BOH still (§2.3) | — | CCTV only, two views |
| Arch vestibule (unnamed) | ✔ | edges in R4C1/R4C2 | — | partial |
| HUB | ✔ | R4C3, R4C4, R5C3, R5C4 + HUB wall R1C2–C4, R2C2, R2C3 (Med) | — | CCTV only (§2.1); no photo |
| HUB 2 | ✔ | R5C1, R5C2, R5C5 = HUB wall R1C1, R2C1, R2C4 (Med) | — | CCTV only (§2.1); no photo |
| Exterior | (doors only) | R1C1–C5, R3C1 | — | CCTV only, night |

## 5. Scale cues for the graybox

| Cue | Value | Method | Conf. |
|---|---|---|---|
| Building / room shells | §1.3 table | printed dims + vector scale 5.6095 pt/ft | High |
| Fixture footprints | §1.5 table | vector plan ("approximate" per legend) | Med |
| Entry opening | 6'-0" × 7'-0" storefront pair (plan draws 9.0 ft) | TI E101 §6.2, Hub ruling | High |
| Delivery door / emergency exit / HUB 2 door | 3.4 / 3.5 / 2.0 ft | vector arcs | Med / Low / Med |
| Interior door arcs (1.2–1.8 ft) | **not real widths** | the symbols are smaller than any code-compliant door. Use a standard 3'-0" × 7'-0" commercial door as a **labelled convention** until measured | Low |
| Arch openings | 3.81 ft (west), 3.0 ft (east) | vector | Med. Height 7'-0" (TI cased openings, §6.2); TI width 3'-0" vs drawn 3.81 west: plan width kept (position-bound) |
| Counter height | POS / back counter / millwork tops **2'-10" (34") max AFF** | TI 2022 A940 details 11/12 (§6.4, render-checked); deli case not in the TI set | High (34" max) |
| Ceiling height / grid | retail gyp 9'-0" with 7'-6" soffits and suspended dark-walnut accent panels; back rooms 2×2 ACT at 8'-0"/9'-0" | TI 2022 A101 RCP (§6.1) | High (heights) |
| Floor tiles | white marble-look large-format (retail field), black/white or brown/white geometric cement tile (counter zones, hall, vestibule), concrete (FOH/BOH), dark gray large-format tile (rack rooms) | visual | Med (finish) / none (tile size) |
| Wall thickness | 0.4–0.5 ft drawn gaps | vector | Low (drafting gap, not a spec) |
| Pendant pitch | 3.0 ft, 6 over registers | vector | Med |
| Register scale stand | ≈1.6 × 1.3 ft footprint, top ≈2.5 ft (≈0.7–1.2 ft below the counter top), 2 levels, acrylic panel ≈0.8–1.2 ft tall on the counter-side edge | keyboard (≈17.5 in convention) in REF-003 stills (§2.2) | Low-Med |
| HUB wire rack bay | ≈4 × 2 ft, ≈6–7 ft tall | about 4 bays span half the 28.3-ft HUB width in HUB R1C3; matches the common chrome-wire bay size | Low (convention) |

## 6. TI set (REF-004)

Source: RSP Architects "Interior TI Approved Set - PHX" (2022, City-approved 2022-12), text-read in REF-004, then imported (`References/TI/`) and spot-checked by render in REF-005 (A940 detail 11, A901 elevations 5/8, A011 entry). Values not render-checked are matched by label and by their order in the extracted text. **DEC-037: heights, materials and fixture types are valid; positions and run lengths are not** (use §1 / A011). Confidence: **High** = labelled value in a schedule or keynote; **Med** = a dimension next to its label in an elevation or detail; **Low** = a dimension whose owner is inferred from text order. No permit/licence numbers, vendor contacts or names are recorded here.

2022 room numbers → current plan: 101 Retail, 102/109 Hall, 103 Unisex (Restroom), 104 Lounge (→ Office), 105 Break, 106 JC, 107 Fulfillment (FOH/BOH zone), 108 Storage, 110/111 Storage (existing, → HUB / HUB 2).

### 6.1 Ceilings and soffits (A101 RCP, A320)
| Room | Ceiling | Height AFF | Conf. |
|---|---|---|---|
| 101 Retail | painted gypsum (PT-1) | 9'-0" | High |
| Retail soffits | gypsum, PT-1 on face and bottom; power for lit signage at the soffit | 7'-6" | High |
| Retail accent | CLG-1: suspended 4'×8' acoustic panels, dark walnut, hung on stainless cable, with end caps (this is the dark "baffle" ceiling in photos 01/05/10) | hung below 9'-0" (drop not given) | High (type) |
| 102 Hall, 103 Unisex, 104 Lounge, 105 Break, 107 Fulfillment | ACT-1 2×2 lay-in | 8'-0" | High |
| 108 Storage / 109 Hall | ACT-1 | 9'-0" | Med (which of the two rooms) |
| 110/111 Storage | existing, open to structure | B.O. truss 11'-0" | Med |
| Structure | existing wood trusses, roof EL 115'-6" over floor EL 100'-0" | — | High |

### 6.2 Doors and openings (A310 door schedule, A101 keynotes)
| Door | Room | W × H | Type / frame | Hardware type | Conf. |
|---|---|---|---|---|---|
| E101 | Retail entry | 6'-0" × 7'-0" | existing aluminum full-glass storefront | existing; "unlocked during business hours" sign | High |
| 101B | Retail | 16'-4¾" × 7'-6" | side-folding open-air security grille, clear anodized, with an 18"×7'-6" access door | — | High |
| 103 | Unisex | 3'-0" × 7'-0" × 1¾" | flush hollow metal, painted, HM frame | privacy lock with indicator, closer, kick plate | High |
| 104 | Lounge → Storage 110 (= office → HUB 2; A101 tag on the lounge south wall, schedule room name STORAGE; REF-013) | 3'-0" × 7'-0" | flush HM, salvaged door reinstalled | schedule set 1.0 (storeroom lock, closer), header set 4.0 (exit device, closer) | High |
| 105 | Break | 3'-0" × 7'-0" | flush HM, painted | storeroom lock, closer | High |
| 106 | JC | 2'-8" × 7'-0" | flush HM, painted | exit-device set | High |
| 107 | Fulfillment | 3'-0" × 7'-0" | flush HM, painted | storeroom lock, closer | High |
| 108 | Storage | 3'-0" × 7'-0" | flush HM, painted | storeroom lock, access-controlled | High |
| E110, E111A, E111B | Storage (existing): A101 tags put E110 on the storage 110 west wall (delivery door), E111A at the north end of the 110/111 partition (HUB 2 → HUB), E111B at the SE corner of 111 (SE exit) (REF-013) | 3'-0" × 7'-0" | existing flush HM | no change | High |
| Cased openings (the arches) | Retail → halls | 3'-0" × 7'-0" | gypsum-finished opening (keynote 10) | — | High |

Door hardware heights (A310): lever/strike centreline 3'-4" min to 3'-6", pull 3'-6", deadlock 4'-0". Switches are 3'-6" to centre (A101 note I).

**REF-012 door contract (DEC-096, DEC-103):** every door and opening, with hinge, swing, closer, lock and NPC use, is in **`Docs/Reference/DOORS.json`** (15 rows; Gameplay builds against it). A310 hardware sets as read (only closer / lock function / lever vs push bar; no access-control detail, DEC-051): set 3.0 (103) privacy lock with indicator + closer; set 2.0 (105) storeroom lever + closer; set 1.0 (108) storeroom lever + closer, "normally closed, latched and locked; free egress". The schedule column and the set headers disagree for 104 (1.0 vs 4.0 exit device), 106 (4.0 vs 2.0) and 107 (2.0 vs 1.0). Every candidate set has a closer and a lock, so only lever vs push bar differed. Existing doors (E101, E110/E111A/E111B) have no hardware scheduled. E101 is marked PAIR. **Propped open in practice (DEC-103):** vestibule→FOH, vestibule→BOH, hall→office, HUB 2→HUB. No second buzzed door after the ID stand (DEC-103).

**REF-013 (DEC-110, A101 tags, A011 vector arcs):**
- **Mapping (from the A101 door-tag positions):** 103 restroom, 104 office→HUB 2 (not hall→office), 105 hall→break, 106 JC, 107 vestibule→FOH, 108 vestibule→BOH, E110 delivery, E111A HUB 2→HUB, E111B SE exit. The hall→office door is not in the 2022 set: A011 (2023) adds it and labels it "ACCESS CONTROLLED DOOR", so it has no scheduled closer (selfClosing placeholder, GAP-138).
- **Hardware (DEC-110 W6, DEC-115 (2)):** push bar only on the retail east emergency exit, the SE exit and the delivery door (Nolan). Every other door follows its evidence: the A310 locksets are levers (sets 1.0, 2.0, 3.0), hall→office and HUB 2→HUB have no scheduled hardware (Low lever placeholders, GAP-138), and the storefront entry pair keeps its pull handles (`storefrontPull`). This replaces the schedule-column reading (JC was pushBar, delivery was lever).
- **Hinges (DEC-110 W5):** "left" = the hinge is on your left when you stand on the push side (the side the door swings away from) and face the door. CCTV-backed hinges stay (hall→office E, office→HUB 2 W, vestibule→FOH N). A011 draws the swing of every leaf. Its hinge agrees with the left default on the restroom (S), hall→break (N), JC (S), vestibule→BOH (N), retail east exit (N) and SE exit (E), and draws HUB 2→HUB (S) and the delivery door (N) right-handed. **DEC-115 (1)** lets the A011 vector override the left default (A011 matched CCTV on all 3 checkable doors), so those two are hinged S and N (Med). A011 swings: restroom in, hall→break in, JC out, the vestibule doors into FOH/BOH, office→HUB 2 into the office (the 2022 A101 had it into storage 110), HUB 2→HUB into HUB, delivery out, both exits out.
- **Restroom (DEC-110 W7):** staff only; the west arch is staff only. GAP-139 closed.
- **Positions:** A011 puts the entry pair at y 8.89–14.90 (from the retail north face; graybox 12.5–18.5) and the retail east exit at y 21.65–24.65 (from the south wall). Both rows carry a `target_opening`.
- Every DOORS.json field now has an `audit` record (conf, exact sources, gap); the changed values are tabled in `Docs/Handoffs/REF-013.md`.

### 6.3 Partitions (A320)
Type A runs full height to the truss: A3 = 3⅝" stud → **4⅞" wall** (typical); A2 3¾", A4 5¼", A6 7¼". Type G has partial-height gypsum on full-height studs: G2 3⅛", G3 4¼" (G3 insulated at exterior walls and the grid-2 south wall), G6 6⅝". Two retail partial walls are tagged **5'-0" tall**. Existing exterior walls are CMU, furred with metal studs and ⅝" gypsum. High.

### 6.4 Millwork and counters (A901 elevations, A940 millwork)
| Item (A940 tag) | Heights / dims | Finish | Conf. |
|---|---|---|---|
| All base cabinets (BC, BD, BP, BO, 3DE, 4D, BT1, BSK) | **counter top 2'-10" (34") max AFF**; 4" toe base (2" recess); 2'-1" overall depth (2'-6" top on the POS cabinet); 1½" countertop with backsplash on the 4D/3DE-breakroom cabinets (details 12, 9) | PL-1 walnut laminate fronts, black melamine interiors | High (34" max: rendered A940 details 11, 12; repeats on every cabinet) |
| POS cabinet (11, "two-drawer POS") and the POS elevations (5 front, 8 back counter, 10/11) | **quartz top with a 2" edge, 34" max AFF, 2'-6" deep top, 4" base** (rendered A940 detail 11 "3DE two-drawer POS cabinet", two equal drawers; the 1½" in the REF-005 first pass belongs to detail 12, the 4D cabinet); elevation 5 runs cabinets 11 + 12 (4D) under QZ-2 with a green wall above; elevation 8 (back counter) runs cabinets 8 + 15 with the register monitors standing on the top; 3'-0" clear arched "open to beyond" pass-throughs in a vertical-slat wall, flanked by 2'-11¼" / 1'-6½" piers; QZ-2 waterfall edge wraps the outside of the POS counter; filler panel painted black | QZ-2 white quartz top, WD-1 walnut veneer POS front, ML-1 black-patina metal laminate, HW-2 brushed-brass edge pulls | High |
| Back-counter tile (POS elevation) | TL-2 8×8 patterned tile with bronze trim; 2'-0", 3'-6" and 7'-0" appear on this elevation (likely backsplash, wainscot top and sconce) | TL-1, TL-2, MTR-3/4 | Low |
| Retail display shelving (BDD 3/7/14, "special wall display" 4) | cabinet base to 34" max, then glass showcase shelves at 1'-2" spacing (×3) plus 8" and 6"; curved top trim R 1'-4¼"; recessed linear LED; anti-glare film on the glass; modular for relocation | black or chrome glass-showcase hardware, WC-1 wallcovering on the rear panel, PL laminate trim | Med |
| Retail display with boxes (7, 16 "box display") | glass-lid, wood-frame boxes on a rolling track; 6 equal spaces over 7'-9"; 2" matte-black bar foot rail between boxes; 4" puck lights | PL-1, tempered glass lids | Med |
| Slat wall (SW, detail 10) | ¾" plywood with Di-Noc wood grain, hung on Z-clips | WC-2 | High |
| Breakroom sink (OS3) | sink rim 34" max, knee clearance 27" min | QZ-1 quartz | High |
| Green wall + backlit logo | in-wall backing and power (green wall supplied by others) | — | High (type) |
| Wall monitor (TV) | outlet at 60" AFF | — | High |
| Neon signage | **72" AFF to the bottom of the fixture**, owner-provided, on the retail elevations | — | High |
| Decorative sconces, semi-flush ceiling fixtures | on the retail elevations | — | High (type) |

The deli case, the deli counter and the jar-wall jar sizes are **not in the 2022 set** (it predates the deli layout), so they stay open (GAP-113). The 2022 retail-display run lengths (27'-9", 19'-2¾", 9'-0", etc.) describe the old layout; do not use them for positions.

### 6.5 Finish and material schedule (A310, I101)
| Tag | Product type | Colour / size | Where |
|---|---|---|---|
| TL-1 | porcelain, marble-look | Statuario Bianco, 12"×24"×⅜" | retail floor field |
| TL-2 | patterned ceramic | "Madrid" 8"×8", dark grey grout | floor zones and walls |
| VCT-1 | vinyl composite tile | 12"×12" | back rooms |
| CONC-1 | ground and sealed concrete | — | storage floors |
| VB-1 | vinyl base | grey, 4" | all base |
| FRP-1 | white FRP | 4'×8' | to 4'-0" AFF in wet rooms |
| PT-1 | paint, SW7646 First Star | eggshell on walls, flat on ceilings | typical walls, all gypsum ceilings and soffits |
| PT-2 | TFS custom mix | — | feature |
| PT-3..PT-8 | SW0016 Billiard Green, SW6060 Moroccan Brown, SW6057 Malted Milk, SW9137 Niebla Azul, SW7747 Recycled Glass, SW6271 Expressive Plum | — | accent walls (retail elevations) |
| WC-1 | patterned wallcovering ("Burst", Kasha) | — | wall behind displays only |
| WC-2 | 3M Di-Noc wood grain | — | slat wall |
| PL-1 / PL-2 | laminate, Italian Walnut / black matte | 4'×8' | millwork / vertical surfaces |
| ML-1 | metal laminate, black patina | — | POS and millwork accents |
| QZ-1 / QZ-2 | quartz, pink-white veined ("Rose Bay") / white ("Vesuvius") | eased edge | counters / POS top |
| WD-1 | walnut veneer | — | POS front |
| GL-1 | green-tinted storefront glass | — | storefront |
| CLG-1 | suspended acoustic panels, dark walnut | 4'×8' | retail accent ceiling |
| HW-1 / HW-2 | vintage-bronze 3" pull / brushed-brass drop-edge pull | — | cabinets / POS drawers |
| MTR-1..5 | Schluter trims: antique bronze, brushed brass, dark anthracite | — | tile edges, transitions |

Switch and outlet plates are white on white walls and matte black on finished walls. Fire-extinguisher cabinets are painted black.

### 6.6 Restroom (A901 enlarged plan, G010)
Mirror 1'-8"×3'-6" at 3'-4" AFF; grab bars 42", 36" and 18" vertical at 33–36" AFF; semi-recessed towel dispenser with waste, wall soap dispenser, surface toilet-paper dispenser and napkin disposal; wall sconce (L6). ACT ceiling at 8'-0", TL-2 floor and wall tile. High (types), Med (positions).

### 6.7 Lighting (E-sheet luminaire schedule, A101 RCP key)
All LED, 3500K, 0–10 V dimming, dimmed to 30 % after hours. L1 2×2 troffer (ACT rooms); L2 2'/4' strip (storage); L3 linear LED (millwork, recessed); L4A/L4B 4½" downlights (retail gypsum ceiling); L5 small flush mount; L6 bathroom sconce; L7 task light; L8 18" under-cabinet. The RCP key also shows pendants, wall sconces and decorative fixtures. High (types).

### 6.8 2026 A011 / A012 (AZDHS update)
A011 "Floor Plan" (Dispensary - Floor Plan) and A012 "Floor Plan - Lighting" (legend: checkout counter light, pendant light, recessed can, 2×2 ACT light, downlight; "windows - natural light"). Room areas match §1.3. A011 entry ("secure entrance / exit", west wall): a 6'-0" out-swinging storefront pair (two 3'-0" leaves, 6.0 ft by vector at 18 pt/ft), which matches TI E101. A011 also shows access-controlled entrance/exits at the west wall by the office and at the SE corner of the 818 SF storage. A011 labels "secure entrance / exit", "emergency exit only", "POS stations", "display cases", "shelving" and "hand washing sink". The working plan is built from A011 + A012. No A013 turned up in that folder; its third sheet is the security plan, which we never read by rule.

### 6.9 "COMPILED_Flower Shop_Int Set.pdf" (REF-005): not this store
Same Floor Plans folder (24 pp, 5.9 MB, read as text). It is the RSP **Ahwatukee** retail interior set (10827 S 51st St, sheets dated 09/2021: I100 demo, I102 RCP, I310 schedules, I701 elevations, I940 millwork). It has no Phoenix/McDowell sheet and no deli case, deli counter or jar items. It shows that the Phoenix millwork (§6.4, the same glass-showcase display family) follows the TFS store standard, but **no values from it are used** (another store). A search of M365 for deli case/jar specs found only Dutchie inventory exports.

## 7. Back-room fixture mapping (REF-008)

Numbers live in **`Docs/Reference/ROOM_FIXTURES.json`** (86 rows after REF-009b: room, fixture, type, size_ft [w,d,h], pos_ft centre, rot, faces, confidence, source tiles, plus a graybox-contradiction list). Positions use the §1.2 frame, mapped into the V5/graybox shells. A011 interior dims (office 13'-8¾", break 10'-6", FOH 12'-1¼", BOH 10'-4¼") do not sum to 47'-2¼" with walls (GAP-125), so A011 features are placed by their fraction of each room.

**Method.** Every tile of both camera walls was cropped from the original PNG and upscaled 2× (wall 2 first), the HUB wall and stills were re-read, and A011 was rendered at 250–300 dpi. Crops are working files only; nothing new is committed. Size refs: 3'-0"×7'-0" doors, 34" counters, 4×2 ft wire bays (convention).
**New chat-only sources (Nolan, 2026-10-29, not in the repo):** `chat_office_L` (new: office looking south), `chat_office_R` (= R3C3), `chat_BOH_L` (= R4C2), `chat_BOH_R` (= BOH still), `chat_FOH_L` (= R4C1), `chat_FOH_R` (new: FOH looking toward its door).
**Excluded by rule:** camera mount layout, access-control hardware, alarm items, safe interiors, screen contents, one large office wall screen. REF-009 (DEC-051) adds: no safe types or positions, cash-handling equipment or camera-system hosting, even where Nolan named them; generic props only. DEC-062: the hall keypad is a plain blank panel only.
**REF-009 (DEC-051, Nolan's answers to REF-008 Q1–15 except Q4 and Q11) and REF-009b (DEC-062, the remaining room answers):** applied below. Placements beyond what Nolan stated (rolling-rack spans, FOH entry props, break-room board/table/bench layout, office east-wall stack, restroom chest, JC props, BOH carton rack position) and the REF-008 Q20 LED strip carry **GAP-127** in the JSON `gap` field. Still open: REF-008 Q4 (vestibule size), Q17 (BOH black frame), Q20 (LED strip). Q21/22 closed: no further photos available (DEC-062).

**Tile triage.** Back rooms appear only in R3C3, R4C5 (office), R3C4 (hall), R3C5 (break), R4C1 (FOH) and R4C2 (BOH), plus the FOH/BOH stills and the chat views. Exterior, retail, HUB, HUB-wall and register frames show nothing behind the arches (R3C2 shows the arch from retail). Wall 1 matches wall 2 apart from people and loose items.

### 7.1 Office
Views: R3C3/R4C5 (looking N), chat_office_L (looking S), R3C4 (through the open door). The hall door is at the **east end of the north wall** (x 10.2–13.3, A011), black, hinged east, swings in. The HUB 2 door is on the south wall (x 7.2–10.2), white, with a coat-hook rail. Layout (Med): black **L desk** along the west wall under a green **"THE FLOWER SHOP" neon**, dual monitors in the NW corner, and a stainless folding-leg worktable along the north wall below a fabric pin board and three floating shelves. **Two plain tall black cabinets** (closed boxes, DEC-051 Q9) on the south wall west of the HUB 2 door. The worktable carries generic desktop office machines incl. a laminator (Q10). Deli prep cart (§2.4) under a wood canister shelf east of that door. East wall (Q13, Q15, Q12): a **standing desk** used as a shelf over several black file cabinets, with the IT rack (a plain box), a desktop computer and a white portable fan on it; step can by the door. The black bar in chat_office_L is part of the door (Q14), not a fixture. Loose items: 2 task chairs, a wire cart, a small drum kit, a plant. White speckled VCT floor. **GAP-121:** V5 and the graybox have the office mirrored east–west.

**REF-012 walkability (DEC-096, playtest 1: "almost unwalkable").** Interior 13.5 × 9.8 ft (x 0.2–13.7, y 36.5–46.3). Standard used: main path ≥ 3.0 ft, a reach zone ≥ 2.5 ft deep in front of each desk/cabinet, door swings kept clear (3.0 ft leaves). The rev6 placement failed it in four places: the wire cart and drum kit filled the whole reach zone of both tall cabinets; the plant sat inside the HUB 2 door swing; cabinet A ran 0.1 ft into the HUB 2 opening and hit the open leaf; the plant–standing-desk pinch on the main path was 2.9 ft. **Corrected placement (ROOM_FIXTURES Office rows):** cabinets B/A at x 2.2–4.6 / 4.6–7.0 against the south wall; deli cart x 10.3–12.8 against the south wall; standing-desk stack and step can pushed to the east wall face (x 11.7–13.7; can y 39.6–40.6); chair 1 y 39.8–41.8; wire cart at the east end of the worktable front (x 8.2–9.7, y 39.2–40.7); drum kit in the SW pocket (x 0.2–2.2, y 44.05–46.25, cut to 2.2 × 2.0); plant east of the deli cart (0.9 ft pot). The result: main path hall door → HUB 2 door ≥ 3.0 ft everywhere (3.0 pinch between the wire cart and the step can, 3.3 at the HUB 2 approach); the L desk, worktable, both cabinets and the standing desk/file cabinets each get a ≥ 2.5 ft reach zone; both door swings are clear. Exception: the deli cart's front reach is only 1.4 ft wide (GAP-136). Every stated fact is kept: L desk + neon on the west wall, the worktable on the north wall ending 0.4 ft short of the hall door, the two cabinets on the south wall west of the HUB 2 door, the cart and canister shelf east of it, and the stack on the east wall with the can by the hall door. Moved or resized guesses carry GAP-135/136. **Final assets will likely be larger:** a real standing desk (~4 ft), a compact drum kit (~3 × 3 ft, which won't fit), task chairs with arms and a 5-star base, spray bottles on the deli-cart rail, and file drawers that open ~1.5–2 ft into the reach zone. The hall→office door is almost always propped open (DEC-103), so its open leaf rests against the east wall north of the step can (y ≤ 39.5).

### 7.2 Hall (west)
R3C4 looks SE from the NW. Break door (black, "EMPLOYEES ONLY", fire label) is on the east wall, y 29.9–33.0. Office door is at the SE corner. Restroom door is on the west wall, y 33.1–36.1 (A011 only). Wood corkboard ≈1.8×2.6 ft with taped notices. A small wall device near the arch (A011) is security hardware (DEC-062): a plain blank panel only. TL-2 black/white tile (High). **GAP-123:** graybox doors are off by 1–2.2 ft.

### 7.3 Break room + JC
R3C5 (from the SW, looking N/NE) and A011 agree (Med). A pilaster at x 18.3–18.9. Plain north wall west of it (labour-law poster); the **first-aid kit** is on the pilaster (DEC-051 Q8). A **bulletin board** (staff schedule, events, updates; contents not modelled) is on the hallway (west) wall between the hall door and the whiteboard (DEC-062; position Low). Wood/black-top cabinets east of it, returning down the east wall to y 37.4, with a double sink at y≈34.4. A magnet-covered **fridge** at y 37.7–40.5. West wall (DEC-051 Q6–7): a **whiteboard** (the red/white frame), a lunch **table** pushed against it, and the wood **bench** beside the table on its east side (longer than the table, so it can't go under it); mini hoop and coat hooks near the SW corner. **JC (GAP-103 closed):** SE corner, x 19.3–23.31, y 41.3–46.3 (≈19.2 SF), with its 2'-8" door on the west face at the south end (the black door with a note in R3C5) and inside it a mop sink (A011), mops and brooms, and a small rack of cleaning supplies (DEC-062). **Staff lockers (store fact, DEC-047):** **one unit, about 2 × 6 ft** (DEC-051 Q5; read as 2 ft wide × 6 ft tall). Its grey top shows in the R3C5 foreground (a cap and a strap sit on it). The wall is still unknown (GAP-126 narrowed, position null in the JSON).

### 7.4 Restroom (no photos; layout from Nolan, DEC-062)
A011: toilet in the NW corner (tank on the west wall), grab bars on the north and west walls, sink in the SW corner, door at the south end of the east wall. Nolan (DEC-062), entering heading west: **straight ahead** a white full-size sink with a full-size mirror; to the sink's **left** an old silver manual paper-towel dispenser (A011 south-wall item); **far right** a standard white toilet; **between sink and toilet** a flat-black storage tool chest (swing-out doors, 2 shelves); one large storage cabinet of bathroom and cleaning supplies, which DEC-062 called the "back wall". **DEC-068 corrects this:** it stands next to the restroom door, against the door (east) wall. The side is not stated, so the placeholder is the north side, the only side that clears the door span: x 6.5–8.0, y 29.7–32.9, 3.2 ft wide, 7 ft tall (Low, GAP-109; REF-010, as built by ART-006). Finishes per TI §6.6.

### 7.5 Vestibule (A011 HALL 35.16 SF)
**≈8.4×4.8 ft** at x 31.4–39.8, y 29.5–34.3 (High). The FOH door is on its west face and the BOH door on its east face, both at the north end, both 3'-0". The arch is x≈34.5–37.6. Supply shelf on the south wall (Low). TL-2 tile. **GAP-122:** the graybox draws it 3.0×2.2. The GAP-104 2.2 ft door exception lapses if ART adopts A011.

### 7.6 FOH
R4C1/still/chat_FOH_L look south from beside the door; chat_FOH_R looks toward the door. **Layout (DEC-051 Q1–3):** the wire-rack **computer desk + white fridge + 2-door glass cooler** stand on the **east wall shared with BOH** (GAP-124 closed). From the NE corner by the vestibule: a black **fire-escape ladder**, then the desk, fridge and cooler (DEC-062; the NE end follows from R4C1 looking south with the cooler right of the fridge). Entering from the vestibule door (heading west): **straight ahead** a small rack of deli bags, exit bags, misc tools and vape batteries; on the **right** (north) an aluminium trash can that usually props the door open, and an electrical box on the wall; on the **left** (south) the product racks start. There are **4 chrome product racks on rollers** with bins, sliding forward and back to open an aisle. They are the only FOH product racks (DEC-062): they replace REF-008's two island runs and the A011 wall strips. Rack length is unknown, sized from the room and photos (6 ft, Low). Sealed concrete with red/white tape. **Contents (DEC-050, store fact):** the racks hold mostly vapes and edibles plus some infused prerolls; the fridge holds drinks (cannabis colas and other beverages); the cooler holds all concentrates and perishable edibles. FOH is staff-only: customers never enter, the budtender fetches. **GAP-124 closed** (east wall). Graybox: `FX_FOH_Fridge` (west wall) and the 2 wire-rack runs disagree.

### 7.7 BOH
R4C2/chat_BOH_L look SW from the NE; the still/chat_BOH_R look NW from the SE. East-wall chrome run from y 31.3 to the desk. 2-bay west run at x 37–39, y 37.3–45.3. South shelving (A011, Low). Left of the vestibule door (seen from the SE), a chrome rack of drink cartons and misc boxes (DEC-062). Ex-register-1 desk on the east wall at y 40.3–44.3 (matches the graybox), with a barcode scanner beside the keyboard (DEC-062). LED strip over the aisle. Graybox `FX_BOH_Racks_W` starts at y 33, which collides with the vestibule.

Box and case brand names are not inventory data.

## 8. Sales floor (REF-011)

Playtest 1 (DEC-096) audit of the graybox against the evidence. Rows are in `Docs/Reference/ROOM_FIXTURES.json` rev8 (REF-013; rooms Retail, HUB and HUB2) and anchors are in `Docs/Reference/SCENE_ANCHORS.json`. The mismatch table is in `Docs/Research/LAYOUT_AUDIT_SALES_FLOOR.md`. Gaps: GAP-129..134.

### 8.1 Register runs (DEC-039/040)
- **Which counter is which (Med-High).** "Back Of Register center/East" (= R2C4), R2C3 and R2C5 sit **behind the south run, looking north**. Beyond the customers they show the north run (DELI STYLE checker wrap, its own jar wall), with the logo living wall and video wall on its left (west), the entry at the far left and the east jar wall on the right. R3C2 sits behind the north run (it has the lit display case) and looks south at the south run, with its jar wall and the east arch on the left. So the plan's "DELI COUNTER" L is the **south register run**. Both runs carry a DELI STYLE wrap. The graybox cameras R2C3/R2C4/R2C5 point the wrong way.
- **Staff aisle (Low-Med).** BAND 10 (rotate 90° clockwise) looks east along the south staff aisle. On the left is the register counter with POS monitors and chrome scale stands (a spray bottle hangs from one stand: DEC-096 kit). On the right is the south jar wall: a back counter with open bins, 2 shelf tiers, kraft bags and a deals sheet. TL-2 8" grout lines give **3.0–4.0 ft clear between the back of the stands and the back counter**, enough for two staff to pass. 3.0 ft is used.
- **South run unusable: cause and fix.** The graybox has 2.4 ft from the south counter's staff edge to the jar-wall front, which leaves 1.1 ft behind the 1.3 ft stands. REF-011 moved it by estimate; **REF-013 measured it (GAP-129 closed, §8.5):** customer face y 20.0, staff edge y 22.5, stand 22.5–23.8, back counter 27.0–29.0, so 3.2 ft clear behind the stands. The station 06 / stanchion-field clash is gone (06 now at x 20.4).
- **East return (Med, GAP-130 narrowed).** It is tight in the plan: 2.3 ft to the jar-wall front. REF-013 puts it at x 37.99–40.49, y 9.2–20.0, with 3.2 ft behind the stands (§8.5). The north run keeps the plan position and has 3.4 ft.
- **Stations.** Each has the monitor centre on the staff edge and the stand to the staff's right. The operator anchor is 1.0 ft off the edge, and the customer 1.2 ft off the counter face.

| Run | Reg | x, y | Operator faces | Clear behind stand | Conf. |
|---|---|---|---|---|---|
| North (staff N) | 08, 09, 10 | x 24.0 / 30.0 / 36.0, y 7.0 | S | 3.4 ft (to back-counter front y 2.3) | Med |
| East (staff E) | 12, 11 | x 40.49, y 12.0 / 16.0 | W | 3.2 ft (to x 44.99) | Med (REF-013) |
| South (staff S) | 07, 02, 03, 04, 05, 06 | x 36.4 / 33.2 / 30.0 / 26.8 / 23.6 / 20.4, y 22.5 | N | 3.2 ft (to y 27.0; 07 has 5.2 ft to the wall at the east arch) | Med: y High, x pitch Low-Med (REF-013) |

South order follows ART-003's reading of "left to right": a customer facing the counter, so 7 is east (GAP-131). Pitch is ≈3.2 ft (monitor pitch in the wide still is 3–3.5 ft). REF-013: 06 starts at x 20.4 because the west return (x 15.28–17.78) closes the aisle's west end. Every customer spot is ≥ 1.0 ft from both columns.

- **Station kit and trash (DEC-103/104).** Every station gets a small trash bin (placeholder: against the back of the stand, as in BAND 10 and wide_stand_A; Low, GAP-131). Three big bins are spread across the floor (rows `Trash_Big_*`). Only the one at the south return end has CCTV support (R2C5); the rest are Low (GAP-134). **Rule (DEC-104): small items are never uniform between stations** (presence, placement, condition), so ART and Assets vary each station's kit rather than copying one. The DEC-096 kit: label/receipt printer, scanner, mouse, keyboard, under-counter storage, a spray bottle on a stand, a rag. The ID-check stand directly left inside the entry (DEC-048) carries an ID scanner with a green light (DEC-103). There is no second door after it, so check-in leads straight onto the floor.

### 8.2 HUB / HUB 2 (DEC-022, §2.1)
- **Naming holds (A011).** HUB is the east room and HUB 2 the west room.
- **HUB.** R1C4 looks **south**: the green SE exit (DEC-030) is in its far-left corner. So the desk and chair (foreground) are at the **north** end of HUB, a long dark counter runs along the **east** wall and the pallets are on the west side. The graybox has the desks at the south (y 70–74.4, from the V5 raster strip) and chrome runs on the north and east walls (GAP-132).
- **HUB 2.** It matches: copier, totes, pallets, work table, merch rack, and cabinets on the office wall. One pose is off: R1C1 looks east, not NNE, since the connecting door is at the far left.
- **Positions settled (REF-013; GAP-132 narrowed to sizes, DEC-115 (4)).** Nolan confirmed the HUB layout (DEC-110 W3): the desk and chair are at the north end by the HUB 2 door, and the long dark counter runs along the east wall. A011, A012 and A101 draw no HUB furniture, so the counter length comes from hub_R1C4: about 20 ft (y 52–72). DEC-079's "HUB against the office wall" is HUB 2, because by A011 only HUB 2 shares a wall with the office. The furniture **sizes** (desk, counter depth/height/length, HUB 2 cabinets) have no drawing or measurable view and stay Low under GAP-132.

### 8.3 Deli walls: three (Med)
The evidence supports **three** stocked deli jar walls, one behind each register run:
- **North**, x 19–44.9: seen in R2C3, R2C4 and the wide still, behind the north run.
- **East**, y 0.2–14.2: backlit teal shelves in arched wood frames over a counter (BAND 11, R2C3, wide still).
- **South**, between the arches: BAND 10, BAND 01/06 beside an arch, R3C2.

The plan already draws all three: "deli flower jar wall" north and south, "jar wall" east. The graybox does not show them as three: the south wall is a solid block, and jarSlots fill only the north and east walls. Each wall is a back counter (TI base cabinet 2'-1", Low) with 2 shelf tiers, and jars also stand on the counter. The DEC-043 retail photo (walnut drawers) is probably the north wall (Low).

### 8.4 Stocking note (for Assets' stocking arranger; generator params unchanged)
Sources: the DEC-043 retail jar-wall photo, BAND 10, BAND 11 and BAND 01. All values are estimates by eye (Low).

| Row | Jar positions occupied | Gaps | Product level inside jars |
|---|---|---|---|
| Top tier | ≈85–95 % (shoulder to shoulder) | kraft bags fill the last 1–2 ft at one end | mostly 50–80 % |
| Middle tier | ≈50–60 % | clusters of 2–3 jars with 1–2 jar-width gaps (the tong cups there were temporary, DEC-043) | 40–70 % |
| Counter row | ≈30–40 % | irregular; some shorter jars, smalls jars and bags | 30–60 % |
| East (arched bays) | ≈1 jar per bay with ≈1 jar-width gaps (≈50 % linear) | lower counter row dense with small packaged jars | 50–80 % |

No shelf is uniformly full, and almost no jar is brim-full. Levels vary jar to jar because each 1 lb jar per strain sells down at its own rate, and house strains are doubled (DEC-079). Jars stay upright with labels facing out.

### 8.5 Drawing measurements (REF-013, DEC-110)
**Method.** Vectors were extracted with PyMuPDF `get_drawings()` and `get_text("words")`; no pixel reads. A011 and A012 are 1/4" = 1'-0". The tick-to-tick dimensions give **17.987 pt/ft** (47'-2¼" = 848.76 pt, 30'-6" = 548.52 pt).
- **Frame.** x = 0 at the A011 retail west interior face (the 47'-2¼" tick). A011 prints the retail interior **30'-6"** deep, but the V5 frame is 29.0 (GAP-125 family; the frame is not re-based here).
  - South-run and south-wall features are placed by their A011 distance from the south wall (y 29.0).
  - West-wall features are placed by their distance from the north wall (y 0). That mapping puts the A011 ATM niche at y 25.5–27.5, against the V5 ATM at 25.8–27.6.
- **Confidence.** High = printed dimension. Med = vector read.

| Item | Measurement | Sheet + vector coordinates | Result in the frame | Conf. |
|---|---|---|---|---|
| South run customer face | 9'-0" from the south wall | A901 detail 17 (printed). A011 drawing 3017 line y 19.99; A012 3109–3122 y 19.99 | y 20.0 | High |
| South run depth | 2'-6" POS top | A901 det. 17 (printed); A940 POS 2'-6"; A011 3019 / A012 3122 staff line y 22.49 | staff edge y 22.5 | High |
| South run length | x 15.28–41.03 | A011 3017/3019, A012 3120/3122 (agree to 0.01 ft); A901 printed 27'-9" (2022, 2.0 ft longer) | x 15.28–41.03 | Med |
| South run west return | 2'-6" wide, runs to the back counter | A901 det. 17 printed 2'-6"; A011 3017 x 15.28 to 3019 x 17.78, y 22.49–26.99 | x 15.28–17.78, y 22.5–27.0 | High (width) / Med |
| South back counter | 2'-0" deep, 19'-2¾" long | A011 2952/3002/3003, A012 3043: x 15.19–34.42, y 26.99–28.99; A901 printed 19'-2¾" = 19.23 | x 15.19–34.42, y 27.0–29.0 | High (length) / Med (depth) |
| **GAP-129 aisle** | counter to back counter 4.5 ft; 3.2 ft behind a 1.3 ft stand | from the rows above | REF-011 estimate 3.0 → **3.2 ft** | High |
| Columns vs customer face | no column drawn in A011, A012, A101 or the S201 foundation plan; V5 columns y 19.6–20.4 | V5 (Med) vs A901 9'-0" | columns centred on the face line (non-structural) | Med |
| East back counter | 2.0 ft deep | A011 2744 x 45.19–47.19, y 2.08–14.24 (south-anchored) | x 44.99–46.99 on the existing wall line | Med |
| East "POS" box | schematic, white-filled label box | A011 5020 x 42.21–43.99; A012 5377 x 41.12–43.62 (1.2–1.6 ft to the jar wall) | not usable as the counter line | — |
| **GAP-130 aisle** | 4.5 ft counter to back counter (the south-run millwork), 2'-6" top | derived from the rows above | counter x 37.99–40.49, 3.2 ft behind the stands | Med |
| Entry pair | 6'-0", hinged at both outer jambs, swings out | A011 2895–2904: hinges y 7.39 / 13.40 south-anchored, i.e. 8.89 ft from the north face | y 8.9–14.9 (graybox 12.5–18.5) | High (size) / Med (frame) |
| Retail east exit | 3'-0" leaf, hinge N, swings out | A011 wall gap y 21.52–24.78 (south-anchored) | y 21.65–24.65 | Med |
| Parking | west stall row 18.2 ft deep at 9.1 ft pitch, 24.3 ft drive aisle, 8.0 ft building walk | G000 key plan drawing 29, scaled 3.75 pt/ft from the building outline (180 × 288.6 pt) | stall heads x −32.7 | Med |
| HUB east counter | no HUB furniture on A011, A012 or A101 | hub_R1C4 perspective | about 20 ft, y 52–72 | Med (position) / Low (length) |
| Door swings | arcs and leaves for every leaf | A011 vector (e.g. the office→HUB 2 arc 4360 hinges at (7.56, 46.44) with R 3.0) | DOORS.json `audit` | Med–High |
