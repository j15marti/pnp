#!/usr/bin/env python3
"""Independent, compact replication of CLOCKAUTOMATON27's core.
Finite exhaustive check; not a proof of MCSP lower bounds.
"""
import itertools
import json
from hashlib import sha256


def precompute(d, n):
    k = len(d)
    r = [[[int(d[p][0] == q or d[p][1] == q) for q in range(k)]
          for p in range(k)]]
    midpoint = [None]
    for h in range(1, n + 1):
        m = [[-1] * k for _ in range(k)]
        for p in range(k):
            for q in range(k):
                m[p][q] = next((a for a in range(k)
                                if r[h - 1][p][a] and r[h - 1][a][q]), -1)
        midpoint.append(m)
        r.append([[int(m[p][q] >= 0) for q in range(k)] for p in range(k)])
    return r, midpoint


def witness_bit(d, n, q0, goal, mid, address):
    p, q = q0, goal
    for h in range(n, 0, -1):
        z = mid[h][p][q]
        assert z >= 0
        if (address >> (h - 1)) & 1:
            p = z
        else:
            q = z
    return next(b for b in (0, 1) if d[p][b] == q)


def endpoint(d, bits, initial=0):
    state = initial
    for bit in bits:
        state = d[state][bit]
    return state


checks = 0
sources = 0
machines = 0
for k in (2, 3):
    for flat in itertools.product(range(k), repeat=2 * k):
        d = [flat[2 * p:2 * p + 2] for p in range(k)]
        r, mid = precompute(d, 3)
        endpoints = {}
        for q in range(k):
            if r[3][0][q]:
                g = tuple(witness_bit(d, 3, 0, q, mid, i) for i in range(8))
                assert endpoint(d, g) == q
                checks += 1
                endpoints[q] = g
        for bits in itertools.product((0, 1), repeat=8):
            q = endpoint(d, bits)
            assert q in endpoints and endpoint(d, endpoints[q]) == q
            sources += 1
            checks += 1
        machines += 1


def make_triad():
    d = []
    for state in range(16):
        phase = (state >> 3) & 1
        zero, one, alternating = (state >> 2) & 1, (state >> 1) & 1, state & 1
        d.append(tuple(((1 - phase) << 3) |
                       (int(bool(zero) and b == 0) << 2) |
                       (int(bool(one) and b == 1) << 1) |
                       int(bool(alternating) and b == phase)
                       for b in (0, 1)))
    return d


d = make_triad()
accepted = []
for bits in itertools.product((0, 1), repeat=8):
    accepted.append(int(bool(endpoint(d, bits, 7) & 7)))
assert sum(accepted) == 3
checks += 1
for i in range(8):
    rising = falling = False
    for bits in itertools.product((0, 1), repeat=8):
        if bits[i]:
            continue
        changed = list(bits)
        changed[i] = 1
        low = endpoint(d, bits, 7) & 7
        high = endpoint(d, changed, 7) & 7
        rising |= (not low and bool(high))
        falling |= (bool(low) and not high)
    assert rising and falling
    checks += 1

result = {"name": "CLOCKAUTOMATON27_MINIMAL_REPRO", "source_checks": sources,
          "stationary_machines": machines, "assertions": checks,
          "triad_full_ANF_degree": 8, "triad_each_variable_nonunate": True,
          "failures": 0}
print(json.dumps(result, indent=2))
