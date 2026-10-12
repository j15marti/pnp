#!/usr/bin/env python3
"""Finite audit for clean-core time-lower-bound quantifier variants.

This is bookkeeping evidence only.  It does not decide any asymptotic claim.
Every tested family is explicit and each loop is deliberately small.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from pathlib import Path


def runtime(kind: str, n: int, p: int = 2) -> int:
    if kind == "poly":
        return 3 * n**p + 7
    if kind == "sqrt_exp":
        return 2 ** math.isqrt(n)
    if kind == "quasipoly":
        return n ** max(1, int(math.log2(max(2, math.log2(n + 2)))))
    if kind == "exp":
        return 2**n
    raise ValueError(kind)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    checks = 0
    failures: list[dict[str, object]] = []

    # Polynomial hostile controls and wrapper-equivalent polynomial overheads.
    controls = {
        "2SAT": 2,
        "Horn": 2,
        "affine_gaussian": 3,
        "bounded_treewidth": 4,
        "independent_products": 5,
    }
    wrappers = {"DIRECT": 0, "COPY": 1, "DEAD": 2, "DELAY": 4,
                "INTERP": 3, "RECOMP": 5}
    polynomial_witnesses = []
    for control, base_degree in controls.items():
        for wrapper, overhead in wrappers.items():
            degree = max(base_degree, overhead)
            d = degree + 1
            C = 10
            n0 = 64
            ok = all(runtime("poly", n, degree) <= C * n**d
                     for n in range(n0, 257))
            checks += 193
            if not ok:
                failures.append({"control": control, "wrapper": wrapper,
                                 "test": "eventual_polynomial_bound"})
            polynomial_witnesses.append({"control": control, "wrapper": wrapper,
                                         "degree": degree, "d": d,
                                         "C": C, "N0": n0, "passes": ok})

    # A fixed exponent is not a P-vs-NP endpoint: n^(c+1) beats n^c but is polynomial.
    fixed_exponent = []
    for c in range(1, 9):
        vals = [n ** (c + 1) > n**c for n in range(2, 129)]
        checks += len(vals)
        fixed_exponent.append({"c": c, "polynomial_degree": c + 1,
                               "beats_fixed_exponent": all(vals)})
        if not all(vals):
            failures.append({"c": c, "test": "fixed_exponent_countermodel"})

    # Without a cofinal threshold, n=1 can witness T(1)>1^d for every d.
    threshold_omission = []
    for d in range(0, 17):
        ok = 2 > 1**d
        checks += 1
        threshold_omission.append({"d": d, "N": 1, "T": 2, "passes": ok})
        if not ok:
            failures.append({"d": d, "test": "threshold_omission"})

    # Pointwise nonuniformity: a different hardwired machine is constant-time
    # on each selected length, while no single machine is selected globally.
    lengths = list(range(1, 65))
    pointwise = [{"N": n, "selected_machine": f"A_{n}", "time_on_length": 1}
                 for n in lengths]
    checks += len(pointwise)

    # Polynomially related encodings/padding preserve polynomiality after
    # explicit exponent conversion.  This does not cover arbitrary padding.
    encoding_checks = []
    for p in range(1, 9):
        for a in range(1, 6):
            for n in range(2, 65):
                encoded_n = n**a
                original_t = n**p
                ok = original_t <= encoded_n ** math.ceil(p / a)
                checks += 1
                if not ok:
                    failures.append({"p": p, "a": a, "n": n,
                                     "test": "polynomial_encoding_conversion"})
            encoding_checks.append({"source_degree": p, "encoding_power": a,
                                    "target_degree": math.ceil(p / a)})

    # Finite superpolynomial proxies: only record which bounded obligations
    # happen to pass; never promote these rows to an asymptotic theorem.
    proxy_rows = []
    for kind in ("sqrt_exp", "quasipoly", "exp"):
        for d in range(0, 7):
            witnesses = []
            for n0 in (8, 16, 32, 64):
                witness = next((n for n in range(n0, 257)
                                if runtime(kind, n) > n**d), None)
                checks += 257 - n0
                witnesses.append({"N0": n0, "witness": witness})
            proxy_rows.append({"kind": kind, "d": d, "bounded_witnesses": witnesses})

    payload = {
        "experiment": "clean_core_time_quantifier_normal_form_audit",
        "status": "COMPUTATIONAL",
        "scope_warning": "Finite audit only; no asymptotic or P-vs-NP inference.",
        "checks": checks,
        "failures": failures,
        "polynomial_controls_and_wrappers": polynomial_witnesses,
        "fixed_exponent_countermodels": fixed_exponent,
        "threshold_omission_countermodel": threshold_omission,
        "pointwise_nonuniform_family": pointwise,
        "polynomial_encoding_conversions": encoding_checks,
        "superpolynomial_proxy_rows": proxy_rows,
        "elapsed_seconds": time.perf_counter() - started,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"checks": checks, "failures": len(failures),
                      "elapsed_seconds": payload["elapsed_seconds"],
                      "payload_sha256": payload["payload_sha256"]}, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
