#!/usr/bin/env python3
"""REFEREE377: exact cut-context cover and native GF(2) shortcut control.

This is an independent semantic checker, not the authoritative historical
R_mix341 byte parser.  It binds the finite calculation to an original DIMACS
source and keeps the proposed split protocol separate from native GF(2).
"""

from __future__ import annotations

import hashlib
import itertools
import json
import pathlib
import time
import tracemalloc

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "results/raw/review/2026-11-05_2052_LSPV5_CUT_CONTEXT_COST377.json"


def parity_clauses(vars3: tuple[int, int, int], rhs: int) -> list[tuple[int, int, int]]:
    out = []
    for a in itertools.product((0, 1), repeat=3):
        if (sum(a) & 1) != rhs:
            out.append(tuple(v if bit == 0 else -v for v, bit in zip(vars3, a)))
    return out


def k4_source(charges: tuple[int, int, int, int]) -> tuple[str, list[tuple[int, int]]]:
    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    incident = [[] for _ in range(4)]
    for eid, (u, v) in enumerate(edges, start=1):
        incident[u].append(eid)
        incident[v].append(eid)
    clauses: list[tuple[int, int, int]] = []
    for v in range(4):
        clauses.extend(parity_clauses(tuple(incident[v]), charges[v]))
    body = "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return f"p cnf 6 16\n{body}", edges


def satisfies(clauses: list[tuple[int, ...]], assignment: tuple[int, ...]) -> bool:
    return all(any((assignment[abs(lit) - 1] == 1) == (lit > 0) for lit in c) for c in clauses)


def parse_source(source: str) -> tuple[int, list[tuple[int, ...]]] | None:
    try:
        lines = source.splitlines()
        if not lines or lines[0].split() != ["p", "cnf", "6", "16"] or len(lines) != 17:
            return None
        clauses = []
        for line in lines[1:]:
            values = list(map(int, line.split()))
            if len(values) != 4 or values[-1] != 0:
                return None
            clause = tuple(values[:-1])
            if any(x == 0 or abs(x) > 6 for x in clause):
                return None
            if len({abs(x) for x in clause}) != 3:
                return None
            clauses.append(clause)
        return 6, clauses
    except ValueError:
        return None


def project_component(
    clauses: list[tuple[int, ...]],
    vertices: set[int],
    charges: tuple[int, int, int, int],
    edges: list[tuple[int, int]],
) -> dict[str, bool]:
    incident = [[] for _ in range(4)]
    for eid, (u, v) in enumerate(edges, start=1):
        incident[u].append(eid)
        incident[v].append(eid)
    boundary = [eid for eid, (u, v) in enumerate(edges, start=1) if (u in vertices) != (v in vertices)]
    internal = [eid for eid, (u, v) in enumerate(edges, start=1) if u in vertices and v in vertices]
    local_clauses = [c for v in sorted(vertices) for c in clauses[4 * v : 4 * v + 4]]
    target = 0
    for v in vertices:
        target ^= charges[v]
    allowed: dict[str, bool] = {}
    for boundary_bits in itertools.product((0, 1), repeat=len(boundary)):
        yes = False
        for internal_bits in itertools.product((0, 1), repeat=len(internal)):
            a = [0] * 6
            for eid, bit in zip(boundary, boundary_bits):
                a[eid - 1] = bit
            for eid, bit in zip(internal, internal_bits):
                a[eid - 1] = bit
            if satisfies(local_clauses, tuple(a)):
                yes = True
                break
        allowed["".join(map(str, boundary_bits))] = yes
        assert yes == ((sum(boundary_bits) & 1) == target)
    return allowed


def projection_full_on_at_most_three(allowed: set[str], free_positions: tuple[int, ...]) -> bool:
    seen = {tuple(int(row[i]) for i in free_positions) for row in allowed}
    return len(seen) == 2 ** len(free_positions)


def context_theorem(k: int) -> dict[str, int | bool]:
    assert k >= 3
    rows = [tuple(bits) for bits in itertools.product((0, 1), repeat=k)]
    even = {"".join(map(str, r)) for r in rows if sum(r) % 2 == 0}
    checks = 0

    # Before k-3 pins, every relation on at most three unpinned coordinates
    # projects to the full cube and therefore cannot be a nontrivial consequence.
    for fixed in range(0, k - 3):
        for prefix in itertools.product((0, 1), repeat=fixed):
            residual = {r for r in even if tuple(map(int, r[:fixed])) == prefix}
            remaining = tuple(range(fixed, k))
            for width in range(1, min(3, len(remaining)) + 1):
                for positions in itertools.combinations(remaining, width):
                    assert projection_full_on_at_most_three(residual, positions)
                    checks += 1

    # At exactly k-3 pins, parity leaves three variables and is nontrivial.
    fixed = k - 3
    leaves = []
    covered: set[str] = set()
    for prefix in itertools.product((0, 1), repeat=fixed):
        cube = {"".join(map(str, prefix + tail)) for tail in itertools.product((0, 1), repeat=3)}
        assert len(cube) == 8 and not (cube & covered)
        covered |= cube
        residual_even = cube & even
        assert 0 < len(residual_even) < len(cube)
        leaves.append(prefix)
        checks += 4
    assert covered == {"".join(map(str, r)) for r in rows}

    lower_bound = (2**k + 7) // 8
    assert lower_bound == 2 ** (k - 3) == len(leaves)

    # Historical wide-row control: two opposite rows XOR to 0=1 in one node.
    mask = (1 << k) - 1
    lhs = (mask, 0)
    rhs = (mask, 1)
    xor_row = (lhs[0] ^ rhs[0], lhs[1] ^ rhs[1])
    assert xor_row == (0, 1)
    assert (lhs[0] ^ lhs[0], lhs[1] ^ lhs[1]) == (0, 0)  # corruption/control

    return {
        "k": k,
        "exact_min_leaf_contexts": lower_bound,
        "canonical_leaf_contexts": len(leaves),
        "canonical_split_internal_nodes_if_paid": len(leaves) - 1,
        "canonical_total_tree_nodes_before_leaf_closure_if_paid": 2 * len(leaves) - 1,
        "critical_path_split_decisions": k - 3,
        "materialized_fixed_bit_records": len(leaves) * (k - 3),
        "dfs_live_fixed_bits": k - 3,
        "native_final_xor_nodes": 1,
        "native_branch_contexts": 0,
        "projection_checks": checks,
        "opposite_rows_close": xor_row == (0, 1),
    }


def main() -> None:
    tracemalloc.start()
    start = time.perf_counter()
    checks = 0

    odd_source, edges = k4_source((1, 0, 0, 0))
    even_source, _ = k4_source((0, 0, 0, 0))
    odd_parsed = parse_source(odd_source)
    even_parsed = parse_source(even_source)
    assert odd_parsed and even_parsed
    checks += 2
    odd_models = sum(satisfies(odd_parsed[1], a) for a in itertools.product((0, 1), repeat=6))
    even_models = sum(satisfies(even_parsed[1], a) for a in itertools.product((0, 1), repeat=6))
    assert odd_models == 0
    assert even_models == 8  # cycle rank |E|-|V|+1 = 3
    checks += 2

    # Connected sides S={0,1} and complement have a four-edge cut.
    left = project_component(odd_parsed[1], {0, 1}, (1, 0, 0, 0), edges)
    right = project_component(odd_parsed[1], {2, 3}, (1, 0, 0, 0), edges)
    assert len(left) == len(right) == 16
    assert {x for x, ok in left.items() if ok} == {x for x, ok in right.items() if not ok}
    checks += 3

    cases = [context_theorem(k) for k in range(3, 13)]
    checks += sum(int(case["projection_checks"]) for case in cases)
    assert cases[1]["exact_min_leaf_contexts"] == 2
    assert cases[1]["native_branch_contexts"] == 0
    checks += 2

    malformed = odd_source.replace("p cnf 6 16", "p cnf 6 15", 1)
    corrupted = odd_source.replace("1 2 3 0", "1 2 7 0", 1)
    assert parse_source(malformed) is None
    assert parse_source(corrupted) is None
    checks += 2

    elapsed = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    record = {
        "run": "LSPV-5/REFEREE377",
        "timestamp_PST": "2026-11-05 20:52",
        "status": "PROVED/RESTRICTED theorem; COMPUTATIONAL controls",
        "scope": "split-to-localize subcube cover versus historical semantic GF(2); not authoritative accepted-byte parser",
        "source_family": "proper strict-3 odd/even K4 Tseitin",
        "odd_source_sha256": hashlib.sha256(odd_source.encode()).hexdigest(),
        "even_source_sha256": hashlib.sha256(even_source.encode()).hexdigest(),
        "odd_source_bytes": len(odd_source.encode()),
        "even_source_bytes": len(even_source.encode()),
        "odd_models": odd_models,
        "even_models": even_models,
        "cut_width": 4,
        "left_boundary_models": sum(left.values()),
        "right_boundary_models": sum(right.values()),
        "historical_mixed_semantic_upper_nodes": 15,
        "producer_checks": checks,
        "host_elapsed_seconds": elapsed,
        "python_tracemalloc_peak_bytes": peak,
        "cases": cases,
        "odd_dimacs": odd_source,
        "even_dimacs": even_source,
        "controls": {
            "malformed_rejected": True,
            "corrupt_literal_rejected": True,
            "same_row_xor_is_not_false": True,
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in record.items() if k not in {"odd_dimacs", "even_dimacs", "cases"}}, indent=2))
    print(f"raw={OUT}")


if __name__ == "__main__":
    main()
