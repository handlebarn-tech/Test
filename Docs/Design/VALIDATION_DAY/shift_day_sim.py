"""DES-004 shift-day check: V2's queue harness (DESIGN_V2/VALIDATION/shift_queue_sim.py, unchanged)
run on the DES-004 phase tables (SPEC_SHIFT_DAY.md §3). Design validator only; numbers are [GDD].
Usage: python shift_day_sim.py   (needs numpy, pandas)
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'DESIGN_V2', 'VALIDATION'))
import pandas as pd
import shift_queue_sim as v2

# (minutes, rate/min); the door line is `door` customers queued at the Rush 1 start (O12), spaced 0-20 s.
DAY = {
 'beginner': {'phases': [(2,0),(4,.66),(4,.30),(5,.54),(4,.90),(4,.54),(3,0)], 'k': 3.0, 'specials': 1, 'door': 2},
 'standard': {'phases': [(2,0),(5,.70),(4,.30),(6,.50),(6,1.00),(5,.54),(4,0)], 'k': 2.5, 'specials': 2, 'door': 3},
 'expert':   {'phases': [(2,0),(6,.72),(4,.32),(6,.55),(7,.94),(6,.55),(4,0)], 'k': 2.2, 'specials': 2, 'door': 3},
}
_v2_arrivals = v2.arrivals

def lock_sec(prof):                               # doors lock at 22:00 = end of Late (DEC-076)
    return sum(m for m, _ in prof['phases'][:-1]) * 60

def arrivals(rng, prof):
    out = _v2_arrivals(rng, dict(prof, specials=0))   # V2 rule: renewal clock restarts at every phase start
    hi = min(1620, lock_sec(prof) - 60)               # V2 draws specials in U(300, 1620); never after the door lock
    out += [float(rng.uniform(300, hi)) for _ in range(prof['specials'])]
    t0 = prof['phases'][0][0] * 60                    # doors open = end of Opening
    out += [t0 + float(rng.uniform(0, 20)) for _ in range(prof['door'])]
    return sorted(out)

v2.arrivals, v2.PROFILES = arrivals, DAY
if __name__ == '__main__':
    jobs = [('beginner','targeted',350),('standard','targeted',700),('standard','all',700),('standard','none',700),('expert','targeted',350)]
    print(pd.DataFrame([v2.batch(*j) for j in jobs]).round(2).to_csv(index=False))
