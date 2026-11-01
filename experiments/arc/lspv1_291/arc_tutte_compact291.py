#!/usr/bin/env python3
"""ARC-TUTTE-CUBE291: self-contained exact original-source Tutte-cube demo.
Python 3 standard library, no imports from the large experimental producer.
This code enumerates small instances OFFLINE and is not an FLMV machine.
For complete 841 certificates and independent U198/V198 replay use run archive.
"""
from itertools import product, combinations
from collections import Counter
import json

Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
    (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
TRI9=((1,2,4),(2,3,5),(1,3,6),(4,7,8),(5,7,9),(6,8,9),
      (-1,-2,-7),(-2,-3,-8),(-1,-3,-9),(-4,-5,-7),
      (-4,-6,-8),(-5,-6,-9))

def canonical(F,n):
    if n<3 or n%3 or len(F)*3!=n*4:return False
    O=Counter()
    seen=set()
    for C in F:
        if len(C)!=3 or len(set(map(abs,C)))!=3:return False
        if not (all(l>0 for l in C) or all(l<0 for l in C)):return False
        if any(not 1<=abs(l)<=n for l in C):return False
        key=tuple(sorted(C))
        if key in seen:return False
        seen.add(key)
        O.update(C)
    return all(O[i]==2 and O[-i]==2 for i in range(1,n+1))

def witness(F,a):
    return all(any(a[abs(l)-1]==int(l>0) for l in C) for C in F)

def requirements(F,p,s):
    return [j for j,C in enumerate(F)
            if (C[0]>0)==(s>0)
            and not any(p[abs(l)-1]==int(l>0) for l in C)]

def graph(F,p,s):
    R=requirements(F,p,s)
    supports={}
    for j in R:
        supports[j]={abs(l) for l in F[j] if p[abs(l)-1]==-1}
        if not supports[j]:return None
    E={(a,b) for a,b in combinations(R,2) if supports[a]&supports[b]}
    return R,E

def odd_parts(R,E,S):
    remaining=set(R)-set(S)
    odd=0
    while remaining:
        start=min(remaining)
        frontier={start}
        component={start}
        while frontier:
            nxt=set()
            for v in frontier:
                for a,b in E:
                    other=b if v==a else a if v==b else None
                    if other in remaining and other not in component:
                        component.add(other);nxt.add(other)
            frontier=nxt
        remaining-=component
        odd+=len(component)%2
    return odd

def best_tutte(F,p,s):
    G=graph(F,p,s)
    if G is None:return None
    R,E=G
    best=-1
    ans=None
    for k in range(len(R)+1):
        for S in combinations(R,k):
            o=odd_parts(R,E,S)
            raw=len(R)+o-k
            assert raw%2==0
            B=raw//2
            if B>best:
                best=B
                ans={"S_original_clause_ids":list(S),"q":len(R),
                     "odd_components":o,"lower_bound":B,
                     "original_required_clause_ids":R}
    return ans

def certify(F,p):
    if not canonical(F,len(p)):return None
    A=best_tutte(F,p,1)
    B=best_tutte(F,p,-1)
    if A is None or B is None:return None
    if A["lower_bound"]+B["lower_bound"]<=p.count(-1):return None
    return {"partial":list(p),"plus":A,"minus":B,
            "free":p.count(-1)}

def manual_check(F,cert):
    if cert is None:return False
    p=tuple(cert["partial"])
    if not canonical(F,len(p)) or cert["free"]!=p.count(-1):return False
    bounds=[]
    for s,key in ((1,"plus"),(-1,"minus")):
        R=requirements(F,p,s)
        S=cert[key]["S_original_clause_ids"]
        G=graph(F,p,s)
        if G is None or len(S)!=len(set(S)) or not set(S)<=set(R):return False
        o=odd_parts(R,G[1],S)
        B=(len(R)+o-len(S))//2
        if B!=cert[key]["lower_bound"] or o!=cert[key]["odd_components"]:return False
        bounds.append(B)
    return sum(bounds)>cert["free"]

def audit(name,F):
    n=max(abs(l) for C in F for l in C)
    assert canonical(F,n)
    models=[a for a in product((0,1),repeat=n) if witness(F,a)]
    count=Counter()
    for p in product((-1,0,1),repeat=n):
        good=any(all(v==-1 or v==a[i] for i,v in enumerate(p)) for a in models)
        count["extendible" if good else "nonextendible"]+=1
        cert=certify(F,p)
        if cert is not None:
            assert manual_check(F,cert) and not good
            count["certified_cubes"]+=1
    return {"source":name,"n":n,"m":len(F),"models":len(models),**dict(count)}

def main():
    rows=[audit("Y6",Y6),audit("TRI9",TRI9)]
    assert [(r["models"],r["extendible"],r["nonextendible"],r["certified_cubes"])
            for r in rows]==[(20,529,200,12),(74,10895,8788,829)]
    p=(-1,-1,-1,0,0,0,1,1,1)
    c=certify(TRI9,p)
    assert c and not c["plus"]["S_original_clause_ids"]
    assert c["minus"]["S_original_clause_ids"]==[]
    assert [c[z]["lower_bound"] for z in ("plus","minus")]==[2,2]
    q=(0,-1,-1,0,-1,0,0,-1,0)
    d=certify(TRI9,q)
    assert d and d["plus"]["S_original_clause_ids"]==[1]
    assert not canonical(TRI9[:-1],9)
    assert not canonical(TRI9+TRI9[:1],9)
    assert not canonical(tuple(TRI9[:1]+((1,3,-6),)+TRI9[2:]),9)
    print(json.dumps({"status":"PASS","offline_exhaustive":True,
                      "sources":rows,"triangle_cut":c,"nonempty_set_cut":d,
                      "physical_FLMV_tapes":"UNMEASURED","A_to_Phi":"OPEN"},
                     indent=2,sort_keys=True))

if __name__=="__main__":
    main()
