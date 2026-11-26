#!/usr/bin/env python3
"""FP12 independent raw-mask certificate. Python standard library only."""
from collections import deque
E=[(0,2),(0,6),(0,9),(2,10),(2,11),(6,5),(6,7),(9,4),(9,8),(1,3),(1,7),(1,10),(3,8),(3,11),(7,8),(10,5),(11,4),(4,5)]
D=[sum(1<<i for i,e in enumerate(E) if u in e) for u in range(12)]
F=[x for x in range(1<<18) if all((x&d).bit_count()%2==0 for d in D)]
full=(1<<18)-1
best={a:min((full^(a|b)).bit_count() for b in F) for a in F}
a,b,c,d=48501,93131,88798,124843
assert len(F)==128 and all(x in F for x in (a,b,c,d,179667))
assert all(full^(a|v)==131072 for v in (b,c,d))
assert [best[x] for x in (a,b,a^b)]==[1,1,0]
assert [best[x] for x in (a,c,a^c)]==[1,1,1]
assert [best[x] for x in (a,d,a^d)]==[1,1,1]
assert (a^b)|179667==full
print("alias: same a and zero, strict escape versus two stalls")
E0=[(0,2),(0,6),(0,9),(1,3),(1,7),(1,10),(2,10),(2,11),(3,8),(3,11),(4,5),(4,9),(4,11),(5,6),(5,10),(6,7),(7,8),(8,9)]
D=[sum(1<<i for i,e in enumerate(E0) if u in e) for u in range(12)]
F=[x for x in range(1<<18) if all((x&d).bit_count()%2==0 for d in D)]
P={(a,b) for a in F for b in F if not (full^(a|b))&~(1<<5)}
start=(110469,185822);sol=(96734,178037)
assert start in P and sol in P and sol[0]|sol[1]==full
seen={start};q=deque([start])
while q:
 a,b=q.popleft()
 for c,d in P:
  if {a,b,a^b}&{c,d,c^d} and (c,d) not in seen:
   seen.add((c,d));q.append((c,d))
assert len(P)==30 and len(seen)==18 and all(a|b!=full for a,b in seen)
print("protected FP04: 30 states, 18 reachable, no proper state")
K=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
D=[sum(1<<i for i,e in enumerate(K) if u in e) for u in range(4)]
F=[x for x in range(64) if all((x&d).bit_count()%2==0 for d in D)]
a,b,c,d=11,51,38,21
assert min((63^(a|v)).bit_count() for v in F)==1
assert all(v in F and (63^(a|v)).bit_count()==1 for v in (b,c,d))
assert b^c^d in F and (63^(a|(b^c^d))).bit_count()==3
print("K4: optimum affine hull includes a three-defect word")
