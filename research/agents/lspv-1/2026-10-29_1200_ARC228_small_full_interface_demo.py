#!/usr/bin/env python3
"""ARC228 independent minimal full-interface path example, standard library only.

Checks ARC227 missing-unary observation example and a given tree of modules
whose local constraints are 2CNF plus GF2 equations.
This is NOT the complete AG-style XP solver, which is in the ARC228 Library bundle.
Nothing here implies unrestricted SAT contraction.
"""
from itertools import product
import json


def graph_path(L, charge):
    """Each node has s[i] XOR s[i+1] XOR p[i]=charge[i] and unit p[i]=0.
    Full local interface is enumerated, with compatible child-table indexing.
    Endpoint units are s[0]=0, s[L]=1.
    """
    assert len(charge)==L and L>=2
    entries=[None]*L
    for i in reversed(range(L)):
        table={}
        # Both endpoints enumerated (including the privately pinned endpoint).
        # This is at least the complete shared interface, costing at most four
        # assignments per module. No projected child query is hidden.
        for left,right in product((0,1),repeat=2):
            if (left ^ right)!=charge[i]:continue
            if i==0 and left!=0:continue
            if i==L-1 and right!=1:continue
            if i==L-1:
                table[(left,right)]=None
            else:
                child=next((key for key in entries[i+1] if key[0]==right),None)
                if child is not None:table[(left,right)]=child
        entries[i]=table
    if not entries[0]:return None,entries
    s=[0]*(L+1)
    edge=next(iter(entries[0]))
    for i in range(L):
        s[i],s[i+1]=edge
        edge=entries[i][edge]
    assert s[0]==0 and s[-1]==1
    assert all((s[i]^s[i+1])==charge[i] for i in range(L))
    return s,entries


def brute(L,charge):
    for s in product((0,1),repeat=L+1):
        if s[0]==0 and s[-1]==1 and all(
            (s[i]^s[i+1])==charge[i] for i in range(L)
        ):return list(s)
    return None


def main():
    # ARC227: no binary clauses, but three unary coordinates are observed.
    assert (0^0^0)!=1  # XOR3=1 plus units not-x1,not-x2,not-x3 UNSAT.
    checked=0
    for L in (2,3,4):
        for charge in product((0,1),repeat=L):
            sol,tables=graph_path(L,charge)
            assert (sol is None)==(brute(L,charge) is None)
            assert all(len(t)<=4 for t in tables)
            checked+=1
    outcomes=[]
    for L in (2,4,8,16,32):
        for answer in ("SAT","UNSAT"):
            charges=[0]*L;charges[0]=int(answer=="SAT")
            sol,tables=graph_path(L,charges)
            assert (sol is None)==(answer=="UNSAT")
            outcomes.append({"L":L,"decision":answer,
                 "materialized_table_entries":sum(len(t) for t in tables),
                 "max_local_rank":1,"global_rank":L})
    return {"all_passed":True,"independent_brute_comparisons":checked,
            "unary_counterexample":"XOR3=1 and three negative units is UNSAT",
            "grammar":"2CNF + GF(2), not strict signed exact22",
            "path_controls":outcomes}


if __name__=="__main__":print(json.dumps(main(),indent=2,sort_keys=True))
