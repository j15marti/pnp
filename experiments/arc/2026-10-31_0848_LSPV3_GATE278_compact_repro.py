#!/usr/bin/env python3
"""Standalone compact GATE278 reproducer.
Exact articulation separator and matched SAT/UNSAT STAR family under renaming.
Full independently verified 29-source raw runs are in the GATE278 ZIP archive;
this compact source is a separate nonidentical mathematical control.
No native FLMV machine claims. Standard Python only.
"""
import itertools, json, math, random
from collections import Counter

def star(k, b):
    C = []
    n = 1
    for i in range(k):
        y, z = n + 1, n + 2
        n += 2
        lit = 1 if (i == k - 1 and b == 1) else -1
        for sy, sz in itertools.product((1, -1), repeat=2):
            C.append((lit, sy * y, sz * z))
        for _ in range(k - 1):
            p, q = n + 1, n + 2
            n += 2
            C.append((y, p, q))
    assert n == 1 + 2 * k * k and len(C) == k * (k + 3)
    return C, n

def permute(C, n, seed):
    r = list(range(1, n + 1))
    random.Random(seed).shuffle(r)
    d = dict(enumerate(r, start=1))
    return [tuple((1 if l > 0 else -1) * d[abs(l)] for l in c) for c in C]

def primal(C, n):
    g = [set() for _ in range(n + 1)]
    for c in C:
        for a, b in itertools.combinations(map(abs, c), 2):
            if a != b:
                g[a].add(b)
                g[b].add(a)
    return g

def components(g, banned=None):
    seen = set()
    out = []
    for v in range(1, len(g)):
        if v in seen or v == banned:
            continue
        seen.add(v)
        queue = [v]
        group = set()
        while queue:
            z = queue.pop()
            group.add(z)
            for w in g[z]:
                if w not in seen and w != banned:
                    seen.add(w)
                    queue.append(w)
        out.append(group)
    return out

def recognize(C, n):
    g = primal(C, n)
    base = len(components(g))
    occ = Counter(abs(l) for c in C for l in c)
    arts = [v for v in range(1, n + 1) if len(components(g, v)) > base]
    return max(arts, key=lambda v: (occ[v], len(g[v]), -v)) if arts else None

def UP_DPLL(C, n, assumptions=None):
    def rec(a):
        while True:
            unit = None
            unresolved = False
            for c in C:
                if any(abs(l) in a and a[abs(l)] == (l > 0) for l in c):
                    continue
                left = [l for l in c if abs(l) not in a]
                if not left:
                    return None
                unresolved = True
                if len(left) == 1:
                    unit = left[0]
                    break
            if unit is None:
                break
            a[abs(unit)] = (unit > 0)
        if not unresolved:
            return a
        choices = Counter(abs(l) for c in C for l in c if abs(l) not in a)
        if not choices:
            return None
        v = choices.most_common(1)[0][0]
        for bit in (True, False):
            b = dict(a)
            b[v] = bit
            ans = rec(b)
            if ans is not None:
                return ans
        return None
    return rec(dict(assumptions or {}))

def join(C, n, x):
    if x is None:
        raise ValueError("This compact test covers one-articulation sources only.")
    groups = components(primal(C, n), x)
    assert len(groups) >= 2
    block = {}
    for i, g in enumerate(groups):
        for v in g:
            block[v] = i
    parts = [[] for _ in groups]
    boundary = []
    for j, c in enumerate(C, start=1):
        ids = {block[abs(l)] for l in c if abs(l) != x}
        assert len(ids) <= 1, ("cross-component source clause", j)
        if ids:
            parts[next(iter(ids))].append((j, c))
        else:
            boundary.append((j, c))
    for bit in (False, True):
        if any(not any(abs(l) == x and (l > 0) == bit for l in c)
               for _, c in boundary):
            continue
        vals = {x: bit}
        complete = True
        for group, part in zip(groups, parts):
            child = [tuple(l for l in c if abs(l) != x)
                     for _, c in part
                     if not any(abs(l) == x and (l > 0) == bit for l in c)]
            model = UP_DPLL(child, n)
            if model is None:
                complete = False
                break
            vals.update({v: model.get(v, False) for v in group})
        if complete and all(any(vals.get(abs(l), False) == (l > 0) for l in c) for c in C):
            return True, vals, parts
    return False, None, parts

def source_extremes(C):
    checks = 0
    for i, c in enumerate(C):
        S = {abs(l): int(l > 0) for l in c}
        U = {abs(l): int(l < 0) for l in c}
        assert all(U[v] == 1 - S[v] for v in S)
        checks += len(c)
        for d in C[i + 1:]:
            a = {abs(l): int(l > 0) for l in d}
            shared = S.keys() & a.keys()
            same = any(S[v] == a[v] for v in shared)
            opp = any(S[v] != a[v] for v in shared)
            modes = (not opp, not same, not same, not opp)
            for j, x in enumerate((S, S, U, U)):
                y = (a, {v: 1 - z for v, z in a.items()})[j % 2]
                if j >= 2:
                    y = (a, {v: 1 - z for v, z in a.items()})[j % 2]
                src = (S if j < 2 else U)
                assert modes[j] == all(src[v] == y[v] for v in shared)
                checks += 1
    return checks

def main():
    rows = []
    checks = 0
    for k in (3, 5, 7, 9):
        for charge in (0, 1):
            for renamed in (False, True):
                C, n = star(k, charge)
                if renamed:
                    C = permute(C, n, 278093 + k * 3 + charge)
                x = recognize(C, n)
                assert x is not None
                sat, model, parts = join(C, n, x)
                label = (charge == 0)
                assert sat == label
                assert (UP_DPLL(C, n) is not None) == sat
                assert len(parts) == k and all(len(p) == k + 3 for p in parts)
                checks += source_extremes(C)
                zero = {v: False for v in range(1, n + 1)}
                one = {v: True for v in range(1, n + 1)}
                for a in (zero, one):
                    vals = [sum(a[abs(l)] == (l > 0) for l in c) for c in C]
                    assert all(0 <= z <= 3 for z in vals)
                    b = {v: not a[v] for v in a}
                    assert all(sum(b[abs(l)] == (l > 0) for l in c) == 3 - vals[j]
                               for j, c in enumerate(C))
                    checks += len(C)
                rows.append({"k": k, "sat": sat, "renamed": renamed,
                             "n": n, "m": len(C), "partitions": len(parts),
                             "unique_articulation_center_occurrences": 4 * k})
    print(json.dumps({"pass": True, "rows": rows, "counted_checks": checks,
                      "status": "restricted exact control; P vs NP OPEN"}, indent=2))

if __name__ == "__main__":
    main()
