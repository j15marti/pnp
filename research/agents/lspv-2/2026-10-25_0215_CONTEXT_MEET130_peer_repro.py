#!/usr/bin/env python3
"""CONTEXT-MEET-FIREWALL130: independent finite verification.
Pure Python 3.11+, standard library. Abstract masks and logical queries only.
This is NOT a full FLMV bit-machine simulation or a P-vs-NP proof.
"""
from itertools import product
from math import ceil, log2
import random, json, hashlib

SEED=202610241015
rng=random.Random(SEED)
counts={"menus":0,"left_sets":0,"pair_tests":0,"identity_tests":0,
        "closure_tests":0,"necessity_witnesses":0,"sufficient_pair_tests":0,
        "pin_truth_rows":0,"random_menus":0,"failures":0}

def profile(left, contexts):
    return sum((bool(left & right) << j) for j,right in enumerate(contexts))

def columns(m, contexts):
    return [sum((((right>>u)&1)<<j) for j,right in enumerate(contexts))
            for u in range(m)]

def or_closure(cols):
    found={0}
    for col in cols:
        found|={x|col for x in tuple(found)}
    return found

def singleton_complete(m, contexts):
    covered=0
    for v in contexts: covered|=v
    return all((1<<u) in contexts for u in range(m) if covered&(1<<u))

def audit_menu(m, contexts, do_pairs):
    counts['menus']+=1
    size=1<<m
    cols=columns(m, contexts)
    closure=or_closure(cols)
    values=[profile(a, contexts) for a in range(size)]
    counts['left_sets']+=size
    assert set(values)==closure
    counts['closure_tests']+=1
    for a in range(size):
        z=0
        for u in range(m):
            if (a>>u)&1: z|=cols[u]
        assert z==values[a]
        counts['identity_tests']+=1
    bits=ceil(log2(len(closure))) if len(closure)>1 else 0
    assert (1<<bits)>=len(closure)
    if bits: assert (1<<(bits-1))<len(closure)
    if do_pairs:
        seen={}
        stable=True
        for a in range(size):
            for b in range(size):
                key=(values[a],values[b]); out=values[a&b]
                if key in seen and seen[key]!=out: stable=False
                else: seen[key]=out
                counts['pair_tests']+=1
        exact=singleton_complete(m, contexts)
        assert stable==exact, (m,contexts,stable,exact)
        if exact: counts['sufficient_pair_tests']+=size*size
        else:
            covered=0
            for right in contexts:covered|=right
            u=next(u for u in range(m) if covered&(1<<u) and (1<<u) not in contexts)
            whole=size-1
            less=whole^(1<<u)
            witness=1<<u
            assert values[whole]==values[less]
            assert values[whole&witness]!=values[less&witness]
            counts['necessity_witnesses']+=1
    return bits,len(closure)

for m in range(1,4):
    all_subsets=range(1<<m)
    for q in range(5):
        for contexts in product(all_subsets, repeat=q):
            audit_menu(m,contexts,True)

for m in range(1,13):
    assert audit_menu(m,[1<<u for u in range(m)],m<=3)==(m,1<<m)
    assert audit_menu(m,[(1<<m)-1]*m,m<=3)==(1,2)
    k,b=audit_menu(m,[(1<<(j+1))-1 for j in range(m)],m<=3)
    assert b==m+1 and k==ceil(log2(m+1))

for _ in range(700):
    m=rng.randrange(1,11); q=rng.randrange(0,11)
    contexts=[rng.randrange(0,1<<m) for __ in range(q)]
    audit_menu(m,contexts,m<=4)
    counts['random_menus']+=1

def pin(lit_value, a, b):
    return all(lit_value or aa or bb for aa,bb in ((a,b),(a,not b),(not a,b),(not a,not b)))
for val,a,b in product((0,1),repeat=3):
    assert pin(val,a,b)==bool(val)
    counts['pin_truth_rows']+=1
U=3; A=1; A_prime=3; C=2
assert profile(A,[U])==profile(A_prime,[U])==1
assert profile(A&C,[U])==0 and profile(A_prime&C,[U])==1
assert A and C and not(A&C)

assert counts['failures']==0
out={"run":"CONTEXT-MEET-FIREWALL130","status":"COMPUTATIONAL / passed finite checks",
     "seed":SEED,"counts":counts,
     "theorem_scope":"Detached, fixed public context menu; arbitrary interface feasibility subsets",
     "not_claimed":"Unrestricted SAT lower bound, FLMV primitive-bit accounting, all-input ARC successor",
     "counterexample":{"universe_size":2,"menu":[[0,1]],"left_A":[0],"left_A_prime":[0,1],"right_C":[1],"profile_A_and_Aprime":1,"joined_A":False,"joined_Aprime":True}}
from pathlib import Path
if __name__ == "__main__":
    dest = Path(__file__).resolve().with_name("context_meet130_results.json")
    with dest.open("w",encoding="utf-8") as f:
        json.dump(out,f,indent=2,sort_keys=True)
    print(json.dumps(out,sort_keys=True))
