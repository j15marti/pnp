#!/usr/bin/env python3
"""CLOCKQ48 independent scalar reproduction, standard library only."""
from itertools import product
beat=lambda a,b:(b-a)%5 in (1,3)
Q=lambda x,y,z:beat(x,y)!=beat(x,z)
P=lambda x,y,z:beat(x,y) and beat(x,z)
C=[(0,1,2),(0,1,3),(1,0,2),(1,2,3),(2,0,3)]
assert sum(Q(*a) for a in product(range(5),repeat=3))==60
assert sum(P(*a) for a in product(range(5),repeat=3))==20
assert all(not (Q(*a) and P(*a)) for a in product(range(5),repeat=3))
count=lambda cs:sum(all(Q(*(a[j] for j in t)) for t in cs) for a in product(range(5),repeat=4))
assert count(C)==0
assert [count(C[:i]+C[i+1:]) for i in range(5)]==[10,40,10,30,25]
for a,b in product(range(5),repeat=2):
    ways=sum(Q(h,a,b) for h in range(5))
    assert ways==(0 if a==b else (4 if (b-a)%5 in (1,4) else 2))
def myc(n,e):
    d=set(e)
    for a,b in e:
        d.add((a,b+n))
        d.add((b,a+n))
    for i in range(n):
        d.add((n+i,2*n))
    return 2*n+1,sorted(d)
n,e=2,[(0,1)]
levels=[]
for lev in range(2,7):
    levels.append((lev,n,len(e)))
    assert all(a<b for a,b in e)
    assert len(e)==len(set(e))
    assert all(not ((min(a,c),max(a,c)) in e and (min(b,c),max(b,c)) in e)
               for a,b in e for c in range(n) if c!=a and c!=b)
    n,e=myc(n,e)
assert levels==[(2,2,1),(3,5,5),(4,11,20),(5,23,71),(6,47,236)]
for a,b in product(range(5),repeat=2):
    assert any(Q(h,a,b) for h in range(5))==(a!=b)
print({'status':'PASS','Q_triples':60,'P_triples':20,
       'critical_deletions':[10,40,10,30,25],
       'Mycielski':levels,'head_pair_checks':25})
