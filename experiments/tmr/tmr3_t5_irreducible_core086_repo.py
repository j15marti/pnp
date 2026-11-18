#!/usr/bin/env python3
"""Compact, independently runnable TMR-3/086 T5 private-chain/affine-closure checker.
Run: python3 tmr3_t5_irreducible_core086_repo.py
"""
from itertools import product
import random
import json

def w(length):
    a=[1,0,0,0,0]
    for _ in range(length):
        b=[0]*5
        for j,v in enumerate(a):
            b[(j+1)%5]+=v
            b[(j+3)%5]+=v
        a=b
    return a

def original_count(n,edges):
    return sum(all((x[v]-x[u])%5 in (1,3) for u,v in edges)
               for x in product(range(5),repeat=n))

def exact_count(n,edges):
    edges=sorted(set(edges))
    out=[[] for _ in range(n)];ind=[0]*n
    for u,v in edges:
        assert 0<=u<n and 0<=v<n
        out[u].append(v);ind[v]+=1
    branch=[i for i in range(n) if len(out[i])!=1 or ind[i]!=1]
    bset=set(branch); chains=[];seen=set();cycles=[]
    for u in branch:
        for v in out[u]:
            seen.add((u,v)); length=1;cur=v
            while cur not in bset:
                nxt=out[cur][0]
                assert (cur,nxt) not in seen
                seen.add((cur,nxt));length+=1;cur=nxt
            chains.append((u,cur,length))
    for u,v in edges:
        if (u,v) in seen:continue
        cur=u;length=0
        while True:
            nxt=out[cur][0]
            assert (cur,nxt) not in seen
            seen.add((cur,nxt));length+=1;cur=nxt
            if cur==u:break
        cycles.append(length)
    assert len(seen)==len(edges)
    if any(z<3 for z in cycles):return 0,0,len(branch)
    roots={v:i for i,v in enumerate(branch)}
    p=list(range(len(branch)));pot=[0]*len(p)
    def find(i):
        if p[i]==i:return i,0
        j,delta=find(p[i]);pot[i]=(pot[i]+delta)%5;p[i]=j
        return j,pot[i]
    for _ in range(len(branch)+1):
        pairs={};merged=False
        for u,v,L in chains:
            if L>3:continue
            a,da=find(roots[u]);b,db=find(roots[v])
            vals={(k+da-db)%5 for k,m in enumerate(w(L)) if m}
            if a==b:
                if 0 not in vals:return 0,0,len(branch)
                continue
            if a>b:
                a,b=b,a;vals={(-x)%5 for x in vals}
            key=a,b
            pairs[key]=vals if key not in pairs else pairs[key]&vals
            if not pairs[key]:return 0,0,len(branch)
        for (a,b),vals in sorted(pairs.items()):
            if len(vals)==1:
                delta=next(iter(vals))
                ra,da=find(a);rb,db=find(b)
                if ra==rb:
                    if (db-da)%5!=delta:return 0,0,len(branch)
                else:
                    p[rb]=ra;pot[rb]=(delta+da-db)%5;merged=True
        if not merged:break
    allroots=sorted({find(i)[0] for i in range(len(branch))})
    ix={rt:j for j,rt in enumerate(allroots)}
    terms=[]
    for u,v,L in chains:
        a,da=find(roots[u]);b,db=find(roots[v])
        terms.append((ix[a],ix[b],da,db,w(L)))
    multiplier=1
    for L in cycles:multiplier*=5*w(L)[0]
    if all(a==b for a,b,da,db,ww in terms):
        for a,b,da,db,ww in terms:
            multiplier*=ww[(db-da)%5]
        return 5**len(allroots)*multiplier,len(allroots),len(branch)
    count=0
    for x in product(range(5),repeat=len(allroots)):
        v=1
        for a,b,da,db,ww in terms:
            v*=ww[(x[b]+db-x[a]-da)%5]
            if not v:break
        count+=v
    return multiplier*count,len(allroots),len(branch)

def make_k(k):
    n=2*k;ee=[]
    for i in range(k):
        for j in range(k):
            v=k+j
            ee.extend(((i,v),(i,n),(n,v)))
            n+=1
    return n,ee

def self_test():
    checks=0
    for n in range(1,4):
        if n!=3:continue
        for mask in range(1<<(n*n)):
            ee=[(j//n,j%n) for j in range(n*n) if mask>>j&1]
            assert exact_count(n,ee)[0]==original_count(n,ee)
            checks+=1
    rng=random.Random(86086)
    for n in range(1,7):
        for z in range(31):
            ee=[(u,v) for u in range(n) for v in range(n) if rng.random()<0.18]
            assert exact_count(n,ee)[0]==original_count(n,ee)
            checks+=1
    for k in [1,2,3,10,100]:
        n,ee=make_k(k)
        actual,r,b=exact_count(n,ee)
        assert actual==5 and r==1 and b==2*k
        checks+=1
    n=6;ee=[(0,1),(0,2),(2,1),(1,3),(1,4),(4,3),(3,0),(3,5),(5,0)]
    assert exact_count(n,ee)[0]==0
    checks+=1
    return {'experiment':'TMR3_086_COMPACT','checks':checks,'failures':0,
            'k100_n':10200,'k100_m':30000,'k100_exact_count':5,
            'status':'COMPUTATIONAL, no P vs NP separation'}

if __name__=='__main__':
    print(json.dumps(self_test(),sort_keys=True,indent=2))
