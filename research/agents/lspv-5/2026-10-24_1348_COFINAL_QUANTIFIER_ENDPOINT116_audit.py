#!/usr/bin/env python3
"""Exact arithmetic and quantifier-regression audit for endpoint report 116."""

from fractions import Fraction
import json


def beta(c: Fraction) -> Fraction:
    return ((c + 2) / (c * c) - c) / 2


def main() -> None:
    c_star = Fraction(241, 200)
    beta_star = beta(c_star)
    examples = [
        (Fraction(121, 100), Fraction(9, 20), Fraction(61, 50)),
        (Fraction(13, 10), Fraction(3, 10), Fraction(131, 100)),
    ]

    checks = []
    checks.append(("beta_star_exact", beta_star == Fraction(11642479, 23232400)))
    checks.append(("beta_star_gt_half", beta_star > Fraction(1, 2)))
    for i, (t, s, c) in enumerate(examples, 1):
        checks.append((f"curve_example_{i}_strict_time", c > max(Fraction(1), t)))
        checks.append((f"curve_example_{i}_strict_space", s < beta(c)))

    # Boolean abstraction of the two cofinal formulations.
    # endpoint_disjoint=True means no achievable route can end in B.
    truth_rows = []
    for e_empty in (False, True):
        p_ne_np = e_empty
        # Fixed unbounded U, conditional on membership of each diagonal in E.
        h_conditional = e_empty
        # Literal existence of an unbounded U contained in achievable diagonals,
        # with every route ending in the forbidden region.  Endpoint disjointness
        # makes this false whether E is empty or nonempty.
        h_literal_existential = False
        truth_rows.append(
            {
                "E_empty": e_empty,
                "P_ne_NP": p_ne_np,
                "H_fixed_U_conditional": h_conditional,
                "H_literal_unbounded_achievable_U": h_literal_existential,
            }
        )
    checks.append(
        (
            "conditional_form_matches_separation",
            all(r["P_ne_NP"] == r["H_fixed_U_conditional"] for r in truth_rows),
        )
    )
    checks.append(
        (
            "literal_existential_not_equivalent",
            any(
                r["P_ne_NP"] != r["H_literal_unbounded_achievable_U"]
                for r in truth_rows
            ),
        )
    )

    # Exact monotonicity witnesses: beta'(c)=-(1+c^-2+4c^-3)/2 < 0.
    monotone_samples = [Fraction(101, 100), Fraction(6, 5), Fraction(3, 2)]
    for i, c in enumerate(monotone_samples, 1):
        derivative = -(1 + 1 / (c * c) + 4 / (c * c * c)) / 2
        checks.append((f"beta_derivative_negative_{i}", derivative < 0))

    result = {
        "run_id": "COFINAL-QUANTIFIER-ENDPOINT116",
        "status": "PASS" if all(ok for _, ok in checks) else "FAIL",
        "classification": "COMPUTATIONAL exact-rational regression; proofs are in the report",
        "beta_star": str(beta_star),
        "beta_star_minus_half": str(beta_star - Fraction(1, 2)),
        "curve_examples": [
            {
                "t": str(t),
                "s": str(s),
                "witness_c": str(c),
                "beta_c": str(beta(c)),
                "margin": str(beta(c) - s),
            }
            for t, s, c in examples
        ],
        "truth_rows": truth_rows,
        "checks": [{"name": name, "pass": ok} for name, ok in checks],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
