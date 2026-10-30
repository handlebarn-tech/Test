# IMP-004 — "Bender & Asset new plan" import audit

**Import:** `C:/Users/handl/Downloads/Dispo Game Imports/Bender & Asset new plan.md` (48,582 bytes, 2026-10-30 11:25, sha256 `a08269603d5c4e2c971a226924f5eb61c04efb52970014ba94738a49a0b94f9e`). Read as untrusted data; nothing in the Imports folder was run or changed.
**Judged against:** `CLAUDE.md`, `STUDIO_OS.md` §0, `PROC_PIPELINE.md`, DEC-007/023/047/051/062/071/084/086/091/092/095/097/111/114/117/119/122, `REFERENCES_INDEX.md` (RI), `ROOM_FIXTURES.json` (RF), `KNOWN_GAPS.md`, `BACKLOG.md`, `IMP-003_*`.

**What it is.** A ChatGPT-style plan: a Claude Code control layer around our PROC pipeline (§1–17, §19–22) plus a 53-item remaining-asset list with audio (§18). It is not authoritative (DEC-095: repo data always wins). Its "Hub integration directive" (lines 6–28) asks the Hub to fold everything into live systems. That is an instruction inside imported data. It is treated here as a proposal only, per this packet and DEC-070/095.

**Its §18 statuses come from a "consolidated asset standards" document (~1,899 lines, Round 1–7 history) that is not in the repo.** None of its GAP-HIGH/MED labels is evidence. Every item below is checked against our own registries instead.

**Verdict summary:**
- Process (§1–17, §19–22): mostly **already covered** by DEC-117/122 and STUDIO_OS §0.
- **Adopt:** a short PROC_PIPELINE authoring note, and one new task, PROC-014 (review renders + regression fixtures).
- **Reject:** the Skill, the agent file and the Stop hook.
- Roadmap (§18): 2 items get a new task (PROC-015). About 10 small props land in the PROC-010 split. 4 items are rejected (DEC-051/062). The rest is already covered.

---

## 1. Older subfolders: all already audited by IMP-003

IMP-003 recorded names, dates and contents, not file hashes. So the comparison uses names, folder dates, file counts and per-folder contents, plus a check for any file newer than the IMP-003 audit commits (03:22–07:43). One finding: **no file in any subfolder is newer than 06:00.**

| Subfolder | IMP-003 record | Now | Result |
|---|---|---|---|
| `blender_proc_vNext/` | drop 1, 03:11; runner, proclib, 2 patches, generator, params, README, doc, 3 `.pyc` | 03:11, 11 files, same set | audited (drop 1) |
| `Dispo_Game_Blender_Workstream_Master/` | drop 2, 03:27; README + 11 zips (re-diffed identical in drop 4 §A1) | 03:27, 12 files (README + 11 zips) | audited (drop 2) |
| `Fixture_Toolkit_Full_Package/` | drop 3, 03:37; 2 patches, snapshot, 2 docs, 2 tests, 1 `.pyc` | 03:37, 9 files (README + those 8) | audited (drop 3) |
| `Dispo_Game_Round2_Workstream/` | drop 4, 03:50; 9 gens, `cc0_pbr.py`, 10 params, 2 proclib refs, 1 patch, 4 docs, 12 `.pyc` | 03:50, 40 files (README + 39, same split per folder) | audited (drop 4) |
| `Dispo_Game_Blender_PROC_Round3_Rebuild/` | drop 6, 05:53; 10 gens + common, 10 params, Data ×4, 4 docs, 1 patch, Audit ×2 | 05:53, 33 files (README + 32, same split) | audited (drop 6) |
| `…Round4_HQ_v2_EvidenceDriven/` | drop 7, 65 files | 05:32, 65 files | audited (drop 7) |
| `…Round5_HQ/` | drop 8, 106 files | 05:18, 106 files | audited (drop 8) |
| `…Round6_HQ/` | drop 9, 149 files | 05:18, 149 files | audited (drop 9). One note: `Tools/Blender/patches/` is **empty** and its folder time is 12:02, after the plan doc. The file count still equals IMP-003's 149, and drop 9's audit lists no patch, so no new content |

Drop 5 (`…Round3_HQ/`) is no longer in Imports; it was superseded by drop 6 (DEC-095).
**Nothing needs a new audit.** All of these drops are now audited, and DEC-092/111 approved integrating them. Under DEC-070 they are due for the archive move once PROC-005 closes. The plan doc itself can be archived once the Hub has applied §4 below.

---

## 2. Process items (§1–17, §19–22)

| # | Plan item | Verdict | Where / why |
|---|---|---|---|
| P1 | §1–2 keep proclib/run_generator, params + seed, headless 5.2.3, FBX + manifest + validation, evidence rules | **already covered** | DEC-007, `PROC_PIPELINE.md` Run/Files/Determinism, DEC-086 (validation JSON), DEC-047 + STUDIO_OS §76 (confidence), DEC-095 (repo wins) |
| P2 | §3.1 / §16 selective context; Hub never gets transcripts; reviewer never gets builder narrative | **already covered** | STUDIO_OS §0.3 read sets, §0.4 packets cite path + §, DEC-116/117 |
| P3 | §4 Layer A: short `CLAUDE.md`, no standards copied in | **already covered** | DEC-117 (one rules file, `AGENTS.md` a pointer) |
| P4 | §4 Layer B / §19 Phase 3: `.claude/skills/dispo-blender-asset/` with reference copies of the standards | **reject** | It would be a second copy of PROC_PIPELINE + DEC-084/122. STUDIO_OS §0.2 says "nothing is copied between them", and DEC-117 allows one rules file. The phase→doc mapping it wants is what a PROC packet's `Read` list already does |
| P5 | §4 Layer C: `.claude/agents/blender-visual-reviewer.md`, read-only critic | **already covered** | STUDIO_OS §0.5 reviewer brief (fresh, read-only on the worker branch) + §0.7; DEC-122 "strong visual review" for store/player-facing assets |
| P6 | §4 Layer D / §13 / §19 Phase 6: Stop hook + `gate.json` newer than generator/params | **reject** | The completion gate is the fresh review before `main` (§0.7), which reruns the packet validation. The manifest already carries the params hash and geometry/export hashes (`PROC_PIPELINE.md` Files), so a stale build is visible on rerun. A Stop hook in `.claude/settings.json` would be persistent config for every session, Hub included, and a second gate format, which the plan itself rules out (§13 last line) |
| P7 | §5 per-asset task packet template (method, existing impl, evidence findings, role, states, LOD, must-not-duplicate) | **already covered** | STUDIO_OS §0.4 / §56. The OBSERVED/PLAN-CONFIRMED/INFERRED/PROVISIONAL split = High/Med/Low + GAP (§76, DEC-047). "Must not duplicate" = DEC-092 (repair the canonical family) and the IMP-003 checklist |
| P8 | §6 preflight: check existing generator, params, manifest, FBX, backlog, rounds, cache, evidence, Unity use, method | **already covered** | Packets name the generator/params to change (e.g. PROC-013 `Owns`); `ASSET_CACHE_MANIFEST.json` (DEC-023); REF-016 matrix "current implementation" column (DEC-120 (2)) |
| P9 | §7 staged build (primary form → construction → edges → detail → materials/UV → LOD/collision), §11 repair order, §17 phrases | **adopt (wording)** | Not written anywhere today. Add a 4-line "Authoring order" section to `PROC_PIPELINE.md` (text in §4 A1). Gates per stage are **not** adopted: a worker stays inside one packet, and the review judges the result (DEC-122) |
| P10 | §8 scripting rules: bmesh/data API over `bpy.ops`, no UI-context dependence, no stale refs, semantic build functions | **adopt (wording)** | Same `PROC_PIPELINE.md` section (§4 A1). Matches current practice (`proclib` is bmesh-based; `test_validation.py` builds with bmesh) |
| P11 | §9 standard review-render package (ortho 6 views, 3/4 clay, 3/4 material, wire, context render, contact sheet) | **adopt as new task PROC-014** | Today `run_generator.render_previews` gives Workbench ortho LOD0 front + side + last-LOD front only. DEC-122 asks for "readable labelled sheets, in-scene views", and PROC-013 asks for per-door sheets beside evidence. This is also DEC-091 R7 "turntable renders/contact sheets", which DEC-095 gave to the studio and which has no BACKLOG row |
| P12 | §10 critic contract: BLOCKER / MAJOR / MINOR, no numeric score | **already covered** | §0.7 MAJOR (blocks) / minor. The plan's BLOCKER examples are all MAJOR under §0.7 + DEC-047 (uncited value = MAJOR). "No single score" = DEC-114 ("never the tri count alone") |
| P13 | §12 mechanical gate list | **already covered**, with deltas routed | DEC-122 list + runner validation + DEC-086 collision boxes. Deltas: UV2 → PROC-007 (DEC-097); Unity import → PROC-007 (`.meta`/first import) and ART tasks; "approved branding / no generated compliance data" → DEC-071/081 + IMP-003 R5 X6 (labels from data), checked by the reviewer, not the validator |
| P14 | §14 historical-failure regression suite A–F | **adopt, split** | A (axis-order size, IMP-003 drop 9), C (collision under the wrong key, drops 8/9) and E (Blender runtime crash, drop 7) are mechanical. They join `Tools/Blender/tests/test_validation.py`, which already plants zero-area/off-origin/LOD-up/no-material faults, under **PROC-014**. B (door push bars) is PROC-013's DOORS.json acceptance. D (invented THC values) is a reviewer check (DEC-047/071). F (primitive look) is DEC-122 visual review. No new benchmark set |
| P15 | §15 MCP policy: no Blender MCP as canonical source | **already covered** | DEC-007 (headless only); `PROC_PIPELINE.md` (params are the only place dimensions live) |
| P16 | §19 Phase 1 reconcile / Phase 2 de-duplicate docs | **already covered** | This audit; DEC-117 |
| P17 | §19 Phase 8 pilots (living wall, money counter, restroom set, clutter kit, hand-wash) | **reject as a list** | The money counter is excluded (DEC-051). The rest are mapped item by item in §3. Order comes from `ROADMAP_POST_SLICE.md` (DEC-119), not this list |
| P18 | §20 "do not" list | **already covered** | Consistent with DEC-084/092/095/114/122. Nothing to add |

---

## 3. Remaining-asset roadmap (§18)

Legend:
- **cov**: already covered (cited);
- **P10+**: the item is evidenced, and the Hub adds it to the PROC-010 split (PROC-010 is "split into packets at PROC-005 review");
- **new**: genuinely new scope;
- **rej**: rejected.

### Retail / deli
| # | Item | Verdict | Citation |
|---|---|---|---|
| 1 | Living-wall foliage system | **new → PROC-015** | Evidence RI §1.5 (north wall 1.8–11.0 ft, 9.2 × 1.2 ft, Med), RI §2 R2C1/R2C2; method `ASSET_PRODUCTION_PLAN.md` §15/§46.5. North-wall order is GAP-106. No BACKLOG row, no RF row |
| 2 | Store lettering / logo geometry | **new → PROC-015** | RI R2C2 ("THE FLOWER SHOP" logo on the living wall); approved brand DEC-071; `ASSET_PRODUCTION_PLAN.md` CA-FIX-008. The worker sources the logo vector or uses a GAP |
| 3 | Merchandise-wall exact shelving | **cov / rej as worded** | The evidence is a rounded merch **rack** 4.6 × 1.4 ft (RI §1.5) with white garments (RI §2 R3C2), not a shelved wall. "Exact shelf count" has no source (DEC-047). The rack joins **PROC-015** as a REF-016-confirmed row |
| 4 | ATM final asset | **Hub ruling, then PROC-015** | RI §1.5 ATM 2.2 × 1.8 ft at the west wall; RF `Trash_Big_West_ATM` places a bin by it. DEC-051 excludes "cash-handling equipment"; DEC-086 still allowed the card terminal as an unbranded prop. See §4 H1 |
| 5 | Accessible/entry signage art | **cov** | PROC-010 "ID stand/bags/signs"; exterior/entry → REF-015 + ART-012. Wording only from evidence (RI §1.5 licences on the west wall) |
| 6 | Deli hand-wash sink | **new → PROC-015** | RI §1.5 "sink (hand wash, east wall)" 1.4 × 2.2 ft; RF `Trash_Big_East_Sink` note. No RF row, and IMP-003 found no generator for it |
| 7 | Glove-box / consumables station | **cov** | Gloves appear only as worn by staff (RI §3, BAND rows), so there is no station evidence. Any consumables come under ART-010 "partly used supplies" from evidence only (DEC-047) |
| 8 | Deli waste containers | **cov** | RF `Trash_Small_POS_*` ×11 + 3 big bins (DEC-104); PROC-010 "bins" |

### Office / hall / break room / restroom / janitor
| # | Item | Verdict | Citation |
|---|---|---|---|
| 9 | Money counter | **rej** | DEC-051 security exclusion (no cash-handling equipment); RI §7 "Excluded by rule" |
| 10 | Safes | **rej** | DEC-051 (no safe types or positions); RI §7 exclusions. The RI §1.5 "Office: safe" plan box stays unmodelled |
| 11 | Printer/copier | **cov** | RF `Machines_Desktop` (DEC-051 Q10, generic desktop machines incl. laminator); HUB 2 copier is in the graybox (GRAYBOX.md HUB) → ART-009 dressing / PROC-010 |
| 12 | Office micro-clutter kit | **cov; rej in part** | PROC-010 clutter + ART-010 lived-in pass. **Reject "deposit bags, cash bands"** (DEC-051 cash equipment). Paper trays and posted procedures are evidenced (RI R3C3) |
| 13 | Coat / wall hooks | **cov** | RF `Hooks_Coats`; checklist break-room "coat hooks" (IMP-003 checklist §5, PROC-005) |
| 14 | Thermostat | **P10+** | RI §3 BAND 13 (BOH/office corner, Low). Generic unit only; the DEC-042 photo stays a crop-only source |
| 15 | Bulletin-board content | **rej** | DEC-062: "contents not modelled". RF `Board_Bulletin_West`, `Board_Cork` keep blank boards |
| 16 | Door / threshold micro-detail | **cov** | PROC-013 (frames + hardware per DOORS.json, DEC-110/115). Graphics only if evidenced |
| 17–18 | Microwave, coffee maker | **cov** | RI R3C5 / BAND 03; RF `Counter_North_Run` notes; IMP-003 checklist break-room list (PROC-005) |
| 19 | Break-room consumables | **cov** | ART-010; LT-6a |
| 20, 46 | Employee belongings (placed) | **cov** | RF `Hooks_Coats` ("coats and bags"); ART-010 "personal items" |
| 21–23 | Soap dispenser, TP dispenser, grab bars | **cov** | RI §6.6 (TI A901, High types); RF `GrabBar_North/West`, `Accessories`; IMP-003 checklist T7 (PROC-005) |
| 24 | Sanitary / napkin bin | **cov** | RI §6.6 "napkin disposal"; same checklist T7 / RF `Accessories` |
| 25 | Restroom vent/light/GFCI | **cov** | TI L6 sconce (RI §6.7); R6 fixtures via PROC-005; placement ART-010 / LIGHT-001 |
| 26 | Dustpan | **rej (no evidence)** | No RI/RF/DEC hit (DEC-047). Reopen only if REF-016 finds one |
| 27 | Wet-floor sign | **P10+** | RI §2 R2C3 "yellow wet-floor sign" (High) |
| 28 | Cleaning-bottle family | **cov** | PROC-010 "spray bottle, rag" (playtest 1); RF `Rack_CleaningSupplies_JC` |
| 29 | Trash-bag / paper stock | **cov** | ART-010 "restroom-cabinet supplies"; RF `Cabinet_Storage_Large` |
| 30 | Utility hooks / tool clips | **cov** | RF `Mops_Brooms_JC`; nothing more is evidenced |
| 31 | Water heater / plumbing | **cov (verify)** | Only if TI/plans show it: REF-016 row. Otherwise nothing (DEC-047) |

### BOH/HUB, exterior, life safety
| # | Item | Verdict | Citation |
|---|---|---|---|
| 32 | Pallets | **cov** | RF `Pallets_BlueCases`; RI R4C4/R5C1/R5C4; ART-009 |
| 33 | Utility cabinet / electrical panel | **cov** | RF `ElectricalBox_Wall` (DEC-051 Q2); R6 adapt via PROC-005/010 |
| 34 | Delivery paperwork | **cov (later)** | ART-009; receiving is PS4 (ROADMAP, gated) |
| 35 | BOH/HUB lived-in clutter | **cov** | ART-009 + ART-010 |
| 36–39 | Dumpster, bollards, hose bib, utility-wall dressing | **cov (verify)** | REF-015 (exterior evidence, GAPs for what no source shows) → ART-012 |
| 40 | Exterior façade graphics | **cov** | REF-015 → ART-012 |
| 41 | Fire extinguisher | **P10+** | RI §6.5 "Fire-extinguisher cabinets are painted black" (TI). Positions come from TI/REF-016, never invented |
| 42 | Smoke detector | **cov (verify)** | RI §7 excludes "alarm items". If the Hub reads that as security alarms only, it goes to REF-016 from the A101 RCP; otherwise not modelled |
| 43 | Emergency light unit | **cov (verify)** | Same route as RG6-2 (A101 RCP positions, IMP-003 handoff DEC-110 note): REF-016 / LIGHT-001 |

### Characters, 2D/UI, audio
| # | Item | Verdict | Citation |
|---|---|---|---|
| 44 | Security-guard visual kit | **cov** | ASSET-008 "guard set (CHARACTERS.md §9)" |
| 45 | Guard animation/pose | **cov** | NPC-001/NPC-002; GAME-026 (guard check-in); DEC-103/109 |
| 47 | Menu-screen / video-wall graphics | **cov** | LT-5 TV ad wall (approved/fictional brands); RI §1.5 menu screen |
| 48 | POS screen art | **cov; rej in-world contents** | GAME-007 POS UI. RI §7 excludes "screen contents" of real screens |
| 49 | Labor/procedure posters | **cov** | RF `Poster_LaborLaw`; PROC-010 signs; generic text only |
| 50 | Bulletin notices | **rej** | DEC-062 (see #15) |
| 51 | Shelf/location labels | **cov** | PROC-010 labels; real data DATA-004 (DEC-050) |
| 52 | Office forms / log sheets | **cov** | ART-010 (RI R3C3 "posted procedures"); no real data |
| 53 | Exterior/entry sign art | **cov** | REF-015 → ART-012 |
| A | Audio list (sales floor, office, break room, BOH, exterior) | **cov; rej in part** | AUDIO-001 Done (`AUDIO_PLAN.md`), AUDIO-002 Later. **Reject the money-counter and safe-keypad/door sounds** (DEC-051). Aircraft ambience only with evidence |

### §18.15–18.17
| Item | Verdict | Citation |
|---|---|---|
| 18.15 "check before adding" list | **cov** | Same rule as DEC-092 / IMP-003 |
| 18.16 production tiers | **rej as priority source** | `ROADMAP_POST_SLICE.md` is the one plan (DEC-119). Tier 1 includes the excluded money counter |
| 18.17 per-item asset ID/status/method/owner/evidence/defects/next/acceptance | **cov** | REF-016 matrix (source, confidence, dims, current implementation, gaps; DEC-120 (2)) + BACKLOG registry (DEC-119). No separate asset registry |

---

## 4. Adoptions for the Hub to apply (smallest wording)

**A1. `PROC_PIPELINE.md`, new section after "Determinism"** (P9, P10). Proposed text:

> ## Authoring order and script rules
> - Build and fix in this order: primary form and proportion → physical construction (thickness, frames, gaps, hardware) → scale-appropriate edge treatment → small detail → materials/UV → LOD, collision, pivots. Never use detail or materials to hide a form or construction fault.
> - Repair the generator or params, never the exported FBX. Script success and a passing validation are not evidence of quality (DEC-122).
> - Prefer `bmesh`/`bpy.data`/`mathutils` and `proclib` helpers; use `bpy.ops` only where no data-API route exists, and never depend on viewport selection, active mode or editor context. Drop Python mesh references after any operation that reallocates mesh data.
> - Name build functions by part (`build_push_bar`), not by step.

**A2. New BACKLOG rows:**

| ID | P | Title | Deps |
|---|---|---|---|
| PROC-014 | P1 | DEC-091 R7 QA tooling (studio-built, DEC-095): a standard review-render set in `run_generator` per asset class (ortho views + 3/4 Workbench clay, 3/4 material, optional wire), labelled and readable (DEC-122), plus planted-fault cases in `test_validation.py` for the IMP-003 failure classes: axis-order size `(w,d,h)` vs Unity `(w,h,d)` (drop 9), collision under the wrong key (drops 8/9), and a Blender runtime error inside `build()` (drop 7) | PROC-005 (owns `run_generator.py` now) |
| PROC-015 | P1 | North-wall and east-wall sales-floor anchors at DEC-084: living-wall backing + instanced foliage clusters (`ASSET_PRODUCTION_PLAN.md` §15/§46.5), TFS lettering (DEC-071), rounded merch rack, deli hand-wash sink, and the ATM shell if H1 allows; sizes from RI §1.5 / REF-016; strong visual review (DEC-122) | REF-016, PROC-005 |

**A3. PROC-010 split** (when the Hub cuts its packets): add the thermostat (RI §3 BAND 13), wet-floor sign (RI §2 R2C3) and fire-extinguisher cabinets (RI §6.5, black). Positions come from REF-016/TI only.

**A4. Remaining DEC-091 R7 items.** Rigged moving parts, state variants and the LOD/impostor + atlas pack have no BACKLOG row either. DEC-111 says every needed asset gets a row. Suggestion: a single Later row, or fold them into PERF-003 (LOD/impostor) and PROC-010 (state variants).

## 5. Hub rulings needed (not Nolan; DEC-105 search done)

- **H1. ATM.**
  - Is a generic, unbranded ATM shell (closed body, blank screen, no cash mechanism detail) allowed under DEC-051?
  - DEC-051 excludes "cash-handling equipment" and names office machines. DEC-086 allowed the POS card terminal as a realistic prop.
  - The ATM is customer-facing and plan-located (RI §1.5).
  - **Recommendation:** allow it as a closed shell, by the DEC-086 card-terminal precedent.
  - **Searched:** DECISIONS (ATM: 0 hits; DEC-051/086/111 cash wording), KNOWN_GAPS (0), RI (§1.5, §2 R3C2, §7 exclusions), RF (`Trash_Big_West_ATM` only), REF-008 handoff.
- **H2. Smoke detectors.** Does RI §7's "alarm items" mean security alarms only? If so, life-safety devices follow TI evidence via REF-016. **Searched:** RI §6–7, DECISIONS ("alarm": DEC-103 emergency-exit alarm placeholder only), KNOWN_GAPS.

No item needs Nolan. Every product or store fact the plan raises is already answered by a DEC, has an evidence row, or has no evidence and is not built (DEC-047).
