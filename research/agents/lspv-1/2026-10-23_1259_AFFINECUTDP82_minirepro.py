#!/usr/bin/env python3
"""Minimal verification of AFFINECUTDP82: no third-party dependencies."""
from itertools import product
def rk(xs):
    piv={}
    for z in xs:
        while z:
            j=z.bit_length()-1
            if j in piv:z^=piv[j]
            else:piv[j]=z;break
    return len(piv)
def synd(A,x):
    return sum(((r&x).bit_count()%2)<<i for i,r in enumerate(A))
def widths(A,b,order,i):
    L=order[:i];R=order[i:];n=len(order)
    left=[r&sum(1<<v for v in L) for r in A]
    right=[r&sum(1<<v for v in R) for r in A]
    a=rk(left);c=rk(right);q=rk(A);eta=a+c-q
    aug=[r|(((b>>j)&1)<<n) for j,r in enumerate(A)]
    pred=1 if rk(aug)>q else (1<<eta)+(a>eta)
    obs=set()
    for bitsL in product([0,1],repeat=len(L)):
        x=sum(bit<<j for j,bit in zip(L,bitsL));res=[]
        for bitsR in product([0,1],repeat=len(R)):
            y=sum(bit<<j for j,bit in zip(R,bitsR))
            res.append(int(synd(A,x|y)==b))
        obs.add(tuple(res))
    assert len(obs)==pred,(len(obs),pred)
    return pred
for g in range(1,5):
    A=[(1<<i)|(1<<(g+i)) for i in range(g)]
    bad=list(range(3*g))
    good=[v for i in range(g) for v in [i,g+i,2*g+i]]
    wa=max(widths(A,0,bad,i) for i in range(3*g+1))
    wb=max(widths(A,0,good,i) for i in range(3*g+1))
    assert wa==2**g and wb<=3
    print({"g":g,"bad":wa,"interleaved":wb})
print("AFFINECUTDP82 mini reproducer PASS")
