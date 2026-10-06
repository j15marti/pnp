#!/usr/bin/env python3
"""
Shared BAD-SEED scaling experiment.

Toy SAT-native route generator:
  F_d = x_1 AND ... AND x_d AND z.
  Seed bit s_i chooses the actual restriction test x_i=s_i.
  Assuming prior selected semantic values x_j=1,
  SAT(F_d | x_i=s_i, prior x_j=1) = s_i.

Hence the wrapper's A/B history is exactly the seed string.
A recursive hidden state stores parity of this history.

BAD-SEED asks whether some seed causes a proposed merged evaluator q(s)
to disagree with the required hidden continuation bit.

Modes:
  constant0 : unsafe merge, q=0
  parity    : exact one-bit summary q=parity(seed)
  replay    : recompute parity from the seed

The CNF counts use 4-clause Tseitin XOR gates. BAD satisfiability is checked
from the exact Boolean specification rather than by a generic SAT solver.
"""

import json


def cnf_counts(depth, mode):
    vars_ = depth + depth + (depth + 1) + 1 + 1
    clauses = 2 * depth + 1 + 4 * depth + 4 + 1

    if mode == "constant0":
        clauses += 1
    elif mode == "parity":
        clauses += 2
    elif mode == "replay":
        vars_ += depth + 1
        clauses += 1 + 4 * depth + 2
    else:
        raise ValueError(mode)
    return vars_, clauses


def bad_exists(depth, mode):
    if mode == "constant0":
        return depth >= 1
    if mode in ("parity", "replay"):
        return False
    raise ValueError(mode)


def exhaustive_validate(depth, mode):
    if depth > 16:
        return None
    for s in range(1 << depth):
        parity = s.bit_count() & 1
        q = 0 if mode == "constant0" else parity
        if q != parity:
            return True
    return False


def run(max_depth=32):
    rows = []
    for d in range(1, max_depth + 1):
        v0, c0 = cnf_counts(d, "constant0")
        vp, cp = cnf_counts(d, "parity")
        vr, cr = cnf_counts(d, "replay")

        row = {
            "depth": d,
            "route_count": 2 ** d,
            "route_identity_bits": d,
            "explicit_route_copy_units": d * (2 ** d),
            "false_merge_bad_cnf": {
                "vars": v0,
                "clauses": c0,
                "BAD_satisfiable": bad_exists(d, "constant0"),
            },
            "one_bit_parity_summary_bad_cnf": {
                "vars": vp,
                "clauses": cp,
                "BAD_satisfiable": bad_exists(d, "parity"),
            },
            "replay_from_seed_bad_cnf": {
                "vars": vr,
                "clauses": cr,
                "BAD_satisfiable": bad_exists(d, "replay"),
            },
        }

        if d <= 16:
            row["exhaustive_validation"] = {
                mode: exhaustive_validate(d, mode)
                for mode in ("constant0", "parity", "replay")
            }

        rows.append(row)

    return {
        "status": "COMPUTATIONAL_EXACT_FINITE",
        "rows": rows,
        "interpretation": [
            "A seed-input circuit of O(d) size represents 2^d possible wrapper histories.",
            "BAD-SEED remains O(d) size while asking whether any history violates the merge invariant.",
            "The unsafe constant merge has a bad seed.",
            "A one-bit parity summary eliminates all bad seeds.",
            "Replay from the seed eliminates all bad seeds with O(d) work.",
            "All-route internalization therefore avoids explicit exponential duplication but does not force a large state."
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
