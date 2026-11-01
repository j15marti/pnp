#!/usr/bin/env python3
"""LSPV-2 314 source-authenticated compact reproduction. Standard library only.
This is a restricted original G_(2t) promise; not an all-input SAT solver.
"""
from itertools import product
from collections import Counter
from math import prod, log2
P=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
N=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
A={5:1};B={5:1,4:0,6:0};Z={};Q={1:0,5:0,6:0}
def original(k):
    out=[]
    for i in range(k):
        for j,c in enumerate(P):
            out.append(tuple((i*9+x) if (j,x)!=(0,5) else ((i+1)%k)*9+5 for x in c))
        out.extend(tuple(-(i*9+x) for x in c) for c in N)
    return out
def valid(F,n):
    cnt=Counter();seen=set()
    if n<3 or n%3 or len(F)*3!=4*n:return False
    for c in F:
        if len(c)!=3 or len(set(map(abs,c)))!=3 or not (all(x>0 for x in c) or all(x<0 for x in c)):return False
        if any(abs(x)>n or x==0 for x in c):return False
        key=tuple(sorted(c))
        if key in seen:return False
        seen.add(key);cnt.update(c)
    return all(cnt[v]==cnt[-v]==2 for v in range(1,n+1))
def mat(pins):
    M=[[0,0],[0,0]];trials=0
    for bits in product((0,1),repeat=9):
        trials+=1
        if any(bits[x-1]!=v for x,v in pins.items()):continue
        if not all(any(bits[x-1]==0 for x in c) for c in N):continue
        for y in (0,1):
            if all(any(y if (j==0 and x==5) else bits[x-1] for x in c) for j,c in enumerate(P)):
                M[bits[4]][y]+=1
    return M,trials
def multiply(L,R):
    return [[sum(L[i][k]*R[k][j] for k in (0,1)) for j in (0,1)] for i in (0,1)]
def trace(word,M):
    v=[[1,0],[0,1]]
    for x in word:v=multiply(v,M[x])
    return v[0][0]+v[1][1]
if __name__=="__main__":
    assert all(valid(original(2*t),18*t) for t in range(1,5))
    ms={name:mat(p) for name,p in [('A',A),('B',B),('Z',Z),('Q',Q)]}
    assert {k:v[0] for k,v in ms.items()}=={
       'A':[[0,0],[23,36]],'B':[[0,0],[0,3]],'Z':[[34,47],[23,36]],'Q':[[0,13],[0,0]]}
    theta={(b,s):trace(('B' if b else 'A','Q' if s else 'Z'),{k:v[0] for k,v in ms.items()})
           for b in (0,1) for s in (0,1)}
    assert theta=={(0,0):2377,(0,1):299,(1,0):108,(1,1):0}
    tests=0
    for t in range(1,5):
        for v in product((0,1),repeat=2*t):
            beta,sigma=v[:t],v[t:]
            word=sum((('B' if b else 'A','Q' if s else 'Z') for b,s in zip(beta,sigma)),())
            count=trace(word,{k:z[0] for k,z in ms.items()})
            assert count==prod(theta[b,s] for b,s in zip(beta,sigma))
            assert (count>0)==(not any(b and s for b,s in zip(beta,sigma)))
            tests+=1
    def onebit(t):
        xs=range(1<<t);best=1.
        for mapping in product((0,1),repeat=1<<t):
            hits=0
            for k in range(t):
                for msg in (0,1):
                    a=sum(mapping[x]==msg and not (x>>k)&1 for x in xs)
                    b=sum(mapping[x]==msg and bool((x>>k)&1) for x in xs)
                    hits+=max(a,b)
            best=min(best,1-hits/(t*(1<<t)))
        return best
    assert [onebit(t) for t in (1,2,3)]==[0,.25,.25]
    print({"status":"PASS","trials":sum(x[1] for x in ms.values()),
           "factor":theta,"words":tests,"one_bit_errors":[0,.25,.25],
           "entropy_coeff_1_3":1+(1/3)*log2(1/3)+(2/3)*log2(2/3),
           "status_pnp":"OPEN"})
