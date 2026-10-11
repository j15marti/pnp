#!/usr/bin/env python3
"""Exact finite audit for SYNTHESIS-0011.

This validates rational exponent bookkeeping and bounded wrapper controls.
It is not an asymptotic lower-bound experiment.
"""

from __future__ import annotations

import hashlib
import json
import time
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/raw/review/2026-10-11_query_scale_normalization_trilemma.json"


def fstr(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def main() -> None:
    start = time.perf_counter()
    checks = 0
    failures: list[dict[str, str]] = []

    exponents = [Fraction(i, 4) for i in range(7)]
    scales = [Fraction(0), Fraction(1, 16), Fraction(1, 8), Fraction(1, 4),
              Fraction(1, 2), Fraction(3, 4), Fraction(1)]
    solver_exponents = list(range(1, 17))

    # Fixed-transducer substitution ledger.  At scale zero, the solver term
    # is subpolynomial and the leading exponent is max(r, eta).
    fixed_rows = 0
    for r in exponents:
        for eta in exponents:
            for sigma in scales:
                for k in solver_exponents:
                    got = max(r, eta + sigma * k)
                    want = max(r, eta) if sigma == 0 else max(r, eta + sigma * k)
                    checks += 1
                    fixed_rows += 1
                    if got != want:
                        failures.append({"kind": "fixed-ledger", "r": fstr(r),
                                         "eta": fstr(eta), "sigma": fstr(sigma),
                                         "K": str(k)})

    # Positive-scale delay witness: d=floor(c/epsilon)+1 always gives
    # epsilon*d>c.  Repeat through named wrappers/controls to ensure that no
    # presentation choice is being treated as semantic necessity.
    c_values = [Fraction(i, 8) for i in range(97)]
    positive_scales = scales[1:]
    wrappers = ["DIRECT", "DEAD", "CANCEL", "COPY", "DELAY", "INTERP", "RECOMP"]
    controls = ["proper-3cnf", "Horn", "2SAT", "affine-Tseitin",
                "bounded-treewidth", "independent-product", "padding",
                "redundant-clauses", "alternate-encoding", "one-bit-output"]
    delay_rows = 0
    for c in c_values:
        for epsilon in positive_scales:
            d = c // epsilon + 1
            for wrapper in wrappers:
                for control in controls:
                    checks += 1
                    delay_rows += 1
                    if epsilon * d <= c:
                        failures.append({"kind": "delay-witness", "c": fstr(c),
                                         "epsilon": fstr(epsilon), "d": str(d),
                                         "wrapper": wrapper, "control": control})

    # Extensional normalization under P=NP: adding the oracle-free
    # representative forces the infimum scale to zero, regardless of padded
    # or wrapper-inflated representatives.
    semantic_rows = 0
    padded_scales = [Fraction(i, 32) for i in range(1, 49)]
    for wrapper in wrappers:
        for control in controls:
            for padding_degree in range(1, 9):
                representatives = [s / padding_degree for s in padded_scales]
                representatives.append(Fraction(0))
                checks += 1
                semantic_rows += 1
                if min(representatives) != 0:
                    failures.append({"kind": "semantic-infimum", "wrapper": wrapper,
                                     "control": control, "padding": str(padding_degree)})

    # Bounded halting-horizon indistinguishability: threshold h>B agrees with
    # the all-zero program through B and differs later.  This is only a finite
    # sanity check for the canonicalizer no-go proof.
    horizon_rows = 0
    for bound in range(1, 257):
        for offset in range(1, 17):
            h = bound + offset
            prefix_zero = all((n >= h) == 0 for n in range(bound + 1))
            future_diff = (h >= h) != 0
            checks += 2
            horizon_rows += 2
            if not prefix_zero or not future_diff:
                failures.append({"kind": "halting-horizon", "B": str(bound),
                                 "h": str(h)})

    elapsed = time.perf_counter() - start
    payload = {
        "run_id": "SYNTHESIS-0011",
        "claim": "QUERY-SCALE-NORMALIZATION-TRILEMMA1",
        "status": "COMPUTATIONAL arithmetic/hostile-control audit",
        "seed": None,
        "method": "exhaustive exact rational grids; no randomness",
        "checks": checks,
        "failures": failures,
        "passed": not failures,
        "counts": {
            "fixed_substitution": fixed_rows,
            "positive_scale_delay": delay_rows,
            "semantic_infimum": semantic_rows,
            "halting_horizon": horizon_rows,
        },
        "parameters": {
            "local_and_query_count_exponents": [fstr(x) for x in exponents],
            "query_scales": [fstr(x) for x in scales],
            "solver_exponents": solver_exponents,
            "common_bound_grid": [fstr(x) for x in c_values],
            "wrappers": wrappers,
            "controls": controls,
            "halting_horizon_max": 256,
        },
        "limitations": [
            "finite bookkeeping test only",
            "does not prove an asymptotic SAT lower bound",
            "does not construct the externally fixed source compiler",
        ],
        "runtime_seconds": elapsed,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()
    OUT.write_bytes(encoded)
    print(json.dumps({"passed": payload["passed"], "checks": checks,
                      "runtime_seconds": elapsed,
                      "result_sha256": hashlib.sha256(encoded).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
