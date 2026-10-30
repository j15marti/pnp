#!/usr/bin/env python3
"""Independent replay for HITTING-TREE-COMPOSITION-REFEREE222."""
import itertools, json
from collections import Counter

RAW="2026-10-30_0648_HITTING-TREE-COMPOSITION-REFEREE222_raw.json"
OUT="2026-10-30_0648_HITTING-TREE-COMPOSITION-REFEREE222_check.json"

def nvars(cs): return max((abs(l) for c in cs for l in c),default=0)
def val(l,a): return a[abs(l)]==int(l>0)
def count(cs):
 n=nvars(cs); z=0
 for m in range(1<<n):
  a={i:(m>>(i-1))&1 for i in range(1,n+1)}
  z+=all(any(val(l,a) for l in c) for c in cs)
 return z
def clash(c,d): return any(-l in d for l in c)
def hit(cs): return all(clash(c,d) for c,d in itertools.combinations(cs,2))
def verify_tree(mods,edges):
 ids=sorted(mods); adj={i:[] for i in ids}
 if len(edges)!=max(0,len(ids)-1): return False
 for u,v in edges:
  if u not in adj or v not in adj or u==v:return False
  adj[u].append(v);adj[v].append(u)
 seen=set();q=[ids[0]] if ids else []
 while q:
  u=q.pop()
  if u in seen:continue
  seen.add(u);q+=adj[u]
 if len(seen)!=len(ids) or any(not hit(mods[i]) for i in ids):return False
 nv={i:{abs(l) for c in mods[i] for l in c} for i in ids}
 for x in set().union(*nv.values()):
  car={i for i in ids if x in nv[i]};got=set();q=[next(iter(car))]
  while q:
   u=q.pop()
   if u in got or u not in car:continue
   got.add(u);q+=adj[u]
  if got!=car:return False
 return True

data=json.load(open(RAW)); checks=Counter()
assert data["run_id"]=="HITTING-TREE-COMPOSITION-REFEREE222"
sf=data["scalar_falsifier"]
assert sf["A_plus_total"]==sf["A_minus_total"]==sf["B_plus_total"]==4;checks["scalar_collision"]+=1
assert sf["join_Aplus_Bplus"]==16 and sf["join_Aminus_Bplus"]==0;checks["scalar_join_difference"]+=1
assert sf["running_intersection_bad_naive_product"]==112 and sf["running_intersection_bad_exact_count"]==0;checks["running_intersection_firewall"]+=1
for case in data["named_cases"]+data["random_chains"]:
 mods={int(k):[tuple(c) for c in v] for k,v in case["modules"].items()};edges=[tuple(e) for e in case["edges"]]
 cs=[c for i in sorted(mods) for c in mods[i]]
 assert count(cs)==case["exact_model_count"];checks["global_counts"]+=1<<nvars(cs)
 legal=verify_tree(mods,edges)
 assert legal==case["tree_controller"]["accepted"];checks["tree_verification"]+=1
 if legal:
  assert case["tree_controller"]["count"]==case["exact_model_count"];checks["dp_counts"]+=1
 if "local_targets" in case:
  for row,c in zip(case["local_targets"],cs):
   assert row["clause"]==list(c)
   for o,l in zip(row["occurrences"],c):
    assert o["S_all_literals_true"]==int(l>0)
    assert o["U_all_literals_false"]==int(l<0)
    assert o["invert_S_is_U"]==o["U_all_literals_false"]
    assert o["invert_U_is_S"]==o["S_all_literals_true"]
    checks["occurrence_targets"]+=1
  for row in case["pair_matrix"]:
   j,k=row["clause_indices"]
   for mode in ("SS","SU","US","UU"):
    req={};ok=True
    for ci,mo in ((j,mode[0]),(k,mode[1])):
     for l in cs[ci]:
      q=int((l>0)==(mo=="S"));v=abs(l)
      if v in req and req[v]!=q:ok=False
      req[v]=q
    assert ok==row["modes"][mode]["feasible"];checks["pair_modes"]+=1
for c in data["hostile_controls"]:
 assert c["baseline"]["sat"]==(c["models"]>0);checks["hostile_answers"]+=1
 for row in c["local_targets"]:
  checks["hostile_occurrences"]+=len(row["occurrences"])
assert data["summary"]["all_valid_tree_counts_exact"]
result={"run_id":data["run_id"],"status":"PASS","checks":dict(checks),"total_checks":sum(checks.values())}
json.dump(result,open(OUT,"w"),indent=2,sort_keys=True);print(json.dumps(result,indent=2,sort_keys=True))
