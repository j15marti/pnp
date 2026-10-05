from __future__ import annotations
import random, statistics, json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score

from experiments.monotone_slice import pair_match_order3 as pm

Q_VALUES=(20,24,28,32)
N=6000
CALIPER=0.75
TRIPLE_SAMPLES=600
TOP_K=8


def run_q(q):
    t=round(pm.DENSITY*q)
    rng=random.Random(pm.BASE_SEED+1000+q)
    rows=[]
    for _ in range(N):
        f=pm.gen_formula(q,t,rng)
        pv,cu=pm.features(f,q)
        rows.append({'f':f,'sat':pm.dpll_sat(f),'pv':pv,'cu':cu})

    half=N//2
    train=rows[:half]
    hold=rows[half:]
    train_sat=[r for r in train if r['sat']]
    hold_sat=[r for r in hold if r['sat']]
    hold_uns=[r for r in hold if not r['sat']]

    mu=np.array([statistics.mean(r['pv'][k] for r in train_sat) for k in pm.DOM_KEYS],float)
    sd=np.array([statistics.stdev(r['pv'][k] for r in train_sat) for k in pm.DOM_KEYS],float)
    Xu=np.array([[(r['pv'][k]-mu[i])/sd[i] for i,k in enumerate(pm.DOM_KEYS)] for r in hold_uns])
    Xs=np.array([[(r['pv'][k]-mu[i])/sd[i] for i,k in enumerate(pm.DOM_KEYS)] for r in hold_sat])

    match,dists=pm.nearest_unique_match(Xu,Xs,random.Random(188000+q))
    keep=[i for i,d in enumerate(dists) if d<=CALIPER]

    uns=[hold_uns[i] for i in keep]
    sat=[hold_sat[match[i]] for i in keep]
    Xu=np.array([Xu[i] for i in keep])
    Xs=np.array([Xs[match[i]] for i in keep])
    residual=np.mean(np.abs(Xu-Xs),axis=0)

    order=list(range(len(keep)))
    random.Random(199000+q).shuffle(order)
    cut=len(order)//2
    disc=order[:cut]
    ev=order[cut:]

    def eval_lr(X,y,groups):
        tr=np.isin(groups,disc)
        te=np.isin(groups,ev)
        mean=X[tr].mean(0)
        std=X[tr].std(0)
        std[std==0]=1
        Z=(X-mean)/std
        clf=LogisticRegression(max_iter=2000,class_weight='balanced',solver='liblinear')
        clf.fit(Z[tr],y[tr])
        return float(balanced_accuracy_score(y[te],clf.predict(Z[te])))

    Xpair=[]
    ypair=[]
    groups=[]
    for i in range(len(keep)):
        Xpair.extend([Xu[i],Xs[i]])
        ypair.extend([1,0])
        groups.extend([i,i])
    Xpair=np.array(Xpair,float)
    ypair=np.array(ypair)
    groups=np.array(groups)
    pair_bal=eval_lr(Xpair,ypair,groups)

    ckeys=['star_mixed','star_same','star_total','deg_sq','pol_prod_sq']
    Xc=[]
    yc=[]
    gc=[]
    for i in range(len(keep)):
        Xc.extend([[uns[i]['cu'][k] for k in ckeys],
                   [sat[i]['cu'][k] for k in ckeys]])
        yc.extend([1,0])
        gc.extend([i,i])
    cubic_bal=eval_lr(np.array(Xc,float),np.array(yc),np.array(gc))

    cache={}
    allkeys=set()
    for i in range(len(keep)):
        for label,row in ((1,uns[i]),(0,sat[i])):
            counts=pm.triple_orbit_sample(
                row['f'],
                TRIPLE_SAMPLES,
                250000+q*1000+i*2+label
            )
            cache[(i,label)]=counts
            allkeys.update(counts)

    diffs=[]
    for key in allkeys:
        u=np.array([cache[(i,1)].get(key,0) for i in disc],float)
        s=np.array([cache[(i,0)].get(key,0) for i in disc],float)
        pool=np.concatenate([u,s])
        std=pool.std()
        if std>0 and pool.mean()>=1:
            diffs.append((
                abs(u.mean()-s.mean())/std,
                np.sign(u.mean()-s.mean()),
                key,
                u.mean(),
                s.mean(),
                std
            ))
    diffs.sort(reverse=True,key=lambda x:x[0])
    selected=diffs[:TOP_K]

    def score(i,label):
        return sum(
            sign*(cache[(i,label)].get(key,0)-sat_mean)/std
            for _,sign,key,_,sat_mean,std in selected
        )

    du=np.array([score(i,1) for i in disc])
    ds=np.array([score(i,0) for i in disc])
    threshold=(du.mean()+ds.mean())/2
    eu=np.array([score(i,1) for i in ev])
    es=np.array([score(i,0) for i in ev])
    triple_bal=float(((eu>=threshold).mean()+(es<threshold).mean())/2)

    result={
        'q':q,
        'hold_uns':len(hold_uns),
        'caliper_keep':len(keep),
        'keep_frac':len(keep)/len(hold_uns),
        'mean_dist':float(np.mean([dists[i] for i in keep])),
        'max_dist':float(np.max([dists[i] for i in keep])),
        'pair_abs_z':{k:float(residual[i]) for i,k in enumerate(pm.DOM_KEYS)},
        'pair_bal':pair_bal,
        'cubic_bal':cubic_bal,
        'triple_bal':triple_bal
    }
    print(json.dumps(result))
    return result


def main():
    print(json.dumps({
        'validation':pm.validate(),
        'N':N,
        'density':pm.DENSITY,
        'caliper':CALIPER,
        'triple_samples':TRIPLE_SAMPLES
    }))
    for q in Q_VALUES:
        run_q(q)
    print('STATUS=PASS')


if __name__=='__main__':
    main()
