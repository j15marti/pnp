#!/usr/bin/env python3
"""Exact arithmetic audit for FINITE-DEPTH-WIDTH-MARGIN24."""

from fractions import Fraction
import json


def audit(max_depth=32, max_k=256):
    checks = 0
    failures = []
    rows = []
    c = Fraction(1, 20)

    for r in range(1, max_depth + 1):
        root_margin = c / (2 ** r)
        first_call_exp = Fraction(1, 2) + 2 * root_margin
        checks += 1
        if first_call_exp > Fraction(3, 5):
            failures.append({"kind": "call_exponent", "depth": r})

        for j in range(r + 1):
            threshold = c / (2 ** j)
            checks += 1
            if root_margin > threshold:
                failures.append({"kind": "margin", "depth": r, "level": j})

        rows.append({
            "depth": r,
            "root_width_coefficient": f"1/{20 * (2 ** r)}",
            "first_call_exponent":
                f"{first_call_exp.numerator}/{first_call_exp.denominator}",
        })

    # N=2^(40k), w=2k: root threshold 2k; sqrt-child threshold k.
    for k in range(1, max_k + 1):
        log_n = 40 * k
        w = 2 * k
        root_threshold = log_n // 20
        child_threshold = (log_n // 2) // 20
        checks += 3
        if w > root_threshold:
            failures.append({"kind": "root_rejected", "k": k})
        if not (w > child_threshold):
            failures.append({"kind": "child_not_rejected", "k": k})
        if child_threshold != k:
            failures.append({"kind": "threshold_arithmetic", "k": k})

    # Concrete proper-3CNF persistent frontiers.
    concrete_cases = 0
    for w in range(3, 65):
        for blocks in range(2, 18):
            clauses = [
                tuple(((i + d) % w) + 1 for d in range(3))
                for _block in range(blocks)
                for i in range(w)
            ]
            checks += 1
            concrete_cases += 1
            if any(len(set(clause)) != 3 for clause in clauses):
                failures.append({
                    "kind": "improper_clause", "w": w, "blocks": blocks
                })
            per_block = [
                clauses[b * w:(b + 1) * w] for b in range(blocks)
            ]
            for block in per_block:
                seen = {v for clause in block for v in clause}
                if seen != set(range(1, w + 1)):
                    failures.append({
                        "kind": "frontier_not_persistent",
                        "w": w,
                        "blocks": blocks,
                    })

    return {
        "run": "FINITE-DEPTH-WIDTH-MARGIN24",
        "status": "PASS" if not failures else "FAIL",
        "checks": checks,
        "failures": failures,
        "depth_range": [1, max_depth],
        "persistent_frontier_k_range": [1, max_k],
        "concrete_persistent_frontier_cases": concrete_cases,
        "rows": rows,
        "random_seed": None,
        "scope":
            "exact exponent and frontier arithmetic; not an all-input SAT contractor",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
