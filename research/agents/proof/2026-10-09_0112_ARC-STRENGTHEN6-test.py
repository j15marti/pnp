#!/usr/bin/env python3
"""Finite checks for the type-correct nested guard and promise closure.

The symbolic proof is in the companion report.  This runner uses the repaired
DENSE-CNF1 signed-literal convention and a 24-second alarm.
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
    return 2 * lit - 1 if lit > 0 else -2 * lit


def encode(clauses, q=None) -> bytes:
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
        out.extend(p0(h, 2 * q + 2 * j + 1, 2 * q + 2 * j + 2))
    return tuple(out), 2 * q + 2 * m + 2


def proper_guard(source, q):
    """The inner guard with only its two binary clauses properly lifted."""
    m = len(source)
    h, r = q + 1, q + 2
    old_max = 2 * q + 2 * m + 2
    zp, zm = old_max + 1, old_max + 2
    out = list(source)
    out += [(h, -r, zp), (h, -r, -zp), (-h, r, zm), (-h, r, -zm)]
    for v in range(1, q + 1):
        out.extend(p0(h, v, q + 2 + v))
    for j in range(1, m + 1):
        out.extend(p0(h, 2 * q + 2 * j + 1, 2 * q + 2 * j + 2))
    return tuple(out), old_max + 2, h


def isolate(source, q):
    """Clause-isolation used by PROPER-AMPLIFIED-FALLBACK2."""
    out = []
    nxt = q
    for clause in source:
        clone_clause = []
        gadgets = []
        for lit in clause:
            y, z, w = nxt + 1, nxt + 2, nxt + 3
            nxt += 3
            x = abs(lit)
            clone_clause.append(y if lit > 0 else -y)
            gadgets += [(-x, y, z), (-x, y, -z),
                        (x, -y, w), (x, -y, -w)]
        out.append(tuple(clone_clause))
        out.extend(gadgets)
    return tuple(out), nxt


def mask_sizes(clauses):
    masks = {}
    for clause in clauses:
        order = tuple(sorted(abs(x) for x in clause))
        signs = tuple(next(x > 0 for x in clause if abs(x) == v) for v in order)
        masks.setdefault(order, set()).add(signs)
    return {len(v) for v in masks.values()}


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
    variables = {abs(x) for c in clauses for x in c}
    if not variables:
        return [tuple()]
    adj = {v: set() for v in variables}
    for c in clauses:
        vs = {abs(x) for x in c}
        for v in vs:
            adj[v].update(vs - {v})
    unseen, groups = set(variables), []
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
    return groups


def sign_balanced(clauses, q):
    signs = {v: set() for v in range(1, q + 1)}
    for c in clauses:
        for x in c:
            signs[abs(x)].add(x > 0)
    return all(s == {False, True} for s in signs.values())


def sources():
    base = [tuple(s[i] * (i + 1) for i in range(3))
            for s in itertools.product((-1, 1), repeat=3)]
    for mask in range(1, 64):
        yield tuple(base[i] for i in range(8) if mask >> i & 1), 3
    rng = random.Random(0xA6C2026)
    for _ in range(48):
        q = rng.randint(4, 9)
        cs = []
        for _ in range(rng.randint(1, 3 * q)):
            vs = rng.sample(range(1, q + 1), 3)
            cs.append(tuple(v if rng.getrandbits(1) else -v for v in vs))
        yield tuple(cs), q


def main():
    signal.alarm(24)
    start = time.monotonic()
    instances = pivots = raw_pairs = 0
    minimum_ratio = float("inf")
    digest = hashlib.sha256()
    minimal_trace = None
    isolated_instances = isolated_pivots = 0

    for source, q in sources():
        inner, qi, h = proper_guard(source, q)
        assert all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in inner)
        assert sign_balanced(inner, qi)
        blob = encode(inner, qi)
        digest.update(blob)
        nbits = 8 * len(blob)
        cap = math.floor(math.sqrt(nbits) * math.log2(nbits + 2))
        residuals = []
        for pivot in range(1, qi + 1):
            child, pairs = dp(inner, pivot)
            largest = max(8 * len(encode(c)) for c in components(child))
            assert largest > cap
            residuals.append(largest)
            minimum_ratio = min(minimum_ratio, largest / cap)
            raw_pairs += pairs
            pivots += 1

        outer, qo = guard(inner, qi)
        assert outer[:len(inner)] == inner
        assert qo == 2 * qi + 2 * len(inner) + 2
        digest.update(encode(outer, qo))
        if q == 3 and len(source) == 1 and minimal_trace is None:
            minimal_trace = {
                "inner_q": qi,
                "inner_clauses": len(inner),
                "inner_bits": nbits,
                "pivot_cap": cap,
                "largest_residual_bits_by_pivot": residuals,
                "outer_q": qo,
                "outer_clauses": len(outer),
                "outer_bits": 8 * len(encode(outer, qo)),
            }
        instances += 1

    # Clause isolation prevents an arbitrary source's full eight-pattern
    # triple from being mistaken for a stand-alone parity contradiction.
    sign_patterns = [tuple(s[i] * (i + 1) for i in range(3))
                     for s in itertools.product((-1, 1), repeat=3)]
    for count in (1, 2, 4, 8):
        isolated, qiso = isolate(tuple(sign_patterns[:count]), 3)
        transformed, qt, _ = proper_guard(isolated, qiso)
        assert all(len(c) == 3 and len({abs(x) for x in c}) == 3
                   for c in transformed)
        assert sign_balanced(transformed, qt)
        assert mask_sizes(transformed) <= {1, 2, 4}
        digest.update(encode(transformed, qt))
        isolated_instances += 1
        if count <= 2:
            nbits = 8 * len(encode(transformed, qt))
            cap = math.floor(math.sqrt(nbits) * math.log2(nbits + 2))
            for pivot in range(1, qt + 1):
                child, _ = dp(transformed, pivot)
                largest = max(8 * len(encode(c)) for c in components(child))
                assert largest > cap
                isolated_pivots += 1

    # Arithmetic used by the universal cap proof.
    for L in range(4, 200001):
        ell = 1 + int(math.log(5 * L + 4, 128))
        upper = 8 * (5 * L + 8 + (15 * L + 14) * ell)
        assert math.sqrt(upper) * math.log2(upper + 2) < 128 * (L - 1)

    assert [(x, zz(x), uleb(zz(x)).hex()) for x in (64, -64, 65, -65)] == [
        (64, 127, "7f"), (-64, 128, "8001"),
        (65, 129, "8101"), (-65, 130, "8201")]

    result = {
        "status": "PASS",
        "instances": instances,
        "pivot_evaluations": pivots,
        "raw_resolution_pairs_counted": raw_pairs,
        "minimum_max_child_to_cap_ratio": round(minimum_ratio, 6),
        "cap_arithmetic_L_max": 200000,
        "clause_isolated_instances": isolated_instances,
        "clause_isolated_pivots": isolated_pivots,
        "minimal_source_parameters_trace": minimal_trace,
        "aggregate_sha256": digest.hexdigest(),
        "elapsed_seconds": round(time.monotonic() - start, 6),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
