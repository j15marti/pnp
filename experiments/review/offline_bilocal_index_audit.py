#!/usr/bin/env python3
"""Bounded audit for OFFLINE-BILOCAL-INDEX1.

This experiment checks exact reconstruction, forward occurrence ranks,
inverse incidence access, semantics, encodings, and hostile wrappers for a
deterministic comparison-sort index compiler.  It establishes finite facts
only; the accompanying report contains the symbolic all-formula theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


Clause = tuple[int, ...]
Formula = tuple[Clause, ...]
Record = tuple[int, int, int, int]  # variable, sign-bit, clause, slot


@dataclass(frozen=True)
class Index:
    forward: tuple[tuple[int, ...], ...]
    inverse: dict[tuple[int, int, int], tuple[int, int]]
    sorted_records: tuple[Record, ...]
    comparisons: int


def merge_sort(records: list[Record]) -> tuple[list[Record], int]:
    """Stable deterministic merge sort with an exact comparison count."""
    if len(records) <= 1:
        return records[:], 0
    mid = len(records) // 2
    left, c1 = merge_sort(records[:mid])
    right, c2 = merge_sort(records[mid:])
    out: list[Record] = []
    i = j = 0
    comparisons = c1 + c2
    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out, comparisons


def build_index(formula: Formula) -> tuple[Index, dict[str, int]]:
    start = time.perf_counter_ns()
    records: list[Record] = []
    parse_ops = 0
    for ci, clause in enumerate(formula):
        for si, lit in enumerate(clause):
            records.append((abs(lit), 1 if lit > 0 else 0, ci, si))
            parse_ops += 1
    sorted_records, comparisons = merge_sort(records)
    forward = [[-1 for _ in clause] for clause in formula]
    inverse: dict[tuple[int, int, int], tuple[int, int]] = {}
    previous: tuple[int, int] | None = None
    rank = -1
    index_writes = 0
    for variable, sign, ci, si in sorted_records:
        key = (variable, sign)
        rank = rank + 1 if key == previous else 0
        previous = key
        forward[ci][si] = rank
        inverse[(variable, sign, rank)] = (ci, si)
        index_writes += 2
    elapsed = time.perf_counter_ns() - start
    return (
        Index(tuple(tuple(row) for row in forward), inverse, tuple(sorted_records), comparisons),
        {
            "literal_records": len(records),
            "parse_ops": parse_ops,
            "comparisons": comparisons,
            "index_writes": index_writes,
            "build_ns": elapsed,
        },
    )


def validate_index(formula: Formula, index: Index) -> dict[str, int]:
    forward_checks = inverse_checks = reconstruction_checks = rank_checks = 0
    reconstructed: list[list[int]] = [[0 for _ in c] for c in formula]
    grouped: dict[tuple[int, int], list[tuple[int, int]]] = {}
    for ci, clause in enumerate(formula):
        for si, lit in enumerate(clause):
            sign = 1 if lit > 0 else 0
            rank = index.forward[ci][si]
            assert index.inverse[(abs(lit), sign, rank)] == (ci, si)
            forward_checks += 1
            inverse_checks += 1
            reconstructed[ci][si] = lit
            reconstruction_checks += 1
            grouped.setdefault((abs(lit), sign), []).append((ci, si))
    assert tuple(tuple(c) for c in reconstructed) == formula
    for (variable, sign), positions in grouped.items():
        expected = sorted(positions)
        actual = [index.inverse[(variable, sign, rank)] for rank in range(len(expected))]
        assert actual == expected
        rank_checks += len(expected)
    return {
        "forward_checks": forward_checks,
        "inverse_checks": inverse_checks,
        "reconstruction_checks": reconstruction_checks,
        "rank_checks": rank_checks,
    }


def eval_formula(formula: Formula, assignment: tuple[bool, ...]) -> bool:
    return all(
        any(assignment[abs(lit) - 1] if lit > 0 else not assignment[abs(lit) - 1] for lit in clause)
        for clause in formula
    )


def semantic_vector(formula: Formula, variables: int) -> tuple[bool, ...]:
    return tuple(eval_formula(formula, a) for a in itertools.product((False, True), repeat=variables))


def horn_sat(formula: Formula) -> tuple[bool, int]:
    true_vars: set[int] = set()
    scans = 0
    changed = True
    while changed:
        changed = False
        for clause in formula:
            scans += 1
            positives = [lit for lit in clause if lit > 0]
            assert len(positives) <= 1
            antecedent = {-lit for lit in clause if lit < 0}
            if antecedent <= true_vars:
                if not positives:
                    return False, scans
                if positives[0] not in true_vars:
                    true_vars.add(positives[0])
                    changed = True
    return True, scans


def twosat_sat(formula: Formula) -> tuple[bool, int]:
    n = max_var(formula)
    size = 2 * n
    graph = [[] for _ in range(size)]
    reverse = [[] for _ in range(size)]

    def node(lit: int) -> int:
        return 2 * (abs(lit) - 1) + (0 if lit > 0 else 1)

    edges = 0
    for clause in formula:
        assert 1 <= len(clause) <= 2
        a = clause[0]
        b = clause[-1]
        for source, target in ((-a, b), (-b, a)):
            u, v = node(source), node(target)
            graph[u].append(v)
            reverse[v].append(u)
            edges += 1
    seen: set[int] = set()
    order: list[int] = []

    def dfs(u: int) -> None:
        seen.add(u)
        for v in graph[u]:
            if v not in seen:
                dfs(v)
        order.append(u)

    for u in range(size):
        if u not in seen:
            dfs(u)
    component = [-1] * size

    def rdfs(u: int, label: int) -> None:
        component[u] = label
        for v in reverse[u]:
            if component[v] < 0:
                rdfs(v, label)

    label = 0
    for u in reversed(order):
        if component[u] < 0:
            rdfs(u, label)
            label += 1
    return all(component[2 * i] != component[2 * i + 1] for i in range(n)), edges


def gaussian_consistent(rows: list[tuple[int, int]], variables: int) -> tuple[bool, int, int]:
    """GF(2) elimination on (bitmask, rhs) rows."""
    matrix = [[mask, rhs] for mask, rhs in rows]
    rank = operations = 0
    for col in range(variables):
        pivot = next((r for r in range(rank, len(matrix)) if (matrix[r][0] >> col) & 1), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        for r in range(len(matrix)):
            if r != rank and ((matrix[r][0] >> col) & 1):
                matrix[r][0] ^= matrix[rank][0]
                matrix[r][1] ^= matrix[rank][1]
                operations += 1
        rank += 1
    consistent = all(mask != 0 or rhs == 0 for mask, rhs in matrix)
    return consistent, rank, operations


def rename(formula: Formula, permutation: tuple[int, ...]) -> Formula:
    return tuple(
        tuple((1 if lit > 0 else -1) * permutation[abs(lit) - 1] for lit in clause)
        for clause in formula
    )


def permute_formula(formula: Formula, seed: int) -> Formula:
    rng = random.Random(seed)
    clauses = [list(c) for c in formula]
    for clause in clauses:
        rng.shuffle(clause)
    rng.shuffle(clauses)
    return tuple(tuple(c) for c in clauses)


def max_var(formula: Formula) -> int:
    return max((abs(lit) for clause in formula for lit in clause), default=0)


def pad_dead(formula: Formula) -> Formula:
    z = max_var(formula) + 1
    w = z + 1
    return formula + ((z, -z, w),)


def duplicate_clause(formula: Formula) -> Formula:
    return formula + (formula[0],) if formula else formula


def product(formulas: Iterable[Formula]) -> Formula:
    out: list[Clause] = []
    offset = 0
    for formula in formulas:
        out.extend(tuple((1 if lit > 0 else -1) * (abs(lit) + offset) for lit in c) for c in formula)
        offset += max_var(formula)
    return tuple(out)


def tseitin_cycle(n: int, odd: bool) -> Formula:
    """Proper 3-CNF encoding of x_i xor x_(i+1) xor a_i = parity."""
    clauses: list[Clause] = []
    aux = n
    for i in range(n):
        x = i + 1
        y = (i + 1) % n + 1
        a = aux + i + 1
        parity = 1 if (odd and i == n - 1) else 0
        bad_assignments = [bits for bits in itertools.product((0, 1), repeat=3) if (bits[0] ^ bits[1] ^ bits[2]) != parity]
        for bits in bad_assignments:
            clauses.append(tuple(-(var) if bit else var for var, bit in zip((x, y, a), bits)))
    return tuple(clauses)


def family_instances() -> list[tuple[str, Formula]]:
    horn = ((-1, -2, 3), (-3, 4), (-4, 5), (1,))
    twosat = ((1, 2), (-1, 3), (-2, -3), (3, 4), (-4, 1))
    bounded_tw = tuple((i, -(i + 1), i + 2) for i in range(1, 7))
    affine = tseitin_cycle(4, odd=False)
    independent = product((horn, twosat))
    padded = pad_dead(twosat)
    redundant = duplicate_clause(horn)
    return [
        ("horn", horn),
        ("2sat", twosat),
        ("affine_tseitin", affine),
        ("bounded_treewidth", bounded_tw),
        ("independent_product", independent),
        ("padding_dead", padded),
        ("redundant_clause", redundant),
    ]


def encoded_lengths(formula: Formula) -> dict[str, int]:
    v = max_var(formula)
    width = max(1, math.ceil(math.log2(v + 1)))
    literal_count = sum(len(c) for c in formula)
    fixed = literal_count * (width + 1) + len(formula) * 2
    delta = 0
    for clause in formula:
        prev = 0
        for lit in sorted(clause, key=abs):
            gap = abs(lit) - prev
            delta += max(1, math.ceil(math.log2(gap + 1))) + 1
            prev = abs(lit)
        delta += 2
    return {"fixed_bits": fixed, "delta_bits": delta, "identifier_width": width}


def token_encode(formula: Formula) -> str:
    return ";".join(",".join(str(lit) for lit in clause) for clause in formula)


def token_decode(text: str) -> Formula:
    if not text:
        return ()
    return tuple(tuple(int(piece) for piece in clause.split(",") if piece) for clause in text.split(";"))


def record_encode(formula: Formula) -> tuple[tuple[tuple[int, int], ...], ...]:
    return tuple(tuple((1 if lit > 0 else 0, abs(lit)) for lit in clause) for clause in formula)


def record_decode(records: tuple[tuple[tuple[int, int], ...], ...]) -> Formula:
    return tuple(tuple(variable if sign else -variable for sign, variable in clause) for clause in records)


def raw_rank_probe_count(stream: list[tuple[int, int]], target_pos: int) -> int:
    """Number of records read by the left scan computing an occurrence rank."""
    target = stream[target_pos]
    probes = 0
    rank = 0
    for pos, record in enumerate(stream):
        probes += 1
        if record == target:
            if pos == target_pos:
                return probes
            rank += 1
    raise AssertionError("target position missing")


def run(seed: int) -> dict:
    totals = {
        "instances": 0,
        "literal_records": 0,
        "comparisons": 0,
        "forward_checks": 0,
        "inverse_checks": 0,
        "reconstruction_checks": 0,
        "rank_checks": 0,
        "semantic_checks": 0,
        "encoding_checks": 0,
        "wrapper_checks": 0,
        "raw_probe_checks": 0,
        "tractable_solver_checks": 0,
        "gaussian_row_operations": 0,
    }
    rows = []
    rng = random.Random(seed)
    for family_name, base in family_instances():
        variants: list[tuple[str, Formula]] = [("direct", base)]
        variants.append(("clause_slot_permutation", permute_formula(base, seed + len(rows))))
        p = list(range(1, max_var(base) + 1))
        rng.shuffle(p)
        variants.append(("interp_renaming", rename(base, tuple(p))))
        variants.append(("copy", tuple(tuple(c) for c in base)))
        variants.append(("recomp", tuple(tuple(c) for c in base)))
        for variant_name, formula in variants:
            index, build = build_index(formula)
            checks = validate_index(formula, index)
            v = max_var(formula)
            if v <= 12:
                vec = semantic_vector(formula, v)
                assert len(vec) == 1 << v
                semantic_checks = len(vec)
            else:
                semantic_checks = 0
            lengths = encoded_lengths(formula)
            assert lengths["fixed_bits"] > 0 and lengths["delta_bits"] > 0
            assert token_decode(token_encode(formula)) == formula
            assert record_decode(record_encode(formula)) == formula
            totals["encoding_checks"] += 4
            stream = [(abs(lit), 1 if lit > 0 else 0) for c in formula for lit in c]
            raw_probes = 0
            for pos in range(len(stream)):
                probes = raw_rank_probe_count(stream, pos)
                assert 1 <= probes <= len(stream)
                raw_probes += probes
                totals["raw_probe_checks"] += 1
            totals["instances"] += 1
            for key in ("literal_records", "comparisons"):
                totals[key] += build[key]
            for key in ("forward_checks", "inverse_checks", "reconstruction_checks", "rank_checks"):
                totals[key] += checks[key]
            totals["semantic_checks"] += semantic_checks
            totals["wrapper_checks"] += 1
            rows.append(
                {
                    "family": family_name,
                    "variant": variant_name,
                    "variables": v,
                    "clauses": len(formula),
                    "literal_records": build["literal_records"],
                    "comparisons": build["comparisons"],
                    "comparison_upper_bound": build["literal_records"] * math.ceil(math.log2(max(1, build["literal_records"]))),
                    "build_ns": build["build_ns"],
                    "semantic_checks": semantic_checks,
                    "raw_left_scan_probe_total": raw_probes,
                    "fixed_bits": lengths["fixed_bits"],
                    "delta_bits": lengths["delta_bits"],
                }
            )
            assert build["comparisons"] <= rows[-1]["comparison_upper_bound"]

        base_vec = semantic_vector(base, max_var(base))
        for name, formula in variants:
            if name in {"direct", "clause_slot_permutation", "copy", "recomp"}:
                assert semantic_vector(formula, max_var(formula)) == base_vec
                totals["wrapper_checks"] += len(base_vec)

        if family_name == "horn":
            answer, scans = horn_sat(base)
            assert answer == any(base_vec)
            totals["tractable_solver_checks"] += 1 + scans
        if family_name == "2sat":
            answer, edges = twosat_sat(base)
            assert answer == any(base_vec)
            totals["tractable_solver_checks"] += 1 + edges
        if family_name == "affine_tseitin":
            n = 4
            rows_gf2 = []
            for i in range(n):
                x, y, a = i, (i + 1) % n, n + i
                rows_gf2.append(((1 << x) | (1 << y) | (1 << a), 0))
            answer, rank, operations = gaussian_consistent(rows_gf2, 2 * n)
            assert answer == any(base_vec) and rank == n
            totals["tractable_solver_checks"] += 1 + len(rows_gf2)
            totals["gaussian_row_operations"] += operations

    original = family_instances()[1][1]
    dead = pad_dead(original)
    for assignment in itertools.product((False, True), repeat=max_var(original)):
        source = eval_formula(original, assignment)
        extension_answers = []
        for fresh in itertools.product((False, True), repeat=max_var(dead) - max_var(original)):
            extension_answers.append(eval_formula(dead, assignment + fresh))
        assert source == any(extension_answers)
        totals["wrapper_checks"] += 1 + len(extension_answers)

    # A hostile occurrence stream: three target keys at the end.  Raw rank
    # acquisition scans linearly, while the built index answers every rank
    # coordinate by one dictionary lookup after preprocessing.
    hostile_rows = []
    for length in (16, 32, 64, 128, 256, 512):
        stream = [(i + 2, 1) for i in range(length - 3)] + [(1, 1), (1, 1), (1, 1)]
        probes = [raw_rank_probe_count(stream, length - 3 + j) for j in range(3)]
        assert probes == [length - 2, length - 1, length]
        hostile_rows.append({"length": length, "raw_probes": probes, "indexed_word_lookups": [1, 1, 1]})
        totals["raw_probe_checks"] += 3

    payload = {
        "claim": "OFFLINE-BILOCAL-INDEX1",
        "status": "COMPUTATIONAL support for symbolic theorem",
        "seed": seed,
        "exhaustive_semantics_limit": 12,
        "sort": "stable deterministic comparison merge sort",
        "totals": totals,
        "hostile_streams": hostile_rows,
        "rows": rows,
        "limitations": [
            "finite audit only; asymptotic theorem is proved separately",
            "Python timings are descriptive and are not extrapolated",
            "offline O(L log L)-comparison preprocessing is not JMV/FLMV on-demand polylog-time/log-space access",
            "no SAT lower bound and no polynomial algorithm for the full H_(2,2) class is claimed",
        ],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["sha256_without_digest"] = hashlib.sha256(canonical).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20261011)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = run(args.seed)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
