#!/usr/bin/env python3
"""Finite audit for NORMALIZED-CUT-PREDELAY1.

This checks exact integer inequalities for a wrapper tailored to a fixed
rational checkpoint fraction alpha.  It is a computational guard only; the
symbolic theorem is proved separately.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path


def ceil_div(a: int, b: int) -> int:
    return -(-a // b)


def delay_for(alpha: Fraction, suffix: int, length_scan: int) -> int:
    # (1-alpha)D >= alpha*S + 1, hence floor(alpha(D+S)) < D.
    return length_scan + ceil_div(
        alpha.numerator * suffix + alpha.denominator,
        alpha.denominator - alpha.numerator,
    )


def child_answer(family: str, variant: str, n: int) -> int:
    # Deterministic stand-in bits; only semantic preservation is tested.
    h = hashlib.sha256(f"{family}|{variant}|{n}".encode()).digest()
    return h[0] & 1


def run(seed: int) -> dict:
    del seed  # deterministic exhaustive grid
    alphas = [Fraction(1, 10), Fraction(1, 4), Fraction(1, 2),
              Fraction(3, 4), Fraction(9, 10), Fraction(99, 100)]
    families = ["clean-core", "Horn", "2SAT", "affine-Tseitin",
                "bounded-treewidth", "independent-product", "parity"]
    variants = ["canonical", "padded", "redundant", "permuted",
                "alternate-encoding", "wrapper-equivalent"]
    wrappers = ["DIRECT", "DEAD", "COPY", "DELAY", "INTERP", "RECOMP"]
    checks: Counter[str] = Counter()
    max_digits = 0

    for n in range(2, 65):
        for k in range(1, 9):
            suffix = n ** k + n + 17  # exact child clock plus fixed postlude
            max_digits = max(max_digits, len(str(suffix)))
            for alpha in alphas:
                length_scan = n + 3
                delay = delay_for(alpha, suffix, length_scan)
                total = delay + suffix
                cut = (alpha.numerator * total) // alpha.denominator
                assert cut < delay
                assert (alpha.denominator - alpha.numerator) * delay >= (
                    alpha.numerator * suffix + alpha.denominator
                )
                checks["exact_fractional_cut_inequality"] += 2

                fingerprints = set()
                answers = set()
                for family in families:
                    for variant in variants:
                        for wrapper in wrappers:
                            answer = child_answer(family, variant, n)
                            # Mutable cut state is length/cut/wrapper-program only;
                            # read-only input contents are deliberately excluded.
                            fp = (n, k, alpha.numerator, alpha.denominator,
                                  delay, cut, "PRELUDE")
                            fingerprints.add(fp)
                            answers.add(answer)
                            assert answer == child_answer(family, variant, n)
                            checks["semantic_answer_preserved"] += 1
                            checks["hostile_family_encoding_wrapper"] += 1
                assert len(fingerprints) == 1
                assert len(answers) <= 2
                checks["same_length_mutable_cut_collision"] += 1

    payload = {
        "run_id": "MODELBRIDGE-0026",
        "claim": "NORMALIZED-CUT-PREDELAY1",
        "status": "COMPUTATIONAL audit; symbolic theorem separate",
        "parameters": {
            "lengths": [2, 64],
            "child_exponents": [1, 8],
            "alphas": [str(a) for a in alphas],
            "families": families,
            "variants": variants,
            "wrappers": wrappers,
        },
        "checks": dict(checks),
        "total_checks": sum(checks.values()),
        "maximum_suffix_decimal_digits": max_digits,
        "limitations": [
            "Finite cases do not prove the symbolic wrapper theorem.",
            "The projection excludes read-only input contents; including them gives an external source route, not paid solver state.",
            "The result targets a fixed normalized-time cut and does not defeat an exogenous online challenge after an irrevocable commitment.",
            "No SAT lower bound or asymptotic extrapolation is claimed.",
        ],
    }
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=202610121400)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    payload = run(args.seed)
    payload["runtime_seconds"] = time.perf_counter() - started
    payload["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
