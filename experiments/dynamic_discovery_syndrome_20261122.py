"""Audit exact-one syndrome aggregation. Run from the repository root with Python 3."""
from itertools import product
from pathlib import Path
import json


def reachable(columns):
    states = {0}
    for start in range(0, len(columns), 3):
        states = {state ^ column for state in states
                  for column in columns[start:start + 3]}
    return states


def explicit(columns):
    return {columns[i] ^ columns[j] for i in range(3) for j in range(3, 6)}


def main():
    sat = 0
    hist = {}
    for columns in product(range(4), repeat=6):
        states = reachable(columns)
        assert states == explicit(columns)
        sat += int(0 in states)
        key = str(sorted(states))
        hist[key] = hist.get(key, 0) + 1
    chains = []
    for mask in range(512):
        bits = [(mask >> i) & 1 for i in range(9)]
        count = 0
        for aux in product(range(2), repeat=6):
            rows = [(bits[0], bits[1], aux[0])]
            rows += [(aux[i-1], bits[i+1], aux[i]) for i in range(1, 6)]
            rows += [(aux[5], bits[7], bits[8])]
            count += int(all(sum(row) % 2 == 0 for row in rows))
        assert count == int(sum(bits) % 2 == 0)
        chains.append(count)
    pair = []
    for last in (8, 9):
        support = set(range(8)) | {last}
        columns = [int(i in support) for i in range(12)]
        possible = reachable(columns)
        assert (0 in possible) == (last == 9)
        pair.append(dict(support=sorted(support), reachable=sorted(possible)))
    raw = dict(enumeration="all ordered six columns over GF(2)^2, two triples",
               total=4096, sat=sat, unsat=4096-sat, reachable_set_histogram=hist,
               chain_extensions_by_mask=chains, four_triple_pair=pair)
    path = Path("results/raw/dynamic_discovery_syndrome_20261122.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(raw, indent=2) + "\n")
    print(sat, 4096-sat, pair)


if __name__ == "__main__":
    main()
