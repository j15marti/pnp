"""Exact shortcut on strict-C inputs. Run from repository root with Python 3."""
from collections import defaultdict
from hashlib import sha256
from itertools import combinations
from math import prod
import json
from pathlib import Path

import t5_construction_disjoint_cut_20261121 as family
import t5_construction_positive_offset1_20261121 as c
import t5_redteam_wrapper_orbit_20261121 as wrapper


def graph(rows):
    adjacent = defaultdict(set)
    for row in rows:
        for v in row:
            adjacent[v].update(set(row) - {v})
    return dict(adjacent)


def order(adjacent, removed=(), limit=9):
    removed = set(removed)
    live = {v: ns - removed for v, ns in adjacent.items() if v not in removed}
    sequence = []
    width = 0
    while live:
        v = min(live, key=lambda x: (len(live[x]), x))
        neighbors = live.pop(v)
        if len(neighbors) > limit:
            return None
        width = max(width, len(neighbors))
        for u in neighbors:
            live[u].remove(v)
            live[u].update(neighbors - {u})
        sequence.append(v)
    return sequence, width


def find_order(adjacent):
    quick = order(adjacent)
    if quick is not None:
        return quick[0], "minimum degree"
    for deleted in combinations(sorted(adjacent), min(7, len(adjacent))):
        slow = order(adjacent, deleted, limit=2)
        if slow is not None:
            return slow[0] + list(deleted), "seven deletions"
    return None, "UNKNOWN"


def join(left, right):
    xs, f = left
    ys, g = right
    common = [y for y in ys if y in xs]
    xkey = [xs.index(y) for y in common]
    ykey = [ys.index(y) for y in common]
    fresh = [i for i, y in enumerate(ys) if y not in xs]
    index = defaultdict(list)
    for assignment, value in g.items():
        index[tuple(assignment[i] for i in ykey)].append(
            (tuple(assignment[i] for i in fresh), value))
    table = {}
    for assignment, value in f.items():
        for tail, weight in index.get(tuple(assignment[i] for i in xkey), ()):
            table[assignment + tail] = value * weight
    return xs + tuple(ys[i] for i in fresh), table


def evaluate(bits):
    try:
        _, links, rows = wrapper.recover(bits)
    except (ValueError, IndexError, AssertionError):
        return None, {"status": "UNKNOWN"}
    adjacent = graph(rows)
    elimination, mode = find_order(adjacent)
    if elimination is None:
        return None, {"status": "UNKNOWN"}
    allowed = dict.fromkeys(c.TABLE, 1)
    factors = [(tuple(row), allowed) for row in rows]
    peak_width = 0
    for v in elimination:
        bucket = [f for f in factors if v in f[0]]
        factors = [f for f in factors if v not in f[0]]
        bucket.sort(key=lambda f: len(f[1]))
        scope, table = bucket[0]
        for other in bucket[1:]:
            scope, table = join((scope, table), other)
        peak_width = max(peak_width, len(scope)-1)
        pos = scope.index(v)
        message = defaultdict(int)
        for values, weight in table.items():
            message[values[:pos] + values[pos+1:]] += weight
        factors.append((scope[:pos] + scope[pos+1:], message))
    assert all(not scope for scope, _ in factors) and peak_width <= 9
    result = prod(table.get((), 0) for _, table in factors) << links
    return result, dict(status="SAT" if result else "UNSAT", links=links,
                        quotient_width_used=peak_width, order_method=mode)


def run():
    # The quotient witness is used only by this structural cross-check.
    # The solver receives only shuffled bytes.
    width_witnesses = []
    for k in (1, 2, 5):
        for a, b in ((0,0), ((1 << k)-1, (1 << k)-1)):
            core = family.image(k, a, b)[-1]
            deleted = (*range(5), 5, 5+k+1)  # anchors, x0, T (second gate)
            certificate = order(graph(core), deleted, limit=2)
            assert certificate is not None
            width_witnesses.append(dict(k=k,a=a,b=b,width=certificate[1]))
    # K11 cannot have a seven-vertex deletion leaving width at most two.
    clique = {v: set(range(11)) - {v} for v in range(11)}
    assert find_order(clique) == (None, "UNKNOWN")
    rows = []
    for k, a, b, seed in [(1,0,0,3),(1,1,1,5),(2,1,2,7),(2,3,1,11),
                          (4,5,10,13),(4,12,4,17)]:
        n, cs = c.decode(family.image(k,a,b)[0])
        bits = wrapper.wrapped(n, cs, seed)
        got, detail = evaluate(bits)
        expected = 0 if a & b else 10 << (98 + 282*k + k - b.bit_count())
        assert got == expected
        rows.append(dict(k=k,a=a,b=b,seed=seed,N=len(bits),
                         input_sha256=sha256(bits.encode()).hexdigest(),
                         count=str(got),**detail))
    controls = []
    for n, cs in [(3,[(0,1,2)]),(4,list(combinations(range(4),3))),
                  (7,[(0,1,2),(0,3,4),(0,5,6)])]:
        bits = c.encode(n,cs)
        value, detail = evaluate(bits)
        if n == 4:
            nn, split, e = c.split(n,cs)
            bits = wrapper.wrapped(nn, split, 19)
            value, detail = evaluate(bits)
            assert value == c.generic_count(n,cs)[0] << e == 0
        elif n == 3:
            assert value == 30
        else:
            assert value is None
        controls.append(dict(n=n,rows=cs,count=value,**detail))
    return dict(lemma="T5-DISJ-ORBIT-WIDTH1", trials=rows, controls=controls,
                width_witnesses=width_witnesses, clique11_order="UNKNOWN",
                sha256={Path(m.__file__).name:sha256(Path(m.__file__).read_bytes()).hexdigest()
                        for m in (family,family.balanced,c,wrapper)})


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
