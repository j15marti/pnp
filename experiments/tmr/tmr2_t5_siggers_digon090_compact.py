#!/usr/bin/env python3
"""Exact T5 no-Siggers certificate: 3 tuples, 2 real power arcs, 1 identity."""
from itertools import product
from collections import Counter

R = lambda a,b: (b-a)%5 in (1,3)
arc = lambda u,v: all(R(a,b) for a,b in zip(u,v))
s,p,t = (0,1,0,2),(3,2,1,0),(1,0,2,1)
assert (s,t)==((0,1,0,2),(1,0,2,1))
assert arc(s,p) and arc(p,t)
assert tuple((b-a)%5 for a,b in zip(s,p))==(3,1,1,3)
assert tuple((b-a)%5 for a,b in zip(p,t))==(3,3,1,1)
assert not any(R(a,b) and R(b,a) for a,b in product(range(5),repeat=2))
# The Siggers identity f(x,y,x,z)=f(y,x,z,y) forces f(s)=f(t).
# A polymorphism would map s->p->t to a target directed 2-cycle. Impossible.

P = list(product(range(5),repeat=4))
hist = Counter()
direct = 0
backwards = 0
for x,y,z in product(range(5),repeat=3):
    a,b=(x,y,x,z),(y,x,z,y)
    direct += arc(a,b)
    backwards += arc(b,a)
    hist[sum(arc(a,v) and arc(v,b) for v in P)] += 1
assert direct==backwards==0
assert hist==Counter({0:110,2:5,4:10})
assert sum(c*n for n,c in hist.items()) == 50
assert len(P)==625 and len(P)*16==10000
print('PASS: no 4-ary Siggers polymorphism; two-arc proof; 125 triples; 50 length-two walks.')
