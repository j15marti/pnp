#!/usr/bin/env python3
"""Compact independent peer audit of SAT-INFORMATION-TRANSFER-CEILING173.
Finite proper-3CNF semantics and seven-step UNSAT proofs; no FLMV physical steps.
"""
from __future__ import annotations
import itertools
import json
import random


def quartet(l, a, b):
    return [(l, a, b), (l, a, -b), (l, -a, b), (l, -a, -b)]


def formula(u, v):
    k = len(u)
    left, right = [], []
    for i in range(k):
        z = i + 1
        a, b, c, d = [k + 4 * i + j for j in range(1, 5)]
        left += quartet(z if u[i] else -z, a, b)
        right += quartet(z if v[i] else -z, c, d)
    return tuple(left + right)


def dpll(cs, env=None):
    env = dict(env or {})
    while True:
        rest, singles = [], []
        for c in cs:
            if any(abs(l) in env and env[abs(l)] == (l > 0) for l in c):
                continue
            r = tuple(l for l in c if abs(l) not in env)
            if not r:
                return False
            rest.append(r)
            if len(r) == 1:
                singles.append(r[0])
        if not rest:
            return True
        changed = False
        for l in singles:
            key, value = abs(l), l > 0
            if key in env and env[key] != value:
                return False
            if key not in env:
                env[key] = value
                changed = True
        cs = rest
        if not changed:
            break
    x = min(abs(l) for c in cs for l in c if abs(l) not in env)
    return dpll(cs, {**env, x: False}) or dpll(cs, {**env, x: True})


def resolve(a, b, pivot):
    a, b = set(a), set(b)
    assert (pivot in a and -pivot in b) or (-pivot in a and pivot in b)
    result = frozenset((a | b) - {pivot, -pivot})
    assert all(-x not in result for x in result)
    return result


def certificate(cs, k, i):
    def unit(start):
        a, b, c, d = [frozenset(cs[start + j]) for j in range(4)]
        forced = set(a) & set(b) & set(c) & set(d)
        assert len(forced) == 1
        l = next(iter(forced))
        diff = next(abs(x) for x in a if -x in b)
        other = next(abs(x) for x in a if abs(x) not in (abs(l), diff))
        assert resolve(resolve(a, b, diff), resolve(c, d, diff), other) == frozenset([l])
        return frozenset([l])
    return resolve(unit(4 * i), unit(4 * k + 4 * i), i + 1) == frozenset()


def simplify(cs, pins):
    out = []
    for c in cs:
        if any(abs(l) in pins and pins[abs(l)] == (l > 0) for l in c):
            continue
        out.append(tuple(l for l in c if abs(l) not in pins))
    return out


def properize(cs):
    count = max((abs(l) for c in cs for l in c), default=0) + 1
    out = []
    for c in cs:
        if len(c) == 3:
            out.append(tuple(c))
        elif len(c) == 2:
            a = count
            count += 1
            out.extend((tuple(c) + (a,), tuple(c) + (-a,)))
        elif len(c) == 1:
            a, b = count, count + 1
            count += 2
            out.extend(tuple(c) + (x, y) for x, y in
                       ((a, b), (a, -b), (-a, b), (-a, -b)))
        elif len(c) == 0:
            a, b, d = count, count + 1, count + 2
            count += 3
            out.extend(itertools.product((a, -a), (b, -b), (d, -d)))
    return out


def run():
    rng = random.Random(20261025)
    n = sat = unsat = checks = certs = levels = 0
    for k in range(1, 5):
        rows = list(itertools.product((0, 1), repeat=k))
        for u in rows:
            for v in rows:
                cs = formula(u, v)
                expected = u == v
                assert len(cs) == 8 * k and len(set(cs)) == len(cs)
                assert all(len(c) == 3 and len({abs(x) for x in c}) == 3
                           for c in cs)
                assert dpll(cs) == expected
                checks += 3
                sat += expected
                unsat += not expected
                n += 1
                if not expected:
                    i = next(j for j in range(k) if u[j] != v[j])
                    assert certificate(cs, k, i)
                    certs += 1
                    checks += 1
                if k in (2, 3):
                    outcomes = []
                    for b1, b2 in itertools.product((False, True), repeat=2):
                        child = properize(simplify(cs, {1: b1}))
                        grand = properize(simplify(cs, {1: b1, 2: b2}))
                        assert all(len(c) == 3 and len(set(map(abs, c))) == 3
                                   for c in grand)
                        assert dpll(grand) == dpll(cs, {1: b1, 2: b2})
                        assert dpll(child) == dpll(cs, {1: b1})
                        outcomes.append(dpll(grand))
                        checks += 3
                    assert any(outcomes) == expected
                    checks += 1
                    levels += 1
    for k in (5, 8, 10):
        for label in (False, True):
            for _ in range(12):
                u = tuple(rng.randrange(2) for _ in range(k))
                v = list(u)
                if not label:
                    v[rng.randrange(k)] ^= 1
                v = tuple(v)
                cs = formula(u, v)
                assert dpll(cs) == label
                checks += 1
                if not label:
                    i = next(j for j in range(k) if u[j] != v[j])
                    assert certificate(cs, k, i)
                    certs += 1
                    checks += 1
                n += 1
                sat += label
                unsat += not label
    return {
        "run": "SAT-INPUT-CUT-CEILING173-PEER",
        "seed": 20261025,
        "sources": n,
        "sat": sat,
        "unsat": unsat,
        "seven_step_certificates": certs,
        "two_level_cases": levels,
        "assertion_groups": checks,
        "failures": 0,
        "model": "finite source bits and DPLL; not physical FLMV cost"
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
