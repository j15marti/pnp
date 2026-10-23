#!/usr/bin/env python3
"""Deterministic audit for EXCEPTION-KERNEL94.

The domain is Z_3.  Affine edges impose x_v=x_u+b (mod 3); exception
edges carry arbitrary 3x3 binary relations.  The audit compares the charged
contraction/vertex-cover solver against exhaustive search.
"""

from __future__ import annotations

import itertools
import json
import random
from collections import defaultdict, deque

SEED = 202610231648
RNG = random.Random(SEED)
assertions = 0


def check(cond, msg="audit assertion failed"):
    global assertions
    assertions += 1
    if not cond:
        raise AssertionError(msg)


def brute(n, affine, exceptions):
    for x in itertools.product(range(3), repeat=n):
        if all(x[v] == (x[u] + b) % 3 for u, v, b in affine) and all(
            (x[u], x[v]) in rel for u, v, rel in exceptions
        ):
            return True
    return False


def contract(n, affine, exceptions):
    adj = [[] for _ in range(n)]
    for u, v, b in affine:
        adj[u].append((v, b % 3))
        adj[v].append((u, (-b) % 3))
    comp = [-1] * n
    pot = [0] * n
    roots = []
    for s in range(n):
        if comp[s] != -1:
            continue
        cid = len(roots)
        roots.append(s)
        comp[s] = cid
        q = deque([s])
        while q:
            u = q.popleft()
            for v, b in adj[u]:
                want = (pot[u] + b) % 3
                if comp[v] == -1:
                    comp[v] = cid
                    pot[v] = want
                    q.append(v)
                elif comp[v] != cid or pot[v] != want:
                    return None

    domains = [set(range(3)) for _ in roots]
    qedges = []
    for u, v, rel in exceptions:
        cu, cv = comp[u], comp[v]
        transformed = {
            (a, b)
            for a in range(3)
            for b in range(3)
            if ((a + pot[u]) % 3, (b + pot[v]) % 3) in rel
        }
        if not transformed:
            return None
        if cu == cv:
            domains[cu] &= {a for a in range(3) if (a, a) in transformed}
        else:
            qedges.append((cu, cv, transformed))
    if any(not d for d in domains):
        return None
    return comp, pot, domains, qedges


def kernel_solve(n, affine, exceptions):
    data = contract(n, affine, exceptions)
    if data is None:
        return False, {"roots": 0, "nonisolated": 0, "cover": 0, "leaves": 0}
    comp, pot, domains, qedges = data
    incident = defaultdict(list)
    cover = set()
    touched = set()
    for idx, (u, v, rel) in enumerate(qedges):
        touched.update((u, v))
        cover.add(u)  # one endpoint per edge is a valid cover
        incident[u].append((idx, True))
        incident[v].append((idx, False))
    cover = sorted(cover)
    outside = sorted(touched - set(cover))
    leaves = 0
    for vals in itertools.product(range(3), repeat=len(cover)):
        leaves += 1
        a = dict(zip(cover, vals))
        if any(a[u] not in domains[u] for u in cover):
            continue
        ok = True
        for u, v, rel in qedges:
            if u in a and v in a and (a[u], a[v]) not in rel:
                ok = False
                break
        if not ok:
            continue
        for z in outside:
            feasible = False
            for color in domains[z]:
                good = True
                for idx, z_is_left in incident[z]:
                    u, v, rel = qedges[idx]
                    pair = (color, a[v]) if z_is_left else (a[u], color)
                    if pair not in rel:
                        good = False
                        break
                if good:
                    feasible = True
                    break
            if not feasible:
                ok = False
                break
        if ok:
            return True, {
                "roots": len(domains),
                "nonisolated": len(touched),
                "cover": len(cover),
                "leaves": leaves,
            }
    return False, {
        "roots": len(domains),
        "nonisolated": len(touched),
        "cover": len(cover),
        "leaves": leaves,
    }


def random_relation():
    return {(a, b) for a in range(3) for b in range(3) if RNG.randrange(2)}


stats = {
    "seed": SEED,
    "random_instances": 0,
    "sat_instances": 0,
    "unsat_instances": 0,
    "max_exception_edges": 0,
    "max_nonisolated_roots": 0,
    "max_cover": 0,
    "query_family_sizes": [],
}

# Random mixed affine/exception CSPs, including loops after contraction.
for n in range(1, 8):
    for _ in range(260):
        affine = []
        for u in range(n):
            for v in range(u + 1, n):
                if RNG.random() < 0.18:
                    affine.append((u, v, RNG.randrange(3)))
        p = RNG.randrange(0, min(5, n * (n + 1) // 2 + 1))
        exceptions = []
        for _j in range(p):
            u = RNG.randrange(n)
            v = RNG.randrange(n)
            while n > 1 and v == u:
                v = RNG.randrange(n)
            exceptions.append((u, v, random_relation()))
        want = brute(n, affine, exceptions)
        got, meta = kernel_solve(n, affine, exceptions)
        check(got == want, (n, affine, exceptions, want, got))
        check(meta["nonisolated"] <= 2 * p)
        check(meta["cover"] <= p)
        check(meta["leaves"] <= 3 ** meta["cover"])
        stats["random_instances"] += 1
        stats["sat_instances"] += int(want)
        stats["unsat_instances"] += int(not want)
        stats["max_exception_edges"] = max(stats["max_exception_edges"], p)
        stats["max_nonisolated_roots"] = max(
            stats["max_nonisolated_roots"], meta["nonisolated"]
        )
        stats["max_cover"] = max(stats["max_cover"], meta["cover"])

# Explicit controls: inconsistent holonomy, inequality/K4, and same-component edge.
got, _ = kernel_solve(3, [(0, 1, 0), (1, 2, 0), (2, 0, 1)], [])
check(not got)

neq = {(a, b) for a in range(3) for b in range(3) if a != b}
k4 = [(u, v, neq) for u in range(4) for v in range(u + 1, 4)]
got, meta = kernel_solve(4, [], k4)
check(not got)
check(meta["cover"] <= len(k4))

eq0 = {(a, b) for a in range(3) for b in range(3) if a == b}
got, _ = kernel_solve(2, [(0, 1, 1)], [(0, 1, eq0)])
check(not got)

# Exact p-field query family: each disjoint relation is either {(0,0)} or empty.
# SAT iff every control bit is one; flipping any unread bit changes the label.
for p in [1, 2, 3, 4, 8, 16, 32, 64]:
    bits = [1] * p
    exceptions = [
        (2 * i, 2 * i + 1, {(0, 0)} if bits[i] else set()) for i in range(p)
    ]
    got, meta = kernel_solve(2 * p, [], exceptions)
    check(got)
    check(meta["nonisolated"] == 2 * p)
    check(meta["cover"] == p)
    for j in range(p):
        bad = list(exceptions)
        bad[j] = (2 * j, 2 * j + 1, set())
        bad_got, _ = kernel_solve(2 * p, [], bad)
        check(not bad_got)
    stats["query_family_sizes"].append(p)

stats["assertions"] = assertions
stats["failures"] = 0
stats["status"] = "COMPUTATIONAL; finite audit only"
print(json.dumps(stats, indent=2, sort_keys=True))
