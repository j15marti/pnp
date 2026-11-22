"""Audit semantic anchor fibers, independently of Construction's implementation."""
import itertools
import json
import math


def anchors(rows):
    m = len(rows)
    arcs = {}
    for x in range(5):
        support = {i for i, row in enumerate(rows) if x in row}
        if not support:
            return None
        starts = [i for i in support if (i - 1) % m not in support]
        if len(support) == m:
            arcs[x] = (0, m)
        elif len(starts) == 1:
            arcs[x] = (starts[0], len(support))
        else:
            return None
    outcomes = []
    for x in rows[0]:
        start, length = arcs[x]
        origin = (start + length) % m
        gap = m - length
        reachable = {0}
        for pos in range(gap):
            if pos in reachable:
                for s, size in arcs.values():
                    if (s - origin) % m == pos and pos + size <= gap:
                        reachable.add(pos + size)
        outcomes.append(int(gap in reachable))
    return tuple(outcomes)


def main():
    representatives = {}
    checked = 0
    for tail in itertools.product(itertools.combinations(range(5), 3), repeat=4):
        rows = ((0, 1, 2),) + tail
        vector = anchors(rows)
        if vector is None:
            continue
        oracle = [0, 0, 0]
        for assignment in itertools.product((0, 1), repeat=5):
            if all(sum(assignment[x] for x in row) == 1 for row in rows):
                for j in range(3):
                    oracle[j] |= assignment[j]
        assert tuple(oracle) == vector
        checked += 1
        representatives.setdefault(vector, rows)
    records = [{"anchors": v, "rows": rows, "ready_bit": int(any(v))}
               for v, rows in sorted(representatives.items())]
    assert len(records) == 8
    # Uniform prior on these eight authentic sources, each with m=5,v=5.
    fibers = {d: [r["anchors"] for r in records if r["ready_bit"] == d]
              for d in (0, 1)}
    assert [len(fibers[d]) for d in (0, 1)] == [1, 7]
    decision_entropy = -sum((len(f)/8)*math.log2(len(f)/8) for f in fibers.values())
    print(json.dumps({"checked_sources": checked, "representatives": records,
                      "fiber_sizes": [1, 7], "joint_anchor_entropy": 3,
                      "decision_entropy": decision_entropy,
                      "anchor_entropy_given_decision": 7/8*math.log2(7),
                      "events": {"READY_reads": 1, "capacity": 1,
                                 "overhead": 0, "reuse": 1},
                      "scope": "source fibers and normalized READY suffix only",
                      "seed": None}, indent=2))


if __name__ == "__main__":
    main()
