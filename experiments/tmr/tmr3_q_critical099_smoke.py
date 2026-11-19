#!/usr/bin/env python3
"""TMR-3/099 independent, deterministic, standard-library smoke test.
Tests new physically critical K3 join odd-cycle Q instances with matched P.
No external SAT/UNSAT oracle, no fixed-input trace used as a lower bound.
"""
from itertools import product
from collections import Counter

W=({1,3},{2,4},{0,3},{1,4},{0,2})
def beat(a,b): return b in W[a]
def Q(h,u,v): return beat(h,u)!=beat(h,v)
def P(h,u,v): return beat(h,u) and beat(h,v)

def join(r):
    L=2*r+1
    e=[(a,b) for a in range(3) for b in range(a+1,3)]
    e += [(3+j,3+(j+1)%L) for j in range(L)]
    e += [(a,3+j) for a in range(3) for j in range(L)]
    return 3+L,e

def deletion_coloring(r,e,i):
    L=2*r+1;a,b=e[i];x=[-1]*(L+3)
    if a<3 and b<3:
        x[a]=x[b]=0;x[3-a-b]=1;x[3]=4
        for j in range(1,L): x[3+j]=2 if j&1 else 3
    elif a>=3 and b>=3:
        x[:3]=[2,3,4]
        start=(a-3+1)%L
        for j in range(L):x[3+(start+j)%L]=j%2
    else:
        k=a if a<3 else b
        v=b if a<3 else a
        other=[u for u in range(3) if u!=k]
        x[k]=0;x[other[0]]=3;x[other[1]]=4
        start=v-3
        x[3+start]=0
        for j in range(1,L):x[3+(start+j)%L]=1 if j&1 else 2
    return x

def extend(n,edges,colors,mode,omit=None):
    f=Q if mode=='Q' else P
    head=[]
    for i,(u,v) in enumerate(edges):
        if i==omit:head.append(0);continue
        value=next((h for h in range(5) if f(h,colors[u],colors[v])),None)
        if value is None:return None
        head.append(value)
    a=colors+head
    assert all(f(a[n+i],a[u],a[v]) for i,(u,v) in enumerate(edges) if i!=omit)
    return a

def exact_kernel():
    q=[sum(Q(h,0,d) for h in range(5)) for d in range(5)]
    p=[sum(P(h,0,d) for h in range(5)) for d in range(5)]
    assert q==[0,4,2,2,4] and p==[2,0,1,1,0]
    assert all(q[d]+2*p[d]==4 for d in range(5))
    return q,p

def weighted_brute(n,edges,weights,omit=None):
    ans=0
    for a in product(range(5),repeat=n):
        v=1
        for i,(u,w) in enumerate(edges):
            if i!=omit:v*=weights[(a[w]-a[u])%5]
            if not v:break
        ans+=v
    return ans*(5 if omit is not None else 1)

def main():
    q,p=exact_kernel()
    tests=0
    for r in [1,2,3,5,10,20]:
        n,edges=join(r)
        assert n==2*r+4 and len(edges)==8*r+7
        for omit in range(len(edges)):
            color=deletion_coloring(r,edges,omit)
            assert all(color[u]!=color[v] for i,(u,v) in enumerate(edges) if i!=omit)
            assert extend(n,edges,color,'Q',omit) is not None
            tests+=1
        assert extend(n,edges,[0]*n,'P') is not None
        tests+=1
    for r in [1,2]:
        n,e=join(r)
        assert weighted_brute(n,e,q)==0
        assert weighted_brute(n,e,p)>0
        for omit in [0,3,3+(2*r+1)]:
            assert weighted_brute(n,e,q,omit)>0
        tests+=5
    print({'status':'PASS','verified_deletions':tests-6-10,
           'other_checks':16,'P_vs_NP':'OPEN'})
if __name__=='__main__':main()
