#!/usr/bin/env python3
"""CLOCKPARITY12 finite controls: GF(4) fingerprint parity reduction,
selector sandwich, and random inventory NO trapping. Pure Python, no dependencies.
"""
import itertools
import json
import math
import random
from pathlib import Path

SEED = 202610182112
rng = random.Random(SEED)

def gf4_mul(a, b):
    value = 0
    for bit in range(2):
        if (b >> bit) & 1:
            value ^= a << bit
    for bit in range(2, 1, -1):
        if value & (1 << bit):
            value ^= 0b111 << (bit - 2)  # X^2+X+1
    return value

def gf4_pow(a, e):
    out = 1
    while e:
        if e & 1:
            out = gf4_mul(out, a)
        a = gf4_mul(a, a)
        e //= 2
    return out

def field_hash(table_bits, length, alpha=2):
    total, power = 0, 1
    for i in range(length):
        if (table_bits >> i) & 1:
            total ^= power
        power = gf4_mul(power, alpha)
    return total

def embedded_table(mask, k):
    out = 0
    for j in range(1 << k):
        if mask & (1 << j):
            out |= (1 << (3*j))
    return out

def linear_hash(table_bits, cols):
    out = 0
    while table_bits:
        lsb = table_bits & -table_bits
        out ^= cols[lsb.bit_length()-1]
        table_bits ^= lsb
    return out

def one_family_exact(N=5,b=2,w=2,f=0b00111):
    weight_words=[v for v in range(1<<N) if v.bit_count()==w]
    fail=0
    matrices=0
    for flat in itertools.product(range(1<<b),repeat=N):
        matrices+=1
        image={linear_hash(g,flat) for g in weight_words}
        if linear_hash(f,flat) not in image:
            fail+=1
    L=math.comb(N,w)
    delta=(2**b-1)/(L+2**b-1)
    assert fail/matrices <= delta + 1e-12
    return {"N":N,"b":b,"weight":w,"L":L,"fixed_f":f,
            "matrix_count":matrices,"no_collision_count":fail,
            "no_collision_frequency":fail/matrices,
            "cantelli_bound":delta}

def family_sampling(N=5,b=2,w=2,f=0b00111,R=3,trials=10000):
    weight_words=[v for v in range(1<<N) if v.bit_count()==w]
    exceptional_any=0
    for _ in range(trials):
        rows=[[rng.randrange(1<<b) for _ in range(N)] for __ in range(R)]
        if any(linear_hash(f,cols) not in {linear_hash(g,cols) for g in weight_words}
               for cols in rows):
            exceptional_any+=1
    single=one_family_exact(N,b,w,f)
    upper=min(1.0,R*single['cantelli_bound'])
    assert exceptional_any/trials <= upper + 0.02, (exceptional_any/trials,upper)
    return {"seed":SEED,"trials":trials,"R":R,"any_seed_NO":exceptional_any,
            "any_seed_NO_rate":exceptional_any/trials,"union_theorem_bound":upper}

def sandwich_exhaustive():
    universe=set(range(8)); Y={0,1,2}; NO=universe-Y; core={0,1}
    available=[core|{i for bit,i in enumerate(sorted(universe-core)) if (mask>>bit)&1}
               for mask in range(1<<(len(universe-core)))]
    checked=0; feasible=0; failed_Y=0; failed_NO=0
    for X0 in available:
        for X1 in available:
            checked+=1
            good_Y=all(x in X0 or x in X1 for x in Y)
            good_NO=all(x not in X0 or x not in X1 for x in NO)
            sandwich=good_Y and good_NO
            if not good_Y: failed_Y+=1
            if not good_NO: failed_NO+=1
            selector_exists=all(any(((x in X) == (x in Y)) for X in [X0,X1]) for x in universe)
            assert sandwich == selector_exists
            feasible+=sandwich
    return {"universe":8,"source_Y":sorted(Y),"low_budget_core":sorted(core),
            "families_checked":checked,"feasible_families":feasible,
            "YES_uncovered_families":failed_Y,"NO_trapped_families":failed_NO}

def main():
    exhaustive_cases=0
    alpha=2
    assert [gf4_pow(alpha,i) for i in range(6)]==[1,2,3,1,2,3]
    for k in range(1,5):
        for original in range(1 << (1 << k)):
            padded=embedded_table(original,k)
            hashed=field_hash(padded,1<<(k+2),alpha)
            assert hashed == original.bit_count()%2,(k,original,hashed)
            exhaustive_cases+=1
    for z in range(4):
        sparse=(z&1)|((z>>1)<<1)
        assert field_hash(sparse,16,alpha)==z
    result={"report":"CLOCKPARITY12","date":"2026-10-18","seed":SEED,
      "GF4":{"minimal_polynomial":"X^2+X+1","alpha_representation":2,"order":3,
             "exhaustive_circuit_truth_tables_tested":exhaustive_cases,
             "assertion_failures":0,"sparse_image_labels_tested":4},
      "selector_sandwich":sandwich_exhaustive(),
      "exact_inventory":one_family_exact(),
      "random_inventory":family_sampling(),
      "proof_status":"finite computational controls, not complexity lower bounds"}
    out=Path("results/raw/meta_lift/2026-10-18_CLOCKPARITY12_raw.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__":
    main()
