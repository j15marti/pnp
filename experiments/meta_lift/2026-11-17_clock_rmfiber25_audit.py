#!/usr/bin/env python3
"""CLOCKRMFIBER25 exact finite controls. Python stdlib only."""
import json, random, hashlib, math, sys
from collections import Counter
SEED=202611171827
rng=random.Random(SEED)
checks=Counter()

def check(flag,label):
    checks[label]+=1
    if not flag:
        raise AssertionError(label)

def mons(N,d):
    return [mask for mask in range(1<<N) if mask.bit_count()<=d]

def poly_values(N,terms):
    out=[]
    for x in range(1<<N):
        v=0
        for mon in terms:
            if x&mon==mon: v^=1
        out.append(v)
    return out

def actual_degree(terms):
    return max((t.bit_count() for t in terms),default=0)

def ax_exp(N,degrees):
    ds=[d for d in degrees if d>0]
    if not ds: return None
    return max(0,math.ceil((N-sum(ds))/max(ds)))

def test_system(N,polys,tag):
    ds=[actual_degree(p) for p in polys]
    vals=[poly_values(N,p) for p in polys]
    sizes=Counter(tuple(v[x] for v in vals) for x in range(1<<N))
    v=ax_exp(N,ds)
    D=sum(ds)
    rmexp=max(0,N-D)
    # Reed-Muller minimum distance / Warning's second theorem: EVERY
    # nonempty fiber has at least 2^(N-sum degrees) elements.
    for count in sizes.values():
        check(count >= (1<<rmexp),"reed_muller_fiber_mass")
    if v is not None and v>0:
        for count in sizes.values():
            check(count%(1<<v)==0,"ax_katz_divisibility")
            check(count >=1<<v,"ax_katz_positive_fiber")
    check(sum(sizes.values())==(1<<N),"fiber_partition")
    return dict(tag=tag,N=N,m=len(polys),degrees=ds,ax_exponent=v,rm_exponent=rmexp,nonempty_fibers=len(sizes),min_fiber=min(sizes.values()),max_fiber=max(sizes.values()))

examples=[]
# Exhaust all degree <=2 polynomial maps on four source truth-table bits.
M=mons(4,2)
for code in range(1<<len(M)):
    poly=[M[i] for i in range(len(M)) if code>>i&1]
    ex=test_system(4,[poly],"all_single_quadratics_N4")
check(len(M)==11,"monomial_count_N4")
examples.append(dict(label="exhaustive_N4_d2",polynomials=1<<len(M)))

# 850 random 1-4 coordinate maps over 8 truth-table bits; coefficients include constants.
for idx in range(850):
    m=rng.randrange(1,5); deg=rng.randrange(1,5)
    bases=mons(8,deg)
    # random 0..4 selected ANF monomials of degree <=deg (sparse and dense variants)
    polys=[]
    for j in range(m):
        p=[t for t in bases if rng.random()<(0.5 if idx%17==0 else .075)]
        polys.append(p)
    ex=test_system(8,polys,"seeded_N8")
    if idx in (0,7,100,500,849): examples.append(ex)

# N=8 nondegenerate quadratic in four disjoint coordinate pairs.
P=[3,12,48,192]
quad=test_system(8,[P],"symplectic_quadratic_N8")
quad_vals=poly_values(8,P)
quad_counts=Counter(quad_vals)
check(quad_counts[0]==136 and quad_counts[1]==120,"quadratic_sharp_fiber_counts")
check(quad["ax_exponent"]==3,"quadratic_sharp_exponent")
examples.append(quad)
# Tight Reed-Muller bound: AND of d of N input coordinates has 2^(N-d)
# satisfying inputs; choosing output 1 attains the minimum mass bound.
for d in range(1,8):
    ex=test_system(8,[[(1<<d)-1]],f"AND_degree_{d}_tight")
    check(ex["min_fiber"]==(1<<(8-d)),"reed_muller_tight_AND")
examples.append(dict(label="and_fiber_bound_tight",tested_degrees=list(range(1,8))))

# High degree x0 OR x1 OR ... OR x7, zero fiber singleton.
# OR(x) has ANF all nonempty monomials.
OR=[v for v in range(1,1<<8)]
high=test_system(8,[OR],"high_degree_OR_N8")
check(high["min_fiber"]==1,"highdegree_escape_singleton")
examples.append(high)

# Exact size<=2 circuit sets for n=3, all 16 binary Boolean gate operations.
# 8-bit truth tables correspond to source functions of three index inputs.
MASK=(1<<8)-1
base=[0,MASK]
for j in range(3): base.append(sum(1<<x for x in range(8) if x>>j&1))
def gate(u,v,op):
    a= ((~u)&(~v))&MASK; b=((~u)&v)&MASK
    c=(u&(~v))&MASK; d=u&v
    return ((a if op&1 else 0)|(b if op&2 else 0)|(c if op&4 else 0)|(d if op&8 else 0))
low0=set(base);low1=set(low0)
for u in base:
    for v in base:
        for op in range(16): low1.add(gate(u,v,op))
low2=set(low1)
for t in low1:
    for u in base+[t]:
        for v in base+[t]:
            for op in range(16):low2.add(gate(u,v,op))
check(low0<=low1<=low2,"circuit_nested")
qfib={0:[],1:[]}
for x,b in enumerate(quad_vals):qfib[b].append(x)
for b in (0,1):
    check(any(x in low2 for x in qfib[b]),"quadratic_fiber_yes")
    check(any(x not in low2 for x in qfib[b]),"quadratic_fiber_no")
examples.append(dict(label="exact_n3_two_gate_circuit_basis",basis="all_16_boolean_binary_gates_with_constants_and_three_inputs",cost0=len(low0),cost_le1=len(low1),cost_le2=len(low2),quadratic_fibers=[dict(output=b,size=len(qfib[b]),small=sum(x in low2 for x in qfib[b]),large=sum(x not in low2 for x in qfib[b])) for b in (0,1)]))

# Affine output control: coordinate projections have exactly 2^(N-m) points per fiber.
for N in (4,8):
    for m in range(1,N+1):
        ps=[[1<<i] for i in range(m)]
        ex=test_system(N,ps,"coordinate_projection_exact")
        check(ex["min_fiber"]==(1<<(N-m)) and ex["max_fiber"]==(1<<(N-m)),"projection_exact_bound")

summary={"status":"COMPUTATIONAL; theorem uses classical Reed-Muller minimum distance plus circuit counting; Ax-Katz is an independent weaker divisibility control", "seed":SEED,"counts":dict(checks),"total_assertions":sum(checks.values()),"failures":0,"examples":examples,"python":sys.version.split()[0],"scope":"exhaustive single-output degree<=2 polynomial maps on 4 raw source bits; seeded multiple-output maps on 8 bits; exact <=2 fan-in-two gates over all 16 binary operations for n=3; no proof of P!=NP"}
path='/mnt/data/2026-11-17_CLOCKRMFIBER25_raw.json'
with open(path,'w') as f:json.dump(summary,f,sort_keys=True,indent=2)
print(json.dumps({k:v for k,v in summary.items() if k not in ['examples']},sort_keys=True,indent=2))
print('Exact circuit/fiber example:',next(x for x in examples if x.get('label')=='exact_n3_two_gate_circuit_basis'))
