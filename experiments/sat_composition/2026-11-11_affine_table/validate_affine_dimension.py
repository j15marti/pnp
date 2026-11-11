"""Exhaustive finite checks for proved affine-interface dimension statements.

These checks supplement the mathematical proofs; they are not asymptotic evidence.
No external packages are needed.
"""

from itertools import combinations
from pathlib import Path
import hashlib
import json
import time


def rank(vectors):
    basis = {}
    for value in vectors:
        while value:
            bit = value.bit_length() - 1
            if bit in basis:
                value ^= basis[bit]
            else:
                basis[bit] = value
                break
    return len(basis)


def affine_dimension(points):
    if not points:
        return 0
    origin = next(iter(points))
    return rank(x ^ origin for x in points)


def periods(points, n):
    if not points:
        return set(range(1 << n))
    return {t for t in range(1 << n) if {x ^ t for x in points} == points}


def rho(points, n):
    if not points:
        return 0
    return affine_dimension(points) - rank(periods(points, n))


def project(points, coordinates):
    return {
        sum(((point >> source) & 1) << target for target, source in enumerate(coordinates))
        for point in points
    }


def main():
    started = time.perf_counter()
    n = 3
    relations = [{x for x in range(1 << n) if (mask >> x) & 1} for mask in range(1 << (1 << n))]
    widths = [rho(relation, n) for relation in relations]
    intersection_checks = 0
    for i, first in enumerate(relations):
        for j, second in enumerate(relations):
            assert rho(first & second, n) <= widths[i] + widths[j]
            intersection_checks += 1

    projection_checks = 0
    for relation, width in zip(relations, widths):
        for k in range(n + 1):
            for coordinates in combinations(range(n), k):
                assert rho(project(relation, coordinates), k) <= width
                projection_checks += 1

    clause = set(range(1, 8))
    assert rho(clause, 3) == 3
    exclusions = {a: rho(clause - {a}, 3) for a in clause}
    assert set(exclusions.values()) == {2}

    product_results = []
    for m in range(1, 4):
        total_bits = 3 * m
        support = {x for x in range(1 << total_bits) if all(((x >> (3 * j)) & 7) != 0 for j in range(m))}
        width = rho(support, total_bits)
        assert width == total_bits
        assert len(support) == 7 ** m
        product_results.append({"clauses": m, "models": len(support), "rho": width})

    union_results = []
    for size in range(1, 4):
        mask = (1 << size) - 1
        first = {x for x in range(1 << (2 * size)) if (x & mask) == 0}
        second = {x for x in range(1 << (2 * size)) if (x >> size) == 0}
        assert rho(first, 2 * size) == rho(second, 2 * size) == 0
        assert rho(first | second, 2 * size) == 2 * size
        union_results.append({"block_bits": size, "rho_union": 2 * size})

    report = {
        "intersection_checks": intersection_checks,
        "projection_checks": projection_checks,
        "single_exclusion_rho": exclusions,
        "disjoint_clause_products": product_results,
        "affine_union_growth": union_results,
        "status": "all assertions passed",
        "scope": "PROVED representation inequalities; all-input polynomial bound OPEN",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "runtime_seconds": time.perf_counter() - started
    }
    Path(__file__).with_name("affine_dimension_validation.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
