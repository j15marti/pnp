"""Exhaustive pair-product fiber audit on Construction's Boolean encodings."""
from collections import Counter, defaultdict
from itertools import permutations, product
import json
import dynamic_construction_table_chain_20261121 as chain


def compose(outer, inner):
    return tuple(outer[x - 1] for x in inner)


def audit():
    compiler = chain.transport.load_generator()
    perms = tuple(permutations(range(1, 4)))
    groups = defaultdict(Counter)
    labels = Counter()
    for a, b, c, d in product(perms, repeat=4):
        tables = (a, b, c, d)
        bits = chain.image(compiler, tables, 1, 1)[0]
        folded = (compose(b, a), compose(d, c))
        path = chain.endpoint(tables, 1)
        sat = chain.endpoint(folded, 1)[-1] == 1
        assert chain.admit(compiler, bits) is sat
        assert sat == (path[-1] == 1)
        groups[folded][path[1], path[3]] += 1
        labels[sat] += 1
    assert len(groups) == 36
    assert all(set(g) == set(product(range(1, 4), repeat=2))
               and set(g.values()) == {4} for g in groups.values())
    return {"r": 3, "pairs": 2, "s": 1, "t": 1,
            "SAT": labels[True], "UNSAT": labels[False], "N": len(bits),
            "columns": ["first_pair_product", "second_pair_product",
                        "multiplicities_lexicographic_odd_vertex_pairs"],
            "rows": [[p, q, [g[k] for k in sorted(g)]]
                     for (p, q), g in sorted(groups.items())]}


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
