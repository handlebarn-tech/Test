"""Synthetic structural test for promotion gates. Requires numpy/pandas."""
import numpy as np, pandas as pd
GATES={
 'Senior':{'SJ':70,'TP':65,'ID':60,'OA':75,'REL':65},
 'Lead':{'SJ':75,'TP':70,'ID':70,'OA':80,'REL':72,'LEAD':65},
 'AssistantManager':{'SJ':78,'TP':72,'ID':76,'OA':82,'REL':78,'LEAD':72},
 'Manager':{'SJ':78,'TP':72,'ID':80,'OA':83,'REL':80,'LEAD':78},
}
PROFILES={
 'balanced_master':{'SJ':84,'TP':80,'ID':83,'OA':88,'REL':85,'LEAD':83},
 'speedrunner':{'SJ':60,'TP':94,'ID':58,'OA':66,'REL':72,'LEAD':60},
 'perfectionist_slow':{'SJ':91,'TP':56,'ID':86,'OA':94,'REL':82,'LEAD':72},
 'careless_sales':{'SJ':72,'TP':88,'ID':52,'OA':55,'REL':70,'LEAD':64},
 'inventory_obsessive':{'SJ':68,'TP':58,'ID':96,'OA':86,'REL':80,'LEAD':65},
 'revenue_only':{'SJ':62,'TP':84,'ID':55,'OA':64,'REL':68,'LEAD':58},
 'balanced_good':{'SJ':78,'TP':74,'ID':76,'OA':82,'REL':78,'LEAD':73},
}

def pass_rate(means,gate,rng,sims=5000,sd=6):
    req=GATES[gate]; ok=0
    for _ in range(sims):
        passed=True
        for c,thr in req.items():
            vals=np.clip(rng.normal(means[c],sd,6),0,100)
            if np.median(vals)<thr or np.sum(vals < thr-10)>1:
                passed=False; break
        ok += passed
    return ok/sims

if __name__=='__main__':
    rng=np.random.default_rng(42); rows=[]
    for name,means in PROFILES.items():
        rows.append({'profile':name,**{g:pass_rate(means,g,rng) for g in GATES}})
    print(pd.DataFrame(rows).round(3).to_csv(index=False))
