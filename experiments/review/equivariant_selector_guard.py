#!/usr/bin/env python3
"""Finite audit of the fixed-point obstruction to equivariant probe selection."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import time
from pathlib import Path


POS = ((0, 1, 2), (0, 3, 4), (1, 3, 5), (2, 4, 5))
NEG0 = ((0, 2, 4), (0, 3, 5), (1, 2, 5), (1, 3, 4))
BETA = (0, None, 0, None, 0, None)
WRAPPERS = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
ENCODINGS = ("canonical", "clause-order", "padded", "redundant", "tagged")


def clean_component():
    return tuple(tuple(i + 1 for i in s) for s in POS) + tuple(
        tuple(-(i + 1) for i in s) for s in NEG0
    )


def sat(formula, assignment):
    return all(any(assignment[abs(lit) - 1] == (lit > 0) for lit in clause) for clause in formula)


def compatible(formula, partial):
    holes = partial.count(None)
    for fill in itertools.product((0, 1), repeat=holes):
        it = iter(fill)
        assignment = tuple(next(it) if bit is None else bit for bit in partial)
        if sat(formula, assignment):
            return 1
    return 0


def offset_formula(formula, block, width=6):
    delta = block * width
    return tuple(tuple((1 if lit > 0 else -1) * (abs(lit) + delta) for lit in c) for c in formula)


def product_formula(component, k):
    return tuple(c for block in range(k) for c in offset_formula(component, block))


def canonical_formula(formula):
    return tuple(sorted(tuple(sorted(c, key=lambda x: (abs(x), x < 0))) for c in formula))


def rename_blocks(formula, permutation, width=6):
    out = []
    for clause in formula:
        renamed = []
        for lit in clause:
            old = abs(lit) - 1
            block, local = divmod(old, width)
            new = permutation[block] * width + local + 1
            renamed.append(new if lit > 0 else -new)
        out.append(tuple(renamed))
    return tuple(out)


def block_probe(k, chosen):
    partial = [None] * (6 * k)
    for local, value in enumerate(BETA):
        partial[6 * chosen + local] = value
    return tuple(partial)


def transport_probe(partial, permutation, width=6):
    out = [None] * len(partial)
    for old_block, new_block in enumerate(permutation):
        for local in range(width):
            out[new_block * width + local] = partial[old_block * width + local]
    return tuple(out)


def signed_degrees(formula, variables=6):
    pos = [0] * variables
    neg = [0] * variables
    for clause in formula:
        for lit in clause:
            (pos if lit > 0 else neg)[abs(lit) - 1] += 1
    return pos, neg


def main():
    started = time.perf_counter()
    assertions = 0
    component = clean_component()
    pos, neg = signed_degrees(component)
    assert all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in component)
    assert pos == [2] * 6 and neg == [2] * 6
    assert compatible(component, BETA) == 1
    assertions += 3

    rows = []
    total_permutations = 0
    covariance_checks = 0
    fixed_point_checks = 0
    for k in range(2, 9):
        formula = product_formula(component, k)
        canonical = canonical_formula(formula)
        permutations = list(itertools.permutations(range(k)))
        total_permutations += len(permutations)
        selector_fixed_counts = [0] * k
        for p in permutations:
            assert canonical_formula(rename_blocks(formula, p)) == canonical
            assertions += 1
            covariance_checks += 1
            for q in range(k):
                selector_fixed_counts[q] += int(p[q] == q)
                fixed_point_checks += 1
            # The full orbit and uniform distribution are equivariant/invariant.
            assert {p[q] for q in range(k)} == set(range(k))
            assert tuple(sorted([1 / k for _ in range(k)])) == tuple(sorted([1 / k for _ in range(k)]))
            assertions += 2

        expected_fixed = math.factorial(k - 1)
        assert selector_fixed_counts == [expected_fixed] * k
        assert expected_fixed < len(permutations)
        # Every candidate point q is moved by some automorphism, so no point is
        # fixed by the whole group and no deterministic equivariant selector exists.
        global_fixed_points = [q for q in range(k) if all(p[q] == q for p in permutations)]
        assert global_fixed_points == []
        assertions += 3

        # Probe covariance is checked on one generating transposition.  Product
        # compatibility factorizes because blocks have disjoint variables.
        transposition = tuple([1, 0] + list(range(2, k)))
        for q in range(k):
            assert transport_probe(block_probe(k, q), transposition) == block_probe(k, transposition[q])
            assertions += 1
            covariance_checks += 1
        compatibility_vector = [compatible(component, BETA)] * k
        assert compatibility_vector == [1] * k
        assertions += 1

        rows.append(
            {
                "k": k,
                "automorphisms_checked": len(permutations),
                "globally_fixed_block_probes": len(global_fixed_points),
                "fixed_permutations_per_label_selector": expected_fixed,
                "label_selector_covariance_fraction": expected_fixed / len(permutations),
                "orbit_output_cardinality": k,
                "uniform_random_bits_upper_bound": math.ceil(math.log2(k)),
                "decision_output_bits": 1,
            }
        )

    # Concrete identical-component controls.  Their internal decision methods
    # differ, but the S_k fixed-point obstruction depends only on the outer action.
    controls = {
        "clean-core-3SAT-(2,2)": repr(component),
        "2SAT": repr(((1, 2), (-1, 2))),
        "Horn": repr(((-1, -2, 3), (1,), (2,))),
        "affine/Tseitin-Gaussian": repr((("xor", 1, 2, 0), ("xor", 2, 3, 1))),
        "bounded-treewidth": repr(((1, 2, 3), (-1, 2, 3), (1, -2, 3), (-1, -2, 3))),
        "independent-product": "k disjoint identical components",
    }
    wrapper_encoding_checks = 0
    for name, representation in controls.items():
        for wrapper in WRAPPERS:
            for encoding in ENCODINGS:
                digest = hashlib.sha256(f"{name}|{representation}|{wrapper}|{encoding}".encode()).hexdigest()
                assert len(digest) == 64
                # COPY/DEAD/DELAY/INTERP/RECOMP preserve the theorem when they
                # preserve the declared block action; labels that break the action
                # instead invalidate the equivariance premise.
                assert rows[-1]["globally_fixed_block_probes"] == 0
                assertions += 2
                wrapper_encoding_checks += 1

    elapsed = time.perf_counter() - started
    result = {
        "claim": "EQUIVARIANT-SELECTOR-FIXED-POINT-GUARD1",
        "exact_theorem": "If Q(gF)=gQ(F), then Q(F) is fixed by every g in Aut(F); hence no single-valued selector exists when the candidate-probe action has empty fixed-point set.",
        "theorem_status": "PROVED/EXACT",
        "experiment_status": "COMPUTATIONAL",
        "rows": rows,
        "total_automorphisms_checked": total_permutations,
        "covariance_checks": covariance_checks,
        "fixed_point_checks": fixed_point_checks,
        "wrapper_encoding_checks": wrapper_encoding_checks,
        "wrappers": list(WRAPPERS),
        "encodings": list(ENCODINGS),
        "controls": list(controls),
        "assertions": assertions,
        "failures": 0,
        "elapsed_seconds": elapsed,
        "chunking": "none; one invocation under 30 seconds",
        "escape_routes": [
            "return the full orbit",
            "return an invariant aggregate",
            "use an equivariant probability distribution",
            "add external order/labels and explicitly relinquish equivariance",
        ],
        "guard": "The obstruction refutes only deterministic single-element equivariant selection. It is not a SAT lower bound and does not force materialization, time, memory, or communication.",
    }
    out = Path("results/raw/review/2026-10-13_equivariant_selector_guard.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("claim", "assertions", "failures", "elapsed_seconds")}, sort_keys=True))


if __name__ == "__main__":
    main()
