# Sales-floor layout audit (REF-011, playtest 1, DEC-096)

This audit compares the current graybox (`UnityProject/Assets/_Game/Art/Graybox/graybox_layout.json`, read-only) with the evidence, room by room.
- Coordinates use the REFERENCES_INDEX §1.2 frame, in feet.
- The corrected layout is stored as data in `Docs/Reference/ROOM_FIXTURES.json` rev7 and `Docs/Reference/SCENE_ANCHORS.json`. The summary is in REFERENCES_INDEX §8.
- "BAND_NN" is the BAND photo `…_NN.jpeg`. "wide/East still" are the 2026-10-29 "Back Of Register" CCTV stills.
- Raw CCTV and photos were viewed only; nothing new is committed.

## Registers

| # | Item | Graybox now | Evidence says | Source (file + tile/crop) | Fix |
|---|---|---|---|---|---|
| R1 | South run (reg 7,2,3,4,5,6) staff room | `FX_DeliCounter_L` long leg y 23.2–25.2; stations y 25.2 staff S; `FX_DeliJarWall_S` front y 27.6 → **2.4 ft** from staff edge to jar wall, **1.1 ft** behind the 1.3-ft stand | Staff aisle behind the stands is **3–4 ft** and two staff pass; the jar wall has a back counter under its shelves | BAND_10 (rotate 90° cw; TL-2 8" grout lines counted at the aisle floor); Photo Deli Jar Wall; TI A940 base cabinet 2'-1" | Long leg → y 20.4–22.6; stations y 22.6; stand 22.6–23.9; aisle 3.0 ft; back counter 26.9–29.0 (GAP-129) |
| R2 | Which counter the south run is | graybox calls it the deli counter; register cameras placed north of the counters looking south | "Back Of Register" cameras are **behind the south run looking north** (living wall + video wall + entry on the left, north run with DELI STYLE wrap ahead, east jar wall on the right). R3C2 is behind the north run (display case) looking south | wide still, East still; wall2_R2C3, R2C4, R2C5, R3C2 | ROOM_FIXTURES `Counter_Register_South`; graybox cameras R2C3 (24, 13.5, yaw 50), R2C4 (30, 2.5, yaw 190), R2C5 (44.8, 1.6, yaw 235) should sit south of the south run facing N/NW |
| R3 | South return | `FX_DeliCounter_L` north arm x 32.2–34.2, y 18.0–23.2 | counter end with a black cabinet end and a trash bin, beside the east white column | wall2_R2C5 | Shorten to y 18.0–20.4 to meet the moved leg |
| R4 | South station spacing | x 15.5…30.5 at 3.0 ft; station 05 (x 18.5) has its customer spot on the west column (x 18.6–19.4) | monitor pitch ≈3–3.5 ft | wide still (monitor centres vs. stand width 1.6 ft) | x 31.0 / 27.8 / 24.6 / 21.4 / 17.8 / 14.8, so the column falls between 05 and 04 |
| R5 | South run vs queue | stanchion field x 6–15, y 11–19.7 was 3.5 ft from the counter | (consequence of R1) | V5 plan | Field now ends 0.7 ft from the counter; station 06's customer spot (14.8, 19.2) is inside the x 12–15 lane. ART/Gameplay shorten the lanes or open the field's south end (GAP-129) |
| R6 | East return (reg 12, 11) | x 39.8–42.0, staff E → 2.3 ft to `FX_JarWall_E` front (1.6 ft counting a back counter) | east jar wall has a counter under arched backlit shelves | BAND_11; wall2_R2C3; wide still | Move to x 38.4–40.6; north leg ends at 40.6 (GAP-130, Low) |
| R7 | North run (reg 10, 9, 8) | y 7.0–9.2, staff N, 4.3 ft to jar-wall front | north run has staff behind it, between it and its jar wall | wall2_R3C2, wide still | Keep; with a 2.1-ft back counter it still has 3.4 ft |
| R8 | Operator spot | `playerOff` 1.0 ft off the staff edge | operator works in front of the monitor; the stand is beside, to the staff's right | REF-003 §2.2 | Keep 1.0 ft; `Anchor_Register_<n>_Operator` |
| R9 | Station kit / small items | one identical kit per station | spray bottle hangs from a stand, a trash can stands behind a stand; DEC-104: small items never uniform between stations | BAND_10; wide_stand_A; DEC-096/104 | Per-station small trash bins `Trash_Small_POS_<n>` (Low); vary the kit per station |
| R10 | Big trash bins | none | DEC-104: big bins spread across the floor; one at the south return end | wall2_R2C5; DEC-104 | `Trash_Big_SouthReturnEnd` (Low), `_West_ATM`, `_East_Sink` (Low, GAP-134) |
| R11 | ID-check stand | anchor-only `TEMP_Anchor_CheckInDesk` (3.0, 13.0) in code | stand directly left inside the entrance, ID scanner with green light, no second door after it | DEC-048, DEC-103; wide still left edge (guard by the glass doors) | `IDCheck_Stand` (1.5–3.5, 10.25–11.75), `IDCheck_Scanner`; `Anchor_CheckIn` (2.5, 11.0) |

## HUB / HUB 2

| # | Item | Graybox now | Evidence says | Source | Fix |
|---|---|---|---|---|---|
| H1 | HUB desk | `FX_HUB_Desks` x 20.2–32.2, y 70–74.4 (south) | R1C4 looks south (green SE exit at its far left), so the desk + chair in its foreground are at the **north** end | hub_R1C4; DEC-030 | `HUB/Desk_Computer` x 23–28, y 47.2–49.7 (Low, GAP-132) |
| H2 | HUB north chrome run | `FX_HUB_RackRun_N` x 21.2–39.2, y 47–49 | the north end holds the desk; perimeter racks are along the far (south) wall | hub_R1C4, hub_R1C3 | `HUB/RackRun_South` y 73.8–75.8 (Low) |
| H3 | HUB east wall | `FX_HUB_RackRun_W` chrome run x 44.2–45.7, y 56–73 | a long dark counter/bench along the east wall, with blue and red rolling carts near it | hub_R1C4, hub_R2C3 | `HUB/Counter_Long_EastWall` (Low) |
| H4 | HUB props | none | yellow tote stack + hand truck, black crates, blue/red carts | hub_R2C2, R1C4 | props for ART/Assets (not rows) |
| H5 | HUB floors | one `Floor_Hub` for both rooms | HUB dark large-format tile; HUB 2 grey square tile | hub_R1C1, R1C3 | split the floor material |
| H6 | HUB 2 camera R5C1 pose | (0.69, 75.4) yaw 25 | connecting door at the far left, copier left foreground → looks east (yaw ≈75) | hub_R1C1 | camera pose only |
| H7 | HUB 2 cabinets | `FX_HUB2_Cabinets` on the office wall | DEC-079 backstock cabinets "in the HUB against the office wall"; only HUB 2 borders the office (A011) | DEC-079; A011 | keep; row `HUB2/Cabinets_Storage_OfficeWall` with contents (GAP-132) |
| H8 | SE exit, HUB↔HUB 2 door, delivery door, room naming | as A011 | agrees | A011, DEC-030 | none |
| H9 | Black door with yellow sign (R1C2) | not modelled | unconfirmed (DEC-030) | — | none |

## Deli walls and shelves

| # | Item | Graybox now | Evidence says | Source | Fix |
|---|---|---|---|---|---|
| D1 | Count | 3 blocks, but jars (`jarSlots`) only on N and E; S is a solid block | **three** stocked deli walls, one behind each register run | wall2_R2C3/R2C4, wide still (N); BAND_11, R2C3 (E); BAND_10, BAND_01/06, R3C2 (S) | jarSlots on all three; rows `DeliJarWall_North/East/South` |
| D2 | Depth | 1.2 ft (plan) | back counter (≈2'-1") + 2 shelf tiers; jars also on the counter | BAND_10, BAND_11, Photo Deli Jar Wall; TI A940 | N y 0.2–2.3, E x 44.9–46.99, S y 26.9–29.0 (Low depth, GAP-133) |
| D3 | Fill | every slot full | top tier ≈85–95 %, middle ≈50–60 %, counter row ≈30–40 %; jar levels 30–80 % | Photo Deli Jar Wall, BAND_10/11/01 | stocking note REFERENCES_INDEX §8.4 (generator params unchanged) |

## REF-013: drawing measurements (DEC-110)
Nolan rejected the REF-011 layout questions: "You literally have the floor plan and exact dimensions". REF-013 measured the vector drawings with PyMuPDF.
- Sources: A011 and A012 (17.987 pt/ft from their own dimension ticks), A901 detail 17 "POS enlarged plan" (printed dims) and the G000 key plan.
- The full measurement table, with drawing ids, is in REFERENCES_INDEX §8.5.
- What changed against the rows above:

| # | Was (REF-011) | Now (REF-013) | Source | Conf. |
|---|---|---|---|---|
| R1 | South counter y 20.4–22.6 (2.2 deep), 3.0 ft aisle behind the stands, back counter 26.9–29.0 | counter y 20.0–22.5 (2'-6"), stand 22.5–23.8, **3.2 ft** clear to the back counter at 27.0–29.0 (2'-0"), x 15.19–34.42 | A901 det. 17 printed 9'-0" + 2'-6"; A011/A012 vectors | High (y) |
| R3 | South return x 32.2–34.2, y 18.0–20.4 | removed: no drawing shows a north arm. A 2'-6" **west** return (x 15.28–17.78, y 22.5–27.0) closes the staff aisle | A011, A012, A901 det. 17 | Med |
| R4 | stations x 31.0…14.8 | x 36.4 / 33.2 / 30.0 / 26.8 / 23.6 / 20.4 (07…06): 06 cannot sit west of the west return; every customer spot is ≥ 1.0 ft from both columns | run extent (vector) + wide-still pitch | Low-Med (GAP-131) |
| R5 | stanchion field 0.7 ft from the counter; station 06's customer spot inside the lane | station 06's spot at x 20.4 is clear of the field (x ≤ 15); the field ends 0.3 ft from the counter's NW corner, which no path uses | — | Med |
| R6 | East return x 38.4–40.6, 3.0 ft aisle | x 37.99–40.49, y 9.2–20.0 (meets the south run); 3.2 ft behind the stands; east back counter 2.0 ft deep | A011/A012 vectors + the south-run millwork standard (the A011/A012 east "POS" boxes are schematic) | Med (GAP-130) |
| R11 | ID stand y 10.25–11.75 (entry 12.5–18.5) | entry pair at y 8.9–14.9 (A011); stand y 7.15–8.65, directly left inside | A011 vector, DEC-048 | Med |
| Spawn | (−4, 14) / (−4, 17), side unknown | (−32.7, 11.9) / (−32.7, 14.9): the west parking row's stall heads opposite the door | G000 key plan vector, DEC-110 W4 | Med |
| H1/H3/H7 | HUB desk north, east counter, cabinets in HUB 2: questions | confirmed (DEC-110 W3); counter ≈ 20 ft (hub_R1C4: no HUB furniture is drawn); cabinets in HUB 2 (A011: the only room on the office wall) | DEC-110, A011, hub_R1C4 | Med |

## Not changed / out of scope
- Office rows belong to REF-012.
- GAP-106 (video wall vs living-wall order) is still open and was not re-asked (DEC-105).
- Main cleaning supplies live in the restroom storage cabinet (DEC-104). That row is not ours.
