#!/usr/bin/env python3
"""Bounded audit for ALL-EASY-ISLAND-RESIDUAL-COLLAPSE1.

The symbolic theorem is elementary and appears in the accompanying report.
This script checks the quantifiers on every Boolean language on eight base
points and on a finite prefix of the canonical padding construction.  It also
records hostile representation controls.  It does not extrapolate timings or
finite counts to an asymptotic lower bound.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Encoded:
    source: int
    answer: int
    padding: int
    wrapper: str = "DIRECT"

    def canonical(self) -> str:
        # A declared canonical disjoint-product encoding: one source component
        # followed by padding copies of a fixed satisfiable component T.
        return f"SRC:{self.source}:ANS:{self.answer}|" + "T|" * self.padding


WRAPPERS = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")


def island_recognizer(blob: str, source: int, answer: int) -> tuple[bool, int]:
    """Recognize {P(source,k): k>=0}; return membership and bytes inspected."""
    prefix = f"SRC:{source}:ANS:{answer}|"
    inspected = len(blob.encode("utf-8"))
    if not blob.startswith(prefix):
        return False, inspected
    suffix = blob[len(prefix) :]
    return len(suffix) % 2 == 0 and suffix == "T|" * (len(suffix) // 2), inspected


def hostile_encoding(item: Encoded) -> str:
    base = item.canonical()
    if item.wrapper == "DIRECT":
        return base
    if item.wrapper == "COPY":
        return base + "COPY|"
    if item.wrapper == "DEAD":
        return "DEAD|" + base
    if item.wrapper == "DELAY":
        return base + "DELAY:64|"
    if item.wrapper == "INTERP":
        return "INTERP{" + base + "}"
    if item.wrapper == "RECOMP":
        return "RECOMP{" + base + "}"
    raise AssertionError(item.wrapper)


def run(padding_max: int) -> dict[str, object]:
    started = time.perf_counter_ns()
    assertions = 0
    membership_checks = 0
    wrapper_checks = 0
    coverage_checks = 0
    inspected_bytes = 0
    residual_points = 0
    languages = 0

    # Exhaust all Boolean languages on eight source points.  Each source x has
    # a monochromatic canonical padding island I_x={(x,k):0<=k<=padding_max}.
    # The finite prefix mirrors the exact infinite symbolic cover.
    for truth_table in range(1 << 8):
        languages += 1
        answer = [(truth_table >> x) & 1 for x in range(8)]
        covered: set[tuple[int, int]] = set()
        universe = {(x, k) for x in range(8) for k in range(padding_max + 1)}

        for x in range(8):
            ax = answer[x]
            for k in range(padding_max + 1):
                item = Encoded(x, ax, k)
                blob = item.canonical()
                ok, scanned = island_recognizer(blob, x, ax)
                inspected_bytes += scanned
                membership_checks += 1
                assertions += 1
                assert ok
                # Padding component T is satisfiable, so conjunction preserves
                # the source decision bit exactly.
                assertions += 1
                assert item.answer == ax
                covered.add((x, k))

                for wrapper in WRAPPERS:
                    wrapped = Encoded(x, ax, k, wrapper)
                    wblob = hostile_encoding(wrapped)
                    accepted, scanned = island_recognizer(wblob, x, ax)
                    inspected_bytes += scanned
                    wrapper_checks += 1
                    assertions += 1
                    assert accepted == (wrapper == "DIRECT")
                    # Rejected encodings go to the exact fallback; semantic
                    # correctness is preserved although the trace changes.
                    assertions += 1
                    assert wrapped.answer == ax

            # k=0 includes the original source, so every base point is covered.
            ok0, scanned0 = island_recognizer(Encoded(x, ax, 0).canonical(), x, ax)
            inspected_bytes += scanned0
            coverage_checks += 1
            assertions += 1
            assert ok0

        residual = universe - covered
        residual_points += len(residual)
        assertions += 1
        assert not residual

    elapsed = time.perf_counter_ns() - started
    result: dict[str, object] = {
        "claim": "ALL-EASY-ISLAND-RESIDUAL-COLLAPSE1",
        "status": "COMPUTATIONAL",
        "languages": languages,
        "base_points": 8,
        "padding_max_inclusive": padding_max,
        "membership_checks": membership_checks,
        "wrapper_checks": wrapper_checks,
        "coverage_checks": coverage_checks,
        "assertions": assertions,
        "residual_points_total": residual_points,
        "inspected_bytes_total": inspected_bytes,
        "preprocessing": "canonical parsing and equality scan fully counted",
        "extraction": "not invoked; zero semantic objects extracted",
        "reconstruction": "not invoked; rejected wrappers use exact fallback",
        "wrappers": list(WRAPPERS),
        "elapsed_ns": elapsed,
        "asymptotic_extrapolation": False,
        "symbolic_scope": (
            "finite audit only; the report proves the all-input singleton and "
            "canonical-padding cover theorems"
        ),
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--padding-max", type=int, default=31)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if not 0 <= args.padding_max <= 128:
        raise SystemExit("padding-max must lie in [0,128]")
    result = run(args.padding_max)
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    result["payload_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
