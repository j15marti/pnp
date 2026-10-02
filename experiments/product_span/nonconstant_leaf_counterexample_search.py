#!/usr/bin/env python3
"""Adversarial symbolic checks for the nonconstant-LDE exterior-rank conjecture.

Searches all Boolean grid words for small h and several primes/output widths.
COMPUTATIONAL only; declared standard binary-label/Hadamard realization.
"""
import json,itertools,math
from pathlib import Path
exec(Path("experiments/product_span/vms_lde_hadamard_leaf.py").read_text().replace("if __name__==\"__main__\":main()",""))
def run():
 out=[]
 for h in range(2,8):
  primes=[p for p in [11,13,17,19,23,29,31,37,41,43,47,53] if p>h]
  for p in primes:
   for m in range(2,min(h+2,8)):
    bad=[]; total=0
    for w in itertools.product([0,1],repeat=h):
     if len(set(w))==1: continue
     total+=1; z=ranks(w,p,m)
     if z["exterior_rank"]<z["exterior_max"]:
      bad.append({"word":"".join(map(str,w)),**z})
      if len(bad)>=5: break
    out.append({"h":h,"p":p,"m":m,"nonconstant_checked":total,"bad":bad})
 print(json.dumps({"status":"COMPUTATIONAL","mode":"exhaustive per listed h,p,m until five counterexamples","cases":out,
 "counterexample_cases":sum(bool(x["bad"]) for x in out),
 "limitations":["standard integer-bit label/Hadamard only","small parameters","not vMS asymptotic regime"]},indent=2))
if __name__=="__main__":run()
