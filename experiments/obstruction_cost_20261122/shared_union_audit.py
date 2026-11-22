#!/usr/bin/env python3
"""Finite, independent truth-table audit of the shared-core recurrence controls."""
import hashlib
import itertools
import json
from pathlib import Path


def minimal_cores(clauses, variable_count, pins=None):
    pins = pins or {}
    assignments = [a for a in itertools.product((0, 1), repeat=variable_count)
                   if all(a[v - 1] == value for v, value in pins.items())]
    cores = []
    for size in range(1, len(clauses) + 1):
        for selected in itertools.combinations(range(len(clauses)), size):
            chosen = frozenset(selected)
            if any(k <= chosen for k in cores):
                continue
            if not any(all(any(a[abs(lit) - 1] == int(lit > 0)
                               for lit in clauses[i]) for i in chosen)
                       for a in assignments):
                cores.append(chosen)
    return set(cores)


def sorted_sets(family):
    return [sorted(k) for k in sorted(family, key=lambda k: (len(k), sorted(k)))]


def audit(clauses, n, split):
    parent = minimal_cores(clauses, n)
    children = [minimal_cores(clauses, n, {split: value}) for value in (0, 1)]
    unions = {a | b for a in children[0] for b in children[1]}
    minimal_unions = {u for u in unions if not any(v < u for v in unions)}
    assert parent == minimal_unions
    mu = min(map(len, parent))
    child_mu = [min(map(len, c)) for c in children]
    child_minima = [{k for k in c if len(k) == minimum}
                    for c, minimum in zip(children, child_mu)]
    restricted_union = min(len(a | b) for a in child_minima[0] for b in child_minima[1])
    return {"clauses": clauses, "variables": n, "split_variable": split,
            "parent_minimal_cores": sorted_sets(parent),
            "slice_minimal_cores": [sorted_sets(c) for c in children],
            "minimum_parent_size": mu, "minimum_slice_sizes": child_mu,
            "minimum_union_using_only_slice_minimum_cores": restricted_union,
            "exact_family_identity": True}


def main():
    # Variable order x,y,z,u,v. All clauses have width at most two.
    control = [(1, 2), (1, -2), (-1, 3), (-1, -3), (4,), (5,), (-4, -5)]
    result = audit(control, 5, 1)
    assert result["minimum_parent_size"] == 3
    assert result["minimum_slice_sizes"] == [2, 2]
    assert result["minimum_union_using_only_slice_minimum_cores"] == 4
    f = [(-1, -2), (2, -3), (1, 3), (-1, 2, 3), (1, -2, -3)]
    g = [(1, 2), (1, -2), (-1, 2, 3), (-1, 2, -3), (-1, -2)]
    ff = audit(f, 3, 1)
    gg = audit(g, 3, 1)
    assert ff["minimum_parent_size"] == gg["minimum_parent_size"] == 5
    assert ff["minimum_slice_sizes"] == [3, 3]
    print(json.dumps({"status": "PASS", "mode": "complete finite truth tables",
                      "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      "minimum_children_fail_control": result,
                      "boolean_five_step_witness": ff,
                      "boolean_four_step_control": gg}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
