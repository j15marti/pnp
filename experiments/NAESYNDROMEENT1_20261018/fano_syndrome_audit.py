#!/usr/bin/env python3
from itertools import product, combinations
import json

edges=[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
q=7
m=len(edges)

def delta(x):
    out=[]
    for u,v,w in edges:
        out.append(((x[u]^x[w])<<1) | (x[v]^x[w]))
    return tuple(out)

gauge=sorted(set(delta(x) for x in product([0,1], repeat=q)))
assert len(gauge)==2**(q-1)

def add(a,b): return tuple(x^y for x,y in zip(a,b))
def canon(lab): return min(add(lab,g) for g in gauge)
deltas=[delta(x) for x in product([0,1], repeat=q)]

def sat(lab):
    return any(all(d[e]!=lab[e] for e in range(m)) for d in deltas)

cosets={}
for lab in product(range(4), repeat=m):
    c=canon(lab)
    if c not in cosets: cosets[c]={"members":[],"sat":sat(lab)}
    assert cosets[c]["sat"]==sat(lab)
    cosets[c]["members"].append(lab)

assert len(cosets)==256
assert {len(v["members"]) for v in cosets.values()}=={64}
satc=[c for c,v in cosets.items() if v["sat"]]
unsatc=[c for c,v in cosets.items() if not v["sat"]]

def prob(cs,I,vals):
    hit=tot=0
    for c in cs:
        for lab in cosets[c]["members"]:
            tot+=1
            hit += all(lab[i]==v for i,v in zip(I,vals))
    return hit/tot

max1=max(abs(prob(satc,(i,),(a,))-prob(unsatc,(i,),(a,)))
         for i in range(m) for a in range(4))
max2=max(abs(prob(satc,(i,j),(a,b))-prob(unsatc,(i,j),(a,b)))
         for i,j in combinations(range(m),2) for a in range(4) for b in range(4))

max3=0.0
witness=None
for I in combinations(range(m),3):
    for vals in product(range(4), repeat=3):
        ps=prob(satc,I,vals)
        pu=prob(unsatc,I,vals)
        d=abs(ps-pu)
        if d>max3:
            max3=d
            witness={"edges":I,"labels":vals,"sat_prob":ps,"unsat_prob":pu}

block_distance=min(sum(v!=0 for v in g) for g in gauge if any(g))

out={
 "support":"Fano plane",
 "vertices":q,
 "edges":m,
 "gauge_rank":q-1,
 "syndrome_dimension":2*m-(q-1),
 "orbit_size":len(gauge),
 "cosets":len(cosets),
 "sat_cosets":len(satc),
 "unsat_cosets":len(unsatc),
 "block_min_distance":block_distance,
 "max_single_pattern_difference":max1,
 "max_pair_pattern_difference":max2,
 "max_triple_pattern_difference":max3,
 "triple_witness":witness,
}
print(json.dumps(out,indent=2,sort_keys=True))
