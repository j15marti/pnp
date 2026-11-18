#!/usr/bin/env python3
"""TMR-3/078. Exact fixed-T5 count: block-cut-tree + local strong-two-covers.

Input (standard input): JSON {"n": nonnegative integer, "arcs": [[u,v], ...]}.
Run without stdin for deterministic finite audit. No external packages or network.
Mathematical scope: recognized 3-parent hub->private-sink incidence graphs.
Other digraphs, and unrecognized cover configurations, use a correct forest
enumerator (potentially exponential). This is an upper bound, not a lower bound.
"""
from itertools import combinations, product
from collections import defaultdict
import functools
import json
import random
import sys


def beat(a, b):
    return (b - a) % 5 in (1, 3)


def triple_weight(a, b, c):
    return sum(beat(a, z) and beat(b, z) and beat(c, z) for z in range(5))


def forest_count(n, edges):
    """Z5 rotation symmetry, binary differences on spanning forest edges."""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append((v, (1, 3)))
        adj[v].append((u, (-1, -3)))
    seen = set()
    total = 1
    for root in range(n):
        if root in seen:
            continue
        seen.add(root)
        order = [root]
        parent = {root: -1}
        delta = {}
        for u in order:
            for v, d in adj[u]:
                if v not in seen:
                    seen.add(v)
                    parent[v] = u
                    delta[v] = d
                    order.append(v)
        local_edges = [(u, v) for u, v in edges if u in parent and v in parent]
        good = 0
        for bits in product((0, 1), repeat=len(order) - 1):
            x = {root: 0}
            for v, bit in zip(order[1:], bits):
                x[v] = (x[parent[v]] + delta[v][bit]) % 5
            good += all(beat(x[u], x[v]) for u, v in local_edges)
        total *= 5 * good
    return total


def biconnected_blocks(vertices, triples):
    """Source-derived Tarjan edge-block decomposition of the triple primal graph."""
    adj = {v: set() for v in vertices}
    for a, b, c in triples:
        for u, v in ((a, b), (a, c), (b, c)):
            adj[u].add(v)
            adj[v].add(u)
    disc, low, edge_stack, blocks = {}, {}, [], []
    timer = 0
    sys.setrecursionlimit(max(1000, 8 * len(vertices) + 100))

    def dfs(u, parent):
        nonlocal timer
        disc[u] = low[u] = timer
        timer += 1
        for v in sorted(adj[u]):
            if v not in disc:
                edge_stack.append((u, v))
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] >= disc[u]:
                    component = set()
                    while True:
                        e = edge_stack.pop()
                        component.update(e)
                        if e == (u, v):
                            break
                    blocks.append(frozenset(component))
            elif v != parent and disc[v] < disc[u]:
                low[u] = min(low[u], disc[v])
                edge_stack.append((u, v))

    for v in vertices:
        if v not in disc:
            dfs(v, None)
    return blocks


def local_cover(vertices, triples, parent, max_cover):
    """Find an internal cover C of size <=max_cover with 2 fixed hubs per triple.

    Parent is externally fixed and is free of charge. Recursive branches are
    complete: any feasible extension covers each deficient triple by 1 or 2
    of its remaining vertices; never rely on provided decomposition certificates.
    """
    seed = frozenset(() if parent is None else (parent,))

    def rec(chosen, budget):
        fixed = chosen | seed
        deficient = next((e for e in triples if len(fixed.intersection(e)) < 2), None)
        if deficient is None:
            return chosen
        need = 2 - len(fixed.intersection(deficient))
        available = sorted(set(deficient) - fixed)
        if need > budget:
            return None
        for option in combinations(available, need):
            answer = rec(chosen | frozenset(option), budget - need)
            if answer is not None:
                return answer
        return None

    for budget in range(max_cover + 1):
        answer = rec(frozenset(), budget)
        if answer is not None:
            return tuple(sorted(answer))
    return None


def block_tree_count(hubs, triples, t=3):
    """Exact count when each derived biconnected block has relative cover <=t."""
    blocks = biconnected_blocks(hubs, triples)
    if not blocks:  # every hub is isolated
        return 5 ** len(hubs), True, 0
    member = defaultdict(list)
    for i, B in enumerate(blocks):
        for v in B:
            member[v].append(i)
    articulation = {v for v in member if len(member[v]) > 1}
    triple_by_block = [[] for _ in blocks]
    edge_to_block = {}
    for i, B in enumerate(blocks):
        for u in B:
            for v in B:
                if u < v:
                    edge_to_block.setdefault((u, v), i)
    for e in triples:
        u, v, z = sorted(e)
        i = edge_to_block[(u, v)]
        assert z in blocks[i], 'triple crosses biconnected blocks'
        triple_by_block[i].append(e)  # MULTIPLICITY retained

    parent_art = [None] * len(blocks)
    children = [defaultdict(list) for _ in blocks]
    roots, order, seen = [], [], set()
    for root in range(len(blocks)):
        if root in seen:
            continue
        roots.append(root)
        seen.add(root)
        stack = [root]
        while stack:
            i = stack.pop()
            order.append(i)
            for v in sorted(blocks[i] & articulation):
                if v == parent_art[i]:
                    continue
                for j in member[v]:
                    if j != i and j not in seen:
                        seen.add(j)
                        parent_art[j] = v
                        children[i][v].append(j)
                        stack.append(j)
    assert len(order) == len(blocks)

    covers = []
    for i in range(len(blocks)):
        C = local_cover(blocks[i], triple_by_block[i], parent_art[i], t)
        if C is None:
            return None, False, len(blocks)
        covers.append(C)

    message = [None] * len(blocks)
    for i in reversed(order):
        P = parent_art[i]
        C = covers[i]
        E = triple_by_block[i]
        fixed_set = set(C) | ({P} if P is not None else set())
        free = sorted(set(blocks[i]) - fixed_set)
        const = []
        by_free = {v: [] for v in free}
        for e in E:
            remaining = [v for v in e if v not in fixed_set]
            if not remaining:
                const.append(e)
            elif len(remaining) == 1:
                by_free[remaining[0]].append(e)
            else:
                raise AssertionError('cover leaves coupled free variables')
        child_unary = {}
        for v, subblocks in children[i].items():
            child_unary[v] = [
                functools.reduce(lambda x, y: x * y,
                                 (message[j][color] for j in subblocks), 1)
                for color in range(5)
            ]

        def evaluate(parent_color):
            base = {} if P is None else {P: parent_color}
            acc = 0
            for assignment in product(range(5), repeat=len(C)):
                colors = dict(base)
                colors.update(zip(C, assignment))
                coeff = 1
                for v in C:
                    if v in child_unary:
                        coeff *= child_unary[v][colors[v]]
                for e in const:
                    coeff *= triple_weight(*(colors[v] for v in e))
                    if not coeff:
                        break
                if not coeff:
                    continue
                for v in free:
                    q = 0
                    for a in range(5):
                        colors[v] = a
                        val = child_unary[v][a] if v in child_unary else 1
                        for e in by_free[v]:
                            val *= triple_weight(*(colors[w] for w in e))
                            if not val:
                                break
                        q += val
                    colors.pop(v, None)
                    coeff *= q
                    if not coeff:
                        break
                acc += coeff
            return acc

        message[i] = evaluate(None) if P is None else [evaluate(a) for a in range(5)]

    z = 5 ** sum(v not in member for v in hubs)
    for root in roots:
        z *= message[root]
    return z, True, len(blocks)


def solve(n, arcs, t=3):
    if type(n) is not int or n < 0 or type(t) is not int or t < 0:
        raise ValueError('invalid vertex count or cover budget')
    edges = set()
    for pair in arcs:
        if not isinstance(pair, (tuple, list)) or len(pair) != 2:
            raise ValueError('invalid edge')
        u, v = pair
        if type(u) is not int or type(v) is not int or not (0 <= u < n and 0 <= v < n):
            raise ValueError('invalid endpoint')
        edges.add((u, v))
    edges = tuple(sorted(edges))
    if any(u == v or (v, u) in edges for u, v in edges):
        return 0, 'structural-zero'
    indeg = [set() for _ in range(n)]
    outdeg = [set() for _ in range(n)]
    for u, v in edges:
        indeg[v].add(u)
        outdeg[u].add(v)
    hubs = tuple(v for v in range(n) if not indeg[v])
    H = set(hubs)
    sinks = [v for v in range(n) if indeg[v]]
    if all(not outdeg[v] and len(indeg[v]) == 3 and indeg[v] <= H for v in sinks):
        triples = [tuple(sorted(indeg[v])) for v in sinks]
        z, ok, bcount = block_tree_count(hubs, triples, t)
        if ok:
            return z, 'block-tree'
    return forest_count(n, edges), 'forest-fallback'


def chain_family(r):
    """r K4 primal blocks in a path, 1+3r hubs and 3r private sinks."""
    hubs = 1 + 3*r
    arcs = []
    for i in range(r):
        a0, a1 = i, i + 1
        b, c = (r + 1 + 2*i), (r + 2 + 2*i)
        for j, e in enumerate(((a0, b, a1), (a0, c, a1), (b, c, a1))):
            s = hubs + 3*i + j
            arcs.extend((v, s) for v in e)
    return 1 + 6*r, arcs


def brute(n, edges):
    return sum(all(beat(x[u], x[v]) for u, v in edges)
               for x in product(range(5), repeat=n))


def hub_count(k, triples):
    return sum(functools.reduce(lambda z, e: z * triple_weight(*(x[u] for u in e)),
                                triples, 1)
               for x in product(range(5), repeat=k))


def audit():
    rng = random.Random(202611172327)
    checks = 0
    modes = defaultdict(int)

    def check(got, ref, label):
        nonlocal checks
        assert got == ref, (label, got, ref)
        checks += 1

    for n in range(7):
        for _ in range(16):
            arcs = [(u, v) for u in range(n) for v in range(n)
                    if u != v and rng.random() < .12]
            z, mode = solve(n, arcs)
            check(z, brute(n, arcs), ('arbitrary', n))
            modes[mode] += 1

    for k in range(3, 8):
        for _ in range(20):
            num = rng.randrange(6)
            triples = [tuple(rng.sample(range(k), 3)) for _ in range(num)]
            arcs = [(v, k+i) for i, e in enumerate(triples) for v in e]
            z, mode = solve(k + num, arcs)
            check(z, hub_count(k, triples), ('incidence', k, triples))
            modes[mode] += 1

    for r in (1, 2, 3, 4, 5, 8, 12, 50):
        z, mode = solve(*chain_family(r))
        check(z, 5 * 28**r, ('chain', r))
        check(mode, 'block-tree', ('chain-mode', r))
        modes[mode] += 1
    for g in ((0, []), (4, []), (2, [(0, 1)]), (2, [(0, 0)]),
              (2, [(0, 1), (1, 0)]), (4, [(0, 3), (1, 3), (2, 3)]),
              (4, [(0, 3), (1, 3), (2, 3)] * 2)):
        z, mode = solve(*g)
        check(z, brute(*g), ('structural', g))
        modes[mode] += 1

    for invalid in ((-1, []), (2, [(0, 2)]), (2, [('0', 1)]),
                    (2, [(True, 1)]), (2, [(0, 1, 1)])):
        try:
            solve(*invalid)
        except ValueError:
            checks += 1
        else:
            raise AssertionError(('malformed accepted', invalid))

    return {'revision': 'TMR3-T5-TREE-ADHESION078-v1',
            'checks': checks, 'failures': 0,
            'modes': dict(sorted(modes.items())),
            'chain50_digits': len(str(5*28**50)),
            'chain50_count': str(solve(*chain_family(50))[0])}


if __name__ == '__main__':
    if not sys.stdin.isatty() and not sys.stdin.closed and sys.stdin.buffer.peek(1):
        g = json.load(sys.stdin)
        z, method = solve(g['n'], g['arcs'], g.get('t', 3))
        print(json.dumps({'count': str(z), 'method': method}, sort_keys=True))
    else:
        print(json.dumps(audit(), sort_keys=True))
