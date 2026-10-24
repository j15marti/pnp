#!/usr/bin/env python3
"""OVERLAP-CUT128 independent compact reproduction (Python standard library).
Certified scoped named streams only. Not an all-input SAT-time bound.
The 1525-check extended auditor is a separate downloadable artifact.
"""
from itertools import product
from functools import lru_cache
from random import Random
import json

SEED = 202610250036

def scan(ev):
    seen, live, cutsets, clauses = set(), set(), [frozenset()], []
    for op, val in ev:
        if op == "O":
            assert val > 0 and val not in seen
            seen.add(val); live.add(val)
        elif op == "D":
            assert val in live
            live.remove(val)
        elif op == "C":
            assert len(val) == 3 and len({abs(z) for z in val}) == 3
            assert all(abs(z) in live for z in val)
            clauses.append(val)
        else:
            raise AssertionError(op)
        cutsets.append(frozenset(live))
    assert not live
    return cutsets, clauses

def edge(a, b, name_aware=True):
    return 1 << (len(a | b) if name_aware else len(a) + len(b))

def shortest(cuts, block, aware=True):
    L = len(cuts)-1
    d = max(1,block//2)
    cost = [None]*(L+1)
    pred = [None]*(L+1)
    cost[0] = 0
    for j in range(1,L+1):
        for i in range(max(0,j-block),j):
            if (j != L and j-i < d) or cost[i] is None: continue
            z = cost[i] + edge(cuts[i], cuts[j], aware)
            if cost[j] is None or z < cost[j]:
                cost[j],pred[j] = z,i
    assert cost[L] is not None
    p = [L];j = L
    while j:
        j=pred[j]; p.append(j)
    return cost[L],tuple(p[::-1])

def core(h, unsat):
    clauses = []
    for bits in product((0,1),repeat=3):
        row = tuple(-v if bits[v-1] else v for v in (1,2,3))
        if not unsat and bits == (1,1,1):row=(1,2,3)
        clauses.append(row)
    clauses += [(1,2,v) for v in range(4,h+1)]
    clauses += [(1,2,3)]*(10*h-len(clauses))
    ev = [("O",v) for v in range(1,h+1)]
    ev += [("C",c) for c in clauses]
    ev += [("D",v) for v in range(h,0,-1)]
    return ev

def random_stream(seed):
    r=Random(SEED+seed)
    k=r.randint(4,14);T=r.randint(9,29)
    opens={t:[] for t in range(T)}
    closes={t:[] for t in range(T)}
    for x in range(4,k+1):
        a=r.randrange(0,T-1)
        z=r.randrange(a+1,T)
        opens[a].append(x);closes[z].append(x)
    ev=[("O",x) for x in (1,2,3)]
    for t in range(T):
        for x in sorted(opens[t]):ev.append(("O",x))
        ev.append(("C",(1,2,3)))
        for x in sorted(closes[t]):ev.append(("D",x))
    ev += [("D",x) for x in (3,2,1)]
    return ev,r.randint(5,17)

def has_witness(clauses,n):
    return any(all(any((a[abs(z)-1] if z>0 else not a[abs(z)-1]) for z in row)
                   for row in clauses)
               for a in product((False,True),repeat=n))

def audit():
    checks=0
    for h in (3,4,6,8,10,12,16):
        both=[]
        for unsat in (False,True):
            cuts,clauses=scan(core(h,unsat))
            if h <= 8:
                assert has_witness(clauses,h)==(not unsat);checks+=1
            old,p0=shortest(cuts,4*h,False)
            new,p1=shortest(cuts,4*h,True)
            assert old==2**(2*h)+2**(h+1)
            assert new==3*2**h
            assert p0==p1==(0,4*h,8*h,12*h)
            both.append((old,new))
            checks+=3
        assert both[0]==both[1]
        checks+=1
    # Matched opposite labels with different optimum schedules.
    ev,b=random_stream(84)
    rows=[tuple(-v if bits[v-1] else v for v in (1,2,3))
          for bits in product((0,1),repeat=3)]
    matched=[]
    for unsat in (False,True):
        rs=rows[:]
        if not unsat:rs[-1]=(1,2,3)
        candidate=ev[:3]+[("C",row) for row in rs]+ev[3:]
        cuts,clauses=scan(candidate)
        assert has_witness(clauses,max(abs(z) for row in clauses for z in row))==(not unsat)
        old,pold=shortest(cuts,b,False)
        new,pnew=shortest(cuts,b,True)
        cost_old_under_new=sum(edge(cuts[i],cuts[j]) for i,j in zip(pold,pold[1:]))
        assert (old,new,cost_old_under_new)==(9224,776,2056)
        assert pold==(0,12,29,45) and pnew==(0,8,21,38,45)
        matched.append((old,new))
        checks+=5
    assert matched[0]==matched[1]
    print(json.dumps({"status":"PASS","checks":checks,
        "core_h":[3,4,6,8,10,12,16],
        "seed84":{"old_product":9224,"true_union":776,"old_path_union":2056},
        "scope":"restricted certified original-source names; not FLMV physical counts"},
        sort_keys=True))
if __name__=="__main__":audit()
