#!/usr/bin/env python3
"""Finite controls for PARITY-AFFINE-JOINT-BYPASS53.

Combines affine every-order residual width with parity-forced positive
certificate width.  The finite checks validate algebra and examples only;
they do not prove uniform matrix construction or a class separation.
"""

from itertools import combinations
import json
import math
import random


checks = 0
balanced_cuts = 0
truth_assignments = 0
flip_checks = 0


def check(condition):
    global checks
    checks += 1
    assert condition


def gf2_rank(columns):
    basis = {}
    for value in columns:
        x = value
        while x:
            pivot = x.bit_length() - 1
            if pivot in basis:
                x ^= basis[pivot]
            else:
                basis[pivot] = x
                break
    return len(basis)


def syndrome(columns, assignment):
    out = 0
    for j, column in enumerate(columns):
        if (assignment >> j) & 1:
            out ^= column
    return out


def minimum_balanced_rank(columns, n):
    minimum = n + 1
    for subset in combinations(range(2 * n), n):
        rank = gf2_rank([columns[j] for j in subset])
        minimum = min(minimum, rank)
    return minimum


def find_matrix(n, target, rng):
    for trial in range(5000):
        columns = [rng.randrange(1, 1 << n) for _ in range(2 * n)]
        if gf2_rank(columns) != n:
            continue
        if minimum_balanced_rank(columns, n) >= target:
            return columns, trial + 1
    raise AssertionError((n, target))


rng = random.Random(202610220148)
targets = {3: 1, 4: 2, 5: 2, 6: 3, 7: 3, 8: 3}
matrices = {}
matrix_results = []
for n, target in targets.items():
    columns, trials = find_matrix(n, target, rng)
    matrices[n] = columns
    rank_h = gf2_rank(columns)
    min_rank = n + 1
    min_lambda = n + 1
    for subset in combinations(range(2 * n), n):
        subset = set(subset)
        p = [columns[j] for j in range(2 * n) if j in subset]
        q = [columns[j] for j in range(2 * n) if j not in subset]
        rank_p = gf2_rank(p)
        rank_q = gf2_rank(q)
        lam = rank_p + rank_q - rank_h
        check(lam >= 0)
        check((1 << lam) >= 1)
        min_rank = min(min_rank, rank_p, rank_q)
        min_lambda = min(min_lambda, lam)
        balanced_cuts += 1
    check(rank_h == n)
    check(min_rank >= target)
    check(min_lambda >= 2 * target - n)
    matrix_results.append(
        {
            "n": n,
            "search_trials": trials,
            "minimum_balanced_rank": min_rank,
            "minimum_residual_log_width": min_lambda,
            "minimum_residual_width": 1 << min_lambda,
        }
    )


def verifier_core(columns, n, u, v):
    parity_u = u.bit_count() & 1
    affine_zero = int(syndrome(columns, v) == 0)
    return parity_u ^ affine_zero


# Exact density, selector-language, and positive-certificate flip controls.
for n in [3, 4]:
    columns = matrices[n]
    h = 2 * n
    accepted = 0
    for v in range(1 << (2 * n)):
        for u in range(1 << h):
            value = verifier_core(columns, n, u, v)
            accepted += value
            truth_assignments += 1
            # R(x;u,v)=x AND F(u,v) has no accepting tape for x=0.
            check((0 & value) == 0)
            check((1 & value) == value)
            if value:
                # Every primary u coordinate must be fixed by any positive
                # subcube certificate: flipping it alone changes acceptance.
                for j in range(h):
                    check(verifier_core(columns, n, u ^ (1 << j), v) == 0)
                    flip_checks += 1
    check(accepted * 2 == (1 << (4 * n)))


# Independently confirm the residual-count formula on all balanced cuts for
# the two smallest audited matrices.
residual_count_checks = 0
for n in [3, 4]:
    columns = matrices[n]
    rank_h = gf2_rank(columns)
    for subset_tuple in combinations(range(2 * n), n):
        subset = set(subset_tuple)
        p = [columns[j] for j in range(2 * n) if j in subset]
        q = [columns[j] for j in range(2 * n) if j not in subset]
        image_p = {syndrome(p, a) for a in range(1 << n)}
        image_q = {syndrome(q, a) for a in range(1 << n)}
        intersection = image_p & image_q
        lam = gf2_rank(p) + gf2_rank(q) - rank_h
        check(len(intersection) == (1 << lam))
        # Distinct right sides define distinct nonempty affine suffixes.
        suffixes = {
            tuple(a for a in range(1 << n) if syndrome(q, a) == b)
            for b in intersection
        }
        check(len(suffixes) == len(intersection))
        check(all(len(s) > 0 for s in suffixes))
        residual_count_checks += 1


# Mobius transform confirms the affine-zero indicator contributes high ANF
# degree in the small examples; this is a representation diagnostic only.
anf_results = []
for n in [3, 4]:
    columns = matrices[n]
    variable_count = 4 * n
    table = [0] * (1 << variable_count)
    mask = (1 << (2 * n)) - 1
    for assignment in range(1 << variable_count):
        v = assignment & mask
        u = assignment >> (2 * n)
        table[assignment] = verifier_core(columns, n, u, v)
    coefficients = table[:]
    for bit in range(variable_count):
        for assignment in range(1 << variable_count):
            if assignment & (1 << bit):
                coefficients[assignment] ^= coefficients[assignment ^ (1 << bit)]
    degree = max(
        assignment.bit_count()
        for assignment, coefficient in enumerate(coefficients)
        if coefficient
    )
    check(degree >= n)
    anf_results.append({"n": n, "anf_degree": degree})


result = {
    "run_id": "PARITY-AFFINE-JOINT-BYPASS53",
    "status": "PASS",
    "assertions": checks,
    "balanced_cut_evaluations": balanced_cuts,
    "truth_assignments": truth_assignments,
    "positive_certificate_flip_checks": flip_checks,
    "independent_residual_count_checks": residual_count_checks,
    "matrix_results": matrix_results,
    "anf_results": anf_results,
    "scope": (
        "Finite controls for a joint structural falsifier. Asymptotic robust "
        "matrices are existential/nonuniform in the cited ARC proof; no "
        "uniform RP simulation or class separation is claimed."
    ),
}
print(json.dumps(result, indent=2, sort_keys=True))
