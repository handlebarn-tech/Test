# REFERENCES INDEX (REF-001)

Canonical finder for every supplied reference. Originals under `References/` are immutable; derived files live in `References/Index/`.
Confidence: **High** = printed/vector value, **Med** = read from a vector drawing or clear image, **Low** = inference or convention.
Staff are described by attire/role only.

## 0. File inventory

| File | Type | What it is | Index section |
|---|---|---|---|
| `References/Floor Plan.pdf` | PDF, 6 pp (pp5–6 blank), Print-to-PDF, no text layer, vector shapes | "The Flower Shop Phoenix · Floor Plan", **Working Plan V5, not for construction**. Built from the RSP Architects A011/A013 sheets (read as text only), cameras and a walkthrough | §1 |
| `References/CCTV Camera Wall.png` | PNG 2048×1137, 5×5 tiles | Camera wall snapshot A (busy floor, overlay timestamps read 2012 = NVR clock, not a real date) | §2 |
| `References/CCTV Camera Wall 2.png` | PNG 2696×1462, 5×5 tiles | Camera wall snapshot B, same tile layout, higher resolution (use this one first) | §2 |
| `References/BAND_TFS Phoenix (NEW)_…/…_01..13.jpeg` | 13 JPEG 1280×960, body-cam style, EXIF 2026-03-16..20 | Eye-level store/staff snapshots | §3 |
| `References/CCTV HUB Wall 2026-10-29.webp` | WEBP 2000×564, 2×4 tiles | HUB/HUB 2 camera wall supplied by Nolan 2026-10-29 (DEC-022). Nolan: "First room on left two pictures, the rest are in the bigger side of the hub... It's mostly misc storage." | §2.1 |
| `References/CCTV Register Back Center East 2026-10-29.webp` | WEBP 1866×755, NVR playback, 2 feeds | "Back Of Register center" (close) + "Back Of Register East", 11:40:16, 1/21/2026. Supplied by Nolan for the scale stand (DEC-026) | §2.2 |
| `References/CCTV Register Back Center Wide 2026-10-29.webp` | WEBP 1134×640, 1 feed | "Back Of Register center", 16:48:53, wide. **Same camera and framing as wall tile R2C4** (DEC-026) | §2.2 |
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
| FOH (floor restock) | "163 or 180" | 23.69–36.49 | 29.5–46.3 | 12.80 × 16.80 | 215 SF drawn. Which of 163/180 belongs to FOH vs BOH is open (GAP-102) |
| BOH (backstock) | "163 or 180" | 36.90–47.19 | 29.5–46.3 | 10.29 × 16.80 | 173 SF drawn |
| HUB (sheet: Product Storage) | 818.53 | 0–28.29 | 46.8–76.03 | 28.29 × 29.24 | deliveries · general storage · entered from office |
| HUB 2 (sheet: Product Storage) | 541.34 | 28.70–47.19 | 46.8–76.03 | 18.49 × 29.24 | only via HUB connecting door; no access from FOH/BOH |
| *Arch vestibule (unnamed, "white wall")* | — | 35.2–38.2 | 29.5–31.7 | 3.0 × 2.2 | small lobby behind the east arch, with doors to FOH and BOH |
| Net / gross | 3,467.77 / 3,590 (assessor) | | | | the plan says walls ≈ 122 SF |

### 1.4 Doors / openings (from the vector plan)

| Opening | Location (ft) | Drawn width | Conf. |
|---|---|---|---|
| ENTRY (customer, double door) | west wall x=0, y 11.0–20.0 | 9.0 opening, two 4.0 leaves | Med |
| EXIT label (orange = position not confirmed) | west wall, just north of entry | — | Low |
| EMERGENCY EXIT | east wall x=47.19, y 20.5–24.0 | 3.5 (swing drawn orange = unconfirmed) | Low |
| West arch (Retail→Hall) | y≈29.25, x 9.10–12.91 | 3.81 | Med |
| East arch (Retail→vestibule) | y≈29.25, x 35.21–38.21 | 3.0 | Med |
| Hall→Restroom door | x≈8.2, y 31.5–33.3 | 1.8 symbol | Low (schematic) |
| Hall→Break room door | x≈13.7, y 31.5–33.3 | 1.8 symbol | Low |
| Hall→Office door | y≈36.1, x 9.5–11.3 | 1.8 symbol | Low |
| Vestibule→FOH door | arc at x 34.0–35.2, y 30.6 | 1.2 symbol | Low |
| Vestibule→BOH door | arc at x 38.2–39.4, y 30.6 | 1.2 symbol | Low |
| Office→HUB door | y≈46.3, x 4.0–5.8 | 1.8 symbol | Low |
| EXT. DELIVERY (employees only) | west wall x=0, y 47.8–51.2 | 3.4 | Med |
| Door to HUB 2 | wall x≈28.3–28.7, y 48.6–50.6 | 2.0 | Med |

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
| REGISTERS (up to 12) — L counter | 20.0–42.0 | 7.0–19.0 (bbox) | L: north run along y≈7–8.x, return leg down the east side to y=19 |
| display case (on register counter) | 38.0–39.4 | 7.4–8.8 | 1.4 × 1.4 |
| globe pendants over register run | 6 circles, centres x 23.0, 26.0, 29.0, 32.0, 35.0, 38.0; y 11.0 | Ø0.8 | 3.0 ft pitch |
| DELI COUNTER — L counter | 14.0–34.2 | 18.0–25.2 (bbox) | L |
| globe pendants, deli west end | centres (15.0, 26.2), (17.0, 26.2) | Ø0.8 | |
| two white columns | x≈19.0 and x≈35.0 | y 19.6–20.4 | ≈0.8 sq |
| queue stanchion lines (dashed, raster-read) | x ≈ 6, 9, 12, 15 | y ≈ 11–19.5 | 4 lanes, Low-Med |
| ATM | 1.2–3.4 | 25.8–27.6 | 2.2 × 1.8 |
| deli flower jar wall (south, between arches) | 13.5–34.7 | 27.6–28.8 | 21.2 × 1.2 |
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
| R2C3 | Register run close | 3–4 POS stations, black counter with open shelves below, scale carts, jar wall with mint/teal backlit shelving on the side wall, yellow wet-floor sign, "HIGH TIDE" stool/seat back | Retail (registers) | High |
| R2C4 | Register run, wider (camera name "Back Of Register center", REF-003) | 3 POS + spare monitor, kraft order bags, globe pendant clusters, DELI STYLE counter behind | Retail (registers) | High |
| R2C5 | Elevated view along register L toward deli/queue | register L end with trash bin, black cabinet end, jar wall on right, entry/queue far left | Retail (NE register L) | Med |
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
| HUB | doors: green door with round logo; black door with yellow sign | 2 | HUB R1C4, R1C2 | Med (exists) / Low (which plan door) |
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
| JC | ✔ | — | — | **BLIND** |
| Restroom | ✔ | — | — | **BLIND** |
| FOH | ✔ | R4C1 | — | CCTV only |
| BOH | ✔ | R4C2 | — | CCTV only |
| Arch vestibule (unnamed) | ✔ | edges in R4C1/R4C2 | — | partial |
| HUB | ✔ | R4C3, R4C4, R5C3, R5C4 + HUB wall R1C2–C4, R2C2, R2C3 (Med) | — | CCTV only (§2.1); no photo |
| HUB 2 | ✔ | R5C1, R5C2, R5C5 = HUB wall R1C1, R2C1, R2C4 (Med) | — | CCTV only (§2.1); no photo |
| Exterior | (doors only) | R1C1–C5, R3C1 | — | CCTV only, night |

## 5. Scale cues for the graybox

| Cue | Value | Method | Conf. |
|---|---|---|---|
| Building / room shells | §1.3 table | printed dims + vector scale 5.6095 pt/ft | High |
| Fixture footprints | §1.5 table | vector plan ("approximate" per legend) | Med |
| Entry opening | 9.0 ft (2 × 4.0 leaves) | vector arcs | Med |
| Delivery door / emergency exit / HUB 2 door | 3.4 / 3.5 / 2.0 ft | vector arcs | Med / Low / Med |
| Interior door arcs (1.2–1.8 ft) | **not real widths** | the symbols are smaller than any code-compliant door. Use a standard 3'-0" × 7'-0" commercial door as a **labelled convention** until measured | Low |
| Arch openings | 3.81 ft (west), 3.0 ft (east) | vector | Med. Height unknown; photo 06 shows the arch top clearly above a standing adult |
| Counter height | none measured | CCTV/photos show the counter top at standing hip height. A 36–42" retail counter is an **industry convention, not a measurement** | Low |
| Ceiling height / grid | none | retail has dark slatted baffles (photos 01/05/10), not a T-bar grid. BOH ceilings are white. No height in any source | none (GAP-001) |
| Floor tiles | white marble-look large-format (retail field), black/white or brown/white geometric cement tile (counter zones, hall, vestibule), concrete (FOH/BOH), dark gray large-format tile (rack rooms) | visual | Med (finish) / none (tile size) |
| Wall thickness | 0.4–0.5 ft drawn gaps | vector | Low (drafting gap, not a spec) |
| Pendant pitch | 3.0 ft, 6 over registers | vector | Med |
| Register scale stand | ≈1.6 × 1.3 ft footprint, top ≈2.5 ft (≈0.7–1.2 ft below the counter top), 2 levels, acrylic panel ≈0.8–1.2 ft tall on the counter-side edge | keyboard (≈17.5 in convention) in REF-003 stills (§2.2) | Low-Med |
| HUB wire rack bay | ≈4 × 2 ft, ≈6–7 ft tall | about 4 bays span half the 28.3-ft HUB width in HUB R1C3; matches the common chrome-wire bay size | Low (convention) |
