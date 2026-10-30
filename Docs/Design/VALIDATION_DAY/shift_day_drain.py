"""DES-004b check: service after the 22:00 door lock (DEC-076: customers inside are served to completion).
Reports overtime = last service end - door lock, in sim seconds. Reuses V2's run() unchanged, returning before
its metrics. Usage: python shift_day_drain.py   (needs numpy, pandas)"""
import inspect, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import shift_day_sim as d; v2 = d.v2
src = inspect.getsource(v2.run).replace("    events=[]", "    return c, served, starts\n    events=[]")
ns = {}; exec(src, v2.__dict__, ns); run = ns['run']
for diff, n in [('beginner', 350), ('standard', 700), ('expert', 350)]:
    lock = d.lock_sec(d.DAY[diff]); over = []; late_arr = 0
    for i in range(n):
        c, served, starts = run(200000 + i, diff, 'targeted')
        late_arr += sum(1 for x in c if x['a'] >= lock)
        over.append(max([0.0] + [starts[j] + x['s'] - lock for j, x in served]))
    o = np.array(over)
    print(diff, 'overtime_s mean', round(o.mean(), 1), 'p90', round(np.percentile(o, 90), 1), 'max', round(o.max(), 1),
          'shifts_with_overtime_%', round((o > 0).mean() * 100, 1), 'arrivals_after_lock', late_arr)
