#!/usr/bin/env python3
"""Bounded checks for the clause-amplified fallback guard.

This runner is finite evidence only.  The report contains the asymptotic
proof and the same-machine achievable-region argument.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import random
import signal
import time

MAGIC = b"CNF1"


def uleb(x: int) -> bytes:
    out = bytearray()
    while True:
        y = x & 127
        x >>= 7
        out.append(y | (128 if x else 0))
        if not x:
            return bytes(out)


def zz(lit: int) -> int:
    return 2 * lit if lit > 0 else -2 * lit - 1


def encode(clauses: tuple[tuple[int, ...], ...], q: int | None = None) -> bytes:
    if q is None:
        q = max((abs(x) for c in clauses for x in c), default=0)
    out = bytearray(MAGIC + uleb(q) + uleb(len(clauses)))
    for c in clauses:
        out += uleb(len(c))
        for lit in c:
            out += uleb(zz(lit))
    return bytes(out)


def p0(x: int, y: int, z: int) -> tuple[tuple[int, ...], ...]:
    # Four clauses for x xor y xor z = 0.
    return ((x, y, -z), (x, -y, z), (-x, y, z), (-x, -y, -z))


def guard(source: tuple[tuple[int, ...], ...], q: int):
    m = len(source)
    h, r = q + 1, q + 2
    clauses = list(source) + [(h, -r), (-h, r)]
    for v in range(1, q + 1):
        clauses.extend(p0(h, v, q + 2 + v))
    for j in range(1, m + 1):
        a = 2 * q + 2 * j + 1
        b = a + 1
        clauses.extend(p0(h, a, b))
    return tuple(clauses), 2 * q + 2 * m + 2, h


def simplify(clauses, var, value):
    good, bad = (var, -var) if value else (-var, var)
    out = []
    for c in clauses:
        if good in c:
            continue
        d = tuple(x for x in c if x != bad)
        if not d:
            return None
        out.append(d)
    return tuple(out)


def sat(clauses):
    clauses = tuple(dict.fromkeys(clauses))
    if not clauses:
        return True
    if any(not c for c in clauses):
        return False
    var = abs(min(clauses, key=len)[0])
    for value in (False, True):
        child = simplify(clauses, var, value)
        if child is not None and sat(child):
            return True
    return False


def restrict(clauses, assignment):
    out = []
    for c in clauses:
        if any(assignment.get(abs(x)) == (x > 0) for x in c if abs(x) in assignment):
            continue
        d = tuple(x for x in c if abs(x) not in assignment)
        if not d:
            return ((),)
        out.append(d)
    return tuple(out)


def is_horn(clauses):
    return all(sum(x > 0 for x in c) <= 1 for c in clauses)


def has_small_strong_horn_backdoor(clauses, variables, limit=2):
    for size in range(limit + 1):
        for backdoor in itertools.combinations(variables, size):
            if all(
                is_horn(restrict(clauses, dict(zip(backdoor, bits))))
                for bits in itertools.product((False, True), repeat=size)
            ):
                return True
    return False


def dp(clauses, pivot):
    pos = [c for c in clauses if pivot in c]
    neg = [c for c in clauses if -pivot in c]
    keep = [c for c in clauses if pivot not in c and -pivot not in c]
    out = {tuple(sorted(c, key=lambda z: (abs(z), z < 0))) for c in keep}
    for a in pos:
        aa = set(a) - {pivot}
        for b in neg:
            rr = aa | (set(b) - {-pivot})
            if any(-x in rr for x in rr):
                continue
            out.add(tuple(sorted(rr, key=lambda z: (abs(z), z < 0))))
    return tuple(sorted(out)), len(pos) * len(neg)


def components(clauses):
    vars_ = {abs(x) for c in clauses for x in c}
    adj = {v: set() for v in vars_}
    for c in clauses:
        vs = {abs(x) for x in c}
        for v in vs:
            adj[v].update(vs - {v})
    groups = []
    unseen = set(vars_)
    while unseen:
        root = next(iter(unseen))
        stack, seen = [root], {root}
        while stack:
            for w in adj[stack.pop()]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        unseen -= seen
        groups.append(tuple(c for c in clauses if any(abs(x) in seen for x in c)))
    return groups or [tuple()]


def source_corpus():
    base = []
    for signs in itertools.product((-1, 1), repeat=3):
        base.append(tuple(signs[i] * (i + 1) for i in range(3)))
    for mask in range(1, 256):
        yield tuple(base[i] for i in range(8) if mask >> i & 1), 3
    rng = random.Random(0xA5C2026)
    for _ in range(80):
        q = rng.randint(4, 7)
        clauses = []
        for _ in range(rng.randint(q, 3 * q)):
            vs = rng.sample(range(1, q + 1), 3)
            clauses.append(tuple(v if rng.getrandbits(1) else -v for v in vs))
        yield tuple(clauses), q


def main():
    signal.alarm(24)
    start = time.monotonic()
    instances = semantic = legacy = pivots = 0
    raw_pairs = 0
    total_bits = 0
    digest = hashlib.sha256()
    min_ratio = float("inf")

    for source, q in source_corpus():
        g, qg, h = guard(source, q)
        blob = encode(g, qg)
        nbits = 8 * len(blob)
        digest.update(blob)
        instances += 1
        total_bits += nbits

        assert sat(source) == sat(g)
        semantic += 1
        signs = {v: set() for v in range(1, qg + 1)}
        for c in g:
            for x in c:
                signs[abs(x)].add(x > 0)
        assert all(x == {False, True} for x in signs.values())
        assert any(len(c) == 2 for c in g)
        assert not is_horn(g) and any(len(c) > 2 for c in g)
        assert len(components(g)) == 1
        assert not has_small_strong_horn_backdoor(g, tuple(range(1, qg + 1)))
        legacy += 1

        B = math.floor(nbits ** 0.5 * math.log2(nbits + 2))
        for v in range(1, qg + 1):
            child, raw = dp(g, v)
            cs = components(child)
            max_bits = max(8 * len(encode(c)) for c in cs)
            assert max_bits > B
            min_ratio = min(min_ratio, max_bits / B)
            raw_pairs += raw
            pivots += 1

    boundary = [(x, zz(x), uleb(zz(x)).hex()) for x in (64, -64, 65, -65)]
    assert boundary == [(64, 128, "8001"), (-64, 127, "7f"),
                        (65, 130, "8201"), (-65, 129, "8101")]

    c = 1201 / 1000
    d = 0.5 * ((c + 2) / (c * c) - c)
    assert 1.2 < c and 0.5 < d
    result = {
        "status": "PASS",
        "instances": instances,
        "semantic_equivalences": semantic,
        "legacy_portfolio_rejections": legacy,
        "pivot_evaluations": pivots,
        "raw_pairs_counted": raw_pairs,
        "minimum_max_child_to_B_ratio": round(min_ratio, 6),
        "encoded_bits_hashed": total_bits,
        "aggregate_sha256": digest.hexdigest(),
        "flmv_c": c,
        "flmv_d_c": d,
        "elapsed_seconds": round(time.monotonic() - start, 6),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
