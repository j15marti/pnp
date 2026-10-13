#!/usr/bin/env python3
"""Independent bounded audit for ALLFIELD22.

Checks only finite/symbolic identities used by the red-team report.  It does
not execute the N^615 enumerator or infer any asymptotic SAT lower bound.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import time


SEED = 131113


def neutral_slot_counts():
    # Variables are (external, a, b, c, d, e); literals use signed indices.
    clauses = [
        (1, 2, 3),
        (2, -4, -5),
        (-2, 4, -6),
        (-2, 5, 6),
        (3, -4, -5),
        (-3, 4, -6),
        (-3, 5, 6),
    ]
    occurrence = {i: [0, 0] for i in range(2, 7)}
    for clause in clauses:
        assert len({abs(x) for x in clause}) == 3
        for lit in clause:
            if abs(lit) >= 2:
                occurrence[abs(lit)][lit < 0] += 1
    assert all(v == [2, 2] for v in occurrence.values())

    counts = []
    all_one_works = []
    for ext in (0, 1):
        count = 0
        for aux in itertools.product((0, 1), repeat=5):
            assignment = (ext,) + aux
            ok = all(any((assignment[abs(lit) - 1] == 1) if lit > 0
                         else (assignment[abs(lit) - 1] == 0)
                         for lit in clause) for clause in clauses)
            count += int(ok)
        counts.append(count)
        all_one = (ext, 1, 1, 1, 1, 1)
        all_one_works.append(all(any((all_one[abs(lit) - 1] == 1) if lit > 0
                                     else (all_one[abs(lit) - 1] == 0)
                                     for lit in clause) for clause in clauses))
    assert counts == [8, 14]
    assert all(all_one_works)
    return {"conditional_models_external_0_1": counts,
            "internal_signed_occurrences": occurrence,
            "all_internal_one_extends_both": True}


def deficit_identities():
    cases = 0
    max_ratio = 0
    for p in range(13):
        for q in range(13):
            if p + q == 0:
                continue
            r = max(p, q, 2)
            d = p + q
            deficit = 2 * r - d
            assert 0 <= deficit <= 3 * d
            max_ratio = max(max_ratio, deficit / d)
            # One neutral gadget adds 7 clauses and 10 occurrences of each sign.
            R0 = r
            R = R0 + 10 * deficit
            m = d / 3
            assert 6 * R == 9 * m + 63 * deficit
            assert 8 * R == 12 * m + 84 * deficit
            cases += 1
    return {"occurrence_pairs": cases, "max_deficit_over_degree": max_ratio}


def transformed_inequality(values, lower, complement_mask):
    # Original sum x_i >= lower, substitute x_i = y_i or 1-y_i.
    coefficients = []
    shift = 0
    for i in range(len(values)):
        if (complement_mask >> i) & 1:
            coefficients.append(-1)
            shift += 1
        else:
            coefficients.append(1)
    rhs = lower - shift
    lhs = sum(a * y for a, y in zip(coefficients, values))
    original = [1 - y if (complement_mask >> i) & 1 else y
                for i, y in enumerate(values)]
    return lhs >= rhs, sum(original) >= lower, coefficients, rhs


def complement_audit():
    checks = 0
    rhs_values = set()
    for degree, lower in ((4, 2), (5, 3)):
        for mask in range(1 << degree):
            for values in itertools.product((0, 1), repeat=degree):
                got, expected, _, rhs = transformed_inequality(values, lower, mask)
                assert got == expected
                assert -5 <= rhs <= 5
                rhs_values.add(rhs)
                checks += 1
    # Right constraints sum x_i <= 2 are -sum x_i >= -2.
    for degree in (4, 5):
        for mask in range(1 << degree):
            for values in itertools.product((0, 1), repeat=degree):
                got_pos, expected_pos, coeff, rhs_pos = transformed_inequality(values, 2, mask)
                # Negate the left expression for the <= constraint directly.
                original = [1 - y if (mask >> i) & 1 else y
                            for i, y in enumerate(values)]
                rhs = -2 + mask.bit_count()
                lhs = sum(-a * y for a, y in zip(coeff, values))
                assert (lhs >= rhs) == (sum(original) <= 2)
                assert -5 <= rhs <= 5
                rhs_values.add(rhs)
                checks += 1
    return {"truth_table_checks": checks, "rhs_min": min(rhs_values),
            "rhs_max": max(rhs_values)}


def cyclic_graph(q):
    # 4-regular simple bipartite graph: shifts 0,1,2,3; q >= 5.
    return {(u, (u + shift) % q) for u in range(q) for shift in range(4)}


def cancellation_audit():
    checks = 0
    digests = []
    for q in (5, 6, 8, 12, 20):
        edges = cyclic_graph(q)
        extra = (0, (0 + 4) % q)
        assert extra not in edges
        edges.add(extra)
        ordered = sorted(edges)
        # Deterministic complement pattern, independent of graph layout.
        complement = {e: ((17 * e[0] + 31 * e[1] + SEED) & 1) for e in ordered}
        coefficient_sum = {e: 0 for e in ordered}
        rhs_sum = 0
        for u in range(q):
            inc = [e for e in ordered if e[0] == u]
            lower = max(len(inc) - 2, 0)
            rhs_sum += lower - sum(complement[e] for e in inc)
            for e in inc:
                coefficient_sum[e] += -1 if complement[e] else 1
        for v in range(q):
            inc = [e for e in ordered if e[1] == v]
            rhs_sum += -2 + sum(complement[e] for e in inc)
            for e in inc:
                coefficient_sum[e] += 1 if complement[e] else -1
        assert all(value == 0 for value in coefficient_sum.values())
        assert rhs_sum == 1
        assert len(ordered) == 4 * q + 1
        digests.append(hashlib.sha256(repr((q, ordered, complement)).encode()).hexdigest()[:16])
        checks += len(ordered) + 2
    return {"graphs": 5, "coefficient_and_rhs_checks": checks,
            "instance_digests": digests}


def support_bound_audit():
    rows = []
    for degree in (4, 5):
        source_clauses = 4 if degree == 4 else 10
        max_clones_per_edge = 6
        implications = degree * max_clones_per_edge
        q_copies_worst = implications  # adversarial triple grouping: one selected port per Q.
        total = source_clauses + implications + 19 * q_copies_worst
        assert total <= 610
        rows.append({"source_degree": degree, "source_clauses": source_clauses,
                     "implications": implications, "Q_copies_worst": q_copies_worst,
                     "support_clauses": total})
    assert max(r["support_clauses"] for r in rows) == 610
    # A selected subformula has <= 3*610 variables; the queried inequality adds <=5.
    assignment_bound_exponent = 3 * 610 + 5
    assert assignment_bound_exponent == 1835
    return {"rows": rows, "truth_table_assignment_bound": f"2^{assignment_bound_exponent}",
            "candidate_pair_bound": "O((M+1)^610 (v+1)^5)"}


def axiom_repair_audit():
    checks = 0
    for modulus in (2, 3, 5, 7):
        for x in range(modulus):
            for xbar in range(modulus):
                # PCR repair x*xbar = x*(x+xbar-1) - (x^2-x).
                assert (x * xbar) % modulus == (
                    x * (x + xbar - 1) - (x * x - x)
                ) % modulus
                # Padded equality implication after port -> 0.
                assert (x * (1 - x)) % modulus == (-(x * x - x)) % modulus
                checks += 2
    return {"fields": [2, 3, 5, 7], "identity_checks": checks}


def main():
    started = time.perf_counter()
    result = {
        "run_id": "REDTEAM-STRENGTHEN8",
        "status": "COMPUTATIONAL supporting exact finite identities",
        "p_vs_np": "OPEN",
        "seed": SEED,
        "neutral_slot": neutral_slot_counts(),
        "deficit": deficit_identities(),
        "complementation": complement_audit(),
        "cancellation": cancellation_audit(),
        "support_bound": support_bound_audit(),
        "axiom_repairs": axiom_repair_audit(),
        "limitations": [
            "Does not execute the full 610-clause enumerator or rational LP.",
            "Does not test the asymptotic expander hypothesis or proof-size lower bound.",
            "Does not construct an all-input PRE-A successor or a SAT lower bound."
        ],
    }
    result["elapsed_seconds"] = round(time.perf_counter() - started, 6)
    semantic = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["semantic_sha256"] = hashlib.sha256(semantic.encode()).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
