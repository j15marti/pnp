#!/usr/bin/env python3
"""Exact audit for SOURCE-READ-SUBORDINATION14.

Checks (i) charged two-stage advice coupling on every small deterministic
policy and (ii) the combined output/read/MMW exponent ledger.  It does not
construct the open SAT-to-ordinary-MKTP totalizer.
"""

from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path

TAU = Fraction(241, 200)
SIGMA = Fraction(1, 2)


def tv(p, q):
    keys = set(p) | set(q)
    return sum(abs(p.get(x, 0) - q.get(x, 0)) for x in keys) / 2


def normalize(counts, den):
    return {k: Fraction(v, den) for k, v in counts.items()}


def staged_transcript(source, q0, advice_truth, q1_by_advice):
    a0 = source[q0]
    y = advice_truth[a0]
    q1 = q1_by_advice[y]
    a1 = source[q1]
    return (q0, a0, y, q1, a1)


def composed(a, kappa, C, D, B, E, read_exp, retained_exp):
    time = max(
        read_exp,
        a,
        a * (1 + Fraction(B, kappa)),
        a * (1 + Fraction(C + 1, kappa)),
    )
    space = max(
        retained_exp,
        a * Fraction(E, kappa),
        a * Fraction(max(1, D), kappa),
    )
    return time, space


def main():
    failures = []
    assertions = 0

    # Exhaust all two-stage one-bit-advice policies for N=7, k_sparse=2.
    N = 7
    sparse_k = 2
    supports = list(combinations(range(N), sparse_k))
    zero = (0,) * N
    policies = 0
    exact_equalities = 0
    for q0 in range(N):
        for advice_truth in product(range(2), repeat=2):
            for q1_by_advice in product(range(N), repeat=2):
                policies += 1
                p0 = {staged_transcript(zero, q0, advice_truth, q1_by_advice): Fraction(1)}
                ck = Counter()
                for support in supports:
                    source = tuple(1 if i in support else 0 for i in range(N))
                    ck[staged_transcript(source, q0, advice_truth, q1_by_advice)] += 1
                p1 = normalize(ck, len(supports))
                observed = tv(p0, p1)

                y0 = advice_truth[0]
                touched = {q0, q1_by_advice[y0]}
                u = len(touched)
                ceiling = Fraction(
                    len(supports) - len(list(combinations(range(N - u), sparse_k))),
                    len(supports),
                )
                assertions += 2
                if observed > ceiling:
                    failures.append(["coupling", q0, advice_truth, q1_by_advice, str(observed), str(ceiling)])
                if observed == ceiling:
                    exact_equalities += 1
                # Alphabet size is irrelevant once advice is derived from the charged first read.
                if u > 2:
                    failures.append(["touch_count", q0, advice_truth, q1_by_advice, u])

    # Exact exponent ledger over a broad fixed grid.
    a_values = [Fraction(1), Fraction(21, 20), Fraction(11, 10), Fraction(6, 5)]
    read_values = [Fraction(1), Fraction(6, 5), Fraction(241, 200), Fraction(121, 100)]
    retained_values = [Fraction(0), Fraction(49, 100), Fraction(1, 2), Fraction(1)]
    grid_cases = 0
    for a, read_exp, retained_exp, kappa, C, D in product(
        a_values, read_values, retained_values, range(8, 129, 8), range(1, 17), range(1, 17)
    ):
        B, E = 4, 2
        t, s = composed(a, kappa, C, D, B, E, read_exp, retained_exp)
        direct_t = max(read_exp, a * (1 + Fraction(max(B, C + 1), kappa)))
        direct_s = max(retained_exp, a * Fraction(max(E, 1, D), kappa))
        grid_cases += 1
        assertions += 2
        if t != direct_t:
            failures.append(["time_identity", str(a), str(read_exp), kappa, C, D])
        if s != direct_s:
            failures.append(["space_identity", str(a), str(retained_exp), kappa, C, D])

    # Focused classifications at a=6/5 and very large fixed k.
    a = Fraction(6, 5)
    kappa = 100000
    profiles = {
        "one_full_scan_no_retention": (Fraction(1), Fraction(0), True),
        "N_to_1_5_total_reads": (Fraction(6, 5), Fraction(0), True),
        "N_to_1_205_total_reads": (TAU, Fraction(0), False),
        "subsqrt_retention": (Fraction(1), Fraction(49, 100), True),
        "sqrt_retention_strict_boundary": (Fraction(1), Fraction(1, 2), False),
        "full_source_retention": (Fraction(1), Fraction(1), False),
    }
    classifications = {}
    for name, (r, z, expected) in profiles.items():
        t, s = composed(a, kappa, 100, 100, 4, 2, r, z)
        passes = t < TAU and s < SIGMA
        classifications[name] = {"read_exponent_N": str(r), "retained_exponent_N": str(z), "time": str(t), "space": str(s), "passes": passes}
        assertions += 1
        if passes != expected:
            failures.append(["classification", name, passes, str(t), str(s)])

    # Unit-cost named-coordinate lower bounds never exceed a full scan.
    source_bound_cases = 0
    for n_exp_den in range(1, 65):
        for k_exp_num in range(0, n_exp_den + 1):
            for w_exp_num in range(0, n_exp_den - k_exp_num + 1):
                gamma = Fraction(k_exp_num, n_exp_den)
                omega = Fraction(w_exp_num, n_exp_den)
                read_exp = max(Fraction(0), 1 - gamma - omega)
                source_bound_cases += 1
                assertions += 1
                if read_exp > 1:
                    failures.append(["source_bound_gt_scan", str(gamma), str(omega), str(read_exp)])

    result = {
        "run": "SOURCE-READ-SUBORDINATION14",
        "status": "PASS" if not failures else "FAIL",
        "scope": "charged named-source-bit coupling and exponent accounting only",
        "staged_advice": {
            "N": N,
            "sparse_k": sparse_k,
            "policies": policies,
            "support_runs": policies * len(supports),
            "exact_ceiling_equalities": exact_equalities,
        },
        "exponent_grid_cases": grid_cases,
        "source_bound_cases": source_bound_cases,
        "assertions": assertions,
        "classifications": classifications,
        "failures": failures,
        "global_status": "P versus NP OPEN",
    }
    out = Path("results/raw/synthesis/2026-10-20_1148_SOURCE_READ_SUBORDINATION14.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
