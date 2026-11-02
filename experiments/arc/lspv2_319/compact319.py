#!/usr/bin/env python3
"""Compact independent reproduction of LSPV2 COFACTOR319.
Run: python compact319.py. Host-level operation test, not native FLMV.
Full proof-bearing producer, independent verifier, raw bitmaps in archived ZIP.
"""
from itertools import product
from collections import Counter

Y6=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
F9=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9)]

def valid(F):
    if not F:return False
    n=max(abs(z) for C in F for z in C)
    counts=Counter(z for C in F for z in C)
    return n%3==0 and len(F)*3==4*n and len(set(tuple(sorted(C)) for C in F))==len(F) and all(
        len(C)==3 and len(set(map(abs,C)))==3 and
        (all(z>0 for z in C) or all(z<0 for z in C)) for C in F) and all(
        counts[k]==counts[-k]==2 for k in range(1,n+1))
def truth(F,a):
    return all(any(a[abs(z)]==int(z>0) for z in C) for C in F)
def cover(F,p,x):
    return all(any(abs(z)!=x and abs(z) in p and p[abs(z)]==int(z>0) for z in C)
               for C in F if any(abs(z)==x for z in C))
def unit_conflict(H,p):
    a=dict(p)
    while True:
        changed=False
        for C in H:
            if any(abs(z) in a and a[abs(z)]==int(z>0) for z in C):continue
            u=[z for z in C if abs(z) not in a]
            if not u:return True
            if len(u)==1:
                k=abs(u[0]);v=int(u[0]>0)
                if k in a and a[k]!=v:return True
                if k not in a:a[k]=v;changed=True
        if not changed:return False
def guard(F,p,x):
    H=[C for C in F if all(abs(z)!=x for z in C)]
    incident=[C for C in F if any(abs(z)==x for z in C)]
    assert len(incident)==4
    for C in incident:
        r=[z for z in C if abs(z)!=x]
        if any(abs(z) in p and p[abs(z)]==int(z>0) for z in r):continue
        assumptions=dict(p);already=True
        for z in r:
            k=abs(z);v=int(z<0)
            if k in assumptions and assumptions[k]!=v:break
            assumptions[k]=v
        else:
            if not unit_conflict(H,assumptions):return False
    return True
def ground(F,p,x):
    n=max(abs(z) for C in F for z in C)
    free=[k for k in range(1,n+1) if k not in p and k!=x]
    pointwise=True;d0=d1=False
    for z in product((0,1),repeat=len(free)):
        a=dict(p);a.update(zip(free,z))
        b0=truth(F,{**a,x:0});b1=truth(F,{**a,x:1})
        pointwise &= b0==b1
        d0 |= b0;d1 |= b1
    return pointwise,d0==d1
def census(name,F):
    assert valid(F)
    n=max(abs(z) for C in F for z in C)
    stats=Counter()
    for x in range(1,n+1):
        rest=[k for k in range(1,n+1) if k!=x]
        for z in product((0,1,2),repeat=n-1):
            p={k:v for k,v in zip(rest,z) if v<2}
            a=cover(F,p,x);b=guard(F,p,x);piv,decision=ground(F,p,x)
            assert not a or b
            assert not b or piv
            stats['states']+=1;stats['cover']+=a;stats['guard']+=b
            stats['pointwise_noop']+=piv;stats['current_label_equal']+=decision
    print(name,dict(stats))
    return stats

if __name__=='__main__':
    a=census('Y6',Y6);b=census('F9',F9)
    assert (a['cover'],a['guard'],a['pointwise_noop'])==(56,324,344)
    assert (b['cover'],b['guard'],b['pointwise_noop'])==(4689,21659,24987)
    fixed={2:0,3:0,4:0,5:0,6:1}
    assert not truth(Y6,{**fixed,1:0}) and truth(Y6,{**fixed,1:1})
    print('PASS: exact cofactor guard counts and canonical pivotal gadget')
