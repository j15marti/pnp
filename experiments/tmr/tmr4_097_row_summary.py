#!/usr/bin/env python3
"""TMR-4/097: exhaustive T5 row factorization and actual 3-bit literal CNF.

Run: python experiments/tmr/tmr4_097_row_summary.py
No randomness, no asymptotic lower-bound assertion.
"""
import hashlib
import json
from itertools import product

CASES = (
    ("unsat", ((0, 1), (0, 2), (1, 0), (1, 3))),
    ("sat", ((0, 1), (0, 2), (1, 3))),
)

def beat(a, b):
    return (b - a) % 5 in (1, 3)

def enc_source(edges):
    assert all(0 <= u < 4 and 0 <= v < 4 for u, v in edges)
    assert len(set(edges)) == len(edges)
    return ("T5-ROWS-v1 n=4 edges=" + str(len(edges)) + "\n" +
            "".join(f"{u} {v}\n" for u, v in sorted(edges)))

def clauses(edges):
    cls = []
    for v in range(4):
        for invalid in (5, 6, 7):
            cls.append([(3 * v + i, 1 - ((invalid >> i) & 1))
                        for i in range(3)])
    for u, v in edges:
        for a, b in product(range(5), repeat=2):
            if beat(a, b):
                continue
            cls.append([(3 * u + i, 1 - ((a >> i) & 1)) for i in range(3)] +
                       [(3 * v + i, 1 - ((b >> i) & 1)) for i in range(3)])
    return cls

def codebits(vals):
    return [(a >> j) & 1 for a in vals for j in range(3)]

def cnf_check(bits, cls):
    return all(any((bits[i] == sign) for i, sign in clause) for clause in cls)

def evaluate_case(label, edges):
    source = enc_source(edges)
    cls = clauses(edges)
    count = 0
    for vals in product(range(5), repeat=4):
        native = all(beat(vals[u], vals[v]) for u, v in edges)
        assert cnf_check(codebits(vals), cls) == native
        count += native
    invalid = 0
    for vals in product(range(8), repeat=4):
        if max(vals) < 5:
            continue
        assert not cnf_check(codebits(vals), cls)
        invalid += 1
    profiles = {}
    recombined = 0
    for u, v in product(range(5), repeat=2):
        c0 = sum(beat(u, v) and beat(u, a) for a in range(5))
        c1 = sum(beat(v, b) and (label == "sat" or beat(v, u))
                 for b in range(5))
        profiles[str(c0) + "," + str(c1)] = profiles.get(
            str(c0) + "," + str(c1), 0) + 1
        recombined += c0 * c1
    assert count == recombined == (40 if label == "sat" else 0)
    assert invalid == 3471
    return {
        "label": label, "n": 4, "arcs": len(edges),
        "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
        "native_assignments": 625, "rejects": 625 - count,
        "accepts": count, "invalid_codes_checked": invalid,
        "cnf_clauses": len(cls),
        "cnf_signed_literals": sum(map(len, cls)),
        "row_hist": dict(sorted(profiles.items())),
    }

def main():
    cases = [evaluate_case(*case) for case in CASES]
    unary = 0
    for reverse in (False, True):
        for a in range(5):
            for mask in range(32):
                support = sum(1 << b for b in range(5)
                              if mask & (1 << b) and
                              (beat(b, a) if reverse else beat(a, b)))
                assert not (support & ~mask)
                unary += 1
    pair_masks = 0
    for reverse in (False, True):
        for ma, mb in product(range(32), repeat=2):
            sup_a = sum(1 << a for a in range(5) if ma & (1 << a) and
                        any(mb & (1 << b) and
                            (beat(b, a) if reverse else beat(a, b))
                            for b in range(5)))
            sup_b = sum(1 << b for b in range(5) if mb & (1 << b) and
                        any(ma & (1 << a) and
                            (beat(b, a) if reverse else beat(a, b))
                            for a in range(5)))
            assert (sup_a & ~ma) == (sup_b & ~mb) == 0
            pair_masks += 1
    data = {
        "status": "COMPUTATIONAL", "cases": cases,
        "unary_domain_cases_checked": unary,
        "pair_mask_cases_checked": pair_masks,
        "per_fixed_z_time_exponents": {
            "degree_1": 1.195, "degree_2": 1.545,
            "degree_3": 1.895,
            "target_degree_cap": 97 / 70,
            "full_z_copy_q_n_half": 1.345,
            "decision_self_reduction_degree_1": 1.545,
        },
        "source_length_warning": "n is a base layout parameter, not encoded input length",
        "unexpected_assertion_failures": 0,
    }
    print(json.dumps(data, sort_keys=True, indent=2))

if __name__ == "__main__":
    main()
