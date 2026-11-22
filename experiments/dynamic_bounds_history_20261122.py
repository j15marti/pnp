"""Audit accumulated-history versus restricted-view entropy on Latin-chain scans."""
from collections import Counter, defaultdict
from itertools import product
from math import log2, isclose
import json

def entropy(values):
    n = len(values)
    return -sum(c/n * log2(c/n) for c in Counter(values).values())

def conditional(values, views):
    groups = defaultdict(list)
    for value, view in zip(values, views):
        groups[view].append(value)
    return sum(len(g)/len(values)*entropy(g) for g in groups.values())

def audit(q):
    inputs = list(product((0, 1), repeat=q))
    profiles = [tuple(min(2, sum(x[:j])) for j in range(1, q+1)) for x in inputs]
    innovation = marginal = lost = 0.0
    for j in range(q):
        u = [p[j] for p in profiles]
        history = [x[:j] for x in inputs]
        retained = [min(2, sum(x[:j])) for x in inputs]
        for x, p in zip(inputs, profiles):
            assert p[j] == min(2, min(2, sum(x[:j])) + x[j])
        fresh = conditional(u, history)
        assert isclose(conditional(u, retained), fresh, abs_tol=1e-12)
        innovation += fresh
        marginal += entropy(u)
        lost += entropy(u) - fresh
    assert isclose(innovation, entropy(profiles), abs_tol=1e-12)
    assert innovation <= q + 1e-12
    assert isclose(marginal, innovation + lost, abs_tol=1e-12)
    return dict(q=q, inputs=len(inputs), innovation=innovation,
                restricted_view_demand=marginal, omitted_information=lost,
                prefix_record_reuse=q, retained_counter_reuse=1)

rows = [audit(q) for q in range(1, 9)]
print(json.dumps(dict(status="PASS", total_inputs=sum(r["inputs"] for r in rows),
                      rows=rows, scope="finite entropy and event-set checks; no native tape simulation"),
                 indent=2))
