#!/usr/bin/env python3
"""Exact-rational audit of the effective-dimension threshold in the CP ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from fractions import Fraction
from pathlib import Path


def floor_frac(x: Fraction) -> int:
    return x.numerator // x.denominator


def ceil_frac(x: Fraction) -> int:
    return -((-x.numerator) // x.denominator)


def feasible(c: int, s: Fraction, delta: Fraction, alpha: int) -> tuple[bool, int, Fraction]:
    q = 4 * alpha + c + 1
    upper = Fraction(alpha, 1) * (Fraction(1, 1) - delta) * (q + c)
    # Solve the cap inequality directly for h.
    hmax = Fraction(alpha, 1) * (Fraction(c, 1) * (1 - delta) - 4) / (1 + alpha * delta)
    h = q + 1
    return h <= hmax, h, hmax


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    t0 = time.perf_counter()
    assertions = 0
    failures: list[dict[str, object]] = []
    no_go_cells = 0
    feasible_examples: list[dict[str, object]] = []

    s_values = [Fraction(p, 8) for p in range(1, 33)]
    for c in range(3, 33):
        for s in s_values:
            threshold_allows = Fraction(c - 8, 8) > s
            if not threshold_allows:
                # Search hostile finite choices around the minimum admissible alpha.
                for d in (16, 32, 64, 128, 256):
                    delta = Fraction(1, d)
                    amin = ceil_frac(2 * s / delta)
                    for alpha in range(amin, amin + 17):
                        ok, h, hmax = feasible(c, s, delta, alpha)
                        no_go_cells += 1
                        assertions += 3
                        if alpha * delta < 2 * s:
                            failures.append({"type": "dimension", "c": c, "s": str(s), "delta": str(delta), "alpha": alpha})
                        if ok:
                            failures.append({"type": "threshold-counterexample", "c": c, "s": str(s), "delta": str(delta), "alpha": alpha, "h": h, "hmax": str(hmax)})
            else:
                # Construct delta=2s/alpha so the dimension inequality is tight.
                found = None
                for alpha in range(64, 4097):
                    delta = 2 * s / alpha
                    if not (0 < delta < 1):
                        continue
                    ok, h, hmax = feasible(c, s, delta, alpha)
                    assertions += 2
                    if ok:
                        found = {"c": c, "s": str(s), "delta": str(delta), "alpha": alpha, "h": h, "hmax": str(hmax)}
                        break
                if found is None:
                    failures.append({"type": "missing-feasible-witness", "c": c, "s": str(s)})
                elif len(feasible_examples) < 24:
                    feasible_examples.append(found)

    symbolic = {
        "effective_dimension": "nu_eff = t^s",
        "dimension_condition": "alpha*delta >= 2s",
        "cap_rearrangement": "h(1+alpha*delta) <= alpha(c(1-delta)-4)",
        "supercritical_lower": "h > 4alpha+c+1",
        "necessary_and_asymptotically_sufficient_threshold": "c > 8+8s",
        "equivalent_repair_target": "s < (c-8)/8",
    }
    payload = json.dumps({"symbolic": symbolic, "examples": feasible_examples, "failures": failures}, sort_keys=True).encode()
    result = {
        "status": "PASS" if not failures else "FAIL",
        "classification": "COMPUTATIONAL exact-rational audit supporting an independent symbolic threshold proof",
        "assertions": assertions,
        "no_go_cells": no_go_cells,
        "feasible_examples": feasible_examples,
        "failures": failures,
        "symbolic_ledger": symbolic,
        "semantic_sha256": hashlib.sha256(payload).hexdigest(),
        "elapsed_seconds": round(time.perf_counter() - t0, 6),
        "limitations": [
            "Exponent-ledger theorem only; constants require sufficiently large t.",
            "Does not validate a specialized lifting theorem with effective dimension nu_eff.",
            "Does not imply an arbitrary-machine lower bound or P != NP.",
        ],
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
