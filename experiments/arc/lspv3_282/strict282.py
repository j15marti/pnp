#!/usr/bin/env python3
"""GATE282 self-contained no-dependency exact small-source falsifier.
Produces the strict q=3, tau=3, q_ext=2 witness. P vs NP remains OPEN."""
from itertools import combinations
from collections import Counter
P=[(1,2,3),(1,4,5),(2,6,7),(4,6,8),(3,9,10),(5,9,11),(7,10,12),(8,11,12)]
Q=[(1,9,11),(5,7,8),(4,6,10),(3,6,11),(1,2,3),(2,8,12),(4,9,12),(5,7,10)]
F=P+[tuple(-x for x in c) for c in Q]
assert len(F)==16 and len(set(tuple(sorted(c)) for c in F))==16
for v in range(1,13):
    assert sum(v in c for c in F)==sum(-v in c for c in F)==2
ends={v:tuple(j for j,c in enumerate(P) if v in c) for v in range(1,13)}
assert all(len(t)==2 for t in ends.values())
matchings=[]
for M in combinations(range(1,13),4):
    verts=[u for e in M for u in ends[e]]
    if len(set(verts))==8:matchings.append(frozenset(M))
danger=[]
for j,c in enumerate(Q):
    if all(set(ends[a]).isdisjoint(ends[b]) for a,b in combinations(c,2)):
        danger.append((j+8,frozenset(c)))
ext=[(j,D) for j,D in danger if any(D<=M for M in matchings)]
assert [j for j,D in danger]==[9,11,14]
assert len(ext)==2 and set(j for j,D in ext)=={9,14}
assert all(A.isdisjoint(B) for (_,A),(_,B) in combinations(danger,2))
assert not any(all(bool(set(H)&D) for _,D in danger) for H in combinations(range(1,13),2))
found=[M for M in matchings if all(not D<=M for j,D in ext)]
assert frozenset((1,7,8,9)) in found
def sat(mask):
    return all(any(bool(mask & (1<<(abs(v)-1))) == (v>0) for v in c) for c in F)
models=[a for a in range(1<<12) if sat(a)]
assert len(models)==268
assert sat(sum(1<<(v-1) for v in (1,7,8,9)))
print({'n':12,'m':16,'q':len(danger),'tau':3,'q_ext':len(ext),
       'model_count':len(models),'perfect_matching_count':len(matchings),
       'witness':[1,7,8,9],'nonextendible_source_clause':11,'PvsNP':'OPEN'})
