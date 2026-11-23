"""Exact Bellman audit of adaptive mask probes on independent fair bits."""
from fractions import Fraction
from functools import cache
from itertools import combinations_with_replacement, product
import json


@cache
def optimal(widths):
    if not widths:
        return Fraction(0)
    actions = []
    for i in range(len(widths)):
        rest = widths[:i] + widths[i+1:]
        on_one = optimal(rest)
        width = widths[i]
        on_zero = 0 if width == 1 else optimal(tuple(sorted(rest + (width-1,))))
        actions.append(1 + (on_zero + on_one) / 2)
    return min(actions)


def ordered_cost(widths):
    reach = Fraction(1)
    result = Fraction(0)
    for k in sorted(widths):
        reach *= 1 - Fraction(1, 2**k)
        result += 2 * reach
    return result


def main():
    profiles = 0
    for size in range(1, 13):
        for widths in combinations_with_replacement((1, 2, 3), size):
            assert optimal(widths) == ordered_cost(widths)
            profiles += 1
    # Interleaved round-robin first reads on unique-witness inputs.
    sparse = 0
    for size in range(1, 7):
        total = 0
        records = set()
        for positions in product(range(3), repeat=size):
            found = {}
            record = []
            for d in range(3):
                for i in range(size):
                    if i not in found:
                        bit = int(positions[i] == d)
                        record.append(bit)
                        if bit:
                            found[i] = d
            assert tuple(found[i] for i in range(size)) == positions
            records.add(tuple(record))
            total += len(record)
            sparse += 1
        assert len(records) == 3**size
        assert total == 2 * size * len(records)
    print(json.dumps(dict(bellman_profiles=profiles, sparse_instances=sparse,
                          full_width_12_fair_optimum=str(optimal((3,)*12)),
                          full_width_12_sparse_optimum=24,
                          full_width_12_worst_case=36), indent=2))


if __name__ == "__main__":
    main()
