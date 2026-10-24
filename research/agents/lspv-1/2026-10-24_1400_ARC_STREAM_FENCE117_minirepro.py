#!/usr/bin/env python3
"""ARC-STREAM-FENCE117 compact independent audit.
Standard library only. Run: python 2026-10-24_1400_ARC_STREAM_FENCE117_minirepro.py
Computational controls verify finite examples and rational arithmetic only.
No SAT lower-bound claim is made from experiment counts.
"""
import itertools
import json
import random
from fractions import Fraction as Q
from pathlib import Path

SEED=202610240600
RNG=random.Random(SEED)
checks=0

def ok(condition):
    global checks
    checks+=1
    if not condition: raise AssertionError("audit check %s" % checks)

def beta(c):
    return ((c+2)/(c*c)-c)/2

def direct_sat(clauses):
    n=max((abs(x) for c in clauses for x in c),default=0)
    for a in range(1<<n):
        if all(any(bool((a>>(abs(x)-1))&1)==(x>0) for x in c) for c in clauses):
            return True
    return False

def events(clauses):
    last={}
    for i,c in enumerate(clauses):
        for x in c:last[abs(x)]=i
    live=set();ev=[]
    for i,c in enumerate(clauses):
        for x in sorted({abs(z) for z in c}):
            if x not in live:live.add(x);ev.append(("I",x))
        ev.append(("C",tuple(c)))
        for x in sorted({abs(z) for z in c}):
            if last[x]==i:live.remove(x);ev.append(("D",x))
    ok(not live)
    ev.append(("END",))
    return ev

def frontier_and_dp(clauses,table=True):
    ev=events(clauses);live=[];rows={0};w=0;peak=1
    for e in ev:
        op=e[0]
        if op=="I":
            ok(e[1] not in live)
            if table:rows|={v|(1<<len(live)) for v in rows}
            live.append(e[1]);w=max(w,len(live))
        elif op=="C":
            ok(all(abs(x) in live for x in e[1]))
            if table:
                mp={v:i for i,v in enumerate(live)}
                rows={v for v in rows if any(bool((v>>mp[abs(x)])&1)==(x>0) for x in e[1])}
        elif op=="D":
            i=live.index(e[1]);live.pop(i)
            if table:
                low=(1<<i)-1
                rows={(v&low)|((v>>(i+1))<<i) for v in rows}
        else:ok(op=="END")
        if table:peak=max(peak,len(rows))
    ok(not live)
    return (w, bool(rows) if table else None, peak if table else None)

def pure_reduce(clauses):
    src=list(clauses);passes=0
    while True:
        sign={}
        for c in src:
            for x in c:
                v=sign.setdefault(abs(x),set());v.add(x>0)
        pure={k if True in v else -k for k,v in sign.items() if len(v)==1}
        if not pure:break
        reduced=[c for c in src if not any(x in pure for x in c)]
        if len(reduced)==len(src):break
        src=reduced;passes+=1
    return src,passes

def clique_source(h,unsat):
    cs=[];z=h+5
    for i in range(1,h+1):
        for j in range(i+1,h+1):
            cs.append((i,j,z));z+=1
    a,b,c,d=h+1,h+2,h+3,h+4
    for signs in itertools.product((-1,1),repeat=3):
        if not unsat and signs==(-1,-1,-1):continue
        cs.append((a*signs[0],b*signs[1],c*signs[2]))
    if not unsat:cs.append((a,b,d))
    cs.append((1,a,d))
    return cs

c=Q(241,200)
ok(beta(c)==Q(11642479,23232400))
tests=[
 (Q(1),Q(0),Q(11,10),Q(1,2),c,True),
 (Q(23,20),Q(1,40),Q(11,10),Q(1,2),c,True),
 (Q(6,5),Q(1,100),Q(11,10),Q(1,2),c,False),
 (Q(1),Q(1,10),Q(11,10),Q(1,5),c,True),
 (Q(11,10),Q(3,20),Q(11,10),Q(3,20),Q(13,10),True),
 (Q(1),Q(1,2),Q(11,10),Q(1,10),c,False),
]
out=[]
for mu,k,r,s,cc,expected in tests:
    t=max(r,mu+k);p=max(s,k)
    actual=(cc>max(Q(1),t) and p<beta(cc))
    ok(actual==expected)
    out.append({"mu":str(mu),"kappa":str(k),"r":str(r),"sigma":str(s),
                "t":str(t),"s":str(p),"c":str(cc),"beta":str(beta(cc)),
                "excluded_by_FLVMonly_if_normalizer_exists":actual})

controls=[]
for h in (3,4,5,8,12,16,32,64):
    for unsat in (False,True):
        cnf=clique_source(h,unsat)
        raw_w,_,_=frontier_and_dp(cnf,False)
        reduced,rounds=pure_reduce(cnf)
        small_w,decision,peak=frontier_and_dp(reduced,True)
        ok(len(reduced)==(8 if unsat else 7))
        ok(raw_w>=h-1)
        ok(small_w==3)
        ok(decision==(not unsat))
        ok(direct_sat(reduced)==(not unsat))
        controls.append({"h":h,"label":"UNSAT" if unsat else "SAT",
              "raw_clause_count":len(cnf),"raw_width":raw_w,
              "residual_clauses":len(reduced),"residual_width":small_w,
              "residual_peak_DP_rows":peak,"pure_rounds":rounds})
for i in range(250):
    n=RNG.randrange(3,8);m=RNG.randrange(1,10)
    f=[]
    for _ in range(m):
        variables=RNG.sample(range(1,n+1),3)
        f.append(tuple(v if RNG.randrange(2) else -v for v in variables))
    _,v,_=frontier_and_dp(f,True)
    ok(v==direct_sat(f))

result={"id":"ARC-STREAM-FENCE117-mini","seed":SEED,"check_count":checks,
  "random_3CNF_controls":250,"clique_controls":len(controls),
  "clique_rows":controls,"FLMV_fractional_checks":out,
  "status":"finite computation only; normalizer impossibility follows from separately stated lemma and published FLMV theorem"}
name=Path(__file__).with_suffix(".json")
name.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"checks":checks,"clique_controls":len(controls),
                  "random_controls":250,"output_json":name.name},indent=2))
