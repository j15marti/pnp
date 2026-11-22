"""Source-level circular order discovery audit.

Run with python experiments/dynamic_discovery_circular_order_20261122.py pq_trees.py
using Sage's src/sage/graphs/pq_trees.py from 1638968e5a546cd04370505d40fd87a80a952e78.
"""
import hashlib
import json
import sys
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path

from dynamic_construction_circular_occurrences_20261122 import family, oracle, solve


def load_reorder(path):
    data = Path(path).read_bytes()
    header = f"blob {len(data)}\0".encode()
    assert hashlib.sha1(header + data).hexdigest() == "92d0f7966ba88b85a38bbd8e30d55e761916a34c"
    # All leaves passed here are frozensets. The list conversion is never used.
    source = data.decode().replace("from sage.sets.set import Set", "Set = frozenset")
    namespace = {}
    exec(compile(source, str(path), "exec"), namespace)
    return namespace["reorder_sets"]


def recover(rows, reorder):
    unique = list(dict.fromkeys(map(frozenset, rows)))
    pivot = unique[0]
    by_leaf = {row ^ pivot: row for row in unique[1:]}
    try:
        leaves = reorder(list(by_leaf))
    except ValueError as exc:
        if str(exc) != "Impossible":
            raise
        return None
    assert len(leaves) == len(by_leaf) and set(leaves) == set(by_leaf)
    ordered = [pivot] + [by_leaf[leaf] for leaf in leaves]
    decision = solve(ordered)
    assert decision is not None
    return decision


def main():
    reorder = load_reorder(sys.argv[1])
    counts = Counter()
    for rows in combinations(combinations(range(5), 3), 5):
        result = recover(rows, reorder)
        exists = any(solve((rows[0],) + tail) is not None for tail in permutations(rows[1:]))
        assert (result is not None) == exists
        if exists:
            assert result == oracle(rows)
        counts[str(result)] += 1
    pairs = []
    for q in range(2, 9):
        for switch in (0, 1):
            rows = family(q, switch)
            shuffled = rows[::2] + rows[1::2]
            assert solve(shuffled) is None
            assert recover(shuffled + shuffled, reorder) == bool(switch)
            pairs.append([q, switch])
    latin = [(i, 3+j, 6+(i+j)%3) for i in range(3) for j in range(3)]
    fano = [tuple((i+d)%7 for d in (0,1,3)) for i in range(7)]
    for rows, answer in ((latin, True), (fano, False)):
        assert recover(rows, reorder) is None and oracle(rows) == answer
    print(json.dumps(dict(five_distinct_rows=dict(counts), scrambled_pairs=pairs,
                          latin="UNKNOWN / SAT", fano="UNKNOWN / UNSAT",
                          scope="source-level recognition and decision", seed=None), indent=2))


if __name__ == "__main__":
    main()
