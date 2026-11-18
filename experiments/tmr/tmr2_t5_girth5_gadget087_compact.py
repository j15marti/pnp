#!/usr/bin/env python3
"""TMR-2/087 compact reproducible audit. Python 3, no dependencies.
Fixed T5: R(a,b) iff (b-a)%5 in {1,3}. Finite tests are COMPUTATIONAL.
"""
from itertools import product, combinations_with_replacement
from collections import deque
from math import prod
import json

def R(a,b): return (b-a)%5 in (1,3)
A = [[int(R(a,b)) for b in range(5)] for a in range(5)]
AT = [[A[b][a] for b in range(5)] for a in range(5)]
I = [[int(a==b) for b in range(5)] for a in range(5)]
def mm(X,Y):
    return [[sum(X[i][h]*Y[h][j] for h in range(5))
             for j in range(5)] for i in range(5)]
def path(k,q):
    M=I
    for s in '-'*q+'+'*(k-q): M=mm(M,AT if s=='-' else A)
    return M[0]
def bundle(ps):
    return [prod(path(k,q)[d] for k,q in ps) for d in range(5)]
def gadget(n,edges):
    new=[]; n2=n
    for u,v in sorted(edges):
        for word in ('--','---','---+'):
            internal=list(range(n2,n2+len(word)-1));n2+=len(internal)
            w=[u]+internal+[v]
            for i,s in enumerate(word):
                a,b=w[i:i+2]
                new.append((a,b) if s=='+' else (b,a))
    return n2,sorted(new)
def count(n,arcs):
    return sum(all(R(x[a],x[b]) for a,b in arcs)
               for x in product(range(5),repeat=n))
def girth(n,arcs):
    adj=[set() for _ in range(n)]
    for a,b in arcs: adj[a].add(b);adj[b].add(a)
    best=n+1
    for root in range(n):
        dist=[-1]*n;par=[-1]*n;dist[root]=0;Q=deque([root])
        while Q:
            u=Q.popleft()
            for v in adj[u]:
                if dist[v]<0: dist[v]=dist[u]+1;par[v]=u;Q.append(v)
                elif par[u]!=v: best=min(best,dist[u]+dist[v]+1)
    return best if best<=n else None

assert path(2,2)==[0,2,0,1,1]
assert path(3,3)==[3,1,1,3,0]
assert path(4,3)==[1,6,1,4,4]
assert bundle(((2,2),(3,3)))==[0,2,0,3,0]
balanced=((2,2),(3,3),(4,3))
assert bundle(balanced)==[0,12,0,12,0]
n,e=gadget(2,[(0,1)])
assert (n,len(e),girth(n,e))==(8,9,5)
assert len({tuple(sorted(z)) for z in e})==9
assert count(n,e)==120
for a,b in product(range(5),repeat=2):
    c=sum(all(R(x[u],x[v]) for u,v in e)
          for z in product(range(5),repeat=6)
          for x in [(a,b)+z])
    assert c==12*int(R(a,b)),(a,b,c)
# Finite search of all path-multisets with total arc budget <=9.
for budget in range(4,10):
    opts=[(k,q) for k in range(2,budget+1) for q in range(k+1)]
    matches=[]
    for countpaths in range(2,budget//2+1):
        for ps in combinations_with_replacement(opts,countpaths):
            if sum(k for k,q in ps)!=budget:continue
            z=bundle(ps)
            if z[0]==z[2]==z[4]==0 and z[1]==z[3]>0:
                matches.append(ps)
    assert matches==([balanced] if budget==9 else []),(budget,matches)
no=((0,1),(1,2),(0,3),(1,3),(2,3))
yes=((1,0),(1,2),(0,3),(1,3),(2,3))
assert count(4,no)==0
assert count(4,yes)==5
n0,e0=gadget(4,no);n1,e1=gadget(4,yes)
assert (n0,len(e0),girth(n0,e0))==(34,45,5)
assert (n1,len(e1),girth(n1,e1))==(34,45,5)
print(json.dumps({'revision':'tmr2-t5-girth5-gadget087.compact',
 'gadget_K':[0,12,0,12,0], 'gadget_girth':5, 'gadget_Z':120,
 'minimum_gadget_arcs':9,'NO':{'n':n0,'m':len(e0),'Z':0},
 'YES':{'n':n1,'m':len(e1),'Z':5*12**5},
 'scope':'Computational checks. Exact transfer identity gives proof.'},indent=2))
