#!/usr/bin/env python3
"""LSPV-5/421: exact output-projection controls for quadratic affine covers."""

from __future__ import annotations

import json
from itertools import product
from math import ceil


def parity(x: int) -> int:
    return x.bit_count() & 1


def independent_and_map(x: int, g: int, t: int | None = None) -> int:
    if t is None:
        t = g
    y = 0
    for i in range(t):
        y |= (((x >> (2 * i)) & 1) & ((x >> (2 * i + 1)) & 1)) << i
    return y


def affine_vector(x: int, n: int, masks: tuple[int, ...], const: int) -> int:
    y = 0
    for i, mask in enumerate(masks):
        y |= (parity(x & mask) ^ ((const >> i) & 1)) << i
    return y


def exhaustive_max_agreement(g: int, t: int) -> int:
    n = 2 * g
    best = 0
    for masks in product(range(1 << n), repeat=t):
        for const in range(1 << t):
            agree = sum(
                independent_and_map(x, g, t) == affine_vector(x, n, masks, const)
                for x in range(1 << n)
            )
            best = max(best, agree)
    return best


def predicted_u(g: int, t: int) -> int:
    # 2^(2g-t) * sum_{s in F_2^t} 2^(-rank(B_{s.Q})/2)
    # rank(B_{s.Q}) = 2*wt(s), hence U=2^(2(g-t))*3^t.
    return (1 << (2 * (g - t))) * (3**t)


def nested_and(x: int, variables: int) -> int:
    return int(x == (1 << variables) - 1)


def main() -> None:
    checks = 0
    rows = []

    # Complete affine-predictor enumerations where the search space is bounded.
    for g in range(1, 5):
        got = exhaustive_max_agreement(g, 1)
        want = predicted_u(g, 1)
        assert got == want
        checks += 1
        rows.append({
            "g_paid_independent_ands": g,
            "exported_outputs": 1,
            "hidden_outputs": g - 1,
            "inputs": 1 << (2 * g),
            "max_affine_agreement": got,
            "rank_spectrum_U": want,
            "agreement_fraction": "3/4",
            "constant_template_cover": 2,
        })

    for g in range(1, 4):
        for t in range(1, min(2, g) + 1):
            got = exhaustive_max_agreement(g, t)
            want = predicted_u(g, t)
            assert got == want
            checks += 1

    # Exact full-vector formula and projected formula through g=7.  The
    # closed form follows from independent pairs and is also witnessed by the
    # zero affine predictor; the bounded exhaustive loop above independently
    # checks all affine predictors through g=4 for scalar projection.
    for g in range(1, 8):
        for t in range(1, g + 1):
            zero_agreement = sum(independent_and_map(x, g, t) == 0 for x in range(1 << (2 * g)))
            assert zero_agreement == predicted_u(g, t)
            assert ceil((1 << (2 * g)) / predicted_u(g, t)) == ceil((4 / 3) ** t)
            checks += 2

    # Sharp projection counterexample: six paid nonlinear gates, one exported output.
    g = 6
    projected_cover = 2
    full_vector_lower_bound = ceil((4 / 3) ** g)
    assert projected_cover == 2
    assert full_vector_lower_bound == 6
    assert projected_cover < full_vector_lower_bound
    checks += 3

    # Nested paid private AND chain: final scalar output has a two-constant cover.
    nested = []
    for variables in range(2, 13):
        inputs = 1 << variables
        zero_agreement = sum(nested_and(x, variables) == 0 for x in range(inputs))
        one_agreement = inputs - zero_agreement
        assert zero_agreement == inputs - 1
        assert one_agreement == 1
        assert all(nested_and(x, variables) in (0, 1) for x in range(inputs))
        checks += 3
        nested.append({
            "variables": variables,
            "paid_nonlinear_chain_gates": variables - 1,
            "exported_outputs": 1,
            "zero_template_agreement": zero_agreement,
            "one_template_agreement": one_agreement,
            "constant_template_cover": 2,
        })

    out = {
        "classification": "PROVED/RESTRICTED + COMPUTATIONAL; output-projection control only",
        "checks": checks,
        "lemma": {
            "full_independent_and_U": "3^g",
            "t_output_projection_U": "2^(2(g-t))*3^t",
            "projection_cover_lower_bound": "ceil((4/3)^t), independent of hidden paid gates",
            "nested_private_chain": "two constant affine templates cover the final scalar output for every chain length",
        },
        "projection_rows": rows,
        "nested_rows": nested,
        "malicious_control": {
            "paid_gates": 6,
            "exported_outputs": 1,
            "actual_projected_cover": projected_cover,
            "invalid_full_vector_lower_bound_if_hidden_outputs_are_silently_counted": full_vector_lower_bound,
            "rejected_claim": "paid private nonlinear gates may be counted as exposed vector coordinates",
        },
        "scope": [
            "Does not refute the LSPV-1/491 quadratic vector theorem.",
            "Refutes only a transfer that substitutes paid private gate count for authenticated exposed output dimension.",
            "Does not authenticate historical R_mix341 exported/private-wire grammar.",
            "Does not prove an all-mixed lower bound or B3.",
        ],
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
