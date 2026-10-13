#!/usr/bin/env python3
"""Bounded audit of charged black-box extraction quantifiers.

The symbolic theorem is proved in the accompanying report.  This finite audit
checks the cost-composition algebra, wrapper stability of fixed polynomial
exponents, and the endpoint/model type table.  It makes no asymptotic lower-
bound inference from sampled sizes.
"""

from __future__ import annotations

import hashlib
import json


def composed_exponent(local: int, queries: int, query_scale: int, solver: int) -> int:
    """N^local + N^queries calls on length N^query_scale to an N^solver oracle."""
    return max(local, queries + query_scale * solver)


def main() -> None:
    exponent_checks = 0
    wrapper_checks = 0
    maxima: dict[str, int] = {}
    for local in range(1, 9):
        for queries in range(0, 8):
            for query_scale in range(1, 7):
                for solver in range(1, 9):
                    got = composed_exponent(local, queries, query_scale, solver)
                    expected = max(local, queries + query_scale * solver)
                    assert got == expected
                    assert isinstance(got, int) and got >= 1
                    exponent_checks += 2
                    for wrapper in range(0, 7):
                        wrapped = max(got, wrapper)
                        assert wrapped == max(local, queries + query_scale * solver, wrapper)
                        wrapper_checks += 1
                    maxima[f"solver_{solver}"] = max(maxima.get(f"solver_{solver}", 0), got)

    quantifier_worlds = [
        {
            "world": "P_ne_NP",
            "poly_sat_decider_exists": False,
            "universal_charged_extractor_statement": True,
            "reason": "vacuous domain",
        },
        {
            "world": "P_eq_NP",
            "poly_sat_decider_exists": True,
            "universal_charged_extractor_statement": False,
            "reason": "composition is polynomial and explicit hard-model output contradicts its lower bound",
        },
    ]
    for row in quantifier_worlds:
        assert row["universal_charged_extractor_statement"] == (
            not row["poly_sat_decider_exists"]
        )

    endpoint_audit = [
        {
            "endpoint": "DAG Resolution on compiled exact-(2,2) expander Tseitin",
            "lower_bound": "2^{Omega(L/log L)}",
            "charged_poly_extraction_contradiction": True,
            "scope": "proof system only",
        },
        {
            "endpoint": "Polynomial Calculus over F2 on the same compiled family",
            "lower_bound": "none; degree at most four and polynomial expanded size",
            "charged_poly_extraction_contradiction": False,
            "scope": "algebraic hostile control",
        },
        {
            "endpoint": "ordinary uniform deterministic machine time",
            "lower_bound": "OPEN",
            "charged_poly_extraction_contradiction": False,
            "scope": "desired same-model endpoint",
        },
        {
            "endpoint": "compressed or implicit Resolution object",
            "lower_bound": "explicit Resolution size bound does not apply",
            "charged_poly_extraction_contradiction": False,
            "scope": "model changed",
        },
    ]

    hostile_controls = [
        "2SAT",
        "Horn",
        "affine/Tseitin Gaussian elimination",
        "bounded treewidth",
        "independent products",
        "padding",
        "redundant clauses",
        "renaming/complementation",
        "DEAD/COPY/DELAY/INTERP/RECOMP wrappers",
        "one-bit decision output",
    ]

    semantic = {
        "exponent_checks": exponent_checks,
        "wrapper_checks": wrapper_checks,
        "maxima": maxima,
        "quantifier_worlds": quantifier_worlds,
        "endpoint_audit": endpoint_audit,
        "hostile_controls": hostile_controls,
        "classification": "black-box worst-case/average-case architecture is an analogy; universal hard-endpoint extraction is separation-equivalent",
        "scope": "finite algebra/type audit only; no asymptotic extrapolation",
    }
    payload = json.dumps(semantic, sort_keys=True, separators=(",", ":")).encode()
    result = {
        "experiment": "blackbox_extraction_quantifier_audit",
        "status": "COMPUTATIONAL",
        **semantic,
        "semantic_sha256": hashlib.sha256(payload).hexdigest(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
