#!/usr/bin/env python3
"""Independent, no-producer-import verification for REFEREE286."""
import argparse, collections, itertools, json
from pathlib import Path

F=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
   (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))

def ok(a):return all(any(a[abs(x)]==(x>0) for x in c) for c in F)
def ass(z):return {i:(z>>(i-1))&1 for i in range(1,10)}

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--raw",required=True);ap.add_argument("--out",required=True);a=ap.parse_args()
    raw=json.loads(Path(a.raw).read_text());checks=0;boundary=[0]*9;models=0;minimum=9
    for z in range(512):
        x=ass(z)
        if not ok(x):continue
        models+=1;marked=set();n1=n3=0
        for c in F:
            t=[abs(q) for q in c if x[abs(q)]==(q>0)]
            if len(t)==1:marked.add(t[0]);n1+=1
            if len(t)==3:n3+=1
        direct=set()
        for v in range(1,10):
            y=dict(x);y[v]^=1
            if not ok(y):direct.add(v)
        assert marked==direct and n1-n3==6 and len(marked)>=3;checks+=12
        minimum=min(minimum,len(marked))
        for v in marked:boundary[v-1]+=1
    miter=[0]*9
    for v in range(1,10):
        rest=[q for q in range(1,10) if q!=v]
        for z in range(256):
            x={q:(z>>i)&1 for i,q in enumerate(rest)};x[v]=0;p=ok(x);x[v]=1;q=ok(x)
            if p!=q:miter[v-1]+=1
            checks+=1
    assert (models,boundary,minimum)==(raw["roots"]["F9"]["models"],raw["roots"]["F9"]["per_variable"],raw["roots"]["F9"]["minimum_witness_pivots"])
    assert miter==boundary and sum(boundary)==raw["roots"]["F9"]["boundary"]
    classes=collections.Counter();rows=0
    for vals in itertools.product((None,0,1),repeat=9):
        pin={i+1:v for i,v in enumerate(vals) if v is not None};free=[i for i in range(1,10) if i not in pin];tab=[]
        for z in range(1<<len(free)):
            x=dict(pin);x.update((v,(z>>i)&1) for i,v in enumerate(free));tab.append(ok(x));rows+=1
        bd=0
        for i in range(len(free)):
            bd+=sum(tab[z]!=tab[z|1<<i] for z in range(1<<len(free)) if not(z>>i&1))
        if not any(tab):classes["UNSAT_ZERO_BOUNDARY"]+=1;assert bd==0
        elif all(tab):classes["SAT_ZERO_BOUNDARY_CONSTANT_TRUE"]+=1;assert bd==0
        else:classes["SAT_POSITIVE_BOUNDARY"]+=1;assert bd>0
        checks+=1
    assert rows==4**9 and dict(classes)==raw["F9"]["pin_census"]["classes"]
    out={"run":"VERIFY-BOUNDARY-CERTIFICATE-EQUIVALENCE-REFEREE286","independent":True,"producer_imported":False,
         "assertion_groups":checks,"F9_models":models,"F9_boundary":sum(boundary),"per_variable":boundary,
         "pin_states":3**9,"completion_rows":rows,"classes":dict(classes),"ok":True}
    Path(a.out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps(out,sort_keys=True))
if __name__=="__main__":main()
