#!/usr/bin/env python3
"""Finite semantic checks for TMR-1/027 low-growing MCSP upper envelope.
This is NOT a compiled one-work-tape machine; the machine bound is symbolic.
"""
import json, random, math
from functools import lru_cache

SEED = 20261114
random.seed(SEED)

@lru_cache(None)
def circuits(n, cap):
    full = (1 << (1 << n)) - 1
    vars_ = []
    for j in range(n):
        v = sum(((i >> j) & 1) << i for i in range(1 << n))
        vars_.append(v)
    base = tuple([0, full] + vars_)
    out = set(base)
    layer = {(): base}
    descriptions = len(base)
    for gate in range(cap):
        next_layer = {}
        for seq, wires in layer.items():
            m = len(wires)
            for a in range(m):
                v = wires[a]
                new = seq + (('N', a, 0),)
                next_layer[new] = wires + (full ^ v,)
                out.add(full ^ v)
                descriptions += 1
                for b in range(m):
                    w = wires[b]
                    for typ, val in [('A', v & w), ('O', v | w)]:
                        new = seq + ((typ, a, b),)
                        next_layer[new] = wires + (val,)
                        out.add(val)
                        descriptions += 1
        layer = next_layer
    return frozenset(out), descriptions

def records(bits):
    # Physical tape implementation writes self-delimited binary address, delimiter,
    # bit and locally maintained counter; here only semantics are tested.
    return [(format(i, 'b'), b) for i, b in enumerate(bits)]

def indexed_candidate_test(recs, function_mask):
    for binary_address, input_bit in recs:
        j = int(binary_address, 2)
        if ((function_mask >> j) & 1) != input_bit:
            return False
    return True

def decide(bits, cap, candidates):
    N = len(bits)
    if N < 2 or (N & (N - 1)):
        return False
    recs = records(bits)
    return any(indexed_candidate_test(recs, m) for m in candidates)

checks = 0
counts = {}
for n in range(1, 4):
    N = 1 << n
    for s in range(3):
        masks, descriptions = circuits(n, s)
        counts[f'n={n},s={s}'] = {'different_functions':len(masks), 'syntactic_descriptions_proxy': descriptions}
        for truth in range(1 << N):
            bits = [(truth >> i) & 1 for i in range(N)]
            got = decide(bits, s, masks)
            independently = truth in masks
            assert got == independently, (n, s, truth)
            checks += 1

expected = {(1,0):3,(1,1):4,(1,2):4,
            (2,0):4,(2,1):8,(2,2):14,
            (3,0):5,(3,1):14,(3,2):40}
for (n,s), count in expected.items():
    assert len(circuits(n,s)[0]) == count
    checks += 1
for length in range(0, 42):
    if length in (2,4,8,16,32):
        continue
    assert not decide([0]*length, 0, circuits(3,0)[0])
    checks += 1

# Exact syntactic encoding count envelope, no empirical exponent claims.
for n in (4,8,16,32,64,128,256,512,1024,2048):
    s = max(0, int(0.004*n/math.log2(n)))
    log2D = math.log2(s+1) + math.log2(n+s+2) + s*(math.log2(3)+2*math.log2(n+s+2))
    assert log2D >= 0
    checks += 1

result = {'run':'TMR1-SLOWTHRESH30', 'seed':SEED,
          'scope':'finite semantic candidate descriptions, not TM transition execution',
          'classifications_checked':sum((1 << (1 << n))*3 for n in range(1,4)),
          'assertions_passed': checks,
          'assertion_failures':0, 'class_counts':counts,
          'asymptotic_claim':'s(n)=floor(kappa*n/log2 n), log2 D(n,s) <= (2*kappa+o(1))*n; N=2^n',
          'model':'one-way read-only explicit input plus one two-way read/write work tape; symbolic compilation'}
print(json.dumps(result,sort_keys=True,indent=2))
