#!/usr/bin/env python3
"""Independent checker for REFEREE218; deliberately does not import producer."""
import json, sys
from collections import Counter

RAW=sys.argv[1] if len(sys.argv)>1 else "2026-10-30_0248_STRICT22-MINIMUM-REFEREE218_raw.json"
d=json.load(open(RAW,encoding="utf-8"))
cases={x["name"]:x for x in d["cases"]}

def lit(x,a): return ((a>>(abs(x)-1))&1)==(x>0)
def models(F):
 n=max(abs(x) for c in F for x in c)
 return [a for a in range(1<<n) if all(any(lit(x,a) for x in c) for c in F)]
def strict22(F):
 n=max(abs(x) for c in F for x in c); cnt=Counter()
 for c in F:
  assert len(c)==3 and len(set(map(abs,c)))==3
  for x in c:cnt[(abs(x),x>0)]+=1
 return all(cnt[(v,False)]==cnt[(v,True)]==2 for v in range(1,n+1))
def matrix(C,D):
 out={}
 for mode in ("SS","SU","US","UU"):
  req={};ok=True
  for clause,m in ((C,mode[0]),(D,mode[1])):
   for x in clause:
    val=int((x>0)==(m=="S"));v=abs(x)
    if v in req and req[v]!=val:ok=False
    req[v]=val
  out[mode]=ok
 return out

checks=0
for name in ("W1_strict22_UNSAT","SWAP6_strict22_SAT","STRICT8_SAT"):
 c=cases[name];F=[tuple(x) for x in c["source_clauses"]]
 assert strict22(F); checks+=1
 ms=models(F);assert len(ms)==c["exact_model_count"];checks+=1
 # Recompute all indexed pair matrices.
 got={(tuple(p["clause_indices"])):{m:z["feasible"] for m,z in p["modes"].items()}
      for p in c["pair_matrix"]}
 for j in range(len(F)):
  for k in range(j+1,len(F)):
   assert got[(j,k)]==matrix(F[j],F[k]);checks+=4

assert cases["W1_strict22_UNSAT"]["exact_model_count"]==0
assert cases["SWAP6_strict22_SAT"]["exact_model_count"]==54
assert len(cases["W1_strict22_UNSAT"]["source_clauses"])==20

# Replay each selector resolution step purely as set resolution.
for st in d["selector_resolution_proof"]["steps"]:
 p=st["pivot"];A=set(st["parents"][0]);B=set(st["parents"][1]);R=set(st["resolvent"])
 assert ((p in A and -p in B) or (-p in A and p in B));checks+=1
 assert R==(A|B)-{p,-p};checks+=1
 assert not any(-x in R for x in R);checks+=1
assert d["selector_resolution_proof"]["steps"][-1]["resolvent"]==[1]

# Every stored forbidden resolvent cube really falsifies both parents for both pivot values.
for name,c in cases.items():
 F=[tuple(x) for x in c["source_clauses"]]
 for r in c["resolvents"]:
  cube={int(v):bool(x) for v,x in r["forbidden_cube"].items()};p=r["pivot"]
  for pv in (False,True):
   a=dict(cube);a[p]=pv
   sat=[any(a[abs(x)]==(x>0) for x in F[j]) for j in r["parents"]]
   assert not all(sat)
  checks+=2

print(json.dumps({"status":"PASS","checks":checks,
 "independent_model_counts":{"W1":0,"SWAP6":54,"STRICT8":len(models([tuple(x) for x in cases['STRICT8_SAT']['source_clauses']]))},
 "scope":"finite source/witness/proof replay only; SAT-2024 lower bound is cited, not reproved"},sort_keys=True))
