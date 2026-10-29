#!/usr/bin/env python3
"""Finite arithmetic controls for REDUCTION-FRONTIER-TRANSFER-REFEREE207.

Dependency-free; symbolic theorems are proved in the accompanying report.
All loops are tiny and deterministic.
"""

from __future__ import annotations

import json
import math


def logn(x: float, n: float) -> float:
    return math.log(x) / math.log(n)


def projection_sizes(t: int) -> dict:
    """Canonical fixed-field sizes for the selector projection control.

    Source: 2t width-three clauses on 1+4t variables.
    Auxiliary-free projection: t^2 width-four clauses on 4t variables.
    One sign bit and one delimiter bit are charged per literal/clause.
    """
    var_count = 1 + 4 * t
    ident = math.ceil(math.log2(var_count + 1))
    source = 2 * t * (3 * (ident + 1) + 1) + 2 * ident
    child = t * t * (4 * (ident + 1) + 1) + 2 * ident
    alpha = logn(child, source)
    return {
        "t_exact_if_small": t if t <= 65536 else None,
        "log2_t": math.log2(t),
        "variables_source_exact_if_small": var_count if t <= 65536 else None,
        "identifier_bits": ident,
        "source_bits_exact_if_small": source if t <= 65536 else None,
        "projected_child_bits_exact_if_small": child if t <= 65536 else None,
        "log2_source_bits": math.log2(source),
        "log2_projected_child_bits": math.log2(child),
        "source_bits_decimal_digits": len(str(source)),
        "projected_child_bits_decimal_digits": len(str(child)),
        "child_over_source": child / source,
        "effective_size_exponent_log_M_over_log_N": alpha,
        "linear_child_solver_materialized_time_exponent": alpha,
        "explicit_child_peak_space_exponent": alpha,
    }


def materialized(alpha: float, r: float, u: float, t: float, s: float,
                 h: float = 0.0, v: float = 0.0) -> dict:
    return {
        "time": max(r, alpha * t, h),
        "space": max(u, alpha, alpha * s, v),
    }


def on_demand(alpha: float, g: float, v: float, t: float, s: float,
              h: float = 0.0, recon_space: float = 0.0) -> dict:
    return {
        "time": max(g + alpha * t, h),
        "space": max(v, alpha * s, recon_space),
    }


def multi_child(alpha: float, mu: float, r: float, u: float,
                t: float, s: float, store_all: bool = False) -> dict:
    space = max(u, alpha * s, alpha + mu if store_all else alpha)
    return {"time": max(r, mu + alpha * t), "space": space}


def relaxed_proxy(n: int) -> dict:
    nbits = n * math.ceil(math.log2(n + 1))
    b = math.sqrt(n / 12.0)
    e = math.sqrt(n / 3.0) - 0.25
    equality_b = n / 3.0
    return {
        "n_variables": n,
        "canonical_N_bits": nbits,
        "continuous_b_star": b,
        "minimum_proxy_log2_time": e,
        "minimum_additive_polynomial_exponent": e / math.log2(nbits),
        "equality_b": equality_b,
        "equality_additive_polynomial_exponent": equality_b / math.log2(nbits),
    }


def integer_proxy_1200() -> dict:
    rows = []
    for b in range(1, 1201):
        q = max(0, math.ceil(1200 / (12 * b) - 0.25))
        rows.append((b, q, b + q))
    minimum = min(x[2] for x in rows)
    ties = [list(x) for x in rows if x[2] == minimum]
    pareto = []
    for x in rows:
        # coordinates are (time exponent b+q, explicit table exponent b)
        dominated = any(
            y[2] <= x[2] and y[0] <= x[0] and (y[2] < x[2] or y[0] < x[0])
            for y in rows
        )
        if not dominated:
            pareto.append(list(x))
    equality = next(list(x) for x in rows if x[1] == 0)
    return {"minimum": minimum, "ties_b_q_t": ties,
            "pareto_b_q_t": pareto, "first_q_zero_b_q_t": equality}


def main() -> None:
    projection = [projection_sizes(2 ** k)
                  for k in (2, 4, 8, 16, 32, 64, 128, 256, 512)]
    # The effective exponent approaches two from below.
    assert all(projection[i]["effective_size_exponent_log_M_over_log_N"] <
               projection[i + 1]["effective_size_exponent_log_M_over_log_N"]
               for i in range(len(projection) - 1))
    assert projection[-1]["effective_size_exponent_log_M_over_log_N"] > 1.97

    transfer_examples = {
        "materialized_alpha_0.6": materialized(.6, 1.1, .3, 3.0, .1),
        "on_demand_alpha_0.6": on_demand(.6, .15, .3, 3.0, .1),
        "N_to_mu_children_sequential": multi_child(.55, .25, 1.0, .2, 2.0, .1),
        "N_to_mu_children_store_all": multi_child(.55, .25, 1.0, .2, 2.0, .1, True),
    }
    expected = {
        "materialized_alpha_0.6": (1.8, .6),
        "on_demand_alpha_0.6": (1.95, .3),
        "N_to_mu_children_sequential": (1.35, .55),
        "N_to_mu_children_store_all": (1.35, .8),
    }
    for key, pair in expected.items():
        assert math.isclose(transfer_examples[key]["time"], pair[0])
        assert math.isclose(transfer_examples[key]["space"], pair[1])

    proxy = [relaxed_proxy(n) for n in (1200, 10_000, 100_000, 1_000_000, 100_000_000)]
    # Both normalized additions diverge; finite-n plots can hide this.
    assert all(proxy[i]["minimum_additive_polynomial_exponent"] <
               proxy[i + 1]["minimum_additive_polynomial_exponent"]
               for i in range(len(proxy) - 1))
    assert all(proxy[i]["equality_additive_polynomial_exponent"] <
               proxy[i + 1]["equality_additive_polynomial_exponent"]
               for i in range(len(proxy) - 1))

    out = {
        "run_id": "REDUCTION-FRONTIER-TRANSFER-REFEREE207",
        "status": {
            "symbolic_results": "PROVED/EXACT in accompanying report",
            "finite_results": "COMPUTATIONAL arithmetic controls",
            "P_vs_NP": "OPEN",
        },
        "seed": None,
        "projection_blowup_control": projection,
        "transfer_examples": transfer_examples,
        "static_proxy_normalization": proxy,
        "n1200_integer_control": integer_proxy_1200(),
        "checks": {
            "projection_rows": len(projection),
            "proxy_rows": len(proxy),
            "all_assertions_passed": True,
            "runtime_chunking": "single dependency-free invocation, designed under 1 second",
        },
        "limitations": [
            "Arithmetic controls are not native Turing-machine measurements.",
            "The selector projection is a representation blowup counterexample, not a SAT lower bound.",
            "No arbitrary-SAT reduction or P-versus-NP implication is established.",
        ],
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
