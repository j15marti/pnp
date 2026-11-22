"""New direct-sum and decoder-fiber audit. Python standard library only."""
from itertools import product
from math import log2
from pathlib import Path
import json


def binary_entropy(probability):
    if probability in (0, 1):
        return 0.0
    return -probability * log2(probability) - (1-probability) * log2(1-probability)


def main():
    evidence = []
    for blocks in range(1, 9):
        fibers = {0: [], 1: []}
        for choices in product((0, 1), repeat=blocks):
            # Disjoint nonzero parity rows have independent pivots.
            rows = [sum(1 << (12*j+i) for i in list(range(8)) + [8+bit])
                    for j, bit in enumerate(choices)]
            assert all(row != 0 for row in rows)
            assert all(rows[i] & rows[j] == 0
                       for i in range(blocks) for j in range(i))
            label = int(all(choices))
            # At normalized READY only the cached label remains.
            configuration = ("READY", 0, str(label))
            record = configuration[2]
            fibers[int(record)].append(choices)
        assert len(fibers[1]) == 1
        assert len(fibers[0]) == 2**blocks-1
        demand = binary_entropy(2**(-blocks))
        ambiguity = (1-2**(-blocks)) * log2(2**blocks-1)
        assert abs(blocks-demand-ambiguity) < 1e-12
        evidence.append(dict(blocks=blocks, p=12*blocks, s=11*blocks, k=blocks,
                             unsat_fiber_size=len(fibers[0]), sat_fiber_size=1,
                             decision_entropy=demand, residual_entropy=ambiguity,
                             collision=fibers[0][:2]))
    path = Path("results/raw/dynamic_bounds_direct_sum_20261122.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(evidence, indent=2) + "\n")
    print(json.dumps({"cases": sum(2**j for j in range(1,9)), "all_passed": True}))


if __name__ == "__main__":
    main()
