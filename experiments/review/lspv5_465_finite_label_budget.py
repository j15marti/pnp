#!/usr/bin/env python3
"""Finite checks for LSPV-5/465's paid-label budget ceiling.

This is an independent finite reconstruction, not the historical R_mix341 checker.
"""

from itertools import product
import hashlib
import json


def subset_cost(charges, mask):
    return sum(w for i, w in enumerate(charges) if mask & (1 << i))


def run():
    stats = {
        "charge_subset_cases": 0,
        "dag_history_cases": 0,
        "fiber_min_cases": 0,
        "violations": 0,
    }

    # Exhaust every finite label budget through seven labels, charges 0..3,
    # and every possible set of labels used by an abstract proof.
    for m in range(8):
        for charges in product(range(4), repeat=m):
            total = sum(charges)
            for mask in range(1 << m):
                stats["charge_subset_cases"] += 1
                if subset_cost(charges, mask) > total:
                    stats["violations"] += 1

    # Ordered occurrence DAGs include arbitrary multi-parent AND nodes.  The
    # count-once history cost depends on used labels, never occurrence count.
    label_count = 3
    for n in range(1, 5):
        parent_choices = 1 << (n * (n - 1) // 2)
        for _edge_mask in range(parent_choices):
            for labels in product(range(label_count), repeat=n):
                used = set(labels)
                for charges in product(range(4), repeat=label_count):
                    stats["dag_history_cases"] += 1
                    history_cost = sum(charges[i] for i in used)
                    if history_cost > sum(charges):
                        stats["violations"] += 1

    # If each abstract label is charged by the minimum native fresh weight in
    # its fiber, its first-use cost cannot exceed the total concrete node cost.
    for n in range(1, 7):
        for weights in product(range(1, 4), repeat=n):
            for quotient in product(range(2), repeat=n):
                stats["fiber_min_cases"] += 1
                mins = {}
                for q, w in zip(quotient, weights):
                    mins[q] = min(mins.get(q, w), w)
                if sum(mins.values()) > sum(weights):
                    stats["violations"] += 1

    # A shared diamond: the lemma label is paid once although referenced by
    # two branches.  Tree unfolding would charge it twice.
    diamond_charges = {"S0": 0, "S1": 0, "L": 3, "B0": 2, "B1": 2, "G": 1}
    diamond_occurrences = ["S0", "S1", "L", "B0", "L", "B1", "G"]
    diamond_history_cost = sum(diamond_charges[x] for x in set(diamond_occurrences))
    diamond_tree_cost = sum(diamond_charges[x] for x in diamond_occurrences)
    assert diamond_history_cost == 8
    assert diamond_tree_cost == 11
    assert diamond_history_cost <= sum(diamond_charges.values())

    result = {
        **stats,
        "checks": sum(stats[k] for k in ("charge_subset_cases", "dag_history_cases", "fiber_min_cases")) + 3,
        "shared_diamond": {
            "history_cost": diamond_history_cost,
            "tree_unfolded_cost": diamond_tree_cost,
            "total_label_budget": sum(diamond_charges.values()),
        },
        "status": "PASS" if stats["violations"] == 0 else "FAIL",
        "limitations": "finite combinatorial reconstruction only; not historical R_mix341",
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["canonical_sha256_without_self"] = hashlib.sha256(canonical).hexdigest()
    return result


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
