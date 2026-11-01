#!/usr/bin/env python3
"""Independent original-source 198-variable U/V SAT-label control for ARC289.
Recompute only triples touching changed original clause indices; independent
of C++ histogram producer. U/V labels come from separately checked original
UNSAT certificate and SAT witness, NOT from these moment measurements.
Run: python experiments/arc/lspv1_289/verify_triple_moments289.py
"""
from itertools import combinations
from collections import Counter
from math import comb
from pathlib import Path
import ast, json
ROOT=Path(__file__).resolve().parents[2]
source=ROOT/'research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt'
raw=source.read_text();U=[tuple(c) for c in ast.literal_eval(raw[raw.index('[['):])]
V=U.copy()
assert (U[2],U[44])==((1,2,197),(33,34,196))
V[2]=(1,2,196);V[44]=(33,34,197)
def valid(F):
    d=Counter(l for c in F for l in c)
    return (len(F)==264 and len({tuple(sorted(c)) for c in F})==264 and
        all(len(c)==3 and len({abs(l) for l in c})==3 and
            (all(l>0 for l in c) or all(l<0 for l in c)) for c in F)
        and all(d[x]==d[-x]==2 for x in range(1,199)))
assert valid(U) and valid(V)
def extreme(F,ids,mode):
    a={}
    for bit,j in enumerate(ids):
        use_U=(mode>>bit)&1
        for l in F[j]:
            x=abs(l);b=int((l>0)^bool(use_U))
            if x in a and a[x]!=b:return None
            a[x]=b
    return mode.bit_count(),len(a),sum(a.values())
delta=Counter();triples=set()
for changed in (2,44):
    others=(i for i in range(264) if i!=changed)
    for pair in combinations(others,2):
        ids=tuple(sorted((changed,*pair)))
        if ids in triples:continue
        triples.add(ids)
        for mode in range(8):
            a=extreme(U,ids,mode);b=extreme(V,ids,mode)
            if a is not None:delta[a]-=1
            if b is not None:delta[b]+=1
delta={k:v for k,v in delta.items() if v}
expected=[
 (0,8,3,-1),(0,9,3,1),
 (1,6,0,-1),(1,7,0,3),(1,8,0,-3),(1,8,5,-2),(1,9,0,1),(1,9,6,2),
 (2,6,6,-1),(2,7,7,3),(2,8,3,-2),(2,8,8,-3),(2,9,3,2),(2,9,9,1),
 (3,8,5,-1),(3,9,6,1)]
assert sorted((*key,val) for key,val in delta.items())==expected
def C(n,k):return comb(n,k) if 0<=k<=n else 0
for w in range(199):
    for k in range(4):
        numerator=sum(v*C(198-u,w-h) for (kk,u,h),v in delta.items() if kk==k)
        target=(
            -C(189,w-4),
            -C(189,w-3)-2*C(189,w-5),
            -C(189,w-6)-2*C(189,w-4),
            -C(189,w-5))[k]
        assert numerator==target,(w,k)
print(json.dumps({
    "status":"PASS","correct_canonical_grammar":True,"changed_original_clause_indices_one_based":[3,45],
    "localized_clause_triples":len(triples),"localized_mode_patterns":8*len(triples),
    "nonzero_histogram_delta_bins":len(delta),"closed_form_checks":199*4,
    "delta_bins":[list(k)+[v] for k,v in sorted(delta.items())],
    "note":"No SAT decision; original full label certificates independently verified elsewhere."
},indent=2))
