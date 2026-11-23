"""Exact finite audit of stopped conjunction records under fair block labels."""
from collections import Counter
from fractions import Fraction
from itertools import product
import json


def main():
    results = []
    for blocks in range(1, 11):
        counts = Counter()
        read_sum = 0
        for labels in product((0, 1), repeat=blocks):
            record = []
            for value in labels:
                record.append(value)
                if value == 0:
                    break
            record = tuple(record)
            assert all(labels) == all(record)
            counts[record] += 1
            read_sum += len(record)
        words = list(counts)
        assert all(not (len(a) < len(b) and b[:len(a)] == a)
                   for a in words for b in words)
        entropy = Fraction(0)
        for record, multiplicity in counts.items():
            assert multiplicity == 2 ** (blocks - len(record))
            entropy += Fraction(multiplicity, 2**blocks) * len(record)
        expectation = Fraction(read_sum, 2**blocks)
        assert entropy == expectation == 2 - Fraction(1, 2**(blocks-1))
        assert sum(Fraction(1, 2**len(word)) for word in words) == 1
        results.append(dict(blocks=blocks, inputs=2**blocks,
                            records=len(words), expected_reads=str(expectation),
                            entropy_bits=str(entropy),
                            residual_entropy_bits=str(blocks-entropy)))
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
