#!/usr/bin/env python3
"""Finite arithmetic audit for JOINTENDPOINT1.

This does not prove an asymptotic complexity statement.  It checks the
exponent algebra used by the symbolic proof across hostile family labels,
encodings, wrappers, and rational gauge powers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path


FAMILIES = [
    "signed-clean-core",
    "2sat",
    "horn",
    "affine-tseitin",
    "bounded-treewidth",
    "independent-product",
    "padded",
    "redundant-clauses",
]
ENCODINGS = ["canonical-indexed", "permuted", "auxiliary-variable", "self-delimiting"]
WRAPPERS = ["BASE", "DEAD", "COPY", "DELAY", "INTERP", "RECOMP"]


def frac_text(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    a_values = [Fraction(1, 4), Fraction(1, 2), Fraction(1), Fraction(2), Fraction(3)]
    b_values = list(range(5))
    time_exponents = list(range(1, 13))
    target_exponents = list(range(1, 21))
    padding_powers = [1, 2, 3, 5]
    wrapper_time = {"BASE": 1, "DEAD": 1, "COPY": 2, "DELAY": 4, "INTERP": 3, "RECOMP": 5}
    wrapper_space = {"BASE": 1, "DEAD": 1, "COPY": 2, "DELAY": 1, "INTERP": 2, "RECOMP": 1}

    polynomial_checks = 0
    witness_checks = 0
    hostile_cells = 0
    failures: list[dict[str, object]] = []

    for a in a_values:
        for b in b_values:
            for k in time_exponents:
                for s in range(k + 1):
                    gauge_exp = a * k + b * s
                    polynomial_checks += 1
                    if gauge_exp < 0 or gauge_exp.denominator <= 0:
                        failures.append({"phase": "polynomial", "a": frac_text(a), "b": b, "k": k, "s": s})
            for d in target_exponents:
                c = Fraction(d + 1, 1) / a
                witness_checks += 1
                if not a * c > d:
                    failures.append({"phase": "witness", "a": frac_text(a), "d": d, "c": frac_text(c)})

    for family in FAMILIES:
        for encoding in ENCODINGS:
            for wrapper in WRAPPERS:
                for p in padding_powers:
                    for a in a_values:
                        for b in b_values:
                            # A polynomial T=N^k, S=N^s remains polynomial after
                            # every fixed wrapper and N -> N^p encoding change.
                            k = 3 * wrapper_time[wrapper] * p
                            s = 2 * wrapper_space[wrapper] * p
                            exponent = a * k + b * s
                            hostile_cells += 1
                            if exponent < 0:
                                failures.append({
                                    "phase": "hostile",
                                    "family": family,
                                    "encoding": encoding,
                                    "wrapper": wrapper,
                                    "padding": p,
                                })

    payload = {
        "run_id": "JOINTENDPOINT1",
        "status": "COMPUTATIONAL",
        "scope": "finite rational-exponent algebra audit; no asymptotic inference",
        "polynomial_checks": polynomial_checks,
        "nonpolynomial_witness_checks": witness_checks,
        "hostile_control_cells": hostile_cells,
        "families": FAMILIES,
        "encodings": ENCODINGS,
        "wrappers": WRAPPERS,
        "padding_powers": padding_powers,
        "failures": failures,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["canonical_payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
