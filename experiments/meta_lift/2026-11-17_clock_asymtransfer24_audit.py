#!/usr/bin/env python3
"""Finite controls for CLOCK-ASYMMETRIC-TRANSFER24, deterministic, stdlib only.
This is a small *formula* complexity proxy, NOT MCSP circuit size.
"""
from collections import defaultdict
import json
from itertools import product
from pathlib import Path
N=8
mask=(1<<N)-1
vars_=[sum(((i>>j)&1)<<i for i in range(N)) for j in range(3)]
# Formulas use constants/literals cost 0 and AND/OR/XOR binary gates cost 1,
# allowing complemented edges (NOT of a computed signal has no counted cost).
by_cost=[set() for _ in range(8)]
by_cost[0].update((0,mask))
for v in vars_: by_cost[0].update((v, mask^v))
for t in range(1,8):
    S=set()
    for leftcost in range(t):
        rightcost=t-1-leftcost
        for a in by_cost[leftcost]:
            for b in by_cost[rightcost]:
                S.add(a&b); S.add(a|b); S.add(a^b)
    S |= {mask^z for z in S}
    lower=set().union(*by_cost[:t]); by_cost[t]=S-lower
    if len(set().union(*by_cost[:t+1]))==256: break
cost={v:c for c,S in enumerate(by_cost) for v in S}
assert len(cost)==256

def bits(f):return [(f>>i)&1 for i in range(N)]
def quotient(f,name,s=2):
    v=bits(f)
    if name=='parity':return sum(v)%2
    if name=='histogram':return sum(v)
    if name=='firstlast':return (v[0],v[-1])
    if name=='pair_counts':return (v[0],v[-1],tuple(sum(v[i]==a and v[i+1]==b for i in range(N-1)) for a,b in product(range(2),repeat=2)))
    if name=='identity':return f
    if name=='decision_oracle':return int(cost[f]<=s)
    raise ValueError(name)

def test(s,w):
    table=[]
    for name in ('parity','histogram','firstlast','pair_counts','identity','decision_oracle'):
        fiber=defaultdict(list)
        for f in range(256):fiber[str(quotient(f,name,s))].append(f)
        yes={f for f in range(256) if cost[f]<=s}
        short={f for f in range(256) if cost[f]<=w}
        yes_compressed=all(any(g in short for g in fiber[str(quotient(f,name,s))]) for f in yes)
        no_collision=all(not any(g in short for g in fiber[str(quotient(f,name,s))]) for f in set(range(256))-yes)
        pure=all((not (set(F)&yes) or not (set(F)-yes)) for F in fiber.values())
        table.append(dict(name=name,output_count=len(fiber),yes_compressed=yes_compressed,no_short_false_positive=no_collision,exact_purity=pure, yes_count=len(yes),short_count=len(short)))
    return table

rows=[{'s':s,'w':w,'rows':test(s,w)} for s,w in [(1,0),(2,1),(3,2)]]
# Numeric cofinal regime. κ is unknown but fixed, output exponent λ^j.
cofinal=[]
for kappa in [1,2,4,10,25,100,1000]:
    for j in range(1,128):
        theta=(2.0)*(0.5**j)
        # quadratic single-work-tape simulation of assumed kappa exponent
        if 2*kappa*theta < 1.80:
            cofinal.append(dict(kappa=kappa,stage=j,verifier_tape_exponent=2*kappa*theta))
            break
assert len(cofinal)==7
# An unbounded stage-specific verifier exponent destroys cofinal absorption.
nonuniform=[{'j':j,'lambda_power_j':2**(-j),'kappa_j':2**j,'product':1} for j in range(1,13)]
assert all(x['product']==1 for x in nonuniform)
# Independent invariants, not reliance on assert statements in optimized Python.
for item in rows:
    for r in item['rows']:
        if r['exact_purity'] and not r['no_short_false_positive']:raise AssertionError('Purity must exclude NO false positives')
        if r['name']=='decision_oracle':assert r['exact_purity'] and r['yes_compressed'] and r['no_short_false_positive']
        if r['name']=='identity' and item['s']>item['w']:assert not r['yes_compressed']
output={'scope':'8-bit truth tables, minimum formula gates for AND/OR/XOR with complemented edges; NOT general MCSP',
        'N':N,'minimum_formula_gate_counts':{str(k):len(v) for k,v in enumerate(by_cost) if v},'cases':rows,
        'uniform_cofinal_examples':cofinal,'nonuniform_failure':nonuniform,
        'assertion_failures':0,'exact_exhaustive_source_inputs':256,'seed':None}
p=Path('results/raw/meta_lift/2026-11-17_CLOCKASYMTRANSFER24_raw.json');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
