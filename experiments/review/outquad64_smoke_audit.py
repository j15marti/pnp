#!/usr/bin/env python3
"""Dependency-free finite audit of outquad64_solver.py; not a lower bound."""
from __future__ import annotations
import json,time,hashlib,argparse
from pathlib import Path
from collections import Counter
import outquad64_solver as s

def mul(a:int,b:int)->int:
    v=0
    while b:
        if b&1:v^=a
        b>>=1;a<<=1
        if a&256:a^=283
    return v

def central(x:int)->int:
    x2=mul(x,x);x4=mul(x2,x2);x8=mul(x4,x4)
    return mul(x,x2)^x8

def rotate(x:int,n:int)->int:return ((x<<n)|(x>>(8-n)))&255

def interpolate(fun)->dict:
    c=fun(0);ls=[fun(1<<i)^c for i in range(8)]
    qs=[fun((1<<i)|(1<<j))^c^ls[i]^ls[j] for i in range(8) for j in range(i+1,8)]
    return {'schema':'raw-quadratic-v1','dimension':8,'coefficients':[c]+ls+qs}

def main(output:Path)->None:
    begin=time.monotonic();tick=s.Budget(25);cnt=Counter();rows=[]
    def check(ok,tag):
        tick();cnt[tag]+=1
        if not ok:raise AssertionError(tag)
    functions=[('canonical',central),('affine_hidden',lambda x:rotate(central(rotate(x,3)^53),5)^145)]
    for name,fun in functions:
        m=s.prepare(interpolate(fun),tick);truth={}
        for x in range(256):
            check(m.evaluate(x)==fun(x),'raw_evaluation')
            truth.setdefault(fun(x),[]).append(x)
        hist=Counter();outcomes=Counter()
        for b in range(256):
            ans=s.solve(m,b,tick);expected=truth.get(b,[])
            check(ans['status']!='UNKNOWN','complete_promised_family')
            check(ans['witnesses']==expected,'complete_bruteforce_fiber')
            check(ans['candidates_examined']<=64,'candidate_bound')
            hist[str(ans['affine_dimension'])]+=1;outcomes[ans['status']]+=1
        rows.append({'name':name,'identities':len(m.identities),'candidate_dimension_histogram':dict(hist),'outcomes':dict(outcomes)})
    m=s.prepare(interpolate(central),tick)
    check(s.solve(m,0)['witnesses']==[0,1,12,80,176,237],'six_roots_at_zero')
    m=s.prepare(interpolate(lambda x:0),tick)
    check(s.solve(m,0)['status']=='UNKNOWN','constant_map_unknown')
    check(s.solve(m,1)['status']=='UNSAT','constant_map_unsat')
    result={'run_id':'OUTQUAD64','batch':'standalone_smoke','status':'COMPUTATIONAL','seed':None,
            'assertions':sum(cnt.values()),'checks_by_group':dict(cnt),'failures':0,'rows':rows,
            'elapsed_seconds':time.monotonic()-begin,'solver_sha256':hashlib.sha256(Path(s.__file__).read_bytes()).hexdigest(),
            'audit_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('outquad64_smoke_results.json'))
    main(p.parse_args().output)
