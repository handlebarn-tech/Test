# REVIEW-W5L — DES-004b+c: 22:00 door lock (DEC-076) + manager refill requests (DEC-079/080)

**Verdict: PASS with minors (GO).** Branch `review/wave-5l` (off `main` 1abafc1) merges `claude/task-des-004b` (8d1d209 + 22ccc85, with merge 75da6ca) cleanly as 1e7eded. Docs/data only: 12 files, +235/−146. Reviewer: independent review session, 2026-10-30.

## DES-004b vs DEC-076
- §2: Late runs to 22:00; doors lock "on the dot"; no arrival at or after 22:00 (door line, phase draws, specials); customers inside are served to completion under normal patience; Closing starts when the last one leaves. Matches DEC-076 word for word, including M3 applying to entry ✔. GAME-011 step 1 + test (b2) and UX-003 item 1 match ✔.
- **No DEC-DAY-F remnants:** `21:45`, `closed_out`, `lastCallSimSec`, `21:59` and DEC-DAY-F appear nowhere in the spec, packets, ROADMAP or validation folder; only the DES-004b handoff mentions them as what was replaced ✔. GAP-DAY-09 row removed ✔.
- W5D m6 fixed: specials in U(300, min(1620, lockSec − 60)) in spec §4, GAME-011 step 2 and `shift_day_sim.py` ✔.
- **Re-runs:** `shift_day_sim.py` reproduces `shift_day_results.csv` and `shift_day_drain.py` reproduces `shift_day_overtime_results.txt` exactly (Standard overtime mean 45 s / p90 118 s) ✔.

## DES-004c vs DEC-079/080
- One 1 lb jar per strain, house doubled; 1 lb bags in the HUB cabinets; managers always refill at the certified silver cart; empty house jar waits on the wooden shelf; one shared line; "at least a couple" at open (2/3/3 kept); GM assigns registers on a floor map; procedure steps — all cited [SRC DEC-079] and quoted accurately ✔. DEC-042's "stainless prep cart labelled for deli use" is consistent with the cart ✔.
- DEC-080: the player requests a refill, the jar is unavailable for a timed window, house strains keep their second jar out, the full loop is a manager-rank unlock via GAME-024 ✔.
- **GAME-012 / GAME-024 scopes are consistent.** GAME-012 owns floor jars/bags/RefillGrams, states incl. REFILLING, the request queue (`ManagerRefills.cs`), tags and EX-013/019/021/022/024; it explicitly does not own the §9b loop and drops the ART-005/BOH anchor dependency. GAME-024's note adds only an unlock flag, matching its Deliverable 2 ("a gate passed unlocks a flag only") ✔. ROADMAP GAME-012 row keeps the original text with a re-scope note; exit test updated ✔.
- **No invented facts:** new numbers (3 s request, 90 s window, FIFO one-at-a-time, 0 bags 10 % / 1–9 bags) are [GDD] or GAP-DAY-10..13 placeholders. GAP-DAY-10's counts check out against `batches.json`: in stock 77, house 6 + smalls 35 + premium 2 = 43 ✔.

## Minors
- **m1** §9a.4 refills only the emptier house jar, but DEC-079's real practice is that the empty jar waits on the shelf until the second is empty or low, then **both** are filled. The DEC-080 simplification is fine; label the one-jar completion [GDD per DEC-080] and note the real pattern for the §9b manager loop.
- **m2** "Sales draw from the fuller jar until it empties" (§9a, GAME-012 deliverable 2) is not in DEC-079: label [GDD].
- **m3** §9b procedure puts "6. Clean" after "4. Fill both jars". DEC-079 says only that managers clean jars after sell-through; it gives no order. Don't sequence cleaning after filling; say "clean emptied jars (order not stated)".
- **m4** EX-016/017/023 (DEC-066: Critical/High need tests before completion) now belong to the §9b loop, which has no packet until GAME-024 lands. Hub: add a BACKLOG row for the manager refill loop so these rows have an owner.
- **m5** DEC-077 ratified DEC-DAY-D (player whole-unit picks, carry ≤ 2, carried grams count for eligibility). DEC-080 moves that to the manager rank; the Hub should amend DEC-077 D to "superseded for PS2 by DEC-080; applies to the §9b manager loop".
- Note: §5 / §14 GAP-DAY-03 still shows 0/4/2/3/5/3/0; the REVIEW-W5K rule (Rush 1 1, Recovery 1, Steady 4, Rush 2 5, Late 5) waits for RES-002's fix.

## For the Hub — questions for Nolan (from the DES-004b handoff)
GAP-DAY-10 which strains get two jars (`house` only, or house smalls/premium too) · GAP-DAY-11 how long a jar is off the floor for a refill, and one manager at a time? · GAP-DAY-12 do managers refill without being asked? GAP-DAY-13 (smalls jar capacity) is a REF task, not Nolan's.
