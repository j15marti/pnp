"""Degree-constrained cubic bipartite SAT sources and an exact flow audit."""
from collections import deque
from itertools import product
import json

from dynamic_synthesis_local_projection_20261121 import project_decision, block_affine_filter
from dynamic_redteam_affine_pivot_20261121 import components
from dynamic_accounting_paid_backdoor_20261121 import find_hit, restrict


def supports(k):
    left = [(3*i+1, 3*i+2, 3*i+3) for i in range(k)]
    right = [tuple(3*((i-j) % k)+j+1 for j in range(3)) for i in range(k)]
    return left + right


def formula(groups, targets):
    return tuple(tuple(-var if bit else var for var, bit in zip(group, bits))
                 for group, target in zip(groups, targets)
                 for bits in product(range(2), repeat=3) if sum(bits) != target)


def flow_decision(k, targets):
    if sum(targets[:k]) != sum(targets[k:]):
        return False
    source, sink = 2*k, 2*k+1
    capacity = [{} for _ in range(2*k+2)]

    def arc(u, v, n):
        capacity[u][v] = n
        capacity[v][u] = 0

    for i in range(k):
        arc(source, i, targets[i])
        arc(k+i, sink, targets[k+i])
        for j in range(3):
            arc(i, k+(i+j) % k, 1)
    value = 0
    while True:
        parent = {source: None}
        queue = deque([source])
        while queue and sink not in parent:
            u = queue.popleft()
            for v, available in capacity[u].items():
                if available and v not in parent:
                    parent[v] = u
                    queue.append(v)
        if sink not in parent:
            return value == sum(targets[:k])
        v = sink
        while v != source:
            u = parent[v]
            capacity[u][v] -= 1
            capacity[v][u] += 1
            v = u
        value += 1


def audit():
    groups = supports(3)
    feasible = {tuple(sum(bits[v-1] for v in group) for group in groups)
                for bits in product(range(2), repeat=9)}
    for target in product((1, 2), repeat=6):
        assert flow_decision(3, target) == (target in feasible)
    local_checks = 0
    for demand in (1, 2):
        clauses = formula([(1,2,3)], [demand])
        for bits in product(range(2), repeat=3):
            assert all(any(bits[abs(v)-1] == (v>0) for v in row)
                       for row in clauses) == (sum(bits)==demand)
            local_checks += 1
    cases = []
    for k in (8, 9, 10):
        groups = supports(k)
        for sat in (True, False):
            left = [2]*3 + [1]*(k-3)
            right = left if sat else [1]*5 + [2]*3 + [1]*(k-8)
            targets = left + right
            rows = formula(groups, targets)
            assert flow_decision(k, targets) == sat
            assert project_decision(rows)[0] == "UNKNOWN"
            assert not block_affine_filter(rows)
            hit, stats = find_hit(rows, k-2)
            assert hit is None and stats["calls"] == (3**(k-1)-1)//2
            # Verify all edge restrictions retain one connected component.
            for v in range(1, 3*k+1):
                for bit in (0,1):
                    assert len(components(restrict(rows, {v:bit}))) == 1
            cases.append(dict(k=k,sat=sat,variables=3*k,clauses=len(rows),
                              calls=stats["calls"],side_total=sum(left),
                              rejected_candidates=3*k))
    return dict(cases=cases,degree_vectors_checked=64,assignments_checked=512,
                clause_truth_rows=local_checks,compiled_runs=0)


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
