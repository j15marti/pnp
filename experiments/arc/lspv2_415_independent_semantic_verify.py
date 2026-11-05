#!/usr/bin/env python3
"""Independent semantic falsifier, no imports from CANON1 checker or JS producer.
Run: python experiments/arc/lspv2_415_independent_semantic_verify.py
"""
import json
from pathlib import Path
p=Path("results/raw/arc/2026-11-05_0412_LSPV2_CANON1_DUPLICATE_DEF415_raw.json")
record=json.loads(p.read_text())
proof=record["witness"]
assert proof["source"]=={"nvars":1,"clauses":[[1]]}
assert [r["rule"] for r in proof["nodes"]]==["DEF","RES","RES","RES"]
def facet_table(t):
    a=[]
    for x in (0,1):
        for y in (0,1):
            wrong=1-t[x+2*y]
            a.append(sorted([1 if x==0 else -1, 1 if y==0 else -1, 2 if wrong==0 else -2],
                            key=lambda l:(abs(l),l<0)))
    return a
def satisfies(c,x,z):
    return any((x if abs(l)==1 else z)==int(l>0) for l in c)
t=proof["nodes"][0]["truth"]
assert t==[0,1,0,1]
facets=facet_table(t)
assert facets==record["def_facets"]
checks=0
for x in (0,1):
    for z in (0,1):
        truth=(z==t[x+2*x])
        assert all(satisfies(c,x,z) for c in facets)==truth
        checks+=1
assert satisfies(proof["source"]["clauses"][0],1,1)
assert all(satisfies(c,1,1) for c in facets)
assert not satisfies(proof["nodes"][1]["clause"],1,1)
checks+=3
for j in (1,2):
    assert -1 in facets[j] and 1 in facets[j]
    checks+=1
affected=[]
for m in range(16):
    tt=[(m>>i)&1 for i in range(4)]
    f=facet_table(tt)
    # Off-diagonal rows (0,1) and (1,0) become tautologies
    assert all((-1 in f[j] and 1 in f[j]) for j in (1,2))
    a=[l for l in f[1] if abs(l)==2]
    b=[l for l in f[2] if abs(l)==2]
    assert len(a)==len(b)==1
    if a[0]==-b[0]: affected.append(m)
    assert (tt[1]!=tt[2]) == (a[0]==-b[0])
    checks+=3
assert affected==record["truth_table_variants_with_attack"]
# A preserving repair keeps only consistent (x,x) rows and removes duplicates.
repaired=[[1,-2],[-1,2]]
for x in (0,1):
    for z in (0,1):
        assert all(satisfies(c,x,z) for c in repaired)==(x==z)
        checks+=1
print(json.dumps({"status":"PASS","independent_semantic_checks":checks,
                  "source_is_sat":True,"attack_variants":affected,
                  "repair_for_this_gate":repaired}))
