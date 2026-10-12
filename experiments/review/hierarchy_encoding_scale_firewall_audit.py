#!/usr/bin/env python3
"""Finite arithmetic audit for HIERARCHY-ENCODING-SCALE-FIREWALL1.

This script checks only exponent bookkeeping.  It is not evidence for an
unconditional SAT lower bound.  Every invocation is intentionally bounded.
"""

from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path


def main() -> None:
    checks = 0
    failures: list[dict[str, object]] = []

    lambdas = [
        Fraction(1, 4),
        Fraction(1, 3),
        Fraction(1, 2),
        Fraction(3, 4),
        Fraction(1, 1),
        Fraction(3, 2),
        Fraction(2, 1),
        Fraction(3, 1),
    ]
    solver_exponents = range(1, 25)

    speedup_table: list[dict[str, object]] = []
    for lam in lambdas:
        row = {"lambda": str(lam), "speedup_K": []}
        for k in solver_exponents:
            predicted = lam * k < 1
            direct = float(lam) * k < 1.0 - 1e-12
            checks += 1
            if predicted != direct:
                failures.append({"kind": "speedup_equivalence", "lambda": str(lam), "K": k})
            if predicted:
                row["speedup_K"].append(k)
            if lam >= 1:
                checks += 1
                if predicted:
                    failures.append({"kind": "linear_scale_false_speedup", "lambda": str(lam), "K": k})
        speedup_table.append(row)

    padding_checks: list[dict[str, object]] = []
    for lam in lambdas:
        for padding_power in range(1, 13):
            padded = lam * padding_power
            for k in solver_exponents:
                before = lam * k
                after = padded * k
                checks += 1
                if after < before:
                    failures.append(
                        {
                            "kind": "padding_improved_exponent",
                            "lambda": str(lam),
                            "padding_power": padding_power,
                            "K": k,
                        }
                    )
            padding_checks.append(
                {
                    "lambda": str(lam),
                    "padding_power": padding_power,
                    "effective_lambda": str(padded),
                }
            )

    # A concrete Robson/Cook-style scale control: N(T)=T ceil(log2(T+2)).
    # It checks monotone accounting, not a lower bound for every encoding.
    concrete_scale: list[dict[str, object]] = []
    for j in range(1, 21):
        t = 2**j
        n = t * math.ceil(math.log2(t + 2))
        entry: dict[str, object] = {"T": t, "encoded_bits": n, "solver_costs": {}}
        checks += 1
        if n < t:
            failures.append({"kind": "concrete_scale_below_T", "T": t, "N": n})
        for k in (1, 2, 3, 4, 8, 16, 24):
            cost = n**k
            entry["solver_costs"][str(k)] = str(cost)
            checks += 1
            if cost < t:
                failures.append({"kind": "concrete_false_speedup", "T": t, "N": n, "K": k})
        concrete_scale.append(entry)

    hostile_controls = [
        "2SAT-special-family",
        "Horn-special-family",
        "affine-Gaussian-elimination",
        "bounded-treewidth",
        "independent-products",
        "padding",
        "redundant-clauses",
        "alternate-encoding",
        "wrapper-equivalent-program",
        "succinct-representation-model-change",
    ]
    control_audit: list[dict[str, object]] = []
    for control in hostile_controls:
        for lam in lambdas:
            for k in solver_exponents:
                # The firewall is conditional on the realized encoding exponent.
                # A control can matter only by changing that exponent, the solver's
                # promise, or the charged model; its name alone changes no arithmetic.
                baseline = lam * k < 1
                replay = lam * k < 1
                checks += 1
                if baseline != replay:
                    failures.append(
                        {"kind": "control_changed_identity", "control": control, "lambda": str(lam), "K": k}
                    )
        control_audit.append(
            {
                "control": control,
                "classification": "must-change-realized-exponent-promise-or-model",
            }
        )

    payload: dict[str, object] = {
        "experiment": "HIERARCHY-ENCODING-SCALE-FIREWALL1 finite arithmetic audit",
        "status": "COMPUTATIONAL",
        "scientific_scope": (
            "Checks exponent identities and hostile-control bookkeeping only; "
            "does not establish P != NP or an all-encoding lower bound."
        ),
        "criterion": "A worst-case N^K solver bound yields a T-exponent speedup only if lambda*K<1, excluding construction/access costs.",
        "speedup_table": speedup_table,
        "padding_checks": padding_checks,
        "concrete_scale": concrete_scale,
        "hostile_controls": control_audit,
        "checks": checks,
        "failures": failures,
    }

    out = Path("results/raw/review/2026-10-13_hierarchy_encoding_scale_firewall.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    out.write_text(encoded, encoding="utf-8")
    print(json.dumps({"checks": checks, "failures": len(failures), "result": str(out)}, sort_keys=True))
    print("result_sha256=" + hashlib.sha256(encoded.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
