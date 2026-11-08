#!/usr/bin/env python3
"""Finite controls for the LSPV-5/424 positive-weight node bridge.

This checks the elementary accounting lemma and explicit countermodels.  It
does not replay Pang's asymptotic lower bound and is not an authoritative
R_mix341 parser/checker execution.
"""

from __future__ import annotations

from itertools import product
import json


def strict3(n: int, clauses: list[tuple[int, ...]]) -> bool:
    return (
        isinstance(n, int)
        and n >= 0
        and all(
            len(c) == 3
            and all(isinstance(x, int) and not isinstance(x, bool) and 0 < abs(x) <= n for x in c)
            and len({abs(x) for x in c}) == 3
            for c in clauses
        )
    )


def model_count(n: int, clauses: list[tuple[int, ...]]) -> int:
    total = 0
    for assignment in product((False, True), repeat=n):
        if all(any(assignment[abs(lit) - 1] == (lit > 0) for lit in clause) for clause in clauses):
            total += 1
    return total


def paid_union(nodes: list[dict]) -> int:
    """Charge each distinct derived node ID once; source axioms are free."""
    paid = {}
    for node in nodes:
        if node["kind"] == "derived":
            prior = paid.setdefault(node["id"], node["weight"])
            assert prior == node["weight"]
    return sum(paid.values())


def main() -> None:
    checks = 0

    # Exhaustive cardinality/weight form of the bridge.  S counts all distinct
    # proof-DAG nodes, at most m of which are free source axioms.
    for m in range(0, 33):
        for source_nodes in range(0, m + 1):
            for q in range(0, 65):
                s = source_nodes + q
                for alpha in range(1, 9):
                    weight = alpha * q
                    assert q >= max(0, s - m)
                    assert weight >= alpha * max(0, s - m)
                    checks += 2

    # Shared DAG: g1/g2 are reused by both branches and charged once.  AND
    # discharges both branches; OR selects one complete alternative.
    common = [
        {"id": "g1", "kind": "derived", "weight": 1},
        {"id": "g2", "kind": "derived", "weight": 1},
    ]
    left = common + [{"id": "l", "kind": "derived", "weight": 1}]
    right = common + [{"id": "r", "kind": "derived", "weight": 1}]
    and_union = left + right
    assert paid_union(left) == 3
    assert paid_union(right) == 3
    assert paid_union(and_union) == 4
    assert min(paid_union(left), paid_union(right)) == 3
    checks += 4

    # Context labels prevent cross-branch leakage.  A branch-local conclusion
    # cannot be reused in the incompatible branch without discharge.
    contexts = {"g1": frozenset(), "g2": frozenset(), "l": frozenset({"x"}), "r": frozenset({"not-x"})}
    assert contexts["g1"] <= contexts["l"] and contexts["g1"] <= contexts["r"]
    assert not contexts["l"] <= contexts["r"]
    assert not contexts["r"] <= contexts["l"]
    checks += 4

    # Countermodel 1: if zero-weight derived nodes are permitted, arbitrarily
    # large node count gives no positive lower bound on weighted work.
    zero_nodes = [{"id": f"z{i}", "kind": "derived", "weight": 0} for i in range(1000)]
    assert paid_union(zero_nodes) == 0
    checks += 1

    # Countermodel 2: a new unit-cost batch node may represent arbitrarily many
    # virtual Pang steps.  This is a calculus change, not a simulation theorem.
    virtual_steps = 1_000_000
    batch_nodes = [{"id": "batch", "kind": "derived", "weight": 1, "virtual_steps": virtual_steps}]
    assert paid_union(batch_nodes) == 1 and batch_nodes[0]["virtual_steps"] == virtual_steps
    checks += 1

    # The Pang family has m=8n source clauses.  Subtracting this linear source
    # allowance preserves any exponential all-node lower bound.
    asymptotic_rows = []
    for n in range(32, 513, 32):
        s_lower = 1 << (n // 8)
        q_lower = max(0, s_lower - 8 * n)
        if n >= 128:
            assert q_lower > 0
            checks += 1
        asymptotic_rows.append({"n": n, "source_bound": 8 * n, "sample_S": s_lower, "derived_lower": q_lower})

    # SAT/UNSAT and malformed strict-3-CNF controls remain separate from proof
    # size.  The full cube forbids all eight assignments.
    cube = [tuple(v if (mask >> (v - 1)) & 1 else -v for v in (1, 2, 3)) for mask in range(8)]
    assert strict3(3, cube) and model_count(3, cube) == 0
    assert strict3(3, cube[:-1]) and model_count(3, cube[:-1]) == 1
    assert model_count(3, []) == 8
    checks += 5
    malformed = [
        [(1, 1, 2)],
        [(1, 2, 0)],
        [(1, 2, 4)],
        [(1, 2)],
        [(1, 2, 3, 4)],
        [(True, 2, 3)],
    ]
    for bad in malformed:
        assert not strict3(3, bad)
        checks += 1

    out = {
        "status": "FINITE ACCOUNTING CONTROLS; no Pang theorem or authoritative R_mix341 checker replay",
        "checks": checks,
        "bridge": "if S counts all distinct nodes, <=m are free sources, and every derived node has weight >= alpha>0, then W>=alpha*max(0,S-m)",
        "unit_weight_specialization": "W=q>=max(0,S-m); if S counts derived nodes then W=S",
        "branching": {"left": 3, "right": 3, "and_union": 4, "or_choice": 3, "shared_nodes_charged_once": 2},
        "context_leak_rejected": True,
        "countermodels": {"zero_weight_nodes": len(zero_nodes), "zero_weight_cost": 0, "batch_virtual_steps": virtual_steps, "batch_cost": 1},
        "asymptotic_rows": asymptotic_rows,
        "sat_unsat_controls": {"full_cube_models": 0, "seven_cube_models": 1, "empty_models": 8},
        "malformed_rejections": len(malformed),
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
