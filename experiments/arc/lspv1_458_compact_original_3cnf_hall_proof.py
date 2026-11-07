#!/usr/bin/env python3
"""LSPV-1/458 compact deterministic authenticated original-3CNF proof generator.

Full producer, separate hostile verifier and all deletion witnesses are in the
LSPV-1/458 reproducibility ZIP. This compact file independently regenerates
the original source and the exact 61-node source-indexed Resolution upper bound.
"""
import itertools as it
import hashlib
import json
import math

def norm(xs):
    if any(-x in xs for x in xs):
        return None
    return tuple(sorted(set(xs), key=lambda x: (abs(x), x < 0)))

def build(n, nh):
    edge = {}
    v = 1
    for i, N in enumerate(nh):
        for j in N:
            edge[i, j] = v
            v += 1
    src = [tuple(edge[i, j] for j in N) for i, N in enumerate(nh)]
    rows = {i: i + 1 for i in range(len(nh))}
    pairs = {}
    for i in range(len(nh)):
        for k in range(i + 1, len(nh)):
            for j in sorted(set(nh[i]) & set(nh[k])):
                z = v
                v += 1
                a = -edge[i, j]
                b = -edge[k, j]
                first = len(src) + 1
                src.extend(((a, b, z), (a, b, -z)))
                pairs[i, k, j] = (first, first + 1, z)
    assert all(len(c) == 3 and len(set(map(abs, c))) == 3 for c in src)
    return src, rows, pairs, edge, v - 1

def refute(src, rows, pairs, nh, group):
    nodes = {i + 1: norm(c) for i, c in enumerate(src)}
    derived = []
    def add(a, b, p):
        ca, cb = nodes[a], nodes[b]
        assert p in ca and -p in cb
        out = norm([x for x in ca if x != p] +
                   [x for x in cb if x != -p])
        assert out is not None
        u = len(src) + 1 + len(derived)
        nodes[u] = out
        derived.append((u, a, b, p))
        return u
    active = {nodes[rows[i]]: rows[i] for i in group}
    for i, k in it.combinations(group, 2):
        for j in sorted(set(nh[i]) & set(nh[k])):
            a, b, p = pairs[i, k, j]
            uid = add(a, b, p)
            active[nodes[uid]] = uid
    for p in sorted({abs(x) for c in active for x in c}):
        left = [(c, u) for c, u in active.items() if p in c]
        right = [(c, u) for c, u in active.items() if -p in c]
        nxt = {c: u for c, u in active.items() if p not in c and -p not in c}
        for ca, a in left:
            for cb, b in right:
                cc = norm([x for x in ca if x != p] +
                          [x for x in cb if x != -p])
                if cc is not None and cc not in nxt:
                    nxt[cc] = add(a, b, p)
        active = nxt
        if () in active:
            break
    assert () in active
    goal = active[()]
    byid = {a: (b, c, p) for a, b, c, p in derived}
    seen = set()
    todo = [goal]
    while todo:
        u = todo.pop()
        if u not in seen:
            seen.add(u)
            if u in byid:
                todo.extend(byid[u][:2])
    paid = [u for u in byid if u in seen]
    depth = {i: 0 for i in range(1, len(src) + 1)}
    for u, a, b, p in derived:
        depth[u] = 1 + max(depth[a], depth[b])
    return {'paid_nodes': len(paid),
            'source_leaves': len(seen - set(byid)),
            'span': depth[goal],
            'candidates': len(derived),
            'goal': goal}

def main():
    n = 5
    d = 3
    triples = list(it.combinations(range(n), d))
    nh = [t for triple in triples for t in (triple,) * d] + [triples[0]]
    assert len(nh) == 31 > 3 * math.comb(n, 3)
    src, rows, pairs, edge, nvar = build(n, nh)
    group = [i for i, t in enumerate(nh) if t == triples[0]]
    assert len(group) == 4
    proof = refute(src, rows, pairs, nh, group)
    assert (len(src), nvar, len(pairs)) == (1669, 912, 819)
    assert tuple(proof[k] for k in
                 ('paid_nodes', 'source_leaves', 'span', 'candidates')) == (61, 40, 10, 157)
    digest = hashlib.sha256(json.dumps([list(c) for c in src],
                    sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    assert digest == 'e3e7c9ea289eddffa65673e21273df4535668403511cb059a941eed29a17a2e4'
    print(json.dumps({'full_source_clauses': len(src),
                      'variables': nvar, 'collisions': len(pairs),
                      'repeated_group': group,
                      'original_signed_source_sha256': digest,
                      'proof': proof}, sort_keys=True))

if __name__ == '__main__':
    main()
