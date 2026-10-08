#!/usr/bin/env python3
"""Bounded audit for aggregate closure, guarded portfolio residue, and PRF3 wedge."""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import signal
import time
from fractions import Fraction
from pathlib import Path

signal.alarm(25)
START = time.time()


def uleb(u: int) -> bytes:
    assert u >= 0
    out = bytearray()
    while True:
        b = u & 0x7F
        u >>= 7
        out.append(b | (0x80 if u else 0))
        if not u:
            return bytes(out)


def zigzag(lit: int) -> int:
    # Repaired DENSE-CNF1 convention: positive odd, negative even.
    return 2 * lit - 1 if lit > 0 else -2 * lit


def normalize(cnf):
    out = set()
    for clause in cnf:
        c = frozenset(clause)
        if any(-x in c for x in c):
            continue
        out.add(c)
    # exact subsumption is safe and makes the size test hostile to the claim
    return tuple(sorted((c for c in out if not any(d < c for d in out)),
                        key=lambda c: (len(c), tuple(sorted(c)))))


def cnf1(cnf) -> bytes:
    f = normalize(cnf)
    maxvar = max((abs(x) for c in f for x in c), default=0)
    out = bytearray(b"CNF1") + bytearray(uleb(maxvar)) + bytearray(uleb(len(f)))
    for c in f:
        lits = sorted(c, key=lambda z: (abs(z), z < 0))
        out += uleb(len(lits))
        for lit in lits:
            out += uleb(zigzag(lit))
    return bytes(out)


def parity0(a, b, c):
    # even parity a xor b xor c = 0
    return [(-a, -b, -c), (-a, b, c), (a, -b, c), (a, b, -c)]


def guarded(n: int):
    # F_n is a satisfiable cyclic proper 3-CNF on densely named variables.
    src = []
    for i in range(n):
        src.append((i + 1, (i + 1) % n + 1, (i + 2) % n + 1))
    h, r = n + 1, n + 2
    clauses = list(src) + [(h, -r), (-h, r)]
    for v in range(1, n + 1):
        clauses += parity0(h, v, n + 2 + v)
    return normalize(clauses), h, r


def dp(cnf, pivot):
    f = normalize(cnf)
    pos = [c for c in f if pivot in c]
    neg = [c for c in f if -pivot in c]
    keep = [c for c in f if pivot not in c and -pivot not in c]
    raw_pairs = len(pos) * len(neg)
    for a in pos:
        for b in neg:
            keep.append(tuple((a - {pivot}) | (b - {-pivot})))
    return normalize(keep), raw_pairs


def components(cnf):
    f = normalize(cnf)
    vars_ = sorted({abs(x) for c in f for x in c})
    adj = {v: set() for v in vars_}
    for c in f:
        vs = [abs(x) for x in c]
        for a in vs:
            adj[a].update(v for v in vs if v != a)
    seen, comps = set(), []
    for root in vars_:
        if root in seen:
            continue
        stack, block = [root], set()
        while stack:
            v = stack.pop()
            if v in block:
                continue
            block.add(v)
            stack.extend(adj[v] - block)
        seen |= block
        comps.append(normalize(c for c in f if any(abs(x) in block for x in c)))
    if any(len(c) == 0 for c in f):
        comps.append((frozenset(),))
    return comps


def residual(cnf, assignment):
    out = []
    for c in cnf:
        if any(assignment.get(abs(x)) == (x > 0) for x in c if abs(x) in assignment):
            continue
        out.append(tuple(x for x in c if abs(x) not in assignment))
    return normalize(out)


def horn(cnf):
    return all(sum(x > 0 for x in c) <= 1 for c in cnf)


def has_small_strong_horn_backdoor(cnf, k=2):
    vars_ = sorted({abs(x) for c in cnf for x in c})
    for size in range(k + 1):
        for subset in itertools.combinations(vars_, size):
            if all(horn(residual(cnf, dict(zip(subset, bits))))
                   for bits in itertools.product([False, True], repeat=size)):
                return True
    return False


def connected(cnf):
    return len(components(cnf)) == 1


def aggregate_fixed_point(r, v, h):
    return max(Fraction(1), r, (v - h) / (1 - h))


checks = 0
target = {
    "r": Fraction(6, 5), "v": Fraction(11, 10),
    "h": Fraction(1, 2), "p": Fraction(1, 2),
}
assert aggregate_fixed_point(target["r"], target["v"], target["h"]) == Fraction(6, 5)
checks += 1

# Compare the closed form against monotone exponent iteration on a rational grid.
grid = []
for h_num in range(1, 10):
    h = Fraction(h_num, 10)
    for v_num in range(5, 16):
        v = Fraction(v_num, 10)
        r = Fraction(1 + (v_num % 4), 4) + 1
        c = Fraction(1)
        for _ in range(300):
            c = max(r, v - h + h * c)
        want = aggregate_fixed_point(r, v, h)
        assert abs(float(c - want)) < 1e-10
        grid.append((str(r), str(v), str(h), str(want)))
        checks += 1

guard_rows = []
for n in [5, 6, 8, 12, 16, 24, 32, 48, 64]:
    f, hub, _ = guarded(n)
    N = 8 * len(cnf1(f))
    B = math.floor(math.sqrt(N) * math.log2(N + 2))
    A = math.floor((N ** 1.2) * (math.log2(N + 2) ** 2))
    small_pivots = []
    for pivot in range(1, n + 1):
        q, pairs = dp(f, pivot)
        max_child = max((8 * len(cnf1(comp)) for comp in components(q)), default=0)
        small_pivots.append((pivot, max_child, pairs))
        assert max_child > B
        checks += 1
    _, hub_pairs = dp(f, hub)
    assert hub_pairs >= 4 * n * n
    checks += 1
    guard_rows.append({
        "n": n, "encoded_bits": N, "child_cap_bits": B,
        "local_cap_proxy": A, "min_source_pivot_max_child": min(x[1] for x in small_pivots),
        "hub_raw_pairs": hub_pairs,
    })

# Directly check Construction5 portfolio guards on bounded members.
portfolio = []
for n in range(3, 9):
    f, _, _ = guarded(n)
    vars_ = {abs(x) for c in f for x in c}
    pure = any(not ({v, -v} <= {x for c in f for x in c}) for v in vars_)
    row = {
        "n": n,
        "no_units": all(len(c) != 1 for c in f),
        "no_pure": not pure,
        "not_2cnf": any(len(c) > 2 for c in f),
        "connected": connected(f),
        "non_horn": not horn(f),
        "no_strong_horn_backdoor_le_2": not has_small_strong_horn_backdoor(f, 2),
        "binary_clause_blocks_parity_star_scanner": any(len(c) == 2 for c in f),
    }
    assert all(v for k, v in row.items() if k != "n")
    checks += 7
    portfolio.append(row)

# PRF3 position-block certificate wedge.
eta, theta, C = Fraction(3, 5), Fraction(1, 2), Fraction(6, 5)
naive_access_exp = eta + theta * C
max_access_exp = Fraction(6, 5) - Fraction(1, 2)
assert naive_access_exp == Fraction(6, 5)
assert max_access_exp == Fraction(7, 10)
assert naive_access_exp - max_access_exp == Fraction(1, 2)
checks += 3
feasible_deltas = []
for k in range(101):
    delta = Fraction(k, 100)
    if 1 - delta <= Fraction(1, 2) and naive_access_exp + delta <= Fraction(6, 5):
        feasible_deltas.append(str(delta))
assert not feasible_deltas
checks += 1

payload = {
    "status": "PASS",
    "checks": checks,
    "aggregate_target_fixed_point": "6/5",
    "aggregate_grid_cases": len(grid),
    "guard_rows": guard_rows,
    "portfolio_rows": portfolio,
    "position_block_wedge": {
        "space_forces_delta_at_least": "1/2",
        "max_certifiable_access_exponent": "7/10",
        "naive_saturated_edge_access_exponent": "6/5",
        "required_access_exponent_saving": "1/2",
        "feasible_grid_deltas": feasible_deltas,
    },
    "elapsed_seconds": round(time.time() - START, 6),
}
digest_body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
payload["sha256_without_digest"] = hashlib.sha256(digest_body).hexdigest()
out = Path(__file__).with_name("2026-10-08_2349_RECOVERY-STRENGTHEN7-results.json")
out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
print(json.dumps(payload, indent=2, sort_keys=True))
