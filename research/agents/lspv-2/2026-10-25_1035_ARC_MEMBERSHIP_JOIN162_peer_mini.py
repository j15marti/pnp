#!/usr/bin/env python3
"""ARC-MEMBERSHIP-JOIN162 independently runnable exact finite peer control.
No SAT oracle: support-set checks use explicit Boolean enumeration.
"""
from itertools import product
def sig(P,u): return tuple(int(u in Q) for Q in P)
def hset(h,Q): return {h[u] for u in Q}
def common(P,S): return bool(set.intersection(*P,S))
checks=0
U=set(range(4))
for A in range(16):
 for B in range(16):
  P=[{u for u in U if A>>u&1},{u for u in U if B>>u&1}]
  h={u:sig(P,u) for u in U}
  for Z in range(16):
   S={u for u in U if Z>>u&1}
   left=common(P,S)
   right=bool(set.intersection(*(hset(h,Q) for Q in P),hset(h,S)))
   assert left==right
   for Q in P: assert hset(h,Q&S)==hset(h,Q)&hset(h,S)
   checks+=3
for A in range(16):
 for B in range(16):
  for C in range(16):
   P=[{u for u in U if z>>u&1} for z in (A,B,C)]
   h={u:sig(P,u) for u in U}
   for Z in range(16):
    S={u for u in U if Z>>u&1}
    assert common(P,S)==bool(set.intersection(*(hset(h,Q&S) for Q in P)))
    checks+=1
P0=[{0,1},{0,1}];P1=[{0},{0,1}];P2=[{0},{1}]
h0={u:sig(P0,u) for u in {0,1}}
assert common(P0,{0,1}) and common(P1,{0,1}) and not common(P2,{0,1})
assert bool(set.intersection(*(hset(h0,Q) for Q in P2)))
h2={u:sig(P2,u) for u in {0,1}}
assert not bool(set.intersection(*(hset(h2,Q) for Q in P2)))
print({'status':'PASS','checks':checks,'stale_false_sat':True,
       'signature_labels_at_most':4,'ARC_EDGE_90':'OPEN'})
