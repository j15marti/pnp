#!/usr/bin/env python3
"""Independent finite T5 path relation and irredundance check (no solver dependency)."""
from itertools import product
R=lambda a,b: (b-a)%5 in (1,3)
def endpoint(word):
    S={0}
    for c in word:
        S={(x+d)%5 for x in S for d in ((1,3) if c==1 else (2,4))}
    return frozenset(S)
relations=sorted({endpoint(w) for L in range(1,4) for w in product((0,1),repeat=L)}, key=lambda s:(len(s),sorted(s)))
assert len(relations)==9
assert all(endpoint(w)==frozenset(range(5)) for w in product((0,1),repeat=4))
max_irred=0; irredundant_count=0; sharp=0
for mask in range(1,512):
    chosen=[r for i,r in enumerate(relations) if mask>>i&1]
    intersection=set.intersection(*map(set,chosen))
    good=(len(chosen)==1 or all(set.intersection(*map(set,chosen[:i]+chosen[i+1:]))!=intersection for i in range(len(chosen))))
    if good:
        irredundant_count+=1
        if len(chosen)>max_irred:max_irred=len(chosen);sharp=0
        if len(chosen)==max_irred:sharp+=1
assert (max_irred,irredundant_count,sharp)==(4,63,4)
print('PASS: 9 short relations, 512 subsets, 63 irredundant, sharp maximum 4; all length-4 paths universal')
