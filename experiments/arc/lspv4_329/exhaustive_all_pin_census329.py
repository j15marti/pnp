#!/usr/bin/env python3
"""Exhaustive coherent-pin same-original cross-check for paired K4/K33.
Independent source truth: explicit model enumeration, no SAT oracle.
Matching side: paid graph compilation and NetworkX, not native FLMV.
Run: python experiments/arc/lspv4_329/exhaustive_all_pin_census329.py
"""
import json
from collections import Counter
from itertools import product
from paired_tutte329 import SOURCES, valid, source_models, decide

def census(name,pos):
    assert valid(pos)
    n=max(map(max,pos))
    models=source_models(pos)
    totals=Counter()
    by_first={}
    for first in (-1,0,1):
        cnt=Counter()
        for rest in product((-1,0,1),repeat=n-1):
            raw=(first,)+rest
            p={i+1:x for i,x in enumerate(raw) if x!=-1}
            truth=any(all(a[i-1]==v for i,v in p.items()) for a in models)
            result=decide(pos,p,certify=False)
            assert truth==result["sat"],(name,p,truth,result)
            key=("SAT" if result["sat"] else
                 "UNSAT_LOCAL" if result.get("local_source_conflict") else
                 "UNSAT_NO_PARITY_H" if not result["cases"] else
                 "UNSAT_TUTTE_REQUIRED")
            cnt[key]+=1
        totals.update(cnt)
        by_first[str(first)]=dict(sorted(cnt.items()))
    assert sum(totals.values())==3**n
    return {"n":n,"models":len(models),"all_coherent_pins":3**n,
            "categories":dict(sorted(totals.items())),"by_first":by_first}

def main():
    out={name:census(name,pos) for name,pos in SOURCES.items()}
    assert out["K4"]["categories"]=={
       "SAT":475,"UNSAT_LOCAL":186,"UNSAT_NO_PARITY_H":24,
       "UNSAT_TUTTE_REQUIRED":44}
    assert out["K33"]["categories"]=={
       "SAT":12001,"UNSAT_LOCAL":6926,"UNSAT_NO_PARITY_H":36,
       "UNSAT_TUTTE_REQUIRED":720}
    out["note"]="All labels checked against brute original-source completions; host matching only, no FLMV"
    out["proof_status"]="COMPUTATIONAL exact finite census, restricted theorem separate; P versus NP OPEN"
    print(json.dumps(out,sort_keys=True,indent=2))

if __name__=="__main__":main()
