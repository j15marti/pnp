#!/usr/bin/env python3
"""Finite controls for the clone-disjointization transfer firewall.

This is an independent semantic/syntactic checker.  It is not an execution of
the historical R_mix341 checker or of a Polynomial Calculus proof checker.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import resource
import time
import tracemalloc
from pathlib import Path


def and_gate(a: int, b: int) -> int:
    return a & b


def overlap_graph(supports: list[set[str]]) -> list[tuple[int, int]]:
    return [
        (i, j)
        for i in range(len(supports))
        for j in range(i + 1, len(supports))
        if supports[i] & supports[j]
    ]


def max_pairwise_disjoint(supports: list[set[str]]) -> int:
    best = 0
    for mask in range(1 << len(supports)):
        chosen = [supports[i] for i in range(len(supports)) if mask >> i & 1]
        if all(not (chosen[i] & chosen[j]) for i in range(len(chosen)) for j in range(i + 1, len(chosen))):
            best = max(best, len(chosen))
    return best


def truth_table_controls(m: int) -> dict:
    # Original gates z_i = x_0 AND x_i.  The cloned gates use fresh y_i.
    mismatches_without_equalities = []
    checked_without = 0
    checked_with = 0
    for bits in itertools.product((0, 1), repeat=m + 1):
        x0, xs = bits[0], bits[1:]
        original = tuple(and_gate(x0, x) for x in xs)
        ys_equal = (x0,) * m
        assert tuple(and_gate(y, x) for y, x in zip(ys_equal, xs)) == original
        checked_with += 1
        for ys in itertools.product((0, 1), repeat=m):
            cloned = tuple(and_gate(y, x) for y, x in zip(ys, xs))
            checked_without += 1
            if cloned != original:
                mismatches_without_equalities.append(
                    {"x": bits, "y": ys, "original": original, "cloned": cloned}
                )
    assert checked_with == 2 ** (m + 1)
    assert mismatches_without_equalities
    return {
        "assignments_with_equalities": checked_with,
        "assignments_without_equalities": checked_without,
        "mismatch_count_without_equalities": len(mismatches_without_equalities),
        "first_mismatch": mismatches_without_equalities[0],
    }


def monomial(*variables: str) -> tuple[str, ...]:
    return tuple(sorted(variables))


def add_term(poly: dict[tuple[str, ...], int], coeff: int, mono: tuple[str, ...]) -> None:
    poly[mono] = poly.get(mono, 0) + coeff
    if poly[mono] == 0:
        del poly[mono]


def telescoping_identity(k: int) -> bool:
    # prod(y_i)-prod(x_i) = sum_i (y_i-x_i) prod_{j<i} y_j prod_{j>i} x_j.
    lhs: dict[tuple[str, ...], int] = {}
    rhs: dict[tuple[str, ...], int] = {}
    add_term(lhs, 1, monomial(*(f"y{i}" for i in range(k))))
    add_term(lhs, -1, monomial(*(f"x{i}" for i in range(k))))
    for i in range(k):
        prefix = [f"y{j}" for j in range(i)]
        suffix = [f"x{j}" for j in range(i + 1, k)]
        add_term(rhs, 1, monomial(*(prefix + [f"y{i}"] + suffix)))
        add_term(rhs, -1, monomial(*(prefix + [f"x{i}"] + suffix)))
    return lhs == rhs


def malformed_controls() -> dict:
    def validate(original_ids: set[int], clone_ids: list[int], equality_targets: list[int]) -> bool:
        if len(set(clone_ids)) != len(clone_ids):
            return False
        if original_ids & set(clone_ids):
            return False
        if len(equality_targets) != len(clone_ids):
            return False
        if any(target not in original_ids for target in equality_targets):
            return False
        return True

    cases = {
        "valid_large_ids": validate({2**31 + 17}, [2**40 + 1, 2**40 + 3], [2**31 + 17] * 2),
        "duplicate_clone_output": validate({1}, [9, 9], [1, 1]),
        "nonfresh_clone_output": validate({1, 9}, [9, 10], [1, 1]),
        "missing_equality": validate({1}, [9, 10], [1]),
        "unknown_equality_target": validate({1}, [9, 10], [1, 2]),
    }
    assert cases == {
        "valid_large_ids": True,
        "duplicate_clone_output": False,
        "nonfresh_clone_output": False,
        "missing_equality": False,
        "unknown_equality_target": False,
    }
    return cases


def run(max_m: int) -> dict:
    started = time.perf_counter()
    tracemalloc.start()
    rows = []
    assertions = 0
    for m in range(2, max_m + 1):
        original_supports = [{"x0", f"x{i}"} for i in range(1, m + 1)]
        cloned_gate_supports = [{f"y{i}", f"x{i}"} for i in range(1, m + 1)]
        equality_extension_supports = [{"x0"} for _ in range(m)]
        row = {
            "m": m,
            "original_overlap_edges": len(overlap_graph(original_supports)),
            "cloned_gate_overlap_edges": len(overlap_graph(cloned_gate_supports)),
            "equality_extension_overlap_edges": len(overlap_graph(equality_extension_supports)),
            "max_disjoint_equality_extensions": max_pairwise_disjoint(equality_extension_supports),
            "truth_table": truth_table_controls(m),
        }
        assert row["original_overlap_edges"] == m * (m - 1) // 2
        assert row["cloned_gate_overlap_edges"] == 0
        assert row["equality_extension_overlap_edges"] == m * (m - 1) // 2
        assert row["max_disjoint_equality_extensions"] == 1
        assertions += 4 + row["truth_table"]["assignments_with_equalities"] + row["truth_table"]["assignments_without_equalities"]
        rows.append(row)

    telescoping = {str(k): telescoping_identity(k) for k in range(1, 9)}
    assert all(telescoping.values())
    assertions += len(telescoping)
    malformed = malformed_controls()
    assertions += len(malformed)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    result = {
        "status": "PASS",
        "scope": "finite semantic/syntactic control; not an authoritative checker execution",
        "claim": {
            "without_equalities": "cloning changes the represented functions",
            "equalities_as_extensions": "supports all contain x0 and cloned gates depend recursively on earlier extension outputs",
            "equalities_as_source_axioms": "the source system is changed; equisatisfiability is not lower-bound preservation",
            "algebraic_upper_control": "the product telescoping identity gives a linear-in-arity derivation once equality equations are legal premises",
        },
        "rows": rows,
        "telescoping_identity": telescoping,
        "malformed_controls": malformed,
        "assertions": assertions,
        "elapsed_seconds": time.perf_counter() - started,
        "python_tracemalloc_current_bytes": current,
        "python_tracemalloc_peak_bytes": peak,
        "process_max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["content_sha256_before_hash_field"] = hashlib.sha256(canonical).hexdigest()
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-m", type=int, default=8)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not 2 <= args.max_m <= 12:
        raise SystemExit("--max-m must be in [2,12]")
    result = run(args.max_m)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
