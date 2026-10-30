"""Reproducible design-tuning harness for Dispo Game queue pressure.
This is a design validator, not production game code or an empirical store model.
Requires numpy and pandas.
"""
import math
import numpy as np
import pandas as pd

ARCH={
 'Novice':(.22,58),'Regular':(.24,46),'Enthusiast':(.14,72),
 'PriceShopper':(.16,40),'DecisiveRepeat':(.14,32),'Indecisive':(.10,76)
}
AMB={'beginner':[.45,.40,.13,.02],'standard':[.25,.40,.25,.10],'expert':[.10,.30,.40,.20]}
PM={'beginner':1.35,'standard':1.0,'expert':.88}
PROFILES={
 'beginner':{'phases':[(2,.09),(5,.54),(4,.86),(4,.32),(4,.99),(4,.54),(3,0)],'k':3.0,'specials':1},
 'standard':{'phases':[(2,.12),(5,.54),(6,.96),(4,.30),(6,1.08),(5,.54),(4,0)],'k':2.5,'specials':2},
 'expert':{'phases':[(2,.13),(5,.55),(7,.94),(4,.32),(7,1.02),(6,.55),(4,0)],'k':2.2,'specials':2},
}

def lnorm(med,sig,rng): return float(rng.lognormal(math.log(med),sig))

def customer(rng,diff,policy):
    names=list(ARCH); probs=[ARCH[x][0] for x in names]
    a=str(rng.choice(names,p=probs)); base=lnorm(ARCH[a][1],.20,rng)
    amb=int(rng.choice([0,1,2,3],p=AMB[diff]))
    if policy=='targeted': add=[0,8,14,22][amb]+(6 if a=='Enthusiast' else 0)
    elif policy=='all': add=42+(6 if a=='Enthusiast' else 0)
    else: add=-6
    svc=max(24.,base+add)
    pt=str(rng.choice(['low','normal','high'],p=[.2,.6,.2]))
    patience=lnorm({'low':140,'normal':230,'high':330}[pt]*PM[diff],.35,rng)
    return svc,patience

def arrivals(rng,prof):
    out=[]; t=0.
    for dur,rate in prof['phases']:
        start=t; end=t+dur*60
        if rate:
            mean=60/rate; cur=start
            while True:
                cur += float(rng.gamma(prof['k'],mean/prof['k']))
                if cur>=end: break
                out.append(cur)
        t=end
    for _ in range(prof['specials']): out.append(float(rng.uniform(300,1620)))
    return sorted(out)

def run(seed,diff='standard',policy='targeted'):
    rng=np.random.default_rng(seed); arr=arrivals(rng,PROFILES[diff])
    c=[{'a':a,'s':customer(rng,diff,policy)[0]} for a in arr]
    # regenerate patience separately in stable loop
    rng=np.random.default_rng(seed); _=arrivals(rng,PROFILES[diff])
    c=[]
    for a in arr:
        s,p=customer(rng,diff,policy); c.append({'a':a,'s':s,'p':p})
    waiting=[]; i=0; t=0.; free=0.; waits=[]; served=[]; abandoned=[]; starts={}
    while i<len(c) or waiting:
        if not waiting:
            t=max(free,c[i]['a'])
            while i<len(c) and c[i]['a']<=t: waiting.append((i,c[i])); i+=1
        else:
            t=max(t,free)
            while i<len(c) and c[i]['a']<=t: waiting.append((i,c[i])); i+=1
        keep=[]
        for j,x in waiting:
            (abandoned if x['a']+x['p']<=t else keep).append((j,x))
        waiting=keep
        if not waiting: continue
        waiting.sort(key=lambda z:z[1]['a']); j,x=waiting.pop(0)
        st=max(t,free,x['a']); starts[j]=st; waits.append(st-x['a']); served.append((j,x)); free=st+x['s']; t=free
        while i<len(c) and c[i]['a']<=t: waiting.append((i,c[i])); i+=1
        keep=[]
        for j2,x2 in waiting:
            (abandoned if x2['a']+x2['p']<=t else keep).append((j2,x2))
        waiting=keep
    events=[]
    for j,x in enumerate(c): events.append((x['a'],1,0))
    for j,x in served: events.append((starts[j],-1,1))
    for j,x in abandoned: events.append((x['a']+x['p'],-1,2))
    q=maxq=0
    for _,d,_ in sorted(events,key=lambda z:(z[0],z[2])): q+=d; maxq=max(maxq,q)
    sv=[x['s'] for _,x in served]
    return {'arrivals':len(c),'served':len(served),'abandon_pct':100*len(abandoned)/len(c) if c else 0,
            'mean_wait_s':float(np.mean(waits)) if waits else 0,'p90_wait_s':float(np.percentile(waits,90)) if waits else 0,
            'median_service_s':float(np.median(sv)) if sv else 0,'max_queue':maxq}

def batch(diff,policy,n,base=200000):
    d=pd.DataFrame([run(base+i,diff,policy) for i in range(n)])
    return {'difficulty':diff,'policy':policy,'arrivals_mean':d.arrivals.mean(),'served_mean':d.served.mean(),
            'abandon_pct':d.abandon_pct.mean(),'mean_wait_s':d.mean_wait_s.mean(),'p90_wait_s':d.p90_wait_s.mean(),
            'median_service_s':d.median_service_s.mean(),'max_queue_mean':d.max_queue.mean(),'max_queue_p90':d.max_queue.quantile(.9),'seeds':n}

if __name__=='__main__':
    jobs=[('beginner','targeted',350),('standard','targeted',700),('standard','all',700),('standard','none',700),('expert','targeted',350)]
    out=pd.DataFrame([batch(*j) for j in jobs])
    print(out.round(2).to_csv(index=False))
