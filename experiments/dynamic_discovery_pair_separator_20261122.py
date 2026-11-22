"""Deterministic source audit for circular roots with binary child messages."""
from itertools import combinations, product
import json


def encode(n, edges):
    root = []
    for i in range(2*n):
        left, middle, right = range(3*i, 3*i+3)
        root.extend([(left, middle, right),
                     (right, 3*((i+1) % (2*n)), 6*n+i)])
    leaves = [(6*u+c, 6*v+c, 8*n+3*j+c)
              for j, (u, v) in enumerate(edges) for c in range(3)]
    return root, leaves


def exact(rows, pins=None):
    # Independent propagation and exhaustive branching on the emitted triples.
    env = dict(pins or {})
    while True:
        before = len(env)
        for row in rows:
            ones = sum(env.get(x, 0) for x in row)
            free = [x for x in row if x not in env]
            if ones > 1 or (not ones and not free):
                return False
            if ones:
                env.update((x, 0) for x in free)
            elif len(free) == 1:
                env[free[0]] = 1
        if len(env) == before:
            break
    unknown = [x for row in rows for x in row if x not in env]
    if not unknown:
        return True
    x = unknown[0]
    return any(exact(rows, dict(env) | {x: value}) for value in (0, 1))


def check_shape(root, leaves):
    names = set().union(*map(set, root))
    neighbors = {x: set() for x in names}
    for row in root:
        for x in row:
            neighbors[x].update(set(row)-{x})
    for x in names:
        flags = [x in r for r in root]
        assert sum(bit and not flags[i-1] for i, bit in enumerate(flags)) == 1
        todo = [next(iter(names-{x}))]
        seen = {x}
        while todo:
            vertex = todo.pop()
            if vertex not in seen:
                seen.add(vertex)
                todo.extend(neighbors[vertex]-seen)
        assert seen == names
    assert len({r[2] for r in leaves}) == len(leaves)
    assert all(set(r) & names == set(r[:2]) and r[0] != r[1] for r in leaves)


def audit():
    counts = []
    for n in range(3, 6):
        pairs = list(combinations(range(n), 2))
        sat = 0
        for mask in range(1 << len(pairs)):
            edges = [p for i, p in enumerate(pairs) if mask >> i & 1]
            root, leaves = encode(n, edges)
            check_shape(root, leaves)
            expected = any(all(c[u] != c[v] for u, v in edges)
                           for c in product(range(3), repeat=n))
            assert exact(root + leaves) == expected
            sat += expected
        counts.append(dict(vertices=n, graphs=1 << len(pairs), sat=sat))
    return counts


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
