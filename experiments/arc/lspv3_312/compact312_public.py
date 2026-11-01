#!/usr/bin/env python3
"""GATE312 compact SAT source-authenticated reproducibility. Standard library only.
Full producer, raw 19,683 cube census, original extrema, flip trails and independent
no-import verification are in the GATE312 ZIP; these are not native FLMV measurements.
"""
from itertools import product,combinations
from collections import Counter
import json
P=("156","238","135","469","247","789")
N=("468","167","234","358","129","579")
F=[tuple(int(c) for c in x) for x in P]+[tuple(-int(c) for c in x) for x in N]
def accepts(bits):
    return all(any(bits[abs(l)-1]==int(l>0) for l in clause) for clause in F)
def agree(bits,p):
    return all(bits[i-1]==v for i,v in p.items())
def fibers(models,p,b=7):
    return [sum(agree(a,p) and a[b-1]==z for a in models) for z in (0,1)]
def empty(p):
    return [j+1 for j,c in enumerate(F) if all(abs(l) in p and p[abs(l)]!=int(l>0) for l in c)]
def check():
    counts=Counter(l for cl in F for l in cl)
    assert len(F)==12 and len(set(F))==12
    assert all(len(set(map(abs,cl)))==3 and len(set(x>0 for x in cl))==1 for cl in F)
    assert all(counts[i]==counts[-i]==2 for i in range(1,10))
    models=[a for a in product((0,1),repeat=9) if accepts(a)]
    assert len(models)==70
    p={1:1,2:0,3:0};q={1:1,2:1,3:0};r={6:1}
    ps=[p,q,p|r,q|r]
    fs=[fibers(models,x) for x in ps]
    assert fs==[[4,4],[4,4],[0,0],[2,0]]
    assert all(not empty(x) for x in ps)
    # An actual 4-source-clause UP refutation, not just two failed endpoints.
    x=dict(p|r)
    for cid,v,b in [(2,8,1),(8,7,0),(5,4,1)]:
        cl=F[cid-1]
        assert v not in x and v in [abs(z) for z in cl]
        assert all(abs(l) in x and x[abs(l)]!=int(l>0)
                   for l in cl if abs(l)!=v)
        x[v]=b
    assert all(abs(l) in x and x[abs(l)]!=int(l>0) for l in F[6])
    assert sum(agree(a,p|r) for a in product((0,1),repeat=9))==32
    assert not any(agree(a,p|r) for a in models)
    compatible=0
    for i,j in combinations(range(12),2):
        for a,b in product(("S","U"),repeat=2):
            targets=[]
            for k,c in ((i,a),(j,b)):
                targets.append({abs(l):int(l>0) if c=="S" else int(l<0) for l in F[k]})
            compatible+=all(v not in targets[1] or targets[1][v]==s
                            for v,s in targets[0].items())
    assert compatible==172
    satc=unsatc=0
    for vals in product((-1,0,1),repeat=9):
        pin={j+1:v for j,v in enumerate(vals) if v>=0}
        if any(agree(a,pin) for a in models):satc+=1
        else:unsatc+=1
    assert (satc,unsatc)==(10508,9175)
    out={"status":"PASS","F9_models":70,"four_fibers":fs,
         "model_counts":[sum(x) for x in fs],
         "UP_source_clause_trace":[2,8,5,7],"compatible_pair_extremes":compatible,
         "coherent_cubes":{"SAT":satc,"UNSAT":unsatc},
         "P_versus_NP":"OPEN"}
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=="__main__":check()
