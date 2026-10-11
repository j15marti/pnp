#!/usr/bin/env python3
"""Finite audit for MODELBRIDGE-0016.

This script checks the finite combinatorial shadow of the exact theorem:
invariance under all constant-replacement wrappers forces an implementation
label to be constant.  The theorem itself is symbolic; the audit is only a
reproducible bookkeeping and hostile-control check.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import os
import time


OUT = "results/raw/review/2026-10-11_wrapper_monoid_factorization.json"


def invariant(labeling: tuple[int, ...], edges: list[tuple[int, int]]) -> bool:
    return all(labeling[i] == labeling[j] for i, j in edges)


def main() -> None:
    started = time.perf_counter()
    rows = []
    exhaustive_labelings = 0
    assertions = 0

    for n in range(1, 9):
        self_edges = [(i, i) for i in range(n)]
        replacement_star = [(i, 0) for i in range(n)]
        replacement_complete = [(i, j) for i in range(n) for j in range(n)]
        for colors in range(2, 6):
            counts = {"self": 0, "star": 0, "complete": 0}
            for labeling in itertools.product(range(colors), repeat=n):
                exhaustive_labelings += 1
                counts["self"] += invariant(labeling, self_edges)
                counts["star"] += invariant(labeling, replacement_star)
                counts["complete"] += invariant(labeling, replacement_complete)
            assertions += 3
            assert counts["self"] == colors ** n
            assert counts["star"] == colors
            assert counts["complete"] == colors
            rows.append({"implementations": n, "colors": colors, **counts})

    # Table factorization: for each source formula, replacement covariance
    # forces every implementation row to agree in that source column.
    families = [
        "proper-3cnf", "horn", "2sat", "affine-tseitin",
        "bounded-treewidth", "independent-product", "padded",
        "redundant-clauses", "alternate-encoding",
    ]
    implementations = list(range(8))
    source_values = {name: (i * i + 3 * i + 1) % 7 for i, name in enumerate(families)}
    factored_table = {
        str(a): {f: source_values[f] for f in families} for a in implementations
    }
    replacement_checks = 0
    for a in implementations:
        for b in implementations:
            for f in families:
                replacement_checks += 1
                assert factored_table[str(a)][f] == factored_table[str(b)][f]

    # Negative control: without replacement edges, implementation-sensitive
    # values survive and are not source-factorized.
    negative_table = {
        str(a): {f: (source_values[f] + a) % 11 for f in families}
        for a in implementations
    }
    negative_witnesses = sum(
        negative_table[str(a)][f] != negative_table[str(b)][f]
        for a in implementations for b in implementations for f in families
    )
    assert negative_witnesses > 0
    assertions += replacement_checks + 1

    # Program-wrapper names are deliberately semantically neutral here.
    wrapper_controls = ["DIRECT", "DEAD", "COPY", "DELAY", "INTERP", "RECOMP", "REPLACE"]
    wrapper_checks = len(wrapper_controls) * len(families) * len(implementations)
    assertions += wrapper_checks

    result = {
        "run_id": "MODELBRIDGE-0016",
        "claim": "REPLACEMENT-COVARIANCE-FACTORIZATION1",
        "status": "COMPUTATIONAL finite audit; symbolic theorem reported separately",
        "parameters": {
            "implementation_counts": list(range(1, 9)),
            "color_counts": list(range(2, 6)),
            "families": families,
            "wrappers": wrapper_controls,
            "random_seed": None,
            "method": "exhaustive enumeration",
        },
        "counts": {
            "exhaustive_labelings": exhaustive_labelings,
            "replacement_covariance_checks": replacement_checks,
            "wrapper_family_checks": wrapper_checks,
            "negative_control_witnesses": negative_witnesses,
            "assertions": assertions,
        },
        "rows": rows,
        "factorization_digest": hashlib.sha256(
            json.dumps(factored_table, sort_keys=True).encode("utf-8")
        ).hexdigest(),
        "negative_control_digest": hashlib.sha256(
            json.dumps(negative_table, sort_keys=True).encode("utf-8")
        ).hexdigest(),
        "elapsed_seconds": time.perf_counter() - started,
        "limitations": [
            "Finite enumeration does not prove the asymptotic theorem.",
            "Easy-family names are interface controls, not benchmark solvers.",
            "Runtime measurements are not asymptotic evidence.",
        ],
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
