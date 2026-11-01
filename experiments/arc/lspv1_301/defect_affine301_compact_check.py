#!/usr/bin/env python3
"""LSPV-1 301: original-source positive-defect affine-budget checks.
Independent finite control using complete assignments, not the producer's GF2
branch enumerator. Run with Python 3 stdlib. No FLMV native machine claim.
"""
from collections import Counter
from itertools import combinations, product
import json

Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
    (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
POS9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
NEG9=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F9=POS9+tuple(tuple(-x for x in c) for c in NEG9)
POS15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),
       (6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
NEG15=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),
       (4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=POS15+tuple(tuple(-x for x in c) for c in NEG15)
PS=dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))
PU=dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0)))
P9={8:0,3:0,7:0,6:0,1:1,5:1}

def grammar(F):
    n=max(abs(x) for c in F for x in c)
    d=Counter(x for c in F for x in c)
    return (3*len(F)==4*n and len(set(tuple(sorted(c)) for c in F))==len(F)
        and all(len(c)==3 and len(set(map(abs,c)))==3
                and (all(x>0 for x in c) or all(x<0 for x in c)) for c in F)
        and all(d[i]==d[-i]==2 for i in range(1,n+1)))

def count(c,a):
    return sum(a[abs(x)]==int(x>0) for x in c)

def gate(F,p):
    n=max(abs(x) for c in F for x in c)
    free=[x for x in range(1,n+1) if x not in p]
    covered=[];uncovered=[]
    for j,c in enumerate(F):
        if any(abs(x) in p and p[abs(x)]==int(x>0) for x in c):
            covered.append(j)
        else:uncovered.append(j)
    if any(all(abs(x) in p for x in F[j]) for j in uncovered):return None
    s=Counter((abs(x),int(x>0)) for j in covered for x in F[j]
              if abs(x) in free)
    eta=sum(min(s[v,0],s[v,1]) for v in free)
    weights={v:abs(s[v,1]-s[v,0]) for v in free if s[v,1]!=s[v,0]}
    pref={v:int(s[v,0]>s[v,1]) for v in weights}
    edges={}
    for j in uncovered:
        remain=tuple(sorted(abs(x) for x in F[j] if abs(x) in free))
        if len(remain)==2:edges.setdefault(remain,[]).append(j)
    tris=[]
    for a,b,c in combinations(free,3):
        if all(pair in edges for pair in ((a,b),(a,c),(b,c))):
            for ids in product(edges[a,b],edges[a,c],edges[b,c]):
                tris.append(tuple(sorted(ids)))
    chosen=[];used=set()
    for cyc in sorted(set(tris)):
        if not used.intersection(cyc):
            chosen.append(cyc);used.update(cyc)
    e=2*len(free)-len(uncovered)
    return free,uncovered,covered,weights,pref,chosen,e,eta,e-eta-len(chosen)

def models(F,p):
    n=max(abs(x) for c in F for x in c)
    free=[v for v in range(1,n+1) if v not in p]
    for bits in product((0,1),repeat=len(free)):
        a=dict(p);a.update(zip(free,bits))
        if all(count(c,a)>=1 for c in F):yield a

def check(F,p,expected_delta,expected_models):
    assert grammar(F)
    g=gate(F,p)
    assert g is not None
    free,uncovered,covered,w,pref,cycles,e,eta,d=g
    assert d==expected_delta
    A=list(models(F,p));assert len(A)==expected_models
    sigs=[]
    for a in A:
        t={j:count(F[j],a) for j in uncovered}
        assert all(t[j]>=1 for j in uncovered)
        overfull={j for j in uncovered if t[j]>=2}
        baseline=[]
        for cyc in cycles:
            hits=[j for j in cyc if j in overfull]
            assert hits
            baseline.append(min(hits))
        extras=overfull-set(baseline)
        defect=sum(t[j]-1 for j in extras)
        spilled=sum(z for v,z in w.items() if a[v]!=pref[v])
        assert defect+spilled==d
        assert all(t[j]==1 for j in uncovered if j not in overfull)
        # The exact affine branch is uniquely specified by overfull true-patterns,
        # the first both-true edge per packed cycle, and signed mismatches.
        pattern=tuple(sorted((j,tuple(sorted(
            abs(x) for x in F[j] if abs(x) in free
            and a[abs(x)]==int(x>0)))) for j in extras))
        key=(tuple(baseline),pattern,tuple(v for v in sorted(w)
             if a[v]!=pref[v]))
        sigs.append(key)
    return {'delta':d,'nu':len(cycles),'models':len(A),
            'distinct_branch_signatures':len(set(sigs))}

def main():
    assert all(grammar(F) for F in (Y6,F9,F15))
    cases={
       'F15_S_delta1':check(F15,{**PS,2:0,6:0},1,1),
       'F15_U_delta1':check(F15,{**PU,2:0,6:0},1,0),
       'F9_U_delta0':check(F9,P9,0,0),
       'Y6_S_delta1':check(Y6,{5:0,6:1},1,6),
       'Y6_S_delta2':check(Y6,{4:0,6:1},2,6)}
    assert sum(1 for _ in models(Y6,{}))==20
    print(json.dumps({'status':'PASS','cases':cases,
          'method':'independent exhaustive original-source control',
          'no_claim':'no polynomial all-input solver, no ARC/FLMV transfer'},indent=2))
if __name__=='__main__':main()
