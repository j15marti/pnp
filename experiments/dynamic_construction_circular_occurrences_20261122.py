"""Run with Python 3. Exact source tests for circular positive exact-one rows."""
from itertools import combinations, product
import json


def solve(rows):
    m = len(rows)
    names = sorted(set().union(*map(set, rows)))
    arcs = []
    for x in names:
        cells = {i for i, row in enumerate(rows) if x in row}
        if len(cells) == m:
            arcs.append((0, m))
            continue
        starts = [i for i in cells if (i-1) % m not in cells]
        if len(starts) != 1:
            return None
        arcs.append((starts[0], len(cells)))
    if (0, m) in arcs:
        return True
    for start, length in arcs:
        if (-start) % m >= length:
            continue
        origin = (start+length) % m
        gap = m-length
        reached = {0}
        for pos in range(gap):
            if pos in reached:
                for s, size in arcs:
                    if (s-origin) % m == pos and pos+size <= gap:
                        reached.add(pos+size)
        if gap in reached:
            return True
    return False


def family(q, switch):
    m = 3*q+1
    rows = [[] for _ in range(m)]
    for start in range(m):
        size = 3 + switch*((start == 0)-(start == 1))
        for i in range(size):
            rows[(start+i) % m].append(start)
    assert all(len(row) == 3 for row in rows)
    return rows


def oracle(rows):
    n = 1+max(max(row) for row in rows)
    masks = [sum(1 << x for x in row) for row in rows]
    return any(all((mask & a).bit_count() == 1 for mask in masks)
               for a in range(1 << n))


def main():
    counts = {"SAT": 0, "UNSAT": 0, "UNKNOWN": 0}
    for rows in product(combinations(range(5), 3), repeat=4):
        ans = solve(rows)
        if ans is None:
            counts["UNKNOWN"] += 1
        else:
            assert ans == oracle(rows)
            counts["SAT" if ans else "UNSAT"] += 1
    pairs = []
    for q in range(2, 11):
        labels = [solve(family(q, bit)) for bit in (0, 1)]
        assert labels == [False, True]
        if q <= 4:
            assert labels == [oracle(family(q, bit)) for bit in (0, 1)]
        pairs.append([q, labels])
    print(json.dumps(dict(counts=counts, pairs=pairs, seed=None,
                          scope="source decision and recognition only"), indent=2))


if __name__ == "__main__":
    main()
