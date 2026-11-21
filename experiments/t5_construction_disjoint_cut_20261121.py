"""Canonical strict-C split images of two-party disjointness."""
from collections import Counter
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

import t5_construction_balanced_polarity_20261121 as balanced
import t5_construction_positive_offset1_20261121 as compiler


def image(k, a, b):
    if k < 1 or min(a, b) < 0 or max(a, b) >= 1 << k:
        raise ValueError("two k-bit masks required")
    gates = []

    def gate(kind, *operands):
        gates.append((kind, *operands))
        return k + len(gates) - 1

    true = gate("or", 0, gate("not", 0))

    def selector(bit):
        zero = gate("not", true)
        one = gate("not", zero)
        first, other = (zero, one) if bit else (one, zero)
        selected = gate("not", first)
        gate("not", other)
        return selected

    left = [selector(a >> i & 1) for i in range(k)]
    middle = [gate("or", x, i) for i, x in enumerate(left)]
    right = [selector(b >> i & 1) for i in range(k)]
    bad = []
    for x, y in zip(middle, right):
        bad.append(gate("not", gate("or", gate("not", x), gate("not", y))))
    any_bad = bad[0]
    for bit in bad[1:]:
        any_bad = gate("or", any_bad, bit)
    out = gate("not", any_bad)
    n, clauses = balanced.twins(k, gates, out)[0]
    degree = Counter(x for row in clauses for x in row)
    nn, split, links = compiler.split(n, clauses)
    data = compiler.encode(nn, split)
    w = nn.bit_length()
    header = len(data) - 3 * len(split) * w

    def packet_start(source_name):
        before = sum(degree[q] - 1 for q in range(source_name))
        return header + w * (3 * len(clauses) + 18 * before)

    lo = packet_start(5 + middle[0])
    hi = packet_start(6 + middle[-1])
    assert hi - lo == 72 * k * w
    assert (n, len(clauses), links, nn, len(split)) == (
        25+66*k, 41+116*k, 98+282*k, 515+1476*k, 629+1808*k)
    return data, (lo, hi), gates, out, n, clauses


def audit(k):
    masks = range(1 << k)
    left = [image(k, a, 0)[0] for a in masks]
    right = [image(k, 0, b)[0] for b in masks]
    rows = []
    for a, b in product(masks, repeat=2):
        data, (lo, hi), gates, out, n, clauses = image(k, a, b)
        assert data[lo:hi] == left[0][lo:hi]
        for cut in (lo, hi):
            assert data == left[a][:cut] + right[b][cut:]
        count = 0 if a & b else 1 << (k - b.bit_count())
        assert compiler.source_count(k, gates, out) == count
        row = dict(a=a, b=b, source_count=count, encoding_sha256=sha256(data.encode()).hexdigest())
        if k == 1 or (k == 2 and (a,b) in ((1,2),(2,1),(1,1),(2,2))):
            got, calls = compiler.generic_count(n, clauses)
            assert got == 10 * count
            row.update(unsplit_generic_count=got, search_calls=calls)
        rows.append(row)
    return dict(k=k, N=len(data), separator_half_open=[lo,hi], cases=rows)


if __name__ == "__main__":
    results = [audit(k) for k in (1,2,3)]
    print(json.dumps(dict(lemma="T5-BALANCED-DISJ-CUT1", results=results,
                          dependencies={Path(mod.__file__).name: sha256(Path(mod.__file__).read_bytes()).hexdigest()
                                        for mod in (compiler, balanced)}), indent=2))
