#!/usr/bin/env python3
"""TMR-2/096 compact exact-one Q source check; Python stdlib, no external seed.
Proves no asymptotic lower bound. Actual K6 follower enumeration only.
Full audit and 236-deletion replay live in the run's independently archived files.
"""
from itertools import product, combinations
W=((1,3),(2,4),(0,3),(1,4),(0,2))
R=lambda a,b:int(b in W[a])
Q=lambda a,b,c:R(a,b)^R(a,c)
P=lambda a,b,c:R(a,b)&R(a,c)
assert (sum(Q(*x) for x in product(range(5),repeat=3)),
        sum(P(*x) for x in product(range(5),repeat=3)),
        sum(Q(*x)*P(*x) for x in product(range(5),repeat=3)))==(60,20,0)
w=[[sum(Q(h,a,b) for h in range(5)) for b in range(5)] for a in range(5)]
assert all(w[a][a]==0 for a in range(5))
assert set(w[a][b] for a in range(5) for b in range(5) if a!=b)=={2,4}
edges=list(combinations(range(6),2))
counts=[0]*15
colors=[0]*15
for a in product(range(5),repeat=6):
    violated=[i for i,(u,v) in enumerate(edges) if a[u]==a[v]]
    if len(violated)!=1:continue
    e=violated[0]
    colors[e]+=1
    weight=1
    for i,(u,v) in enumerate(edges):
        if i!=e: weight*=w[a[u]][a[v]]
    counts[e]+=weight
assert colors==[120]*15
assert counts==[251658240]*15
# Matching old P is always satisfiable with all followers A, heads C.
assert P(2,0,0)==1
# Every full 5-valued domain passes Q single-clause generalized AC.
for pos in range(3):
    for color in range(5):
        assert any(Q(*(tuple([color if k==pos else
                            (z[k] if k<pos else z[k-1])
                            for k in range(3)])))
                   for z in product(range(5),repeat=2))
print({"status":"PASS","K6_deletions":15,"count_each":counts[0],
       "Q":60,"P":20,"intersection":0,
       "SOURCE_PROBE_THEOREM":"symbolic, see report, NOT established by this test"})
