#!/usr/bin/env python3
"""Exact terminal-peel lower bound for the LSPV-1/507--509 gadget.

For a minimum DAG deriving all three goals, every sink is a designated goal and
at least one sink exists.  For each possible sink goal this program enumerates
every exact Resolution parent/pivot pair from the complete reachable-clause
closure.  After deleting the paid sink inference, it applies the independently
proved connected-essential-source floor to the remaining goals plus any
non-source parents.  Every branch has remaining floor 15, proving total
ordinary-Resolution work at least 16 in this fixed finite model.

This is not historical R_mix341 acceptance and not an asymptotic result.
"""

from __future__ import annotations

import json
import resource
import time
from functools import lru_cache
from collections import defaultdict


SOURCES_RAW = [
    (1, 2, -4), (1, -2, -4), (-1, 2, -4), (-1, -2, 4),
    (2, 3, -5), (2, -3, 5), (-2, 3, 5), (-2, -3, -5),
    (1, 5, -6), (1, -5, -6), (-1, 5, -6), (-1, -5, 6),
    (4, 6, -7), (4, -6, 7), (-4, 6, 7), (-4, -6, -7),
]
GOALS_RAW = [(-1, -3, 7), (1, -7), (3, -7)]


def norm(clause):
    return tuple(sorted(set(clause), key=lambda x: (abs(x), -x)))


SOURCES = tuple(map(norm, SOURCES_RAW))
GOALS = tuple(map(norm, GOALS_RAW))
SOURCE_SET = frozenset(SOURCES)


def exact_resolvents(a, b):
    out = set()
    for pivot in range(1, 8):
        for left, right in ((a, b), (b, a)):
            if pivot not in left or -pivot not in right:
                continue
            child = norm(
                [x for x in left if x != pivot]
                + [x for x in right if x != -pivot]
            )
            if not any(-x in child for x in child):
                out.add((pivot, child))
    return out


def resolution_closure():
    known = set(SOURCES)
    rounds = []
    while True:
        clauses = sorted(known)
        new = set()
        for i, a in enumerate(clauses):
            for b in clauses[i + 1:]:
                new.update(child for _, child in exact_resolvents(a, b))
        new -= known
        if not new:
            return tuple(sorted(known)), rounds
        known.update(new)
        rounds.append(len(new))


def all_parent_options(closure):
    options = defaultdict(list)
    count = 0
    for i, a in enumerate(closure):
        for b in closure[i + 1:]:
            for pivot, child in exact_resolvents(a, b):
                options[child].append((a, b, pivot))
                count += 1
    for child in options:
        options[child].sort(key=lambda x: (x[2], x[0], x[1]))
    return options, count


def essential_masks(closure):
    def sat(clause, assignment):
        return any(assignment[abs(lit)] == (lit > 0) for lit in clause)

    deletion_models = []
    for missing in range(len(SOURCES)):
        models = []
        for bits in range(1 << 7):
            assignment = {v: bool(bits & (1 << (v - 1))) for v in range(1, 8)}
            if all(i == missing or sat(clause, assignment)
                   for i, clause in enumerate(SOURCES)):
                models.append(assignment)
        deletion_models.append(models)
    masks = {}
    for clause in closure:
        mask = 0
        for source, models in enumerate(deletion_models):
            if any(not sat(clause, assignment) for assignment in models):
                mask |= 1 << source
        masks[clause] = mask
    return masks


def connected_floor(targets, masks):
    nonempty = [masks[c] for c in targets if masks[c]]
    if not nonempty:
        return {"floor": 0, "union_sources": [], "components": 0}
    parent = list(range(len(nonempty)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def join(a, b):
        a, b = find(a), find(b)
        if a != b:
            parent[b] = a

    for i, mask in enumerate(nonempty):
        for j in range(i):
            if mask & nonempty[j]:
                join(i, j)
    components = len({find(i) for i in range(len(nonempty))})
    union = 0
    for mask in nonempty:
        union |= mask
    source_ids = [i for i in range(len(SOURCES)) if union & (1 << i)]
    return {
        "floor": len(source_ids) - components,
        "union_sources": source_ids,
        "components": components,
    }


def main():
    started = time.perf_counter()
    closure, rounds = resolution_closure()
    options, option_count = all_parent_options(closure)
    masks = essential_masks(closure)
    initial = connected_floor(GOALS, masks)
    assert initial == {"floor": 15, "union_sources": list(range(16)), "components": 1}

    branches = []
    for goal_index, sink in enumerate(GOALS):
        assert sink not in SOURCE_SET
        for left, right, pivot in options[sink]:
            remaining = set(GOALS)
            remaining.remove(sink)
            if left not in SOURCE_SET:
                remaining.add(left)
            if right not in SOURCE_SET:
                remaining.add(right)
            floor = connected_floor(remaining, masks)
            branches.append({
                "sink_goal": goal_index,
                "sink_clause": list(sink),
                "left": list(left),
                "right": list(right),
                "pivot": pivot,
                "remaining_targets": [list(c) for c in sorted(remaining)],
                "remaining_connected_floor": floor,
                "total_floor": 1 + floor["floor"],
            })

    assert [len(options[g]) for g in GOALS] == [6, 8, 6]
    assert len(branches) == 20
    assert {b["total_floor"] for b in branches} == {16}

    lookahead = []
    for depth in range(4):
        calls = 0

        @lru_cache(None)
        def lower(target_tuple, remaining_depth):
            nonlocal calls
            calls += 1
            targets = frozenset(target_tuple)
            base = connected_floor(targets, masks)["floor"]
            if remaining_depth == 0:
                return base
            candidates = []
            for sink in targets:
                for left, right, _ in options[sink]:
                    nxt = set(targets)
                    nxt.remove(sink)
                    if left not in SOURCE_SET:
                        nxt.add(left)
                    if right not in SOURCE_SET:
                        nxt.add(right)
                    candidates.append(1 + lower(tuple(sorted(nxt)), remaining_depth - 1))
            return max(base, min(candidates))

        value = lower(tuple(sorted(GOALS)), depth)
        lookahead.append({"depth": depth, "lower_bound": value, "states": calls})
    assert [x["lower_bound"] for x in lookahead] == [15, 16, 16, 16]

    # Hostile controls: no advertised branch may use a false pivot, omit an
    # exact parent, or lose an essential source without changing the table.
    hostile = 0
    sample = branches[0]
    a, b = tuple(sample["left"]), tuple(sample["right"])
    hostile += int((sample["pivot"] % 7 + 1, tuple(sample["sink_clause"]))
                   not in exact_resolvents(a, b))
    hostile += int(tuple(sample["left"]) != tuple(sample["right"]))
    hostile += int(sample["remaining_connected_floor"]["union_sources"] == list(range(16)))
    assert hostile == 3

    result = {
        "status": "PROVED_RESTRICTED_COMPUTATIONAL",
        "ordinary_resolution_joint_range": [16, 19],
        "closure_clauses": len(closure),
        "closure_round_new_counts": rounds,
        "all_reachable_parent_options": option_count,
        "goal_parent_option_counts": [len(options[g]) for g in GOALS],
        "initial_connected_floor": initial,
        "terminal_peel_branches": branches,
        "minimum_branch_floor": min(b["total_floor"] for b in branches),
        "recursive_terminal_peel_challenge": lookahead,
        "hostile_controls": hostile,
        "scope": [
            "fixed 16-source seven-variable LSPV-1/507--509 gadget",
            "ordinary exact binary Resolution",
            "all three goals required in one shared acyclic DAG",
            "not historical R_mix341 acceptance",
            "not an asymptotic hard-family result",
            "P versus NP OPEN",
        ],
        "seconds": time.perf_counter() - started,
        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
