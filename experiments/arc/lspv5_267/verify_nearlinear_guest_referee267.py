#!/usr/bin/env python3
"""Independent, no-producer-import verifier for referee267."""
import argparse,json,hashlib
from itertools import product
from pathlib import Path

F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),
    (-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
PS={1:0,2:0,8:1,9:1};PU={3:0,6:1,7:1,9:1}

def sat(F,a):return all(any(a[abs(x)]==int(x>0) for x in c) for c in F)
def count(F,n,p):
    free=[v for v in range(1,n+1) if v not in p];z=0
    for b in product((0,1),repeat=len(free)):z+=sat(F,{**p,**dict(zip(free,b))})
    return z
def res(F,p):return [tuple(x for x in c if abs(x) not in p) for c in F if not any(abs(x) in p and p[abs(x)]==int(x>0) for x in c)]
def bits(F,n):
    w=max(1,n.bit_length());h=max(8,max(n,len(F)).bit_length())
    return 2*h+sum(2+len(c)*(1+w) for c in F)
def chain(t):
    F=[tuple((1 if x>0 else -1)*(abs(x)+9*b) for x in c) for b in range(t) for c in F9]
    for b in range(t-1):
        i=12*b;j=i+12;A=list(F[i]);B=list(F[j]);A[0],B[0]=B[0],A[0];F[i]=tuple(A);F[j]=tuple(B)
    return F
def valid(F,n):
    d={(v,s):0 for v in range(1,n+1) for s in (0,1)};seen=set()
    if len(F)*3!=4*n:return False
    for c in F:
        if len(c)!=3 or len(set(map(abs,c)))!=3 or not(all(x>0 for x in c) or all(x<0 for x in c)):return False
        k=tuple(sorted(c))
        if k in seen:return False
        seen.add(k)
        for x in c:d[abs(x),int(x>0)]+=1
    return all(x==2 for x in d.values())

def main():
    ap=argparse.ArgumentParser();ap.add_argument('raw');ap.add_argument('--output',required=True);a=ap.parse_args()
    raw=Path(a.raw);R=json.loads(raw.read_text());checks=0
    def ck(x,m):
        nonlocal checks
        assert x,m;checks+=1
    ck(R['P_versus_NP']=='OPEN','open');ck((count(F9,9,{}),count(F9,9,PS),count(F9,9,PU))==(70,2,0),'F9 labels')
    ck((count(Y6,6,{}),count(Y6,6,{5:0,6:1}),count(Y6,6,{3:1,4:0,5:0,6:1}))==(20,6,0),'Y6 labels')
    rs,ru=res(F9,PS),res(F9,PU);ck((bits(F9,9),bits(rs,9),bits(ru,9))==(220,88,78),'encoding')
    for row in R['sources']['F9']['UNSAT_proof']:
        aa={**PU,**dict(zip((1,2,4,5,8),row['free_bits']))};j=row['first_falsified_original_clause']
        ck(not any(aa[abs(x)]==int(x>0) for x in F9[j]),'UNSAT row')
    for row in R['connected_family']:
        t=row['t'];F=chain(t);n=9*t;ck(valid(F,n),'family grammar')
        p={v+9*b:x for b in range(t) for v,x in PS.items()};ck((bits(F,n),bits(res(F,p),n))==(row['source_bits'],row['residual_bits']),'family lengths')
    for side,M in [('F9_SAT',88),('F9_UNSAT',78)]:
        for z in R['charged_protocols'][side]:
            q=z['q'];Q=M**q;ck(z['DELAY_native_steps_lower_bound']==Q,'delay')
            ck(z['RECOMP_full_parent_reads']==220*Q,'recomp');ck(z['COPY_child_writes']==M,'copy')
            ck(z['logical_residual_endpoint_xor']==0,'xor')
    ck(R['lemma']['gap'].startswith('This rejects one monolithic'),'scope')
    out={"run":"VERIFY_NEARLINEAR_GUEST_REENTRY_REFEREE267","status":"PASS",
         "independent_checks":checks,"raw_sha256":hashlib.sha256(raw.read_bytes()).hexdigest(),
         "same_source_labels":{"F9":"70/2/0","Y6":"20/6/0"},"P_vs_NP":"OPEN"}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps(out,indent=2))
if __name__=='__main__':main()
