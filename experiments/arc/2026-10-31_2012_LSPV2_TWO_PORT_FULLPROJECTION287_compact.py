#!/usr/bin/env python3
"""Independent compact exhaustive audit, six-variable closed M22 two-port theorem.
Python stdlib; no producer imports; all 75^2 target formulas and 337500 two-pin fibers.
P vs NP OPEN. Full 198-variable certificates and physical events in ZIP archive.
"""
from itertools import combinations,product
from collections import Counter
import json
triples=list(combinations(range(6),3))
families=[T for T in combinations(triples,4)
          if all(sum(v in t for t in T)==2 for v in range(6))]
assert len(families)==75
states=list(product((0,1),repeat=6))
positive=[];negative=[]
for T in families:
    positive.append(sum(1<<a for a,b in enumerate(states)
                        if all(any(b[v] for v in t) for t in T)))
    negative.append(sum(1<<a for a,b in enumerate(states)
                        if all(any(not b[v] for v in t) for t in T)))
checks={1:[],2:[],3:[]}
for size in checks:
    for positions in combinations(range(6),size):
        for pattern in product((0,1),repeat=size):
            checks[size].append(sum(1<<a for a,b in enumerate(states)
                if all(b[pos]==bit for pos,bit in zip(positions,pattern))))
minimum={1:64,2:64,3:64};zeros={1:0,2:0,3:0}
minimum_models=64;maximum_models=0
for pm in positive:
    for nm in negative:
        models=pm&nm
        count=models.bit_count()
        minimum_models=min(minimum_models,count)
        maximum_models=max(maximum_models,count)
        for k,masks in checks.items():
            a=[(models&mask).bit_count() for mask in masks]
            minimum[k]=min(minimum[k],min(a))
            zeros[k]+=a.count(0)
assert (minimum_models,maximum_models)==(18,26)
assert minimum[1]==9 and minimum[2]==1
assert zeros=={1:0,2:0,3:56160}
print(json.dumps({'PASS':True,'families':75,'formula_pairs':5625,
 'one_port_cylinders':67500,'two_port_cylinders':337500,
 'one_port_min':minimum[1],'two_port_min':minimum[2],
 'three_port_empty_cylinders':zeros[3],
 'parent_model_range':[minimum_models,maximum_models],
 'ARC_FLMV_and_P_versus_NP':'OPEN'},indent=2))
