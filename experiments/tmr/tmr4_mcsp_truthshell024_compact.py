#!/usr/bin/env python3
"""Native CPython verifier for TMR4/024. Run: python tmr4_mcsp_truthshell024_compact.py.
All gates are fan-in-two OR/AND or unary NOT. This is a finite validator,
not a TM compiler or proof of asymptotic hardness.
"""
import hashlib, itertools, json, math, random
from pathlib import Path

seed=20261114
rng=random.Random(seed)

def C(s, vars=(1,2,3)):
    return tuple(-v if (s>>i)&1 else v for i,v in enumerate(vars))

def direct(F,a):
    return all(any(bool((a>>(abs(z)-1))&1)==(z>0) for z in cl) for cl in F)

def compile_(n,F):
    u=sorted(set(tuple(sorted(cl,key=abs)) for cl in F))
    assert all(len(cl)==3 and len({abs(z) for z in cl})==3 for cl in u)
    gates=[]
    def add(op,x,y=0):
        gates.append((op,x,y)); return n+len(gates)-1
    neg=[add('NOT',i) for i in range(n)]
    if not u: return gates,add('OR',0,neg[0]),0
    cs=[]
    for cl in u:
        wires=[z-1 if z>0 else neg[-z-1] for z in cl]
        cs.append(add('OR',add('OR',wires[0],wires[1]),wires[2]))
    out=cs[0]
    for v in cs[1:]:out=add('AND',out,v)
    assert len(gates)==n+3*len(u)-1
    return gates,out,len(u)

def evaluate(n,gates,out,a):
    wire=[(a>>i)&1 for i in range(n)]
    for op,x,y in gates:
        wire.append(1-wire[x] if op=='NOT' else (wire[x]|wire[y] if op=='OR' else wire[x]&wire[y]))
    return bool(wire[out])

def trial(n,F):
    gates,out,d=compile_(n,F)
    mask=0
    for a in range(1<<n):
        v=direct(F,a)
        assert evaluate(n,gates,out,a)==v
        mask|=int(v)<<a
    b=n.bit_length()
    L=24+3*len(F)*(b+1)
    return dict(n=n,m=len(F),d=d,gates=len(gates),L=L,N=1<<n,
                sat=bool(mask),models=mask.bit_count(),truth=hex(mask))

def pair(n,r):
    extra=tuple((i,1,2) for i in range(4,n+1))
    return (tuple(C(s) for s in range(8) for _ in range(r))+extra,
            tuple(C(0) for _ in range(8*r))+extra)

def main():
    distinct=set(); checked=0; named=[]; formula_count=0
    for mask in range(256):
        F=tuple(C(s) for s in range(8) if (mask>>s)&1)
        t=trial(3,F); formula_count+=1; checked+=t['N']
        assert t['models']==8-mask.bit_count()
        distinct.add(t['truth'])
    assert len(distinct)==256
    for n in range(3,10):
        for r in (1,2,7,50):
            x,y=pair(n,r)
            a,b=trial(n,x),trial(n,y)
            assert not a['sat'] and b['sat'] and a['L']==b['L']
            checked+=a['N']+b['N']; formula_count+=2
            if (n,r) in ((3,50),(8,50)):
                named.extend([dict(label='UNSAT',**a),dict(label='SAT',**b)])
    extras=[(3,(C(0),C(3),C(5),C(6))),
            (3,((1,2,3),(1,2,-3))),
            (3,((1,-2,-3),(-1,2,-3),(-1,-2,3),(-1,-2,-3))),
            (6,((1,2,3),(-1,-2,-3),(4,5,6),(-4,-5,-6)))]
    for n,F in extras:
        t=trial(n,F); checked+=t['N']; formula_count+=1
    for n in range(3,10):
        for _ in range(24):
            F=[]
            for _ in range(rng.randrange(45)):
                vs=rng.sample(range(1,n+1),3)
                F.append(tuple(z if rng.randrange(2) else -z for z in vs))
            t=trial(n,tuple(F)); checked+=t['N']; formula_count+=1
    caps={str(n):n+24*math.comb(n,3)-1 for n in (3,8,20,35,80,160,200,250)}
    cutoffs={}
    for mu in (0.125,0.25,0.5,0.75):
        cond=[mu*n>=math.log2(n+24*math.comb(n,3)-1) for n in range(3,256)]
        cutoffs[str(mu)]=next((n for n in range(3,256) if all(cond[n-3:])),None)
    assert all(v is not None for v in cutoffs.values())
    src=Path(__file__).read_bytes()
    raw=dict(backend='native CPython',status='COMPUTATIONAL',seed=seed,
             code_sha256=hashlib.sha256(src).hexdigest(),formula_count=formula_count,
             truth_evaluations=checked,distinct_three_variable_truth_tables=len(distinct),
             opposite_label_equal_length_examples=named,
             gate_upper_caps=caps,finite_threshold_crossings=cutoffs,
             failures=0,exact_TM_simulation=False)
    out=Path(__file__).with_name('2026-11-14_0941_TMR4_MCSP_SHELL024_RAW.json')
    out.write_text(json.dumps(raw,sort_keys=True,indent=2)+'\n')
    print(json.dumps(raw,sort_keys=True,indent=2))

if __name__=='__main__':main()
