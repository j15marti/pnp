#!/usr/bin/env python3
"""LSPV-1/544 finite independent verifier for a shared-AND/OR obligation system.
It is not a historical R_mix341 checker and does not decide CNF-SAT.
"""
from fractions import Fraction
from itertools import combinations
import json

def universe(n):
    return set(combinations(range(n), 2))

def verify(n):
    U=universe(n)
    stars=[{e for e in U if i in e} for i in range(n)]
    feasible=[]
    transitions=0
    weights={e:Fraction(1,n-1) for e in U}
    assert all(sum((weights[e] for e in stars[i]),Fraction(0))==1 for i in range(n))
    for mask in range(1<<n):
        paid={i for i in range(n) if mask & (1<<i)}
        covered=set().union(*(stars[i] for i in paid)) if paid else set()
        is_goal=(covered==U)
        assert is_goal==(len(paid)>=n-1)
        if is_goal: feasible.append(len(paid))
        for i in range(n):
            next_covered=covered|stars[i]
            delta=sum((weights[e] for e in next_covered-covered),Fraction(0))
            cost=0 if i in paid else 1
            assert delta <= cost
            transitions += 1
    assert min(feasible)==n-1
    assert sum(weights.values(),Fraction(0))==Fraction(n,2)
    return {"n":n, "obligations":len(U), "subsets_checked":1<<n,
            "transitions_checked":transitions,"integer_optimum":min(feasible),
            "max_additive_potential":str(Fraction(n,2)),
            "additive_gap":str(Fraction(2*(n-1),n))}

if __name__=="__main__":
    cases=[verify(n) for n in range(3,10)]
    print(json.dumps({"status":"PASS", "model":"distinct abstract AND/OR cover-only, NOT R_mix341",
        "all_cases":cases, "total_subsets":sum(x["subsets_checked"] for x in cases),
        "total_transitions":sum(x["transitions_checked"] for x in cases),
        "exact_rational":True, "seed":None, "historical_checker_executed":False},
        indent=2,sort_keys=True))
