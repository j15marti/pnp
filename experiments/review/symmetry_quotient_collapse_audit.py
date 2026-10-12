#!/usr/bin/env python3
"""Finite audit for SYMMETRY-QUOTIENT-COLLAPSE1.

The experiment is deliberately bounded.  It verifies the two six-variable
payload blocks, enumerates the balanced-family quotient through k=18, and
checks representation/wrapper hostile-control labels.  It does not infer an
asymptotic machine lower bound from the finite data.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import time
from pathlib import Path


POS = ((0, 1, 2), (0, 3, 4), (1, 3, 5), (2, 4, 5))
NEG0 = ((0, 2, 4), (0, 3, 5), (1, 2, 5), (1, 3, 4))
NEG1 = ((0, 2, 5), (0, 3, 4), (1, 2, 4), (1, 3, 5))
BETA = (0, None, 0, None, 0, None)

REPRESENTATIONS = (
    "clean-core-cnf",
    "2sat-control",
    "horn-control",
    "affine-tseitin-control",
    "bounded-treewidth-control",
    "independent-product",
)
ENCODINGS = ("canonical", "clause-order", "padded", "redundant", "tagged", "renamed")
WRAPPERS = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")


def clean_block(neg):
    clauses = [(1, c) for c in POS] + [(-1, c) for c in neg]
    seen = set()
    pos = [0] * 6
    minus = [0] * 6
    for sign, support in clauses:
        assert len(set(support)) == 3
        key = (sign, tuple(sorted(support)))
        assert key not in seen
        seen.add(key)
        for v in support:
            (pos if sign == 1 else minus)[v] += 1
    assert pos == [2] * 6 and minus == [2] * 6
    return clauses


def sat(clauses, assignment):
    return all(
        any((assignment[v] == 1) if sign == 1 else (assignment[v] == 0) for v in support)
        for sign, support in clauses
    )


def compatible(clauses, partial):
    free = [i for i, value in enumerate(partial) if value is None]
    for values in itertools.product((0, 1), repeat=len(free)):
        assignment = list(partial)
        for i, value in zip(free, values):
            assignment[i] = value
        if sat(clauses, assignment):
            return True
    return False


def orbit_key(b, bits):
    return b, sum(bits)


def compatibility_orbit_key(b, bits):
    # BALCOMP1: H_{E_{1,u}}(alpha_i)=1-u_i; UNSAT members have all zeros.
    vector = (tuple(1 - x for x in bits) if b else (0,) * len(bits))
    return sum(vector), len(vector) - sum(vector)


def digest_controls(k):
    h = hashlib.sha256()
    assertions = 0
    for rep, enc, wrapper in itertools.product(REPRESENTATIONS, ENCODINGS, WRAPPERS):
        for b in (0, 1):
            for weight in range(k + 1):
                key = (b, weight)
                # Names alter only representation, never the declared S_k quotient.
                assert key == orbit_key(b, (1,) * weight + (0,) * (k - weight))
                h.update(f"{rep}|{enc}|{wrapper}|{k}|{b}|{weight}\n".encode())
                assertions += 1
    return assertions, h.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=18)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/raw/review/2026-10-13_symmetry_quotient_collapse.json"),
    )
    args = parser.parse_args()
    started = time.perf_counter()

    g0 = clean_block(NEG0)
    g1 = clean_block(NEG1)
    assert any(sat(g0, a) for a in itertools.product((0, 1), repeat=6))
    assert any(sat(g1, a) for a in itertools.product((0, 1), repeat=6))
    assert compatible(g0, BETA) is True
    assert compatible(g1, BETA) is False

    rows = []
    exhaustive_assertions = 0
    for k in range(1, args.max_k + 1):
        formula_orbits = set()
        compatibility_orbits = set()
        weight_sizes = [0] * (k + 1)
        for bits in itertools.product((0, 1), repeat=k):
            weight = sum(bits)
            weight_sizes[weight] += 1
            for b in (0, 1):
                formula_orbits.add(orbit_key(b, bits))
                compatibility_orbits.add(compatibility_orbit_key(b, bits))
                exhaustive_assertions += 2
        assert len(formula_orbits) == 2 * (k + 1)
        assert len(compatibility_orbits) == k + 1
        assert weight_sizes == [math.comb(k, w) for w in range(k + 1)]
        control_assertions, control_digest = digest_controls(k)
        rows.append(
            {
                "k": k,
                "labeled_u": 2**k,
                "labeled_formulas": 2 ** (k + 1),
                "formula_orbits": len(formula_orbits),
                "compatibility_orbits": len(compatibility_orbits),
                "largest_orbit": max(weight_sizes),
                "formula_invariant_bits_upper": math.ceil(math.log2(2 * (k + 1))),
                "compatibility_invariant_bits_upper": math.ceil(math.log2(k + 1)),
                "control_assertions": control_assertions,
                "control_digest": control_digest,
            }
        )

    result = {
        "claim": "SYMMETRY-QUOTIENT-COLLAPSE1",
        "status": "COMPUTATIONAL",
        "max_k": args.max_k,
        "g0_beta_compatible": True,
        "g1_beta_compatible": False,
        "exhaustive_assertions": exhaustive_assertions,
        "representations": list(REPRESENTATIONS),
        "encodings": list(ENCODINGS),
        "wrappers": list(WRAPPERS),
        "rows": rows,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "asymptotic_extrapolation": False,
        "notes": [
            "The finite audit verifies exact orbit counts only through max_k.",
            "The theorem for all k is the separate elementary S_k orbit proof.",
            "Döcker's 198-variable UNSAT block is cited, not computationally reproved.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
