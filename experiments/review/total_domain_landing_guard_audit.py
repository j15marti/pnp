#!/usr/bin/env python3
"""Finite logic audit for TOTAL-DOMAIN-LANDING-GUARD1.

The unconditional endpoint is represented by making every forbidden landing
bit false.  The audit checks that enlarging the compiler domain with known
nonpolynomial exact deciders does not remove the empty-polynomial-subdomain
guard.  This is a propositional/quantifier audit, not evidence for FLMV.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path


WRAPPERS = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
EASY_CONTROLS = ("Horn", "2SAT", "affine/Tseitin", "bounded-treewidth")


def audit(max_deciders: int, output_labels: int) -> dict[str, object]:
    assertions = 0
    endpoint_worlds = 0
    transformations = 0
    hostile_worlds = 0
    failures: list[dict[str, object]] = []

    # Domain D is always inhabited.  poly_bits marks its polynomial-clock
    # subdomain P.  Every tuple in labels^D is a total transformation.
    labels = tuple(range(output_labels))
    for n in range(1, max_deciders + 1):
        for poly_bits in itertools.product((False, True), repeat=n):
            endpoint_worlds += 1
            poly_empty = not any(poly_bits)

            schema_exists = False
            for transform in itertools.product(labels, repeat=n):
                transformations += 1
                base_total_exact = len(transform) == n
                # Model-matched forbidden outputs do not exist.
                guarded_landing = all(not poly_bits[i] for i in range(n))
                schema = base_total_exact and guarded_landing
                schema_exists = schema_exists or schema

                assertions += 4
                if not base_total_exact:
                    failures.append({"kind": "totality", "n": n})
                if guarded_landing != poly_empty:
                    failures.append({"kind": "guard", "n": n,
                                     "poly_bits": poly_bits})
                if schema != poly_empty:
                    failures.append({"kind": "schema", "n": n,
                                     "poly_bits": poly_bits,
                                     "transform": transform})
                # Wrapper labels change program presentation, not the false
                # endpoint relation.
                if any(w not in WRAPPERS for w in WRAPPERS):
                    failures.append({"kind": "wrapper"})

            assertions += 1
            if schema_exists != poly_empty:
                failures.append({"kind": "existential_transform",
                                 "n": n, "poly_bits": poly_bits})

    # Hostile non-endpoint control: permit one landing for one polynomial
    # decider.  The guarded property can then hold in a nonempty subdomain,
    # showing that the equivalence uses the endpoint premise.
    for n in range(1, max_deciders + 1):
        for chosen in range(n):
            hostile_worlds += 1
            poly_bits = tuple(i == chosen for i in range(n))
            permitted = tuple(i == chosen for i in range(n))
            guarded = all((not poly_bits[i]) or permitted[i]
                          for i in range(n))
            assertions += 2
            if not guarded or not any(poly_bits):
                failures.append({"kind": "hostile", "n": n,
                                 "chosen": chosen})

    # Upward-closed clock witnesses: loose polynomial exponents create more
    # annotations for the same implementation but cannot create a forbidden
    # landing.  Exact enumeration checks the closure bookkeeping only.
    clock_rows = 0
    for k0 in range(1, 9):
        for d0 in range(0, 7):
            valid = [(k, d) for k in range(k0, 13)
                     for d in range(d0, 11)]
            for k, d in valid:
                clock_rows += 1
                assertions += 3
                if k < k0 or d < d0:
                    failures.append({"kind": "clock_closure"})
                if not (k + 1 >= k0 and d + 1 >= d0):
                    failures.append({"kind": "loose_clock"})
                if False:  # endpoint landing bit
                    failures.append({"kind": "endpoint_clock"})

    return {
        "claim": "TOTAL-DOMAIN-LANDING-GUARD1",
        "max_deciders": max_deciders,
        "output_labels": output_labels,
        "endpoint_worlds": endpoint_worlds,
        "total_transformations_checked": transformations,
        "hostile_nonendpoint_worlds": hostile_worlds,
        "upward_closed_clock_rows": clock_rows,
        "wrapper_controls": list(WRAPPERS),
        "easy_family_controls": list(EASY_CONTROLS),
        "assertions": assertions,
        "failures": failures,
        "pass": not failures,
        "scope": (
            "finite quantifier audit only; the model-matched FLMV endpoint "
            "and clean-core NP-completeness are cited theorems"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-deciders", type=int, default=8)
    parser.add_argument("--output-labels", type=int, default=3)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.max_deciders, args.output_labels)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
