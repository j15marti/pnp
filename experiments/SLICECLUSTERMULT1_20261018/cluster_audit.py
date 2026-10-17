#!/usr/bin/env python3
import itertools, json, math, random
from collections import defaultdict
from pathlib import Path

SEED=20261018
random.seed(SEED)

def spread_ok(G, rho):
    G=[frozenset(x) for x in G]
    if not G: return True
    w=len(next(iter(G)))
    assert all(len(x)==w for x in G)
    L=len(G)
    universe=sorted(set().union(*G)) if G else []
    for a in range(0,w+1):
        for A in itertools.combinations(universe,a):
            A=set(A)
            d=sum(A.issubset(T) for T in G)
            if d > L*(rho**(-a))+1e-12:
                return False
    return True

def decompose_uniform(H, rho, core=frozenset()):
    H=[frozenset(x) for x in H]
    if not H: return []
    w=len(H[0])
    assert all(len(x)==w for x in H)
    if spread_ok(H,rho):
        return [(frozenset(core),w,H)]
    universe=sorted(set().union(*H))
    witness=None
    for a in range(1,w+1):
        for A_t in itertools.combinations(universe,a):
            A=frozenset(A_t)
            d=sum(A.issubset(T) for T in H)
            if d > len(H)*(rho**(-a))+1e-12:
                witness=A; break
        if witness is not None: break
    assert witness is not None
    Hyes=[T-witness for T in H if witness.issubset(T)]
    Hno=[T for T in H if not witness.issubset(T)]
    out=[]
    out += decompose_uniform(Hyes,rho,core|witness)
    out += decompose_uniform(Hno,rho,core)
    return out

def decompose(F,rho):
    by_w=defaultdict(list)
    for T in F: by_w[len(T)].append(frozenset(T))
    raw=[]
    for w,H in by_w.items(): raw+=decompose_uniform(H,rho)
    merged={}
    for C,w,G in raw:
        key=(C,w)
        merged.setdefault(key,set()).update(G)
    clusters=[]
    for (C,w),Gs in merged.items():
        G=list(Gs)
        assert spread_ok(G,rho)
        clusters.append((C,w,G))
    return clusters

def represented_terms(clusters):
    out=set()
    for C,w,G in clusters:
        for R in G: out.add(C|R)
    return out

def cluster_event(C,G,X):
    if not C.issubset(X): return False
    XR=X-C
    return any(R.issubset(XR) for R in G)

def exact_prob_family(F,N,t):
    xs=list(itertools.combinations(range(N),t))
    hit=0
    for x in xs:
        X=set(x)
        if any(set(T).issubset(X) for T in F): hit+=1
    return hit/len(xs)

def cluster_prob(C,G,N,t):
    xs=list(itertools.combinations(range(N),t))
    hit=0
    for x in xs:
        if cluster_event(C,G,set(x)): hit+=1
    return hit/len(xs)

def multiplicity_bound(t,W):
    return sum((W-c+1)*math.comb(t,c) for c in range(W+1))

def spread_second_moment_bound(C,w,G,N,t,rho):
    c=len(C); tc=t-c; Nc=N-c
    if w==0: return 1.0,1.0
    if w>tc/2: return None,None
    p=tc/Nc
    c0=math.exp(-w*(w-1)/tc)
    L=len(G); lam=L*(p**w); theta=rho*p
    lb=c0*c0*lam/(1+math.exp(w/theta)*lam)
    rem=[i for i in range(N) if i not in C]
    xs=list(itertools.combinations(rem,tc))
    hit=0
    for x in xs:
        X=set(x)
        if any(set(R).issubset(X) for R in G): hit+=1
    ex=hit/len(xs)
    return lb,ex

def main():
    tests=[]; failures=[]; assertions=0
    for N,t,W,rho in [(8,3,2,2.0),(9,4,3,2.0),(10,4,3,2.5)]:
        all_terms=[frozenset(c) for w in range(1,W+1) for c in itertools.combinations(range(N),w)]
        for rep in range(40):
            F=set(random.sample(all_terms, random.randint(1,min(len(all_terms),25))))
            clusters=decompose(F,rho)
            assertions+=1
            if represented_terms(clusters)!=F: failures.append(['partition',N,t,W,rep])
            keys=[(C,w) for C,w,G in clusters]
            assertions+=1
            if len(keys)!=len(set(keys)): failures.append(['unique_keys',N,t,W,rep])
            assertions+=len(clusters)
            for C,w,G in clusters:
                if not spread_ok(G,rho): failures.append(['spread',N,t,W,rep,list(C),w])
            M=multiplicity_bound(t,W)
            xs=list(itertools.combinations(range(N),t))
            maxhit=0
            for x in xs:
                X=set(x)
                h=sum(cluster_event(C,G,X) for C,w,G in clusters)
                maxhit=max(maxhit,h)
                assertions+=1
                if h>M: failures.append(['multiplicity',N,t,W,rep,h,M])
            eta=exact_prob_family(F,N,t)
            sumcp=sum(cluster_prob(C,G,N,t) for C,w,G in clusters)
            assertions+=1
            if sumcp>M*eta+1e-12: failures.append(['sum_cluster_prob',N,t,W,rep,sumcp,M*eta])
            checked=0
            for C,w,G in clusters:
                lb,ex=spread_second_moment_bound(C,w,G,N,t,rho)
                if lb is not None:
                    assertions+=1; checked+=1
                    if ex+1e-12<lb: failures.append(['second_moment',N,t,W,rep,float(lb),float(ex)])
            tests.append({'N':N,'t':t,'W':W,'rho':rho,'rep':rep,'clusters':len(clusters),'max_hit':maxhit,'multiplicity_bound':M,'eta':eta,'sum_cluster_probs':sumcp,'second_moment_clusters':checked})
    out={'status':'PASS' if not failures else 'FAIL','seed':SEED,'assertions':assertions,'failures':failures,'tests':tests}
    p=Path('cluster_audit.json');p.write_text(json.dumps(out,indent=2,sort_keys=True))
    print(json.dumps({'status':out['status'],'assertions':assertions,'failures':len(failures),'num_tests':len(tests),'max_clusters':max(x['clusters'] for x in tests),'max_hit':max(x['max_hit'] for x in tests)},indent=2))
    if failures: raise SystemExit(1)
if __name__=='__main__': main()
