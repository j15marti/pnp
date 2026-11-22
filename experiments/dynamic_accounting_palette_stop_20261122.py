"""Exact audit of the post-acquisition palette record. Python 3."""
from collections import Counter
from fractions import Fraction
from itertools import product
import json

CODE = {1: "00", 2: "01", 3: "10"}

def record(values):
    k = len(values)
    assert k >= 2
    if k >= 4:
        return "", False
    total = 0
    bits = ""
    for j, value in enumerate(values, 1):
        bits += CODE[value]
        total += value
        if total + k - j > 3:
            return bits, False
    return bits, True

def decode(bits, k):
    if k >= 4:
        assert bits == ""
        return (), False
    inverse = {v: k for k, v in CODE.items()}
    prefix, total = [], 0
    for offset in range(0, len(bits), 2):
        value = inverse[bits[offset:offset+2]]
        prefix.append(value)
        total += value
        if total + k - len(prefix) > 3:
            assert offset + 2 == len(bits)
            return tuple(prefix), False
    assert len(prefix) == k
    return tuple(prefix), True

def main():
    results = []
    checked = 0
    for k in range(2, 9):
        counts = Counter()
        symbols = 0
        sat = 0
        for values in product((1,2,3), repeat=k):
            bits, answer = record(values)
            prefix, reconstructed = decode(bits,k)
            assert answer == (sum(values) <= 3) == reconstructed
            assert prefix == values[:len(bits)//2]
            events = list(range(len(bits)))
            assert len(events) == len(set(events))
            counts[bits] += 1
            symbols += len(prefix)
            sat += answer
            checked += 1
        words = sorted(counts)
        assert all(not b.startswith(a) for a,b in zip(words, words[1:]))
        kraft = sum((Fraction(1,2**len(w)) for w in words), Fraction())
        assert kraft <= 1
        expected_reads = Fraction(symbols,3**k)
        assert expected_reads == ({2:Fraction(5,3),3:Fraction(13,9)}.get(k,0))
        # A ternary uniform source assigns each terminal prefix probability 3^-r.
        assert all(Fraction(count,3**k) == Fraction(1,3**(len(bits)//2))
                   for bits,count in counts.items())
        results.append(dict(k=k, inputs=3**k, sat=sat, records=len(words),
                            mean_grade_reads=str(expected_reads),
                            mean_bit_reads=str(2*expected_reads),
                            kraft_sum=str(kraft), maximum_bits=max(map(len,words))))
    print(json.dumps(dict(checked=checked, status="PASS", cases=results),indent=2))

if __name__ == "__main__":
    main()
