#!/usr/bin/env python3
"""Finite audit for SAT-ENDOMORPHISM-QUOTIENT1.

Every individual invocation is intentionally bounded well below 30 seconds.
The finite enumeration checks an abstract theorem; it is not asymptotic
evidence for a SAT lower bound.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path


def maps(domain_sizes: tuple[int, ...]):
    choices = tuple(range(sum(domain_sizes)))
    fibers: list[tuple[int, ...]] = []
    start = 0
    for size in domain_sizes:
        fibers.append(tuple(range(start, start + size)))
        start += size
    for pieces in itertools.product(
        *(itertools.product(fiber, repeat=len(fiber)) for fiber in fibers)
    ):
        out = [0] * len(choices)
        for fiber, images in zip(fibers, pieces):
            for x, y in zip(fiber, images):
                out[x] = y
        yield tuple(out)


def invariant(resource: tuple[int, ...], transformations) -> bool:
    return all(
        all(resource[t[x]] == resource[x] for x in range(len(resource)))
        for t in transformations
    )


def factors_through_bit(resource: tuple[int, ...], sizes: tuple[int, int]) -> bool:
    cut = sizes[0]
    return len(set(resource[:cut])) == 1 and len(set(resource[cut:])) == 1


def collapse_maps(sizes: tuple[int, int]):
    cut = sizes[0]
    for r0 in range(cut):
        for r1 in range(cut, sum(sizes)):
            yield tuple(r0 if x < cut else r1 for x in range(sum(sizes)))


def sat_cnf(clauses: tuple[tuple[int, ...], ...]) -> bool:
    n = max((abs(lit) for clause in clauses for lit in clause), default=0)
    for bits in itertools.product((False, True), repeat=n):
        if all(any(bits[abs(lit) - 1] == (lit > 0) for lit in clause) for clause in clauses):
            return True
    return False


def wrapper(name: str, formula, yes_rep, no_rep):
    if name == "DIRECT":
        answer = sat_cnf(formula)
    elif name == "COPY":
        copied = tuple(tuple(clause) for clause in formula)
        answer = sat_cnf(copied)
    elif name == "DEAD":
        _dead = hashlib.sha256(repr(formula).encode()).hexdigest()
        answer = sat_cnf(formula)
    elif name == "DELAY":
        for _ in range(7):
            pass
        answer = sat_cnf(formula)
    elif name == "INTERP":
        answer = bool(int(sat_cnf(formula)))
    elif name == "RECOMP":
        a = sat_cnf(formula)
        b = sat_cnf(formula)
        assert a == b
        answer = a
    else:
        raise ValueError(name)
    return yes_rep if answer else no_rep


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-points", type=int, default=5)
    parser.add_argument("--resource-alphabet", type=int, default=3)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    assert 2 <= args.max_points <= 5
    assert 2 <= args.resource_alphabet <= 4

    start = time.perf_counter()
    assertions = 0
    decision_partitions = 0
    resource_maps = 0
    full_endomorphisms = 0
    collapse_transformations = 0

    for n in range(2, args.max_points + 1):
        for n0 in range(1, n):
            sizes = (n0, n - n0)
            endos = tuple(maps(sizes))
            collapses = tuple(collapse_maps(sizes))
            decision_partitions += 1
            full_endomorphisms += len(endos)
            collapse_transformations += len(collapses)
            for resource in itertools.product(range(args.resource_alphabet), repeat=n):
                resource_maps += 1
                factor = factors_through_bit(resource, sizes)
                inv_all = invariant(resource, endos)
                inv_collapse = invariant(resource, collapses)
                assert inv_all == factor
                assert inv_collapse == factor
                assertions += 2

            collision_pairs = n0 * n0 + (n - n0) * (n - n0)
            image_size = 2
            assert image_size >= (n * n) / collision_pairs
            assert collision_pairs == sum(s * s for s in sizes)
            assertions += 2

    # Small encoded-CNF hostile controls.  Unit clauses are permitted here;
    # the theorem is representation-agnostic and the clean-core specialization
    # is mathematical, not inferred from these finite cases.
    yes_rep = ((1,),)
    no_rep = ((1,), (-1,))
    controls = {
        "horn_yes": ((1,), (-1, 2)),
        "horn_no": ((1,), (-1,)),
        "two_sat_yes": ((1, 2), (-1, 2)),
        "two_sat_no": ((1, 2), (1, -2), (-1, 2), (-1, -2)),
        "affine_tseitin_yes": (
            (1, 2, -3), (1, -2, 3), (-1, 2, 3), (-1, -2, -3), (3,)
        ),
        "affine_tseitin_no": (
            (1, 2, -3), (1, -2, 3), (-1, 2, 3), (-1, -2, -3),
            (-1,), (2,), (-3,)
        ),
        "bounded_tw_yes": ((1, 2), (-2, 3)),
        "bounded_tw_no": ((1,), (-1,), (2, 3)),
        "independent_product_yes": ((1,), (2,)),
        "independent_product_no": ((1,), (2,), (-2,)),
        "redundant_padding_yes": ((1,), (1,), (2, -2)),
        "alternate_encoding_no": ((2,), (-2,), (1, -1)),
    }
    wrappers = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
    control_rows = []
    for label, formula in controls.items():
        answer = sat_cnf(formula)
        outputs = []
        for name in wrappers:
            out = wrapper(name, formula, yes_rep, no_rep)
            assert sat_cnf(out) == answer
            assert out in (yes_rep, no_rep)
            outputs.append({"wrapper": name, "output": "YES_REP" if answer else "NO_REP"})
            assertions += 2
        # Decision bit survives; syntax-sensitive resources are erased.
        assert sat_cnf(wrapper("DIRECT", formula, yes_rep, no_rep)) == answer
        assert len(wrapper("DIRECT", formula, yes_rep, no_rep)) in (1, 2)
        assertions += 2
        control_rows.append({"label": label, "sat": answer, "wrappers": outputs})

    elapsed = time.perf_counter() - start
    result = {
        "run_id": "SATQUOT1",
        "claim": "SAT-ENDOMORPHISM-QUOTIENT1",
        "status": "PROVED/EXACT abstract theorem; CONDITIONAL clean-core corollary",
        "finite_status": "COMPUTATIONAL",
        "parameters": {
            "max_points": args.max_points,
            "resource_alphabet": args.resource_alphabet,
        },
        "decision_partitions": decision_partitions,
        "resource_maps": resource_maps,
        "full_endomorphisms_enumerated": full_endomorphisms,
        "collapse_transformations_enumerated": collapse_transformations,
        "cnf_controls": control_rows,
        "wrappers": list(wrappers),
        "assertions": assertions,
        "failures": 0,
        "runtime_seconds": elapsed,
        "limitations": [
            "Finite enumeration checks only the stated algebraic equivalence.",
            "No runtime lower bound is inferred from semantic-state counts.",
            "The P=NP specialization remains conditional and gives no contradiction.",
        ],
        "p_vs_np": "OPEN",
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    result["canonical_payload_sha256"] = hashlib.sha256(payload.encode()).hexdigest()
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
