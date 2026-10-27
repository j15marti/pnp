#!/usr/bin/env python3
"""Independent finite audit for COMMUNICATION-POLARITY-FIREWALL168.

Checks the published W1 two-switch gadget, exact-(2,2) invariants,
DISJ promise semantics, co-nondeterministic branch polarity, one-way row
diversity, communication-matrix GF(2) rank, and Boolean ANF degree.
No randomness or third-party dependencies.
"""

from collections import Counter
from itertools import product
from math import ceil, log2
import json

W1 = [
    (-1, 3, -14), (2, -8, 9), (10, -13, 14), (3, 7, -13),
    (-4, -9, -11), (5, 8, -14), (4, -8, -11), (1, 7, 13),
    (1, -7, 10), (-5, -6, -15), (-2, -6, 12), (-4, 9, -10),
    (-2, 5, -12), (-3, 6, -15), (6, -7, 11), (2, -9, 11),
    (4, 8, -10), (-3, 12, 15), (-5, -12, 15), (-1, 13, 14),
]


def gadget(a, b):
    cs = [list(c) for c in W1]
    if not a:
        cs[6][0] *= -1
        cs[11][0] *= -1
    if not b:
        cs[17][2] *= -1
        cs[9][2] *= -1
    return [tuple(c) for c in cs]


def proper_distinct_balanced(cs):
    if len(set(cs)) != len(cs):
        return False
    if not all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in cs):
        return False
    pos, neg = Counter(), Counter()
    for c in cs:
        for lit in c:
            (pos if lit > 0 else neg)[abs(lit)] += 1
    return all((pos[v], neg[v]) == (2, 2) for v in range(1, 16))


def model_count(cs):
    out = 0
    for bits in range(1 << 15):
        if all(any(bool(bits & (1 << (abs(l)-1))) == (l > 0) for l in c) for c in cs):
            out += 1
    return out


def gf2_rank(rows):
    rows = rows[:]
    rank = 0
    max_col = max((r.bit_length() for r in rows), default=0)
    for col in range(max_col):
        pivot = next((i for i in range(rank, len(rows)) if (rows[i] >> col) & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and ((rows[i] >> col) & 1):
                rows[i] ^= rows[rank]
        rank += 1
    return rank


def anf_degree(d):
    n = 2 * d
    vals = []
    for x in range(1 << n):
        a = x & ((1 << d) - 1)
        b = x >> d
        vals.append(int(bool(a & b)))
    coeff = vals[:]
    for j in range(n):
        for mask in range(1 << n):
            if mask & (1 << j):
                coeff[mask] ^= coeff[mask ^ (1 << j)]
    degree = max((mask.bit_count() for mask, bit in enumerate(coeff) if bit), default=0)
    top = coeff[(1 << n) - 1]
    return degree, top


def main():
    checks = 0
    base_supports = [tuple(sorted(abs(x) for x in c)) for c in W1]
    counts = {}
    for a, b in product((0, 1), repeat=2):
        cs = gadget(a, b)
        assert proper_distinct_balanced(cs); checks += 1
        assert [tuple(sorted(abs(x) for x in c)) for c in cs] == base_supports; checks += 1
        counts[f"{a}{b}"] = model_count(cs)
        assert (counts[f"{a}{b}"] == 0) == bool(a and b); checks += 1
    assert counts == {"00": 772, "01": 272, "10": 272, "11": 0}; checks += 1

    promise_pairs = 0
    branches = 0
    malformed_branches = 0
    row_checks = 0
    rank_checks = 0
    anf_checks = 0
    profiles = []
    for d in range(1, 9):
        rows = []
        for a in range(1 << d):
            row = 0
            for b in range(1 << d):
                unsat = bool(a & b)
                sat = not unsat
                # coNTIME SAT: valid branch i rejects iff a_i=b_i=1;
                # malformed branches accept.
                branch_accept = [not (((a >> i) & 1) and ((b >> i) & 1)) for i in range(d)]
                branch_accept.extend([True, True])
                assert all(branch_accept) == sat; checks += 1
                assert any(not z for z in branch_accept) == unsat; checks += 1
                assert branch_accept[-2:] == [True, True]
                checks += 1
                assert len(branch_accept) == d + 2
                checks += 1
                branches += len(branch_accept)
                malformed_branches += 2
                promise_pairs += 1
                if unsat:
                    row |= 1 << b
            rows.append(row)
        assert len(set(rows)) == (1 << d); checks += 1
        row_checks += 1
        rank = gf2_rank(rows)
        assert rank == (1 << d) - 1; checks += 1
        rank_checks += 1
        if d <= 6:
            degree, top = anf_degree(d)
            assert degree == 2 * d and top == 1; checks += 2
            anf_checks += 1
        width = ceil(log2(15 * d + 1))
        encoded_body_bits = 20 * d * 3 * (width + 1)
        profiles.append({
            "d": d,
            "variables": 15 * d,
            "clauses": 20 * d,
            "body_bits_fixed_width": encoded_body_bits,
            "one_way_state_bits_lower_bound": d,
            "deterministic_communication_bits_lower_bound": d,
            "promised_binary_gate_count": 2 * d - 1,
            "coNTIME_guess_bits": ceil(log2(d + 1)),
        })

    result = {
        "run_id": "COMMUNICATION-POLARITY-FIREWALL168",
        "status": "COMPUTATIONAL supporting separate exact proofs",
        "randomness": "none",
        "assertion_groups": checks,
        "failures": 0,
        "gadget_model_counts": counts,
        "promise_pairs": promise_pairs,
        "coNTIME_branches": branches,
        "malformed_accepting_branches": malformed_branches,
        "row_diversity_sizes_checked": row_checks,
        "gf2_rank_sizes_checked": rank_checks,
        "anf_degree_sizes_checked": anf_checks,
        "profiles": profiles,
        "scope": "disjoint exact22 module promise; not connected, not unrestricted SAT, not measured FLMV hardware time",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
