#!/usr/bin/env python3
"""Independent finite referee for branching full-interface composition.

This is deliberately exponential brute-force verification, NOT the
polynomial solver. See FULL_INTERFACE_COMPOSITION165_repro.py for the
full deterministic 2SAT+codimension-one acquisition algorithm.
"""
import itertools
import json
import random


def sat_clause(c, a):
    return any(a[abs(z)] == (z > 0) for z in c)


def sat_local(node, a):
    return all(sat_clause(c, a) for c in node['C']) and all(
        (sum(a[x] for x in xs) & 1) == b for xs, b in node['A'])


def possible_local(node, pins):
    free = sorted(set(node['bag']) - set(pins))
    for bits in itertools.product((0, 1), repeat=len(free)):
        a = dict(pins)
        a.update(zip(free, bits))
        if sat_local(node, a):
            return a
    return None


def tables(tree):
    kids = {u: [] for u in tree}
    roots = []
    for u, rec in tree.items():
        if rec['parent'] is None:
            roots.append(u)
        else:
            kids[rec['parent']].append(u)
    assert len(roots) == 1
    root = roots[0]
    loc = {}
    for u, rec in tree.items():
        for v in rec['bag']:
            loc.setdefault(v, set()).add(u)
    for v, sites in loc.items():
        reached = {next(iter(sites))}
        while True:
            grow = reached | {
                u for u in sites if (tree[u]['parent'] in reached or
                     any(z in reached for z in kids[u]))}
            if grow == reached:
                break
            reached = grow
        assert reached == sites, 'running intersection violated'
    order = []
    def visit(u):
        for c in kids[u]:
            visit(c)
        order.append(u)
    visit(root)
    out = {}
    trials = 0
    for u in order:
        node = tree[u]
        bag = set(node['bag'])
        own = {v for v in bag if loc[v] == {u}}
        B = sorted(bag - own)
        parent = node['parent']
        sep = sorted(bag & set(tree[parent]['bag'])) if parent is not None else []
        good = set()
        for bits in itertools.product((0, 1), repeat=len(B)):
            trials += 1
            pins = dict(zip(B, bits))
            if any(tuple(pins[v] for v in sorted(bag & set(tree[c]['bag'])))
                   not in out[c] for c in kids[u]):
                continue
            if possible_local(node, pins) is not None:
                good.add(tuple(pins[v] for v in sep))
        out[u] = good
    return (() in out[root]), trials


def brute(tree):
    vars_ = sorted({v for node in tree.values() for v in node['bag']})
    for bits in itertools.product((0, 1), repeat=len(vars_)):
        a = dict(zip(vars_, bits))
        if all(sat_local(node, a) for node in tree.values()):
            return True
    return False


def main():
    rng = random.Random(165165)
    checks = 0
    sat = 0
    unsat = 0
    trials = 0
    for k in range(2, 6):
        for _ in range(40):
            parents = {0: None}
            for u in range(1, k):
                parents[u] = rng.randrange(u)
            center = 3 * k + 1
            tree = {}
            for u in range(k):
                bag = {u + 1, center}
                for v in range(1, k):
                    if parents[v] == u:
                        bag.add(k + v)
                    if v == u:
                        bag.add(k + v)
                bag = sorted(bag)
                clauses = [tuple((z if rng.randrange(2) else -z)
                                 for z in rng.choices(bag, k=2))
                           for _ in range(rng.randrange(1, 5))]
                mask = tuple(x for x in bag if rng.randrange(2))
                affine = [(mask, rng.randrange(2))] if mask else []
                tree[u] = {'parent': parents[u], 'bag': bag,
                           'C': clauses, 'A': affine}
            decision, count = tables(tree)
            assert decision == brute(tree)
            sat += int(decision)
            unsat += int(not decision)
            checks += 1
            trials += count
    star = []
    for m in (4, 8):
        tree = {0: {'parent': None, 'bag': list(range(1, m + 1)),
                    'C': [], 'A': []}}
        for i in range(1, m + 1):
            tree[i] = {'parent': 0, 'bag': [i], 'C': [(i,)], 'A': []}
        dec, tests = tables(tree)
        assert dec and tests >= 2 ** m
        star.append({'m': m, 'edge_width': 1, 'full_hub_width': m,
                     'hub_assignments': 2 ** m})
    return {'independent_global_checks': checks, 'SAT': sat,
            'UNSAT': unsat, 'all_agree': True, 'total_full_table_trials': trials,
            'star': star}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
