#!/usr/bin/env python3
"""TMR-5/096: exact C10 double-cover audit for all-left-to-right T5 DAGs."""
from itertools import product

def R(a,b):return (b-a)%5 in (1,3)
def cycle(i,j):return (j-i)%10 in (1,9)
def phi(side,k):return (4*k+(7 if side else 0))%10
for x,y in product(range(5),repeat=2):
    assert R(x,y)==cycle(phi(0,x),phi(1,y))
assert len({phi(s,k) for s in range(2) for k in range(5)})==10

def count(l,r,edges,N):
    adj=R if N==5 else cycle
    groups=[[i for i,j in edges if j==v] for v in range(r)]
    return sum(__import__('math').prod(sum(all(adj(x[i],y) for i in group)
                      for y in range(N)) for group in groups)
               for x in product(range(N),repeat=l))

def components(l,r,edges):
    g=[set() for _ in range(l+r)]
    for i,j in edges:g[i].add(l+j);g[l+j].add(i)
    seen=set();c=0
    for v in range(l+r):
        if v in seen:continue
        c+=1;stack=[v];seen.add(v)
        while stack:
            for w in g[stack.pop()]:
                if w not in seen:seen.add(w);stack.append(w)
    return c

checked=0
for l,r in ((2,2),(3,3)):
    for mask in range(1<<(l*r)):
        edges=[(i,j) for i in range(l) for j in range(r) if mask>>(i*r+j)&1]
        c=components(l,r,edges)
        a=count(l,r,edges,5);b=count(l,r,edges,10)
        assert b==(1<<c)*a,(l,r,mask,a,b,c)
        checked+=1
assert count(3,3,list(product(range(3),repeat=2)),5)==70
print({'graphs_checked':checked,'target_C10':True,'K33_T5_count':70,'failures':0})
