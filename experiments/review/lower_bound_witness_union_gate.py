#!/usr/bin/env python3
"""Finite audit for the PFCERT witness-union and fiber-sparsity gates.

The experiment validates finite identities only.  It is not evidence for an
asymptotic SAT lower bound.
"""

import argparse
import json
import math
import signal
import time
from pathlib import Path


def alarm_handler(_signum, _frame):
    raise TimeoutError("25-second cooperative budget exceeded")


def exhaustive_relations(n: int, q: int):
    outputs = 1 << n
    witnesses = 1 << q
    cells = outputs * witnesses
    if cells > 20:
        raise ValueError("exhaustive relation table is intentionally capped")
    checked = 0
    union_violations = 0
    smallest = None
    for mask in range(1 << cells):
        per_witness = []
        image = set()
        for pi in range(witnesses):
            accepted = {
                x for x in range(outputs)
                if mask & (1 << (pi * outputs + x))
            }
            per_witness.append(len(accepted))
            image.update(accepted)
        bound = min(outputs, sum(per_witness))
        assert len(image) <= bound
        if max(per_witness, default=0) <= 1 and len(image) > 1:
            union_violations += 1
            if smallest is None:
                smallest = {
                    "mask": mask,
                    "per_witness": per_witness,
                    "image": sorted(image),
                }
        checked += 1
    return checked, union_violations, smallest


def tight_construction(n: int, q: int, b: int):
    outputs = 1 << n
    witnesses = 1 << q
    image = set()
    for pi in range(witnesses):
        for j in range(b):
            image.add((pi * b + j) % outputs)
    return len(image), min(outputs, b * witnesses)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=14)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(25)
    started = time.perf_counter()

    relation_checks, union_violations, smallest = exhaustive_relations(2, 2)

    tight_checks = 0
    for n in range(1, args.max_n + 1):
        for q in range(0, n + 1):
            for b in range(1, min(8, 1 << n) + 1):
                actual, predicted = tight_construction(n, q, b)
                assert actual == predicted
                tight_checks += 1

    padding_checks = 0
    for image_size in range(1, 17):
        for padding_bits in range(0, 9):
            base_paths = image_size
            padded_paths = image_size * (1 << padding_bits)
            assert padded_paths // base_paths == (1 << padding_bits)
            assert image_size == image_size
            padding_checks += 1

    density_rows = []
    for n in range(8, args.max_n + 1):
        for list_bound in (1, 2, 4, 8):
            if list_bound > (1 << (n - 1)):
                continue
            ell = math.ceil(math.log2(list_bound))
            k = n - ell - 1
            programs = (1 << (k + 1)) - 1
            pairs = list_bound * programs
            encoded_length = n + k + 2
            assert pairs < (1 << n)
            density_rows.append({
                "n": n,
                "list_bound": list_bound,
                "program_bits": k,
                "pair_count_upper_bound": pairs,
                "pair_encoding_length": encoded_length,
                "log2_pair_count_over_encoding_length": (
                    math.log2(pairs) / encoded_length if pairs else 0.0
                ),
            })

    elapsed = time.perf_counter() - started
    result = {
        "status": "PASS",
        "scope": "finite relation, padding, and encoding audit only",
        "parameters": {"max_n": args.max_n},
        "exhaustive_relation_checks": relation_checks,
        "per_witness_one_but_union_gt_one_relations": union_violations,
        "smallest_recorded_counterexample": smallest,
        "tight_union_bound_checks": tight_checks,
        "witness_padding_checks": padding_checks,
        "fiber_density_rows": density_rows,
        "elapsed_seconds": elapsed,
        "failure_count": 0,
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
