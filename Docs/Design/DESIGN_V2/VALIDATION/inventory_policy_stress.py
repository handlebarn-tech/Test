"""Stylized 18-SKU ordering stress simulation used for design validation.
Requires numpy/pandas. This is not production economy code or a real-world financial forecast.
"""
import numpy as np, pandas as pd

def make_catalog(seed=7):
    rng=np.random.default_rng(seed); rows=[]; group_demand=[2.2,1.8,1.5,1.2,.9,.7]
    for g,gd in enumerate(group_demand):
        for j in range(3):
            cost=float(rng.uniform(5,14)); price=cost*float(rng.uniform(1.45,2.25))
            rows.append({'id':f'G{g+1}S{j+1}','group':g,'cost':cost,'price':price,'unit_margin':price-cost,'pref':float(rng.uniform(.7,1.3)),'gd':gd})
    return pd.DataFrame(rows),group_demand
CAT,GROUP_DEMAND=make_catalog()

def run(policy,seed=1,shifts=50,storage_cap=70,start_cash=900):
    rng=np.random.default_rng(seed); n=len(CAT); exp=np.zeros(n)
    for g,gd in enumerate(GROUP_DEMAND):
        idx=np.where(CAT.group.values==g)[0]; w=CAT.pref.values[idx]; exp[idx]=gd*w/w.sum()
    sigma=np.maximum(.15,exp*.55); lm,ls=2.,.6
    inv=[[0]*max(1,int(round(exp[i]*1.5))) for i in range(n)]; pipe=[]; cash=start_cash
    revenue=cogs=holding=waste=0.; unmet=sold=0
    for shift in range(shifts):
        remain=[]
        for arr,i,q,cost in pipe:
            if arr<=shift:
                room=storage_cap-sum(map(len,inv)); take=max(0,min(q,room)); inv[i].extend([0]*take); cash-=take*cost
            else: remain.append((arr,i,q,cost))
        pipe=remain
        for g,gd in enumerate(GROUP_DEMAND):
            lam=float(rng.gamma(4.,gd/4.)); qty=int(rng.poisson(lam)); idx=np.where(CAT.group.values==g)[0]; w=CAT.pref.values[idx]; p=w/w.sum()
            for _ in range(qty):
                pref=int(rng.choice(idx,p=p))
                if inv[pref]: choose=pref
                else:
                    avail=[i for i in idx if inv[i]]
                    if not avail or rng.random()>=.75: unmet+=1; continue
                    aw=np.array([CAT.pref.iloc[i] for i in avail]); aw=aw/aw.sum(); choose=int(rng.choice(avail,p=aw))
                inv[choose].pop(0); sold+=1; revenue+=float(CAT.price.iloc[choose]); cogs+=float(CAT.cost.iloc[choose]); cash+=float(CAT.price.iloc[choose])
        for i in range(n):
            inv[i]=[a+1 for a in inv[i]]; holding += .03*float(CAT.cost.iloc[i])*len(inv[i]); keep=[]
            for a in inv[i]:
                if a>14: waste+=float(CAT.cost.iloc[i])
                else: keep.append(a)
            inv[i]=keep
        if shift%2==0:
            on=np.array([len(x) for x in inv]); oo=np.zeros(n,dtype=int)
            for arr,i,q,c in pipe: oo[i]+=q
            pos=on+oo; ss=1.28*np.sqrt(lm*sigma**2+(exp**2)*(ls**2))
            if policy=='balanced':
                selected=[]
                for g in range(6):
                    idx=np.where(CAT.group.values==g)[0]; score=CAT.pref.values[idx]*(.6+.4*(CAT.unit_margin.values[idx]/CAT.unit_margin.max())); selected+=list(idx[np.argsort(score)[-2:]])
                target=np.ceil(exp*lm+ss+exp)
            elif policy=='breadth': selected=list(range(n)); target=np.ceil(exp*lm+.5*ss)
            elif policy=='depth':
                selected=[]
                for g in range(6):
                    idx=np.where(CAT.group.values==g)[0]; selected.append(int(idx[np.argmax(CAT.pref.values[idx])]))
                for g in [0,1]:
                    idx=np.where(CAT.group.values==g)[0]; selected.append(int(idx[np.argsort(CAT.pref.values[idx])[-2]]))
                target=np.ceil(exp*lm+1.4*ss+exp*1.8)
            elif policy=='margin': selected=list(np.argsort(CAT.unit_margin.values)[-8:]); target=np.ceil(exp*lm+ss+exp)
            elif policy=='everything': selected=list(range(n)); target=np.ceil(exp*lm+1.8*ss+exp*2.5)
            needs=[]
            for i in set(selected):
                q=max(0,int(target[i]-pos[i]))
                if q:
                    group_inv=sum(pos[j] for j in np.where(CAT.group.values==CAT.group.iloc[i])[0]); bonus=4. if group_inv<=1 else 0.; needs.append((exp[i]*CAT.unit_margin.iloc[i]+bonus,i,q))
            needs.sort(reverse=True); projected=sum(map(len,inv))+sum(q for _,_,q,_ in pipe); available=max(0,cash-180)
            for _,i,q in needs:
                oq=min(q,max(0,storage_cap-projected),int(available//CAT.cost.iloc[i]))
                if oq<=0: continue
                lead=max(1,int(round(rng.normal(lm,ls)))); pipe.append((shift+lead,i,oq,float(CAT.cost.iloc[i]))); available-=oq*float(CAT.cost.iloc[i]); projected+=oq
    inv_value=sum(len(inv[i])*CAT.cost.iloc[i] for i in range(n)); fill=sold/(sold+unmet) if sold+unmet else 1
    return {'fill_rate_pct':100*fill,'contribution':revenue-cogs-holding-waste,'unmet':unmet,'waste':waste,'holding_burden':holding,'end_inventory_value':inv_value,'end_cash':cash}

if __name__=='__main__':
    rows=[]
    for policy in ['balanced','breadth','depth','margin','everything']:
        d=pd.DataFrame([run(policy,5000+s) for s in range(45)])
        rows.append({'policy':policy,**{c:d[c].mean() for c in d.columns},'seeds':45,'shifts_per_seed':50})
    print(pd.DataFrame(rows).round(2).to_csv(index=False))
