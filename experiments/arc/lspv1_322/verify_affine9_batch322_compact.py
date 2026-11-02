#!/usr/bin/env python3
"""No producer imports; independent fixture/semantic replay for LSPV-1 322."""
from itertools import combinations
pos=((1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9))
neg=((1,5,9),(2,6,7),(3,4,8),(1,6,8),(2,4,9),(3,5,7))
def accepts(a):
    return all(any(a&(1<<(v-1)) for v in c) for c in pos) and all(not all(a&(1<<(v-1)) for v in c) for c in neg)
models=[a for a in range(512) if accepts(a)]
assert len(models)==18
pairs={}
for c in pos+neg:
    for x,y in combinations(c,2):
        q=tuple(sorted((x,y)));pairs[q]=pairs.get(q,0)+1
assert len(pairs)==36 and all(v==1 for v in pairs.values())
for x in range(1,10):
    links={v for (i,j) in pairs for v in ((j,) if i==x else ((i,) if j==x else ()))}
    assert len(links)==8
for bit,needed in ((0,0),(1,2)):
    assert sum(((a&15)==(14+bit)) for a in models)==needed
counts=[0]*4
for a in range(256):
    b0=accepts(a<<1);b1=accepts((a<<1)|1)
    counts[2*int(b0)+int(b1)]+=1
assert counts==[239,8,8,1]
print('PASS independent 512 original assignments; 36 unique pairs; all 9 degree-8; same-source SAT2/UNSAT0; exact cofactors')
