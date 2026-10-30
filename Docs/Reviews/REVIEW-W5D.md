# REVIEW-W5D — DES-004: PS2 "Full Shift Day" spec + UX-003 / GAME-011 / GAME-012 packets

**Verdict: FAIL (one must-fix, M1; otherwise ready).** Branch `review/wave-5d` (off `main` 6559a51) merges `claude/blissful-nobel-6a5526` @ a693cef cleanly. Reviewer: independent review session, 2026-10-30. M1 is a two-line spec/packet edit; re-review is a diff check of M1 only.

## Scope
8 files, +425/−4, all doc/data plus one design-validation script. DECISIONS, BACKLOG, PROJECT_STATE, KNOWN_GAPS untouched (Hub-owned) ✔. ROADMAP edit: one header line + the DES-004 / UX-003 / GAME-011 / GAME-012 rows set Done/Ready with deps; original row text kept ✔.

## Against the DES-004 row (ROADMAP §3)
| Row item | Spec | |
|---|---|---|
| DP §61–65 as input | §2 phases, §3/§7 compression (DP §62/63), §8 PressureLevel (DP §64: arrival rate, queue, tasks, stock, events; staff = 0 in PS2), §9 events (DP §65; "register unavailable" → receipt-paper event, plausible) | ✔ |
| 08–22 clock, O12/O13 traffic | §2 (O1, O12), §4/§5 (O13) | ✔ but see **M1** |
| opening-lite 2–5 min, closing-lite O11 subset | §10: 2 min opening; closing items 1–4 all in O11 | ✔ |
| restock rules | §9a (DP §40–50, DEC-055/061) | ✔ |
| report v2 (O16) | §11, section list matches O16 exactly | ✔ |
| V2 numbers, labelled [GDD] | §3 tables, §4, §6, §7, §9a all tagged [GDD]; lengths 26/32/35 sum correctly; patience, k, specials = V2 `default_tuning.yaml` | ✔ |
| Caveat: renewal clock | §4: port V2's per-phase restart exactly; nominal vs realised documented | ✔ |
| Caveat: single server vs 11 registers | §5: player = 1 register; others ambient, no sim effect (DEC-039/040 cited correctly) | ✔ |
| Caveat: compression never skips a decision | §7: pre-generated sim-time schedule + FF start/stop rules + determinism test | ✔ |
| DEC-056 25–40 min | §13 exit test | ✔ |

**Harness re-run:** `python -I Docs/Design/VALIDATION_DAY/shift_day_sim.py` reproduces `shift_day_results.csv` byte-for-byte (Standard targeted 19.96 arrivals / 4.47 % / mean peak 3.24 / p90 5). The script only monkey-patches `arrivals` and `PROFILES`; V2's `shift_queue_sim.py` is unchanged ✔. Note: 19.96 sits at the top edge of the 18–20 gate.

## Store facts (no invention)
O1, O11, O12, O13, O14, O16 quotes match `Research/OFFICE_FINDINGS.md` §3. DEC-019 (454 g), DEC-039/040 (11 floor registers), DEC-041 (BOH wire racks), DEC-049, DEC-052, DEC-055/061 cited correctly. Every unknown is a GAP-DAY-01..08 with a labelled placeholder ✔.

## Findings
- **M1 (must-fix, compliance) — sales after 22:00.** §2: "At 22:00 no more arrivals; customers already queued are still served (Closing waits for an empty queue)", with the Closing clock running "22:00 →"; GAME-011 packet step 1 encodes the same. AZ R9-18-308(A)(1)(a) allows sales only 07:00–22:00 (`Research/AZ_COMPLIANCE.md` G1, DEC-036 M3), DEC-032 forbids letting the player do what the store legally can't, and `SliceTests.cs:292–296` already asserts the shift stays inside store hours. Fix (any one, [GDD]): lock the doors at a last-entry time before 22:00 (e.g. 21:45) and map the drain so the last sale is ≤ 21:59; or clamp the displayed clock at 21:59 until the queue is empty; plus an EditMode assert "no sale timestamp ≥ `salesHoursEnd`". Real last-entry practice = a new GAP-DAY-09 for Nolan.
- **m1** §11 cites "nickel, DEC-036" for rounding; the rounding decision is **DEC-035**.
- **m2** §2 Opening displays 07:30 → 08:00. No sales, so it is legal (window opens 07:00), but staff arrival time is not a sourced fact: label it [GDD].
- **m3** DEC-DAY-A reorders DP §61 ("Recommended target"). The spec states it as a Hub call and keeps the order in config; justified by O12. Ratifying it means a store fact overriding DP's generic order: fine by CLAUDE.md, but the Hub should record that explicitly.
- **m4** §7 determinism test says "identical stock at each arrival": only true with a scripted bot taking identical actions; say so in the GAME-011 test.
- **m5** GAME-011 row drops DP §51 demand inputs (deal, repeat, availability); §9 moves deal rush out of PS2 (GAME-016) and repeats to special slots. Consistent, but worth one line in the row.

## For the Hub — proposed DECs (from the handoff)
- **DEC-DAY-A** phase order follows the store: Opening → Rush 1 (door) → Recovery → Steady → Rush 2 → Late → Closing (O12). Config swap if DP order preferred (re-run the script).
- **DEC-DAY-B** one player register; other registers ambient, no sim effect until PS4.
- **DEC-DAY-C** V2 renewal arrivals restarted per phase + door line + specials, pre-generated from `arrival_rng`; Quick shift keeps its RNG/goldens.
- **DEC-DAY-D** restock: whole-unit picks, carry ≤ 2, atomic pick/Transfer, carried grams count for TFS eligibility; tags Proactive/Reactive/Emergency/Unneeded.
- **DEC-DAY-E** report v2 omits unmodelled O16 sections rather than zero-filling.
Reviewer view: A–E sound; ratify after M1. GAPs GAP-DAY-01..08 (+09 from M1) and handoff questions 1–7 go to KNOWN_GAPS / Nolan.
