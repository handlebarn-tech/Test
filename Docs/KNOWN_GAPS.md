# KNOWN GAPS

Unknowns stay visible here instead of becoming invented facts. Format: `GAP-### | area | unknown | confidence of current placeholder | replacement path`

Seeded from MASTER_PLAN §20–21; REF-001 and MIG-001 extend this file.

- GAP-001 | building | exact ceiling height/grid | none | measure from CCTV/photos (REF-001) or ask user
- GAP-002 | building | exact fixture dimensions not on floor plan | none | photo scale estimation (REF-001)
- GAP-003 | game | original Three.js game loop/systems | n/a (source unavailable) | GAMEPLAY_SIMULATION_SPEC is authoritative

## REF-001 (see `Docs/REFERENCES_INDEX.md`)
- GAP-101 | building | floor plan is "Working Plan V5, not for construction"; fixtures/doors are "approximate"; original RSP A011/A013 sheets not in repo | Med (fixtures) / High (room shells) | obtain the A011/A013 PDFs or a site tape-measure pass
- GAP-102 | building | which of FOH/BOH is 163 vs 180 SF (drawn 215 / 173 SF) | Low | user confirmation
- GAP-103 | building | JC corner within break room and true size (drawn 3×3 = 9 SF vs printed 19.19 SF) | Low | user confirmation / photo
- GAP-104 | building | wall thickness; interior door widths/heights (plan arcs 1.2–1.8 ft are schematic) | none (use 3'-0"×7'-0" labelled convention; exception, ART-001: the two vestibule doors (to FOH, BOH) use the full 2.2 ft vestibule side because 3'-0" does not fit the drawn 3.0 × 2.2 vestibule) | measure on site
- GAP-105 | cctv | CLOSED by REF-002: Nolan's HUB wall (DEC-022) maps R4C3, R4C4, R5C3, R5C4 → HUB and R5C1, R5C2, R5C5 → HUB 2 (+1 new HUB view); see REFERENCES_INDEX §2.1. Residual: camera poses and which plan door each visible door is | Med (rooms) / Low (poses) | Nolan confirms left column = HUB 2 if ART needs certainty
- GAP-106 | building | north-wall order: CCTV R2C2/R2C4 show the video-wall TV west of the logo living wall; the plan puts the living wall west of the menu screen | Low | user confirmation; graybox follows the plan meanwhile. REF-003: the wide back-of-register still (= R2C4 camera) shows, left to right beyond the queue: video wall → logo living wall → DELI STYLE counter → jar walls; no new evidence on compass direction, still open
- GAP-107 | building | register numbering (Register 1) and exact station positions; plan says "up to 12", CCTV shows 3–4 per view. REF-002: the DEC-021 scale stand is found (one chrome wire stand per POS, staff side, REFERENCES_INDEX §2.2), so the fixture is resolved; numbering and station count stay open. REF-003: stand size/shelves/acrylic panel spec'd from Nolan's back-of-register stills (REFERENCES_INDEX §2.2: ≈1.6×1.3 ft, top ≈2.5 ft, 2 levels, one per POS to the staff's right of the monitor); 4 POS in the R2C4 view, ≥4 stands | Med (stand type, placement) / Low-Med (size) / Low (count) | Nolan: total POS count + numbering; a tape measure on one stand would make size High
- GAP-108 | building | counter heights (register, deli, display case) not measured anywhere | none (36–42" convention) | site measure
- GAP-109 | building | Restroom and JC have no CCTV or photo coverage (blind) | none | user photo or generic fit-out
- GAP-110 | building | HUB and HUB 2 interiors: CCTV only (8 HUB-wall tiles, 7 distinct views, REFERENCES_INDEX §2.1); no photo; plan positions of racks/desks are raster-read only | Med | photos or Nolan confirmation of rack layout
- GAP-111 | building | fixtures seen but not on the plan: two glass-door coolers (FOH, R4C1), "Fine Cannabis" neon and blue-lit counter fronts (photo 05), wood bench + planters by the entry (R2C2), merch garment rack (R3C2). REF-003: no new unplaced fixtures; adds customer-facing card terminals per POS and a black wire trash bin beside the stands (on the counter run, not plan items) | Low (position) | user to place on plan
- GAP-112 | building | EXIT label and emergency-exit swing are drawn orange (= position not confirmed) | Low | user confirmation
- GAP-113 | building | floor tile sizes, jar dimensions, arch height, pendant drop height not measurable from the sources | none | site measure / product spec
- GAP-114 | ui | LIVE_TFS_BUDTENDER_v7.11.4.md has behaviour only, no visual tokens (colours, fonts, layout) | none | screenshots of the live app

## MIG-001 (see `Docs/Reconstruction/`)
- GAP-201 | engine | the About page lists an "Energy" domain (L2108), but the code has none: domains are sedation, uplift, anxiety_relief, pain_inflammation, focus_cognitive, antimicrobial (L15042) | High (code wins) | use the code ids; ask the user only if the game must show the About labels
- GAP-202 | data | live per-store stock (Supabase `location_stock`) at any moment; golden cases use the master JSON `status` snapshot of 2026-10-29T19:13Z (77 in-stock batches) | Med | DATA-001 re-imports a newer master; regenerate goldens with the same harness
- GAP-203 | engine | real-world validity of every DB weight, BA scalar and threshold; the tool's accuracy has never been measured (TRACKER SCI-8) | n/a (heuristic by design) | keep the "matching heuristic, not pharmacology" framing; satisfaction stays a game model
- GAP-204 | pricing | tax rounding: code floors to $0.05 (`priceFloor` L21123) | Low | game POS rounds to nearest $0.05 (DEC-035); cards keep `priceFloor`; tool-side question stays with the TFS hub
- GAP-205 | engine | "multi-terpene synergy" / large interaction dataset (UNITY_MIGRATION_PLAN §7) does not exist in code; only clusters + CLUSTER_BONUS | High that it is absent | do not invent coefficients; design-only if ever wanted
- GAP-206 | engine | NEW defect candidate: `_sleepAsk` (L16086) matches `sleep|insomnia` but not "sleeping", so "trouble sleeping but gotta work at 6" drops the sedation request (golden X-15) | High (reproduced) | the game fixes it; relayed to the TFS tool project hub session on 2026-10-29 (read-only for us)
- GAP-207 | qa | goldens come from the engine's source lines run in a Node vm, not from the full page in a browser; DOM-free logic is verbatim, but the page's state setup is replicated by hand | Med-High | optional: compare against the tool's own `rank_compare.py` output when its hub next runs it on this inventory
- GAP-208 | ui | domain display scores saturate at 99 (anxiety/pain on most in-stock strains), so bars do not separate strains; ranking uses unclamped raw | High (observed) | parity first; a later design task may choose relative bars
- GAP-209 | engine | the About page claims "281 search patterns" (L2066); code has 287 INTENTS keys + 54 phrases + 10 negations + 8 fuzzy | High (code wins) | none needed
- GAP-210 | engine | v7.11.5 (unreleased, `dev/v7115`) changes MC-7, V73-NT5 and Tier 2 14 g $77; not live, so not in the goldens | Med | re-run goldens on v7.11.5 once it is deployed

## PROC-001 (see `Docs/Assets/Specs/PROC_PIPELINE.md`; values live in `Tools/Blender/params/*.json`)
- GAP-PROC-01 | asset | deli jar 0.15 × 0.15 × 0.28 m, 18 mm radius, 4 mm wall | Low (shape from REFERENCES_INDEX photos 01/07/11; photo 07 is the only size cue) | measure a jar on site, edit params, rerun
- GAP-PROC-02 | asset | jar lid 30 mm tall, 4 mm overhang, black | Low (lids visible, unmeasured) | site measure / photo
- GAP-PROC-03 | asset | jar label card 100 × 120 mm, 30 mm up | Low (white card in photo 07) | site measure / photo
- GAP-PROC-04 | asset | package box 65 × 25 × 100 mm, 20 mm lid | none (conventional carton) | real SKU dimensions
- GAP-PROC-05 | asset | pouch 100 × 150 mm, 40 mm gusset, 15 mm seal | none (conventional stand-up pouch) | real SKU dimensions
- GAP-PROC-06 | asset | package label rectangles | none | real packaging references
