#!/usr/bin/env python3
"""Finite controls for ONEBIT-REUSE-ENTROPY-REFEREE190.

Combines a fixed-length proper-3CNF scalar source Phi_m(b) with the
one-boundary-bit lift G_F.  The current exact projection has one semantic bit,
but no-reread reuse under h authenticated source-bit overwrites has
1 + sum_{j<=h} binom(m,j) behaviours (h<m), or 2^m (h>=m).

This is a restricted dynamic-state theorem, not a static SAT lower bound.
"""
from __future__ import annotations

import collections
import hashlib
import itertools
import json
import math

ASSERT = collections.Counter()


def ck(cond, tag):
    ASSERT["total"] += 1
    if not cond:
        raise AssertionError(tag)


class Vars:
    def __init__(self):
        self.n = 0

    def one(self):
        self.n += 1
        return self.n

    def many(self, k):
        return [self.one() for _ in range(k)]


def force(lit, u, v):
    return [
        (lit, u, v),
        (lit, u, -v),
        (lit, -u, v),
        (lit, -u, -v),
    ]


def phi(bits):
    """LSPV-4 fixed-length proper 3CNF, SAT iff all bits are one."""
    m = len(bits)
    V = Vars()
    x = V.many(m)
    uv = [V.many(2) for _ in range(m)]
    y = V.many(m + 1)
    tw = [V.many(2) for _ in range(m)]
    y_aux = [V.many(2), V.many(2)]
    clauses = []
    control_positions = []
    for i, bit in enumerate(bits):
        lit = x[i] if bit else -x[i]
        start = len(clauses)
        clauses.extend(force(lit, *uv[i]))
        control_positions.append([(start + j, 0) for j in range(4)])
    for i in range(m):
        t, w = tw[i]
        clauses.extend([
            (-y[i + 1], y[i], t),
            (-y[i + 1], y[i], -t),
            (-y[i + 1], x[i], w),
            (-y[i + 1], x[i], -w),
            (y[i + 1], -y[i], -x[i]),
        ])
    clauses.extend(force(y[0], *y_aux[0]))
    clauses.extend(force(y[-1], *y_aux[1]))
    ck(V.n == 6 * m + 5, "phi variable count")
    ck(len(clauses) == 9 * m + 8, "phi clause count")
    return tuple(clauses), V.n, control_positions


def lift(formula, n):
    """G_F(z): each (a,b,c) becomes (~z,a,t) & (~t,b,c)."""
    z = n + 1
    clauses = []
    control_map = []
    next_var = z
    for ci, (a, b, c) in enumerate(formula):
        next_var += 1
        t = next_var
        clauses.append((-z, a, t))
        clauses.append((-t, b, c))
        control_map.append((2 * ci, 1))
    return tuple(clauses), next_var, z, control_map


def proper(formula):
    return all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in formula)


def connected(formula, n):
    g = {v: set() for v in range(1, n + 1)}
    for c in formula:
        a = list(map(abs, c))
        for u in a:
            for v in a:
                if u != v:
                    g[u].add(v)
    seen = {1}
    q = [1]
    for u in q:
        for v in g[u]:
            if v not in seen:
                seen.add(v)
                q.append(v)
    return len(seen) == n


def simplify(clauses, var, val):
    sat_lit = var if val else -var
    bad_lit = -sat_lit
    out = []
    for c in clauses:
        if sat_lit in c:
            continue
        d = tuple(x for x in c if x != bad_lit)
        if not d:
            return None
        out.append(d)
    return tuple(out)


def dpll(clauses):
    clauses = tuple(clauses)
    while True:
        unit = next((c[0] for c in clauses if len(c) == 1), None)
        if unit is None:
            break
        clauses = simplify(clauses, abs(unit), unit > 0)
        if clauses is None:
            return False
        if not clauses:
            return True
    if not clauses:
        return True
    var = abs(min(clauses, key=len)[0])
    for val in (False, True):
        nxt = simplify(clauses, var, val)
        if nxt is not None and dpll(nxt):
            return True
    return False


def fixed_width_bytes(formula, n):
    width = max(1, ((2 * n + 2).bit_length() + 7) // 8)
    data = bytearray(b"OBR190\x00")
    data.extend(n.to_bytes(4, "big"))
    data.extend(len(formula).to_bytes(4, "big"))
    data.append(width)
    for c in formula:
        for lit in c:
            word = 2 * abs(lit) + (lit < 0)
            data.extend(word.to_bytes(width, "big"))
    return bytes(data)


def class_count(m, h):
    if h >= m:
        return 1 << m
    return 1 + sum(math.comb(m, j) for j in range(h + 1))


def behavior_class(zero_set, m, h):
    s = frozenset(zero_set)
    return s if len(s) <= h else "overflow"


def distinguish(S, T, h):
    """A common <=h set-to-one stream distinguishing two class reps."""
    S, T = set(S), set(T)
    if len(S) <= h and not T.issubset(S):
        stream = sorted(S)
    elif len(T) <= h and not S.issubset(T):
        stream = sorted(T)
    else:
        return None
    ans_s = not (S - set(stream))
    ans_t = not (T - set(stream))
    ck(ans_s != ans_t, "distinguishing stream")
    return stream


finite_sources = []
dpll_cases = 0
length_checks = 0
for m in range(1, 5):
    lengths = set()
    for bits in itertools.product((0, 1), repeat=m):
        F, n, controls = phi(bits)
        G, gn, z, cmap = lift(F, n)
        ck(proper(F), "proper phi")
        ck(proper(G), "proper lift")
        ck(connected(G, gn), "connected lift")
        ck(len(controls) == m and all(len(x) == 4 for x in controls), "four controls")
        ck(all(cmap[pos[0]][1] == 1 for group in controls for pos in group), "lifted controls")
        # Exact current one-bit projection: z=0 always SAT; z=1 iff AND(bits).
        sat0 = dpll(G + ((-z,),))
        sat1 = dpll(G + ((z,),))
        dpll_cases += 2
        ck(sat0, "z=0 must satisfy")
        ck(sat1 == all(bits), "z=1 projection")
        raw = fixed_width_bytes(G, gn)
        lengths.add(len(raw))
        finite_sources.append({
            "m": m,
            "bits": "".join(map(str, bits)),
            "projection": "TOP" if sat1 else "NOT_Z",
            "variables": gn,
            "clauses": len(G),
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
        })
    ck(len(lengths) == 1, "equal physical length")
    length_checks += 1


entropy_rows = []
pair_checks = 0
for m in range(1, 11):
    universe = range(m)
    subsets = [frozenset(i for i in universe if mask >> i & 1) for mask in range(1 << m)]
    for h in range(0, m + 1):
        classes = {behavior_class(s, m, h) for s in subsets}
        expected = class_count(m, h)
        ck(len(classes) == expected, "class count")
        reps = []
        for c in classes:
            if c == "overflow":
                reps.append(frozenset(range(h + 1)))
            else:
                reps.append(c)
        for i in range(len(reps)):
            for j in range(i + 1, len(reps)):
                ck(distinguish(reps[i], reps[j], h) is not None, "pair distinguishable")
                pair_checks += 1
        entropy_rows.append({
            "m": m,
            "h": h,
            "classes": expected,
            "minimum_bits": (expected - 1).bit_length(),
            "current_projection_values": 2,
        })


# Regression: current one-bit table aliases many sources that future edits separate.
alias_rows = []
for m in (4, 8, 16, 32, 64, 128):
    for h in sorted({1, min(2, m), min(4, m), min(8, m)}):
        e = class_count(m, h)
        alias_rows.append({
            "m": m,
            "h": h,
            "response_classes": e,
            "minimum_retained_bits": (e - 1).bit_length(),
            "one_bit_table_deficit": max(0, (e - 1).bit_length() - 1),
        })
        ck(e >= 2, "nontrivial aliases")


out = {
    "run": "ONEBIT-REUSE-ENTROPY-REFEREE190",
    "status": "PASS",
    "model": "fixed-length proper-3CNF one-bit projection; no source reread; at most h authenticated point updates",
    "symbolic_theorem": {
        "classes_h_lt_m": "1 + sum_{j=0}^h binom(m,j)",
        "classes_h_ge_m": "2^m",
        "current_projection_bits": 1,
        "interpretation": "summary value is not reusable authenticated state",
    },
    "finite_projection_sources": len(finite_sources),
    "finite_projection_dpll_queries": dpll_cases,
    "equal_length_groups": length_checks,
    "pairwise_distinguishability_checks": pair_checks,
    "assertions": ASSERT["total"],
    "finite_sources": finite_sources,
    "entropy_rows": entropy_rows,
    "alias_rows": alias_rows,
    "limitations": [
        "Restricted scalar-chain/lift family, not arbitrary SAT.",
        "Dynamic no-reread reuse is not a static decision-time lower bound.",
        "A writable or rereadable source escapes the retained-state premise at charged time.",
        "Finite DPLL checks are not native TM transition measurements or kernel proofs.",
        "No unconditional ordinary-SAT N^lambda child constructor is proved or refuted.",
    ],
}
print(json.dumps(out, indent=2, sort_keys=True))
