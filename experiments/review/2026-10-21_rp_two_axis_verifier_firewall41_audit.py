#!/usr/bin/env python3
"""Finite audit for RP-TWO-AXIS-VERIFIER-FIREWALL41."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path


@dataclass
class Stats:
    verifier_runs: int = 0
    semantic_equivalence_checks: int = 0
    density_checks: int = 0
    fourier_checks: int = 0
    replay_support_checks: int = 0
    assertions: int = 0


def parity(x: int) -> int:
    return x.bit_count() & 1


def quadratic_accept(tape: int, m: int) -> int:
    q = 0
    for j in range(0, m, 2):
        q ^= ((tape >> j) & 1) & ((tape >> (j + 1)) & 1)
    return 1 ^ q


def run_verifier(x: int, tape: int, m: int, high_fourier: bool,
                 high_replay: bool) -> tuple[int, tuple[int, ...]]:
    """Return acceptance and the exact random-address read multiplicities."""
    counts = [0] * m
    bits = [0] * m
    if high_fourier:
        for i in range(m):
            bits[i] = (tape >> i) & 1
            counts[i] += 1
            if high_replay:
                again = (tape >> i) & 1
                counts[i] += 1
                assert again == bits[i]
        rebuilt = sum(bit << i for i, bit in enumerate(bits))
        coin_accept = quadratic_accept(rebuilt, m)
    else:
        if high_replay:
            for i in range(m):
                first = (tape >> i) & 1
                second = (tape >> i) & 1
                counts[i] += 2
                assert first == second
        coin_accept = 1
    return parity(x) & coin_accept, tuple(counts)


def fwht(values: list[int]) -> list[int]:
    out = list(values)
    step = 1
    while step < len(out):
        for base in range(0, len(out), 2 * step):
            for j in range(base, base + step):
                a, b = out[j], out[j + step]
                out[j], out[j + step] = a + b, a - b
        step *= 2
    return out


def fourier_l1(truth: list[int]) -> Fraction:
    spectrum = fwht(truth)
    return Fraction(sum(abs(v) for v in spectrum), len(truth))


def audit(max_m: int, source_bits: int, stats: Stats) -> dict:
    cases = []
    for m in range(2, max_m + 1, 2):
        tapes = 1 << m
        h = m // 2
        expected_high_density = Fraction(1, 2) + Fraction(1, 1 << (h + 1))
        expected_high_l1 = Fraction(1, 2) + Fraction(1 << (h - 1), 1)
        variants = {}

        for high_fourier in (False, True):
            for high_replay in (False, True):
                key = ("high" if high_replay else "low") + "_replay__" + (
                    "high" if high_fourier else "low") + "_fourier"
                truth = []
                recurrent_sizes = set()
                for tape in range(tapes):
                    value, counts = run_verifier(
                        1, tape, m, high_fourier, high_replay
                    )
                    stats.verifier_runs += 1
                    stats.assertions += 1
                    assert value in (0, 1)
                    truth.append(value)
                    recurrent_sizes.add(sum(c > 1 for c in counts))

                density = Fraction(sum(truth), tapes)
                norm = fourier_l1(truth)
                expected_density = expected_high_density if high_fourier else Fraction(1)
                expected_norm = expected_high_l1 if high_fourier else Fraction(1)
                expected_recurrent = m if high_replay else 0
                stats.assertions += 3
                stats.density_checks += 1
                stats.fourier_checks += 1
                stats.replay_support_checks += 1
                assert density == expected_density
                assert norm == expected_norm
                assert recurrent_sizes == {expected_recurrent}
                variants[key] = {
                    "acceptance_density_on_yes": str(density),
                    "fourier_l1": str(norm),
                    "minimal_recurrent_address_support": expected_recurrent,
                }

        # Repeating and discarding reads changes the trace, not semantics.
        for high_fourier in (False, True):
            for x in range(1 << source_bits):
                for tape in range(tapes):
                    low, _ = run_verifier(x, tape, m, high_fourier, False)
                    high, _ = run_verifier(x, tape, m, high_fourier, True)
                    stats.verifier_runs += 2
                    stats.semantic_equivalence_checks += 1
                    stats.assertions += 1
                    assert low == high

        # All four implementations recognize the same parity language.
        for x in range(1 << source_bits):
            for high_fourier in (False, True):
                for high_replay in (False, True):
                    accepts = 0
                    for tape in range(tapes):
                        value, _ = run_verifier(
                            x, tape, m, high_fourier, high_replay
                        )
                        accepts += value
                        stats.verifier_runs += 1
                    stats.assertions += 1
                    if parity(x) == 0:
                        assert accepts == 0
                    else:
                        assert 2 * accepts >= tapes

        cases.append({
            "m": m,
            "language": "odd parity of source input",
            "expected_high_fourier_l1": str(expected_high_l1),
            "variants": variants,
        })
    return {"cases": cases}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-m", type=int, default=16)
    parser.add_argument("--source-bits", type=int, default=4)
    parser.add_argument(
        "--output", default="RP_TWO_AXIS_VERIFIER_FIREWALL41_raw.json"
    )
    args = parser.parse_args()
    if args.max_m < 2 or args.max_m % 2:
        raise SystemExit("--max-m must be even and at least 2")

    stats = Stats()
    body = audit(args.max_m, args.source_bits, stats)
    result = {
        "claim": "RP-TWO-AXIS-VERIFIER-FIREWALL41",
        "status": "PASS",
        "parameters": {
            "max_m": args.max_m,
            "source_bits": args.source_bits,
        },
        "theorem_checks": {
            "all_four_variants_recognize_same_parity_language": True,
            "replay_support_can_be_zero_or_m_without_semantic_change": True,
            "fourier_l1_can_be_one_or_exponential_for_same_language": True,
            "simultaneous_failure_of_both_restricted_hypotheses_is_not_language_hardness": True,
        },
        "stats": asdict(stats),
        **body,
        "scope": [
            "finite tests validate implementations, not complexity-class separation",
            "replay support is measured on the selected verifier implementation",
            "Fourier mass is measured on the selected acceptance function",
            "P versus RP and P versus NP remain open",
        ],
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(args.output).write_text(payload, encoding="utf-8")
    print(json.dumps({
        "output": args.output,
        "sha256": hashlib.sha256(payload.encode()).hexdigest(),
        "stats": asdict(stats),
        "status": "PASS",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
