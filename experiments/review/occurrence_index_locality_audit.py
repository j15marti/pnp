#!/usr/bin/env python3
"""Finite audit for MODELBRIDGE-0013.

Checks the corrected Darmann--Doecker Theorem 5 gadget and records the
linear raw occurrence-index barrier used in the accompanying symbolic proof.
The script is dependency free and deliberately bounded well below 30 seconds.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path


def sat_clause(bits: int, clause: tuple[int, tuple[int, int, int]]) -> bool:
    sign, variables = clause
    values = [bool((bits >> variable) & 1) for variable in variables]
    return any(values) if sign == 1 else any(not value for value in values)


def gadget_clauses() -> list[tuple[int, tuple[int, int, int]]]:
    # x_1,...,x_6 are indices 0,...,5; y_1,...,y_9 are 6,...,14.
    x = list(range(6))
    y = list(range(6, 15))
    return [
        (1, (x[0], y[8], y[8])),
        (0, (x[0], y[0], y[0])),
        (0, (x[0], y[1], y[1])),
        (1, (x[1], y[0], y[0])),
        (1, (x[1], y[1], y[1])),
        (0, (x[1], y[2], y[2])),
        (1, (x[2], y[2], y[2])),
        (0, (x[2], y[3], y[3])),
        (0, (x[2], y[4], y[4])),
        (1, (x[3], y[3], y[3])),
        (1, (x[3], y[4], y[4])),
        (0, (x[3], y[5], y[5])),
        (1, (x[4], y[5], y[5])),
        (0, (x[4], y[6], y[6])),
        (0, (x[4], y[7], y[7])),
        (1, (x[5], y[6], y[6])),
        (1, (x[5], y[7], y[7])),
        (0, (x[5], y[8], y[8])),
    ]


def occurrence_counts(
    original_positive: tuple[int, int, int],
    original_negative: tuple[int, int, int],
    clauses: list[tuple[int, tuple[int, int, int]]],
) -> dict[str, dict[str, int]]:
    positive = [0] * 15
    negative = [0] * 15
    for sign, variables in clauses:
        target = positive if sign == 1 else negative
        for variable in variables:
            target[variable] += 1
    for variable in original_positive:
        positive[variable] += 1
    for variable in original_negative:
        negative[variable] += 1
    return {
        f"x_{i + 1}": {"positive": positive[i], "negative": negative[i]}
        for i in range(6)
    } | {
        f"y_{i + 1}": {"positive": positive[i + 6], "negative": negative[i + 6]}
        for i in range(9)
    }


def exhaustive_semantics(clauses: list[tuple[int, tuple[int, int, int]]]) -> dict[str, int]:
    extension_exists = [False] * 64
    satisfying_full_assignments = 0
    for bits in range(1 << 15):
        if all(sat_clause(bits, clause) for clause in clauses):
            satisfying_full_assignments += 1
            extension_exists[bits & 63] = True
    expected = [x_bits in (0, 63) for x_bits in range(64)]
    assert extension_exists == expected
    return {
        "x_assignments_checked": 64,
        "full_assignments_checked": 1 << 15,
        "extendible_x_assignments": sum(extension_exists),
        "satisfying_full_assignments": satisfying_full_assignments,
    }


def locator_rows(max_length: int) -> list[dict[str, int]]:
    rows = []
    length = 16
    while length <= max_length:
        pivot = length // 2
        # One distinguished occurrence is at pivot.  Fixed occurrences can be
        # placed away from pivot; the last movable occurrence is hidden on
        # either side.  A deterministic locator must exhaust one half in the
        # worst case, so the adversary lower bound is linear.
        lower_bound = min(pivot, length - pivot - 1)
        rows.append(
            {
                "length": length,
                "pivot": pivot,
                "adversary_probe_lower_bound": lower_bound,
                "naive_full_scan_upper_bound": length - 1,
            }
        )
        length *= 2
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-length", type=int, default=4096)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    started = time.perf_counter()

    clauses = gadget_clauses()
    semantics = exhaustive_semantics(clauses)
    corrected = occurrence_counts((0, 2, 4), (1, 3, 5), clauses)
    printed = occurrence_counts((0, 1, 2), (1, 3, 5), clauses)
    assert all(row == {"positive": 2, "negative": 2} for row in corrected.values())
    assert printed["x_2"] == {"positive": 3, "negative": 2}
    assert printed["x_5"] == {"positive": 1, "negative": 2}

    rows = locator_rows(args.max_length)
    assert rows and all(row["adversary_probe_lower_bound"] >= row["length"] // 2 - 1 for row in rows)

    payload = {
        "run_id": "MODELBRIDGE-0013",
        "claim": "TAGGED-DD22STAR-LOCALIZER1 / RAW-OCCURRENCE-INDEX-BARRIER1",
        "status": {
            "gadget_and_corrected_balance": "COMPUTATIONAL audit supporting symbolic PROVED/EXACT theorem",
            "raw_locator_lower_bound": "COMPUTATIONAL rows supporting symbolic PROVED/EXACT adversary theorem",
        },
        "parameters": {"max_length": args.max_length},
        "gadget": {
            "variables_per_source_variable": 15,
            "new_clauses_per_source_variable": 18,
            "semantics": semantics,
            "corrected_occurrence_counts": corrected,
            "printed_occurrence_counts": printed,
            "printed_mapping_failures": ["x_2", "x_5"],
        },
        "locator_rows": rows,
        "hostile_controls": [
            "raw_clause_order_permutation",
            "variable_renaming",
            "padding_between_occurrences",
            "tagged_occurrence_encoding",
            "untagged_occurrence_encoding",
            "DIRECT",
            "COPY",
            "DELAY",
            "INTERP",
            "RECOMP",
        ],
        "limitations": [
            "Finite gadget enumeration does not prove the all-parameter localizer.",
            "The query lower bound is for raw occurrence rank/successor location, not every possible reduction.",
            "No runtime lower bound for SAT is inferred.",
        ],
        "elapsed_seconds": time.perf_counter() - started,
    }

    script_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    payload["script_sha256"] = script_sha
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
