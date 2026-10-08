#!/usr/bin/env python3
"""Exact checks for PREFIX-FALLBACK-NOEDGE1.

The proof is symbolic.  This executable checks exact rational witnesses for
the scalar obstruction, exhausts small positive phase weights for directed
cycles, and records hostile-control envelopes.  It is intentionally bounded
to finish well below the repository's 30-second limit.
"""

from __future__ import annotations

import argparse
import json
import signal
import time
from fractions import Fraction
from itertools import product
from pathlib import Path


def fstr(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}"


def prefix(pair: tuple[Fraction, Fraction], guard: tuple[Fraction, Fraction]):
    return tuple(max(x, g) for x, g in zip(pair, guard))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--seed", type=int, default=20261008)
    parser.add_argument("--max-weight", type=int, default=4)
    parser.add_argument("--max-cycle", type=int, default=4)
    args = parser.parse_args()

    signal.alarm(25)
    started = time.perf_counter()
    guard = (Fraction(1), Fraction(2, 3))
    lam = Fraction(2, 3)
    drift = Fraction(1, 100)
    directions = [
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(1)),
        (Fraction(1), Fraction(1)),
        (Fraction(2), Fraction(3)),
    ]

    # Scalar counterwitnesses: for z=r*u above the guard, F(z)=z and
    # (1-lambda)<v,z> > c.  The selected integer r is exact.
    scalar = []
    for v in directions:
        u = tuple(max(Fraction(1), x) for x in v)
        dot = sum(x * y for x, y in zip(v, u))
        if dot == 0:
            continue
        threshold = drift / ((1 - lam) * dot)
        r = max(2, threshold.numerator // threshold.denominator + 1)
        z = tuple(Fraction(r) * x for x in u)
        lhs = sum(x * y for x, y in zip(v, prefix(z, guard)))
        rhs = lam * sum(x * y for x, y in zip(v, z)) + drift
        assert lhs > rhs
        scalar.append(
            {
                "v": [fstr(x) for x in v],
                "u": [fstr(x) for x in u],
                "r": r,
                "lhs": fstr(lhs),
                "rhs": fstr(rhs),
            }
        )

    # For a pure identity-leading edge q->r, every-coordinate asymptotics
    # require v_r <= lambda*v_q.  Exhaust all small positive integer weights
    # and confirm no directed cycle can satisfy all such inequalities.
    checked = 0
    feasible_cycles = 0
    minimal_failed_edge_histogram: dict[str, int] = {}
    weight_vectors = [tuple(map(Fraction, w)) for w in product(range(1, args.max_weight + 1), repeat=2)]
    for k in range(1, args.max_cycle + 1):
        for weights in product(weight_vectors, repeat=k):
            checked += 1
            failed = 0
            for i in range(k):
                source = weights[i]
                target = weights[(i + 1) % k]
                if not all(target[j] <= lam * source[j] for j in range(2)):
                    failed += 1
            if failed == 0:
                feasible_cycles += 1
            minimal_failed_edge_histogram[str(failed)] = minimal_failed_edge_histogram.get(str(failed), 0) + 1
    assert feasible_cycles == 0

    # Hostile controls: source carry/padding leaves a current-scale fallback;
    # easy-family success can be constant but the worst-case envelope is still
    # the fallback max; independent products take coordinatewise maxima.
    hostile_pairs = [
        (Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(1, 2)),
        (Fraction(3, 2), Fraction(1, 4)),
        (Fraction(5), Fraction(7, 3)),
    ]
    hostile = []
    for z in hostile_pairs:
        out = prefix(z, guard)
        assert all(a >= b for a, b in zip(out, z))
        hostile.append({"fallback": [fstr(x) for x in z], "envelope": [fstr(x) for x in out]})

    result = {
        "claim": "PREFIX-FALLBACK-NOEDGE1",
        "status": "COMPUTATIONAL exact-rational regression supporting a symbolic proof",
        "seed": args.seed,
        "parameters": {
            "guard": [fstr(x) for x in guard],
            "lambda": fstr(lam),
            "drift": fstr(drift),
            "max_weight": args.max_weight,
            "max_cycle": args.max_cycle,
        },
        "scalar_counterwitnesses": scalar,
        "cycle_weight_assignments_checked": checked,
        "feasible_cycles": feasible_cycles,
        "failed_edge_histogram": minimal_failed_edge_histogram,
        "hostile_controls": hostile,
        "limitations": [
            "Finite enumeration is not the proof.",
            "The result concerns the certified max-envelope, not unknown tighter implementation bounds.",
            "A mixed cycle containing a genuinely contractive non-prefix edge is not excluded.",
        ],
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
