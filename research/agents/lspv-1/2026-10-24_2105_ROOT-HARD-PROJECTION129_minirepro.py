#!/usr/bin/env python3
"""ROOT-HARD-PROJECTION129 compact independent semantic reproducer.
Runs the proper-three-clause compiler on every 3-variable clause subset.
This is finite COMPUTATIONAL evidence, not a SAT time/space lower bound.
"""
import itertools
import json

def xor_gadget(a,b,e):
    return [(a,b,-e),(-a,-b,-e),(a,-b,e),(-a,b,e)]

def force_false(v,p,q):
    return [(-v,sp*p,sq*q) for sp in (1,-1) for sq in (1,-1)]

def compile_root(source,n=3):
    """d=2,h=2: comparator [unsigned(b)<2] iff b_most=0."""
    b0,b1=n+1,n+2
    p,q=n+3,n+4
    clauses=list(source)+force_false(b1,p,q)
    e=n+5
    for v in list(range(2,n+1))+[b0,b1]:
        clauses.extend(xor_gadget(1,v,e))
        e+=1
    assert all(len({abs(v) for v in cl})==3 for cl in clauses)
    return clauses,(b0,b1)

def exact_sat(clauses,pins=None):
    """Independent exact DPLL, retaining pinned source/boundary assignments."""
    def search(a):
        a=dict(a)
        while True:
            progress=False
            for cl in clauses:
                if any(v in a and a[abs(v)]==(v>0) for v in cl):
                    continue
                unseen=[v for v in cl if abs(v) not in a]
                if not unseen:
                    return False
                if len(unseen)==1:
                    v=unseen[0]
                    a[abs(v)]=(v>0)
                    progress=True
                    break
            if not progress:
                break
        for cl in clauses:
            if any(v in a and a[abs(v)]==(v>0) for v in cl):
                continue
            v=next(v for v in cl if abs(v) not in a)
            for val in (False,True):
                b=dict(a);b[abs(v)]=val
                if search(b):
                    return True
            return False
        return True
    return search(pins or {})

signed_clauses=[tuple(sign*(j+1) for j,sign in enumerate(pattern))
                for pattern in itertools.product((-1,1),repeat=3)]
checks=0;sat_sources=0;unsat_sources=0;pin_checks=0
for mask in range(256):
    F=[signed_clauses[j] for j in range(8) if mask&(1<<j)]
    truth=any(all(any((v>0)==bool((bits>>(abs(v)-1))&1) for v in cl)
                  for cl in F) for bits in range(8))
    assert truth==exact_sat(F)
    clauses,b=compile_root(F)
    assert exact_sat(clauses)==truth
    for bits in range(4):
        pins={b[j]:bool((bits>>j)&1) for j in range(2)}
        answer=exact_sat(clauses,pins)
        assert answer==(truth and bits<2)
        checks+=1;pin_checks+=1
    sat_sources+=int(truth)
    unsat_sources+=int(not truth)
    checks+=2
print(json.dumps({"run_id":"ROOT-HARD-PROJECTION129",
                  "independent_test":"all 256 ternary clause subsets on three variables",
                  "SAT_sources":sat_sources,"UNSAT_sources":unsat_sources,
                  "pinned_cases":pin_checks,"assertions":checks,
                  "failures":0,"status":"COMPUTATIONAL only; ARC-EDGE-90 OPEN"},
                 indent=2))
