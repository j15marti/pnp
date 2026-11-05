#!/usr/bin/env python3
"""Finite mock-clock and original signed SAT controls; not a HALT oracle."""
from itertools import combinations, product
import json, hashlib

def signed(n, cs):
    return f"p cnf {n} {len(cs)}\n" + "".join(" ".join(map(str,c))+" 0\n" for c in cs)
def U(n):
    return signed(n, [(j,) for j in range(1,n+1)])
def exact_sat(n,cs):
    return any(all(any(a[abs(l)-1] == (l>0) for l in c) for c in cs)
               for a in product((False, True), repeat=n))
def classify_marker(n,halt_at):
    src=U(n)
    assert src.startswith(f"p cnf {n} {n}\n")
    return "UNSAT" if halt_at is not None and n>=halt_at else "SAT"

clauses=((1,),(-1,),(2,),(-2,),(1,2),(1,-2),(-1,2),(-1,-2))
labels=[]
for mask in range(256):
    cs=[clauses[i] for i in range(8) if mask>>i&1]
    labels.append("SAT" if exact_sat(2,cs) else "UNSAT")
assert labels.count("SAT")==95 and labels.count("UNSAT")==161
checks=256
halt_times=[None,0,1,2,3,5,9,17,25]
for t in halt_times:
    for n in range(1,25):
        assert classify_marker(n,t)==("UNSAT" if t is not None and n>=t else "SAT")
        checks+=1
assert exact_sat(2,[(1,),(-2,)]) and not exact_sat(2,[(1,),(-1,)])
print(json.dumps({"test":"LSPV1_415_COMPACT","label_counts":{"SAT":95,"UNSAT":161},
                 "toy_runs":216,"checks":checks,"status":"COMPUTATIONAL finite only",
                 "P_vs_NP":"OPEN"}))
