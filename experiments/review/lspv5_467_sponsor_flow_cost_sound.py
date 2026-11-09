#!/usr/bin/env python3
"""Exhaustive audit of a Hall/max-flow certificate for DAG cost soundness.

Abstract charged nodes have demands.  Concrete paid nodes have count-once
capacities.  An eligibility edge means that a rule/context/provenance
certificate permits that concrete node to sponsor that abstract charge.

The script compares the generalized Hall inequalities with an independently
implemented integer max-flow decision.  It is an accounting-layer model, not
the historical R_mix341 checker and not a rule-coverage proof.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import resource
import time
from collections import deque
from pathlib import Path


def hall_feasible(eligibility, demands, capacities):
    m = len(demands)
    for subset in range(1, 1 << m):
        demand = sum(demands[u] for u in range(m) if subset >> u & 1)
        neighbors = set()
        for u in range(m):
            if subset >> u & 1:
                neighbors.update(eligibility[u])
        capacity = sum(capacities[v] for v in neighbors)
        if demand > capacity:
            return False, {
                "abstract_subset": [u for u in range(m) if subset >> u & 1],
                "neighbor_sponsors": sorted(neighbors),
                "demand": demand,
                "capacity": capacity,
            }
    return True, None


def maxflow_feasible(eligibility, demands, capacities):
    m, n = len(demands), len(capacities)
    source, sink = 0, 1 + m + n
    size = sink + 1
    cap = [[0] * size for _ in range(size)]
    total = sum(demands)
    for u, demand in enumerate(demands):
        cap[source][1 + u] = demand
        for v in eligibility[u]:
            cap[1 + u][1 + m + v] = total
    for v, capacity in enumerate(capacities):
        cap[1 + m + v][sink] = capacity

    flow = 0
    while True:
        parent = [-1] * size
        parent[source] = source
        q = deque([source])
        while q and parent[sink] < 0:
            x = q.popleft()
            for y in range(size):
                if parent[y] < 0 and cap[x][y] > 0:
                    parent[y] = x
                    q.append(y)
        if parent[sink] < 0:
            break
        aug = total
        y = sink
        while y != source:
            x = parent[y]
            aug = min(aug, cap[x][y])
            y = x
        y = sink
        while y != source:
            x = parent[y]
            cap[x][y] -= aug
            cap[y][x] += aug
            y = x
        flow += aug
    return flow == total, flow


def local_individual_feasible(eligibility, demands, capacities):
    return all(any(capacities[v] >= demands[u] for v in eligibility[u])
               for u in range(len(demands)))


def enumerate_cases(max_side):
    counts = {
        "cases": 0,
        "feasible": 0,
        "infeasible": 0,
        "hall_flow_mismatches": 0,
        "locally_safe_globally_unsafe": 0,
    }
    witness = None
    for m in range(1, max_side + 1):
        for n in range(1, max_side + 1):
            nonempty_masks = range(1, 1 << n)
            for masks in itertools.product(nonempty_masks, repeat=m):
                eligibility = [tuple(v for v in range(n) if mask >> v & 1)
                               for mask in masks]
                for demands in itertools.product((1, 2, 3), repeat=m):
                    for capacities in itertools.product((0, 1, 2, 3), repeat=n):
                        hall, cut = hall_feasible(eligibility, demands, capacities)
                        flow, value = maxflow_feasible(eligibility, demands, capacities)
                        counts["cases"] += 1
                        counts["feasible" if hall else "infeasible"] += 1
                        if hall != flow:
                            counts["hall_flow_mismatches"] += 1
                        if local_individual_feasible(eligibility, demands, capacities) and not hall:
                            counts["locally_safe_globally_unsafe"] += 1
                            if witness is None:
                                witness = {
                                    "eligibility": eligibility,
                                    "demands": demands,
                                    "capacities": capacities,
                                    "violating_cut": cut,
                                    "maxflow": value,
                                }
    return counts, witness


def explicit_controls():
    controls = {}
    cases = {
        "shared_duplication": ([(0,), (0,)], (1, 1), (1,)),
        "scaled_half_partition": ([(0,), (0,)], (1, 1), (2,)),
        "separate_sponsors": ([(0,), (1,)], (1, 1), (1, 1)),
        "safe_collapse": ([(0, 1)], (1,), (1, 1)),
        "context_erased": ([(0, 1), (0, 1)], (1, 1), (1, 1)),
        "context_exact": ([(0,), (0,)], (1, 1), (1, 1)),
    }
    for name, (eligibility, demands, capacities) in cases.items():
        hall, cut = hall_feasible(eligibility, demands, capacities)
        flow, value = maxflow_feasible(eligibility, demands, capacities)
        controls[name] = {
            "eligibility": eligibility,
            "demands": demands,
            "capacities": capacities,
            "hall_feasible": hall,
            "maxflow_feasible": flow,
            "maxflow_value": value,
            "violating_cut": cut,
            "locally_individual_feasible": local_individual_feasible(
                eligibility, demands, capacities),
        }
    return controls


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-side", type=int, default=3)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if not 1 <= args.max_side <= 4:
        raise SystemExit("max-side must be 1..4")
    started = time.perf_counter()
    counts, witness = enumerate_cases(args.max_side)
    controls = explicit_controls()
    status = "PASS" if (
        counts["hall_flow_mismatches"] == 0
        and counts["locally_safe_globally_unsafe"] > 0
        and not controls["shared_duplication"]["hall_feasible"]
        and controls["scaled_half_partition"]["hall_feasible"]
        and controls["separate_sponsors"]["hall_feasible"]
        and controls["safe_collapse"]["hall_feasible"]
        and controls["context_erased"]["hall_feasible"]
        and not controls["context_exact"]["hall_feasible"]
    ) else "FAIL"
    result = {
        "status": status,
        "scope": (
            "finite integer sponsor-flow accounting model; not the authoritative "
            "R_mix341 checker, a historical-rule coverage proof, or B3"
        ),
        "max_side": args.max_side,
        "demands": [1, 2, 3],
        "capacities": [0, 1, 2, 3],
        "counts": counts,
        "first_locally_safe_globally_unsafe": witness,
        "explicit_controls": controls,
        "resource_ledger": {
            "elapsed_seconds": time.perf_counter() - started,
            "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "python": platform.python_version(),
        },
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["payload_sha256_before_self_hash"] = hashlib.sha256(canonical).hexdigest()
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": status, **counts, "output": args.output}, sort_keys=True))


if __name__ == "__main__":
    main()
