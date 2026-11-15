#!/usr/bin/env python3
"""TSEITIN-TRANSFER-GATE058. Finite tests only, not an asymptotic proof."""
import itertools
import json
import random
from collections import defaultdict

def graph(kind, n=4):
    if kind == "K4":
        return 4, list(itertools.combinations(range(4), 2))
    if kind == "K33":
        return 6, [(u, v) for u in range(3) for v in range(3, 6)]
    if kind == "cube":
        return 8, [(u, u ^ (1 << k)) for u in range(8)
                   for k in range(3) if u < (u ^ (1 << k))]
    if kind == "prism":
        assert n >= 3
        e = [(i, (i+1)%n) for i in range(n)]
        e += [(i+n, (i+1)%n+n) for i in range(n)]
        e += [(i, i+n) for i in range(n)]
        return 2*n, e
    raise ValueError(kind)

def parity_block(xs, charge):
    return [tuple(-x if a else x for x, a in zip(xs, bits))
            for bits in itertools.product((0, 1), repeat=3)
            if sum(bits) % 2 != charge]

def formula(h, edges, charges):
    inc = [[] for _ in range(h)]
    for j, (u, v) in enumerate(edges, 1):
        inc[u].append(j)
        inc[v].append(j)
    assert all(len(s) == 3 for s in inc)
    return [c for v in range(h) for c in parity_block(sorted(inc[v]), charges[v])]

def specialized(source):
    """Parse actual clauses; return None when noncanonical or malformed."""
    blocks = defaultdict(list)
    for c in source:
        if len(c) != 3 or 0 in c or len(set(map(abs, c))) != 3:
            return None
        blocks[tuple(sorted(map(abs, c)))].append(tuple(sorted(c)))
    if not blocks:
        return None
    vertices = []
    for xs, cls in blocks.items():
        if len(cls) != 4 or len(set(cls)) != 4:
            return None
        choices = [b for b in (0, 1)
                   if set(cls) == {tuple(sorted(c)) for c in parity_block(xs, b)}]
        if len(choices) != 1:
            return None
        vertices.append((xs, choices[0]))
    occ = defaultdict(list)
    for v, (xs, _) in enumerate(vertices):
        for x in xs:
            occ[x].append(v)
    if any(len(vs) != 2 or vs[0] == vs[1] for vs in occ.values()):
        return None
    adj = [set() for _ in vertices]
    for a, b in occ.values():
        adj[a].add(b)
        adj[b].add(a)
    seen = set()
    for v in range(len(vertices)):
        if v in seen:
            continue
        stack = [v]
        seen.add(v)
        parity = 0
        while stack:
            u = stack.pop()
            parity ^= vertices[u][1]
            for w in adj[u]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        if parity:
            return "UNSAT"
    return "SAT"

def brute(source):
    vs = sorted({abs(t) for clause in source for t in clause})
    for bits in itertools.product((0, 1), repeat=len(vs)):
        assignment = dict(zip(vs, bits))
        if all(any(assignment[abs(t)] == (t > 0) for t in c) for c in source):
            return "SAT"
    return "UNSAT"

def total_decider(source):
    fast = specialized(source)
    return fast if fast is not None else brute(source)

def xor_all(h, edges, charges):
    lhs = 0
    for v in range(h):
        row = 0
        for j, (u, w) in enumerate(edges):
            if v in (u, w):
                row ^= 1 << j
        lhs ^= row
    return lhs, sum(charges) % 2

def run():
    rng = random.Random(202611142056)
    checks = 0
    examples = []
    for kind, m in [("K4", 4), ("K33", 6), ("cube", 8),
                    ("prism", 3), ("prism", 4)]:
        h, edges = graph(kind, m)
        for parity in (0, 1):
            charges = [parity] + [0] * (h-1)
            source = formula(h, edges, charges)
            expected = "UNSAT" if parity else "SAT"
            assert len(source) == 4*h; checks += 1
            assert all(len(set(map(abs, c))) == 3 for c in source); checks += 1
            assert specialized(source) == expected; checks += 1
            assert total_decider(source) == expected; checks += 1
            assert xor_all(h, edges, charges) == (0, parity); checks += 1
            if len(edges) <= 12:
                assert brute(source) == expected; checks += 1
            for _ in range(4):
                ids = list(range(11, len(edges)+11))
                rng.shuffle(ids)
                lookup = {i+1: ids[i] for i in range(len(ids))}
                altered = [tuple((1 if x > 0 else -1)*lookup[abs(x)]
                                 for x in c) for c in source]
                rng.shuffle(altered)
                altered = [tuple(rng.sample(c, len(c))) for c in altered]
                assert specialized(altered) == expected; checks += 1
            assert specialized(source[:-1]) is None; checks += 1
            examples.append([kind, h, len(edges), len(source), parity, expected])
    h, edges = graph("K4")
    edges2 = edges + [(u+h, v+h) for u, v in edges]
    two_odd = [1, 0, 0, 0, 1, 0, 0, 0]
    src = formula(2*h, edges2, two_odd)
    assert specialized(src) == "UNSAT"; checks += 1
    assert brute(src) == "UNSAT"; checks += 1
    assert xor_all(2*h, edges2, two_odd) == (0, 0); checks += 1
    even_src = formula(h, edges, [0]*h)
    malformed = even_src + [(1, 2, 3)]
    assert specialized(malformed) is None; checks += 1
    assert total_decider(malformed) == brute(malformed); checks += 1
    print(json.dumps({"claim":"TSEITIN-TRANSFER-GATE058",
                      "native_assertions":checks,"failures":0,
                      "controls":"exact 3-CNF parity, even/odd, renaming, clause permutation, source removal, two odd components, malformed fallback",
                      "examples":examples,
                      "scope":"finite tests only; expander Resolution lower bound imported from primary theorem"},
                     sort_keys=True, indent=2))

if __name__ == "__main__":
    run()
