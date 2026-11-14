#!/usr/bin/env python3
"""TMR-2 shared-preprocessing oracle sensitivity audit, 2026-11-14.
Pure Python, no dependencies, fixed seeds. Verifies restricted finite inequalities,
not a machine-time lower bound. Output is machine-readable JSON.
"""
from __future__ import annotations
import json, random, hashlib, sys
from collections import Counter


def execute(mask: int, m: int, nout: int, b: int, q: int, seed: int):
    """Deterministic source-independent adaptive black-box transformation.
    Stage P: at most b distinct oracle coordinates on a zero input.
    Each output bit independently makes at most q queries, starting with P state.
    Source input is a bit-mask for tests, never exposed to decision routine.
    """
    x = lambda a: (mask >> a) & 1
    used = []
    global_state = (seed * 0x9E3779B1) & 0xFFFFFFFF
    responses = []
    for t in range(b):
        a = (global_state + 7 * t + seed) % m
        while a in used:
            a = (a + 1) % m
        z = x(a)
        used.append(a)
        responses.append(z)
        global_state = (global_state * 1664525 + 1013904223 + z * (t + 3)) & 0xFFFFFFFF
    outs = []
    for j in range(nout):
        local_state = (global_state ^ (j * 2246822519) ^ seed) & 0xFFFFFFFF
        local_read = []
        local_bits = []
        for t in range(q):
            a = (local_state + 11 * t + 17 * j) % m
            while a in local_read:
                a = (a + 1) % m
            z = x(a)
            local_read.append(a)
            local_bits.append(z)
            local_state = (local_state * 1103515245 + z * 12345 + t) & 0xFFFFFFFF
        # Any nonlinear deterministic postprocessing of P and local queries.
        out = (sum(responses) + sum(local_bits) + (local_state & 3) + j) % 2
        outs.append(out)
    return tuple(outs), tuple(used)


def sharp(mask: int, m: int, nout: int, b: int, q: int):
    """Sharp nonadaptive construction when nout multiple of m-b."""
    pre = tuple(range(b))
    pvalue = any((mask >> a) & 1 for a in pre)
    rem = list(range(b, m))
    outs = []
    for j in range(nout):
        w = [rem[(j + t) % (m-b)] for t in range(q)]
        outs.append(int(pvalue or any((mask >> a) & 1 for a in w)))
    return tuple(outs)


def main():
    grouped = Counter()
    exhaustive_yes_masks = 0
    sharp_cases = 0
    zero_local_controls = 0
    witnessed_global_controls = 0
    rng = random.Random(32028)
    for v in range(1, 6):
        m = 1 << v
        for b in sorted(set([0, 1, m//3, m//2, m-1])):
            for q in sorted(set([0, 1, 2, min(3, m)])):
                if q > m: continue
                for seed in [0, 1, 7, 19]:
                    nout = rng.choice([1, m//2+1, m, 2*m+1])
                    base, zero_global_queries = execute(0, m, nout, b, q, seed)
                    b_eff = len(set(zero_global_queries))
                    assert b_eff == b
                    sum_outside = 0
                    sum_total = 0
                    for a in range(m):
                        y, _ = execute(1 << a, m, nout, b, q, seed)
                        diff = sum(u != w for u, w in zip(y, base))
                        sum_total += diff
                        if a not in zero_global_queries:
                            sum_outside += diff
                            assert diff <= nout
                    assert sum_outside <= nout*q, (v,b,q,seed,sum_outside,nout*q)
                    assert sum_total <= nout*(b_eff+q)
                    grouped['adaptive_global_local_cases'] += 1
                    grouped['singletons'] += m
                    grouped['output_coordinates'] += nout*m
                    if q == 0:
                        zero_local_controls += 1
                        for a in range(m):
                            if a not in zero_global_queries:
                                y, _ = execute(1 << a, m, nout, b, q, seed)
                                assert y == base
                if b < m:
                    nout = 2 * (m-b)
                    q_use = min(q, m-b)
                    base = sharp(0, m, nout, b, q_use)
                    assert not any(base)
                    all_sum, outside_sum = 0, 0
                    for a in range(m):
                        y = sharp(1 << a, m, nout, b, q_use)
                        diff = sum(y)
                        all_sum += diff
                        if a >= b:
                            outside_sum += diff
                            assert diff == nout*q_use//(m-b)
                        else:
                            assert diff == nout
                    assert outside_sum == nout*q_use
                    assert all_sum == nout * (b+q_use)
                    sharp_cases += 1
                    grouped['sharp_singletons'] += m
                    if q_use == 0:
                        witnessed_global_controls += 1
    print(json.dumps({
       'name':'TMR2_SHARED_ORACLE_PREPROCESS032',
       'date_pst':'2026-11-14 14:16',
       'model':'fixed source-independent evaluation oracle; shared b-query adaptive preprocessing followed by independently restarted <=q queries per output bit',
       'assertions_failed':0,
       'random_seed':32028,
       'counts':dict(grouped),
       'sharp_cases':sharp_cases,
       'zero_local_controls':zero_local_controls,
       'sharp_global_controls':witnessed_global_controls,
       'theorem':'sum outside_Q0 Hamming(Y(f_a),Y(0)) <= N*q; sum all <= N*(b+q). Bounds sharp when N divisible by M-b.',
       'status':'COMPUTATIONAL finite check; asymptotic result from separate elementary proof'
    },sort_keys=True,indent=2))

if __name__=='__main__':
    main()
