"""DES-004 M1 check: customers still unserved when sales lock, i.e. service ending after doors-lock + W seconds
(SPEC_SHIFT_DAY.md §2 last call). Reuses V2's run() unchanged, returning before its metrics. Usage: python shift_day_drain.py"""
import sys, inspect, numpy as np
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import shift_day_sim as d; v2 = d.v2
src = inspect.getsource(v2.run).replace("    events=[]", "    return c, served, starts\n    events=[]")
ns = {}; exec(src, v2.__dict__, ns); run = ns['run']
for diff, n in [('beginner',350),('standard',700),('expert',350)]:
    ph = d.DAY[diff]['phases']; lock = sum(m for m, _ in ph[:-1]) * 60
    for W in (60, 120, 180):
        lost = shifts = 0
        for i in range(n):
            c, served, starts = run(200000+i, diff, 'targeted')
            k = sum(1 for j, x in served if starts[j] + x['s'] > lock + W)
            lost += k; shifts += k > 0
        print(diff, 'W', W, 'closed_out/shift', round(lost/n, 3), 'shifts with any', round(shifts/n*100, 1), '%')
