"""Check forest-normalized triangle bundles. Python 3, no dependencies or seed."""
import json
from collections import Counter
from itertools import combinations, permutations, product

P = list(permutations(range(3)))
odd = [sum(p[i] > p[j] for i, j in combinations(range(3), 2)) % 2 for p in P]
ok = [[[all(f[i] != g[p[i]] for i in range(3)) for g in P] for f in P] for p in P]


def witness_exists(n, edges, labels):
    # Direct test of all triangle edge inequalities, with global color symmetry.
    incoming = [[] for _ in range(n)]
    for (u, v), p in zip(edges, labels):
        incoming[v].append((u, p))
    choices = [0] * n
    def extend(v):
        if v == n:
            return True
        for g in range(6):
            if all(ok[p][choices[u]][g] for u, p in incoming[v]):
                choices[v] = g
                if extend(v + 1):
                    return True
        return False
    return extend(1)


def audit(n, edges, tree, clique):
    counts = Counter()
    chords = [e for e in edges if e not in tree]
    assert len(tree) == n-1
    for values in product(range(6), repeat=len(chords)):
        tags = dict(zip(chords, values))
        labels = [tags.get(e, 0) for e in edges]
        actual = witness_exists(n, edges, labels)
        # On normalized K4, the three star neighbors must avoid root color.
        # Independently enumerate their two possible cyclic shifts.
        predicted = not any(odd[p] for p in values)
        if predicted and clique:
            predicted = any(all((b[v-1]+P[tags[u,v]][0]-b[u-1]) % 3
                                for u, v in chords)
                            for b in product((1, 2), repeat=3))
        assert predicted == actual, (edges, values)
        counts["SAT" if actual else "UNSAT"] += 1
    return dict(counts)


if __name__ == "__main__":
    k4 = list(combinations(range(4), 2))
    bip = [(u,v) for u in range(3) for v in range(3,6)]
    prism = sorted([(0,1),(1,2),(0,2),(3,4),(4,5),(3,5),(0,3),(1,4),(2,5)])
    print(json.dumps({
        "K4": audit(4,k4,k4[:3],True),
        "K33": audit(6,bip,[(0,3),(0,4),(0,5),(1,3),(2,3)],False),
        "prism": audit(6,prism,[(0,1),(1,2),(0,3),(3,4),(4,5)],False)
    }, sort_keys=True))
