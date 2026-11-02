#!/usr/bin/env python3
"""No-producer-import verifier for REFEREE287."""
import argparse,itertools,json
from pathlib import Path
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Z=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6))
def sh(F,k):return tuple(tuple((1 if x>0 else -1)*(abs(x)+k) for x in c) for c in F)
F=F9+sh(Z,9)
def sat(C,a):return all(any(a[abs(x)]==(x>0) for x in c) for c in C)
def audit(p):
    free=[v for v in range(1,16) if v not in p and v!=10];q=[0,0,0,0,0]
    for z in range(1<<len(free)):
        a=dict(p);a.update((v,(z>>i)&1) for i,v in enumerate(free));a[10]=0;f0=sat(F,a);a[10]=1;f1=sat(F,a)
        q[0]+=f0;q[1]+=f1;q[2]+=f0 and f1;q[3]+=f0 and not f1;q[4]+=f1 and not f0
    return q
def main():
    p=argparse.ArgumentParser();p.add_argument("--raw",required=True);p.add_argument("--out",required=True);a=p.parse_args();r=json.loads(Path(a.raw).read_text());checks=0
    root=audit({});sp=audit({1:0,4:0,5:1,8:0});up=audit({1:1,4:0,5:1,8:0})
    assert root==[630,630,280,350,350];assert sp==[63,63,28,35,35];assert up==[0,0,0,0,0];checks+=15
    assert root==[r["F9_Z6"]["root"][k] for k in ("cofactor0_models","cofactor1_models","shared_models","only0","only1")]
    # Separate product truth check on all complete rows.
    models=0
    for z in range(1<<15):
        x={v:(z>>(v-1))&1 for v in range(1,16)}
        left=sat(F9,x);right=sat(sh(Z,9),x);assert sat(F,x)==(left and right);models+=left and right;checks+=1
    assert models==1260
    # Z cofactor table independently: 9/9, common4, five each direction.
    zq=[0,0,0,0,0]
    for bits in range(32):
        x={v+2:(bits>>v)&1 for v in range(5)};x[1]=0;u=sat(Z,x);x[1]=1;v=sat(Z,x)
        zq[0]+=u;zq[1]+=v;zq[2]+=u and v;zq[3]+=u and not v;zq[4]+=v and not u;checks+=1
    assert zq==[9,9,4,5,5]
    out={"run":"VERIFY-COFACTOR-EQUALITY-DUALITY-REFEREE287","producer_imported":False,"independent":True,
         "assertion_groups":checks,"root":root,"SAT_pins":sp,"UNSAT_pins":up,"product_models":models,"Z6_pair":zq,"ok":True}
    Path(a.out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps(out,sort_keys=True))
if __name__=="__main__":main()
