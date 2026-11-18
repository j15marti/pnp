#!/usr/bin/env python3
"""Independent compact CLOCKAFFINEISLAND45 reproduction; stdlib Python 3."""
from collections import Counter
from math import log2

def sample_indices(n):
    return [0]+[1<<k for k in range(n-1)]

def encode(z,n):
    return sum(1<<(2*j+((z>>j)&1 ^ 1)) for j in range(1<<(n-1)))

def output(f,n):
    N=1<<n
    p=tuple((f>>(2*j))&1 for j in sample_indices(n))
    full=int(f==(1<<N)-1)
    paired=int(any((f>>(2*j))&3==3 for j in range(N//2)))
    return p+(full,paired)

checks=0
for n in (2,3,4,5):
    B=1<<(n-1)
    hist=Counter()
    for z in range(1<<B):
        result=output(encode(z,n),n)
        assert result==tuple((z>>j)&1 for j in sample_indices(n))+(0,0)
        hist[result]+=1
        checks+=1
    assert len(hist)==1<<n and set(hist.values())=={1<<(B-n)}
    checks+=2

n=20;t=4096;s=500;N=1<<n;B=N//2
logU=log2(t+1)+log2(n+t+2)+t*(4+2*log2(n+t+2))
assert n*n+10<=s<=t and B-n>logU
checks+=1
print({'run':'CLOCKAFFINEISLAND45','checks':checks,'failures':0,
       'n20_min_fiber_log2':B-n,'n20_upper_log2_easy_circuits':round(logU,4),
       'n20_yes_gate_bound':n*n+10,'P_vs_NP':'OPEN'})
