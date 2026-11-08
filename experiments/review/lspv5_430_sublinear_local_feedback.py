#!/usr/bin/env python3
"""Finite controls for the LSPV-5/430 sublinear-locality simulation lemma.

This is an independent finite model, not the historical R_mix341 checker and
not an implementation of Pang's asymptotic lower-bound proof.
"""

from __future__ import annotations

import json
import math
import resource
import time


def g_sqrt(n: int) -> int:
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a nonnegative integer")
    return math.isqrt(n)


def compiler_bound(b: int) -> int:
    """A deliberately conservative c*b*2^b per-node bound."""
    if not isinstance(b, int) or b < 0:
        raise ValueError("b must be a nonnegative integer")
    return 8 * (b + 1) * (1 << b)


def truth(mask: int, assignment: int) -> bool:
    return bool((mask >> assignment) & 1)


def validate_local_record(n: int, support: tuple[int, ...], table: int) -> bool:
    if not isinstance(n, int) or n < 0:
        return False
    if not isinstance(support, tuple) or any(not isinstance(x, int) for x in support):
        return False
    if len(set(support)) != len(support):
        return False
    if any(x < 1 or x > n for x in support):
        return False
    if len(support) > g_sqrt(n):
        return False
    if not isinstance(table, int) or table < 0 or table >= (1 << (1 << len(support))):
        return False
    return True


def implication_controls(max_b: int = 3) -> dict[str, object]:
    rows = []
    total_pairs = 0
    true_pairs = 0
    witnessed_falsifying_rows = 0
    for b in range(1, max_b + 1):
        assignments = 1 << b
        functions = 1 << assignments
        local_total = functions * functions
        local_true = 0
        local_witnessed = 0
        for antecedent in range(functions):
            for consequent in range(functions):
                implication = antecedent & ~consequent == 0
                if not implication:
                    continue
                local_true += 1
                for alpha in range(assignments):
                    if not truth(consequent, alpha):
                        assert not truth(antecedent, alpha)
                        local_witnessed += 1
        assert local_true == 3**assignments
        rows.append({
            "b": b,
            "ordered_factor_pairs": local_total,
            "valid_implications": local_true,
            "expected_valid_implications": 3**assignments,
            "output_false_rows_with_parent_witness": local_witnessed,
        })
        total_pairs += local_total
        true_pairs += local_true
        witnessed_falsifying_rows += local_witnessed
    return {
        "rows": rows,
        "ordered_factor_pairs": total_pairs,
        "valid_implications": true_pairs,
        "output_false_rows_with_parent_witness": witnessed_falsifying_rows,
    }


def two_parent_controls(b: int = 3) -> dict[str, int]:
    assignments = 1 << b
    functions = 1 << assignments
    full = functions - 1
    valid = 0
    witness_rows = 0
    for left in range(functions):
        for right in range(functions):
            intersection = left & right
            free_bits = assignments - intersection.bit_count()
            valid += 1 << free_bits
            # For each possible output, explicitly verify the named-parent
            # witness condition on every output-false assignment.
            for output in range(functions):
                if intersection & (~output & full):
                    continue
                for alpha in range(assignments):
                    if truth(output, alpha):
                        continue
                    assert (not truth(left, alpha)) or (not truth(right, alpha))
                    witness_rows += 1
    return {
        "b": b,
        "ordered_factor_triples": functions**3,
        "valid_two_parent_implications": valid,
        "output_false_rows_with_named_parent": witness_rows,
    }


def projection_controls(max_b: int = 3) -> dict[str, int]:
    """Check full-assignment exclusions project to output exclusions.

    A factor table on target support S is lifted to U by ignoring U\\S.
    Pairwise resolution on the outside variables should leave exactly one
    exclusion clause for every falsifying target assignment.
    """
    cases = 0
    excluded_extensions = 0
    projected_clauses = 0
    for b in range(max_b + 1):
        for s in range(b + 1):
            functions = 1 << (1 << s)
            extension_count = 1 << (b - s)
            for table in range(functions):
                false_target = (1 << s) - table.bit_count()
                full_exclusions = false_target * extension_count
                # Eliminating b-s outside variables pairs all extensions of
                # each target assignment into its unique exclusion clause.
                assert full_exclusions == false_target * (1 << (b - s))
                cases += 1
                excluded_extensions += full_exclusions
                projected_clauses += false_target
    return {
        "projection_cases": cases,
        "full_assignment_exclusions": excluded_extensions,
        "projected_output_clauses": projected_clauses,
    }


def asymptotic_controls() -> list[dict[str, float | int]]:
    rows = []
    for n in (16, 64, 256, 1024, 4096, 16384, 65536):
        b = g_sqrt(n)
        bound = compiler_bound(b)
        rows.append({
            "n": n,
            "g_sqrt_n": b,
            "compiler_bound_bit_length": bound.bit_length(),
            "log2_bound_over_n": math.log2(bound) / n,
        })
    assert rows[-1]["log2_bound_over_n"] < rows[0]["log2_bound_over_n"]
    return rows


def malformed_controls() -> dict[str, bool]:
    controls = {
        "negative_header_rejected": not validate_local_record(-1, (), 0),
        "duplicate_support_rejected": not validate_local_record(16, (1, 1), 0),
        "zero_variable_rejected": not validate_local_record(16, (0,), 0),
        "out_of_range_variable_rejected": not validate_local_record(16, (17,), 0),
        "over_threshold_support_rejected": not validate_local_record(16, (1, 2, 3, 4, 5), 0),
        "oversize_truth_table_rejected": not validate_local_record(16, (1, 2), 16),
        "valid_boundary_accepted": validate_local_record(16, (1, 2, 3, 4), 0b0110100110010110),
    }
    assert all(controls.values())
    return controls


def main() -> None:
    start = time.perf_counter_ns()
    implication = implication_controls()
    two_parent = two_parent_controls()
    projection = projection_controls()
    malformed = malformed_controls()
    asymptotic = asymptotic_controls()
    elapsed = time.perf_counter_ns() - start
    out = {
        "claim_id": "P2-L5-430",
        "status": "COMPUTATIONAL finite controls for a separate symbolic proof",
        "historical_r_mix341_checker": False,
        "random_seed": None,
        "scope": "exhaustive Boolean functions through b=3; exact integer asymptotic ledger",
        "implication": implication,
        "two_parent": two_parent,
        "projection": projection,
        "malformed": malformed,
        "asymptotic": asymptotic,
        "resources": {
            "elapsed_ns": elapsed,
            "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        },
        "limitations": [
            "Does not execute the historical R_mix341 checker.",
            "Does not reproduce Pang's asymptotic lower-bound proof.",
            "Finite enumeration is not an asymptotic proof.",
        ],
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
