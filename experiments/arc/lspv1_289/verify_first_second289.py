#!/usr/bin/env python3
"""ARC289 independent all-layer first/second original clause-count moment audit.
No import from third-order C++ producer or localized third-order verifier.
Checks every N0/N1/N2/N3 single and all 16 ordered N_r*N_s moments
on the canonical opposite-label original U198 and V198 pair.
"""
from pathlib import Path
from itertools import product
from collections import Counter
from math import comb
import ast,json
ROOT=Path(__file__).resolve().parents[2]
p=ROOT/'research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt'
raw=p.read_text();U=[tuple(c) for c in ast.literal_eval(raw[raw.index('[['):])]
V=U.copy()
assert (U[2],U[44])==((1,2,197),(33,34,196))
V[2]=(1,2,196);V[44]=(33,34,197)
def valid(F):
    d=Counter(l for C in F for l in C)
    return len(F)==264 and len({tuple(sorted(c)) for c in F})==264 and all(
        len(C)==3 and len({abs(l) for l in C})==3 and
        (all(l>0 for l in C) or all(l<0 for l in C)) for C in F
    ) and all(d[x]==d[-x]==2 for x in range(1,199))
assert valid(U) and valid(V)
def events(F,ids):
    clauses=[F[j] for j in ids]
    names=sorted({abs(l) for C in clauses for l in C})
    H=Counter()
    for b in product((0,1),repeat=len(names)):
        a=dict(zip(names,b))
        counts=tuple(sum(a[abs(l)]==int(l>0) for l in C) for C in clauses)
        H[(counts,len(names),sum(b))]+=1
    return H
changed=(2,44)
first=Counter()
for j in changed:
    for s,F in ((-1,U),(1,V)):
        for ((r,),u,h),v in events(F,(j,)).items():
            first[(r,u,h)]+=s*v
first={key:v for key,v in first.items() if v}
pairs=[(i,j) for i in range(264) for j in range(i+1,264)
       if i in changed or j in changed]
assert len(pairs)==525
second=Counter()
probe_assignments=0
for ids in pairs:
    probe_assignments+=2**len({abs(l) for j in ids for l in U[j]})
    for sign,F in ((-1,U),(1,V)):
        for ((r,s),u,h),v in events(F,ids).items():
            second[(r,s,u,h)]+=sign*v
            second[(s,r,u,h)]+=sign*v
second={key:v for key,v in second.items() if v}
C=lambda n,k:comb(n,k) if 0<=k<=n else 0
for w in range(199):
    D=[sum(v*C(198-u,w-h) for (r,u,h),v in first.items() if r==q)
       for q in range(4)]
    assert D==[0]*4
    for r in range(4):
        for s in range(4):
            t=sum(v*C(198-u,w-h)
                  for (rr,ss,u,h),v in second.items() if rr==r and ss==s)
            assert t+(D[r] if r==s else 0)==0
print(json.dumps({
 "status":"PASS","canonical_grammar":True,"changed_source_clause_ids_1based":[3,45],
 "localized_unordered_pairs":len(pairs),
 "assignment_patterns_to_pair_union_per_source":probe_assignments,
 "nonzero_first_source_histogram_differences":len(first),
 "nonzero_ordered_second_source_histogram_differences":len(second),
 "Hamming_weights":199,"first_moment_assertions":796,
 "ordered_second_moment_assertions":3184,
 "scope":"exact finite source statistics only, no SAT inference"},indent=2))
