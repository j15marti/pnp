#!/usr/bin/env python3
"""LSPV-2 368 public exact local falsified-premise tree optimizer.
This checks local semantic implications, NOT a global Rmix341 optimum.
The independent complete proof-DAG verifier and full data live in the ZIP archive.
"""
from functools import lru_cache
from itertools import product
import json

FIXTURES = [
    ("two_sat_resolvent", 3, [(1,2),(-1,3)], [(2,3)], [2]),
    ("two_sat_forced_unit", 2, [(1,2),(-1,2)], [(2,)], [2]),
    ("three_link_chain", 4, [(1,2),(-2,3),(-3,4)], [(1,4)], [3]),
    ("equality_xor_eliminate", 3, [(-1,2),(1,-2),(-2,3),(2,-3)], [(-1,3),(1,-3)], [2,2]),
    ("parity_all_eight_blocks", 3,
     [tuple(-i if (k >> (i-1))&1 else i for i in range(1,4)) for k in range(8)],
     [()], [8]),
    ("short_unit_with_wide_irrelevant", 6,
     [(1,), (2,3,4,5,6), (-2,3,4,5,6)], [(1,)], [1]),
    ("not_entailed_sat", 2, [(1,2)], [(1,)], [None]),
    ("opposite_label_sat", 2, [(1,2)], [(2,)], [None]),
    ("contradictory_units", 1, [(1,),(-1,)], [()], [2]),
]

def valid_clause(c, n):
    if not isinstance(c,(list,tuple)) or any(type(l) is not int or not l or abs(l)>n for l in c):
        raise ValueError("malformed literal")
    if len(set(c))!=len(c) or any(-l in c for l in c):
        raise ValueError("duplicate or tautological literal")
    return tuple(c)

def false_clause(c, a):
    return all(abs(l) in a and bool(a[abs(l)]) == (l<0) for l in c)

def min_leaves(n, premises, conclusion):
    p=[valid_clause(c,n) for c in premises]
    c=valid_clause(conclusion,n)
    scope=sorted({abs(x) for cl in p+[c] for x in cl})
    fixed={abs(l):int(l<0) for l in c}
    @lru_cache(None)
    def f(items):
        a=dict(items)
        if any(false_clause(cl,a) for cl in p): return 1
        available=[v for v in scope if v not in a]
        if not available: return float("inf")
        return min(f(tuple(sorted([*items,(v,0)])))+
                   f(tuple(sorted([*items,(v,1)]))) for v in available)
    ans=f(tuple(sorted(fixed.items())))
    return None if ans==float("inf") else ans

def main():
    tests=0
    rec=[]
    for name,n,p,targets,expected in FIXTURES:
        found=[min_leaves(n,p,c) for c in targets]
        assert found==expected, (name,found,expected)
        tests+=len(targets)
        rec.append(dict(name=name, min_leaves=found))
    for malformed in ([0],[1,-1],[1,1],[7]):
        try: valid_clause(malformed,3)
        except ValueError: continue
        raise AssertionError("accepted malformed literal list")
    print(json.dumps(dict(status="PASS",fixture_count=len(FIXTURES),targets=tests,
         entailed=8,not_entailed=2,malformed_rejected=4,records=rec,
         scope="exact local variable-query tree only; no B1, B2 or B3 result"),indent=2))

if __name__=="__main__":
    main()
