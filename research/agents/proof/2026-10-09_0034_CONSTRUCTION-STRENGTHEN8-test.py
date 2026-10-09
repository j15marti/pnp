#!/usr/bin/env python3
"""Bounded audit of GUARD-STRIP-PIVOT2 under repaired DENSE-CNF1.

The symbolic theorem is in the companion report.  This runner checks exact
bytes, guard recognition, SAT preservation, the completed two-stage phase,
and a mixed affine/non-affine noncoverage family.  Alarm: 24 seconds.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import signal
import time

MAGIC = b"CNF1"


def uleb(x: int) -> bytes:
    out = bytearray()
    while True:
        b = x & 127
        x >>= 7
        out.append(b | (128 if x else 0))
        if not x:
            return bytes(out)


def zz(lit: int) -> int:
    assert lit
    return 2 * abs(lit) - (1 if lit > 0 else 0)


def encode(clauses, q=None) -> bytes:
    clauses = tuple(tuple(c) for c in clauses)
    if q is None:
        q = max((abs(x) for c in clauses for x in c), default=0)
    out = bytearray(MAGIC + uleb(q) + uleb(len(clauses)))
    for c in clauses:
        out += uleb(len(c))
        for lit in c:
            out += uleb(zz(lit))
    return bytes(out)


def p0(x: int, y: int, z: int):
    return ((x, y, -z), (x, -y, z), (-x, y, z), (-x, -y, -z))


def guard(source, q):
    source = tuple(tuple(c) for c in source)
    m = len(source)
    h, r = q + 1, q + 2
    out = list(source) + [(h, -r), (-h, r)]
    for v in range(1, q + 1):
        out.extend(p0(h, v, q + 2 + v))
    for j in range(1, m + 1):
        a = 2 * q + 2 * j + 1
        out.extend(p0(h, a, a + 1))
    return tuple(out), 2 * q + 2 * m + 2


def recognize_guard(clauses, qg):
    """Return (proper source, source q) iff this is the exact amplified grammar."""
    clauses = tuple(tuple(c) for c in clauses)
    c = len(clauses)
    if qg < 4 or qg % 2 or c < 7:
        return None
    L = (qg - 2) // 2
    m = c - 4 * L - 2
    q = L - m
    if q < 1 or m < 1 or 5 * m + 4 * q + 2 != c:
        return None
    src = clauses[:m]
    if any(len(d) != 3 or len({abs(x) for x in d}) != 3 for d in src):
        return None
    if any(abs(x) > q for d in src for x in d):
        return None
    if max(abs(x) for d in src for x in d) != q:
        return None
    h, r = q + 1, q + 2
    expected = [(h, -r), (-h, r)]
    for v in range(1, q + 1):
        expected.extend(p0(h, v, q + 2 + v))
    for j in range(1, m + 1):
        a = 2 * q + 2 * j + 1
        expected.extend(p0(h, a, a + 1))
    if clauses[m:] != tuple(expected):
        return None
    return src, q


def simplify(clauses, var, value):
    t, f = (var, -var) if value else (-var, var)
    out = []
    for c in clauses:
        if t in c:
            continue
        d = tuple(x for x in c if x != f)
        if not d:
            return None
        out.append(d)
    return tuple(out)


def sat(clauses):
    clauses = tuple(dict.fromkeys(tuple(c) for c in clauses))
    if not clauses:
        return True
    if any(not c for c in clauses):
        return False
    var = abs(min(clauses, key=len)[0])
    return any(ch is not None and sat(ch) for ch in
               (simplify(clauses, var, False), simplify(clauses, var, True)))


def dp(clauses, pivot):
    pos = [c for c in clauses if pivot in c]
    neg = [c for c in clauses if -pivot in c]
    keep = [c for c in clauses if pivot not in c and -pivot not in c]
    key = lambda c: tuple(sorted(c, key=lambda z: (abs(z), z < 0)))
    out = {key(c) for c in keep}
    raw = 0
    for a in pos:
        for b in neg:
            raw += 1
            r = (set(a) - {pivot}) | (set(b) - {-pivot})
            if any(-x in r for x in r):
                continue
            out.add(key(r))
    return tuple(sorted(out)), raw


def components(clauses):
    vs = {abs(x) for c in clauses for x in c}
    adj = {v: set() for v in vs}
    for c in clauses:
        w = {abs(x) for x in c}
        for v in w:
            adj[v].update(w - {v})
    ans, unseen = [], set(vs)
    while unseen:
        root = next(iter(unseen))
        stack, seen = [root], {root}
        while stack:
            for w in adj[stack.pop()]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        unseen -= seen
        ans.append(tuple(c for c in clauses if any(abs(x) in seen for x in c)))
    return ans or [tuple()]


def caps(nbits):
    return (math.floor(nbits ** 0.5 * math.log2(nbits + 2)),
            math.floor(nbits ** 1.1 * math.log2(nbits + 2) ** 2))


def pivot_plan(source, q):
    nbits = 8 * len(encode(source, q))
    B, V = caps(nbits)
    for pivot in range(1, q + 1):
        residual, raw = dp(source, pivot)
        kids = components(residual)
        sizes = [8 * len(encode(k)) for k in kids]
        if max(sizes, default=0) <= B and sum(sizes) <= V and all(s < nbits for s in sizes):
            return pivot, kids, sizes, raw
    return None


def proper_pivot_family(k):
    """Connected proper 3CNF; eliminating variable 1 yields k tiny components."""
    out = []
    for i in range(k):
        a, b, c, d = 2 + 4 * i, 3 + 4 * i, 4 + 4 * i, 5 + 4 * i
        out.extend(((1, a, b), (-a, b, c), (-a, b, -c),
                    (a, -b, d), (a, -b, -d)))
    return tuple(out), 1 + 4 * k


def lifted_cross(k):
    """Proper lift of (x or a_i) and (not x or b_i)."""
    out = []
    next_v = 2 * k + 2
    for i in range(k):
        a = 2 + i
        z = next_v + i
        out.extend(((1, a, z), (1, a, -z)))
    next_v += k
    for i in range(k):
        b = 2 + k + i
        z = next_v + i
        out.extend(((-1, b, z), (-1, b, -z)))
    return tuple(out), 4 * k + 1


def main():
    signal.alarm(24)
    started = time.monotonic()
    digest = hashlib.sha256()
    accepted = semantic = mutations = executed = child_bits = 0
    accepted_rows = []

    for k in (2, 3):
        f, q = proper_pivot_family(k)
        g, qg = guard(f, q)
        assert recognize_guard(g, qg) == (f, q)
        assert sat(f) == sat(g)
        semantic += 1

    for k in (4, 8, 16, 32, 64, 128, 256):
        f, q = proper_pivot_family(k)
        g, qg = guard(f, q)
        parsed = recognize_guard(g, qg)
        assert parsed == (f, q)
        plan = pivot_plan(*parsed)
        assert plan is not None and plan[0] == 1
        _, kids, sizes, raw = plan
        N, M = 8 * len(encode(g, qg)), 8 * len(encode(f, q))
        B, V = caps(N)
        assert max(sizes) <= B and sum(sizes) <= V
        assert len(kids) == k
        accepted += 1
        executed += len(kids)
        child_bits += sum(sizes)
        data = encode(g, qg)
        digest.update(data)
        accepted_rows.append({
            "k": k, "parent_bits": N, "stripped_source_bits": M,
            "internal_ratio": round(M / N, 6),
            "internal_exponent": round(math.log(M, N), 6),
            "children": len(kids), "max_child_bits": max(sizes),
            "aggregate_child_bits": sum(sizes), "parent_cap_bits": B,
            "raw_pairs_at_selected_pivot": raw,
        })

        # Exact grammar must reject local corruption, truncation, and bad header.
        variants = [g[:-1], g + ((qg + 1,),), tuple(reversed(g)),
                    g[:len(f)] + ((q + 1, q + 2),) + g[len(f) + 1:]]
        for bad in variants:
            assert recognize_guard(bad, qg) is None
            mutations += 1
        assert recognize_guard(g, qg + 2) is None
        mutations += 1

    hostile_rows = []
    for k in (1, 2, 4, 8, 16, 32, 64, 128):
        f, q = lifted_cross(k)
        g, qg = guard(f, q)
        assert recognize_guard(g, qg) == (f, q)
        plan = pivot_plan(f, q)
        N = 8 * len(encode(g, qg))
        source_bits = 8 * len(encode(f, q))
        # The typed double phase declines: stripping alone is not a boundary.
        assert plan is None
        hostile_rows.append({"k": k, "parent_bits": N,
                             "source_bits": source_bits,
                             "strip_exponent": round(math.log(source_bits, N), 6)})
        digest.update(encode(g, qg))

    result = {
        "status": "PASS",
        "proof_status": "COMPUTATIONAL corroboration only",
        "encoding": "DENSE-CNF1 positive-odd/negative-even zigzag",
        "accepted_guarded_instances": accepted,
        "semantic_equivalences_bruteforced": semantic,
        "grammar_mutations_rejected": mutations,
        "executed_children_with_multiplicity": executed,
        "aggregate_executed_child_bits": child_bits,
        "accepted_rows": accepted_rows,
        "hostile_mixed_rows": hostile_rows,
        "aggregate_sha256": digest.hexdigest(),
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "limitations": "Finite checks do not prove the symbolic composition theorem, all-input coverage, or machine-space bound.",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
