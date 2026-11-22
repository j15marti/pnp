"""Diamond networks: spanning-forest decision against terminal enumeration."""
from itertools import combinations, permutations, product
from collections import Counter
import json
from dynamic_construction_triangle_bundle_20261122 import expand
from dynamic_construction_join_palette_20261122 import encode, recover

G = tuple(permutations(range(3)))
I = (0, 1, 2)


def mul(a, b):
    return tuple(a[b[i]] for i in range(3))


def inv(a):
    return tuple(a.index(i) for i in range(3))


def decide(q, labels):
    adjacency = [[] for _ in range(q)]
    for (u, v), p in labels.items():
        adjacency[u].append((v, p))
        adjacency[v].append((u, inv(p)))
    potential = {}
    for root in range(q):
        if root in potential:
            continue
        potential[root] = I
        todo = [root]
        while todo:
            u = todo.pop()
            for v, p in adjacency[u]:
                expected = mul(potential[u], p)
                if v in potential:
                    if potential[v] != expected:
                        return False
                else:
                    potential[v] = expected
                    todo.append(v)
    return True


def oracle(q, labels):
    for rest in product(G, repeat=q-1):
        maps = (I,) + rest
        if all(all(maps[v][a] == maps[u][p[a]] for a in range(3))
               for (u, v), p in labels.items()):
            return True
    return False


def source(q, labels):
    matching = {}
    for j, ((u, v), p) in enumerate(sorted(labels.items())):
        a, b = q+2*j, q+2*j+1
        matching.update({(u,a):I, (u,b):I, (a,b):I, (v,a):p, (v,b):p})
    h, edges = expand(q+2*len(labels), matching)
    n, rows = encode(h, edges)
    assert n == 33*q+111*len(labels)
    assert len(rows) == 21*q+87*len(labels)
    assert recover(n, [row[::-1] for row in rows[::-1]]) == (h, edges)
    return n, len(rows)


def main():
    outcomes = Counter()
    cases = []
    # Exhaust every absent/label choice on three vertices.
    # Four vertices use two noncommuting transpositions plus absent edges.
    for q, options in ((3, (None,)+G), (4, (None,(1,0,2),(0,2,1)))):
        pairs = tuple(combinations(range(q), 2))
        count = 0
        for choices in product(options, repeat=len(pairs)):
            labels = {e:p for e,p in zip(pairs,choices) if p is not None}
            answer = decide(q, labels)
            assert answer == oracle(q, labels)
            source(q, labels)
            outcomes[str(answer)] += 1
            count += 1
        cases.append(dict(q=q, cases=count))
    # Every tree label is consistent, including reversed traversal of 3-cycles.
    for p in G:
        assert decide(4, {(0,2):p, (1,2):(1,2,0), (1,3):(0,2,1)})
    # An even but nonidentity triangle gain must reject.
    assert not decide(3, {(0,1):I, (1,2):I, (0,2):(1,2,0)})
    print(json.dumps(dict(cases=cases, outcomes=outcomes,
                          encoded_roundtrips=sum(x["cases"] for x in cases),
                          reverse_edge_tree_controls=6,
                          even_nonidentity_cycle_rejected=True), indent=2))


if __name__ == "__main__":
    main()
