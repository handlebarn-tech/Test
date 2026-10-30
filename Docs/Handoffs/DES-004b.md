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

## DES-004c: DEC-079 store answers + DEC-080 manager refill (same branch, merged main 465992e)
- **Spec §9a rewritten:** the budtender **requests a manager refill**.
  - 3 s request; FIFO, one manager at a time.
  - The jar leaves for `refillWindowSimSec` 90 s; a house strain keeps its second jar out.
  - Completion is atomic from 1 lb HUB bags.
  - New state REFILLING. Tags keep their meaning (start = the request). Unneeded costs a sellable jar plus the manager slot (DP-018 remapped).
  - Backstock 0 bags (10 %) or 1–9 bags, from "≈ 10 lb per shipment".
- **New §9b:** manager refill loop (office silver cart, bowl on scale, inventory moves, fill both jars, clean, wooden shelf, HUB cabinets) moved to the manager rank. Physical-job design and EX-016/017/023 go with it.
- **§5:** GM-assigned register per shift (floor map at Opening, `assignableRegisters`); one shared line called up as registers free. **§3:** door line 2/3/3 stays (Nolan: "at least a couple").
- **Smaller edits:** §7 refills don't block fast-forward and their completion stops it; §8 `refillsPending` replaces `awayWithQueue`; §10 Opening/Closing (flag jars for the closing manager); §12 attribution back to 3 criteria; §13/§14 updated.
- **GAPs:** 01/02/04/05/06/07/08 closed (DEC-079); 03 → RES-002.
- **Packets:**
  - GAME-012 rewritten (no BOH anchor, no ART-005 dependency).
  - GAME-011: assigned register, shared-line HUD, 3 criteria.
  - UX-003: refill request UI, register map, shared line.
  - GAME-024: DES-004c note (unlock flag only; the loop gets its own packet later).
  - ROADMAP: GAME-012 row re-scope note + exit test.

### Questions for Nolan (through the Hub)
1. **GAP-DAY-10:** which deli strains get two jars? Catalog tiers in stock: `house` 6, `smalls` 35, `premium` 2, `t1–t3` 30, `fttp` 4. Is it only the `house` tier, or all house lanes (house smalls, house premium, Bring the Heat, RES-001 P3)? Placeholder: house + smalls + premium (43 of 77).
2. **GAP-DAY-11:** about how long is a jar off the floor when a manager refills it? Does one manager do them one at a time? Placeholder: 90 s of game time (≈ a short real wait), one at a time.
3. **GAP-DAY-12:** do managers ever refill a low jar without a budtender asking? Placeholder: no.
- GAP-DAY-13 (REF, not Nolan): capacity of the house-smalls jar (DEC-042 product page). Placeholder 454 g.

### Notes for the Hub
- DEC-079's "a popular strain can sell a pound in under an hour" is store-wide. Under DEC-DAY-B, ambient registers don't sell, so PS2 jar pressure comes from seeded start fills. Letting ambient registers drain jars at a background rate would be more faithful, but it amends DEC-DAY-B. That is a PS4 option or your call.
- House double jars add up to 43 wall jars (placeholder): ART/REF wall-jar count impact.
- ART-005's "deli backstock location" is now known (HUB cabinets against the office wall). It is only needed for the manager rank and the optional manager NPC walk.
