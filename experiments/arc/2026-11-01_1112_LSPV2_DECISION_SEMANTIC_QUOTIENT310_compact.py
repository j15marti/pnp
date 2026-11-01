#!/usr/bin/env python3
"""Decision-only G_t semantic quotient, self-contained standard-library compact check."""
from itertools import product, combinations
from collections import Counter, defaultdict
from functools import lru_cache
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
def good(v,b):
    return all(any((b if j==0 and x==5 else v[x-1]) for x in c) for j,c in enumerate(P)) and all(any(not v[x-1] for x in c) for c in N)
@lru_cache(None)
def M(p):
    if 2 in p:
        j=p.index(2); a=M(p[:j]+(0,)+p[j+1:]); b=M(p[:j]+(1,)+p[j+1:])
        return tuple(x+y for x,y in zip(a,b))
    v=p; a=v[4]
    return tuple(int(a==i and good(v,j)) for i in (0,1) for j in (0,1))
def mask(m):return sum((1<<i) for i,x in enumerate(m) if x)
def compose(a,b):
    return sum(1<<(2*i+k) for i in (0,1) for k in (0,1) if any((a>>(2*i+j))&1 and (b>>(2*j+k))&1 for j in (0,1)))
def sat(a):return bool(a&9)
def mul(a,b):return tuple(sum(a[2*i+j]*b[2*j+k] for j in (0,1)) for i in (0,1) for k in (0,1))
def tr(a):return a[0]+a[3]
def pin(**kw):
    p=[2]*9
    for i,x in kw.items():p[int(i)-1]=x
    return tuple(p)
states=list(product((0,1,2),repeat=9))
hist=Counter(mask(M(p)) for p in states)
assert hist=={0:8525,2:650,3:3952,8:855,10:278,11:15,12:3175,15:2233}
R=set(hist)|{9}
while True:
    nextR=R|{compose(a,b) for a in R for b in R}
    if nextR==R:break
    R=nextR
assert R=={0,2,3,8,9,10,11,12,15}
g=defaultdict(list)
for a in sorted(R):g[tuple(sat(compose(a,c)) for c in sorted(R))].append(a)
classes=sorted((sorted(x) for x in g.values()),key=lambda x:x[0])
assert classes==[[0],[2],[3],[8,10],[9,11],[12,15]]
for cls in classes:
    for a,b in product(cls,repeat=2):
        for c in R:
            assert tuple(sat(compose(compose(a,c),d)) for d in sorted(R))==tuple(sat(compose(compose(b,c),d)) for d in sorted(R))
A=pin(**{'1':1,'2':0,'3':1,'4':0,'8':0})
B=pin(**{'1':1,'2':1,'3':0,'4':0,'8':0})
p8=pin(**{'1':0,'3':0,'6':0});p12=pin(**{'5':1});k2=pin(**{'1':0,'5':0,'6':0})
assert M(pin())==(34,47,23,36)
assert M(A)==(1,1,0,0) and M(B)==(0,0,0,0)
assert [mask(M(x)) for x in (p8,p12,k2)]==[8,12,2]
assert tr(mul(M(p8),M(k2)))==0 and tr(mul(M(p12),M(k2)))==299
assert tr(mul(M(A),M(A)))==1 and tr(mul(M(B),M(A)))==0
assert sat(12) and sat(15) and not sat(compose(12,1)) and sat(compose(15,1))
E=(2,3,4,6,7,8,9)
short=Counter()
for names in combinations(E,2):
    for bits in product((0,1),repeat=2):
        p=pin(**{str(i):v for i,v in zip(names,bits)})
        short[mask(M(p))]+=1
assert short=={15:81,3:2,11:1}
print('PASS: 19683 pins, 8 supports, 9 monoid states, 6 continuation classes; G2 SAT299/UNSAT0')
