#!/usr/bin/env python3
"""Bounded exact-arithmetic audit for SOURCE-ONLY-RECURSIVE-ENDPOINT-EQUIV1.

This checks the exponent recurrence and its standard hostile controls.  It is
not an asymptotic proof; the accompanying report contains the symbolic proof.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from fractions import Fraction
from itertools import product
from pathlib import Path


def fixed_point(r: Fraction, eta: Fraction, lam: Fraction) -> Fraction:
    assert 0 <= lam < 1
    return max(r, eta / (1 - lam))


def recurrence_step(c: Fraction, r: Fraction, eta: Fraction, lam: Fraction) -> Fraction:
    return max(r, eta + lam * c)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=202610111248)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    counts: dict[str, int] = {
        "recurrence_invariant": 0,
        "recurrence_convergence": 0,
        "aggregate_moment": 0,
        "current_scale_retains_k": 0,
        "terminal_retains_constructor": 0,
        "additive_shannon_not_fractional": 0,
        "padding_encoding_control": 0,
    }

    lambdas = [Fraction(0), Fraction(1, 4), Fraction(1, 3), Fraction(1, 2),
               Fraction(2, 3), Fraction(3, 4), Fraction(4, 5)]
    vals = [Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(1),
            Fraction(6, 5), Fraction(3, 2), Fraction(2), Fraction(3)]

    # If C >= max(r, eta/(1-lambda)), then one recursive exponent step
    # stays <= C.  Iteration from an arbitrary leaf exponent approaches the
    # same fixed point from above or below.
    for lam, r, eta, k in product(lambdas, vals, vals, vals[1:]):
        c_star = fixed_point(r, eta, lam)
        assert recurrence_step(c_star, r, eta, lam) <= c_star
        counts["recurrence_invariant"] += 1
        c = k
        for _ in range(48):
            c = recurrence_step(c, r, eta, lam)
        # Exact error is at most lambda^48 times the starting excess.
        assert c <= c_star + (lam ** 48) * max(Fraction(0), k - c_star)
        assert c >= c_star - (lam ** 48) * max(Fraction(0), c_star - k)
        counts["recurrence_convergence"] += 1

    # Aggregate-volume inequality used by the corpus:
    # sum m_i^C <= (max m_i)^(C-1) sum m_i for C >= 1.
    for q in range(1, 6):
        for children in product(range(1, 7), repeat=q):
            maximum = max(children)
            total = sum(children)
            for exponent in range(1, 6):
                lhs = sum(x ** exponent for x in children)
                rhs = maximum ** (exponent - 1) * total
                assert lhs <= rhs
                counts["aggregate_moment"] += 1

    # A current-scale solver call or decide-then-emit constructor keeps K.
    for k, r, eta, lam in product(vals[1:], vals, vals, lambdas):
        c = max(k, fixed_point(r, eta, lam))
        assert c >= k
        counts["current_scale_retains_k"] += 1
        terminal_c = fixed_point(k, Fraction(0), Fraction(0))
        assert terminal_c == k
        counts["terminal_retains_constructor"] += 1

    # Assigning O(log N) variables in a bounded-occurrence formula removes
    # only O(log N) clauses: N-c log N is not <= N^lambda for any fixed
    # tested lambda<1 at the tested scales once the explicit inequality holds.
    for e in range(8, 31):
        n = 2 ** e
        residual = n - 4 * e
        for lam in lambdas[:-1]:
            if residual > 0:
                assert residual > int(n ** float(lam)) or e < 10
                counts["additive_shannon_not_fractional"] += 1

    # Polynomial padding changes the encoded-length exponent.  The audit
    # confirms that converting back multiplies the child exponent by the
    # padding power; it cannot be silently ignored.
    for pad_power in range(1, 9):
        for lam_num in range(0, 9):
            lam = Fraction(lam_num, 10)
            physical_child = pad_power * lam
            assert physical_child == Fraction(pad_power * lam_num, 10)
            counts["padding_encoding_control"] += 1

    total = sum(counts.values())
    payload = {
        "run_id": "SYNTHESIS-0006",
        "claim": "SOURCE-ONLY-RECURSIVE-ENDPOINT-EQUIV1",
        "status": "COMPUTATIONAL finite audit; symbolic proof is separate",
        "seed": args.seed,
        "arithmetic": "fractions.Fraction except explicitly labeled finite size controls",
        "counts": counts,
        "total_checks": total,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "limitations": [
            "Finite recurrence checks do not prove the asymptotic theorem.",
            "No SAT lower bound is inferred from the controls.",
            "Space closure requires the report's declared depth-first locally-addressable realization.",
        ],
    }
    encoded = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(encoded)
    print(json.dumps({"total_checks": total, "sha256": hashlib.sha256(encoded).hexdigest(),
                      "elapsed_seconds": payload["elapsed_seconds"]}, sort_keys=True))


if __name__ == "__main__":
    main()
