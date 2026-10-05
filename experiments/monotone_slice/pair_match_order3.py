from __future__ import annotations
from itertools import combinations, permutations
from math import comb
import random, statistics, json, time
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score

Q_VALUES=(20,24,28,32)
N=6000
DENSITY=3.5
BASE_SEED=73100
TRIPLE_SAMPLES=400
TOP_K=8
Clause=tuple[int,int,int]
PERMS=list(permutations(range(3)))
PAIR_KEYS=['00','10','11','20','21','22','31','32','33']
DOM_KEYS=['00','10','11','20','21','22']


def gen_clause(q,rng):
    vs=rng.sample(range(q),3)
    lits=[(v+1) if rng.getrandbits(1) else -(v+1) for v in vs]
    return tuple(sorted(lits,key=abs))


def gen_formula(q,t,rng):
    s=set()
    while len(s)<t:
        s.add(gen_clause(q,rng))
    return tuple(sorted(s))


def simplify(clauses,var,val):
    tl=var if val else -var
    fl=-tl
    out=[]
    for c in clauses:
        if tl in c:
            continue
        if fl in c:
            nc=tuple(l for l in c if l!=fl)
            if not nc:
                return None
            out.append(nc)
        else:
            out.append(c)
    return tuple(out)


def dpll_sat(clauses):
    def rec(cs):
        while True:
            if not cs:
                return True
            unit=None
            for c in cs:
                if len(c)==0:
                    return False
                if len(c)==1:
                    unit=c[0]
                    break
            if unit is None:
                break
            cs=simplify(cs,abs(unit),unit>0)
            if cs is None:
                return False
        pol={}
        for c in cs:
            for l in c:
                v=abs(l)
                pol[v]=pol.get(v,0)|(1 if l>0 else 2)
        for v,m in pol.items():
            if m in (1,2):
                rr=simplify(cs,v,m==1)
                return False if rr is None else rec(rr)
        c=min(cs,key=len)
        l=c[0]
        v=abs(l)
        a=simplify(cs,v,l>0)
        if a is not None and rec(a):
            return True
        b=simplify(cs,v,l<0)
        return b is not None and rec(b)
    return rec(tuple(clauses))


def brute_sat(f,q):
    for a in range(1<<q):
        ok=True
        for c in f:
            if not any(((a>>(abs(l)-1))&1)==(1 if l>0 else 0) for l in c):
                ok=False
                break
        if ok:
            return True
    return False


def validate():
    rng=random.Random(99174)
    n=0
    for q in range(4,9):
        for _ in range(50):
            t=rng.randint(1,min(4*q,8*comb(q,3)))
            f=gen_formula(q,t,rng)
            assert dpll_sat(f)==brute_sat(f,q)
            n+=1
    return n


def c2(x):
    return x*(x-1)//2


def c3(x):
    return x*(x-1)*(x-2)//6


def features(f,q):
    pos=[0]*q
    neg=[0]*q
    pair_groups={}
    triple_groups={}
    for c in f:
        vs=tuple(abs(l)-1 for l in c)
        sg={abs(l)-1:(1 if l>0 else -1) for l in c}
        for l in c:
            if l>0:
                pos[l-1]+=1
            else:
                neg[-l-1]+=1
        for a,b in combinations(vs,2):
            if a>b:
                a,b=b,a
            pair_groups.setdefault((a,b),[]).append((sg[a],sg[b]))
        key=tuple(sorted(vs))
        triple_groups.setdefault(key,[]).append(tuple(sg[v] for v in key))

    s3=[0,0,0,0]
    for arr in triple_groups.values():
        for x,y in combinations(arr,2):
            h=sum(a!=b for a,b in zip(x,y))
            s3[h]+=1

    raw2=[0,0,0]
    for arr in pair_groups.values():
        for x,y in combinations(arr,2):
            h=(x[0]!=y[0])+(x[1]!=y[1])
            raw2[h]+=1

    exact2=raw2[:]
    for h,count in enumerate(s3):
        if not count:
            continue
        exact2[0]-=count*c2(3-h)
        exact2[1]-=count*h*(3-h)
        exact2[2]-=count*c2(h)

    raw1_same=sum(c2(a)+c2(b) for a,b in zip(pos,neg))
    raw1_opp=sum(a*b for a,b in zip(pos,neg))
    ex1_same=raw1_same
    ex1_opp=raw1_opp
    for h,count in enumerate(exact2):
        ex1_same-=count*(2-h)
        ex1_opp-=count*h
    for h,count in enumerate(s3):
        ex1_same-=count*(3-h)
        ex1_opp-=count*h

    used=ex1_same+ex1_opp+sum(exact2)+sum(s3)
    s0=c2(len(f))-used
    pv={
        '00':s0,'10':ex1_same,'11':ex1_opp,
        '20':exact2[0],'21':exact2[1],'22':exact2[2],
        '31':s3[1],'32':s3[2],'33':s3[3]
    }
    cubic={
        'star_mixed':sum(c2(a)*b+a*c2(b) for a,b in zip(pos,neg)),
        'star_same':sum(c3(a)+c3(b) for a,b in zip(pos,neg)),
        'star_total':sum(c3(a+b) for a,b in zip(pos,neg)),
        'deg_sq':sum((a+b)**2 for a,b in zip(pos,neg)),
        'pol_prod_sq':sum((a*b)**2 for a,b in zip(pos,neg)),
    }
    return pv,cubic


def canonical_triple(cset):
    best=None
    for p in PERMS:
        d={}
        for j,idx in enumerate(p):
            for l in cset[idx]:
                v=abs(l)
                s=1 if l>0 else -1
                if v not in d:
                    d[v]=[0,0,0]
                d[v][j]=s
        pats=[]
        for vec in d.values():
            a=tuple(vec)
            b=tuple(-x for x in vec)
            pats.append(a if a<b else b)
        key=tuple(sorted(pats))
        if best is None or key<best:
            best=key
    return best


def triple_orbit_sample(f,nsamp,seed):
    rng=random.Random(seed)
    n=len(f)
    counts={}
    for _ in range(nsamp):
        i,j,k=rng.sample(range(n),3)
        key=canonical_triple((f[i],f[j],f[k]))
        counts[key]=counts.get(key,0)+1
    return counts


def nearest_unique_match(Xu,Xs,rng):
    order=list(range(len(Xu)))
    rng.shuffle(order)
    unused=set(range(len(Xs)))
    match=[None]*len(Xu)
    dists=[None]*len(Xu)
    for i in order:
        ids=np.fromiter(unused,dtype=int)
        ds=((Xs[ids]-Xu[i])**2).sum(axis=1)
        jloc=int(np.argmin(ds))
        j=int(ids[jloc])
        match[i]=j
        dists[i]=float(ds[jloc]**0.5)
        unused.remove(j)
    return match,dists


def run_q(q):
    t=round(DENSITY*q)
    rng=random.Random(BASE_SEED+q)
    rows=[]
    start=time.time()
    for _ in range(N):
        f=gen_formula(q,t,rng)
        pv,cu=features(f,q)
        rows.append({'f':f,'sat':dpll_sat(f),'pv':pv,'cu':cu})

    half=N//2
    train=rows[:half]
    hold=rows[half:]
    train_sat=[r for r in train if r['sat']]
    hold_sat=[r for r in hold if r['sat']]
    hold_uns=[r for r in hold if not r['sat']]

    mu=np.array([statistics.mean(r['pv'][k] for r in train_sat) for k in DOM_KEYS],float)
    sd=np.array([statistics.stdev(r['pv'][k] for r in train_sat) for k in DOM_KEYS],float)
    Xu=np.array([[(r['pv'][k]-mu[i])/sd[i] for i,k in enumerate(DOM_KEYS)] for r in hold_uns])
    Xs=np.array([[(r['pv'][k]-mu[i])/sd[i] for i,k in enumerate(DOM_KEYS)] for r in hold_sat])
    match,dists=nearest_unique_match(Xu,Xs,random.Random(88000+q))
    matched_sat=[hold_sat[j] for j in match]
    pair_abs=np.mean(np.abs(Xu-np.array([Xs[j] for j in match])),axis=0)

    m=len(hold_uns)
    order=list(range(m))
    random.Random(99000+q).shuffle(order)
    cut=m//2
    disc=order[:cut]
    ev=order[cut:]

    Xpair=[]
    ypair=[]
    groups=[]
    for i in range(m):
        Xpair.append(Xu[i]); ypair.append(1); groups.append(i)
        Xpair.append(Xs[match[i]]); ypair.append(0); groups.append(i)
    Xpair=np.array(Xpair)
    ypair=np.array(ypair)
    groups=np.array(groups)
    trmask=np.isin(groups,disc)
    temask=np.isin(groups,ev)
    pc=LogisticRegression(max_iter=2000,class_weight='balanced',solver='liblinear').fit(Xpair[trmask],ypair[trmask])
    pbal=balanced_accuracy_score(ypair[temask],pc.predict(Xpair[temask]))

    ckeys=['star_mixed','star_same','star_total','deg_sq','pol_prod_sq']
    Xc=[]
    yc=[]
    gc=[]
    for i in range(m):
        Xc.append([hold_uns[i]['cu'][k] for k in ckeys]); yc.append(1); gc.append(i)
        Xc.append([matched_sat[i]['cu'][k] for k in ckeys]); yc.append(0); gc.append(i)
    Xc=np.array(Xc,float)
    yc=np.array(yc)
    cmu=Xc[trmask].mean(axis=0)
    csd=Xc[trmask].std(axis=0)
    csd[csd==0]=1
    Xcz=(Xc-cmu)/csd
    cc=LogisticRegression(max_iter=2000,class_weight='balanced',solver='liblinear').fit(Xcz[trmask],yc[trmask])
    cbal=balanced_accuracy_score(yc[temask],cc.predict(Xcz[temask]))

    tri_cache={}
    allkeys=set()
    for i in range(m):
        for label,r in ((1,hold_uns[i]),(0,matched_sat[i])):
            cnt=triple_orbit_sample(r['f'],TRIPLE_SAMPLES,120000+q*1000+i*2+label)
            tri_cache[(i,label)]=cnt
            allkeys.update(cnt)

    diffs=[]
    for key in sorted(allkeys):
        u=np.array([tri_cache[(i,1)].get(key,0) for i in disc],float)
        s=np.array([tri_cache[(i,0)].get(key,0) for i in disc],float)
        pool=np.concatenate([u,s])
        sdv=pool.std()
        if sdv>0 and pool.mean()>=1:
            diffs.append((abs(u.mean()-s.mean())/sdv,np.sign(u.mean()-s.mean()),key,u.mean(),s.mean(),sdv))
    diffs.sort(reverse=True,key=lambda x:x[0])
    sel=diffs[:TOP_K]

    def score(i,label):
        return sum(sg*(tri_cache[(i,label)].get(key,0)-sm)/sdv
                   for _,sg,key,_,sm,sdv in sel)

    du=np.array([score(i,1) for i in disc])
    ds=np.array([score(i,0) for i in disc])
    threshold=(du.mean()+ds.mean())/2
    eu=np.array([score(i,1) for i in ev])
    es=np.array([score(i,0) for i in ev])
    tpr=float((eu>=threshold).mean())
    tnr=float((es<threshold).mean())
    tbal=(tpr+tnr)/2

    result={
        'q':q,'t':t,'N':N,'hold_uns':m,'hold_sat':len(hold_sat),
        'match_dist_mean':float(np.mean(dists)),
        'match_dist_max':float(np.max(dists)),
        'pair_abs_z':{k:float(pair_abs[i]) for i,k in enumerate(DOM_KEYS)},
        'pair_bal_acc_eval':float(pbal),
        'cubic_bal_acc_eval':float(cbal),
        'triple_bal_acc_eval':float(tbal),
        'triple_tpr':tpr,'triple_tnr':tnr,
        'top_triple':[(float(a),int(sg),repr(key),float(um),float(sm),float(sdv))
                      for a,sg,key,um,sm,sdv in sel],
        'elapsed':time.time()-start
    }
    print(json.dumps(result))
    return result


def main():
    print(json.dumps({
        'validation':validate(),
        'N':N,
        'density':DENSITY,
        'triple_samples':TRIPLE_SAMPLES,
        'top_k':TOP_K
    }))
    for q in Q_VALUES:
        run_q(q)
    print('STATUS=PASS')


if __name__=='__main__':
    main()
