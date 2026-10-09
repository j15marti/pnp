#!/usr/bin/env python3
"""Independent bounded audit of ARC-STRENGTHEN5.

Checks the repaired positive-odd/negative-even DENSE-CNF1 serializer, the
amplified guard semantics, every one-pivot largest-child cap on a finite
corpus, and the closed-form cap inequality.  Finite results are
COMPUTATIONAL; the accompanying report supplies the symbolic proof.
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
        b = x & 127
        x >>= 7
        out.append(b | (128 if x else 0))
        if not x:
            return bytes(out)


def zz(lit: int) -> int:
    """Repository convention: positive odd, negative even."""
    assert lit
    return 2 * abs(lit) - (1 if lit > 0 else 0)


def retired_zz(lit: int) -> int:
    """The opposite convention accidentally used by ARC5's runner."""
    return 2 * lit if lit > 0 else -2 * lit - 1


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


def p0(x, y, z):
    return ((x, y, -z), (x, -y, z), (-x, y, z), (-x, -y, -z))


def guard(source, q):
    m = len(source)
    h, r = q + 1, q + 2
    out = list(source) + [(h, -r), (-h, r)]
    for v in range(1, q + 1):
        out.extend(p0(h, v, q + 2 + v))
    for j in range(1, m + 1):
        a = 2 * q + 2 * j + 1
        out.extend(p0(h, a, a + 1))
    return tuple(out), 2 * q + 2 * m + 2, h


def simplify(clauses, var, value):
    true_lit, false_lit = (var, -var) if value else (-var, var)
    out = []
    for c in clauses:
        if true_lit in c:
            continue
        d = tuple(x for x in c if x != false_lit)
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
    for value in (False, True):
        child = simplify(clauses, var, value)
        if child is not None and sat(child):
            return True
    return False


def dp(clauses, pivot):
    pos = [c for c in clauses if pivot in c]
    neg = [c for c in clauses if -pivot in c]
    keep = [c for c in clauses if pivot not in c and -pivot not in c]
    key = lambda c: tuple(sorted(c, key=lambda z: (abs(z), z < 0)))
    out = {key(c) for c in keep}
    for a in pos:
        aa = set(a) - {pivot}
        for b in neg:
            resolvent = aa | (set(b) - {-pivot})
            if any(-x in resolvent for x in resolvent):
                continue
            out.add(key(resolvent))
    return tuple(sorted(out)), len(pos) * len(neg)


def components(clauses):
    variables = {abs(x) for c in clauses for x in c}
    adjacency = {v: set() for v in variables}
    for c in clauses:
        vs = {abs(x) for x in c}
        for v in vs:
            adjacency[v].update(vs - {v})
    groups, unseen = [], set(variables)
    while unseen:
        root = next(iter(unseen))
        stack, seen = [root], {root}
        while stack:
            for w in adjacency[stack.pop()]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        unseen -= seen
        groups.append(tuple(c for c in clauses if any(abs(x) in seen for x in c)))
    return groups or [tuple()]


def corpus():
    base = [tuple(s[i] * (i + 1) for i in range(3))
            for s in itertools.product((-1, 1), repeat=3)]
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


def cap_ratio_upper(L):
    U = 160 * L * math.log2(L)
    return math.sqrt(U) * math.log2(161 * L * math.log2(L)) / (128 * (L - 1))


def properize_block(clause, fresh=(4, 5, 6)):
    """Five proper clauses equivalent after existentially quantifying fresh vars."""
    a, b, c = fresh
    signs = {}
    tautology = False
    for lit in clause:
        v = abs(lit)
        s = lit > 0
        if v in signs and signs[v] != s:
            tautology = True
        signs[v] = s
    filler = (a, b, c)
    if tautology:
        return (filler,) * 5
    simple = tuple((v if s else -v) for v, s in sorted(signs.items()))
    if len(simple) == 3:
        return (simple,) + (filler,) * 4
    if len(simple) == 2:
        x, y = simple
        return ((x, y, a), (x, y, -a)) + (filler,) * 3
    assert len(simple) == 1
    x = simple[0]
    return ((x, a, b), (x, a, -b), (x, -a, b), (x, -a, -b), filler)


def clause_value(clause, assignment):
    return any(assignment[abs(x)] == (x > 0) for x in clause)


def properization_audit():
    checks = 0
    literals = (-3, -2, -1, 1, 2, 3)
    for clause in itertools.product(literals, repeat=3):
        block = properize_block(clause)
        assert len(block) == 5
        assert all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in block)
        for source_bits in itertools.product((False, True), repeat=3):
            source_assignment = dict(zip((1, 2, 3), source_bits))
            lhs = clause_value(clause, source_assignment)
            rhs = False
            for fresh_bits in itertools.product((False, True), repeat=3):
                assignment = source_assignment | dict(zip((4, 5, 6), fresh_bits))
                rhs |= all(clause_value(c, assignment) for c in block)
            assert lhs == rhs
            checks += 1
    return checks


def main():
    signal.alarm(24)
    started = time.monotonic()

    boundary = [(x, zz(x), uleb(zz(x)).hex()) for x in (64, -64, 65, -65)]
    expected = [(64, 127, "7f"), (-64, 128, "8001"),
                (65, 129, "8101"), (-65, 130, "8201")]
    assert boundary == expected
    retired_boundary = [(x, retired_zz(x), uleb(retired_zz(x)).hex())
                        for x in (64, -64, 65, -65)]
    assert retired_boundary != expected
    properization_checks = properization_audit()

    instances = pivots = raw_pairs = encoded_bits = 0
    min_child_ratio = float("inf")
    digest = hashlib.sha256()
    for source, q in corpus():
        g, qg, _ = guard(source, q)
        data = encode(g, qg)
        N = 8 * len(data)
        digest.update(data)
        encoded_bits += N
        instances += 1
        assert sat(source) == sat(g)
        B = math.floor(N ** 0.5 * math.log2(N + 2))
        for pivot in range(1, qg + 1):
            child, raw = dp(g, pivot)
            max_child = max(8 * len(encode(c)) for c in components(child))
            assert max_child > B
            min_child_ratio = min(min_child_ratio, max_child / B)
            pivots += 1
            raw_pairs += raw

    # Exhaust a large deterministic prefix of the universal closed-form cap.
    max_cap_ratio = 0.0
    cap_argmax = None
    for L in range(4, 200_001):
        ratio = cap_ratio_upper(L)
        if ratio > max_cap_ratio:
            max_cap_ratio, cap_argmax = ratio, L
        assert ratio < 1
    assert cap_argmax == 4

    c = 1201 / 1000
    d = 0.5 * ((c + 2) / c**2 - c)
    assert 1.2 < c and 0.5 < d

    result = {
        "status": "PASS",
        "seed": "0xa5c2026",
        "instances": instances,
        "pivot_evaluations": pivots,
        "raw_pairs_counted": raw_pairs,
        "encoded_bits_hashed": encoded_bits,
        "minimum_max_child_to_B_ratio": round(min_child_ratio, 6),
        "correct_boundary": boundary,
        "retired_boundary": retired_boundary,
        "properization_assignment_checks": properization_checks,
        "cap_L_checked_through": 200000,
        "maximum_closed_form_cap_ratio": round(max_cap_ratio, 12),
        "cap_ratio_argmax": cap_argmax,
        "aggregate_sha256": digest.hexdigest(),
        "flmv_c": c,
        "flmv_d_c": d,
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "limitations": "Finite checks do not prove the universal theorem or machine-space bound.",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
