"""Exact rational audit of stopped-scan records, Python 3 standard library."""
from collections import Counter
from fractions import Fraction
from itertools import product
import json


def audit(t):
    counts = [Counter() for _ in range(t)]
    total_reads = 0
    total_memberships = 0
    maximum_reuse = 0
    for word in product((0, 1), repeat=t):
        stop = word.index(1) + 1 if 1 in word else t
        record = word[:stop]
        total_reads += stop
        reuse = Counter()
        for j in range(1, t + 1):
            prefix = record[:j]
            counts[j-1][prefix] += 1
            for event in range(len(prefix)):
                reuse[event] += 1
        assert max(reuse.values()) == t
        assert sum(reuse.values()) == sum(min(j, stop) for j in range(1, t+1))
        total_memberships += sum(reuse.values())
        maximum_reuse = max(maximum_reuse, max(reuse.values()))
    entropy_sum = Fraction(0)
    for j, count in enumerate(counts, 1):
        records = list(count)
        assert all(not (len(x) < len(y) and y[:len(x)] == x)
                   for x in records for y in records)
        assert sum(Fraction(1, 2**len(x)) for x in records) == 1
        entropy = Fraction(0)
        for record, frequency in count.items():
            probability = Fraction(frequency, 2**t)
            assert probability == Fraction(1, 2**len(record))
            entropy += probability * len(record)
        assert entropy == 2 - Fraction(1, 2**(j-1))
        entropy_sum += entropy
    mean_reads = Fraction(total_reads, 2**t)
    assert mean_reads == 2 - Fraction(1, 2**(t-1))
    assert entropy_sum == 2*t - 2 + Fraction(1, 2**(t-1))
    assert entropy_sum == Fraction(total_memberships, 2**t)
    assert entropy_sum / maximum_reuse <= mean_reads
    return dict(t=t, inputs=2**t, mean_reads=str(mean_reads),
                summed_entropy=str(entropy_sum), reuse=maximum_reuse,
                corrected_bound=str(entropy_sum/maximum_reuse))


if __name__ == "__main__":
    print(json.dumps([audit(t) for t in (3, 5, 7, 9, 11)], indent=2))
