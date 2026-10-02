#!/usr/bin/env python3
# Sweep p/h and m for Boolean LDE leaves under declared integer-label/Hadamard realization.
import json,itertools,math
from pathlib import Path
ns={}
exec(Path("experiments/product_span/vms_lde_hadamard_leaf.py").read_text().replace('if __name__=="__main__":main()',''),ns)
ranks=ns["ranks"]
PR=[11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,127,131,149,151,181,191,211,251,257,509,521,1021]
rows=[]; first_bad=[]
for h in range(2,8):
 for m in range(2,min(8,h+3)):
  for p in [q for q in PR if q>h]:
   bad=0; total=0; minext=10**9
   for w in itertools.product([0,1],repeat=h):
    if len(set(w))==1: continue
    total+=1; z=ranks(w,p,m); minext=min(minext,z["exterior_rank"])
    if z["exterior_rank"]<z["exterior_max"]:
     bad+=1
     if len(first_bad)<30:first_bad.append({"h":h,"m":m,"p":p,"word":"".join(map(str,w)),"rank":z["exterior_rank"],"max":z["exterior_max"]})
   rows.append({"h":h,"m":m,"p":p,"ratio":p/h,"total":total,"bad":bad,"minext":minext,"maxext":m*(m-1)//2})
print(json.dumps({"status":"COMPUTATIONAL","rows":rows,"first_bad":first_bad},separators=(",",":")))
