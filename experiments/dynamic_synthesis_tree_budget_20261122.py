"""Exhaustive local correlation-cover audit, not a full circular solver.

Enumerates all 16^3 binary table systems on the three pairs of one
exact-one triple, and all 3^2 partial pin patterns on its first two names.
The local exact-one feasibility oracle is exhaustive and deliberately tiny.
"""
import hashlib
import itertools
import json
from pathlib import Path

BITS = (0, 1)
PAIRS = ((0, 1), (0, 2), (1, 2))
TUPLES = tuple(itertools.product(BITS, repeat=2))
TABLES = tuple(frozenset(t for i, t in enumerate(TUPLES) if mask >> i & 1)
               for mask in range(16))
ASSIGNMENTS = tuple(itertools.product(BITS, repeat=3))


def direct(tables, pins):
    return any(sum(a) == 1 and all(a[x] == b for x, b in pins.items())
               and all((a[x], a[y]) in q for (x, y), q in zip(PAIRS, tables))
               for a in ASSIGNMENTS)


def covered(tables, pins):
    if any(not q for q in tables):
        return False
    domains = [set(BITS) for _ in range(3)]
    correlations = []
    for pair, q in zip(PAIRS, tables):
        left = {t[0] for t in q}
        right = {t[1] for t in q}
        if q == set(itertools.product(left, right)):
            domains[pair[0]] &= left
            domains[pair[1]] &= right
        else:
            correlations.append((pair, q))
    # Deterministic maximal matching; its endpoints form a vertex cover.
    cover = set()
    for (x, y), _ in correlations:
        if x not in cover and y not in cover:
            cover.update((x, y))
    assert all(x in cover or y in cover for (x, y), _ in correlations)
    names = sorted(cover)
    for values in itertools.product(BITS, repeat=len(names)):
        branch = [d.copy() for d in domains]
        for x, b in itertools.chain(zip(names, values), pins.items()):
            branch[x] &= {b}
        for (x, y), q in correlations:
            allowed = {(a, b) for a, b in q if a in branch[x] and b in branch[y]}
            branch[x] &= {a for a, _ in allowed}
            branch[y] &= {b for _, b in allowed}
        # All residual tables are products because an endpoint is fixed.
        if any(sum(a) == 1 and all(a[x] in branch[x] for x in range(3))
               for a in ASSIGNMENTS):
            return True
    return False


def main():
    checked = sat = 0
    for tables in itertools.product(TABLES, repeat=3):
        for values in itertools.product((None, 0, 1), repeat=2):
            pins = {x: b for x, b in enumerate(values) if b is not None}
            expected, actual = direct(tables, pins), covered(tables, pins)
            assert expected == actual, (tables, pins, expected, actual)
            checked += 1
            sat += expected
    result = {
        "status": "PASS", "checked": checked, "sat": sat,
        "unsat": checked - sat, "seed": None,
        "scope": "local binary-table reduction with exact-one oracle; no full tree or tape implementation",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
