#!/usr/bin/env python3
"""Finite controls for LOCAL-PORT-HIERARCHY-REFEREE200.

The program checks the single-variable elimination identity, the ternary
majority witness, and exact bounded-fanin hierarchy node counts.  It does not
claim a lower bound for SAT algorithms or a native Turing-machine runtime.
"""

from __future__ import annotations

import itertools
import json
import math


def min_internal_nodes(leaves: int, fanin: int) -> int:
    assert leaves >= 1 and fanin >= 2
    return math.ceil((leaves - 1) / (fanin - 1))


def construct_level_counts(leaves: int, fanin: int) -> tuple[list[int], int]:
    levels = [leaves]
    internal = 0
    live = leaves
    while live > 1:
        parents = math.ceil(live / fanin)
        internal += parents
        levels.append(parents)
        live = parents
    return levels, internal


def elimination_identity(t: int) -> int:
    """Check all assignments after eliminating z from 2t width-3 clauses."""
    checked = 0
    for bits in itertools.product((False, True), repeat=4 * t):
        aa = [bits[4 * i] or bits[4 * i + 1] for i in range(t)]
        bb = [bits[4 * i + 2] or bits[4 * i + 3] for i in range(t)]
        left = any(
            all(z or a for a in aa) and all((not z) or b for b in bb)
            for z in (False, True)
        )
        resolvents = all(a or b for a in aa for b in bb)
        circuit = all(aa) or all(bb)
        assert left == resolvents == circuit
        checked += 1
    return checked


def ternary_clause(bits: tuple[int, int, int]) -> bool:
    a, b, c = bits
    return (not a) or (not b) or bool(c)


def majority(*rows: tuple[int, ...]) -> tuple[int, ...]:
    assert len(rows) == 3
    return tuple(int(sum(column) >= 2) for column in zip(*rows))


def main() -> None:
    witnesses = ((1, 0, 0), (0, 1, 0), (1, 1, 1))
    maj = majority(*witnesses)
    assert all(ternary_clause(x) for x in witnesses)
    assert maj == (1, 1, 0) and not ternary_clause(maj)

    elimination = {str(t): elimination_identity(t) for t in range(1, 5)}
    assert sum(elimination.values()) == 69904

    hierarchy = []
    for fanin in (2, 3, 4):
        for power in range(1, 21):
            leaves = 2**power
            levels, constructed = construct_level_counts(leaves, fanin)
            optimum = min_internal_nodes(leaves, fanin)
            # Level batching can be suboptimal for nonmatching powers, but it
            # must never beat the exact edge-count lower bound.
            assert constructed >= optimum
            if power in (4, 12, 20):
                hierarchy.append(
                    {
                        "fanin": fanin,
                        "leaves": leaves,
                        "edge_count_lower_bound": optimum,
                        "level_batch_internal": constructed,
                        "levels": levels,
                    }
                )

    growth = []
    for power in (6, 10, 14, 18, 22, 26, 30):
        m = 2**power
        canonical_n = m * math.ceil(math.log2(m + 2))
        for lam in (0.75, 0.9, 0.99):
            growth.append(
                {
                    "m": m,
                    "lambda": lam,
                    "m_over_N_to_lambda": m / (canonical_n**lam),
                }
            )

    result = {
        "status": "PASS",
        "elimination_assignment_checks": elimination,
        "elimination_assignment_checks_total": sum(elimination.values()),
        "compact_projection_circuit_gates": {
            str(t): 4 * t - 1 for t in (1, 2, 3, 4, 8, 16, 32)
        },
        "ternary_clause_majority_control": {
            "members": witnesses,
            "majority": maj,
            "majority_is_member": ternary_clause(maj),
        },
        "hierarchy_controls": hierarchy,
        "linear_floor_ratios": growth,
        "limitations": [
            "Hierarchy counts apply only when every leaf and merge gadget is physically retained.",
            "A recognizable easy grammar may compute and emit only its constant root summary.",
            "Discarding arbitrary subinstances requires exact summary acquisition and is the open step.",
            "Finite ratios and truth tables are not SAT runtime lower bounds.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
