#!/usr/bin/env python3
"""Exact affine-profile tree DP and deterministic, staged finite audits.

No general polynomial SAT claim. Input constraints are explicit 2CNF and
GF(2) rows; a complete source-owned running-intersection tree is required.
Budgets yield UNKNOWN before DP rather than an unsupported SAT/UNSAT answer.
The XP backend is the unchanged, inspected ARC228 reference implementation.
Run --stage all to write independently reproducible JSON audit outputs.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from hashlib import sha256
from itertools import product
import importlib.util
import json
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent
REFERENCE = HERE.parents[1] / 'agents/lspv-1/2026-10-29_1200_ARC228_fixed_codimension_solver.py'
spec = importlib.util.spec_from_file_location('arc228_reference', REFERENCE)
assert spec and spec.loader, REFERENCE
xp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(xp)
SEED = 202610291323


def affine_space(n, equations):
    """RREF: None for inconsistency, else (anchor, nullspace basis, rank)."""
    rows = [[int(m), int(b)] for m, b in equations]
    if any(m < 0 or m >> n or b not in (0, 1) for m, b in rows):
        raise ValueError('invalid affine row')
    pivots = []
    k = 0
    for col in range(n):
        pivot = next((j for j in range(k, len(rows)) if rows[j][0] >> col & 1), None)
        if pivot is None:
            continue
        rows[k], rows[pivot] = rows[pivot], rows[k]
        for j in range(len(rows)):
            if j != k and rows[j][0] >> col & 1:
                rows[j][0] ^= rows[k][0]
                rows[j][1] ^= rows[k][1]
        pivots.append(col)
        k += 1
    if any(m == 0 and b for m, b in rows):
        return None
    anchor = sum(rows[j][1] << p for j, p in enumerate(pivots))
    free = [i for i in range(n) if i not in pivots]
    basis = []
    for f in free:
        v = 1 << f
        for j, p in enumerate(pivots):
            v |= ((rows[j][0] >> f) & 1) << p
        basis.append(v)
    return anchor, basis, k


def span_basis(vectors):
    pivots = {}
    for v in vectors:
        while v:
            p = v.bit_length() - 1
            if p in pivots:
                v ^= pivots[p]
            else:
                pivots[p] = v
                break
    return tuple(pivots[p] for p in sorted(pivots))


def project_mask(mask, coordinates):
    return sum(((mask >> v) & 1) << i for i, v in enumerate(coordinates))


def coset_points(anchor, basis):
    # Gray enumeration, one independent-basis addition per new row.
    point = anchor
    yield point
    for i in range(1, 1 << len(basis)):
        point ^= basis[(i & -i).bit_length() - 1]
        yield point


def source_holds(source, assignment):
    for c in source:
        if c['kind'] == 'cnf':
            if not any(((assignment >> (abs(lit)-1)) & 1) == int(lit > 0)
                       for lit in c['lits']):
                return False
        elif ((assignment & c['mask']).bit_count() & 1) != c['rhs']:
            return False
    return True


def validate(instance):
    n, modules, source, edges = (instance[k] for k in ('n', 'modules', 'source', 'edges'))
    if n < 0 or not modules or len(edges) != len(modules)-1:
        raise ValueError('not a nonempty tree')
    m = len(modules)
    graph = [set() for _ in modules]
    for a, b in edges:
        if a == b or not (0 <= a < m and 0 <= b < m) or b in graph[a]:
            raise ValueError('invalid or repeated edge')
        graph[a].add(b)
        graph[b].add(a)
    parent = [-2] * m
    parent[0] = -1
    order = [0]
    for t in order:
        for u in sorted(graph[t]):
            if u == parent[t]:
                continue
            if parent[u] != -2:
                raise ValueError('cycle')
            parent[u] = t
            order.append(u)
    if len(order) != m:
        raise ValueError('disconnected tree')
    occurrences = defaultdict(set)
    ownership = Counter()
    bags = []
    for t, mod in enumerate(modules):
        bag = set(mod['bag'])
        if len(bag) != len(mod['bag']) or any(v < 0 or v >= n for v in bag):
            raise ValueError('invalid bag variables')
        bags.append(bag)
        for v in bag:
            occurrences[v].add(t)
        for cid in mod['ids']:
            if cid < 0 or cid >= len(source):
                raise ValueError('invalid source ID')
            ownership[cid] += 1
            c = source[cid]
            if c['kind'] == 'cnf':
                if len(c['lits']) > 2 or any(l == 0 or abs(l) > n for l in c['lits']):
                    raise ValueError('invalid 2CNF source')
                scope = {abs(l)-1 for l in c['lits']}
            elif c['kind'] == 'xor':
                if c['mask'] < 0 or c['mask'] >> n or c['rhs'] not in (0, 1):
                    raise ValueError('invalid XOR source')
                scope = {v for v in range(n) if c['mask'] >> v & 1}
            else:
                raise ValueError('unknown source type')
            if not scope <= bag:
                raise ValueError('source scope outside owner bag')
    if set(ownership) != set(range(len(source))) or any(v != 1 for v in ownership.values()):
        raise ValueError('source ownership is not exactly once')
    if set(occurrences) != set(range(n)):
        raise ValueError('declared variable has no bag')
    for v, nodes in occurrences.items():
        seen = {min(nodes)}
        queue = list(seen)
        for t in queue:
            for u in graph[t] & nodes:
                if u not in seen:
                    seen.add(u)
                    queue.append(u)
        if seen != nodes:
            raise ValueError('running intersection fails')
    boundaries = [tuple(sorted(v for v in bag if len(occurrences[v]) > 1)) for bag in bags]
    separators = [() if parent[t] < 0 else tuple(sorted(bags[t] & bags[parent[t]]))
                  for t in range(m)]
    return bags, boundaries, separators, parent, order


def pin_module(instance, t, boundary, beta, private):
    bvals = {v: (beta >> j) & 1 for j, v in enumerate(boundary)}
    local_index = {v: j for j, v in enumerate(private)}
    clauses, equations = [], []
    for cid in instance['modules'][t]['ids']:
        c = instance['source'][cid]
        if c['kind'] == 'cnf':
            if any(v in bvals and bvals[v] == int(lit > 0)
                   for lit in c['lits'] for v in (abs(lit)-1,)):
                continue
            clauses.append(tuple((local_index[abs(lit)-1]+1) * (1 if lit > 0 else -1)
                                 for lit in c['lits'] if abs(lit)-1 not in bvals))
        else:
            rhs = c['rhs']
            for v, val in bvals.items():
                if c['mask'] >> v & 1:
                    rhs ^= val
            equations.append((project_mask(c['mask'], private), rhs))
    return clauses, equations


def local_solver(n, clauses, equations, stats):
    stats['local_calls'] += 1
    space = affine_space(n, equations)
    if space is None:
        return None
    anchor, basis, rank = space
    # Both are explicitly computable upper-bound scores. Choosing by them is
    # an upper-bound strategy; it does not assert which backend is fastest.
    # The inspected DFS reference can revisit pivot orders. Use its conservative
    # n^{O(rank)} bound, not the sharper binomial bound of a different algorithm.
    xp_score = (n+1) ** (rank+1)
    if (1 << len(basis)) <= xp_score:
        stats['enumerative_calls'] += 1
        for a in coset_points(anchor, basis):
            stats['private_candidates'] += 1
            if all(any(((a >> (abs(l)-1)) & 1) == int(l > 0) for l in c) for c in clauses):
                return a
        return None
    stats['xp_calls'] += 1
    a = xp.fixed_codim_solver(n, clauses, equations, stats)
    return None if a is None else sum(v << i for i, v in enumerate(a))


def solve_tree(instance, row_budget=1 << 16):
    bags, boundaries, separators, parent, order = validate(instance)
    n = instance['n']
    stats = Counter(validated_constraints=len(instance['source']), validated_bags=len(bags))
    all_affine = [(c['mask'], c['rhs']) for c in instance['source'] if c['kind'] == 'xor']
    global_space = affine_space(n, all_affine)
    if global_space is None:
        return {'status': 'UNSAT', 'reason': 'global affine contradiction', 'stats': dict(stats)}
    anchor, global_basis, global_rank = global_space
    plans = []
    for t, boundary in enumerate(boundaries):
        profile_anchor = project_mask(anchor, boundary)
        profile_basis = span_basis(project_mask(v, boundary) for v in global_basis)
        private = tuple(sorted(bags[t] - set(boundary)))
        _, rows = pin_module(instance, t, boundary, profile_anchor, private)
        private_space = affine_space(len(private), [(mask, 0) for mask, _ in rows])
        assert private_space is not None
        private_rank = private_space[2]
        plans.append({'boundary': boundary, 'private': private, 'anchor': profile_anchor,
                      'basis': profile_basis, 'd': len(profile_basis), 'r': private_rank,
                      'u': len(private)-private_rank})
    profile_rows = sum(1 << p['d'] for p in plans)
    summary = {'global_rank': global_rank, 'global_nullity': len(global_basis),
               'profile_rows': profile_rows, 'raw_rows': sum(1 << len(b) for b in boundaries),
               'max_b': max(map(len, boundaries)), 'max_d': max(p['d'] for p in plans),
               'max_private_rank': max(p['r'] for p in plans),
               'profiles': [{k: p[k] for k in ('d', 'r', 'u')} for p in plans]}
    if row_budget is not None and profile_rows > row_budget:
        return {'status': 'UNKNOWN', 'reason': 'profile-row budget', 'stats': dict(stats), **summary}
    children = [[] for _ in bags]
    for t in order[1:]:
        children[parent[t]].append(t)
    # Exact separator tables; never substitute an affine hull for a relation.
    messages = [dict() for _ in bags]
    for t in reversed(order):
        p = plans[t]
        bpos = {v: i for i, v in enumerate(p['boundary'])}
        for beta in coset_points(p['anchor'], p['basis']):
            stats['boundary_rows'] += 1
            pointers = []
            compatible = True
            for u in children[t]:
                key = tuple((beta >> bpos[v]) & 1 for v in separators[u])
                stats['child_lookups'] += 1
                row = messages[u].get(key)
                if row is None:
                    compatible = False
                    stats['failed_child_lookups'] += 1
                    break
                pointers.append((u, key))
            if not compatible:
                continue
            clauses, equations = pin_module(instance, t, p['boundary'], beta, p['private'])
            w = local_solver(len(p['private']), clauses, equations, stats)
            if w is None:
                continue
            local = {v: (beta >> j) & 1 for j, v in enumerate(p['boundary'])}
            local.update({v: (w >> j) & 1 for j, v in enumerate(p['private'])})
            key = tuple(local[v] for v in separators[t])
            if key not in messages[t]:
                messages[t][key] = (local, pointers)
                stats['stored_rows'] += 1
    if () not in messages[0]:
        return {'status': 'UNSAT', 'reason': 'empty root table', 'stats': dict(stats), **summary}
    result = {}
    stack = [(0, ())]
    while stack:
        t, key = stack.pop()
        local, pointers = messages[t][key]
        for v, value in local.items():
            assert v not in result or result[v] == value, 'incompatible reconstructed source name'
            result[v] = value
        stack.extend(pointers)
    assignment = sum(result[v] << v for v in range(n))
    assert source_holds(instance['source'], assignment)
    stats['source_witness_checks'] += 1
    return {'status': 'SAT', 'assignment': assignment, 'stats': dict(stats), **summary}


def add_source(source, module, constraint):
    module['ids'].append(len(source))
    source.append(constraint)


def random_tree(rng, n):
    count = rng.randrange(1, 5)
    edges = [(t, rng.randrange(t)) for t in range(1, count)]
    graph = [set() for _ in range(count)]
    for t, u in edges:
        graph[t].add(u); graph[u].add(t)
    modules = [{'bag': [], 'ids': []} for _ in range(count)]
    for v in range(n):
        nodes = {rng.randrange(count)}
        for _ in range(rng.randrange(count)):
            frontier = [(t, u) for t in nodes for u in graph[t] if u not in nodes]
            if not frontier:
                break
            nodes.add(rng.choice(frontier)[1])
        for t in nodes:
            modules[t]['bag'].append(v)
    source = []
    for mod in modules:
        vs = mod['bag']
        if not vs:
            continue
        for _ in range(rng.randrange(0, 2*len(vs)+1)):
            chosen = rng.sample(vs, rng.randrange(1, min(2, len(vs))+1))
            add_source(source, mod, {'kind': 'cnf', 'lits': [(v+1)*rng.choice((-1, 1)) for v in chosen]})
        for _ in range(rng.randrange(0, min(4, len(vs))+1)):
            chosen = rng.sample(vs, rng.randrange(len(vs)+1))
            add_source(source, mod, {'kind': 'xor', 'mask': sum(1 << v for v in chosen), 'rhs': rng.randrange(2)})
    return {'n': n, 'modules': modules, 'source': source, 'edges': edges}


def strip_family(k, width, unsat=False):
    """Large actual boundary, unbounded global nullity, at most four profiles/bag."""
    assert k >= 2 and width >= 2
    edge_groups = [tuple(range(e*width, (e+1)*width)) for e in range(k-1)]
    offset = (k-1)*width
    source, modules = [], []
    for t in range(k):
        u, v = offset+2*t, offset+2*t+1
        left = edge_groups[t-1] if t else ()
        right = edge_groups[t] if t+1 < k else ()
        mod = {'bag': sorted((*left, *right, u, v)), 'ids': []}
        modules.append(mod)
        for bit in (u, v):
            add_source(source, mod, {'kind': 'cnf', 'lits': [bit+1]})
        for group in (left, right):
            if group:
                for bit in group[1:]:
                    for lits in ((-(bit+1), group[0]+1), (bit+1, -(group[0]+1))):
                        add_source(source, mod, {'kind': 'cnf', 'lits': list(lits)})
        if right:
            for bit in right[1:]:
                add_source(source, mod, {'kind': 'xor', 'mask': (1 << bit) | (1 << right[0]), 'rhs': 0})
        mask = (1 << u) | (1 << v)
        for group in (left, right):
            if group:
                mask ^= 1 << group[0]
        add_source(source, mod, {'kind': 'xor', 'mask': mask, 'rhs': int(unsat and t == k-1)})
    return {'n': offset+2*k, 'source': source, 'modules': modules,
            'edges': [(t-1, t) for t in range(1, k)]}


def discover_strip(n, source):
    """Source-first polynomial partial recognizer; no supplied bags or SAT calls.

    Binary affine rows form shared groups. Each remaining affine row owns two
    private names and meets one or two groups. Groups must join these modules
    into a path. Arbitrary 2CNF clauses are accepted when an owner bag covers
    their scope. Return None for unsupported structure.
    """
    adjacency = [set() for _ in range(n)]
    binary_ids, other_ids = [], []
    for cid, c in enumerate(source):
        if c['kind'] != 'xor':
            continue
        scope = [v for v in range(n) if c['mask'] >> v & 1]
        if len(scope) == 2:
            a, b = scope
            adjacency[a].add(b); adjacency[b].add(a)
            binary_ids.append(cid)
        elif len(scope) >= 3:
            other_ids.append(cid)
        else:
            return None
    if len(other_ids) < 2:
        return None
    groups, group_of = [], {}
    for start in range(n):
        if start in group_of or not adjacency[start]:
            continue
        gid = len(groups); nodes = [start]; group_of[start] = gid
        for v in nodes:
            for w in adjacency[v]:
                if w not in group_of:
                    group_of[w] = gid; nodes.append(w)
        groups.append(set(nodes))
    modules, group_owners, private_owner = [], defaultdict(set), {}
    for cid in other_ids:
        scope = {v for v in range(n) if source[cid]['mask'] >> v & 1}
        private = scope - set(group_of)
        seen_groups = [group_of[v] for v in scope if v in group_of]
        if len(private) != 2 or not (1 <= len(seen_groups) <= 2) or len(set(seen_groups)) != len(seen_groups):
            return None
        if any(v in private_owner for v in private):
            return None
        t = len(modules)
        bag = set(private)
        for gid in seen_groups:
            group_owners[gid].add(t); bag.update(groups[gid])
        for v in private:
            private_owner[v] = t
        modules.append({'bag': sorted(bag), 'ids': [cid]})
    if set(private_owner) | set(group_of) != set(range(n)):
        return None
    if any(len(group_owners[g]) != 2 for g in range(len(groups))):
        return None
    edges = [tuple(sorted(group_owners[g])) for g in range(len(groups))]
    if len(set(edges)) != len(edges) or len(edges) != len(modules)-1:
        return None
    degree = Counter(v for e in edges for v in e)
    if max(degree.values(), default=0) > 2:
        return None
    used = set(other_ids)
    for cid in binary_ids:
        v = next(v for v in range(n) if source[cid]['mask'] >> v & 1)
        modules[min(group_owners[group_of[v]])]['ids'].append(cid)
        used.add(cid)
    clause_rotation = Counter()
    for cid, c in enumerate(source):
        if cid in used:
            continue
        if c['kind'] != 'cnf' or len(c['lits']) > 2:
            return None
        scope = {abs(l)-1 for l in c['lits']}
        candidates = [t for t, mod in enumerate(modules) if scope <= set(mod['bag'])]
        if not candidates:
            return None
        key = tuple(sorted(c['lits']))
        t = candidates[clause_rotation[key] % len(candidates)]
        clause_rotation[key] += 1
        modules[t]['ids'].append(cid)
    out = {'n': n, 'source': deepcopy(source), 'modules': modules, 'edges': edges}
    try:
        validate(out)
    except ValueError:
        return None
    return out


def rename(instance, permutation, flips):
    out = deepcopy(instance)
    out['modules'] = [{'bag': sorted(permutation[v] for v in m['bag']), 'ids': list(m['ids'])}
                      for m in instance['modules']]
    for c in out['source']:
        if c['kind'] == 'cnf':
            c['lits'] = [(permutation[abs(l)-1]+1) * (1 if (l > 0) ^ bool(flips[abs(l)-1]) else -1)
                         for l in c['lits']]
        else:
            c['rhs'] ^= sum(flips[v] for v in range(instance['n']) if c['mask'] >> v & 1) & 1
            c['mask'] = sum(1 << permutation[v] for v in range(instance['n']) if c['mask'] >> v & 1)
    return out


def audit_algebra():
    rng = random.Random(SEED)
    counts = Counter()
    for n in range(0, 8):
        for _ in range(100):
            equations = [(rng.randrange(1 << n), rng.randrange(2)) for _ in range(rng.randrange(n+3))]
            brute = {a for a in range(1 << n) if all(((a & m).bit_count() & 1) == b for m, b in equations)}
            space = affine_space(n, equations)
            got = set() if space is None else set(coset_points(space[0], space[1]))
            assert got == brute
            counts['affine_spaces'] += 1
            boundary = tuple(i for i in range(n) if rng.randrange(2))
            private = tuple(i for i in range(n) if i not in boundary)
            projected = {project_mask(a, boundary) for a in brute}
            if space is not None:
                basis = span_basis(project_mask(v, boundary) for v in space[1])
                assert set(coset_points(project_mask(space[0], boundary), basis)) == projected
                private_rank = affine_space(len(private), [(project_mask(m, private), 0) for m, _ in equations])[2]
                assert len(basis) == len(boundary)-space[2]+private_rank
                counts['projection_rank_identities'] += 1
            counts['projection_comparisons'] += 1
    return dict(counts)


def audit_local():
    rng, stats = random.Random(SEED+1), Counter()
    counts = Counter()
    for n in range(0, 9):
        for _ in range(120):
            clauses = []
            for _ in range(rng.randrange(2*n+1)):
                vs = rng.sample(range(n), rng.randrange(1, min(2, n)+1))
                clauses.append(tuple((v+1)*rng.choice((-1, 1)) for v in vs))
            equations = [(rng.randrange(1 << n), rng.randrange(2)) for _ in range(rng.randrange(n+1))]
            brute = next((a for a in range(1 << n)
                          if all(any(((a >> (abs(l)-1)) & 1) == int(l > 0) for l in c) for c in clauses)
                          and all(((a & m).bit_count() & 1) == b for m, b in equations)), None)
            got = local_solver(n, clauses, equations, stats)
            assert (got is None) == (brute is None)
            counts['local_comparisons'] += 1
            counts['SAT' if got is not None else 'UNSAT'] += 1
    return {**dict(counts), 'logical_counters': dict(stats)}


def audit_tree():
    rng, counts, stats = random.Random(SEED+2), Counter(), Counter()
    for n in range(1, 11):
        for _ in range(45):
            instance = random_tree(rng, n)
            brute = next((a for a in range(1 << n) if source_holds(instance['source'], a)), None)
            got = solve_tree(instance)
            assert got['status'] == ('SAT' if brute is not None else 'UNSAT')
            counts['tree_comparisons'] += 1
            counts[got['status']] += 1
            stats.update(got['stats'])
    return {**dict(counts), 'logical_counters': dict(stats)}


def audit_controls():
    counts = Counter()
    base = strip_family(4, 3)
    invalid = []
    q = deepcopy(base); q['modules'][0]['ids'].append(q['modules'][1]['ids'][0]); invalid.append(q)
    q = deepcopy(base); q['modules'][0]['ids'].pop(); invalid.append(q)
    q = deepcopy(base); q['modules'][0]['bag'].pop(); invalid.append(q)
    # Minimal disconnected-occurrence path, all original source IDs owned.
    invalid.append({'n': 3, 'source': [{'kind': 'cnf', 'lits': [1]}, {'kind': 'cnf', 'lits': [-1]}],
                    'modules': [{'bag': [0, 1], 'ids': [0]}, {'bag': [1, 2], 'ids': []},
                                {'bag': [0, 2], 'ids': [1]}], 'edges': [(0, 1), (1, 2)]})
    q = deepcopy(base); q['edges'][1] = q['edges'][0]; invalid.append(q)
    for q in invalid:
        try:
            solve_tree(q)
        except ValueError:
            counts['invalid_certificates_rejected'] += 1
        else:
            raise AssertionError('malformed certificate accepted')
    # Empty-separator UNSAT must not be lost during projection.
    empty = {'n': 1, 'source': [{'kind': 'cnf', 'lits': []}],
             'modules': [{'bag': [0], 'ids': []}, {'bag': [], 'ids': [0]}], 'edges': [(0, 1)]}
    assert solve_tree(empty)['status'] == 'UNSAT'; counts['empty_separator_controls'] += 1
    # The referee's affine star is dispatched before any exponential DP.
    q = 20
    star = {'n': 2*q, 'source': [{'kind': 'xor', 'mask': (1 << (2*q))-1, 'rhs': 1}],
            'modules': [{'bag': list(range(2*q)), 'ids': [0]}], 'edges': []}
    for j in range(q):
        mod = {'bag': [2*j, 2*j+1], 'ids': []}
        add_source(star['source'], mod, {'kind': 'xor', 'mask': 3 << (2*j), 'rhs': 0})
        star['modules'].append(mod); star['edges'].append((0, j+1))
    st = solve_tree(star, row_budget=10)
    assert st['status'] == 'UNSAT' and st['reason'] == 'global affine contradiction'
    assert st['stats'].get('local_calls', 0) == 0
    counts['global_affine_star_control'] += 1
    for clauses, expected in (([(1, 2), (-1, 2), (-2,)], 'UNSAT'),
                              ([(-1, 2), (-2, 3), (1,)], 'SAT'),
                              ([(1, -2), (2, -3), (-1,)], 'SAT'),
                              ([(1,), (-1,)], 'UNSAT')):
        easy = {'n': 3, 'source': [{'kind': 'cnf', 'lits': list(c)} for c in clauses],
                'modules': [{'bag': [0, 1, 2], 'ids': list(range(len(clauses)))}], 'edges': []}
        assert solve_tree(easy)['status'] == expected
        counts['Horn_dual_Horn_2SAT_controls'] += 1
    # One rank-one module projects to a 3-clause, outside 2CNF AND affine.
    truth = []
    for x, y, z in product((0, 1), repeat=3):
        got = any((x or a) and (y or b) and ((a ^ b ^ z) == 1)
                  for a, b in product((0, 1), repeat=2))
        assert got == bool(x or y or z)
        truth.append(int(got)); counts['rank_one_clause_rows'] += 1
    models = [(x, y, z) for x, y, z in product((0, 1), repeat=3) if x or y or z]
    assert all(any((sum(row[j] << j for j in range(3)) & mask).bit_count() % 2 != rhs
                   for row in models) for mask in range(1, 8) for rhs in range(2))
    counts['nontrivial_affine_equations_rejected'] = 14
    # Full binary hull is tautology: every unary/binary partial assignment extends.
    for i in range(3):
        for j in range(i+1, 3):
            assert {(r[i], r[j]) for r in models} == set(product((0, 1), repeat=2))
            counts['binary_hull_pair_checks'] += 1
    # A consistent affine source with n global free source ports defeats a universal dimension bound.
    n = 12
    source, modules = [], [{'bag': list(range(n)), 'ids': []}]
    for j in range(n):
        a, b = n+2*j, n+2*j+1
        ports = (j, (j+1) % n, (j+2) % n)
        mod = {'bag': sorted((*ports, a, b)), 'ids': []}; modules.append(mod)
        add_source(source, mod, {'kind': 'cnf', 'lits': [ports[0]+1, a+1]})
        add_source(source, mod, {'kind': 'cnf', 'lits': [ports[1]+1, b+1]})
        add_source(source, mod, {'kind': 'xor', 'mask': (1 << a) | (1 << b) | (1 << ports[2]), 'rhs': 1})
    generic = {'n': 3*n, 'source': source, 'modules': modules,
               'edges': [(0, j) for j in range(1, n+1)]}
    g = solve_tree(generic, row_budget=100)
    assert g['status'] == 'UNKNOWN' and g['max_d'] == n and g['stats'].get('local_calls', 0) == 0
    counts['general_gadget_budget_rejection'] += 1
    rng = random.Random(SEED+3)
    for unsat in (False, True):
        base = strip_family(4, 3, unsat)
        for _ in range(20):
            permutation = list(range(base['n'])); rng.shuffle(permutation)
            flips = [rng.randrange(2) for _ in permutation]
            renamed = rename(base, permutation, flips)
            rng.shuffle(renamed['source'])
            recovered = discover_strip(renamed['n'], renamed['source'])
            assert recovered is not None
            got = solve_tree(recovered)
            assert got['status'] == ('UNSAT' if unsat else 'SAT') and got['max_d'] == 2
            counts['source_first_signed_renaming_and_clause_order_controls'] += 1
    assert discover_strip(generic['n'], generic['source']) is None
    counts['unsupported_discovery_rejections'] += 1
    return {**dict(counts), 'rank_one_projection_truth_table': truth,
            'generic_gadget': {k: g[k] for k in ('status', 'max_d', 'profile_rows', 'stats')}}


def audit_scaling():
    rows = []
    for k, width in ((2, 2), (3, 3), (4, 4), (8, 8), (12, 12), (16, 16), (24, 24)):
        for unsat in (False, True):
            instance = strip_family(k, width, unsat)
            recovered = discover_strip(instance['n'], instance['source'])
            assert recovered is not None
            got = solve_tree(recovered)
            assert got['status'] == ('UNSAT' if unsat else 'SAT')
            assert got['global_nullity'] == 2*k-1
            assert got['profile_rows'] == 4*k-4
            assert got['max_private_rank'] == 1
            if k > 2:
                assert got['max_b'] == 2*width and got['max_d'] == 2
            if instance['n'] <= 15:
                brute = any(source_holds(instance['source'], a) for a in range(1 << instance['n']))
                assert brute == (not unsat)
            rows.append({'k': k, 'width': width, 'n': instance['n'],
                         'encoded_json_bytes': len(json.dumps(instance, sort_keys=True, separators=(',', ':')).encode()),
                         **{key: got[key] for key in ('status', 'global_rank', 'global_nullity', 'raw_rows',
                                                    'profile_rows', 'max_b', 'max_d', 'max_private_rank', 'stats')}})
    return {'strip_cases': len(rows), 'rows': rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', choices=('algebra', 'local', 'tree', 'controls', 'scaling', 'all'), default='all')
    parser.add_argument('--out', type=Path, default=HERE)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    stages = {'algebra': audit_algebra, 'local': audit_local, 'tree': audit_tree,
              'controls': audit_controls, 'scaling': audit_scaling}
    for name, run in stages.items():
        if args.stage not in (name, 'all'):
            continue
        result = {'run_id': 'AFFINE_PROFILE_COMPOSITION1', 'stage': name, 'seed': SEED,
                  'status': 'COMPUTATIONAL finite controls; unrestricted SAT OPEN',
                  'code_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
                  'reference_sha256': sha256(REFERENCE.read_bytes()).hexdigest(), 'results': run()}
        target = args.out / ('AFFINE_PROFILE_COMPOSITION1_' + name + '.json')
        target.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
        print(json.dumps({'stage': name, 'output': str(target),
                          'counts': {k: v for k, v in result['results'].items() if isinstance(v, int)}}))


if __name__ == '__main__':
    main()
