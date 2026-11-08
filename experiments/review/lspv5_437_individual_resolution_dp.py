#!/usr/bin/env python3
"""Exact tree-DP controls for the LSPV-1/507-/508 three-goal gadget.

For each goal, /508 supplies a deletion witness for every source in the
ESSENTIAL set below.  Any binary Resolution DAG deriving that goal therefore
has at least |ESSENTIAL|-1 inference nodes.  This program independently finds
a tree proof meeting that floor, which certifies the individual minimum in
ordinary exact binary Resolution.  It says nothing about the minimum of one
joint DAG deriving all three goals, and nothing about historical R_mix341.
"""

from __future__ import annotations

import json
import resource
import time


SOURCES = [
    (1, 2, -4), (1, -2, -4), (-1, 2, -4), (-1, -2, 4),
    (2, 3, -5), (2, -3, 5), (-2, 3, 5), (-2, -3, -5),
    (1, 5, -6), (1, -5, -6), (-1, 5, -6), (-1, -5, 6),
    (4, 6, -7), (4, -6, 7), (-4, 6, 7), (-4, -6, -7),
]
GOALS = [(-1, -3, 7), (1, -7), (3, -7)]
ESSENTIAL = [
    (2, 3, 5, 7, 10, 11, 13, 14),
    (0, 1, 8, 9, 12),
    (0, 1, 2, 3, 4, 6, 8, 9, 10, 11, 12, 15),
]


def norm(clause):
    return tuple(sorted(set(clause), key=lambda x: (abs(x), -x)))


SOURCES = tuple(norm(c) for c in SOURCES)
GOALS = tuple(norm(c) for c in GOALS)


def resolvents(left, right):
    out = []
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
        if any(-x in child for x in child):
            continue
        out.append((child, pivot))
    return out


def sat(clause, assignment):
    return any(
        ((assignment >> (abs(lit) - 1)) & 1) == (1 if lit > 0 else 0)
        for lit in clause
    )


def deletion_essential_sources(goal):
    """Return sources whose deletion admits a model falsifying goal."""
    answer = []
    witnesses = {}
    for omitted in range(len(SOURCES)):
        found = None
        for assignment in range(1 << 7):
            if (all(sat(clause, assignment)
                    for i, clause in enumerate(SOURCES) if i != omitted)
                    and not sat(goal, assignment)):
                found = assignment
                break
        if found is not None:
            answer.append(omitted)
            witnesses[f"S{omitted:02d}"] = found
    return tuple(answer), witnesses


def find_tree(goal_index):
    source_ids = ESSENTIAL[goal_index]
    k = len(source_ids)
    full = (1 << k) - 1
    # table[mask][clause] = (left_mask, left_clause, right_mask,
    #                        right_clause, pivot), or None at a source leaf.
    table = [dict() for _ in range(full + 1)]
    for local, source in enumerate(source_ids):
        table[1 << local][SOURCES[source]] = None

    for size in range(2, k + 1):
        for mask in range(1, full + 1):
            if mask.bit_count() != size:
                continue
            low = mask & -mask
            left = (mask - 1) & mask
            while left:
                if left & low:
                    right = mask ^ left
                    if right and table[left] and table[right]:
                        for lc in table[left]:
                            for rc in table[right]:
                                for child, pivot in resolvents(lc, rc):
                                    table[mask].setdefault(
                                        child, (left, lc, right, rc, pivot)
                                    )
                left = (left - 1) & mask

    target = GOALS[goal_index]
    if target not in table[full]:
        raise AssertionError(f"no floor-meeting tree for goal {goal_index}")

    nodes = []
    memo = {}

    def emit(mask, clause):
        key = (mask, clause)
        if key in memo:
            return memo[key]
        if mask.bit_count() == 1:
            local = mask.bit_length() - 1
            ident = f"S{source_ids[local]:02d}"
            memo[key] = ident
            return ident
        left, lc, right, rc, pivot = table[mask][clause]
        left_id = emit(left, lc)
        right_id = emit(right, rc)
        ident = f"R{len(nodes) + 1:02d}"
        nodes.append({
            "id": ident,
            "left": left_id,
            "right": right_id,
            "pivot": pivot,
            "clause": list(clause),
        })
        memo[key] = ident
        return ident

    root = emit(full, target)
    assert len(nodes) == k - 1
    return {
        "goal": list(target),
        "essential_sources": [f"S{x:02d}" for x in source_ids],
        "lower_bound_binary_fanin_nodes": k - 1,
        "tree_witness_nodes": nodes,
        "root": root,
        "minimum_distinct_inference_nodes": k - 1,
        "reachable_clause_states": sum(len(x) for x in table),
    }


def verify(result):
    db = {f"S{i:02d}": clause for i, clause in enumerate(SOURCES)}
    for item in result["tree_witness_nodes"]:
        candidates = dict(
            (pivot, clause)
            for clause, pivot in resolvents(db[item["left"]], db[item["right"]])
        )
        assert tuple(item["clause"]) == candidates[item["pivot"]]
        db[item["id"]] = tuple(item["clause"])
    assert db[result["root"]] == tuple(result["goal"])


def main():
    started = time.perf_counter()
    deletion_checks = []
    for g, goal in enumerate(GOALS):
        computed, witnesses = deletion_essential_sources(goal)
        assert computed == ESSENTIAL[g]
        deletion_checks.append({
            "goal": list(goal),
            "essential_sources": [f"S{x:02d}" for x in computed],
            "deletion_witness_assignments": witnesses,
        })
    results = [find_tree(g) for g in range(3)]
    for result in results:
        verify(result)
    print(json.dumps({
        "status": "PROVED_RESTRICTED_EXACT_INDIVIDUAL_MINIMA",
        "scope": [
            "fixed 16-source seven-variable LSPV-1/507-/508 gadget",
            "ordinary exact binary Resolution",
            "each goal optimized separately; not the joint three-goal DAG",
            "deletion-witness essentiality imported from /508 and rechecked",
            "not historical R_mix341 acceptance",
            "not an asymptotic hard-family result",
            "P versus NP OPEN",
        ],
        "results": results,
        "deletion_essentiality_checks": deletion_checks,
        "elapsed_seconds": time.perf_counter() - started,
        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
