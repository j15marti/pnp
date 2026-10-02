#!/usr/bin/env python3
"""Hand-checkable controls, distinct from the C++ construction/search."""
import csv
import json
import math
import sys
from functools import lru_cache
from pathlib import Path

out = Path(sys.argv[1])

# All 256 simple three-variable formulas, grouped by number of clauses.
d3 = []
for m in range(9):
    formulas = [f for f in range(256) if f.bit_count() == m]
    unsat = sum(f == 255 for f in formulas)
    assert len(formulas) == math.comb(8, m)
    assert unsat == (1 if m == 8 else 0)
    d3.append(dict(n=3, m=m, formulas=len(formulas), unsat=unsat,
                   minimum_decision_nodes=0))

# This recurrence optimizes TREES, not globally shared DAGs.
@lru_cache(None)
def tree_opt(rows, available):
    if len({x.bit_count() % 2 for x in rows}) <= 1:
        return 0
    return min(1 + tree_opt(tuple(x for x in rows if not (x >> q & 1)),
                            tuple(v for v in available if v != q))
                 + tree_opt(tuple(x for x in rows if x >> q & 1),
                            tuple(v for v in available if v != q))
               for q in available)

unique = {}
def bdd(rows, level):
    vals = {x.bit_count() % 2 for x in rows}
    if len(vals) == 1:
        return vals.pop()
    lo = bdd(tuple(x for x in rows if not (x >> level & 1)), level + 1)
    hi = bdd(tuple(x for x in rows if x >> level & 1), level + 1)
    if lo == hi:
        return lo
    key = (level, lo, hi)
    return unique.setdefault(key, len(unique) + 2)

tree_nodes = tree_opt(tuple(range(8)), (0, 1, 2))
bdd(tuple(range(8)), 0)
assert tree_nodes == 7 and len(unique) == 5

# Aggregate profile counts must recover the complete fixed-(n,m) populations.
profile_totals = {}
with (out / "imbalance_variance.csv").open() as f:
    for row in csv.DictReader(f):
        m = int(row["m"])
        totals = profile_totals.setdefault(m, [0, 0])
        totals[0] += int(row["formulas"])
        totals[1] += int(row["unsat"])
with (out / "verification.csv").open() as f:
    for row in csv.DictReader(f):
        m = int(row["m"])
        assert int(row["inputs"]) == math.comb(32, m)
        assert profile_totals[m] == [int(row["inputs"]), int(row["unsat"])]
        assert int(row["dag_errors"]) == int(row["circuit_errors"]) == 0

# Inspect the actual netlist, including fan-in, connected gate count and depth.
lines = (out / "coverage.circuit").read_text().splitlines()
inputs, gate_count, output = map(int, lines[0].split())
depth = [0] * inputs
net = {}
for line in lines[1:]:
    i, op, a, b = line.split()
    i, a, b = int(i), int(a), int(b)
    assert i == len(depth) and 0 <= a < i and 0 <= b < i
    assert op in {"A", "O", "N"}
    net[i] = (op, a, b)
    depth.append(1 + max(depth[a], depth[b]))
seen = set()
def walk(i):
    if i < inputs or i in seen:
        return
    seen.add(i)
    _, a, b = net[i]
    walk(a)
    walk(b)
walk(output)
assert gate_count == len(seen) == 64 and depth[output] == 7

result = dict(d3=d3, parity3_tree_nodes=tree_nodes,
              parity3_ordered_dag_nodes=len(unique),
              circuit_gates=64, circuit_depth=7,
              profile_totals=profile_totals, status="PASS")
(out / "controls.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
