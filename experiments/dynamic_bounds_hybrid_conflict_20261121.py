"""Finite graph audit for DYNAMIC-HYBRID-CONFLICT-CODE1. Python 3, no dependencies."""
from itertools import combinations, product
from collections import Counter
import json

def main():
    graphs = colorings = 0
    for n in range(1, 5):
        pairs = list(combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            edges = [e for j,e in enumerate(pairs) if mask >> j & 1]
            alpha = max(sum(bits) for bits in product((0,1), repeat=n)
                        if all(not(bits[u] and bits[v]) for u,v in edges))
            graphs += 1
            for colors in product(range(n), repeat=n):
                if any(colors[u] == colors[v] for u,v in edges):
                    continue
                counts = Counter(colors)
                assert max(counts.values()) <= alpha
                # Uniform conditional entropy <= log2(alpha), exactly after exponentiation.
                assert product_power(counts.values()) <= alpha ** n
                colorings += 1
    return dict(status="COMPUTATIONAL", graphs=graphs, proper_colorings=colorings,
                scope="Finite coloring/fiber inequality only; reachability is a proof premise.")

def product_power(counts):
    result = 1
    for count in counts:
        result *= count ** count
    return result

if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
