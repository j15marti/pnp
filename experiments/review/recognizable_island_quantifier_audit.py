#!/usr/bin/env python3
"""Finite audit for SYNTHESIS-0008's recognizable-island wrapper theorem.

The symbolic theorem is elementary: if a language is constant on a uniformly
recognizable set S, then any total exact decider can be guarded by the
recognizer and shortcut on S.  This program exhaustively tests the semantic
identity on all languages over an eight-element universe, all nonempty
monochromatic subsets S, and six extensionally equivalent wrapper styles.

The audit is finite evidence only.  It does not prove an asymptotic SAT lower
bound or upper bound.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path


UNIVERSE_SIZE = 8
WRAPPERS = ("DIRECT", "INTERP", "RECOMP", "DEAD", "COPY", "DELAY")


def bit(mask: int, x: int) -> int:
    return (mask >> x) & 1


def guarded_answer(language: int, subset: int, constant: int, x: int, style: str) -> int:
    """Six implementations of the same recognize-then-fallback wrapper."""
    in_subset = bool((subset >> x) & 1)
    if style == "DIRECT":
        return constant if in_subset else bit(language, x)
    if style == "INTERP":
        table = (constant, bit(language, x))
        return table[0 if in_subset else 1]
    if style == "RECOMP":
        recognized = any(y == x and ((subset >> y) & 1) for y in range(UNIVERSE_SIZE))
        return constant if recognized else bit(language, x)
    if style == "DEAD":
        _dead_semantic_object = tuple(bit(language, y) for y in range(UNIVERSE_SIZE))
        return constant if in_subset else bit(language, x)
    if style == "COPY":
        copied_subset = int(f"{subset:b}", 2)
        return constant if ((copied_subset >> x) & 1) else bit(language, x)
    if style == "DELAY":
        accumulator = 0
        for j in range(17):
            accumulator ^= j
        assert accumulator == 16
        return constant if in_subset else bit(language, x)
    raise ValueError(style)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=202610111448)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    started = time.perf_counter()
    monochromatic_pairs = 0
    semantic_checks = 0
    failures: list[dict[str, int | str]] = []
    constant_counts = {"0": 0, "1": 0}

    full = (1 << UNIVERSE_SIZE) - 1
    for language in range(1 << UNIVERSE_SIZE):
        for constant, carrier in ((1, language), (0, full ^ language)):
            subset = carrier
            while subset:
                monochromatic_pairs += 1
                constant_counts[str(constant)] += 1
                for style in WRAPPERS:
                    for x in range(UNIVERSE_SIZE):
                        semantic_checks += 1
                        got = guarded_answer(language, subset, constant, x, style)
                        expected = bit(language, x)
                        if got != expected:
                            failures.append(
                                {
                                    "language": language,
                                    "subset": subset,
                                    "constant": constant,
                                    "input": x,
                                    "style": style,
                                    "got": got,
                                    "expected": expected,
                                }
                            )
                subset = (subset - 1) & carrier

    expected_pairs = 2 * (3**UNIVERSE_SIZE) - 2 * (2**UNIVERSE_SIZE)
    assert monochromatic_pairs == expected_pairs == 12610
    assert semantic_checks == expected_pairs * UNIVERSE_SIZE * len(WRAPPERS)

    structural_controls = [
        {
            "family": "dense Horn / dual-Horn and 2SAT islands",
            "recognition": "canonical syntax scan",
            "constant_answer": "family-specific YES or NO subfamilies",
            "consequence": "treewidth or semantic-table size is not pointwise all-decider cost",
        },
        {
            "family": "affine/Tseitin islands",
            "recognition": "canonical equation template",
            "constant_answer": "rank/consistency bit",
            "consequence": "Gaussian elimination or a template shortcut can bypass chosen SAT structure",
        },
        {
            "family": "LB-0012 disconnected paired H22 products",
            "recognition": "canonical block parser",
            "constant_answer": "YES",
            "consequence": "exponential compatibility rank is not pointwise central decision work",
        },
        {
            "family": "TESTS-0007 connected paired H22 chains",
            "recognition": "canonical chain parser",
            "constant_answer": "YES",
            "consequence": "connectedness does not repair pointwise rank-to-work transfer",
        },
        {
            "family": "RT-0012 connected nonpaired H22 chains",
            "recognition": "canonical switched-chain parser",
            "constant_answer": "YES",
            "consequence": "nonpairedness does not repair pointwise rank-to-work transfer",
        },
        {
            "family": "padding, redundant clauses, alternate encodings",
            "recognition": "wrapper-aware parser",
            "constant_answer": "inherited",
            "consequence": "encoded size and optional traces alone are not pointwise work",
        },
    ]

    payload = {
        "run_id": "SYNTHESIS-0008",
        "claim": "RECOGNIZABLE-ISLAND-BARRIER1",
        "seed": args.seed,
        "universe_size": UNIVERSE_SIZE,
        "languages": 1 << UNIVERSE_SIZE,
        "monochromatic_nonempty_pairs": monochromatic_pairs,
        "expected_pairs_formula": "2*3^8-2*2^8",
        "constant_pair_counts": constant_counts,
        "wrappers": list(WRAPPERS),
        "semantic_checks": semantic_checks,
        "failures": len(failures),
        "failure_examples": failures[:10],
        "structural_controls": structural_controls,
        "quantifier_scope": {
            "retired": "forall F in P, forall exact deciders A: structural_property(F) forces large cost on F",
            "not_refuted": "forall exact deciders A, forall d, forall N0, exists F in P of length at least N0 with time_A(F)>|F|^d",
        },
        "status": "COMPUTATIONAL finite audit; symbolic wrapper theorem proved separately",
        "elapsed_seconds": time.perf_counter() - started,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["payload_sha256"] = hashlib.sha256(canonical).hexdigest()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
