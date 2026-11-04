#!/usr/bin/env python3
"""Exhaustive two-variable minimum ordinary-DAG-Resolution cost control."""
from itertools import product,combinations
from collections import deque,Counter

def resolve(a,b):
    for k in (1,2):
        for x,y in ((a,b),(b,a)):
            if k in x and -k in y:
                z=(set(x)|set(y))-{k,-k}
                if not any(-v in z for v in z):yield frozenset(z)

def optimum(src):
    if frozenset() in src:return 0
    st=frozenset(src);queue=deque([(st,0)]);seen={st}
    while queue:
        state,d=queue.popleft()
        for x,y in combinations(state,2):
            for r in resolve(x,y):
                if r in state:continue
                if not r:return d+1
                nxt=state|{r}
                if nxt not in seen:seen.add(nxt);queue.append((nxt,d+1))
    return None

u=[frozenset((i+1)*a for i,a in enumerate(t) if a) for t in product((-1,0,1),repeat=2) if t!=(0,0)]
assert len(u)==8
counts=Counter();sat=unsat=0
for mask in range(1<<len(u)):
    source=frozenset(u[i] for i in range(8) if mask>>i&1)
    models=sum(all(any((bool(a>>(abs(z)-1)&1)==(z>0)) for z in c) for c in source) for a in range(4))
    q=optimum(source)
    assert (models==0)==(q is not None)
    if models: sat+=1
    else: unsat+=1;counts[q]+=1
assert (sat,unsat,dict(counts))==(95,161,{1:112,2:48,3:1})
print({'total':sat+unsat,'SAT':sat,'UNSAT':unsat,'minimal_inference_counts':dict(sorted(counts.items()))})
