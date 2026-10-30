# PROC-005 handoff

## Fix wave for REVIEW-PROC5 (2026-10-30), branch `claude/elated-satoshi-3a4844`
This branch merges slice 1 (`worktree-agent-ac7414483b9f8bb4a` @ e9f8173) and then main.

Per-family worker notes are in `Docs/Handoffs/PROC-005-fixwave/`. Each one holds the change log, the tri table, the GAP rows and DEC-047 questions.

| Finding | Fix |
|---|---|
| 1 DEC-084 visual bar | **Infra:** `proctex.py` makes 18 tileable 2K PBR finish sets: BaseColor/Normal/HDRP Mask, 2048–20480 px/m, in `UnityProject/Assets/_Game/Art/Procedural/Textures/` (LFS, byte-identical reruns). It also adds a per-vertex `Wear` attribute (edge wear + grime), a manifest `finishes` block and Eevee contact sheets (`PROC_<gen>_contact_sheet.jpg`, 4 tiles: 3/4, front, close-up, LODn). **Families:** all 8 non-wire families rebuilt at LOD0 with real construction: bevels, seams and reveals, hardware, hems, gaskets, toe kicks, electronics detail. Tri counts are guides under DEC-114. |
| 2 register mapping | `register_counter_run` now models RF `Counter_Register_North` (10/9/8), `_EastReturn` (12/11, GAP-130), `_South` (7,2,3,4,5,6, GAP-129) and `_SouthReturn`, per RI §1.5 rows 98/101. LegA/LegB were dropped. Station anchors come from RF POS + SCENE_ANCHORS. |
| 3 phantom deli counter | `DeliCounter_LegA/LegB` were dropped, with their FBX, Unity copy, validation file and manifest entries. |
| 4 jar-wall depth/fittings | Depth is RF 2.1 ft (0.64 m); `rf` = RF ids; the TI showcase pitch is gone (GAP-113). South wall: open bins (GAP-PROC-25). Walnut drawers on North only. East: arched bays + backlit teal (GAP-PROC-26). |
| 5 mop bucket | DEC-079 citation removed. The bucket is a labelled GAP-PROC-30 placeholder, and every janitor colour and material is GAP neutral grey. |
| 6 GAP-106 mis-cite | Removed from params and from GAP-PROC-15. The stray GAP-107 citation is gone too. |
| 7/8 minor cites | Every size, count, colour and finish now has an `_src` or GAP, covered by new rows GAP-PROC-22..39 in KNOWN_GAPS. The backsplash height is GAP-PROC-19. Grab-bar depth stays 3 in, with a `_note`. Wire-shelving counts are cited or GAP-PROC-29; their FBX are byte-identical. |

**Validation:**
- All 92 manifest assets pass (`blender.ps1 <gen>` for all 9 families), and `tests/test_validation.py` passes.
- Determinism: a full rerun of all 9 families gave the same `export_sha256` for every asset as the workers' runs.
- Jar, fill and packaged-goods manifest entries are unchanged.

**LOD0 tris:**

| Family | LOD0 tris |
|---|---|
| register station | 0.5–7.3k |
| counters | 1.2–11.0k |
| deli walls | 8.1–64.1k |
| cooler | 3.7–15.2k |
| office | 3.5–10.6k |
| break room | 0.14–15.0k |
| restroom | 0.7–4.3k |
| janitor | 1.5–8.7k |
| wire | 27.9–71.2k |

**Not done; owed with a Unity editor slot (none was free; the Hub said Blender + validation only):**
- the Unity import check and EditMode run (`studio.ps1`);
- `.meta` files for every Fixtures FBX (WireShelving included) and for the textures (Normal type, sRGB off for Mask);
- an HDRP material builder reading manifest `finishes` + `finishes.json`;
- the `to_unity`/BoxCollider EditMode test (item 12 below).

**Known limits:**
- Box-projection UVs stay until PROC-007 (DEC-097).
- Wood grain follows world X, so it runs sideways on cabinet doors.
- Some acrylic and glass renders near-opaque in Eevee previews.
- The Board assets are flat framed panels, because what is pinned to them is unrecorded (GAP-PROC-34).

### Questions for Nolan (through the Hub); full DEC-047 detail is in the fixwave notes
1. **Registers:**
   - counter-top colour (TI white quartz vs black stone in the stills, GAP-PROC-23);
   - the keyboard has no room in front of the monitor at the RF slot;
   - the finish of the East/South return faces (GAP-PROC-24).
2. **Deli walls:**
   - is there a third shelf board on South?
   - East tier count (GAP-133);
   - are North/South backlit?
   - does South's "wire bins" mean bins in the counter or the chrome rack beside it (GAP-PROC-25)?
   - does the walnut-drawer photo (DEC-043) show North?
3. **Cooler/janitor/wire:**
   - cooler shelf count (5 est.);
   - BOH south rack: one 5.3 ft section or 4-ft sections (DEC-088)?
   - does a mop bucket exist, and what colour is it?
   - break-room fridge colour.
4. **Office:**
   - worktable undershelf: there is none in wall2_R3C3 (GAP-PROC-33);
   - standing-desk colour;
   - tall-cabinet doors;
   - desk frames.
5. **Break room:**
   - lunch-table finish;
   - mini-hoop colours;
   - bulletin board look;
   - coat-hook count;
   - locker body colour.
6. **Restroom:**
   - accessory finishes (GAP-PROC-37);
   - storage-cabinet shelves and doors (GAP-PROC-38);
   - TP dispenser form (GAP-PROC-39);
   - toilet seat colour.

---

## Slice 1 handoff (superseded where the fix wave says so)

**Branch:** `worktree-agent-ac7414483b9f8bb4a`. It merges `claude/clever-lamport-837e7f` (core 4ef04ae + WIP 87807ad) and `main` at e0fc82c (IMP-003 R3b–R6 sections, DEC-111).

## Commits (one per family)
| Commit | Family | Checklist |
|---|---|---|
| 4ef04ae | core slice | C1–C11, Q0.5 |
| 102f126 | wire shelving: fork sweep axes, LOD3 extents, race ≤ collar; 8 RF racks | C12, W1–W8, J2 |
| c1fdf71 | register station: 7 unbranded POS props, no cash drawer | R1–R5 |
| 4070f60 | register counter run: 2 L legs to TI §6.4, DEC-039 anchors | RC1–RC5 |
| 3c4119e | deli: jar walls N/S/E + deli counter legs | D1–D5 |
| 34509ce | cooler + 2 fridges | K1–K5 |
| f824a1f | office: 10 RF assets | O1–O8 |
| 744d24d | break room: 17 RF assets | B1–B5 |
| be8d185 | restroom: 13 assets | T1–T7 |
| e2db8c4 | janitor closet: 3 assets | J1, J3 |
| fcf5aff (+ this) | GAP-PROC-14..21 in KNOWN_GAPS; PP "Fixture families" section | P1–P6 |

Every family has `Docs/Assets/Specs/PROC_<generator>_contact_sheet.png`. The checklist has a "PROC-005 done" note per family.

## Validation (every family)
- `blender.ps1` validation passes, with the opt-in checks on.
- Two runs give byte-identical FBX (sha256).
- Every existing manifest entry is unchanged (jar/fill/packaged-goods `export_sha256`, checked by a manifest diff per commit). Only new assets were added.
- FBX copies are in `UnityProject/Assets/_Game/Art/Procedural/Fixtures/<Family>/` and have no `.meta` yet.
- Not run: the Unity import check and the EditMode test, because no editor slot was available.

## LOD0 tris vs the DEC-084 guide
- Wire racks are inside the guide: 27.9–71.2k (fixture 20–80k).
- Everything else is below the lower guide, and validation warns. Values are given in each checklist note and in the PP table:
  - register props 0.4–7.3k;
  - counters 1.8–4.5k;
  - deli 0.2–4.6k;
  - cooler 7.8k, fridges 0.9–1.6k;
  - office 0.1–3.2k;
  - break room 0.1–2.3k;
  - restroom 0.1–0.8k;
  - janitor 0.3–1.0k.
- I added only real detail. See question 1.

## Left, in order
1. **§12 architecture kit** (A1–A7). Door hardware per DEC-110: push bars only on emergency exits and the delivery door, levers on every other door.
2. **§13 exterior** (E1–E3).
3. **§14 ladder** (L1–L2).
4. **§15 display cases** (V1–V3). The register run already references `PROC_DisplayCase_Countertop` via `display_case_slot`.
5. **§16 clutter** (X1–X5, plus the wire-rack bins/trays and the JC rack contents moved here).
6. **§17 arranger** (H1–H4, with GAME-004). H2 inner shelf anchors are already done in `wire_shelving` and `register_station`.
7. **§18 labels** (N1–N4).
8. **§19 materials** (M1–M4).
9. **§20 ID stand / bags / signs** (I1–I3).
10. **Q0.3 / Q0.4 / Q0.6.** Q0.2 UVs are PROC-007 (DEC-097), so the current layout is kept.
11. **R3b, R4, R5, R6** (DEC-111). Skip the rejected items: cash tray, vehicles, R4 wardrobe/hair/gloves (PROC-008/009, ASSET-005..007). Re-enable the round-6-disabled families where our docs confirm them.
12. **Unity import check:**
    - an EditMode test for the `to_unity` X negation and the BoxCollider placement from `collision_boxes`;
    - generate the `.meta` files;
    - a frame-budget check per room (Q0.6).

## Questions for the lead (pipeline/ART, not for Nolan)
1. **DEC-084 lower guide on small props and flat fixtures.** Examples: a receipt printer at 5k, a plywood-front counter at 30k, a plain black cabinet (DEC-051 Q9) at 20k. Meeting these needs invented geometry.
   - Options: per-family `tri_guide.lod0_min` (for example 1k for countertop electronics and plain boxes), or carry the detail in Q0.3 normal maps.
   - Placeholder meanwhile: real-detail tris, with the warnings.
2. **Register leg mapping (ART, DEC-039 / GAP-106).**
   - Draft: LegA 22 ft run holds 7,2,3,4,5,6,12,11; LegB 9.5 ft return holds 10,9,8.
   - Measured from: RI §1.5 L bbox 20.0–42.0 × 7.0–19.0 ft and the TI §6.4 2'-6" top depth.
   - It is a params edit if ART maps it differently.
   - The deli L split is also a draft: 20.2 ft + 4.7 ft at the west end, depth 2.5 ft. Measured from RI §1.5 bbox 14.0–34.2 × 18.0–25.2 ft. Depth and height are not in TI (GAP-113).
3. **Heights that exceed the RF row.**
   - Counter backsplash +4 in (TI §6.4), sink gooseneck +0.35 m, mop-sink splash guards +0.3 m, register-counter grommet lip +1.5 mm.
   - Measured from: RF rows plus TI §6.4/§6.6.
   - Fine for placement? The RF h is kept as the counter/rim/basin height, and `_note` records the excess.
4. **RF rows that include soft goods.** `Hooks_Coats` (2.5 × 0.8 × 5.5 ft) includes the hanging coats. I generated the rail only (0.76 × 0.08 × 0.12 m). Is this OK, or does ART want draped coats?
5. **Uppers_East is skipped.** RF marks it Low and CCTV shows uppers on the north run only.

## Questions for Nolan (through the Hub)
None. Per DEC-105 and DEC-110 I searched:
- `DECISIONS.md` (DEC-039/043/047/050/051/062/068/079/084/086/088/090);
- `KNOWN_GAPS.md` (GAP-PROC rows, GAP-106..113/126/127);
- `REFERENCES_INDEX.md` §1.5, §2.2, §2.4, §6.4, §6.6;
- `ROOM_FIXTURES.json` (every row used);
- the IMP-003 handoff.

Every open size is a GAP param, and the open mappings are ART's.
