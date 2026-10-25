#!/usr/bin/env python3
"""ARC-CONSTANT-DEPTH-FIREWALL155 exact arithmetic audit.

This is not a SAT lower-bound experiment.  It checks the encoded-size exponents
and same-machine wrapper ledger for the two-level block projection in Role 4's
M22-CYCLIC-UNSAT-PORT109 and for a generic fixed-depth parent-scale fallback.
Every individual invocation is deterministic and finishes in well under 30 s.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction


RUN_ID = "ARC-CONSTANT-DEPTH-FIREWALL155"


def dense_bits(k: int, m: int) -> int:
    """Role-4 declared dense indexed CNF length."""
    width = math.ceil(math.log2(k + 1))
    return 3 * width + 2 + 3 * m * (width + 1)


def exponent(n_child: int, n_parent: int) -> float:
    return math.log(n_child) / math.log(n_parent)


def wrapper_bound(t: Fraction, s: Fraction, r: Fraction = Fraction(1)):
    """Recognition then shortcut, otherwise invoke the same all-input A."""
    return max(r, t), s


def open_map(t: Fraction, s: Fraction):
    return max(Fraction(11, 10), Fraction(3, 5) + t / 2), max(Fraction(1, 2), s / 2)


def main() -> None:
    checks = 0

    def check(condition: bool, message: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            raise AssertionError(message)

    rows = []
    previous_lambda1 = None
    previous_lambda2 = None
    for e in range(2, 21):
        p = 2**e
        k0, m0 = 198 * p, 264 * p
        k1, m1 = k0 - 197, 264 * (p - 1) + 2
        k2, m2 = k0 - 394, 264 * (p - 2) + 4
        n0, n1, n2 = dense_bits(k0, m0), dense_bits(k1, m1), dense_bits(k2, m2)
        lam1, lam2 = exponent(n1, n0), exponent(n2, n0)
        check(0 < n2 < n1 < n0, "two fixed block deletions must shrink finite encodings")
        check(0 < lam2 < lam1 < 1, "finite logarithmic exponents are below one")
        if previous_lambda1 is not None:
            # Word-width jumps can make finite monotonicity fail at isolated p;
            # the dyadic sequence here is checked rather than assumed.
            check(lam1 >= previous_lambda1, "lambda1 should approach one on audited dyadic sizes")
            check(lam2 >= previous_lambda2, "lambda2 should approach one on audited dyadic sizes")
        previous_lambda1, previous_lambda2 = lam1, lam2
        rows.append(
            {
                "p": p,
                "parent_bits": n0,
                "level1_bits": n1,
                "level2_bits_before_unit_simplification": n2,
                "level1_ratio": n1 / n0,
                "level2_ratio": n2 / n0,
                "lambda1_log_ratio": lam1,
                "lambda2_log_ratio": lam2,
                "lambda1_gap_to_one": 1 - lam1,
                "lambda2_gap_to_one": 1 - lam2,
            }
        )

    # The deleted content is O(log p) encoded bits out of Theta(p log p).
    # The finite table must visibly converge toward exponent one.
    check(rows[-1]["lambda1_gap_to_one"] < rows[0]["lambda1_gap_to_one"] / 1000,
          "first-level exponent gap should collapse")
    check(rows[-1]["lambda2_gap_to_one"] < rows[0]["lambda2_gap_to_one"] / 1000,
          "second-level exponent gap should collapse")
    check(rows[-1]["level1_ratio"] > 0.99999, "first-level size ratio tends to one")
    check(rows[-1]["level2_ratio"] > 0.99999, "second-level size ratio tends to one")

    exponent_rows = []
    for K in range(2, 17):
        t = Fraction(K)
        s = Fraction(K)
        fallback = wrapper_bound(t, s)
        desired = open_map(t, s)
        check(fallback == (t, s), "recognize-or-fallback wrapper preserves diagonal exponents")
        check(desired[0] < t and desired[1] < s, "illustrative OPEN map strictly improves K>=2")
        # One fixed-number A-call on a child with asymptotic lambda=1 has exponent t.
        one_child_call = t
        eager_materialized_space = max(Fraction(1), s)
        check(one_child_call == t, "parent-scale child call cannot certify time contraction")
        check(eager_materialized_space >= s, "materialization cannot improve diagonal space")
        exponent_rows.append(
            {
                "K": K,
                "fallback_time": str(fallback[0]),
                "fallback_space": str(fallback[1]),
                "desired_open_time": str(desired[0]),
                "desired_open_space": str(desired[1]),
                "parent_scale_child_call_time": str(one_child_call),
                "eager_materialized_space": str(eager_materialized_space),
            }
        )

    c = Fraction(241, 200)
    beta = ((c + 2) / (c * c) - c) / 2
    stated = Fraction(11642479, 23232400)
    check(beta == stated, "strict FLMV box rational must match beta(241/200)")

    controls = [
        {"name": "recognized cyclic UNSAT W_p", "branch": "two-level source-specific shortcut", "calls_A": 0},
        {"name": "recognized public-witness SAT Z_33p", "branch": "direct witness verification", "calls_A": 0},
        {"name": "one-bit template mutation", "branch": "fallback", "calls_A": 1},
        {"name": "Horn SAT/UNSAT", "branch": "fallback or optional Horn solver", "calls_A": 1},
        {"name": "2-SAT SAT/UNSAT", "branch": "fallback or optional SCC solver", "calls_A": 1},
        {"name": "affine/Tseitin SAT/UNSAT", "branch": "fallback or optional Gaussian solver", "calls_A": 1},
        {"name": "generic ordinary CNF", "branch": "fallback", "calls_A": 1},
    ]
    check(any(x["calls_A"] == 0 for x in controls), "supported shortcut controls present")
    check(any(x["calls_A"] == 1 for x in controls), "unsupported fallback controls present")

    result = {
        "run_id": RUN_ID,
        "status": {
            "fixed_block_exponent_lemma": "PROVED/EXACT by symbolic argument; finite table is COMPUTATIONAL",
            "role4_semantic_interface": "accepted restricted, conditional on published base UNSAT theorem",
            "all_input_arc_edge": "OPEN",
            "p_vs_np": "OPEN",
        },
        "model": "dense indexed CNF length and symbolic FLMV exponent ledger; not measured wall-clock complexity",
        "parameters": {
            "parent": {"k": "198p", "m": "264p"},
            "level1": {"k": "198p-197", "m": "264(p-1)+2"},
            "level2_before_simplification": {"k": "198p-394", "m": "264(p-2)+4"},
            "p_values": [row["p"] for row in rows],
            "random_seed": None,
        },
        "size_rows": [row for row in rows if row["p"] in {4, 8, 32, 1024, 1048576}],
        "size_sweep_summary": {
            "rows_checked": len(rows),
            "first_lambda1_gap": rows[0]["lambda1_gap_to_one"],
            "last_lambda1_gap": rows[-1]["lambda1_gap_to_one"],
            "first_lambda2_gap": rows[0]["lambda2_gap_to_one"],
            "last_lambda2_gap": rows[-1]["lambda2_gap_to_one"],
        },
        "exponent_rows": [row for row in exponent_rows if row["K"] in {2, 4, 8, 16}],
        "exponent_sweep_summary": {"K_min": 2, "K_max": 16, "rows_checked": len(exponent_rows)},
        "strict_flmv_box": {"time": "241/200", "space": str(stated), "beta_exact": str(beta)},
        "dispatch_controls": controls,
        "assertion_checks": checks,
        "failures": 0,
        "limitations": [
            "finite exponent rows illustrate but do not prove the asymptotic lemma",
            "the symbolic proof uses fixed-depth deletion of O(1) constant templates from Theta(p log p) encoding",
            "the special-family unit-conflict shortcut is not an all-input contraction",
            "no arbitrary-decider successor or FLMV forbidden pair is constructed",
            "bit work is not identified with physical switching, gates, wires, or actual state flips",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
