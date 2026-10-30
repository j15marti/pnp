#!/usr/bin/env python3
"""Independent concise hostile controls for OCCURRENCE-LAZY-MERGE176.
Python 3 stdlib. Run directly; no SAT oracles, third-party dependencies.
For full 4063-prefix and charged DPLL study see full _repro.py artifact.
"""
from collections import defaultdict
from itertools import product

def grid(r,s):
    return [(1,2,2+i) for i in range(1,r+1)] + [(-1,2,2+r+j) for j in range(1,s+1)]

def one_step(F):
    out=[]
    for x in {abs(l) for c in F for l in c}:
        for A in F:
            if x not in A: continue
            for B in F:
                if -x not in B:continue
                a=set(A)-{x}; b=set(B)-{-x}; R=a|b
                if all(-l not in R for l in R):out.append((tuple(sorted(R)),bool(a&b)))
    return out

def val(l,p):
    x=p[abs(l)-1]
    return None if x is None else x==(l>0)

def up(F,p):
    p=list(p)
    while True:
        change=False
        for c in F:
            states=[val(l,p) for l in c]
            if True in states:continue
            left=[l for l,s in zip(c,states) if s is None]
            if not left:return True,tuple(p)
            if len(left)==1:
                i=abs(left[0])-1;v=left[0]>0
                if p[i] is None:p[i]=v;change=True
        if not change:return False,tuple(p)

def lazy(F,p):
    bad,s=up(F,p)
    if bad:return True,s
    for _ in range(len(s)+1):
        if all(any(val(l,s) for l in c) for c in F):return False,s
        chosen=None
        for R,merge in one_step(F):
            if not merge:continue
            q=[val(l,s) for l in R]
            if True in q:continue
            unset=[l for l,z in zip(R,q) if z is None]
            if len(unset)==1:chosen=unset[0];break
        if chosen is None:return False,s
        z=list(s);z[abs(chosen)-1]=chosen>0
        bad,s=up(F,z)
        if bad:return True,s
    raise AssertionError('too many firings')

def check(F,n):
    H=F+[R for R,_ in one_step(F)]
    cnt=0
    for p in product((None,False,True),repeat=n):
        a=up(H,p);b=lazy(F,p)
        assert a[0]==b[0] and (a[0] or a[1]==b[1]),(F,p,a,b)
        cnt+=1
    return cnt

def cubes(F,n):
    rs=[R for R,_ in one_step(F)]
    overlap=0
    for a in product((False,True),repeat=n):
        hit=any(all(val(l,a) is False for l in R) for R in rs)
        original=any(all(val(l,a) is False for l in C) for C in F)
        assert not hit or original
        overlap+=hit
    return len(rs),len(set(rs)),overlap

def main():
    F=grid(2,2)
    assert check(F,6)==729
    assert cubes(F,6)==(4,4,18)
    assert cubes(grid(3,3),8)==(9,9,98)
    xor=[(1,2,3),(1,-2,-3),(-1,2,-3),(-1,-2,3)]
    assert check(xor,3)==27 and len(one_step(xor))==0
    assert check([(1,2),(-1,3),(-3,2)],3)==27
    assert check([(-1,-2,3),(-3,4),(-4,)],4)==81
    assert check([tuple(sign*(i+1) for i,sign in enumerate(bits))
                   for bits in product((-1,1),repeat=3)],3)==27
    for t in range(1,7):
        F=grid(t,t);n=2*t+2
        m,d,c=cubes(F,n)
        assert (m,d,c)==(t*t,t*t,2*(2**t-1)**2)
    print('SPOTCHECK PASS: 891 exhaustive partial prefixes, six exact grid cubes, XOR, 2SAT, Horn, UNSAT')

if __name__=='__main__':main()
