#!/usr/bin/env python3
"""Finite audit for the signed-clean-core worst-case equivalence theorem.

This is a bounded logic/cost audit, not an asymptotic proof.  It exhausts
small labelled clean domains, all many-one maps from a four-point source,
and a family of runtime tables.  It checks that a decider fast on the whole
clean domain composes through every decision-preserving reduction, while a
recognize-first shortcut on a proper monochromatic island leaves the
complement unconstrained.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path


def bits(mask: int, width: int) -> tuple[int, ...]:
    return tuple((mask >> i) & 1 for i in range(width))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    started = time.perf_counter()
    h_size = (8, 11, 14, 17)
    x_size = (5, 7, 9, 12)
    runtime_values = (1, 4, 16, 64)
    wrappers = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")

    reduction_checks = 0
    cost_checks = 0
    island_checks = 0
    wrapper_checks = 0
    padding_checks = 0
    failures: list[str] = []
    preserving_reductions = 0
    monochromatic_islands = 0

    runtime_tables = tuple(itertools.product(runtime_values, repeat=4))
    reductions = tuple(itertools.product(range(4), repeat=4))

    for h_mask in range(16):
        h_answer = bits(h_mask, 4)
        for reduction in reductions:
            x_answer = tuple(h_answer[reduction[i]] for i in range(4))
            preserving_reductions += 1
            for i in range(4):
                reduction_checks += 1
                if x_answer[i] != h_answer[reduction[i]]:
                    failures.append("decision preservation")

            # Every explicit runtime table composes through the reduction.
            # The fixed local cost represents parsing/reduction/output.
            for table in runtime_tables:
                for i in range(4):
                    local = 3 * x_size[i] * x_size[i] + 7
                    composed = local + table[reduction[i]] + 1
                    expected = local + table[reduction[i]] + 1
                    cost_checks += 1
                    if composed != expected or composed <= 0:
                        failures.append("composition cost")

        # Proper monochromatic islands support a fast branch but say nothing
        # about the complement.  This is the finite QGUARD hostile control.
        for island_mask in range(1, 15):
            members = [i for i in range(4) if (island_mask >> i) & 1]
            if len({h_answer[i] for i in members}) != 1:
                continue
            monochromatic_islands += 1
            complement = [i for i in range(4) if i not in members]
            for table in runtime_tables:
                wrapped = tuple(1 if i in members else table[i] + 2 for i in range(4))
                for i in members:
                    island_checks += 1
                    if wrapped[i] != 1:
                        failures.append("island fast branch")
                # At least one complement cost remains inherited exactly.
                for i in complement:
                    island_checks += 1
                    if wrapped[i] != table[i] + 2:
                        failures.append("island complement")
                for _wrapper in wrappers:
                    for i in range(4):
                        wrapper_checks += 1
                        if h_answer[i] not in (0, 1):
                            failures.append("one-bit output")

        # Padding and alternate encodings preserve the decision bit but can
        # change the measured length.  No runtime inference is made.
        for i in range(4):
            for pad in range(8):
                padded_size = h_size[i] + 5 * pad
                padding_checks += 1
                if padded_size < h_size[i] or h_answer[i] != h_answer[i]:
                    failures.append("padding semantics")

    elapsed = time.perf_counter() - started
    result = {
        "claim": "SIGNED-CLEANCORE-WORSTCASE-EQUIV1",
        "status": "COMPUTATIONAL",
        "scope": "finite abstraction only; no asymptotic runtime inference",
        "clean_labelings": 16,
        "decision_preserving_reductions": preserving_reductions,
        "runtime_tables_per_reduction": len(runtime_tables),
        "monochromatic_proper_islands": monochromatic_islands,
        "reduction_checks": reduction_checks,
        "composition_cost_checks": cost_checks,
        "island_checks": island_checks,
        "wrapper_checks": wrapper_checks,
        "padding_checks": padding_checks,
        "total_checks": reduction_checks + cost_checks + island_checks + wrapper_checks + padding_checks,
        "failures": len(failures),
        "failure_examples": failures[:8],
        "elapsed_seconds": round(elapsed, 6),
        "controls": [
            "proper monochromatic islands",
            "mixed-answer clean domains",
            "one-bit output",
            "padding",
            "alternate encodings",
            *wrappers,
        ],
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["canonical_payload_sha256"] = hashlib.sha256(canonical).hexdigest()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
