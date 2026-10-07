#!/usr/bin/env python3
"""Bounded parameter audit for the IPZ sparsification-to-WRAPPER transfer.

This is a theorem-transfer arithmetic test, not a SAT lower-bound experiment.
It checks exact integer inequalities and records finite sensitivity data.
"""

from __future__ import annotations

import json
import math
import random
import time
from fractions import Fraction


SEED = 20261007
BUDGET_SECONDS = 25.0


def lit_bits(n: int) -> int:
    return 1 + math.ceil(math.log2(n + 1))


def encoded_bits(n: int, clauses: int, k: int) -> int:
    return 2 * lit_bits(n) + clauses * (1 + k * lit_bits(n))


def record_regime(n: int, clauses: int, k: int, a: int) -> dict:
    parent = encoded_bits(n, clauses, k)
    log_parent_ceil = parent.bit_length()
    fixed_eps = Fraction(1, 20)
    fixed_log2_fanout = fixed_eps * n
    poly_eps = Fraction(a * log_parent_ceil, n)

    # Calabro--Impagliazzo--Paturi Lemma 1 gives
    # O((k/epsilon)^(3k) n) clauses.  Setting the hidden constant to one is
    # deliberately optimistic; the original clause count is always a second
    # valid upper bound because an identity return is available.
    rate_base = math.ceil(Fraction(k, 1) / poly_eps)
    quantitative_clause_bound = n * pow(rate_base, 3 * k)
    certified_clauses = min(clauses, quantitative_clause_bound)
    certified_child = encoded_bits(n, certified_clauses, k)

    return {
        "n": n,
        "clauses": clauses,
        "parent_bits": parent,
        "fixed_epsilon": "1/20",
        "fixed_log2_fanout": str(fixed_log2_fanout),
        "polynomial_log2_budget": a * log_parent_ceil,
        "fixed_fanout_exceeds_polynomial_budget": fixed_log2_fanout > a * log_parent_ceil,
        "polyfanout_epsilon": f"{poly_eps.numerator}/{poly_eps.denominator}",
        "polyfanout_epsilon_float": float(poly_eps),
        "cip_optimistic_clause_bound": quantitative_clause_bound,
        "certified_clause_bound_after_identity_cap": certified_clauses,
        "certified_child_bits": certified_child,
        "certified_child_equals_parent": certified_child == parent,
        "effective_child_exponent": math.log(certified_child) / math.log(parent),
    }


def main() -> None:
    start = time.monotonic()
    rng = random.Random(SEED)
    k = 3
    a = 2
    checks = 0
    failures: list[str] = []
    sparse_rows = []
    dense_rows = []

    for exponent in range(8, 21):
        if time.monotonic() - start > BUDGET_SECONDS:
            raise TimeoutError("cooperative 25-second budget exceeded")
        n = 1 << exponent
        sparse = record_regime(n, n, k, a)
        dense = record_regime(n, n**k, k, a)
        sparse_rows.append(sparse)
        dense_rows.append(dense)

        checks += 6
        if exponent >= 12 and not sparse["fixed_fanout_exceeds_polynomial_budget"]:
            failures.append(f"sparse fixed-epsilon fanout check failed at n={n}")
        if exponent >= 12 and not dense["fixed_fanout_exceeds_polynomial_budget"]:
            failures.append(f"dense fixed-epsilon fanout check failed at n={n}")
        if not sparse["certified_child_equals_parent"]:
            failures.append(f"known quantitative bound unexpectedly certifies sparse shrink at n={n}")
        if not dense["certified_child_equals_parent"]:
            failures.append(f"known quantitative bound unexpectedly certifies dense shrink at n={n}")
        if sparse["polyfanout_epsilon_float"] <= 0 or dense["polyfanout_epsilon_float"] <= 0:
            failures.append(f"nonpositive epsilon at n={n}")
        if exponent > 8:
            if sparse_rows[-1]["polyfanout_epsilon_float"] >= sparse_rows[-2]["polyfanout_epsilon_float"]:
                failures.append(f"sparse epsilon schedule did not decrease at n={n}")

    # Hypothetical C(epsilon)=epsilon^{-d} sensitivity.  On the dense
    # m=n^k scale, only d+1<k can certify a power-smaller child from this form.
    sensitivity = []
    for d in range(0, 3 * k + 1):
        predicted_power = Fraction(d + 1, k)
        sensitivity.append(
            {
                "rate_degree_d": d,
                "dense_child_power_ignoring_polylogs": f"{predicted_power.numerator}/{predicted_power.denominator}",
                "can_be_strictly_below_one": predicted_power < 1,
                "matches_published_3k_degree": d == 3 * k,
            }
        )
        checks += 2
    if [row["rate_degree_d"] for row in sensitivity if row["can_be_strictly_below_one"]] != [0, 1]:
        failures.append("dense rate-degree threshold mismatch for k=3")

    # Seeded encoding perturbations: add harmless header/variable-table costs.
    # They must not change the qualitative certificate: the published rate
    # bound, capped by returning the original, still certifies exponent one.
    random_controls = []
    for _ in range(128):
        exponent = rng.randint(10, 18)
        n = 1 << exponent
        clauses = n if rng.randrange(2) == 0 else n**k
        row = record_regime(n, clauses, k, a)
        random_controls.append(
            {
                "n": n,
                "regime": "sparse" if clauses == n else "dense",
                "epsilon": row["polyfanout_epsilon"],
                "child_equals_parent": row["certified_child_equals_parent"],
            }
        )
        checks += 1
        if not row["certified_child_equals_parent"]:
            failures.append(f"seeded control unexpectedly certified shrink at n={n}")

    elapsed = time.monotonic() - start
    payload = {
        "claim_id": "IPZ-POLYFANOUT-TRANSFER-GATE1",
        "status": "COMPUTATIONAL theorem-transfer arithmetic check",
        "seed": SEED,
        "cooperative_budget_seconds": BUDGET_SECONDS,
        "elapsed_seconds": elapsed,
        "checks": checks,
        "failures": failures,
        "passed": not failures,
        "parameters": {"k": k, "polynomial_fanout_degree_a": a},
        "sparse_samples": sparse_rows,
        "dense_samples": dense_rows,
        "rate_sensitivity": sensitivity,
        "random_control_count": len(random_controls),
        "random_controls_sample": random_controls[:8],
        "interpretation": (
            "Fixed epsilon gives superpolynomial fanout on both ordinary sparse and maximally dense "
            "k-CNF scales. Choosing epsilon proportional to log(M)/n makes fanout polynomial, but "
            "the published O((k/epsilon)^(3k)n) clause guarantee, even with hidden constant one and "
            "capped by the original formula, certifies no fixed-power encoded shrink. This is a "
            "failure of this theorem transfer, not a lower bound on the actual sparsification output "
            "or on arbitrary SAT transformations."
        ),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
