#!/usr/bin/env python3
"""Bounded tests for one-pivot Davis--Putnam acquisition plus factoring.

The Python containers are only a finite semantic oracle for the test suite;
they are not evidence for the report's bit-machine workspace theorem.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import random
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


def zz(x: int) -> int:
    return 2 * abs(x) - (1 if x > 0 else 0)


def normalize(formula):
    out = set()
    for clause in formula:
        c = frozenset(clause)
        if any(-x in c for x in c):
            continue
        out.add(c)
    return tuple(sorted(out, key=lambda c: (len(c), tuple(sorted(c)))))


def encode(formula) -> bytes:
    f = normalize(formula)
    q = max((abs(x) for c in f for x in c), default=0)
    out = bytearray(MAGIC + uleb(q) + uleb(len(f)))
    for c in f:
        out += uleb(len(c))
        for x in sorted(c, key=lambda z: (abs(z), z < 0)):
            out += uleb(zz(x))
    return bytes(out)


def maxvar(formula):
    return max((abs(x) for c in normalize(formula) for x in c), default=0)


def sat(formula) -> bool:
    f = normalize(formula)
    q = max((abs(x) for c in f for x in c), default=0)
    for bits in itertools.product((False, True), repeat=q):
        if all(any(bits[abs(x) - 1] == (x > 0) for x in c) for c in f):
            return True
    return False


def dp_eliminate(formula, pivot):
    f = normalize(formula)
    pos = [c for c in f if pivot in c]
    neg = [c for c in f if -pivot in c]
    keep = [c for c in f if pivot not in c and -pivot not in c]
    attempts = 0
    resolvents = []
    for p in pos:
        for n in neg:
            attempts += 1
            r = (p - {pivot}) | (n - {-pivot})
            if any(-x in r for x in r):
                continue
            resolvents.append(r)
    return normalize(keep + resolvents), attempts


def components(formula):
    f = normalize(formula)
    if any(len(c) == 0 for c in f):
        return [tuple([frozenset()])]
    variables = sorted({abs(x) for c in f for x in c})
    adjacency = {v: set() for v in variables}
    for c in f:
        vs = {abs(x) for x in c}
        for v in vs:
            adjacency[v].update(vs - {v})
    groups = []
    unseen = set(variables)
    probes = 0
    while unseen:
        root = min(unseen)
        stack = [root]
        seen = {root}
        unseen.remove(root)
        while stack:
            v = stack.pop()
            probes += len(adjacency[v])
            for w in adjacency[v]:
                if w not in seen:
                    seen.add(w)
                    unseen.discard(w)
                    stack.append(w)
        groups.append(tuple(c for c in f if any(abs(x) in seen for x in c)))
    return groups, probes


def acquire(formula):
    f = normalize(formula)
    source = encode(f)
    n = 8 * len(source)
    if any(len(c) == 0 for c in f):
        return {"status": "UNSAT", "N": n, "steps": len(source), "children": []}
    if not f:
        return {"status": "SAT", "N": n, "steps": len(source), "children": []}
    max_child = math.floor(math.sqrt(n) * max(1.0, math.log2(n)))
    volume_cap = math.floor((n ** 1.1) * max(1.0, math.log2(n)) ** 2)
    step_cap = math.floor((n ** 1.2) * max(1.0, math.log2(n)) ** 2)
    steps = len(source)
    variables = sorted({abs(x) for c in f for x in c})
    for pivot in variables:
        residual, attempts = dp_eliminate(f, pivot)
        steps += len(f) + attempts + sum(len(c) for c in residual)
        if steps > step_cap:
            return {"status": "UNKNOWN", "N": n, "steps": steps,
                    "reason": "step_cap", "children": []}
        if any(len(c) == 0 for c in residual):
            return {"status": "UNSAT", "N": n, "steps": steps, "children": []}
        if not residual:
            return {"status": "SAT", "N": n, "steps": steps, "children": []}
        comps, probes = components(residual)
        steps += probes + len(residual)
        blobs = [encode(c) for c in comps]
        sizes = [8 * len(b) for b in blobs]
        steps += sum(len(b) for b in blobs)
        dense_children = all(maxvar(c) <= 128 * size for c, size in zip(comps, sizes))
        if (steps <= step_cap and max(sizes, default=0) <= max_child and
                sum(sizes) <= volume_cap and all(s < n for s in sizes) and
                dense_children):
            return {"status": "CHILDREN", "N": n, "steps": steps,
                    "pivot": pivot, "children": comps, "sizes": sizes,
                    "volume": sum(sizes), "max_child_cap": max_child,
                    "volume_cap": volume_cap, "step_cap": step_cap}
    return {"status": "UNKNOWN", "N": n, "steps": steps,
            "reason": "no_favorable_pivot", "children": []}


def accepted_family(m):
    hub = 1
    clauses = []
    for i in range(m):
        a, b = 2 + 2 * i, 3 + 2 * i
        clauses += [(hub, a, b), (-a, b), (a, -b)]
    return clauses


def cross_product_hostile(m):
    # Eliminating x creates m^2 resolvents; eliminating a leaf leaves a
    # source-scale connected component through x.
    x = 1
    return [(x, 2 + i) for i in range(m)] + [(-x, 2 + m + j) for j in range(m)]


def xor3(a, b, c, rhs):
    clauses = []
    for bits in itertools.product((False, True), repeat=3):
        if (sum(bits) & 1) != rhs:
            clauses.append(tuple(-v if bit else v for v, bit in zip((a, b, c), bits)))
    return clauses


def k4_parity_blocker():
    return (xor3(1, 2, 3, 1) + xor3(1, 4, 5, 0) +
            xor3(2, 4, 6, 0) + xor3(3, 5, 6, 0))


def public_metrics(result):
    out = {k: result[k] for k in result if k not in {"children", "sizes"}}
    sizes = result.get("sizes", [])
    if sizes:
        out.update({"child_count": len(sizes), "min_child_bits": min(sizes),
                    "max_child_bits": max(sizes)})
    return out


def main():
    started = time.monotonic()
    rng = random.Random(0xC0577)
    semantic = accepted = hostile_reject = 0
    executed_children = total_volume = 0
    digest = hashlib.sha256()

    for q in range(1, 8):
        for _ in range(45):
            formula = []
            for _ in range(rng.randint(0, 12)):
                width = rng.randint(0, min(3, q))
                vs = rng.sample(range(1, q + 1), width)
                formula.append(tuple(v if rng.getrandbits(1) else -v for v in vs))
            result = acquire(formula)
            parent = sat(formula)
            if result["status"] == "SAT":
                assert parent
            elif result["status"] == "UNSAT":
                assert not parent
            elif result["status"] == "CHILDREN":
                assert parent == all(sat(c) for c in result["children"])
                assert result["volume"] == sum(result["sizes"])
                assert max(result["sizes"]) <= result["max_child_cap"]
                assert result["steps"] <= result["step_cap"]
                executed_children += len(result["children"])
                total_volume += result["volume"]
                accepted += 1
            semantic += 1
            digest.update(encode(formula))

    family_metrics = []
    for m in [4, 8, 16, 32, 64, 128]:
        result = acquire(accepted_family(m))
        assert result["status"] in {"CHILDREN", "SAT"}
        if result["status"] == "CHILDREN":
            assert len(result["children"]) == m
            assert all(len(c) == 2 for c in result["children"])
            executed_children += m
            total_volume += result["volume"]
        family_metrics.append(public_metrics(result))

    hostile_metrics = []
    for m in [8, 16, 32, 64, 128, 256]:
        result = acquire(cross_product_hostile(m))
        assert result["status"] == "UNKNOWN"
        hostile_reject += 1
        hostile_metrics.append(public_metrics(result))

    k4 = k4_parity_blocker()
    assert not sat(k4)
    k4_source_bytes = len(encode(k4))
    k4_eliminated_bytes = [len(encode(dp_eliminate(k4, v)[0])) for v in range(1, 7)]
    assert k4_source_bytes == 70
    assert min(k4_eliminated_bytes) == 78

    output = {
        "status": "PASS",
        "seed": "0xc0577",
        "semantic_instances": semantic,
        "random_children_accepts": accepted,
        "executed_children_counted_with_multiplicity": executed_children,
        "executed_child_volume_bits": total_volume,
        "accepted_family": family_metrics,
        "hostile_rejections": hostile_reject,
        "hostile_family": hostile_metrics,
        "k4_parity_blocker": {"source_bytes": k4_source_bytes,
                               "eliminated_bytes_by_pivot": k4_eliminated_bytes,
                               "satisfiable": False},
        "aggregate_sha256": digest.hexdigest(),
        "elapsed_seconds": round(time.monotonic() - started, 6),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
