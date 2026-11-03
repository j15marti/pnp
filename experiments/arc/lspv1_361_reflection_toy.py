#!/usr/bin/env python3
"""Finite signed CNF controls for LSPV-1 361. Deterministic, no outside imports.
Exhaustive 3-variable check is a diagnostic, not a P-time SAT solver.
"""
import hashlib
import json
from itertools import product

SOURCE = [(1,), (2,), (-1,3), (-2,-3)]
PROOF = [
    {"parents":[0,2],"pivot":1,"clause":[3]},
    {"parents":[1,3],"pivot":2,"clause":[-3]},
    {"parents":[4,5],"pivot":3,"clause":[]}
]

def sat_clause(c,a):
    return any(a[abs(x)] == (x>0) for x in c)

def models(cs):
    out=[]
    for bits in product([0,1], repeat=3):
        a={i+1:bool(bits[i]) for i in range(3)}
        if all(sat_clause(c,a) for c in cs): out.append(a)
    return out

def resolvent(a,b,p):
    a,b=set(a),set(b)
    if p in a and -p in b:
        out=(a-{p})|(b-{-p})
    elif -p in a and p in b:
        out=(a-{-p})|(b-{p})
    else: raise ValueError("not an opposite signed pivot")
    if any(-x in out for x in out): raise ValueError("tautology")
    return sorted(out,key=lambda x:(abs(x),x))

def replay(proof):
    rows=[list(c) for c in SOURCE]
    for step in proof:
        i,j=step["parents"]
        if i<0 or j<0 or i>=len(rows) or j>=len(rows):
            raise ValueError("bad parent index")
        c=resolvent(rows[i],rows[j],step["pivot"])
        if c!=sorted(step["clause"],key=lambda x:(abs(x),x)):
            raise ValueError("bad conclusion")
        rows.append(c)
    return rows[-1]==[]

def label(s):
    if len(s)!=2 or any(x not in "01" for x in s):
        return "MALFORMED"
    return "UNSAT" if s=="11" else "SAT"

assert replay(PROOF)
assert not models(SOURCE)
deletes=[]
flips=[]
for i,c in enumerate(SOURCE):
    w=models(SOURCE[:i]+SOURCE[i+1:])
    assert w
    deletes.append({"clause_index":i,"witness":{str(k):int(v) for k,v in w[0].items()}})
    for j,l in enumerate(c):
        changed=list(c)
        changed[j]=-l
        w=models(SOURCE[:i]+[tuple(changed)]+SOURCE[i+1:])
        assert w
        flips.append({"clause_index":i,"literal_index":j,
                      "witness":{str(k):int(v) for k,v in w[0].items()}})
labels=[]
for s in ["00","01","10","11","","1","12","a1","111"]:
    l=label(s)
    if l!="MALFORMED":
        f=([(3,)] if s[0]=="1" else [])+([(-3,)] if s[1]=="1" else [])
        assert ("SAT" if models(f) else "UNSAT")==l
    labels.append({"code":s,"label":l})

bad=[
    [{"parents":[0,3],"pivot":1,"clause":[3]},*PROOF[1:]],
    [*PROOF[:2],{"parents":[4,5],"pivot":2,"clause":[]}],
    [*PROOF[:2],{"parents":[4,5],"pivot":3,"clause":[3]}],
]
for trial in bad:
    try: replay(trial)
    except ValueError: continue
    raise AssertionError("corrupt proof accepted")

dimacs="p cnf 3 4\n"+"\n".join(" ".join(map(str,c))+" 0" for c in SOURCE)+"\n"
payload={
  "run":"LSPV1_ER2_UNIVERSAL_REFLECTION_COMPLETENESS361",
  "date":"2026-11-03 04:12 PST",
  "source":[list(x) for x in SOURCE],
  "source_dimacs":dimacs,
  "source_sha256":hashlib.sha256(dimacs.encode()).hexdigest(),
  "proof":PROOF,"paid_nodes":3,"source_count":4,
  "delete_witnesses":deletes,
  "flip_witnesses":flips,"input_labels":labels,
  "corrupt_proofs_rejected":3,
  "status":"COMPUTATIONAL: finite toy, not a B3 proof"
}
print(json.dumps(payload,sort_keys=True,indent=2))
