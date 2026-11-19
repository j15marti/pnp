#!/usr/bin/env python3
"""Compact, standard-library audit for TMR-5/095. Full verifier in evidence ZIP."""
from itertools import product, permutations
from collections import deque

def R(a,b): return (b-a)%5 in (1,3)
def step(L):
    z=[0]*5
    for inc in product((1,3),repeat=L): z[sum(inc)%5]+=1
    return z
def det(M):
    out=0
    for p in permutations(range(5)):
        sign=(-1)**sum(p[i]>p[j] for i in range(5) for j in range(i+1,5))
        term=sign
        for i,j in enumerate(p): term*=M[i][j]
        out+=term
    return out

a,b=step(4),step(8)
assert a==[4,4,1,6,1] and b==[36,70,36,57,57]
w=[x*y for x,y in zip(a,b)]
assert w==[144,280,36,342,57]

def val(n,p):
    t=0
    while n%p==0: t+=1;n//=p
    return t
M=[[val(v,p) for v in w] for p in (2,3,5,19)]+[[1]*5]
assert det(M)==-2

checks=0
for u,v in product(range(5),repeat=2):
    n=0
    for a,b,c in product(range(5),repeat=3):
        n+=int(R(u,a) and R(a,b) and R(b,c) and R(u,c) and R(c,v))
        checks+=1
    assert n==int((v-u)%5 in (1,4))

# A 12-vertex, 15-arc acyclic C5 triangle lift.
src=[];pos=3
for u,v in ((0,1),(0,2),(1,2)):
    a,b,c=range(pos,pos+3);pos+=3
    src.extend(((u,a),(a,b),(b,c),(u,c),(c,v)))
assert pos==12 and len(src)==15

out=[];labels=[0]*pos;partition=[0]*pos
for u,v in src:
    for increments in ((3,3,3,1),(3,1,1,1,1,1,1,1)):
        p=u
        color=0
        for d in increments[:-1]:
            labels.append((labels[p]+d)%5)
            color=1-color
            partition.append(color)
            q=len(labels)-1
            out.append((p,q));p=q
        out.append((p,v))
assert len(labels)==162 and len(out)==180
assert all(R(labels[u],labels[v]) for u,v in out)
assert all(partition[u]!=partition[v] for u,v in out)

indeg=[0]*len(labels); successors=[[] for _ in labels]
for u,v in out: indeg[v]+=1; successors[u].append(v)
queue=deque(i for i,d in enumerate(indeg) if d==0)
visited=0
while queue:
    u=queue.popleft(); visited+=1
    for v in successors[u]:
        indeg[v]-=1
        if indeg[v]==0:queue.append(v)
assert visited==len(labels)

print({"A4":step(4),"A8":step(8),"w":w,"det":det(M),
       "private_assignments":checks,"lift_vertices":len(labels),
       "lift_arcs":len(out),"lift_satisfiable":True})
