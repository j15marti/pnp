#!/usr/bin/env python3
"""MAGRED-DISTANCE-OVERLAP9 reproducible finite red-team controls.

Enumerates every 0-, 1- and 2-gate AND/OR/NOT Boolean function on six
variables. Finds minimum counterexample anti-checkers by exhaustive
search and runs seeded fixed-size random anti-checker trials.
This is a finite computation, not an asymptotic circuit lower bound.
"""
from itertools import combinations, combinations_with_replacement
from random import Random
from pathlib import Path
import json


def easy(n, t):
    N = 1 << n
    mask = (1 << N) - 1
    x = tuple(sum(((i >> j) & 1) << i for i in range(N)) for j in range(n))
    base = (0, mask) + x
    seen = set(base)
    states = {()}
    for _ in range(t):
        updated = set()
        for st in states:
            vals = base + st
            for a in vals:
                g = mask ^ a
                updated.add(st + (g,))
                seen.add(g)
            for a, b in combinations_with_replacement(vals, 2):
                for g in (a & b, a | b):
                    updated.add(st + (g,))
                    seen.add(g)
        states = updated
    return seen


def tt(n, func):
    return sum(int(bool(func(i))) << i for i in range(1 << n))


def parity(n):
    return tt(n, lambda i: i.bit_count() & 1)


def incompatible(selected, f, targets):
    return all(any(((f ^ g) >> i) & 1 for i in selected) for g in targets)


def min_antichecker(f, targets, N, maximum=4):
    for m in range(1, maximum + 1):
        for S in combinations(range(N), m):
            if incompatible(S, f, targets):
                return list(S)
    return None


def main():
    n = 6
    N = 1 << n
    t1 = easy(n, 1)
    t2 = easy(n, 2)
    s3 = easy(n, 3)
    assert len(t1) == 44 and len(t2) == 294

    yes = tt(n, lambda i: ((i & 1) and ((i >> 1) & 1)) or
                                 (((i >> 2) & 1) and ((i >> 3) & 1)))
    no = parity(n)
    assert yes in s3 and yes not in t2
    assert no not in s3
    # Six-variable parity depends on all six inputs, while any three-gate
    # fan-in-two circuit depends on at most four input variables.
    d_yes = min((yes ^ g).bit_count() for g in t1)
    d_no = min((no ^ g).bit_count() for g in t1)
    assert d_yes == 12 and d_no == 32

    S_yes = min_antichecker(yes, t1, N)
    S_no = min_antichecker(no, t1, N)
    S_parity2 = min_antichecker(no, t2, N)
    assert S_yes == [1, 2, 3, 12], S_yes
    assert S_no == [0, 1, 3], S_no
    assert S_parity2 == [0, 1, 2, 3], S_parity2
    assert min((no ^ g).bit_count() for g in t2) == 32

    # On standard AND/OR/NOT, XOR(a,b)=(a OR b) AND NOT(a AND b)
    # needs four gates. Parity on six bits needs at most 5*4=20 gates.
    seed = 20261018
    fixed_sample = {}
    rng = Random(seed)
    for m in [8, 10, 12, 14, 16, 20]:
        count = sum(incompatible(rng.sample(range(N), m), no, t2)
                    for _ in range(1500))
        fixed_sample[str(m)] = {"inconsistent": count, "trials": 1500}
    assert [fixed_sample[str(m)]["inconsistent"] for m in [8,10,12,14,16,20]] == [
        1215, 1414, 1483, 1495, 1500, 1500]

    # Bernoulli sampling demonstrates the failure even during a
    # single forward read, before target-machine composition.
    bernoulli = {}
    for p in [0.125, 0.25, 0.5]:
        rng2 = Random(seed)
        by_label = {}
        for name, f in [("source_yes", yes), ("source_no", no)]:
            bad = 0
            total = 0
            for _ in range(1000):
                S = [i for i in range(N) if rng2.random() < p]
                bad += incompatible(S, f, t1)
                total += len(S)
            by_label[name] = {
                "target_no_outputs": bad,
                "trials": 1000,
                "mean_sample_records": round(total/1000, 3),
            }
        bernoulli[str(p)] = by_label

    output = {
        "report": "MAGRED-DISTANCE-OVERLAP9",
        "status": "COMPUTATIONAL finite checks only",
        "date": "2026-10-18",
        "n": n, "N": N,
        "gate_basis": "AND/OR/NOT with fan-in <=2 and free input wires/constants",
        "size_1_target_functions": len(t1),
        "size_2_target_functions": len(t2),
        "size_3_source_functions": len(s3),
        "threshold3_to_threshold1": {
            "source_yes": "(x0 AND x1) OR (x2 AND x3)",
            "source_no": "parity6",
            "yes_min_distance": d_yes,
            "no_min_distance": d_no,
            "yes_smallest_antichecker": S_yes,
            "no_smallest_antichecker": S_no
        },
        "parity6_as_source_yes_threshold20": {
            "source_gate_upper_bound": 20,
            "target_threshold": 2,
            "target_min_distance": 32,
            "smallest_antichecker": S_parity2,
            "random_fixed_size_samples": fixed_sample
        },
        "bernoulli_samples": bernoulli,
        "seed": seed,
        "warning": "Not a proof of one-tape time bounds or hardness transport"
    }
    out = Path(__file__).resolve().with_name("MAGRED_DISTANCE_OVERLAP9_raw.json")
    out.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
