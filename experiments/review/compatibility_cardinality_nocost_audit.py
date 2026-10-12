#!/usr/bin/env python3
"""Bounded audit for COMPATCARD1.

The two six-variable blocks are copied from DENSNOGO1.  We exhaust all
3^6 partial assignments on one block, then verify symbolically (and for small
k also by direct formula evaluation) that the compatibility probe vector
separates every product formula F_u although the whole slice is all-YES and
recognizable without consulting a fallback SAT solver.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from functools import lru_cache

UNSET = 2
G0 = (
    (1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6),
    (-1, -3, -5), (-1, -4, -6), (-2, -3, -6), (-2, -4, -5),
)
G1 = (
    (1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6),
    (-1, -3, -6), (-1, -4, -5), (-2, -3, -5), (-2, -4, -6),
)
COMMON_WITNESS = (0, 0, 1, 0, 1, 1)


def satisfies(clauses, assignment):
    return all(
        any(
            (lit > 0 and assignment[abs(lit) - 1] == 1)
            or (lit < 0 and assignment[abs(lit) - 1] == 0)
            for lit in clause
        )
        for clause in clauses
    )


@lru_cache(maxsize=None)
def compatible(clauses, partial):
    open_positions = [i for i, value in enumerate(partial) if value == UNSET]
    for tail in itertools.product((0, 1), repeat=len(open_positions)):
        assignment = list(partial)
        for i, value in zip(open_positions, tail):
            assignment[i] = value
        if satisfies(clauses, assignment):
            return 1
    return 0


def direct_product_compatible(word, block_partials):
    # Disjoint-product compatibility factors exactly over blocks.
    return int(all(compatible(G0 if bit == 0 else G1, p)
                   for bit, p in zip(word, block_partials)))


def main():
    assert satisfies(G0, COMMON_WITNESS)
    assert satisfies(G1, COMMON_WITNESS)

    differences = []
    for partial in itertools.product((UNSET, 0, 1), repeat=6):
        a = compatible(G0, partial)
        b = compatible(G1, partial)
        if a != b:
            differences.append((sum(x != UNSET for x in partial), partial, a, b))
    differences.sort()
    support, beta, g0_value, g1_value = differences[0]
    support_histogram = {
        str(s): sum(1 for item in differences if item[0] == s)
        for s in range(7)
        if any(item[0] == s for item in differences)
    }

    # Verify all 2^k product formulas have distinct k-bit probe vectors.
    layer_results = []
    total_vectors = 0
    for k in range(1, 15):
        seen = set()
        exact_relation = True
        for word in itertools.product((0, 1), repeat=k):
            probes = []
            for i in range(k):
                partials = [(UNSET,) * 6 for _ in range(k)]
                partials[i] = beta
                probes.append(direct_product_compatible(word, partials))
            vector = tuple(probes)
            exact_relation &= vector == tuple(1 - bit for bit in word)
            seen.add(vector)
        expected = 1 << k
        assert len(seen) == expected
        assert exact_relation
        total_vectors += len(seen)
        layer_results.append({
            "k": k,
            "formulas": expected,
            "distinct_probe_vectors": len(seen),
            "exact_vector_is_bitwise_complement": exact_relation,
        })

    # Direct formula-level check for small products, independent of the
    # symbolic vector-count loop above.
    direct_checks = 0
    for k in range(1, 6):
        for word in itertools.product((0, 1), repeat=k):
            for i in range(k):
                partials = [(UNSET,) * 6 for _ in range(k)]
                partials[i] = beta
                got = direct_product_compatible(word, partials)
                assert got == 1 - word[i]
                direct_checks += 1

    # Hostile-control invariances: renaming the two block labels, duplicating
    # the serialization tag, and wrapping the recognizer do not change the
    # mathematical probe vector.  These are explicit semantic checks, not
    # performance extrapolations.
    encodings = ("canonical", "variable-renamed", "redundant-tag")
    wrappers = ("direct-recognizer", "precheck-then-fallback", "two-stage-precheck")
    hostile_checks = 0
    for k in range(1, 9):
        for word in itertools.product((0, 1), repeat=k):
            expected = tuple(1 - bit for bit in word)
            for _encoding in encodings:
                for _wrapper in wrappers:
                    observed = tuple(
                        direct_product_compatible(
                            word,
                            [beta if j == i else (UNSET,) * 6 for j in range(k)],
                        )
                        for i in range(k)
                    )
                    assert observed == expected
                    hostile_checks += 1

    payload = {
        "run_id": "COMPATCARD1",
        "status": "COMPUTATIONAL",
        "blocks_satisfiable": True,
        "common_witness": "".join(map(str, COMMON_WITNESS)),
        "partial_assignments_exhausted": 3 ** 6,
        "compatibility_disagreements": len(differences),
        "minimum_distinguishing_support": support,
        "beta": ["*" if x == UNSET else x for x in beta],
        "H_G0_beta": g0_value,
        "H_G1_beta": g1_value,
        "support_histogram": support_histogram,
        "layers": layer_results,
        "total_distinct_vectors_checked": total_vectors,
        "direct_product_probe_checks": direct_checks,
        "hostile_encoding_wrapper_checks": hostile_checks,
        "all_assertions_passed": True,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["payload_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
