#!/usr/bin/env python3
"""stdlib-only independent exhaustive audit; n<=6, one 15-variable UNSAT sample."""
from functools import lru_cache
from itertools import combinations,product
import json
K4=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6)]
H1=[(1,3,5),(1,-3,6),(-1,4,5),(-1,-4,6),(2,3,-5),(2,-3,-6),(-2,4,-5),(-2,-4,-6)]
W1=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
def t(c,a):return sum(((a>>(abs(l)-1))&1)==(l>0) for l in c)
def demand(c,mode):return {abs(l):int(l>0) if mode=='S' else int(l<0) for l in c}
def pair(c,d):
    vs=sorted(set(map(abs,c+d)))
    for u,v in product('SU',repeat=2):
        a,b=demand(c,u),demand(d,v)
        theory=all(a[x]==b[x] for x in a.keys()&b.keys())
        enum=any(t(c,z)==(3 if u=='S' else 0) and t(d,z)==(3 if v=='S' else 0)
                 for z in (sum(bit<<(x-1) for bit,x in zip(bits,vs))
                           for bits in product((0,1),repeat=len(vs))))
        assert theory==enum
    return 4
def tau(F,anchor):
    n=max(abs(l) for c in F for l in c)
    bad=[i for i,c in enumerate(F) if t(c,anchor)==0]
    incid={x:[i for i in bad if x in set(map(abs,F[i]))] for x in range(1,n+1)}
    assert max(map(len,incid.values()),default=0)<=2
    edges={(bad.index(js[0]),bad.index(js[1])) for js in incid.values() if len(js)==2}
    q=len(bad)
    @lru_cache(None)
    def matching(mask):
        if mask==0:return 0
        i=(mask&-mask).bit_length()-1
        v=matching(mask^(1<<i))
        for j in range(q):
            if mask&(1<<j) and ((i,j) in edges or (j,i) in edges):
                v=max(v,1+matching(mask^(1<<i)^(1<<j)))
        return v
    result=q-matching((1<<q)-1)
    for h in range(n+1):
        exists=any(all(any(abs(l) in S for l in F[j]) for j in bad)
                   for S in combinations(range(1,n+1),h))
        if exists:assert h==result;break
    return result

def up_dpll(F):
    n=max(abs(l) for c in F for l in c);nodes=0
    def up(r):
        r=dict(r)
        while True:
            changed=False
            for c in F:
                if any(abs(l) in r and r[abs(l)]==(l>0) for l in c):continue
                free=[l for l in c if abs(l) not in r]
                if not free:return None
                if len(free)==1:r[abs(free[0])]=int(free[0]>0);changed=True
            if not changed:return r
    def go(r):
        nonlocal nodes;nodes+=1
        r=up(r)
        if r is None:return None
        if len(r)==n:return r
        x=next(i for i in range(1,n+1) if i not in r)
        for val in (0,1):
            hit=go({**r,x:val})
            if hit is not None:return hit
        return None
    answer=go({})
    if answer is not None:assert all(any(answer[abs(l)]==(l>0) for l in c) for c in F)
    return nodes,answer is not None

def check(name,F):
    n=max(abs(l) for c in F for l in c)
    for j,c in enumerate(F):
        for l in c:
            assert demand(c,'S')[abs(l)]==int(l>0)
            assert demand(c,'U')[abs(l)]==int(l<0)
    tests=sum(pair(F[i],F[j]) for i,j in combinations(range(len(F)),2))
    for a in range(1<<n):
        b=((1<<n)-1)^a
        assert all(t(c,b)==3-t(c,a) for c in F)
    ta=[tau(F,a) for a in (0,(1<<n)-1)]
    cubes=0
    if n<=6:
        for row in product((None,0,1),repeat=n):
            rho={i+1:v for i,v in enumerate(row) if v is not None}
            for a,T in zip((0,(1<<n)-1),ta):
                far=sum(v!=((a>>(i-1))&1) for i,v in rho.items())+n-len(rho)
                if far<T:
                    cubes+=1
                    assert any(all(abs(l) in rho and rho[abs(l)]==((a>>(abs(l)-1))&1) for l in c)
                               for c in F if not t(c,a))
    nodes,sat=up_dpll(F)
    assert sat==any(all(t(c,a)>0 for c in F) for a in range(1<<n))
    return dict(name=name,n=n,m=len(F),SAT=sat,UP_DPLL_nodes=nodes,
                pair_checks=tests,anchor_taus=ta,certified_balls_partial_cubes=cubes,
                N0123_0=[sum(t(c,0)==r for c in F) for r in range(4)],
                N0123_1=[sum(t(c,(1<<n)-1)==r for c in F) for r in range(4)])
if __name__=='__main__':print(json.dumps([check('K4_SAT',K4),check('H1_SAT',H1),check('W1_UNSAT',W1)],indent=2))
