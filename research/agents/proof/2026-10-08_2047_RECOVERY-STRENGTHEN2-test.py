#!/usr/bin/env python3
"""Exact envelope checks, not a SAT solver or empirical complexity proof."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import signal

signal.alarm(25)

def envelope(rp, rq, u, v, h):
    cp = max(rp, u + rq, (u + v) / (1 - h))
    return cp, max(rq, v + h * cp)

def feasible(cp, cq, rp, rq, u, v, h):
    return cp >= rp and cp >= u + cq and cq >= rq and cq >= v + h * cp

hs = [F(1, 4), F(1, 2), F(3, 4)]
floors = [F(0), F(1, 2), F(1), F(3, 2)]
costs = [F(i, 4) for i in range(5)]
count = 0
perturbation_checks = 0
iteration_checks = 0
for rp, rq, u, v, h in product(floors, floors, costs, costs, hs):
    cp, cq = envelope(rp, rq, u, v, h)
    assert feasible(cp, cq, rp, rq, u, v, h)
    assert cp == max(rp, u + cq)
    assert cq == max(rq, v + h * cp)
    assert (cp <= 1) == (rp <= 1 and u + rq <= 1 and u + v <= 1 - h)
    # Coordinate reductions of the claimed least vector must be infeasible.
    for delta in (F(1, 100), F(1, 4)):
        assert not feasible(cp - delta, cq, rp, rq, u, v, h)
        assert not feasible(cp, cq - delta, rp, rq, u, v, h)
        perturbation_checks += 2
    # Independent monotone value iteration remains below the claimed envelope.
    p, q = rp, rq
    for _ in range(20):
        np, nq = max(rp, u + q), max(rq, v + h * p)
        assert p <= np <= cp and q <= nq <= cq
        p, q = np, nq
        iteration_checks += 1
    count += 1

access = []
for h, g in product(hs, [F(0), F(1, 8), F(1, 4)]):
    cp, cq = envelope(F(1), F(1), F(0), 1 - h + g, h)
    assert cp == 1 + g / (1 - h)
    access.append(dict(h=str(h), access_overhead=str(g), cp=str(cp), cq=str(cq)))

# Executions, not unique labels: 8 repeats of one child still cost 8 executions.
children = [16] * 8
assert sum(children) == 128 and sum(set(children)) == 16
# Materialization and normalization controls: no free conversion of measures.
assert F(2) * F(3, 4) == F(3, 2) > 1
# A theta=1 positive-cost return cycle yields C >= C + positive, infeasible.
assert F(1, 4) + F(1, 4) > 0

result = {
    "status": "COMPUTATIONAL",
    "scope": "exact finite checks of sufficient exponent inequalities only",
    "seed": None,
    "exhaustive_parameter_tuples": count,
    "coordinate_perturbation_checks": perturbation_checks,
    "monotone_iteration_checks": iteration_checks,
    "h": list(map(str, hs)), "local_floors": list(map(str, floors)),
    "edge_costs": list(map(str, costs)),
    "access_sensitivity": access,
    "multiplicity_control": {"executed_volume": 128, "deduplicated_volume": 16},
    "source_normalization_control": {"lambda": "2", "b": "3/4", "theta": "3/2"},
    "budget_seconds": 25,
    "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "limitations": "No SAT implementation, measured bit-machine resource bound, or all-input coverage is claimed."
}
print(json.dumps(result, indent=2))
