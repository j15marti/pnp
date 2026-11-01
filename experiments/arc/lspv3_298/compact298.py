#!/usr/bin/env python3
"""LSPV-3 GATE298 compact independent reproducer for the coefficient gate.
The full affine-rank producer and independent no-import verification of 762
cubes are in the GATE298 complete reproducibility archive linked in the report.
This code checks source grammar, odd-cycle parity, exact branch descriptions,
SAT truth tables, and one-defect cases on canonical original sources.
"""
from itertools import product
from collections import Counter
from math import comb
import json

F9=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
F9 += [tuple(-x for x in c) for c in
       [(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]]
Y6=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),
    (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]

def valid(F):
    if not F: return False
    n=max(abs(v) for c in F for v in c)
    if len(F)*3!=4*n:return False
    counts=Counter();seen=set()
    for c in F:
        if len(c)!=3 or len(set(abs(v) for v in c))!=3:return False
        if len(set(v>0 for v in c))!=1:return False
        key=tuple(sorted(c))
        if key in seen:return False
        seen.add(key)
        for v in c:counts[v]+=1
    return all(counts[v]==counts[-v]==2 for v in range(1,n+1))

def state(F,p,cycles):
    n=max(abs(x) for c in F for x in c)
    free=[x for x in range(1,n+1) if x not in p]
    covered_spill=Counter();uncovered=[]
    for j,c in enumerate(F):
        if any(abs(l) in p and p[abs(l)]==int(l>0) for l in c):
            for l in c:
                if abs(l) not in p:covered_spill[l]+=1
        else:
            rest=[l for l in c if abs(l) not in p]
            if not rest:return None
            uncovered.append((j,rest))
    used=set()
    for cycle in cycles:
        assert len(cycle)%2==1 and len(set(cycle))==len(cycle)
        assert not used.intersection(cycle)
        used.update(cycle)
        degrees=Counter()
        for j in cycle:
            rest=[abs(l) for l in F[j] if abs(l) not in p]
            assert len(rest)==2
            degrees.update(rest)
        assert len(degrees)==len(cycle) and all(d==2 for d in degrees.values())
    eta=sum(min(covered_spill[v],covered_spill[-v]) for v in free)
    delta=2*len(free)-len(uncovered)-eta-len(cycles)
    pref={v:(0 if covered_spill[v]>covered_spill[-v] else 1,
             abs(covered_spill[v]-covered_spill[-v]))
          for v in free if covered_spill[v]!=covered_spill[-v]}
    return (free,uncovered,pref,delta,used)

def branch_coefficient(F,p,cycles):
    data=state(F,p,cycles)
    if data is None:return 0,None
    free,uncovered,pref,delta,used=data
    if delta<0:return 0,delta
    groups=[]
    for cy in cycles:
        groups.append({2*j:comb(len(cy),2*j+1)
                       for j in range((len(cy)-1)//2+1)})
    for j,rest in uncovered:
        if j in used:continue
        groups.append({1:{0:1},2:{0:1,1:1},3:{0:1,1:3,2:1}}[len(rest)])
    for _,(_,w) in pref.items():groups.append({0:1,w:1})
    dp={0:1}
    for P in groups:
        nxt=Counter()
        for d,c in dp.items():
            for k,a in P.items():
                if d+k<=delta:nxt[d+k]+=c*a
        dp=dict(nxt)
    return dp.get(delta,0),delta

def brute_and_parity(F,p,cycles):
    data=state(F,p,cycles)
    if data is None:return 0
    free,uncovered,pref,delta,used=data
    models=0
    for bits in product((0,1),repeat=len(free)):
        a={**p,**dict(zip(free,bits))}
        if not all(any(a[abs(l)]==int(l>0) for l in c) for c in F):continue
        models+=1
        charge=0
        for cy in cycles:
            r=sum(sum(a[abs(l)]==int(l>0) for l in F[j] if abs(l) in free)==2 for j in cy)
            assert r%2==1
            charge+=r-1
        for j,rest in uncovered:
            if j not in used:
                charge+=sum(a[abs(l)]==int(l>0) for l in rest)-1
        for v,(b,w) in pref.items():charge+=w*(a[v]!=b)
        assert charge==delta
        if delta<=1:
            for cy in cycles:
                assert sum(sum(a[abs(l)]==int(l>0) for l in F[j] if abs(l) in free)==2 for j in cy)==1
    return models

def main():
    assert valid(Y6) and valid(F9)
    controls=[
      ("F9_U",F9,{8:0,3:0,7:0,6:0,1:1,5:1},[(3,4,10)]),
      ("F9_S",F9,{8:0,3:0,7:0,6:0,1:0,5:1},[]),
      ("Y6_defect1",Y6,{5:0,6:1},[])
    ]
    out={}
    for name,F,p,cycles in controls:
        B,delta=branch_coefficient(F,p,cycles)
        models=brute_and_parity(F,p,cycles)
        out[name]={"delta":delta,"branch_descriptions":B,"exact_original_models":models}
    assert out["F9_U"]=={"delta":0,"branch_descriptions":3,"exact_original_models":0}
    assert out["F9_S"]=={"delta":2,"branch_descriptions":4,"exact_original_models":2}
    assert out["Y6_defect1"]=={"delta":1,"branch_descriptions":8,"exact_original_models":6}
    print(json.dumps({"check":"PASS","controls":out,"P_vs_NP":"OPEN"},indent=2))

if __name__=="__main__":main()
