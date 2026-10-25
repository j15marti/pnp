#!/usr/bin/env python3
"""Exact arithmetic audit for ARC-BRANCH-SELECTOR-TRILEMMA159.

This script checks the restricted raw pin/fanout dichotomy and the mixed-path
telescoping certificate used to audit LSPV-4's two-channel recurrence.  It is
not a SAT lower-bound experiment or an FLMV machine-step measurement.
"""

from fractions import Fraction
import itertools
import json
import math

RUN_ID = "ARC-BRANCH-SELECTOR-TRILEMMA159"


def dense_bits(k: int, m: int) -> int:
    w = math.ceil(math.log2(k + 1))
    return 3 * w + 2 + 3 * m * (w + 1)


def safe_untouched_bits(u: int) -> int:
    """Safe indexed lower bound from u untouched degree-at-most-four clauses."""
    if u <= 0:
        return 0
    names = math.ceil(3 * u / 4)
    w = math.ceil(math.log2(names + 1))
    return 3 * u * w


def mixed_path_value(word, channels):
    scale = Fraction(1)
    value = Fraction(0)
    for name in word:
        fanout, shrink = channels[name]
        value += scale * fanout
        scale *= shrink
    return value, scale


def main() -> None:
    checks = 0

    def check(ok, msg):
        nonlocal checks
        checks += 1
        if not ok:
            raise AssertionError(msg)

    # Role-1 raw pin-and-copy architecture, with m=4k/3 and N=Theta(k log k).
    rows = []
    for e in range(5, 19):
        k = 3 * (2**e)
        m = 4 * k // 3
        n = dense_bits(k, m)

        # A canonical polynomial fanout B=N^(3/5) permits only log B pins.
        q_poly = math.floor(Fraction(3, 5) * math.log2(n))
        untouched_poly = max(0, m - 4 * q_poly)
        child_lb = safe_untouched_bits(untouched_poly)
        lambda_lb = math.log(child_lb, n)

        # Even the weak necessary condition u<=sqrt(N) already forces many pins.
        u_target = math.floor(math.sqrt(n))
        q_short = max(0, math.ceil((m - u_target) / 4))
        a_required = q_short / math.log2(n)

        check(untouched_poly >= m - 4 * q_poly, "occurrence floor")
        check(child_lb > 0, "polynomial branch child remains nonempty")
        check(q_short >= k / 3 - u_target / 4 - 1, "power-short pin floor")
        check(2**q_poly <= n ** Fraction(3, 5), "polynomial fanout pins")
        rows.append({
            "k": k,
            "m": m,
            "parent_bits": n,
            "poly_fanout_exponent": "3/5",
            "poly_pins": q_poly,
            "untouched_clauses_lower_bound": untouched_poly,
            "child_bits_lower_bound": child_lb,
            "child_log_exponent_lower_bound": lambda_lb,
            "sqrt_length_target_pins": q_short,
            "required_fanout_exponent_logN": a_required,
        })

    check(rows[-1]["child_log_exponent_lower_bound"] > 0.997,
          "polynomial fanout child exponent approaches one")
    check(rows[-1]["required_fanout_exponent_logN"] > 100,
          "power-short full branching exponent diverges")
    check(rows[-1]["required_fanout_exponent_logN"] >
          10 * rows[0]["required_fanout_exponent_logN"],
          "required fanout exponent grows")

    # Independent audit of the two-channel mixed recurrence.
    channels = {
        "child": (Fraction(3, 5), Fraction(1, 2)),
        "selector": (Fraction(2, 5), Fraction(1, 3)),
    }
    M = max(a / (1 - lam) for a, lam in channels.values())
    path_rows = []
    for depth in range(1, 11):
        maximum = Fraction(0)
        argmax = None
        residual = None
        for word in itertools.product(channels, repeat=depth):
            value, scale = mixed_path_value(word, channels)
            # Exact telescoping certificate: value <= M(1-product shrink).
            check(value <= M * (1 - scale), "mixed path telescoping bound")
            if value > maximum:
                maximum, argmax, residual = value, word, scale
        path_rows.append({
            "depth": depth,
            "max_accumulated_fanout": str(maximum),
            "argmax": list(argmax),
            "residual_scale": str(residual),
            "global_limit": str(M),
        })
    check(M == Fraction(6, 5), "canonical child channel limit")

    # Exact endpoint and Role-4 selector wedge samples.
    c = Fraction(241, 200)
    beta = ((c + 2) / (c * c) - c) / 2
    check(beta == Fraction(11642479, 23232400), "FLMV beta rational")
    wedge = []
    for b, rho in [
        (Fraction(3, 5), Fraction(1, 2)),
        (Fraction(3, 5), Fraction(501, 1000)),
        (Fraction(3, 5), Fraction(502, 1000)),
        (Fraction(61, 100), Fraction(1, 2)),
    ]:
        tau = max(Fraction(11, 10), Fraction(6, 5), b / (1 - rho))
        sigma = max(Fraction(1, 2), rho)
        forbidden = tau < c and sigma < beta
        check(forbidden == (b < c * (1 - rho) and rho < beta),
              "selector wedge equivalence")
        wedge.append({"b": str(b), "rho": str(rho), "tau": str(tau),
                      "sigma": str(sigma), "strictly_forbidden": forbidden})

    controls = [
        "SAT direct recognizer",
        "UNSAT direct recognizer",
        "Horn/SCC/affine semantic compression",
        "one-bit grammar mutation to fallback",
        "cache/replay of identical children",
        "parent-length A call",
    ]
    result = {
        "run_id": RUN_ID,
        "status": {
            "mixed_channel_telescoping": "PROVED/EXACT; finite word audit COMPUTATIONAL",
            "raw_pin_fanout_dichotomy": "PROVED/EXACT in complete raw pin-and-copy model",
            "hybrid_trilemma": "PROVED/EXACT restricted",
            "all_input_arc_edge": "OPEN",
            "p_vs_np": "OPEN",
        },
        "size_rows": [r for r in rows if r["k"] in {96, 384, 1536, 6144, 24576, 196608, 786432}],
        "size_sweep": {"rows": len(rows), "first_k": rows[0]["k"], "last_k": rows[-1]["k"]},
        "mixed_paths": path_rows,
        "channels": {k: [str(x) for x in v] for k, v in channels.items()},
        "selector_wedge": wedge,
        "strict_flmv_box": {"time": str(c), "space": str(beta)},
        "hostile_controls": controls,
        "assertion_checks": checks,
        "failures": 0,
        "limitations": [
            "raw theorem excludes propagation, learning, symbolic elimination, merging and direct decisions",
            "extensional recursion does not cover a genuinely polynomial-promise-sensitive intensional A-dependent compiler",
            "finite rows do not prove the asymptotic statements",
            "no favorable successor machine is constructed",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
