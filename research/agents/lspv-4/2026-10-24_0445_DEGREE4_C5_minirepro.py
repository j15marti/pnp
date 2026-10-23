#!/usr/bin/env python3
"""Self-contained exact C5 obstruction and paired-graph degree-four audit.
Standard library only. The larger downloadable package additionally replays
an explicit 1,776-square rational SOS certificate coefficient by coefficient.
"""
from fractions import Fraction as F
from itertools import combinations, permutations, product
from collections import defaultdict
import json

checks=0

def ck(ok):
    global checks
    checks+=1
    if not ok:raise AssertionError(checks)

E5={tuple(sorted((v,(v+1)%5))) for v in range(5)}
VP=[tuple((a+e*v)%5 for v in range(5)) for a in range(5) for e in [-1,1]]
CP=list(permutations(range(3)))

def add(*ps):
    d=defaultdict(F)
    for p in ps:
        for m,a in p.items():d[m]+=a
    return {m:a for m,a in d.items() if a}
def scale(p,a):return {m:a*b for m,b in p.items() if a*b}
def mon(ids):return sum(1<<i for i in ids)
def reduce(m):
    ids=[i for i in range(15) if m>>i&1]
    for i,j in combinations(ids,2):
        u,c=divmod(i,3);v,d=divmod(j,3)
        if u==v or (c==d and tuple(sorted((u,v))) in E5):return None
    return m
def mul(p,q):
    out=defaultdict(F)
    for m,a in p.items():
        for n,b in q.items():
            ck(m.bit_count()+n.bit_count()<=4)
            z=reduce(m|n)
            if z is not None:out[z]+=a*b
    return {m:a for m,a in out.items() if a}
def avg(p):
    out=defaultdict(F)
    for vp in VP:
        for cp in CP:
            for m,a in p.items():
                z=mon([3*vp[i//3]+cp[i%3] for i in range(15) if m>>i&1])
                out[z]+=a/60
    return {m:a for m,a in out.items() if a}
def cs(v):return {0:F(-1),**{1<<(3*v+c):F(1) for c in range(3)}}

q={mon(ids):F(a) for a,ids in [(-2,[0]),(1,[0,4]),(1,[0,7]),(-1,[1,6]),
 (1,[0,10]),(-1,[1,9]),(1,[0,13]),(1,[5,6]),(1,[9,14])]}
Y={mon([3*u+c,3*v+c]):F(1) for u,v in combinations(range(5),2) if (u,v) not in E5 for c in range(3)}
Q=add(Y,{0:F(-2)})
LO=[('-10/3',[],0),('-10',[0],1),('-20',[0,4],2),('20',[0,6],1),
 ('10',[0,6],3),('20',[0,4,6],3),('-20',[0,4,8],3),('20',[0,4,9],2)]
HI=[('2',[],0),('-6',[0],2),('12',[0,4],2),('-15',[0,6],1),
 ('-6',[0,6],3),('24',[0,4,8],3),('-24',[0,4,9],2)]
for lhs,terms in [(add(scale(mul(Q,Q),F(1,3)),scale(Q,-1)),LO),
                  (add(scale(avg(mul(q,q)),3),Q),HI)]:
    rhs={}
    for a,ids,v in terms:rhs=add(rhs,scale(avg(mul({mon(ids):F(1)},cs(v))),F(a)))
    ck(lhs==rhs)
    ck(add(rhs,{0:F(1)})!=lhs)

NO=[(0,1),(0,4),(0,6),(0,9),(1,2),(1,5),(1,7),(2,3),(2,6),(2,8),
 (3,4),(3,7),(3,9),(4,5),(4,8),(5,10),(5,11),(6,10),(6,11),(7,8),
 (7,11),(8,10),(9,10),(9,11)]
YES=sorted((set(NO)-{(0,1),(2,6)})|{(0,2),(1,6)})
AUT=[list(range(12)),[0,4,3,2,1,5,9,8,7,6,11,10],
 [1,0,6,11,5,4,2,9,10,7,8,3],[4,0,9,10,5,1,3,6,11,8,7,2],
 [1,5,11,6,0,4,7,10,9,2,3,8],[4,5,10,9,0,1,8,11,6,3,2,7],
 [5,1,7,8,4,0,11,2,3,10,9,6],[5,4,8,7,1,0,10,3,2,11,6,9]]

def classify(es):
    es=set(es);adj=[set() for _ in range(12)]
    for u,v in es:adj[u].add(v);adj[v].add(u)
    ck(all(len(z)==4 for z in adj));ck(all(not(adj[u]&adj[v]) for u,v in es))
    colors=[-1]*12;count=0
    def visit():
        nonlocal count
        todo=[v for v in range(12) if colors[v]<0]
        if not todo:count+=1;return
        v=max(todo,key=lambda u:(len({colors[w] for w in adj[u] if colors[w]>=0}),-u))
        used={colors[w] for w in adj[v] if colors[w]>=0}
        for c in range(3):
            if c not in used:colors[v]=c;visit()
        colors[v]=-1
    visit()
    cycles=[]
    for vs in combinations(range(12),5):
        induced=[uv for uv in combinations(vs,2) if uv in es]
        if len(induced)==5 and all(sum(v in uv for uv in induced)==2 for v in vs):
            cycles.append(vs)
            j=sum(len(adj[u]&adj[v]) for u,v in combinations(vs,2) if (u,v) not in es)
            ck(F(5,3)+F(j,12)>2)
    return count,cycles

nc,ncycles=classify(NO);yc,ycycles=classify(YES)
ck((nc,yc)==(0,108));ck((len(ncycles),len(ycycles))==(44,28))
for a in AUT:
    ck(sorted(a)==list(range(12)))
    ck({tuple(sorted((a[u],a[v]))) for u,v in NO}==set(NO))
ne=[uv for uv in combinations(range(12),2) if uv not in NO]
reps={uv:min(tuple(sorted((a[uv[0]],a[uv[1]]))) for a in AUT) for uv in ne}
keys=sorted(set(reps.values()))
ck(keys==[(0,2),(0,5),(0,7),(0,10),(2,7),(2,9),(2,10)])
chosen=[(0,1,2,3,4),(0,1,2,3,9),(0,1,2,4,8),(0,1,3,7,9),(0,2,3,6,9),(2,3,6,7,11)]
rows=[[sum(u in vs and v in vs for u,v in ne if reps[u,v]==r) for r in keys] for vs in chosen]
for vs in chosen:ck(vs in ncycles)
a=[[F(x) for x in row] for row in rows];rank=0
for col in range(7):
    pivot=next((i for i in range(rank,6) if a[i][col]),None)
    if pivot is None:continue
    a[rank],a[pivot]=a[pivot],a[rank];z=a[rank][col];a[rank]=[x/z for x in a[rank]]
    for i in range(6):
        if i!=rank and a[i][col]:
            z=a[i][col];a[i]=[x-z*y for x,y in zip(a[i],a[rank])]
    rank+=1
ck(rank==6)
sol=[(0,1),(-2,6),(0,1),(2,-4),(2,-4),(0,1),(0,1)]
for row in rows:
    ck(sum(x*b for x,(b,s) in zip(row,sol))==2)
    ck(sum(x*s for x,(b,s) in zip(row,sol))==0)
def quadratic(w):
    b=F(sum(x*x for x in w));s=F(0)
    for u,v in combinations(range(12),2):
        b-=w[u]*w[v]
        if (u,v) in reps:
            bb,ss=sol[keys.index(reps[u,v])]
            b+=3*w[u]*w[v]*bb;s+=3*w[u]*w[v]*ss
    return b,s
ck(quadratic([int(v in {0,1,4,5}) for v in range(12)])==(F(-14),F(36)))
ck(quadratic([1]*12)==(F(6),F(-24)))
ck(F(7,18)>F(1,4))
print(json.dumps({'checks':checks,'unexpected_failures':0,
 'SAT_colorings':yc,'UNSAT_colorings':nc,'five_cycles':[len(ycycles),len(ncycles)],
 'local_degree_four_identities':'both exactly verified',
 'canonical_extension':'impossible whenever a 5-cycle is present',
 'UNSAT_unrestricted_degree_four':'infeasible: t >= 7/18 and t <= 1/4',
 'scope':'fixed equality-SOS encoding; P versus NP OPEN'},indent=2))
