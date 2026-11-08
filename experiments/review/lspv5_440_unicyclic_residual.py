#!/usr/bin/env python3
"""Exact tree-residual challenge for the /507--/510 three-goal gadget.

If a legal 16-inference proof existed, /510 plus /439 would make the graph
obtained after deleting a sink goal a connected 15-inference/16-source tree.
This program challenges each of the 20 exact sink-parent branches by a complete
recursive decomposition of any such tree at one of its sink targets.

The search is deliberately finite and restricted to exact proper Resolution.
It is not an R_mix341 checker and not an asymptotic lower bound.
"""

from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
import json
import pathlib
import resource
import sys
import time


SOURCES_RAW = [
    (1, 2, -4), (1, -2, -4), (-1, 2, -4), (-1, -2, 4),
    (2, 3, -5), (2, -3, 5), (-2, 3, 5), (-2, -3, -5),
    (1, 5, -6), (1, -5, -6), (-1, 5, -6), (-1, -5, 6),
    (4, 6, -7), (4, -6, 7), (-4, 6, 7), (-4, -6, -7),
]
GOALS_RAW = [(-1, -3, 7), (1, -7), (3, -7)]


def norm(clause):
    return tuple(sorted(set(clause), key=lambda x: (abs(x), -x)))


SOURCES = tuple(norm(c) for c in SOURCES_RAW)
GOALS = tuple(norm(c) for c in GOALS_RAW)
SOURCE_INDEX = {c: i for i, c in enumerate(SOURCES)}
FULL = (1 << len(SOURCES)) - 1


def resolvents(a, b):
    out = set()
    for p in range(1, 8):
        for left, right in ((a, b), (b, a)):
            if p not in left or -p not in right:
                continue
            child = norm([x for x in left if x != p] +
                         [x for x in right if x != -p])
            if not any(-x in child for x in child):
                out.add((p, child))
    return out


def closure_and_options():
    known = set(SOURCES)
    while True:
        old = sorted(known)
        new = set()
        for i, a in enumerate(old):
            for b in old[i + 1:]:
                new.update(c for _, c in resolvents(a, b))
        new -= known
        if not new:
            break
        known.update(new)
    closure = tuple(sorted(known))
    options = defaultdict(list)
    for i, a in enumerate(closure):
        for b in closure[i + 1:]:
            for p, c in resolvents(a, b):
                options[c].append((a, b, p))
    return closure, options


def essential_masks(closure):
    def sat(clause, bits):
        return any(bool(bits & (1 << (abs(x) - 1))) == (x > 0)
                   for x in clause)

    deletion_models = []
    for missing in range(16):
        deletion_models.append([
            bits for bits in range(1 << 7)
            if all(i == missing or sat(c, bits)
                   for i, c in enumerate(SOURCES))
        ])
    answer = {}
    for c in closure:
        m = 0
        for i, models in enumerate(deletion_models):
            if any(not sat(c, bits) for bits in models):
                m |= 1 << i
        answer[c] = m
    return answer


def main():
    started = time.perf_counter()
    closure, options = closure_and_options()
    essential = essential_masks(closure)
    stats = defaultdict(int)

    @lru_cache(None)
    def possible(source_mask, targets_tuple):
        """Whether one connected underlying tree can derive all targets.

        The tree contains exactly the selected source vertices and therefore
        exactly popcount(source_mask)-1 binary inference vertices.  Every sink
        must be among targets.  The caller uses unique-clause normal form:
        in a minimum acyclic proof, a later node repeating an earlier clause
        can be redirected to the earlier node and deleted.  Internal recursive
        components are still allowed to reuse a clause label independently,
        which only relaxes the search.
        """
        stats["states"] += 1
        targets = tuple(dict.fromkeys(targets_tuple))
        if any(essential[t] & ~source_mask for t in targets):
            stats["essential_prunes"] += 1
            return False
        m = source_mask.bit_count()
        if m == 1:
            source = SOURCES[source_mask.bit_length() - 1]
            return all(t == source for t in targets)
        if not targets:
            return False

        # In a finite pruned DAG/tree at least one sink is a designated target.
        for sink_i, sink in enumerate(targets):
            if sink in SOURCE_INDEX:
                continue
            rest = targets[:sink_i] + targets[sink_i + 1:]
            for left, right, _pivot in options[sink]:
                stats["parent_options"] += 1
                # Assign the remaining requested clauses to the two components.
                # A clause identical to a parent is forced to that component.
                free = [t for t in rest if t != left and t != right]
                if any(t == left == right for t in rest):
                    continue
                for assign in range(1 << len(free)):
                    lt = [left]
                    rt = [right]
                    for j, t in enumerate(free):
                        (rt if assign & (1 << j) else lt).append(t)
                    # Existing parent targets were removed from free and are
                    # already represented once on their forced side.
                    l_need = 0
                    r_need = 0
                    for t in lt:
                        l_need |= essential[t]
                    for t in rt:
                        r_need |= essential[t]
                    if l_need & r_need or (l_need | r_need) & ~source_mask:
                        stats["partition_prunes"] += 1
                        continue
                    leftover = source_mask & ~(l_need | r_need)
                    sub = leftover
                    while True:
                        lm = l_need | sub
                        rm = source_mask ^ lm
                        if lm and rm:
                            # Canonicalize target sets but keep clauses exact.
                            lkey = tuple(sorted(set(lt)))
                            rkey = tuple(sorted(set(rt)))
                            if possible(lm, lkey) and possible(rm, rkey):
                                return True
                        if sub == 0:
                            break
                        sub = (sub - 1) & leftover
        return False

    # Positive completeness controls: the three exact individual tree minima
    # from /437 must be rediscovered on their indispensable source sets.  A
    # two-source one-step tree is checked separately below.
    individual_masks = [
        sum(1 << i for i in (2, 3, 5, 7, 10, 11, 13, 14)),
        sum(1 << i for i in (0, 1, 8, 9, 12)),
        sum(1 << i for i in (0, 1, 2, 3, 4, 6, 8, 9, 10, 11, 12, 15)),
    ]
    positive_controls = [
        possible(mask, (goal,))
        for mask, goal in zip(individual_masks, GOALS)
    ]
    one_step = next(iter(resolvents(SOURCES[0], SOURCES[1])))[1]
    positive_controls.append(possible(0b11, (one_step,)))
    assert positive_controls == [True, True, True, True]

    branches = []
    for goal_index, sink in enumerate(GOALS):
        for left, right, pivot in options[sink]:
            targets = set(GOALS)
            targets.remove(sink)
            if left not in SOURCE_INDEX:
                targets.add(left)
            if right not in SOURCE_INDEX:
                targets.add(right)
            ok = possible(FULL, tuple(sorted(targets)))
            branches.append({
                "peeled_goal": goal_index,
                "left": list(left), "right": list(right), "pivot": pivot,
                "residual_tree_exists": ok,
            })
            print("BRANCH", len(branches), ok, "states", stats["states"],
                  file=sys.stderr, flush=True)

    result = {
        "status": "PROVED_RESTRICTED_COMPUTATIONAL",
        "branches": branches,
        "all_16_node_proofs_excluded": all(not b["residual_tree_exists"] for b in branches),
        "stats": dict(stats),
        "cache": possible.cache_info()._asdict(),
        "positive_tree_controls": positive_controls,
        "seconds": time.perf_counter() - started,
        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "scope": [
            "fixed /507--/510 source and three goals",
            "exact proper binary Resolution",
            "tree residual forced by hypothetical q=16",
            "unique-clause normal form; duplicate derived nodes are eliminable by topological redirection",
            "independent recursive components may reuse labels as a relaxation",
            "not historical R_mix341",
            "not an asymptotic result",
            "P versus NP OPEN",
        ],
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    out = pathlib.Path(
        "experiments/review/raw/lspv5_440_unicyclic_residual_results.json"
    )
    out.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
