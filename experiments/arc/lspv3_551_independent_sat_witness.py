#!/usr/bin/env python3
"""LSPV-3/551: independent construction/evaluation of the published SAT source.
No use of the original /341 verifier, producer or JavaScript implementation.
Run: python experiments/arc/lspv3_551_independent_sat_witness.py
"""
from itertools import combinations
import json
e=[]
for i,j in combinations(range(4),2):
    if (i,j)!=(0,1): e.append((i,j))
e += [(0,4),(1,4)]
for i in range(3):
    j=(i+1)%3
    if (i,j)!=(0,1):e.append((5+i,5+j))
    e.extend([(8+i,8+j),(5+i,8+i)])
e += [(5,11),(6,11),(4,11)]
e.remove((0,4));e.insert(12,(0,4))
assert len(e)==18
assert [i for i,edge in enumerate(e) if 0 in edge]==[0,1,12]
clauses=[]
for v in range(12):
    inc=[i for i,edge in enumerate(e) if v in edge]
    assert len(inc)==3
    if v==0:
        forbidden=[(0,0,0),(0,0,1),(1,1,0),(1,1,1)]
    else:
        forbidden=[tuple((m>>k)&1 for k in range(3)) for m in range(8) if m.bit_count()%2]
    for bits in forbidden:
        clauses.append(tuple((1 if val==0 else -1)*(edge+1) for val,edge in zip(bits,inc)))
assert len(clauses)==48
witness=[0]*18
for i in (0,2,5,12):witness[i]=1
def holds(c,w):return any(w[abs(lit)-1]==int(lit>0) for lit in c)
assert all(holds(c,witness) for c in clauses)
assert all(sum(witness[i] for i,edge in enumerate(e) if v in edge)%2==0 for v in range(12))
mismatches=[]
for m in range(8):
    a,b,c=[(m>>i)&1 for i in range(3)]
    actual=a^b
    false_alias=a^b^c
    if actual!=false_alias:mismatches.append([a,b,c])
assert len(mismatches)==4
print(json.dumps({"variables":18,"clauses":48,"witness":"".join(map(str,witness)),
                  "satisfied_original_clauses":sum(holds(c,witness) for c in clauses),
                  "local_clause_lits":clauses[:4],"semantic_row_mismatches":mismatches,
                  "source_is_SAT":True},indent=2))
