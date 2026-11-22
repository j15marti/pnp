"""Exact finite fibers for joint preprocessing debit; not a tape simulation.

Run: python3 experiments/dynamic_bounds_joint_prepayment_20261122.py
The family and local relations are pinned in the companion Bounds report.
"""
from collections import Counter, defaultdict
from itertools import combinations, product
from math import comb, log2
import hashlib
import json
from pathlib import Path


def entropy(values):
    counts = Counter(values)
    size = sum(counts.values())
    return -sum((n / size) * log2(n / size) for n in counts.values())


def conditional(values, side):
    fibers = defaultdict(list)
    for value, given in zip(values, side):
        fibers[given].append(value)
    return sum(len(v) * entropy(v) for v in fibers.values()) / len(values)


def source_label(t, marks, kind):
    # Independent enumeration of z cycles for uniform AA or CC columns.
    relation = {(0, 0), (1, 1), (1, 0)} if kind == "A" else {(0, 1), (1, 0)}
    return any(all((z[i], z[(i + 1) % t]) in relation for i in range(t))
               and sum(z[i] for i in marks) % 2 == 0
               for z in product((0, 1), repeat=t))


def audit(t):
    samples = [(marks, kind) for marks in combinations(range(t), 3) for kind in "AC"]
    markers = [s[0] for s in samples]
    labels = [int(source_label(t, marks, kind)) for marks, kind in samples]
    assert labels == [int(kind == "A") for _, kind in samples]
    assert Counter(labels) == {0: comb(t, 3), 1: comb(t, 3)}
    # The retained statistic is M only, not the answer or the whole configuration.
    assert all(Counter(labels[i] for i, m in enumerate(markers) if m == mark) == {0: 1, 1: 1}
               for mark in set(markers))
    rows = []
    for repetitions in (1, 2, 5):
        obligations = [tuple([m] * repetitions + [d]) for m, d in zip(markers, labels)]
        joint = entropy(obligations)
        residual = conditional(obligations, markers)
        marginal = repetitions * entropy(markers) + entropy(labels)
        chain = sum(conditional([u[j] for u in obligations],
                                [(m, u[:j]) for m, u in zip(markers, obligations)])
                    for j in range(repetitions + 1))
        assert abs(joint - (log2(comb(t, 3)) + 1)) < 1e-10
        assert abs(residual - 1) < 1e-10 and abs(chain - residual) < 1e-10
        # Exact decoding from empty marker records and one decision bit.
        for m, d, u in zip(markers, labels, obligations):
            records = [""] * repetitions + [str(d)]
            decoded = tuple([m] * repetitions + [int(records[-1])])
            assert decoded == u and sum(map(len, records)) == 1
        rows.append(dict(repetitions=repetitions, joint_bits=joint,
                         marginal_bits=marginal, retained_marker_bits=entropy(markers),
                         residual_joint_bits=residual, conditional_chain_bits=chain,
                         invalid_marginal_minus_single_debit=marginal-entropy(markers),
                         charged_payload_bits=1, framing_bits=0, maximum_reuse=1))
    return dict(t=t, samples=len(samples), marker_fibers=comb(t, 3),
                labels=dict(Counter(labels)), rows=rows)


if __name__ == "__main__":
    print(json.dumps(dict(
        code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        mode="exhaustive finite fibers; entropy logs floating; no native tape simulation",
        seed=None, cases=[audit(t) for t in (3, 5, 7, 9)]), indent=2))
