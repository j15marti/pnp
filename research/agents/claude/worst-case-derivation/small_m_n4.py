#!/usr/bin/env python3
"""All MU formulas on exactly-or-fewer 4 variables with at most M clauses; exact min DAG-resolution
cost per symmetry class.  Usage: small_m_n4.py M"""
import sys, json, time
from wbar_exact import clauses, falsified, perms_signs, canon, min_refutation
n=4; M=int(sys.argv[1]); t=time.time()
cl=[c for c in clauses(n) if c!=(0,0)]; cov=[falsified(c,n) for c in cl]; full=(1<<(1<<n))-1
found=set()
def dfs(ch,covd):
    if covd==full:
        for j in ch:
            o=0
            for k in ch:
                if k!=j: o|=cov[k]
            if o==full: return
        found.add(tuple(sorted(ch))); return
    if len(ch)==M: return
    low=(~covd)&(covd+1)
    for i,cv in enumerate(cov):
        if cv&low and i not in ch: dfs(ch+[i],covd|cv)
dfs([],0)
G=perms_signs(n); cls={}
for f in found:
    k=canon([cl[i] for i in f],G); cls[k]=cls.get(k,0)+1
rows=[]
for r in sorted(cls):
    w,pf=min_refutation(list(r)); rows.append({"F":[list(c) for c in r],"m":len(r),"orbit":cls[r],"W":w,"proof":pf})
out={"n":n,"M":M,"chunk":[0,1],"num_MU":len(found),"num_classes":len(cls),"rows":rows,"secs":round(time.time()-t,2)}
json.dump(out,open(f"wbar_n4_mle{M}.json","w"))
from collections import Counter
print("MU",len(found),"classes",len(cls),Counter((x["m"],x["W"]) for x in rows),out["secs"])
