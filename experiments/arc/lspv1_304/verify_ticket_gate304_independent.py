#!/usr/bin/env python3
"""Independent source-truth verifier for ARC-TICKET-GATE-AMPLIFICATION304.
Does not import the producer, and does not use a source SAT oracle.
Full test battery with assertion ledger is in the reproducibility archive.
"""
from itertools import product, combinations
from collections import Counter
from math import comb
import json

F=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
   (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
P={5:0,6:1,7:0,8:0,9:1}
Q={**P,3:1}
U={8:0,3:0,7:0,6:0,1:1,5:1}
S={**U,1:0}

def truth(c,a):
    return sum(a[abs(l)]==int(l>0) for l in c)
def completions(p):
    free=[x for x in range(1,10) if x not in p]
    for bits in product((0,1),repeat=len(free)):
        a={**p,**dict(zip(free,bits))}
        if all(truth(c,a)>0 for c in F):
            yield tuple(a[x] for x in range(1,10))
def ticket(p,pref,extra,cycle_edge=None):
    cov={j for j,c in enumerate(F)
         if any(abs(l) in p and p[abs(l)]==int(l>0) for l in c)}
    free=[x for x in range(1,10) if x not in p]
    result=set()
    for bits in product((0,1),repeat=len(free)):
        a={**p,**dict(zip(free,bits))}
        if any(a[x]!=b for x,b in pref.items()):continue
        if all(truth(c,a)==(2 if j==cycle_edge or j in extra else 1)
               for j,c in enumerate(F) if j not in cov):
            result.add(tuple(a[x] for x in range(1,10)))
    return result

def main():
    ct=Counter(l for c in F for l in c)
    assert all(ct[x]==ct[-x]==2 for x in range(1,10))
    assert len({tuple(sorted(c)) for c in F})==12
    assert all(len(set(map(abs,c)))==3 for c in F)
    assert len(list(completions({})))==70
    parent=set(completions(P));child=set(completions(Q))
    assert parent==child and len(parent)==3
    assert not set(completions(U)) and len(list(completions(S)))==2
    assert all(a[2]==1 for a in parent)
    # Original-source unit derived from IDs 1,10 then ID 2.
    # (x2 v x3), (~x1 v ~x2) -> (x3 v ~x1),
    # then (x1 v x3) -> (x3).
    assert tuple(l for l in F[1] if abs(l) not in P)==(2,3)
    assert tuple(l for l in F[10] if abs(l) not in P)==(-1,-2)
    assert tuple(l for l in F[2] if abs(l) not in P)==(1,3)
    pbranches=[ticket(P,{3:1},set(),j) for j in (1,2,10)]
    assert len(pbranches)==3
    assert set.union(*pbranches)==parent and sum(map(len,pbranches))==3
    qbranches=[ticket(Q,{1:0,2:0},{j}) for j in (4,8,10)]
    qbranches += [ticket(Q,{1:1,2:0},set()),
                  ticket(Q,{1:0,2:1},set())]
    assert len(qbranches)==5
    assert set.union(*qbranches)==child and sum(map(len,qbranches))==3
    assert [len(x) for x in qbranches].count(0)==2
    modes=Counter();checked=0
    for j,k in combinations(range(12),2):
        C,D=F[j],F[k]
        vs=sorted(set(map(abs,C+D)))
        masks={(truth(C,dict(zip(vs,bits))),truth(D,dict(zip(vs,bits))))
              for bits in product((0,1),repeat=len(vs))}
        got=tuple((v,w) in masks for v,w in ((3,3),(3,0),(0,3),(0,0)))
        shared=set(map(abs,C))&set(map(abs,D))
        expected=((True,)*4 if not shared else
                  (True,False,False,True) if C[0]*D[0]>0 else
                  (False,True,True,False))
        assert got==expected
        modes[''.join(str(int(v)) for v in got)]+=1;checked+=4
    assert checked==264
    for bits in product((0,1),repeat=9):
        a=dict(enumerate(bits,1))
        a2={x:1-b for x,b in a.items()}
        assert all(truth(c,a)+truth(c,a2)==3 for c in F)
    for t in range(1,9):
        assert comb(5*t,t)>=5**t
        assert 5*t*3**(t-1)>3**t
    out=dict(status="PASS",label="COMPUTATIONAL",
             original_F9_models=70,same_source_SAT_models=3,
             same_source_UNSAT_SAT=[0,2],
             parent_ticket_models=[len(z) for z in pbranches],
             child_ticket_models=[len(z) for z in qbranches],
             source_pair_extreme_flags_checked=checked,
             compatibility_hist=dict(modes),
             P_vs_NP="OPEN")
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=="__main__":main()
