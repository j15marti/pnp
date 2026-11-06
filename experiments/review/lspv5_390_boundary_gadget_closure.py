#!/usr/bin/env python3
"""Exact source-once closure for the six-item bridge boundary quotient.

The two equation leaves are the authenticated XOR summaries of the four
complete internal parity rows on each side.  The four clause leaves are the
essential boundary clauses of REFEREE386's 36-clause MUS core.
"""
from __future__ import annotations
import hashlib, json, resource, time

VARS = tuple(range(1, 16))
INDEX = {v: i for i, v in enumerate(VARS)}

def clause(*lits):
    return ("C", tuple(sorted(lits, key=lambda z: (abs(z), z < 0))))

def eq(vars_, rhs):
    mask = 0
    for v in vars_: mask ^= 1 << INDEX[v]
    return ("E", mask, rhs & 1)

SIX_SOURCES = (
    eq((1, 2), 1),
    clause(1, -2, 15),
    clause(-1, 2, 15),
    eq((8, 9), 0),
    clause(8, 9, -15),
    clause(-8, -9, -15),
)

ROW_SOURCES = (
    eq((1, 3, 4), 1),
    eq((2, 5, 6), 0),
    eq((3, 5, 7), 0),
    eq((4, 6, 7), 0),
    clause(1, -2, 15),
    clause(-1, 2, 15),
    eq((8, 10, 11), 0),
    eq((9, 12, 13), 0),
    eq((10, 12, 14), 0),
    eq((11, 13, 14), 0),
    clause(8, 9, -15),
    clause(-8, -9, -15),
)

def support(x):
    if x[0] == "C": return frozenset(abs(v) for v in x[1])
    if x[0] == "E": return frozenset(VARS[i] for i in range(len(VARS)) if x[1] >> i & 1)
    return frozenset(x[1])

def holds(x, bits):
    if x[0] == "C":
        return any((bits[INDEX[abs(v)]] == 1) == (v > 0) for v in x[1])
    if x[0] == "E":
        return (sum(bits[i] for i in range(len(VARS)) if x[1] >> i & 1) & 1) == x[2]
    loc = tuple(bits[INDEX[v]] for v in x[1])
    idx = sum(b << i for i, b in enumerate(loc))
    return bool(x[2] >> idx & 1)

def factor(a, b):
    sup = tuple(sorted(support(a) | support(b)))
    if len(sup) > 3: return None
    table = 0
    for idx in range(1 << len(sup)):
        bits = [0] * len(VARS)
        for j, v in enumerate(sup): bits[INDEX[v]] = idx >> j & 1
        if holds(a, bits) and holds(b, bits): table |= 1 << idx
    return ("F", sup, table)

def affine_alias(f):
    sup, table = f[1], f[2]
    sup_mask = sum(1 << INDEX[v] for v in sup)
    mask = sup_mask
    masks = []
    while True:
        masks.append(mask)
        if mask == 0: break
        mask = (mask - 1) & sup_mask
    for mask in masks:
        for rhs in (0, 1):
            e = ("E", mask, rhs)
            ok = True
            for idx in range(1 << len(sup)):
                bits = [0] * len(VARS)
                for j, v in enumerate(sup): bits[INDEX[v]] = idx >> j & 1
                if holds(e, bits) != bool(table >> idx & 1): ok = False; break
            if ok: return e
    return None

def resolve(a, b):
    if a[0] != b[0] or a[0] != "C": return None
    A, B = set(a[1]), set(b[1])
    piv = {abs(v) for v in A if -v in B}
    if len(piv) != 1: return None
    p = next(iter(piv))
    out = (A | B) - {p, -p}
    if any(-v in out for v in out): return None
    return clause(*out)

def closure(sources):
    n = len(sources)
    dp = [set() for _ in range(1 << n)]
    for i, s in enumerate(sources): dp[1 << i].add(s)
    tests = {"RES": 0, "AND3": 0, "XOR": 0}
    for size in range(2, n + 1):
        for sub in range(1, 1 << n):
            if sub.bit_count() != size: continue
            a = (sub - 1) & sub
            while a:
                b = sub ^ a
                if b and a < b:
                    for x in dp[a]:
                        for y in dp[b]:
                            if x[0] == y[0] == "C":
                                tests["RES"] += 1
                                z = resolve(x, y)
                                if z is not None: dp[sub].add(z)
                            tests["AND3"] += 1
                            z = factor(x, y)
                            if z is not None:
                                dp[sub].add(z)
                                e = affine_alias(z)
                                if e is not None: dp[sub].add(e)
                            if x[0] == y[0] == "E":
                                tests["XOR"] += 1
                                dp[sub].add(("E", x[1] ^ y[1], x[2] ^ y[2]))
                a = (a - 1) & sub
    return dp, tests

def main():
    t0 = time.perf_counter()
    cases = {}
    for name, sources in (("six_summary", SIX_SOURCES), ("twelve_row_respecting", ROW_SOURCES)):
        dp, tests = closure(sources)
        full = dp[-1]
        false = [
            x for x in full
            if (x[0] == "C" and not x[1])
            or (x[0] == "E" and x[1] == 0 and x[2] == 1)
            or (x[0] == "F" and x[2] == 0)
        ]
        cases[name] = {
            "sources": [repr(x) for x in sources],
            "source_sha256": hashlib.sha256(repr(sources).encode()).hexdigest(),
            "full_outcomes": len(full),
            "full_outcomes_by_type": {k: sum(x[0] == k for x in full) for k in ("C","F","E")},
            "contradictions": [repr(x) for x in false],
            "pair_tests": tests,
        }
    raw = {
        "run": "LSPV-5/REFEREE390 boundary quotient closure",
        "scope": "six-summary and complete twelve-item row-respecting quotients; strict source-once RES+AND3+XOR; no LOCAL/DEF",
        "cases": cases,
        "wall_seconds": time.perf_counter() - t0,
        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "status": "COMPUTATIONAL_EXACT_FINITE",
    }
    print(json.dumps(raw, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
