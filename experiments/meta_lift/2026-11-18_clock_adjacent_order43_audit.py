#!/usr/bin/env python3
"""CLOCKSOURCEVERIFY43 addendum: order-sensitive nonlinear adjacent-run output.
Finite controls; full-source streaming, parity, previous bit, and adjacent pair flag.
"""
import json, pathlib, random
SEED=20261118204343
rng=random.Random(SEED)
counts={'source_cases':0,'flip_cases':0,'assertions':0,'anf_mobius_values':0,'order_witnesses':0}
records=[]
def check(z,label):
    counts['assertions']+=1
    if not z:raise AssertionError(label)
def scan(f,N):
    b=prev=adj=0
    for i in range(N):
        bit=(f>>i)&1
        adj|=prev&bit
        prev=bit
        b^=bit
    return b,adj
def simple(f,N):
    return (f.bit_count()%2,int(any((f>>i&3)==3 for i in range(N-1))))
def canonical(N, parity, adj):
    if adj==0:return 0 if parity==0 else 1
    if parity==0:return 3
    if N>=3:return 7
    return None

def degree(N):
    poly=[simple(x,N)[1] for x in range(1<<N)]
    for bit in range(N):
        mask=1<<bit
        for m in range(1<<N):
            if m&mask:poly[m]^=poly[m^mask]
    counts['anf_mobius_values']+=N*(1<<N)
    d=max((m.bit_count() for m,c in enumerate(poly) if c),default=-1)
    return d,poly[-1]

for N in [2,4,8,16]:
    samples=list(range(1<<N)) if N<=8 else [0,1,3,7,5,15,(1<<N)-1]+[rng.getrandbits(N) for _ in range(512)]
    outputs=set()
    for f in samples:
        y=scan(f,N)
        check(y==simple(f,N),'stream functional equality')
        z=canonical(N,*y)
        check(z is not None and scan(z,N)==y,'canonical section')
        outputs.add(y)
        indices=range(N) if N<=8 else [0,1,N//2,N-2,N-1]
        for i in indices:
            chk=scan(f^(1<<i),N)
            check(chk[0]!=y[0],'full coordinate sensitivity')
            counts['flip_cases']+=1
        counts['source_cases']+=1
    check(outputs == ({(0,0),(1,0),(0,1)} if N==2 else {(0,0),(1,0),(0,1),(1,1)}),'fiber coverage')
    if N>=4:
        check(scan(3,N)!=(scan(5,N)),'order-sensitive equal-weight pair')
        counts['order_witnesses']+=1
    d,top=degree(N)
    check(d>=2*((N+1)//3),'linear ANF degree lower bound')
    records.append({'N':N,'tested_sources':len(samples),'distinct_labels':len(outputs),'exact_anf_degree':d,'top_coefficient':top})

out={'model':'CLOCKSOURCEVERIFY43 40-state order-sensitive nonlinear addendum','seed':SEED,'counts':counts,'records':records,'failures':0,'independent_review':'OPEN','p_vs_np':'OPEN'}
p=pathlib.Path(__file__).with_name('2026-11-18_CLOCKSOURCEVERIFY43_order_raw.json')
p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,sort_keys=True,indent=2))
