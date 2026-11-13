#!/usr/bin/env python3
"""LSPV-4/588 independent typed-local-row span/register DP audit.
No original checker is executed here. Run:
python3 experiments/arc/lspv4_588_independent_dp.py
"""
import json
from functools import lru_cache
@lru_cache(None)
def all_shapes(n):
    if n == 1: return frozenset({(3,1),(2,2)})
    out=set()
    for k in range(1,n):
        for da,ra in all_shapes(k):
            for db,rb in all_shapes(n-k):
                out.add((1+max(da,db),max(ra,rb)+(ra==rb)))
    return frozenset(out)
def pareto(points):
    return frozenset((d,r) for d,r in points if not any(
        e<=d and s<=r and (e<d or s<r) for e,s in points))
@lru_cache(None)
def dp(n):
    if n==1: return frozenset({(3,1),(2,2)})
    out=set()
    for k in range(1,n):
        for da,ra in dp(k):
            for db,rb in dp(n-k):
                out.add((1+max(da,db),max(ra,rb)+(ra==rb)))
    return pareto(out)
for n in range(1,9):
    assert pareto(all_shapes(n))==dp(n), n
frontier={}
for n in [4,6,8,10,12,32]:
    pts=sorted(dp(n),key=lambda z:-z[0])
    assert min(d for d,r in pts)==2+(n-1).bit_length()
    assert (n+2,2) in pts
    frontier[str(n)]=[{"span":d,"registers":r} for d,r in pts]
print(json.dumps({"id":"LSPV4-588-INDEPENDENT","exhaustive_plain_tree_n1_to_n8":"PASS",
 "source_model":"four read-only SOURCE leaves per local row; AND3 quartet; XOR joins",
 "frontier":frontier,"original_checker_executed":False},indent=2))
