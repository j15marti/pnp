#!/usr/bin/env python3
"""stdlib-only CUBICCOVER75 source-valid three-bridge counterexample."""
from collections import Counter, deque
from functools import lru_cache

edges=[]
for i in range(3):
    a,b,c,d,s=(1+5*i+j for j in range(5))
    for u,v in [(a,c),(a,d),(b,c),(b,d),(c,d),(a,s),(b,s),(0,s)]:
        edges.append(tuple(sorted((u,v))))
assert len(edges)==24 and len(set(edges))==24
adj=[set() for _ in range(16)]
for u,v in edges:
    adj[u].add(v); adj[v].add(u)
assert all(len(neigh)==3 for neigh in adj)

@lru_cache(None)
def matching(mask):
    if not mask: return 0
    b=mask&-mask; u=b.bit_length()-1
    rem=mask^b
    return max([matching(rem)]+
      [1+matching(rem^(1<<v)) for v in adj[u] if rem&(1<<v)])
assert matching((1<<16)-1)==7

clauses=[]
for v in range(16):
    clauses.append(tuple((e+1 if v==u else -(e+1))
          for e,(u,z) in enumerate(edges) if v in (u,z)))
for e in range(24):
    y=25+e; ynext=25+(e+1)%24; x=e+1
    clauses += [(y,-ynext,x),(y,-ynext,-x)]
assert len(clauses)==64 and len({frozenset(c) for c in clauses})==64
assert all(len(c)==3 and len(set(map(abs,c)))==3 for c in clauses)
counts=Counter(lit for c in clauses for lit in c)
assert all(counts[i]==counts[-i]==2 for i in range(1,49))

# Cyclic orientation of a triangle, followed by a directed spanning forest.
orient={(1,3):(1,3),(3,4):(3,4),(1,4):(4,1)}
visited={1,3,4}; todo=deque(sorted(visited))
while todo:
    v=todo.popleft()
    for u in sorted(adj[v]):
        if u not in visited:
            visited.add(u);todo.append(u)
            orient[tuple(sorted((v,u)))]=(v,u)
assert len(visited)==16
for u,v in edges:
    orient.setdefault((u,v),(u,v))
values={25+i:0 for i in range(24)}
for e,(u,v) in enumerate(edges):
    head=orient[(u,v)][1]
    values[e+1]=int(head==u)
def truth(c):
    return any((values[abs(l)]==1)==(l>0) for l in c)
assert all(truth(c) for c in clauses)
print({'n':48,'m':64,'p':24,'delta':16,'max_matching':7,
       'min_ternary_cover':9,'SAT_witness_replayed':True,
       'each_signed_occurrence':2})