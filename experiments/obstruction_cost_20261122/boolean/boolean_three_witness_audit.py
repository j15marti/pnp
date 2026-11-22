#!/usr/bin/env python3
"""Independently audit a five-clause three-variable resolution-cost gap.

The BFS searches all non-tautological binary-resolution derivations by
monotonically adding derived clauses. Input reads and preprocessing are not
represented by this combinatorial inference count.
"""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import time

VARIABLES = ("x", "y", "z")
INPUT = {
    "A": (-1, -1, 0),
    "B": (0, 1, -1),
    "C": (1, 0, 1),
    "D": (-1, 1, 1),
    "E": (1, -1, -1),
}
UNIVERSE = tuple(product((-1, 0, 1), repeat=3))
INDEX = {clause: index for index, clause in enumerate(UNIVERSE)}
EMPTY = (0, 0, 0)
EMPTY_BIT = 1 << INDEX[EMPTY]
ASSIGNMENTS = tuple(product((0, 1), repeat=3))


def resolvents(left, right):
    result = set()
    for pivot in range(3):
        if not left[pivot] or left[pivot] != -right[pivot]:
            continue
        out = []
        for variable in range(3):
            if variable == pivot:
                out.append(0)
            elif left[variable] and right[variable] and left[variable] != right[variable]:
                break
            else:
                out.append(left[variable] or right[variable])
        else:
            result.add(tuple(out))
    return result


RESOLVENT_TABLE = {
    (i, j): sum(1 << INDEX[c] for c in resolvents(left, right))
    for i, left in enumerate(UNIVERSE)
    for j, right in enumerate(UNIVERSE)
    if i < j
}


def bit_indices(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def clause_true(clause, assignment):
    return any(sign and assignment[v] == (1 if sign > 0 else 0)
               for v, sign in enumerate(clause))


def exact_resolution_minimum():
    initial = sum(1 << INDEX[c] for c in INPUT.values())
    seen = {initial}
    frontier = {initial}
    layers = [{"inferences": 0, "states": 1}]
    for depth in range(1, 7):
        next_frontier = set()
        terminal = False
        for state in frontier:
            available = list(bit_indices(state))
            possible = 0
            for i, j in combinations(available, 2):
                possible |= RESOLVENT_TABLE[(i, j)]
            possible &= ~state
            if possible & EMPTY_BIT:
                terminal = True
            for clause in bit_indices(possible):
                successor = state | (1 << clause)
                if successor not in seen:
                    next_frontier.add(successor)
        layers.append({"inferences": depth, "states": len(next_frontier),
                       "empty_clause_reached": terminal})
        if terminal:
            return depth, layers
        seen.update(next_frontier)
        frontier = next_frontier
    raise AssertionError("Expected a refutation within six inferences")


def audit_explicit_proof():
    available = dict(INPUT)
    steps = [
        ("P", "D", "B", (-1, 1, 0)),
        ("N", "P", "A", (-1, 0, 0)),
        ("Q", "E", "B", (1, 0, -1)),
        ("X", "Q", "C", (1, 0, 0)),
        ("BOTTOM", "N", "X", EMPTY),
    ]
    result = []
    for label, left, right, clause in steps:
        assert clause in resolvents(available[left], available[right])
        available[label] = clause
        result.append({"label": label, "parents": [left, right], "clause": clause})
    return result


def main():
    started = time.monotonic()
    blocked = {}
    for label, clause in INPUT.items():
        blocked[label] = [a for a in ASSIGNMENTS if not clause_true(clause, a)]
    private = {}
    for omitted in INPUT:
        private[omitted] = [a for a in ASSIGNMENTS
                            if all(clause_true(c, a) for label, c in INPUT.items()
                                   if label != omitted)]
        assert private[omitted]
        assert all(not clause_true(INPUT[omitted], a) for a in private[omitted])
    assert not [a for a in ASSIGNMENTS if all(clause_true(c, a) for c in INPUT.values())]
    assert all(sum(not clause_true(c, a) for c in INPUT.values()) == 1
               for a in ASSIGNMENTS)
    unit_from_inputs = any(sum(bool(sign) for sign in resolvent) == 1
                           for left, right in combinations(INPUT.values(), 2)
                           for resolvent in resolvents(left, right))
    assert not unit_from_inputs
    optimum, layers = exact_resolution_minimum()
    assert optimum == 5
    masks = {label: sum(1 << ASSIGNMENTS.index(a) for a in assignments)
             for label, assignments in blocked.items()}
    assert sum(masks.values()) == 255
    output = {
        "scope": "Three fresh unknown Boolean variables; ordinary non-tautological binary resolution, charging one per inference.",
        "input": INPUT,
        "assignment_order": ASSIGNMENTS,
        "blocked_assignments": blocked,
        "private_assignments": private,
        "first_three_clause_models": [a for a in ASSIGNMENTS
                                      if all(clause_true(INPUT[label], a)
                                             for label in ("A", "B", "C"))],
        "minimum_unsatisfiable_core_size": 5,
        "input_pair_derives_unit": unit_from_inputs,
        "minimum_binary_resolution_inferences": optimum,
        "bfs_layers": layers,
        "explicit_proof": audit_explicit_proof(),
        "blocking_masks": masks,
        "blocking_mask_union": 255,
        "abstract_binary_mask_OR_operations": 4,
        "mask_construction_cost_included_in_OR_count": False,
        "source_acquisition_cost_included_in_inference_count": False,
        "seconds": time.monotonic() - started,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
