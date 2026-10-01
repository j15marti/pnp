#!/usr/bin/env python3
"""Toy tests for CRS-PPC-SAT transcript mechanics.

These tests do NOT test SAT hardness. They test:
1. fresh stopping-time snapshots;
2. transcript divergence caused by solve-time differences;
3. agreement with the Timing-Sensitivity Lemma.

Seed family starts at 20261001.
"""
import itertools
import random
import statistics
from collections import Counter

def eval_cnf(clauses, a):
    for clause in clauses:
        if not any((bool((a >> v) & 1) == sign) for v, sign in clause):
            return False
    return True

def formula_from_block(block, n=8, m=28, epoch=0):
    seed = 0
    for bit in block:
        seed = (seed << 1) | bit
    rr = random.Random(seed ^ (epoch * 2654435761))
    clauses = []
    for _ in range(m):
        vs = rr.sample(range(n), 3)
        clauses.append([(v, bool(rr.getrandbits(1))) for v in vs])
    return clauses

def brute(clauses, n=8):
    for a in range(1 << n):
        if eval_cnf(clauses, a):
            return True, a, a + 1
    return False, None, 1 << n

def fast_control(clauses, n=8):
    # Compute the correct result for bookkeeping, but charge unit solve time.
    for a in range(1 << n):
        if eval_cnf(clauses, a):
            return True, a, 1
    return False, None, 1

def run(G, b, z, kind, n=8, m=28):
    tau = 0
    out = []
    for e in range(z):
        if tau + b > len(G):
            break
        block = tuple(G[tau:tau + b])
        phi = formula_from_block(block, n, m, e)
        sat, w, steps = brute(phi, n) if kind == "brute" else fast_control(phi, n)
        out.append((tau, block, sat, w, steps))
        tau += b + steps
    return out

def transcript_trials(b, num=200, z=6):
    diff2 = 0
    nodiv = 0
    matches = []
    for q in range(num):
        rr = random.Random(20261001 + 10000 * b + q)
        G = [rr.getrandbits(1) for _ in range(12000)]
        A = run(G, b, z, "brute")
        B = run(G, b, z, "fast")
        same = [A[i][1] == B[i][1] for i in range(z)]
        matches.append(sum(same))
        if z > 1 and not same[1]:
            diff2 += 1
        if all(same):
            nodiv += 1
    return {
        "b": b,
        "trials": num,
        "epoch2_diff_fraction": diff2 / num,
        "mean_matching_epochs": statistics.mean(matches),
        "no_divergence_runs": nodiv,
    }

def conditioned_trials(b, num=1000):
    differing = equal = 0
    for q in range(num):
        rr = random.Random(314159 + 10000 * b + q)
        G = [rr.getrandbits(1) for _ in range(5000)]
        A = run(G, b, 2, "brute")
        B = run(G, b, 2, "fast")
        if A[0][4] != B[0][4]:
            differing += 1
            equal += (A[1][1] == B[1][1])
    return {
        "b": b,
        "different_timing": differing,
        "equal_next_snapshot": equal,
        "empirical_equal_rate": equal / differing,
        "theoretical_2^-b": 2 ** (-b),
    }

def exact_stopping_test():
    # tau = first 1 among positions 1..3; if none, tau=3.
    # Inspect the next two bits. Enumerate all 5-bit source strings.
    cnt = Counter()
    for bits in itertools.product([0, 1], repeat=5):
        tau = 3
        for i in range(3):
            if bits[i] == 1:
                tau = i + 1
                break
        block = bits[tau:tau + 2]
        cnt[block] += 1
    return dict(sorted(cnt.items()))

if __name__ == "__main__":
    print("EXACT_STOPPING_TEST", exact_stopping_test())
    for b in [4, 8, 12, 16]:
        print("TRANSCRIPT", transcript_trials(b))
    for b in [4, 8, 12]:
        print("CONDITIONED", conditioned_trials(b))
