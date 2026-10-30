# DES-004b handoff: 22:00 door lock per DEC-076

**Status:** done. Doc-only, branch `claude/task-des-004b` (off main 989d702).

## Changed
- `SPEC_SHIFT_DAY.md` §2: Late runs 20:00 → 22:00; the doors lock at 22:00 on the dot (DEC-076). No arrivals at or after 22:00. Customers inside are served to completion (normal patience rules), the clock runs past 22:00, and Closing starts when the last customer leaves. This replaces DEC-DAY-F (21:45 lock, last call, 22:00 POS cut-off, `closed_out`). GAP-DAY-09 row removed (closed by DEC-076).
- §4 + GAME-011: specials drawn in U(300, min(1620, lockSec − 60)), so none arrives after the lock (REVIEW-W5D m6). Before this fix, Beginner's special arrived after its 1380 s lock in about 18 % of shifts.
- §12/§13 + GAME-011 test (b2): `closed_out` dropped. New: `overtimeSimSec` is logged; the test asserts no arrival after the lock, nobody cut off by the clock, and Closing only with an empty store.
- UX-003 item 1: "Doors locked" banner and the clock past 22:00.
- `VALIDATION_DAY/`:
  - `shift_day_sim.py` applies the specials cap. Standard/Expert results are unchanged; Beginner is now 0.27 % abandonment, 27 s mean wait, mean peak 1.92.
  - `shift_day_drain.py` now measures service after 22:00: Standard mean 45 s / p90 118 s / max 303 s; Expert 44 / 112 / 226 s; Beginner 31 / 85 / 205 s; 0 arrivals after the lock (`shift_day_overtime_results.txt`). The old `shift_day_drain_results.txt` is removed.

## For the Hub
- Nothing else depends on DEC-DAY-F; DES-004.md keeps it as history.
- No questions for Nolan.
