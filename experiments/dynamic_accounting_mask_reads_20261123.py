"""Exact finite transcript audit. Run from repository root, Python 3."""
from collections import Counter
from fractions import Fraction
from itertools import product, permutations
import json

def scan(masks, context):
    transcript = []
    for mask, allowed in zip(masks, context):
        for bit in range(3):
            if allowed & (1 << bit):
                value = (mask >> bit) & 1
                transcript.append(value)
                if value:
                    break
        else:
            return tuple(transcript), False
    return tuple(transcript), True

def prediction(context):
    reach = Fraction(1)
    expected = Fraction(0)
    for mask in context:
        p = 1 - Fraction(1, 2**mask.bit_count())
        reach *= p
        expected += 2 * reach
    return expected, reach

def main():
    contexts = inputs = 0
    examples = []
    for m in (1, 2, 3):
        for context in product(range(1, 8), repeat=m):
            counts = Counter()
            sat = 0
            for masks in product(range(8), repeat=m):
                word, answer = scan(masks, context)
                assert answer == all(a & b for a, b in zip(masks, context))
                counts[word] += 1
                sat += answer
                inputs += 1
            total = 8**m
            words = sorted(counts)
            assert all(not b[:len(a)] == a for a,b in zip(words, words[1:]))
            assert sum(Fraction(1, 2**len(w)) for w in words) == 1
            assert all(n == 2**(3*m-len(w)) for w,n in counts.items())
            measured = sum(Fraction(n*len(w),total) for w,n in counts.items())
            expected, probability = prediction(context)
            assert measured == expected and Fraction(sat,total) == probability
            contexts += 1
            if context == (7,)*m:
                examples.append(dict(m=m, expected_reads=str(expected),
                                     residual_bits=str(3*m-expected),
                                     sat_probability=str(probability)))
    order_tests = 0
    for lengths in product((1,2,3), repeat=5):
        masks = tuple((1 << k)-1 for k in lengths)
        best = prediction(sorted(masks, key=int.bit_count))[0]
        assert all(best <= prediction(order)[0] for order in set(permutations(masks)))
        order_tests += 1
    print(json.dumps(dict(contexts=contexts, source_mask_pairs=inputs,
                         order_tests=order_tests, full_context_examples=examples), indent=2))

if __name__ == "__main__":
    main()
