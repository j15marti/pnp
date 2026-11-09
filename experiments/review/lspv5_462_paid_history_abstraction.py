#!/usr/bin/env python3
"""Finite replay for LSPV-5/462 paid-history abstraction obstruction.

The concrete transition system has three states:

  fresh --(pay r)--> cached --(reuse 0)--> goal.

We enumerate every set partition (state abstraction) and assign each abstract
edge its greatest sound class-local charge: the minimum concrete edge charge
in that abstract edge class.  If ``fresh`` and ``cached`` are merged, the
projected zero-cost reuse becomes an immediately available spurious abstract
path and the abstract distance collapses to zero.
"""

from __future__ import annotations

import hashlib
import heapq
import json
from dataclasses import dataclass
from itertools import product


STATES = ("fresh", "cached", "goal")


@dataclass(frozen=True)
class Edge:
    src: str
    dst: str
    cost: int
    name: str


def canonical_partitions(n: int):
    """Yield restricted-growth strings, one per set partition."""
    for labels in product(range(n), repeat=n):
        if labels[0] != 0:
            continue
        seen_max = 0
        ok = True
        for i in range(1, n):
            if labels[i] > seen_max + 1:
                ok = False
                break
            seen_max = max(seen_max, labels[i])
        if ok:
            yield labels


def shortest(nodes, edges, start, goals):
    adj = {u: [] for u in nodes}
    for u, v, c in edges:
        adj.setdefault(u, []).append((v, c))
    dist = {start: 0}
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        if u in goals:
            return d
        for v, c in adj.get(u, ()):
            nd = d + c
            if nd < dist.get(v, 10**18):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return None


def run():
    cases = []
    assertions = 0
    for paid_cost in range(1, 9):
        concrete = (
            Edge("fresh", "cached", paid_cost, "first_insert"),
            Edge("cached", "goal", 0, "reuse"),
        )
        concrete_distance = shortest(
            STATES,
            [(e.src, e.dst, e.cost) for e in concrete],
            "fresh",
            {"goal"},
        )
        assert concrete_distance == paid_cost
        assertions += 1

        for labels in canonical_partitions(len(STATES)):
            alpha = dict(zip(STATES, labels))
            edge_class = {}
            for e in concrete:
                key = (alpha[e.src], alpha[e.dst])
                edge_class[key] = min(edge_class.get(key, 10**18), e.cost)

            abstract_nodes = tuple(sorted(set(labels)))
            abstract_edges = [(u, v, c) for (u, v), c in edge_class.items()]
            abstract_distance = shortest(
                abstract_nodes,
                abstract_edges,
                alpha["fresh"],
                {alpha["goal"]},
            )

            merges_paid_history = alpha["fresh"] == alpha["cached"]
            if merges_paid_history:
                assert abstract_distance == 0
            else:
                # Goal merging can also collapse the distance; when the goal
                # remains separate, paid-history separation recovers r here.
                if alpha["fresh"] != alpha["goal"]:
                    assert abstract_distance == paid_cost
            assert abstract_distance is not None
            assert abstract_distance <= concrete_distance
            assertions += 3

            cases.append(
                {
                    "paid_cost": paid_cost,
                    "partition": list(labels),
                    "alpha": alpha,
                    "merges_paid_history": merges_paid_history,
                    "concrete_distance": concrete_distance,
                    "abstract_distance": abstract_distance,
                    "abstract_edges": abstract_edges,
                }
            )

    summary = {
        "schema": "lspv5-462-paid-history-abstraction-v1",
        "states": list(STATES),
        "concrete_edges_template": [
            ["fresh", "cached", "r", "first_insert"],
            ["cached", "goal", 0, "reuse"],
        ],
        "paid_costs": list(range(1, 9)),
        "partition_count_per_cost": 5,
        "case_count": len(cases),
        "assertion_count": assertions,
        "merged_history_zero_count": sum(
            c["merges_paid_history"] and c["abstract_distance"] == 0
            for c in cases
        ),
        "separated_history_exact_count": sum(
            (not c["merges_paid_history"])
            and c["alpha"]["fresh"] != c["alpha"]["goal"]
            and c["abstract_distance"] == c["paid_cost"]
            for c in cases
        ),
        "cases": cases,
    }
    canonical = json.dumps(summary, sort_keys=True, separators=(",", ":"))
    summary["canonical_payload_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return summary


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
