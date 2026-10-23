#!/usr/bin/env python3
"""Minimal stdlib recheck of LSPV-4 PROJECTION-BLOWUP59."""
from itertools import product

def build(p, positive):
    ids = {}
    def var(name):
        if name not in ids:
            ids[name] = len(ids) + 1
        return ids[name]
    A = [var("a"+str(i)) for i in range(p)]
    B = [var("b"+str(i)) for i in range(p)]
    u = var("u")
    clauses = [(-x, u) for x in A] + [(-u, -x) for x in B]
    blockers = [var(s) for s in ("s", "t", "v", "w")]
    for i, x in enumerate(blockers):
        r = var("r"+str(i))
        clauses.extend([(-x,r),(-x,-r)])
    fillers = []
    for z in A+B:
        f = var("f"+str(z)); g = var("g"+str(z))
        fillers.extend((f,g)); clauses.append((z,f,g))
    for f in fillers:
        h = var("h"+str(f))
        clauses.extend([(-f,h),(f,-h)])
    clauses.extend([(A[0],blockers[0],blockers[1]),
                    (B[0] if positive else -B[0],blockers[2],blockers[3])])
    return ids, clauses

def solve(clauses, assignment=None):
    a = dict(assignment or {})
    while True:
        simplified=[]; units=[]
        for clause in clauses:
            if any(abs(l) in a and a[abs(l)] == (l>0) for l in clause):
                continue
            rest = [l for l in clause if abs(l) not in a]
            if not rest: return None
            simplified.append(rest)
            if len(rest)==1: units.append(rest[0])
        if not units: break
        old = len(a)
        for lit in units:
            v=abs(lit); val=(lit>0)
            if v in a and a[v]!=val: return None
            a[v]=val
        if len(a)==old: break
        clauses=simplified
    if not simplified: return a
    v=abs(simplified[0][0])
    for val in (False,True):
        result=solve(simplified,{**a,v:val})
        if result is not None: return result
    return None

def check(p):
    for positive in (False,True):
        ids,cls=build(p,positive)
        assert len(ids)==10*p+9 and len(cls)==12*p+10
        assert all(len(c) in (2,3) and len({abs(x) for x in c})==len(c) for c in cls)
        signed={l for c in cls for l in c}
        assert all(v in signed and -v in signed for v in range(1,len(ids)+1))
        found=solve(cls)
        assert (found is None)==positive
        if found is not None:
            filled={v:found.get(v,False) for v in range(1,len(ids)+1)}
            assert all(any(filled[abs(l)] == (l>0) for l in c) for c in cls)
    for av,bv in product(range(1<<p),repeat=2):
        expected=av==0 or bv==0
        mediated=any((all(not(av>>i&1) or u for i in range(p)) and
                      all(not u or not(bv>>j&1) for j in range(p)))
                     for u in (False,True))
        assert expected==mediated
        projected=all(not(av>>i&1 and bv>>j&1) for i in range(p) for j in range(p))
        assert projected==expected
    return dict(p=p,n=10*p+9,m=12*p+10,k=2*p+2,projected_clauses=p*p)

if __name__=="__main__":
    for p in range(1,7):
        print(check(p))
