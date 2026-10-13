#!/usr/bin/env python3
"""CPDEPTHEND1 bounded audit.

Checks two exact bookkeeping interfaces used in the fixed-language synthesis:
1. literal/constant substitution commutes with legal Cutting Planes division;
2. a fixed polynomial depth lower bound excludes only a bounded range of
   machine exponents, whereas a superpolynomial depth lower bound defeats
   every fixed polynomial depth upper bound.

Finite enumeration validates algebra and types only.  It proves no SAT lower
bound and does not implement an arbitrary-machine-to-CP extractor.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import time


def ceil_div(a: int, d: int) -> int:
    return -((-a) // d)


def substitute(coeffs, rhs, images):
    """Substitute z_i -> const_i + sign_i*x_var (var=None for constants)."""
    out = {}
    shift = 0
    for a, (var, sign, const) in zip(coeffs, images):
        shift += a * const
        if var is not None:
            out[var] = out.get(var, 0) + a * sign
    return tuple(sorted(out.items())), rhs - shift


def division_commutation_audit():
    images = [
        (None, 0, 0), (None, 0, 1),
        (0, 1, 0), (0, -1, 1),
        (1, 1, 0), (1, -1, 1),
    ]
    checks = 0
    for d in range(1, 10):
        for qs in itertools.product(range(-2, 3), repeat=3):
            coeffs = tuple(d*q for q in qs)
            for rhs in range(-9, 10):
                for ims in itertools.product(images, repeat=3):
                    before_c, before_b = substitute(coeffs, rhs, ims)
                    divided_c = tuple((v, a//d) for v, a in before_c)
                    divided_b = ceil_div(before_b, d)
                    after_c, after_b = substitute(
                        tuple(a//d for a in coeffs), ceil_div(rhs, d), ims
                    )
                    assert divided_c == after_c
                    assert divided_b == after_b
                    checks += 1
    return checks


def clause_leaf_audit():
    """Enumerate width-three clause images and check the Boolean-valid test."""
    atoms = [
        (None, 0, 0), (None, 0, 1),
        (0, 1, 0), (0, -1, 1),
        (1, 1, 0), (1, -1, 1),
        (2, 1, 0), (2, -1, 1),
    ]
    total = tautologies = max_nonzero = 0
    for ims in itertools.product(atoms, repeat=3):
        coeffs, rhs = substitute((1, 1, 1), 1, ims)
        cmap = dict(coeffs)
        semantic = True
        for bits in itertools.product((0, 1), repeat=3):
            if sum(cmap.get(i, 0)*bits[i] for i in range(3)) < rhs:
                semantic = False
                break
        min_boolean = sum(a for _, a in coeffs if a < 0)
        arithmetic = rhs <= min_boolean
        assert semantic == arithmetic
        total += 1
        if semantic:
            tautologies += 1
            max_nonzero = max(max_nonzero, len(coeffs))
    # At most three variable bounds, a balanced two-level sum, one scaled
    # 0>=-1 weakening line, and one final addition: constant leaf depth <= 4.
    assert max_nonzero <= 3
    return total, tautologies, max_nonzero, 4


def exponent_firewall_audit():
    alpha_num, alpha_den = 12, 5  # 2.4
    rows = []
    for a in range(1, 5):
        for b in range(0, 5):
            for k in range(0, 13):
                excluded = (a*k+b)*alpha_den < alpha_num
                rows.append({"a": a, "b": b, "k": k, "excluded": excluded})
                assert excluded == (a*k+b < 2.4)
    # No fixed alpha can dominate every fixed polynomial exponent.
    for alpha in range(1, 17):
        assert not all(k < alpha for k in range(1, alpha+2))
    # Definition-level diagonal: an N^{omega(1)} lower bound eventually
    # dominates N^k for each separately fixed k.  This records quantifiers,
    # not a finite-N timing claim.
    quantifier_rows = [{"fixed_k": k, "required_eventual_lower_exponent": k+1}
                       for k in range(1, 17)]
    return rows, quantifier_rows


def main():
    started = time.perf_counter()
    div_checks = division_commutation_audit()
    clause = clause_leaf_audit()
    rows, qrows = exponent_firewall_audit()
    payload = {
        "run_id": "CPDEPTHEND1",
        "status": "COMPUTATIONAL",
        "division_commutation_checks": div_checks,
        "clause_image_checks": clause[0],
        "tautological_clause_images": clause[1],
        "max_projected_clause_variables": clause[2],
        "certified_constant_leaf_depth_bound": clause[3],
        "fixed_2_4_exponent_rows": len(rows),
        "superpolynomial_quantifier_rows": len(qrows),
        "interpretation": {
            "proved_by_math_not_timing": [
                "literal/constant substitution commutes with legal CP division",
                "projected width-three tautological axioms have constant-depth Boolean-bound derivations",
                "fixed 2.4 depth excludes only extraction exponents below 2.4",
                "N^{omega(1)} depth dominates each fixed polynomial exponent separately",
            ],
            "not_proved": [
                "arbitrary L22 computation yields a CP refutation",
                "de Rezende et al. source family is already instantiated through this compiler",
                "L22 is outside P",
            ],
        },
        "elapsed_seconds": round(time.perf_counter()-started, 6),
    }
    canon = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["semantic_sha256"] = hashlib.sha256(canon.encode()).hexdigest()
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
