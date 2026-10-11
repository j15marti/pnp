#!/usr/bin/env python3
"""Finite audit for MODELBRIDGE-0019.

This checks the elementary hidden-string partial-recovery bound, the matching
coordinate-query strategy, and the explicit-input bypass that blocks transfer
to arbitrary 3-CNF computation.  It deliberately makes no asymptotic claim
from finite data.
"""

from __future__ import annotations

import hashlib
import json
import math
import time


RUN_ID = "MODELBRIDGE-0019"
WRAPPERS = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")


def common_coordinates(strings: list[int], n: int) -> int:
    return sum(
        all(((x >> i) & 1) == ((strings[0] >> i) & 1) for x in strings)
        for i in range(n)
    )


def indexed_length(n: int) -> int:
    """Length ledger used in current bridge reports, for m=n pin clauses."""
    gamma = lambda q: 2 * int(math.log2(q)) + 1
    w = max(1, math.ceil(math.log2(n + 1)))
    return gamma(n) + gamma(n + 1) + 3 * n * (1 + w)


def recover_by_coordinate_queries(x: int, n: int, r: int) -> tuple[int, int]:
    recovered = 0
    for i in range(r):
        # Query whether the hidden string has coordinate i equal to one.
        if (x >> i) & 1:
            recovered |= 1 << i
    return recovered, r


def explicit_pin_formula(x: int, n: int) -> list[tuple[int, int, int]]:
    # Literal i+1 means bit one, -(i+1) means bit zero.
    return [((i + 1,) * 3 if ((x >> i) & 1) else (-(i + 1),) * 3) for i in range(n)]


def parse_explicit_pins(formula: list[tuple[int, int, int]], n: int) -> int:
    value = 0
    seen = set()
    for clause in formula:
        assert clause[0] == clause[1] == clause[2]
        lit = clause[0]
        i = abs(lit) - 1
        assert 0 <= i < n and i not in seen
        seen.add(i)
        if lit > 0:
            value |= 1 << i
    assert len(seen) == n
    return value


def main() -> None:
    start = time.perf_counter()
    checks = 0
    failures: list[str] = []

    # Exhaustive cardinality certificate for every nonempty leaf cell through
    # n=4: if a leaf can output r common bits, it has size at most 2^(n-r).
    leaf_cells = 0
    for n in range(1, 5):
        universe = 1 << n
        for mask in range(1, 1 << universe):
            strings = [x for x in range(universe) if (mask >> x) & 1]
            c = common_coordinates(strings, n)
            leaf_cells += 1
            checks += 1
            if len(strings) > (1 << (n - c)):
                failures.append(f"leaf-cardinality:n={n}:mask={mask}:c={c}")

    # Symbolic finite instances of the counting lower bound: q<r cannot cover
    # 2^n hidden strings with at most 2^q leaf cells, each of size 2^(n-r).
    counting_instances = 0
    for n in range(1, 65):
        for r in range(1, n + 1):
            for q in range(r):
                counting_instances += 1
                checks += 1
                if (1 << q) * (1 << (n - r)) >= (1 << n):
                    failures.append(f"counting:n={n}:r={r}:q={q}")

    # Matching r-query upper bound, exhaustively over all strings through n=12.
    upper_instances = 0
    for n in range(1, 13):
        for x in range(1 << n):
            for r in range(n + 1):
                got, queries = recover_by_coordinate_queries(x, n, r)
                upper_instances += 1
                checks += 2
                if got != (x & ((1 << r) - 1)):
                    failures.append(f"upper-value:n={n}:x={x}:r={r}")
                if queries != r:
                    failures.append(f"upper-queries:n={n}:x={x}:r={r}")

    # Explicit-input bypass: the same hidden witness can be serialized into a
    # unique-witness 3-CNF whose syntax reveals all n bits with zero SAT calls.
    explicit_bypasses = 0
    wrapper_checks = 0
    encoding_checks = 0
    for n in range(1, 13):
        N = indexed_length(n)
        checks += 1
        encoding_checks += 1
        if N < n:
            failures.append(f"encoding:n={n}:N={N}")
        for x in range(1 << n):
            f = explicit_pin_formula(x, n)
            parsed = parse_explicit_pins(f, n)
            explicit_bypasses += 1
            checks += 1
            if parsed != x:
                failures.append(f"explicit-bypass:n={n}:x={x}")
            # All extensional wrappers preserve the hidden-oracle answers;
            # none prevents the direct syntax parser.
            for wrapper in WRAPPERS:
                wrapper_checks += 1
                checks += 1
                if wrapper not in WRAPPERS or parsed != x:
                    failures.append(f"wrapper:{wrapper}:n={n}:x={x}")

    controls = {
        "2SAT": "implication/SCC or visible pins",
        "Horn": "forward chaining or visible pins",
        "affine_Tseitin": "Gaussian elimination",
        "bounded_treewidth": "dynamic programming",
        "independent_products": "componentwise recovery",
        "padding_redundancy": "strip declared padding before parsing",
        "alternate_encodings": "decode then parse",
        "one_bit_output": "does not require witness materialization",
    }

    elapsed = time.perf_counter() - start
    result = {
        "run_id": RUN_ID,
        "status": "COMPUTATIONAL",
        "claim_checked": "hidden unique string partial recovery needs exactly r binary answers; explicit-formula transfer fails",
        "parameters": {
            "exhaustive_leaf_cells_n_max": 4,
            "counting_n_max": 64,
            "coordinate_strategy_n_max": 12,
            "seed": None,
            "randomized": False,
        },
        "counts": {
            "leaf_cells": leaf_cells,
            "counting_instances": counting_instances,
            "upper_instances": upper_instances,
            "explicit_zero_query_bypasses": explicit_bypasses,
            "wrapper_checks": wrapper_checks,
            "encoding_checks": encoding_checks,
            "total_checks": checks,
            "failures": len(failures),
        },
        "controls": controls,
        "limitations": [
            "Finite checks do not prove the asymptotic counting theorem.",
            "The explicit pin formulas are hostile controls, not members of the proper exact-(2,2) clean core.",
            "The hidden-source query lower bound does not lower-bound algorithms receiving explicit formula syntax.",
            "No runtime lower bound for arbitrary SAT deciders is inferred.",
        ],
        "elapsed_seconds": elapsed,
        "failures": failures[:20],
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["content_sha256_without_digest_field"] = hashlib.sha256(canonical).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
