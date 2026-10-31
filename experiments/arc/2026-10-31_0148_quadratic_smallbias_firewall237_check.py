#!/usr/bin/env python3
"""Independent checker for FIREWALL237 raw output; imports no producer code."""
import json
from pathlib import Path

P=Path("results/raw/arc/2026-10-31_0148_LSPV5_QUADRATIC_SMALLBIAS_FIREWALL237_raw.json")
d=json.loads(P.read_text())
checks=0
def ck(x):
    global checks
    checks+=1
    assert x

for row in d["exhaustive_bent_rows"]:
    r=row["r"]; z=(1<<(2*r-1))+(1<<(r-1)); o=(1<<(2*r-1))-(1<<(r-1))
    ck(row["zero_set_size"]==z); ck(row["one_set_size"]==o)
    ck(row["max_nonzero_linear_bias_numerator"]==(1<<(r-1)))
    ck(abs(row["max_nonzero_linear_bias"]-1/((1<<r)+1))<1e-15)
    ck(abs(row["quadratic_gap"]-(1-2**(-r))/2)<1e-15)
for row in d["symbolic_exact_rows"]:
    r=row["r"]
    ck(row["epsilon_denominator"]==(1<<r)+1)
    ck(row["quadratic_gap_numerator"]==(1<<r)-1)
for src in d["same_source_sat_unsat_controls"]:
    models=[]
    for mask in range(8):
        good=True
        for c in src["clauses"]:
            if not any((((mask>>(abs(l)-1))&1)==1) if l>0 else (((mask>>(abs(l)-1))&1)==0) for l in c):
                good=False; break
        if good: models.append(tuple((mask>>i)&1 for i in range(3)))
    ck(len(models)==src["model_count"])
    ck(src["dpll"]["sat"]==bool(models))
    for p in src["pair_modes"]:
        ck(p["predicted"]==p["actual"])
    for e in src["endpoints_and_flips"]:
        ck(all(y==3-x for x,y in zip(e["truth_counts"],e["complement_truth_counts"])))
ck(d["same_source_sat_unsat_controls"][0]["model_count"]==1)
ck(d["same_source_sat_unsat_controls"][1]["model_count"]==0)
ck(d["status"]["p_vs_np"]=="OPEN")
print(json.dumps({"status":"PASS","independent_checks":checks,"raw":str(P)},indent=2))
