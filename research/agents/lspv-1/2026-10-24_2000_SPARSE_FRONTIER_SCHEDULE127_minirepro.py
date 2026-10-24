#!/usr/bin/env python3
"""SPARSE-FRONTIER-SCHEDULE127 compact independent finite reproducer.
This tests Boolean semantics and structural accounting, not FLMV Turing-machine steps.
Run: python3 2026-10-24_2000_SPARSE_FRONTIER_SCHEDULE127_minirepro.py
"""
from fractions import Fraction
import itertools
import json
import random

SEED = 202610241950
rng = random.Random(SEED)
checks = 0
records = []

def check(cond, label):
    global checks
    checks += 1
    if not cond:
        raise AssertionError(label)

def brute(F, n):
    for a in range(1 << n):
        if all(any(bool(a & (1 << (abs(x) - 1))) == (x > 0)
                   for x in clause) for clause in F):
            return True
    return False

def scoped_dp(events):
    active = []
    table = {0}
    psi = 0
    visits = 0
    peak = 0
    for kind, value in events:
        old = len(active)
        if kind == "open":
            check(value not in active, "duplicate variable")
            active.append(value)
            table = {b for a in table for b in (a, a | (1 << old))}
            visits += len(table)
        elif kind == "clause":
            check(all(abs(x) in active for x in value), "invalid clause scope")
            check(len({abs(x) for x in value}) == 3, "not proper")
            pos = [(active.index(abs(x)), x > 0) for x in value]
            nxt = set()
            for a in table:
                visits += 1
                if any(bool(a & (1 << i)) == s for i, s in pos):
                    nxt.add(a)
            table = nxt
        elif kind == "close":
            check(value in active, "close missing")
            i = active.index(value)
            nxt = set()
            for a in table:
                visits += 1
                nxt.add((a & ((1 << i) - 1)) | ((a >> (i + 1)) << i))
            table = nxt
            active.pop(i)
        else:
            raise ValueError(kind)
        peak = max(peak, len(active))
        psi += 1 << max(old, len(active))
    check(not active, "nonempty boundary")
    check(visits <= 2 * psi, "too many table visits")
    return bool(table), psi, visits, peak

def events_for(F, n):
    return ([("open", i) for i in range(1, n + 1)] +
            [("clause", c) for c in F] +
            [("close", i) for i in range(n, 0, -1)])

# Eight clauses on one scope prohibit every assignment; deleting one makes SAT.
unsat_core = [tuple(-i if x else i for i, x in zip((1, 2, 3), b))
              for b in itertools.product((0, 1), repeat=3)]
check(not brute(unsat_core, 3), "eight-clause UNSAT")
check(brute(unsat_core[:-1], 3), "seven-clause SAT")

# A wide frontier can be transient, and weighted cost is strictly smaller
# than events * 2^peak; syntax is proper and incidence-connected.
for q in range(3, 9):
    for source_label in ("SAT", "UNSAT"):
        F = list(unsat_core if source_label == "UNSAT" else unsat_core[:-1])
        for i in range(30):
            F.append((1, 2, 3) if i % 2 else (1, -2, 3))
        n = q + 3
        for k in range(q):
            F.append((1, 4 + k, 4 + ((k + 1) % q)))
        ev = ([("open", i) for i in (1, 2, 3)] +
              [("clause", c) for c in F[:len(F)-q]] +
              [("open", i) for i in range(4, n + 1)] +
              [("clause", c) for c in F[len(F)-q:]] +
              [("close", i) for i in range(n, 0, -1)])
        actual = brute(F, n)
        result, psi, visits, peak = scoped_dp(ev)
        check(actual == result, "burst mismatch")
        check(actual == (source_label == "SAT"), "burst source label")
        check(psi < len(ev) * (1 << peak), "no strict weighted advantage")
        records.append({"kind": "burst", "q": q, "expected": actual,
                        "psi": psi, "flat": len(ev) * (1 << peak),
                        "visits": visits, "peak": peak})

for i in range(96):
    n = rng.randint(3, 8)
    m = rng.randint(0, 16)
    F = []
    for _ in range(m):
        ids = rng.sample(range(1, n + 1), 3)
        F.append(tuple(x if rng.randrange(2) else -x for x in ids))
    predicted = brute(F, n)
    observed, psi, visits, peak = scoped_dp(events_for(F, n))
    check(predicted == observed, f"random trial {i}")
    records.append({"kind": "random", "i": i, "n": n, "m": m,
                    "sat": observed, "psi": psi, "visits": visits})

def beta(c):
    return (Fraction(1, 2) *
            ((c + 2) / (c * c) - c))

c = Fraction(53, 50)
check(beta(c) == Fraction(233623, 280900), "FLMV rational")
check(Fraction(21, 20) < c, "strict time entry")
check(Fraction(43, 100) < beta(c), "strict space entry")
check(beta(Fraction(143, 100)) ==
      Fraction(505793, 4089800), "old estimate at endpoint")
print(json.dumps({"run": "SPARSE-FRONTIER127-compact", "seed": SEED,
                  "cases": len(records), "checks": checks,
                  "failures": 0,
                  "first": records[0], "last": records[-1]},
                 sort_keys=True))
