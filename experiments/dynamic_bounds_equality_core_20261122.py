"""Audit equality cores with no grouped degree-two pivot."""
from itertools import combinations, product
import json


def rank(masks):
    pivots = {}
    for value in masks:
        while value:
            pivot = value.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = value
                break
            value ^= pivots[pivot]
    return len(pivots)


def audit(t, label):
    factors = [tuple(range(3*i, 3*i+3)) for i in range(t)]
    equations, joins = [], []
    names = 3*t
    for i, j in combinations(range(t), 2):
        for k in range(3):
            x, y = factors[i][k], factors[j][k]
            a, b = names, names+1
            names += 2
            equations.extend([(x,a,b), (y,a,b)])
            joins.append((x,y,a,b))
    extra = (factors[0][0], factors[1][1], factors[2][2 if not label else 0])
    equations.append(extra)
    group = {v:i for i,row in enumerate(factors) for v in row}
    for v in range(3*t, names):
        group[v] = t+v-3*t
    graph = {i:set() for i in set(group.values())}
    for row in equations:
        for x,y in combinations({group[v] for v in row},2):
            graph[x].add(y)
            graph[y].add(x)
    assert min(map(len, graph.values())) == 3
    seen = {0}
    for _ in graph:
        seen |= set().union(*(graph[v] for v in seen))
    assert len(seen) == len(graph)
    masks = [sum(1<<v for v in row) for row in equations]
    projected_codimension = rank(masks) - rank([v >> (3*t) for v in masks])
    assert projected_codimension == 3*t-2
    accepted = 0
    for choices in product(range(3), repeat=t):
        values = {v:int(k==choice) for row,choice in zip(factors,choices)
                  for k,v in enumerate(row)}
        if any(values[x] != values[y] for x,y,_,_ in joins):
            continue
        if sum(values[v] for v in extra)%2:
            continue
        for x,y,a,b in joins:
            values[a],values[b] = 0,values[x]
        assert all(sum(values[v] for v in row)%2==0 for row in equations)
        accepted += 1
    assert accepted == (2 if label else 0)
    return dict(t=t, label=label, names=names, clauses=5*t+4*len(equations),
                min_degree=3, projected_dimension=2, accepted_port_assignments=accepted)


if __name__ == '__main__':
    print(json.dumps([audit(t,label) for t in range(3,9) for label in (0,1)],indent=2))
