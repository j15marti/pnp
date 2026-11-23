"""Check the Z3 sign convention and all normalized gains on a square joined to a hexagon."""
from itertools import permutations, product
import json

from dynamic_construction_triangle_bundle_20261122 import expand, oracle
from dynamic_construction_join_palette_20261122 import encode, recover


def affine(slope, offset):
    return tuple((slope * i + offset) % 3 for i in range(3))


def test_edges():
    cases = 0
    for p in permutations(range(3)):
        a = (p[1] - p[0]) % 3
        for b, x, y in product((1, 2), range(3), range(3)):
            c = b * a % 3
            u, v = affine(b, x), affine(c, y)
            actual = all(u[i] != v[p[i]] for i in range(3))
            assert actual == ((x - y) % 3 != c * p[0] % 3)
            cases += 1
    return cases


def main():
    # Cycles 0-1-2-3-0 and 0-1-4-5-6-7-0 share only edge 01.
    tree = [(0,1),(1,2),(2,3),(1,4),(4,5),(5,6),(6,7)]
    chords = [(0,3),(0,7)]
    tests = 0
    for gains in product(range(3), repeat=2):
        offsets = dict.fromkeys(tree, 0)
        offsets.update(zip(chords, gains))
        for slopes in ((1,)*8, (1,2,1,2,2,1,1,2)):
            match = {(u,v): affine(slopes[u]*slopes[v], slopes[v]*g)
                     for (u,v),g in offsets.items()}
            h, edges = expand(8, match)
            n, rows = encode(h, edges)
            assert recover(n, rows[::-1]) == (h, edges)
            assert oracle(8, match)
            tests += 1
    print(json.dumps(dict(local_cases=test_edges(), square_hexagon_sources=tests,
                          normalized_gains=9, sat=tests), sort_keys=True))


if __name__ == "__main__":
    main()
