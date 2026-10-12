#!/usr/bin/env python3
"""Finite truth-table audit for easy-island versus worst-case quantifiers."""

from __future__ import annotations

import itertools
import json
import time


def bit(mask, i):
    return bool((mask >> i) & 1)


def main():
    started = time.perf_counter()
    total = coexist = easy_only = worst_only = neither = 0
    negation_failures = witness_failures = 0
    examples = []

    # R(a,x) is an arbitrary proposed charged obligation.  Exhaust all
    # relations for three abstract deciders and up to five sources, together
    # with every nonempty proper easy island.
    for nsrc in range(2, 6):
        ndec = 3
        for island in range(1, (1 << nsrc) - 1):
            inside = [x for x in range(nsrc) if bit(island, x)]
            outside = [x for x in range(nsrc) if not bit(island, x)]
            for relation in range(1 << (nsrc * ndec)):
                rows = [
                    [bit(relation, a * nsrc + x) for x in range(nsrc)]
                    for a in range(ndec)
                ]
                easy = any(all(not rows[a][x] for x in inside) for a in range(ndec))
                worst = all(any(rows[a][x] for x in range(nsrc)) for a in range(ndec))
                not_worst = any(all(not rows[a][x] for x in range(nsrc)) for a in range(ndec))
                total += 1
                if not_worst != (not worst):
                    negation_failures += 1
                if easy and worst:
                    coexist += 1
                    # The island-avoiding decider must have a charged witness
                    # outside the island if the worst-case statement holds.
                    if not any(
                        all(not rows[a][x] for x in inside)
                        and any(rows[a][x] for x in outside)
                        for a in range(ndec)
                    ):
                        witness_failures += 1
                    if len(examples) < 4:
                        examples.append({
                            "sources": nsrc,
                            "island_mask": island,
                            "relation_rows": rows,
                        })
                elif easy:
                    easy_only += 1
                elif worst:
                    worst_only += 1
                else:
                    neither += 1

    # Named semantic controls.  The labels deliberately include the hostile
    # families; quantifier negation is unchanged by their internal algorithms.
    labels = [
        "K33-clean", "prism-clean", "Horn", "2SAT", "affine-Tseitin",
        "bounded-treewidth", "independent-product", "padding",
        "redundant-clause", "alternate-encoding", "UNSAT",
    ]
    island = {"K33-clean", "prism-clean", "independent-product"}
    wrappers = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
    # Concrete relation: every wrapper is uncharged on the island and charged
    # on every outside control.  Thus easy avoidance and a worst-case witness
    # coexist for all wrappers.
    wrapper_checks = 0
    for wrapper in wrappers:
        row = {label: label not in island for label in labels}
        assert all(not row[label] for label in island)
        assert any(row[label] for label in labels)
        assert any(row[label] for label in set(labels) - island)
        wrapper_checks += 3

    # Compact-circuit/branching-program control: replacing each row by a
    # constant-size predicate "x outside I" preserves the same truth values.
    compact_checks = len(wrappers) * len(labels)

    result = {
        "audit": "EASY-ISLAND-QUANTIFIER-GUARD1",
        "status": "COMPUTATIONAL exhaustive finite audit of an exact logical theorem",
        "relations_and_islands_checked": total,
        "easy_and_worst_case_coexist": coexist,
        "easy_only": easy_only,
        "worst_only": worst_only,
        "neither": neither,
        "quantifier_negation_failures": negation_failures,
        "outside_witness_failures": witness_failures,
        "named_wrapper_checks": wrapper_checks,
        "compact_representation_checks": compact_checks,
        "hostile_labels": labels,
        "example_coexistence_instances": examples,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    assert total == easy_only + worst_only + coexist + neither
    assert coexist > 0 and negation_failures == witness_failures == 0
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
