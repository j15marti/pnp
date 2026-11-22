"""Run with Python 3. Integers are zero-based in memory."""
from collections import Counter
from itertools import combinations, product
import json
import random


def encode(h, edges):
    rows = []
    for i in range(2*h):
        rows.extend([(3*i, 3*i+1, 3*i+2),
                     (3*i+2, 3*((i+1) % (2*h)), 6*h+i)])
    for j, (u, v) in enumerate(sorted(edges)):
        rows.extend((6*u+c, 6*v+c, 8*h+3*j+c) for c in range(3))
    return 8*h+3*len(edges), rows


def recover(n, rows):
    m = len(rows)
    h, rem = divmod(n-m, 4)
    if rem or h < 3 or 4*h > m:
        return None
    if any(len(row) != 3 or len(set(row)) != 3 or
           any(x < 0 or x >= n for x in row) for row in rows):
        return None
    counts = Counter(tuple(sorted(row)) for row in rows)
    for row in encode(h, [])[1]:
        key = tuple(sorted(row))
        if counts[key] != 1:
            return None
        del counts[key]
    private, triples = set(), set()
    for (x, y, z), mult in counts.items():
        u, c = divmod(x, 6)
        v, d = divmod(y, 6)
        if (mult != 1 or not (u < v < h and c == d < 3) or
                z < 8*h or z in private or (u,v,c) in triples):
            return None
        private.add(z)
        triples.add((u,v,c))
    edges = {(u,v) for u,v,c in triples}
    if len(triples) != 3*len(edges):
        return None
    return h, edges


def join_verdict(h, edges):
    graph = [set() for _ in range(h)]
    for u,v in edges:
        graph[u].add(v)
        graph[v].add(u)
    unseen = set(range(h))
    demand = 0
    parts = 0
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        queue, part = [start], {start}
        while queue:
            children = unseen - graph[queue.pop()]
            part.update(children)
            unseen.difference_update(children)
            queue.extend(children)
        parts += 1
        if len(part) == h:
            return None
        colors = {}
        need = 1
        for start in sorted(part):
            if start in colors:
                continue
            queue = [start]
            colors[start] = 0
            while queue:
                x = queue.pop()
                for y in graph[x] & part:
                    need = max(need, 2)
                    if y not in colors:
                        colors[y] = 1-colors[x]
                        queue.append(y)
                    elif colors[y] == colors[x]:
                        need = 3
        demand += need
    return demand <= 3


def family(q, odd):
    rim = 2*q
    edges = {tuple(sorted((i,(i+1) % rim))) for i in range(rim)}
    edges.add((0,2 if odd else 3))
    edges.update((i,j) for i in range(rim) for j in range(rim,3*q))
    return 3*q, edges


def main():
    rng = random.Random(324)
    ans = Counter()
    for h in (3,4,5):
        pairs = list(combinations(range(h), 2))
        for mask in range(1 << len(pairs)):
            edges = {p for i,p in enumerate(pairs) if mask >> i & 1}
            n, rows = encode(h, edges)
            rows = [tuple(rng.sample(r,3)) for r in rows]
            rng.shuffle(rows)
            assert recover(n,rows) == (h,edges)
            value = join_verdict(h,edges)
            ans[str(value)] += 1
            if value is not None:
                assert value == any(all(a[u] != a[v] for u,v in edges)
                                    for a in product(range(3),repeat=h))
    for q in range(3,15):
        for odd in (False, True):
            h, edges = family(q,odd)
            n, rows = encode(h,edges)
            assert recover(n,rows) == (h,edges)
            assert join_verdict(h,edges) == (not odd)
            # Duplicate the other color while keeping the same dimensions.
            rows[-1] = rows[-2]
            assert recover(n,rows) is None
    print(json.dumps(dict(small_graphs=dict(ans), family_cases=24,
                          malformed_cases=24, seed=324),sort_keys=True))


if __name__ == "__main__":
    main()
