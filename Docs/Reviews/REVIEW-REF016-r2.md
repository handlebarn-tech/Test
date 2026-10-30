# REVIEW-REF016 round 2: store-evidence matrix (fresh evidence reviewer, DEC-120 (3))

**Reviewed:** `claude/magical-einstein-182567` @ `fb78346` (fix round on 14332c3) against `main` · **Review branch:** `review/ref016-r2` (cut from `fb78346`)
**Read:** packet `Docs/Tasks/Active/REF-016.md`; diff `main...fb78346` and the fix-round diff `14332c3..fb78346`; handoff Fix round, Validation and Not-done; round-1 review `Docs/Reviews/REVIEW-REF016.md` @ `908abbd`.
**Evidence opened directly:** TI approved set (`References/TI/Interior TI Approved Set - PHX.pdf`) p.35 E101 and p.13 A901 det. 17, word positions via PyMuPDF `get_text("words")` at 18 pt/ft. No CCTV re-measurement this round (round 1 read R2C1/R2C3/R2C5 and the wide still; the fix round changed no CCTV reading except R07's y, which round 1 itself described).

## Verdict: PASS with minors

## M1 (round 1 MAJOR): resolved

| Requirement from round 1 | Check | Result |
|---|---|---|
| Report the TI grouping as drawn | My own read: E101 `POS` words x 644/710/875/947/1021 pt (y 774) → gaps **3.67 / 9.16 / 4.00 / 4.12 ft**; A901 `TV` words x 438/506/669/743/816 pt (y 202) → **3.75 / 9.08 / 4.09 / 4.08 ft**. The matrix (`POS_02..06.matrix.src_primary`, REFERENCES_INDEX §8.1, §9.1, §9.2 row) now states these gaps and "2 + 3 with a 9.1 ft gap". No "pitch 3.75–4.08" text remains in the live files (grep at fb78346; the one stale `y 25.2` hit is the history list `graybox_contradictions`, labelled as history). | PASS |
| Say which source wins for x and why | §9.1: CCTV wins because the store changed (DEC-120); A011 run x 15.28–41.03 = 25.75 ft vs A901 27'-9". Arithmetic checked: west-aligned 15.28 + offsets = 19.06 / 22.81 / 31.89 / 35.97 / 40.05; east-aligned 13.28 + offsets = 17.06 / 20.81 / 29.89 / 33.97 / 38.05. Both put the fifth outlet at or past the east-return face 37.99. | PASS (see n2 on the margin) |
| Keep conf/GAP on the result | `POS_02..06.matrix.conf.position` "High (y) / Low (x)", gaps GAP-131/GAP-108; §9.3 rows 6–10 carry the same. | PASS |
| Note R2C5's 4 monitors vs 5 | §9.1 and handoff record it as unresolved; count of 5 rests on TI circuits + DEC-039 (Med, GAP-131). | PASS |

## Round-1 minors

| # | Fix | Check | Result |
|---|---|---|---|
| m1 | R07 monitor y 25.2 → 23.2; stand y 24.0–25.6 (operator's left); bin to y 24.8; both R07 anchors y 23.2 | `POS_07` pos_ft (17.56, 23.2), stand_rect y 24.0–25.6, notes match round 1's R2C1 description; operator (18.78, 23.2) is 0.7 ft south of the run's staff face y 22.5, on staff floor; `Trash_Small_POS_07` x 19.08–20.23 sits behind (east of) the west-facing stand; §8.1 table, §9.1, §9.3 row 5 updated | PASS |
| m2 | `target_opening.role` = clear leaf span; wall cut = `rough_opening` 21.38–24.72 | DOORS `_about`, row notes, implemented detail, §6.2, §8.5 table and §9.3 row 27 all say the same | PASS |
| m3 | Guard anchor flagged placeholder | `Anchor_Guard_Post.note` and §9.1 flag the stand x / guard x pair for ART-013, GAP-134 | PASS |
| m4 | 15 all-Low rows get GAP-127 | Script over all 132 RF rows: every row has `matrix.src_primary` and `implemented.status`; no row with all-Low `conf` lacks a gap (0 found). `Chair_Task_2` spot-checked: `gap` and `matrix.gaps` = GAP-127 | PASS |
| m5 | `Trash_Big_East_Sink` note/side | note places it east of the south-wall sink (x 45.6–46.8 vs sink 43.67–45.56), staff floor, clear of the exit, records the possible duplicate of `Trash_Big_SouthReturnEnd`; `served_side` staff | PASS |
| m6 | R07 anchors Med → Low | both anchors Low with the weakest-field reason | PASS (see n1) |

## DEC-047 spot check
JSONs parse (all three). All 132 ROOM_FIXTURES rows carry a primary source and an implemented status; every Low row carries a GAP id. Spot-checked POS_04, POS_07, Counter_Register_SouthWestReturn, Trash_Small_POS_07, Trash_Big_East_Sink, Chair_Task_2, the two R07 anchors, `Anchor_Guard_Post` and `Emergency_RetailE`: every value cites a source or a GAP. No invented store fact found.

## minor (non-blocking)

- **n1. Row-level `confidence` still Med on POS_07 and POS_02..06** while `matrix.conf.position` is Low (x for 02..06, y for 07). The fix round applied the weakest-field rule (REVIEW-REF013b m1) to the R07 anchors but not to the station rows' own top-level `confidence`. The per-field conf is explicit, so ART-013 is not misled; align the top-level field when next touched.
- **n2. M1 rationale is thin at the east end.** East-aligned, the TI's fifth outlet lands at x 38.05, only 0.06 ft past the east-return face 37.99, so "cannot be today's" rests mostly on the west-aligned case and on CCTV's even spacing. The conclusion stands (CCTV is the direct evidence of today's store and the result is Low/GAP-131); the wording could say CCTV is the deciding source and the run-length shift is supporting.
- **n3. R2C5 view direction wording:** REFERENCES_INDEX §2 row says "looking NW", §9.1 says "looking W". Cosmetic.

Not run: `Tools/Studio/room_fixtures_layout.py --check` (ART-owned, fails on a stale row name, as the handoff says).
