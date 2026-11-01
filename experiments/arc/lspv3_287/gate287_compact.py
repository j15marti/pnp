#!/usr/bin/env python3
"""GATE287: independent exhaustive small canonical M22 forced-value certificates."""
from itertools import product, combinations

Y = [[1,2,3],[1,4,5],[2,4,6],[3,5,6],
     [-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]]
C = [[1,2,3],[1,4,5],[2,6,7],[4,6,8],[3,9,10],
     [5,9,11],[7,10,12],[8,11,12],[-1,-9,-11],[-5,-7,-8],
     [-4,-6,-10],[-3,-6,-11],[-1,-2,-3],[-2,-8,-12],[-4,-9,-12],[-5,-7,-10]]

def check_grammar(f,n):
    assert len(f)*3==4*n and len(set(tuple(sorted(c)) for c in f))==len(f)
    assert all(len(c)==3 and len(set(map(abs,c)))==3
               and (all(x>0 for x in c) or all(x<0 for x in c)) for c in f)
    assert all(sum(x==i for c in f for x in c)==2
               and sum(x==-i for c in f for x in c)==2 for i in range(1,n+1))

def exact_cover(f,p,sign):
    free=[i for i,x in enumerate(p) if x is None]
    required=[]
    for c in f:
        if (c[0]>0)!=(sign>0): continue
        if any(p[abs(x)-1] is not None
               and p[abs(x)-1]==int(x>0) for x in c): continue
        candidates=[i for i in range(len(free)) if free[i]+1 in map(abs,c)]
        if not candidates: return float("inf")
        required.append(sum(1<<i for i in candidates))
    for k in range(len(free)+1):
        for indices in combinations(range(len(free)),k):
            chosen=sum(1<<i for i in indices)
            if all(chosen&mask for mask in required): return k
    return float("inf")

def valid_models(f,p,w):
    return [''.join(map(str,a)) for a in product((0,1),repeat=len(p))
            if sum(a)==w and all(x is None or a[i]==x for i,x in enumerate(p))
            and all(any(a[abs(l)-1]==int(l>0) for l in c) for c in f)]

for name,f,w,forced in [('Y6',Y,4,[5]),('CUBE12',C,8,[6,12])]:
    n=max(abs(x) for c in f for x in c)
    check_grammar(f,n)
    p=[0]+[None]*(n-1)
    budget=n-w-p.count(0)
    before=exact_cover(f,p,-1)
    assert before==budget and valid_models(f,p,w)
    for v in forced:
        q=p.copy();q[v-1]=1
        assert exact_cover(f,q,-1)>budget
        assert valid_models(f,q,w)==[]
    print(name,'weight',w,'forced FALSE variables',forced,
          'remaining witnesses',len(valid_models(f,p,w)))
assert len(valid_models(Y,[0]+[None]*5,3))==7
assert any(s[4]=='1' for s in valid_models(Y,[0]+[None]*5,3))
print('PASS. Fixed-weight deductions do not extend to different weights.')
