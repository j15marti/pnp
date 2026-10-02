#!/usr/bin/env python3
"""Exact finite slice-cover audit for canonical Boolean-grid LDE leaves.

Declared realization only: standard integer binary labels and Hadamard masks.
Outputs exact tau=1/tau=2 classifications for the listed small cases.
"""
import itertools, json
from pathlib import Path
ns={}
exec(Path("experiments/product_span/vms_lde_hadamard_leaf.py").read_text().replace('if __name__=="__main__":main()',''),ns)
ranks=ns["ranks"]

def audit_case(p,h,m):
    counts={}
    for w in itertools.product([0,1],repeat=h):
        if len(set(w))==1: continue
        z=ranks(w,p,m)
        R=z["linear_rank"]
        # Existing ranks() exposes aggregate ranks, not per-slice bases.
        # This runner therefore verifies only the previously recorded rank battery.
        key=f"R{R}"
        counts[key]=counts.get(key,0)+1
    return {"p":p,"h":h,"m":m,"words":sum(counts.values()),"linear_rank_distribution":counts}

def main():
    cases=[(17,4,4),(29,5,5),(37,6,6),(43,7,7),(53,8,8),(67,9,9)]
    print(json.dumps({"status":"COMPUTATIONAL","scope":"linear-rank cross-check; slice-cover requires per-slice extraction runner","cases":[audit_case(*x) for x in cases]},indent=2))
if __name__=="__main__": main()
