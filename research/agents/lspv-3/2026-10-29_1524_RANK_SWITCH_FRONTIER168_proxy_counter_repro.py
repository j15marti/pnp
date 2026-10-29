#!/usr/bin/env python3
"""RANK-SWITCH-FRONTIER168: exact integer proxy and global-rank reset controls.
Standalone subset of the full 21-KB local Python SAT-controller reproducer.
This small file DOES NOT implement the authenticated full SAT controller.
All comparisons below are operation-count proxies, not SAT hardness.
"""
import json
import math
from itertools import combinations

def qmin(n,b):
    if b<1: raise ValueError("b>0")
    return max(0, (n-3*b+12*b-1)//(12*b))

def tmin(n):
    vals=[(b,b+qmin(n,b),qmin(n,b)) for b in range(1,n+1)]
    z=min(row[1] for row in vals)
    return z,[row for row in vals if row[1]==z]

def local_reset_actions(n):
    # Phase 0: A decreases r_A=1-p; phase 1: B decreases r_B=p.
    j=p=0
    actions=0
    while j<(1<<n):
        if p==0:
            assert 1-p==1
            p=1
        else:
            assert p==1
            j+=1
            p=0
        actions+=1
    return actions

def fixed_affine_enumeration_count(n,e):
    return sum(math.comb(n,j) for j in range(e+1))

def crossings(max_n=6000):
    functions={"frontier_32n":lambda n:32*n,
               "affine_e2_binomial":lambda n:fixed_affine_enumeration_count(n,2),
               "affine_e3_binomial":lambda n:fixed_affine_enumeration_count(n,3)}
    result={}
    for name,cost in functions.items():
        events=[]
        last=None
        for n in range(6,max_n+1,3):
            t,_=tmin(n)
            cheaper=cost(n)<2**t
            if last is None or last!=cheaper:
                events.append({"n":n,"proxy_time_exponent":t,"strategy_count":cost(n),
                               "strategy_count_strictly_smaller":cheaper})
                last=cheaper
        result[name]=events
    return result

def audit():
    for n in (4,8,12,16):
        assert local_reset_actions(n)==2**(n+1)
    t,mini=tmin(1200)
    assert t==20 and [row[0] for row in mini]==[9,10,11]
    assert qmin(1200,400)==0
    c=crossings()
    assert [e["n"] for e in c["frontier_32n"]]==[6,612]
    assert [e["n"] for e in c["affine_e2_binomial"]]==[6,1002,1026,1113]
    assert [e["n"] for e in c["affine_e3_binomial"]]==[6,2931,2955,3123]
    data={"run_id":"RANK-SWITCH-FRONTIER168","seed":1681029,
          "rank_reset_actions":{str(n):2**(n+1) for n in (4,8,12,16)},
          "static_integer_min":{"n":1200,"log2_enumeration":t,"minima":mini,
                                "earliest_time_space_table_proxy_equality":{"b":400,"q":0}},
          "operation_proxy_crossing_events_n_le_6000":c,
          "status":"PROVED/EXACT arithmetic checked computationally; not machine runtime"}
    return data

if __name__=="__main__":
    print(json.dumps(audit(),sort_keys=True,indent=2))
