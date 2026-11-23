"""Exhaustive finite audit of rooted F3 switching on K4 plus an isolate."""
from collections import Counter
from itertools import combinations, product
import json


def main():
    edges = list(combinations(range(4), 2))
    tree = {(0, 1), (0, 2), (0, 3)}
    chords = [edge for edge in edges if edge not in tree]
    fibers = Counter()
    comparisons = 0
    sat = 0
    for values in product(range(3), repeat=len(edges)):
        gains = dict(zip(edges, values))
        # Root 0 and isolated root 4 have potential zero.
        potential = [0] + [(-gains[0, v]) % 3 for v in range(1, 4)] + [0]
        normalized = {edge: (gains[edge] - potential[edge[0]]
                            + potential[edge[1]]) % 3 for edge in edges}
        assert all(normalized[edge] == 0 for edge in tree)
        record = tuple(normalized[edge] for edge in chords)
        fibers[record] += 1
        bits = ''.join(format(trit, '02b') for trit in record)
        decoded = tuple(int(bits[i:i+2], 2) for i in range(0, len(bits), 2))
        assert decoded == record
        # Anchoring the isolate is sufficient, as it has no incident edge.
        satisfiable = False
        for assignment in product(range(3), repeat=4):
            shifted = [(assignment[v] - potential[v]) % 3 for v in range(4)]
            before = all((assignment[u] - assignment[v]) % 3 != gains[u, v]
                         for u, v in edges)
            after = all((shifted[u] - shifted[v]) % 3 != normalized[u, v]
                        for u, v in edges)
            assert before == after
            satisfiable |= before
            comparisons += 1
        sat += satisfiable
    assert len(fibers) == 27
    assert set(fibers.values()) == {27}
    print(json.dumps(dict(gain_vectors=729, normalized_vectors=len(fibers),
                         fiber_size=27, assignment_checks=comparisons,
                         sat=sat, unsat=729-sat, record_bits=6,
                         q=5, k=6, components=2, cycle_rank=3), sort_keys=True))


if __name__ == '__main__':
    main()
