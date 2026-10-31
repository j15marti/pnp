#!/usr/bin/env python3
"""Compact independent exact smoke checks for SOURCE-LATTICE-ADMISSION269.
Full 17-source experiment is archived separately; no FLMV benchmark implied.
"""
from itertools import product
def sat(F,rho=()):
    n=max((abs(x) for C in F for x in C), default=3)
    for bits in product((False,True), repeat=n):
        if any(bits[abs(l)-1] != (l>0) for l in rho): continue
        if all(any(bits[abs(l)-1]==(l>0) for l in C) for C in F):
            return tuple(int(v) for v in bits)
    return None
clauses=[tuple(j+1 if (p>>j)&1 else -(j+1) for j in range(3)) for p in range(8)]
for mask in range(256):
    F=[C for i,C in enumerate(clauses) if (mask>>i)&1]
    assert (sat(F) is None) == (mask==255)
H7=clauses[:-1]; H8=clauses
assert sat(H7) is not None and sat(H8) is None
assert sat([(1,)])==(1,)
assert sat([(1,),(-1,)]) is None
assert sat([(1,)],(-1,)) is None
for r in range(1,15):
 for h in range(r):
  for A in range(0,30):
   d=r-h; q=A//d+1
   for u in range(1,40):
    online=u*r if u<q else q*r+A+(u-q)*h
    offline=min(u*r,r+A+(u-1)*h)
    assert online<=2*offline,(r,h,A,u,online,offline)
print('PASS: 256 original 3CNF truth-table cases, witness/cube monotonicity, 122,850 tariff conditions')
