#!/usr/bin/env python3
"""AFFINE-GUARD257 independent compact theorem check; Python 3 standard library.
The full producer, independent proof-tree checker and raw 26-instance corpus
are in LSPV2_AFFINE_GUARD257_2026-10-30.zip (run artifact).
P vs NP and the fully charged ARC contractor are OPEN.
"""
from itertools import product
from collections import defaultdict
import json

def cnf_xor(scope, rhs):
    return [tuple(-v if b else v for v,b in zip(scope,bits))
            for bits in product((0,1),repeat=len(scope))
            if sum(bits)%2 != rhs]

def sat(F):
    vs=sorted({abs(l) for c in F for l in c})
    return any(all(any(dict(zip(vs,bits))[abs(l)]==(l>0) for l in c)
                   for c in F) for bits in product((False,True),repeat=len(vs)))

def extract(F):
    groups=defaultdict(dict)
    for j,c in enumerate(F,1):
        scope=tuple(sorted(abs(l) for l in c))
        if len(set(scope))!=len(c):continue
        sign=tuple(int(next(l for l in c if abs(l)==v)<0) for v in scope)
        groups[scope][sign]=j
    out=[]
    for scope,records in groups.items():
        if len(scope)>12:continue
        for banned_parity in (0,1):
            wanted=[bits for bits in product((0,1),repeat=len(scope))
                    if sum(bits)%2==banned_parity]
            if all(bits in records for bits in wanted):
                out.append((scope,1-banned_parity,tuple(records[b] for b in wanted)))
    return sorted(out)

def row_truth(F,row):
    scope,rhs,ids=row
    seen=set()
    for j in ids:
        c=F[j-1]
        assert sorted(abs(l) for l in c)==list(scope)
        mask=tuple(int(next(l for l in c if abs(l)==v)<0) for v in scope)
        seen.add(mask)
    expected={bits for bits in product((0,1),repeat=len(scope))
              if sum(bits)%2!=rhs}
    assert seen==expected and len(ids)==len(expected)
    return sum(1<<(v-1) for v in scope),rhs

def verify_group_for_all_coherent_assignments(F,row):
    scope,rhs,ids=row
    for bits in product((0,1),repeat=len(scope)):
        a=dict(zip(scope,bits))
        clauses_sat=all(any(a[abs(l)]==(l>0) for l in F[j-1]) for j in ids)
        assert clauses_sat == (sum(bits)%2==rhs)

def xor_sum(terms):
    mask=rhs=0
    for m,b in terms:mask^=m;rhs^=b
    return mask,rhs

def verify_cases():
    c0=cnf_xor((1,2,3),0)
    c1=cnf_xor((1,2,4),0)
    c2=cnf_xor((3,4),1)
    cycle=c0+c1+c2
    e=extract(cycle)
    assert len(e)==3 and not sat(cycle)
    for row in e:
        verify_group_for_all_coherent_assignments(cycle,row)
    assert xor_sum(row_truth(cycle,row) for row in e)==(0,1)

    forced=cnf_xor((1,2,3),0)+cnf_xor((1,2),0)
    ef=extract(forced)
    assert len(ef)==2 and sat(forced)
    assert xor_sum(row_truth(forced,row) for row in ef)==(1<<(3-1),0)
    assert not sat(forced+[(3,)])  # x3=0 forced without search.

    incomplete=cnf_xor((1,2,3),0)[:-1]+[(1,2,3)]
    assert not extract(incomplete)
    assert sat(incomplete)
    # Both labels share the exact same authenticated affine extraction.
    base=cnf_xor((1,2,3),0)+[(1,),(-1,4),(-4,5)]
    yes=base+[(-5,1)]
    no=base+[(-5,-1)]
    assert extract(yes)==extract(no)
    assert sat(yes) and not sat(no)
    # A parity-only selector would classify these alike and is unsound.
    return {"run":"AFFINE-GUARD257","compact_checks_passed":True,
            "source_xor_cycle_unsat":True,"source_xor_forced_bit":3,
            "same_affine_core_opposite_labels":True,
            "incomplete_block_not_promoted":True,"arc_contraction":"OPEN"}

if __name__=="__main__":
    print(json.dumps(verify_cases(),sort_keys=True))
