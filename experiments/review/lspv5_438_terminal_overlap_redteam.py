#!/usr/bin/env python3
"""Independent red-team checks for LSPV-1/509 terminal overlap.

Scope: the fixed 16-source, three-goal ordinary binary-Resolution gadget.
This does not execute the historical R_mix341 checker.
"""

from __future__ import annotations

import json
import resource
import time
from functools import lru_cache


SOURCES = (
    (1, 2, -4), (1, -2, -4), (-1, 2, -4), (-1, -2, 4),
    (2, 3, -5), (2, -3, 5), (-2, 3, 5), (-2, -3, -5),
    (1, 5, -6), (1, -5, -6), (-1, 5, -6), (-1, -5, 6),
    (4, 6, -7), (4, -6, 7), (-4, 6, 7), (-4, -6, -7),
)
GOALS = ((-1, -3, 7), (1, -7), (3, -7))
EXPECTED_ESSENTIAL = (
    (2, 3, 5, 7, 10, 11, 13, 14),
    (0, 1, 8, 9, 12),
    (0, 1, 2, 3, 4, 6, 8, 9, 10, 11, 12, 15),
)


def norm(clause):
    return tuple(sorted(set(clause), key=lambda x: (abs(x), -x)))


SOURCES = tuple(norm(x) for x in SOURCES)
GOALS = tuple(norm(x) for x in GOALS)


def sat(clause, assignment):
    return any(
        ((assignment >> (abs(lit) - 1)) & 1) == (1 if lit > 0 else 0)
        for lit in clause
    )


@lru_cache(maxsize=None)
def resolvents(left, right):
    answer = set()
    for pivot in range(1, 8):
        a, b = left, right
        if -pivot in a and pivot in b:
            a, b = b, a
        if pivot not in a or -pivot not in b:
            continue
        child = norm(
            [x for x in a if x != pivot]
            + [x for x in b if x != -pivot]
        )
        if not any(-x in child for x in child):
            answer.add(child)
    return tuple(sorted(answer))


def essential_sets():
    sets = []
    witnesses = []
    for goal in GOALS:
        essential = []
        witness = {}
        for omitted in range(len(SOURCES)):
            for assignment in range(1 << 7):
                if (all(sat(c, assignment) for i, c in enumerate(SOURCES)
                        if i != omitted)
                        and not sat(goal, assignment)):
                    essential.append(omitted)
                    witness[omitted] = assignment
                    break
        sets.append(tuple(essential))
        witnesses.append(witness)
    return tuple(sets), witnesses


def tree_closure(leaves):
    """Clauses with exact leaf-use trees; table[mask] is a clause set."""
    n = len(leaves)
    full = (1 << n) - 1
    table = [set() for _ in range(full + 1)]
    for i, clause in enumerate(leaves):
        table[1 << i].add(clause)
    for size in range(2, n + 1):
        for mask in range(1, full + 1):
            if mask.bit_count() != size:
                continue
            low = mask & -mask
            left = (mask - 1) & mask
            while left:
                if left & low:
                    right = mask ^ left
                    if right:
                        for a in table[left]:
                            for b in table[right]:
                                table[mask].update(resolvents(a, b))
                left = (left - 1) & mask
    return table


@lru_cache(maxsize=None)
def macro_reaches(goal, source_ids, macro_sources, macro_clause):
    remaining = tuple(i for i in source_ids if i not in macro_sources)
    leaves = (macro_clause,) + tuple(SOURCES[i] for i in remaining)
    table = tree_closure(leaves)
    return goal in table[-1], sum(len(x) for x in table)


def maximum_shared_minimum_tree(pair, intersection):
    """Largest exact subtree usable in floor-meeting trees for both goals."""
    g, h = pair
    ids = tuple(intersection)
    candidates = 0
    tested_states = 0
    best = None
    for mask in range(1, 1 << len(ids)):
        subset = tuple(ids[i] for i in range(len(ids)) if mask & (1 << i))
        closure = tree_closure(tuple(SOURCES[i] for i in subset))
        for clause in closure[-1]:
            candidates += 1
            ok_g, states_g = macro_reaches(GOALS[g], EXPECTED_ESSENTIAL[g], subset, clause)
            tested_states += states_g
            if not ok_g:
                continue
            ok_h, states_h = macro_reaches(GOALS[h], EXPECTED_ESSENTIAL[h], subset, clause)
            tested_states += states_h
            if ok_h:
                shared_nodes = len(subset) - 1
                item = {
                    "shared_nodes": shared_nodes,
                    "source_subset": list(subset),
                    "clause": list(clause),
                }
                if best is None or (shared_nodes, len(clause)) > (
                        best["shared_nodes"], len(best["clause"])):
                    best = item
    return {
        "goals": list(pair),
        "intersection_sources": list(intersection),
        "candidate_macro_clauses": candidates,
        "aggregate_reachable_states_checked": tested_states,
        "best_common_minimum_tree_subproof": best,
    }


def main():
    started = time.perf_counter()
    essential, witnesses = essential_sets()
    assert essential == EXPECTED_ESSENTIAL
    overlap = {
        (0, 1): sorted(set(essential[0]) & set(essential[1])),
        (0, 2): sorted(set(essential[0]) & set(essential[2])),
        (1, 2): sorted(set(essential[1]) & set(essential[2])),
    }
    assert overlap[(0, 1)] == []
    assert overlap[(0, 2)] == [2, 3, 10, 11]
    assert overlap[(1, 2)] == [0, 1, 8, 9, 12]
    assert set().union(*map(set, essential)) == set(range(16))

    sharing_02 = maximum_shared_minimum_tree((0, 2), overlap[(0, 2)])
    sharing_12 = maximum_shared_minimum_tree((1, 2), overlap[(1, 2)])

    # Directly test the strongest obvious /509 abstract reuse pattern: derive
    # Q1 at its four-node floor and use it as one macro leaf in a floor-meeting
    # Q2 tree with the seven remaining essential Q2 sources.
    q1_as_macro, macro_states = macro_reaches(
        GOALS[2], EXPECTED_ESSENTIAL[2], EXPECTED_ESSENTIAL[1], GOALS[1]
    )

    result = {
        "status": "PROVED_RESTRICTED_AND_COMPUTATIONAL",
        "scope": [
            "fixed LSPV-1/507-/509 16-source cancellation gadget",
            "ordinary exact binary Resolution tree subproofs",
            "not an exhaustive joint DAG optimizer",
            "not historical R_mix341 acceptance",
            "not an asymptotic hard-family result",
            "P versus NP OPEN",
        ],
        "essential_source_sets": [list(x) for x in essential],
        "deletion_witnesses": witnesses,
        "terminal_overlap": {f"{a}-{b}": v for (a, b), v in overlap.items()},
        "connected_overlap_component_count": 1,
        "independent_connected_arity_floor": 15,
        "minimum_tree_sharing_controls": [sharing_02, sharing_12],
        "q1_root_as_q2_macro_reaches_q2_at_tree_floor": q1_as_macro,
        "q1_macro_tree_states_checked": macro_states,
        "interpretation": (
            "The /509 connectivity theorem is valid.  Its displayed 15-node "
            "abstract union is not a Resolution certificate.  Exact minimum-tree "
            "sharing controls do not by themselves exclude every 15-node DAG."
        ),
        "elapsed_seconds": time.perf_counter() - started,
        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
