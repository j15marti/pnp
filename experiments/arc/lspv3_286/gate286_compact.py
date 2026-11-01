#!/usr/bin/env python3
"""GATE286 compact, independent standard-library adversarial control.
The full 20-source producer and independent verifier are in the complete ZIP."""
from itertools import combinations, product
from collections import Counter

F = [
    (1,2,3),(1,4,5),(2,6,7),(4,6,8),
    (3,9,10),(5,9,11),(7,10,12),(8,11,12),
    (-1,-9,-11),(-5,-7,-8),(-4,-6,-10),(-3,-6,-11),
    (-1,-2,-3),(-2,-8,-12),(-4,-9,-12),(-5,-7,-10)
]
N = 12

def grammar(F, n):
    h=Counter()
    seen=set()
    if len(F)*3!=n*4: return False
    for C in F:
        if len(C)!=3 or len(set(map(abs,C)))!=3: return False
        if not (all(x>0 for x in C) or all(x<0 for x in C)):return False
        if any(abs(x)<1 or abs(x)>n for x in C):return False
        key=tuple(sorted(C))
        if key in seen:return False
        seen.add(key)
        h.update(C)
    return all(h[i]==2 and h[-i]==2 for i in range(1,n+1))

def sat(a):
    return all(any(a[abs(l)-1]==int(l>0) for l in C) for C in F)

def needed(p, positive):
    r=[]
    for j,C in enumerate(F):
        if (C[0]>0)!=positive:continue
        if any(p[abs(l)-1]==int(positive) for l in C if p[abs(l)-1] is not None):continue
        r.append((j,{abs(l) for l in C if p[abs(l)-1] is None}))
    return r

def exact_min_cover(p,positive):
    R=needed(p,positive)
    if any(len(V)==0 for _,V in R):return float("inf")
    free=[i+1 for i,a in enumerate(p) if a is None]
    for k in range(len(free)+1):
        for S in combinations(free,k):
            if all(set(S).intersection(V) for _,V in R):return k
    return float("inf")

def main():
    assert grammar(F,N)
    p=[0,0,1]+[None]*9
    w=8
    plus=exact_min_cover(p,True)
    minus=exact_min_cover(p,False)
    assert (plus,minus)==(3,3)
    assert {j for j,_ in needed(p,False)}=={9,10,11,14,15}
    assert minus>N-w-p.count(0) and plus+minus<=p.count(None)
    weights=Counter()
    rejected=0
    for a in product((0,1),repeat=N):
        is_sat=sat(a)
        if is_sat:weights[sum(a)]+=1
        if sum(a)==w and all(p[i] is None or p[i]==a[i] for i in range(N)):
            rejected+=1
            assert not is_sat
    assert sum(weights.values())==268 and weights[8]==5
    assert rejected>0
    assert not grammar(F[:1],N)
    print({"status":"PASS","label":"SAT","models":268,"weight8_models":5,
           "partial_weight8_slice":"UNSAT",
           "tau_positive":plus,"tau_negative":minus,
           "old_unweighted_cut_applies":False,
           "full_formula_UNSAT":False})
if __name__=="__main__": main()
