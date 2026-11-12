"""Independent finite verification of the accompanying proved counterexamples.

Dependency-free. Each complete run is designed to finish below 30 seconds.
"""

from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import time


def dot(mask, value):
    return (mask & value).bit_count() & 1


def rank(vectors):
    pivots = {}
    for value in vectors:
        while value:
            bit = value.bit_length() - 1
            if bit in pivots:
                value ^= pivots[bit]
            else:
                pivots[bit] = value
                break
    return len(pivots)


def affine_rank(points):
    if not points:
        return -1
    origin = points[0]
    return rank(value ^ origin for value in points)


def models_cnf(n, clauses):
    return [value for value in range(1 << n) if all(
        any(bool((value >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause)
        for clause in clauses
    )]


def models_affine(n, equations):
    return [value for value in range(1 << n) if all(dot(mask, value) == bit for mask, bit in equations)]


def all_projections_full(points, n, arity):
    checked = 0
    for size in range(min(n, arity) + 1):
        for coordinates in combinations(range(n), size):
            images = {sum(((value >> source) & 1) << target for target, source in enumerate(coordinates)) for value in points}
            assert len(images) == 1 << size
            checked += 1
    return checked


def strings(points, n):
    return [''.join(str((value >> i) & 1) for i in range(n)) for value in points]


def main():
    started = time.perf_counter()
    chain = [(-2, 1), (-3, 2), (-4, 3), (-5, 4)]
    equations = [((1 << 1) | (1 << 2) | (1 << 4), 1),
                 ((1 << 0) | (1 << 3) | (1 << 4), 0)]
    hmodels = models_cnf(5, chain)
    amodels = models_affine(5, equations)
    assert affine_rank(hmodels) == 5
    assert set(hmodels).isdisjoint(amodels)
    projection_checks = all_projections_full(amodels, 5, 2)
    assert sorted([equations[0][0].bit_count(), equations[1][0].bit_count(),
                   (equations[0][0] ^ equations[1][0]).bit_count()]) == [3, 3, 4]
    rank_two = {
        "variables": 5,
        "H_models": strings(hmodels, 5),
        "H_affine_rank": affine_rank(hmodels),
        "A_models": len(amodels),
        "projection_checks": projection_checks,
        "intersection_models": 0,
        "dual_nonzero_weights": [3, 3, 4],
    }

    blocks = []
    for k in range(1, 5):
        t = k + 1
        n = 2 * t
        clauses = [(-(i + 1), -(j + t + 1)) for i in range(t) for j in range(t)]
        equations = [((1 << t) - 1, 1), (((1 << t) - 1) << t, 1)]
        hm = models_cnf(n, clauses)
        am = models_affine(n, equations)
        assert affine_rank(hm) == n
        assert set(hm).isdisjoint(am)
        checks = all_projections_full(am, n, k)
        blocks.append({"k": k, "variables": n, "H_clauses": len(clauses),
                       "H_affine_rank": affine_rank(hm), "A_models": len(am),
                       "full_projection_checks": checks, "intersection_models": 0})

    expansion = []
    for m in range(1, 10):
        # Bit zero is the common anchor; the remaining bits are selectors.
        closures = set()
        for choices in product(range(3), repeat=m):
            closure = 1
            for i, choice in enumerate(choices):
                closure |= 1 << (1 + 3 * i + choice)
            assert closure & 1
            assert all(((closure >> (1 + 3 * i)) & 7).bit_count() == 1 for i in range(m))
            closures.add(closure)
        assert len(closures) == 3 ** m
        expansion.append({"triples": m, "variables": 1 + 3 * m,
                          "distinct_closed_monomials": len(closures),
                          "explicit_witness": 1 | sum(1 << (1 + 3 * i) for i in range(m))})

    report = {
        "status": "all assertions passed",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "runtime_seconds": time.perf_counter() - started,
        "minimal_rank_two": rank_two,
        "bounded_projection_controls": blocks,
        "connected_expansion_controls": expansion,
        "scope": "Finite checks supplement proofs; no unrestricted complexity conclusion."
    }
    output = Path(__file__).with_name("obstruction_validation.json")
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
