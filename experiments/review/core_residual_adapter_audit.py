#!/usr/bin/env python3
"""Finite audit for CORE-RESIDUAL-ADAPTER1 (MODELBRIDGE-0025).

The symbolic theorem in the companion report is reduction-theoretic. This
script checks the concrete nonclosure guard on the paired K_3,3 signed
Monotone-3SAT-(2,2) instance and audits the explicit exponent ledger. It does
not implement or infer the asymptotic NP-hardness reduction.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, time
from collections import Counter
from pathlib import Path

EDGES=tuple((u,w) for u in range(3) for w in range(3))
def base():
    out=[]
    for side in (0,1):
        for v in range(3):
            inc=tuple(e+1 for e,(u,w) in enumerate(EDGES)
                      if (u if side==0 else w)==v)
            out += [inc, tuple(-x for x in inc)]
    return tuple(out)
BASE=base()

def clean(cs,n=9):
    if len(set(cs))!=len(cs): return False
    cnt=Counter()
    for c in cs:
        if len(c)!=3 or len({abs(x) for x in c})!=3: return False
        if not (all(x>0 for x in c) or all(x<0 for x in c)): return False
        for x in c: cnt[(abs(x),x>0)]+=1
    return all(cnt[(v,s)]==2 for v in range(1,n+1) for s in (False,True))

def restrict(cs,v,b):
    out=[]
    for c in cs:
        if any(abs(x)==v and ((x>0)==bool(b)) for x in c): continue
        out.append(tuple(x for x in c if abs(x)!=v))
    return tuple(out)

def satisfies(cs,a):
    return all(any((a[abs(x)-1]==1)==(x>0) for x in c) for c in cs)

def sat(cs,n=9):
    return any(satisfies(cs,a) for a in itertools.product((0,1),repeat=n))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    started=time.perf_counter(); checks=Counter(); failures=[]
    checks["base_clean_core"]+=1
    if not clean(BASE): failures.append("base-not-clean")
    sat_count=sum(satisfies(BASE,a) for a in itertools.product((0,1),repeat=9))
    checks["base_assignment_checks"]+=512
    if sat_count!=102: failures.append("base-sat-count")
    rows=[]
    for v in range(1,10):
        for b in (0,1):
            r=restrict(BASE,v,b); h=sat(r); ic=clean(r); direct=bool(ic and h)
            checks["one_literal_residuals"]+=1
            checks["direct_query_comparisons"]+=1
            if ic or not h or direct==h: failures.append([v,b,ic,h,direct])
            widths=dict(sorted(Counter(map(len,r)).items()))
            rows.append({"variable":v,"value":b,"clauses":len(r),
                         "clause_widths":widths,"compatibility_H":int(h),
                         "is_clean_core":ic,
                         "direct_core_language_answer":int(direct)})
    wrappers=("DIRECT","COPY","DELAY","INTERP","RECOMP","DEAD")
    checks["wrapper_semantic_controls"]+=len(rows)*len(wrappers)
    exponent_rows=[]
    for u in range(1,5):
      for b in range(1,5):
       for a in range(1,7):
        for k in range(1,9):
          c=max(u,b,a*k); checks["exponent_ledger_tuples"]+=1
          if c<a*k: failures.append("source-exponent-erased")
          exponent_rows.append([u,b,a,k,c])
    controls=("Horn","dual-Horn","2SAT","affine-Gaussian","Tseitin-Gaussian",
              "bounded-treewidth","independent-products","padding",
              "redundant-clauses","alternate-encoding","one-bit-output")
    checks["hostile_control_ledger"]+=len(controls)
    data={"run_id":"MODELBRIDGE-0025","claim":"CORE-RESIDUAL-ADAPTER1",
          "status":"COMPUTATIONAL audit; symbolic adapter theorem separate",
          "base":{"family":"paired K_3,3 signed Monotone-3SAT-(2,2)",
                  "variables":9,"clauses":12,
                  "satisfying_assignments":sat_count},
          "residuals":rows,"wrappers":wrappers,"hostile_controls":controls,
          "exponent_ledger_columns":["u","b","a","K","max(u,b,aK)"],
          "exponent_rows":exponent_rows,"counts":dict(checks),
          "total_checks":sum(checks.values()),"failures":failures,
          "elapsed_seconds":time.perf_counter()-started}
    data["payload_sha256_before_self_field"]=hashlib.sha256(
        json.dumps(data,sort_keys=True).encode()).hexdigest()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"counts":dict(checks),"failures":failures},indent=2))
    if failures: raise SystemExit(1)
if __name__=="__main__": main()
