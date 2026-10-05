#!/usr/bin/env python3
"""Finite cut-bottleneck audit. Status: COMPUTATIONAL, not a SAT lower bound."""
from itertools import product
import math, json

def behavior_classes(K, family):
    if family == "ARBITRARY":
        return {tuple(x) for x in product([0,1], repeat=K)}
    if family == "AFFINE_INDEX":
        return {tuple(a ^ (b & (i & 1)) for i in range(K))
                for a,b in product([0,1], repeat=2)}
    if family == "CONSTANT":
        return {tuple([a]*K) for a in [0,1]}
    raise ValueError(family)

out={"status":"COMPUTATIONAL","seed":20261005,"direct_cut":[],"controls":[],"wrapper":[]}
for K in range(2,11):
    for S in range(K+1):
        unresolved=K-S
        out["direct_cut"].append({
            "K":K,"persistent_bits":S,"unresolved":unresolved,
            "persistent_plus_reread":S+unresolved,
            "persistent_plus_recompute_source_crossings":S+unresolved,
            "bound_met":S+unresolved>=K})
    for family in ("ARBITRARY","AFFINE_INDEX","CONSTANT"):
        c=len(behavior_classes(K,family))
        out["controls"].append({
            "K":K,"family":family,"behavior_classes":c,
            "min_cut_information_bits":math.ceil(math.log2(c))})
for rounds in (1,2,4,8,16,32):
    out["wrapper"].append({
        "K":10,"wrapper":"RECOMP_REPEAT","rounds":rounds,
        "raw_source_crossings":10*rounds,
        "continuation_information_bits":10})
print(json.dumps(out,indent=2,sort_keys=True))
