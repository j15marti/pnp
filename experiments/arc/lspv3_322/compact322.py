#!/usr/bin/env python3
"""LSPV-3 GATE322 compact standalone reproduction; all truth tables are OFFLINE."""
from collections import Counter,defaultdict
from itertools import combinations
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
    (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
def valid(F,n):
    d=Counter();seen=set()
    if n%3 or len(F)*3!=4*n:return False
    for c in F:
        if len(c)!=3 or len({abs(z) for z in c})!=3 or any(type(z)!=int or not 1<=abs(z)<=n for z in c):return False
        if not(all(z>0 for z in c) or all(z<0 for z in c)):return False
        if tuple(sorted(c)) in seen:return False
        seen.add(tuple(sorted(c)));d.update(c)
    return all(d[v]==d[-v]==2 for v in range(1,n+1))
def original(F,x):
    return all(any(bool(x&(1<<(abs(z)-1)))==(z>0) for z in c) for c in F)
def residual(F,S,A):
    out=[]
    for j,c in enumerate(F):
        if any((S>>(abs(z)-1)&1) and bool(A&(1<<(abs(z)-1)))==(z>0) for z in c):continue
        rem=frozenset(z for z in c if not(S>>(abs(z)-1)&1))
        if not rem:return None
        out.append((j,rem))
    return out
def antichain(rows):
    if rows is None:return ('DEAD',)
    return tuple(sorted(tuple(sorted(c)) for _,c in rows
        if not any(k!=j and (d<c or(d==c and k<j)) for k,d in rows)))
def up(key):
    if key==('DEAD',):return key
    cs=[set(c) for c in key];forces={}
    while True:
        fresh=[]
        for c in cs:
            if len(c)==1:
                z=next(iter(c))
                if abs(z) in forces and forces[abs(z)]!=z:return ('DEAD',)
                if abs(z) not in forces:fresh.append(z)
        if not fresh:break
        for z in fresh:
            if abs(z) in forces and forces[abs(z)]!=z:return ('DEAD',)
            forces[abs(z)]=z
        cs=[{z} for z in forces.values()]+[
            c.difference({-z for z in forces.values()}) for c in cs
            if len(c)>1 and not any(z in c for z in forces.values())]
        if any(not c for c in cs):return ('DEAD',)
    unique={frozenset(c) for c in cs}
    return tuple(sorted(tuple(sorted(c)) for c in unique if not any(d<c for d in unique)))
def source(F,S,A):
    out=[]
    for j,c in enumerate(F):
        inside=[z for z in c if S>>(abs(z)-1)&1]
        if len(inside)==3 and not any(bool(A&(1<<(abs(z)-1)))==(z>0) for z in c):
            return ('DEAD',)
        if inside and len(inside)<3:
            if any(bool(A&(1<<(abs(z)-1)))==(z>0) for z in inside):out.append(j)
    return (S,tuple(out))
def truth(T,n,S,A):
    free=[i for i in range(n) if not(S>>i&1)]
    z=0
    for x in range(1<<len(free)):
        full=A|sum(((x>>j)&1)<<i for j,i in enumerate(free))
        z|=int(T[full])<<x
    return z
def census(F,n):
    assert valid(F,n)
    T=[original(F,x) for x in range(1<<n)]
    totals=Counter()
    for S in range(1<<n):
        vars=[i for i in range(n) if S>>i&1]
        groups=[defaultdict(set) for _ in range(4)]
        sem=set()
        for q in range(1<<len(vars)):
            A=sum(((q>>j)&1)<<i for j,i in enumerate(vars))
            s=source(F,S,A);a=antichain(residual(F,S,A));u=up(a)
            t=truth(T,n,S,A)
            for group,key in zip(groups,(s,a,u)):group[key].add(t)
            sem.add(t);totals['cubes']+=1
            totals['offline_truth_bits']+=1<<(n-len(vars))
        assert all(len(g)==1 for d in groups for g in d.values())
        for typ,group in zip(('source_keys','antichain_keys','unit_keys'),groups):
            totals[typ]+=len(group)
        totals['semantic_cofactors']+=len(sem)
    return {'models':sum(T),**totals}
if __name__=='__main__':
    import json
    f9=census(F9,9);y6=census(Y6,6)
    assert [f9[k] for k in ('source_keys','antichain_keys','unit_keys','semantic_cofactors')]==[10325,8486,7036,7026]
    assert [y6[k] for k in ('source_keys','antichain_keys','unit_keys','semantic_cofactors')]==[483,420,400,400]
    bad=(F9[:-1],F9+((1,2,3),),F9[:-1]+((1,1,2),),F9[:-1]+((1,2,-3),))
    assert all(not valid(f,9) for f in bad)
    print(json.dumps({'F9':f9,'Y6':y6,'malformed_rejected':len(bad),
                      'note':'No free SAT label: complete truth tables are offline diagnostic only.'},indent=2))
