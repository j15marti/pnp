#!/usr/bin/env python3
"""CC09: exact circulation hulls, guarded exchanges, and source controls.

Standard-library-only, deterministic. This is a research checker, not a claimed
polynomial SAT solver. Exhaustive reference searches are explicitly bounded.
Run: python3 CC09_check.py --stage controls --output CC09_results.json
     python3 CC09_check.py --stage scaling --output CC09_scaling.json
"""
from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass
from itertools import combinations, product
import hashlib
import json
from pathlib import Path
import platform
import random
import time

CHECKS = 0


def check(condition, message="check failed"):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(message)


def parity(x):
    return x.bit_count() & 1


def basis(rows):
    piv = {}
    for r in rows:
        while r:
            j = r.bit_length() - 1
            if j in piv:
                r ^= piv[j]
            else:
                piv[j] = r
                break
    return [piv[j] for j in sorted(piv)]


def orthogonal(rows, n):
    p = {r.bit_length() - 1: r for r in basis(rows)}
    ans = []
    for j in range(n):
        if j in p:
            continue
        v = 1 << j
        for k, r in sorted(p.items()):
            if parity(r & v):
                v |= 1 << k
        ans.append(v)
    return ans


def in_span(x, rows):
    for r in reversed(basis(rows)):
        if x & (1 << (r.bit_length() - 1)):
            x ^= r
    return x == 0


AP3 = [
    [(0, 1, 2), (3, 4, 5), (6, 7, 8)],
    [(0, 3, 6), (1, 4, 7), (2, 5, 8)],
    [(0, 4, 8), (1, 5, 6), (2, 3, 7)],
    [(0, 5, 7), (1, 3, 8), (2, 4, 6)],
]
SAT12 = [
    [(0, 4, 8), (1, 5, 9), (2, 6, 10), (3, 7, 11)],
    [(0, 5, 10), (1, 4, 11), (2, 7, 8), (3, 6, 9)],
    [(0, 6, 11), (1, 7, 10), (2, 4, 9), (3, 5, 8)],
    [(0, 7, 9), (1, 6, 8), (2, 5, 11), (3, 4, 10)],
]


def flatten(parts):
    return [c for p in parts for c in p]


def valid_source(parts, n):
    return (all(sorted(v for c in p for v in c) == list(range(n)) for p in parts)
            and all(len(set(c) & set(d)) <= 1 for c, d in combinations(flatten(parts), 2)))


def nae(word, clauses):
    return all(0 < sum((word >> v) & 1 for v in c) < 3 for c in clauses)


def models(n, clauses, pins=None):
    pins = pins or {}
    return [x for x in range(1 << n) if all(((x >> v) & 1) == b for v, b in pins.items()) and nae(x, clauses)]


def nae_cnf(clauses):
    return [tuple(s * (v + 1) for v in c) for c in clauses for s in (1, -1)]


def unit_close(cnf, pins=None):
    """Only syntactic unit consequences. Pins are guarded assumptions."""
    out = dict(pins or {})
    scans = 0
    while True:
        scans += 1
        changed = False
        for c in cnf:
            if any(abs(l) - 1 in out and out[abs(l) - 1] == int(l > 0) for l in c):
                continue
            free = [l for l in c if abs(l) - 1 not in out]
            if not free:
                return None, scans
            if len(free) == 1:
                l = free[0]
                out[abs(l) - 1] = int(l > 0)
                changed = True
                break  # restart after each deduction
        if not changed:
            return out, scans  # stagnation, before any exhaustive branching


@dataclass(frozen=True)
class Arc:
    u: int
    v: int
    lo: int
    hi: int
    source: int = -1


def network(parts, n, pins=None):
    """Two triple partitions; parallel original arcs retain distinct IDs."""
    pins = pins or {}
    p, q = parts
    m = len(p)
    if len(q) != m or any(sorted(v for c in t for v in c) != list(range(n)) for t in (p, q)):
        raise ValueError("not two partitions")
    left = {v: 1 + i for i, c in enumerate(p) for v in c}
    right = {v: 1 + m + i for i, c in enumerate(q) for v in c}
    arcs = [Arc(0, 1 + i, 1, 2) for i in range(m)]
    arcs += [Arc(left[v], right[v], pins.get(v, 0), pins.get(v, 1), v) for v in range(n)]
    arcs += [Arc(1 + m + i, 0, 1, 2) for i in range(m)]
    return 1 + 2 * m, arcs


def feasible(V, arcs):
    """Integral lower-bound circulation by explicit augmenting paths."""
    graph = [[] for _ in range(V + 2)]
    demand = [0] * V
    locs = []

    def add(u, v, cap):
        if u == v:
            raise ValueError("self arcs unsupported in this source compiler")
        pos = len(graph[u])
        graph[u].append([v, len(graph[v]), cap])
        graph[v].append([u, pos, 0])
        return u, pos

    for a in arcs:
        if a.lo > a.hi:
            return None
        locs.append(add(a.u, a.v, a.hi - a.lo))
        demand[a.u] -= a.lo
        demand[a.v] += a.lo
    S, T = V, V + 1
    needed = 0
    for v, b in enumerate(demand):
        if b > 0:
            add(S, v, b)
            needed += b
        elif b < 0:
            add(v, T, -b)
    sent = 0
    while sent < needed:
        pred = {S: None}
        queue = deque([S])
        while queue and T not in pred:
            u = queue.popleft()
            for i, (v, rev, cap) in enumerate(graph[u]):
                if cap > 0 and v not in pred:
                    pred[v] = (u, i)
                    queue.append(v)
        if T not in pred:
            return None
        v, d = T, needed - sent
        while v != S:
            u, i = pred[v]
            d = min(d, graph[u][i][2])
            v = u
        v = T
        while v != S:
            u, i = pred[v]
            e = graph[u][i]
            e[2] -= d
            graph[v][e[1]][2] += d
            v = u
        sent += d
    flow = [a.hi - graph[u][i][2] for a, (u, i) in zip(arcs, locs)]
    check_flow(V, arcs, flow)
    return flow


def check_flow(V, arcs, flow):
    bal = [0] * V
    for a, f in zip(arcs, flow):
        check(a.lo <= f <= a.hi, (a, f))
        bal[a.u] -= f
        bal[a.v] += f
    check(not any(bal), bal)


def word_of(arcs, flow):
    return sum(f << a.source for a, f in zip(arcs, flow) if a.source >= 0)


def flow_of_word(parts, n, word):
    p, q = parts
    return ([sum((word >> v) & 1 for v in c) for c in p]
            + [(word >> v) & 1 for v in range(n)]
            + [sum((word >> v) & 1 for v in c) for c in q])


def residual(arcs, flow):
    out = []
    for i, (a, f) in enumerate(zip(arcs, flow)):
        if a.hi - a.lo not in (0, 1):
            raise ValueError("unit-width hypothesis required")
        if f < a.hi:
            out.append((a.u, a.v, i, 1, a.source))
        if f > a.lo:
            out.append((a.v, a.u, i, -1, a.source))
    return out


def odd_cycle(V, res, w, stats):
    """Find an odd-labeled simple directed cycle via a two-sheet lift."""
    adj = [[] for _ in range(V)]
    for i, (u, v, aid, delta, source) in enumerate(res):
        adj[u].append((v, i, int(source >= 0 and bool(w & (1 << source)))))
    stats['parity_queries'] = stats.get('parity_queries', 0) + 1
    for start in range(V):
        src, target = 2 * start, 2 * start + 1
        pred = {src: None}
        queue = deque([src])
        while queue and target not in pred:
            state = queue.popleft()
            u, p = state // 2, state % 2
            for v, ri, label in adj[u]:
                stats['lift_arc_scans'] = stats.get('lift_arc_scans', 0) + 1
                nxt = 2 * v + (p ^ label)
                if nxt not in pred:
                    pred[nxt] = (state, ri)
                    queue.append(nxt)
        if target not in pred:
            continue
        walk, state = [], target
        while state != src:
            state, ri = pred[state]
            walk.append(ri)
        walk.reverse()
        vertices, edges, where = [start], [], {start: 0}
        for ri in walk:
            u, v, *_ = res[ri]
            check(vertices[-1] == u)
            if v in where:
                j = where[v]
                cyc = edges[j:] + [ri]
                label = 0
                for e in cyc:
                    vsrc = res[e][4]
                    if vsrc >= 0:
                        label ^= int(bool(w & (1 << vsrc)))
                if label:
                    return cyc
                for z in vertices[j + 1:]:
                    del where[z]
                vertices = vertices[:j + 1]
                edges = edges[:j]
            else:
                edges.append(ri)
                where[v] = len(vertices)
                vertices.append(v)
        raise AssertionError("odd closed walk had no odd simple cycle")
    return None


def apply_cycle(flow, res, cycle):
    new = flow.copy()
    for r in cycle:
        _, _, i, delta, _ = res[r]
        new[i] += delta
    return new


def acquire_hull(V, arcs, n):
    f = feasible(V, arcs)
    stats = {'parity_queries': 0, 'lift_arc_scans': 0}
    if f is None:
        return None, [], [], stats
    anchor = word_of(arcs, f)
    res = residual(arcs, f)
    rows, identities, witnesses = [], [], []
    # M07's primal/dual bookkeeping: each oracle answer increases one rank.
    while len(rows) + len(identities) < n:
        w = next(w for w in orthogonal(rows, n) if not in_span(w, identities))
        cyc = odd_cycle(V, res, w, stats)
        if cyc is None:
            identities = basis(identities + [w])
        else:
            g = apply_cycle(f, res, cyc)
            check_flow(V, arcs, g)
            y = word_of(arcs, g)
            d = y ^ anchor
            check(parity(d & w) == 1)
            check(not in_span(d, rows))
            check(all(parity(d & z) == 0 for z in identities))
            rows = basis(rows + [d])
            witnesses.append({'word': y, 'cycle_arcs': [res[i][2] for i in cyc]})
    check(stats['parity_queries'] <= n)
    stats['annihilator_basis'] = identities
    return anchor, rows, witnesses, stats


def full_hull_certificate(parts, n):
    """Every unpinned pair has full affine hull: two disjoint matchings."""
    V, arcs = network(parts, n)
    exact = [Arc(a.u, a.v, 1, 1) if a.source < 0 else a for a in arcs]
    f = feasible(V, exact)
    check(f is not None)
    A = word_of(exact, f)
    second = [Arc(a.u, a.v, 0, 0, a.source) if a.source >= 0 and (A >> a.source) & 1 else a for a in exact]
    g = feasible(V, second)
    check(g is not None)
    B = word_of(second, g)
    check((A & B) == 0)
    check(nae(A, flatten(parts)) and nae(B, flatten(parts)))
    for e in range(n):
        M = B if (A >> e) & 1 else A
        check(not ((M >> e) & 1))
        check(nae(M ^ (1 << e), flatten(parts)))
    return {'matching_A': A, 'matching_B': B, 'unit_directions_certified': n}


def simple_cycles(V, res):
    """Explicit, potentially exponential catalogue, tests only."""
    adj = [[] for _ in range(V)]
    for i, e in enumerate(res):
        adj[e[0]].append((e[1], i))
    cycles = []
    for start in range(V):
        def dfs(v, seen, path):
            for u, i in adj[v]:
                if u == start:
                    cycles.append(path + [i])
                elif u > start and u not in seen:
                    dfs(u, seen | {u}, path + [i])
        dfs(start, {start}, [])
    return cycles


def euler_cycles(V, res, selected):
    """Decompose an Eulerian residual edge set; original arc IDs preserved."""
    remaining = set(selected)
    out = []
    while remaining:
        first = min(remaining)
        start = res[first][0]
        vertices, edges, where = [start], [], {start: 0}
        while True:
            v = vertices[-1]
            choices = [i for i in remaining if res[i][0] == v]
            check(bool(choices), 'non-Eulerian difference')
            i = min(choices)
            u = res[i][1]
            edges.append(i)
            if u in where:
                cyc = edges[where[u]:]
                out.append(cyc)
                remaining.difference_update(cyc)
                break
            where[u] = len(vertices)
            vertices.append(u)
    return out


def guarded_catalogue_check(parts, n):
    V, arcs = network(parts, n)
    f = feasible(V, arcs)
    res = residual(arcs, f)
    cats = simple_cycles(V, res)
    ids = {frozenset(c): i for i, c in enumerate(cats)}
    check(len(ids) == len(cats))
    masks = [sum(1 << e for e in c) for c in cats]
    rows = []
    for x in models(n, flatten(parts)):
        g = flow_of_word(parts, n, x)
        sel = {i for i, e in enumerate(res) if g[e[2]] != f[e[2]]}
        dec = euler_cycles(V, res, sel)
        check(all(frozenset(c) in ids for c in dec))
        check(sum(len(c) for c in dec) == len(sel))
        h = f.copy()
        for cyc in dec:
            h = apply_cycle(h, res, cyc)
        check(h == g)
        rows.append(len(dec))
    # All singleton and pair choices independently check capacity guards.
    legal = illegal = 0
    for i, j in combinations(range(len(cats)), 2):
        g = apply_cycle(apply_cycle(f, res, cats[i]), res, cats[j])
        bounded = all(a.lo <= z <= a.hi for a, z in zip(arcs, g))
        disjoint = not (masks[i] & masks[j])
        check(bounded == disjoint)
        if bounded:
            check_flow(V, arcs, g)
            check(nae(word_of(arcs, g), flatten(parts)))
            legal += 1
        else:
            illegal += 1
    return {'variables': n, 'cycles': len(cats), 'source_models': len(rows),
            'max_cycles_in_reconstruction': max(rows), 'legal_cycle_pairs': legal,
            'forbidden_cycle_pairs': illegal}


def chart_for_model(parts, n, word):
    """One opposite pair per triple; remove union-of-matchings cycles."""
    clauses = flatten(parts)
    chosen = [next((u, v) for u, v in combinations(c, 2) if ((word >> u) ^ (word >> v)) & 1) for c in clauses]
    repairs = 0
    while True:
        parent = list(range(n))
        def find(x):
            while parent[x] != x:
                x = parent[x]
            return x
        redundant = None
        for i, (u, v) in enumerate(chosen):
            a, b = find(u), find(v)
            if a == b:
                redundant = i
                break
            parent[a] = b
        if redundant is None:
            groups = {}
            for v in range(n):
                groups.setdefault(find(v), []).append(v)
            check(len(groups) == n // 3)
            return [sum(1 << v for v in group) for group in groups.values()], repairs
        u, v = chosen[redundant]
        w = next(z for z in clauses[redundant] if z not in (u, v))
        chosen[redundant] = (u, w) if ((word >> u) ^ (word >> w)) & 1 else (v, w)
        repairs += 1
        check(repairs <= n)


def selector_encoding(cnf):
    """3SAT -> disjoint ternary XOR rows + negative binary conflicts."""
    lits = [l for c in cnf for l in c]
    groups = [tuple(range(3 * i, 3 * i + 3)) for i in range(len(cnf))]
    conflicts = {tuple(sorted((i, j))) for g in groups for i, j in combinations(g, 2)}
    conflicts.update((i, j) for i, j in combinations(range(len(lits)), 2) if lits[i] == -lits[j])
    return lits, groups, sorted(conflicts)


def selector_models(cnf):
    lits, groups, conflicts = selector_encoding(cnf)
    ans = []
    # Explicit exactly-one enumeration, equivalent to XOR plus pair guards.
    for choice in product(range(3), repeat=len(groups)):
        selected = {3 * i + z for i, z in enumerate(choice)}
        if any(i in selected and j in selected for i, j in conflicts):
            continue
        assignment = {}
        for i in selected:
            assignment[abs(lits[i]) - 1] = int(lits[i] > 0)
        w = sum(v << i for i, v in assignment.items())
        check(all(any(((w >> (abs(l) - 1)) & 1) == int(l > 0) for l in c) for c in cnf))
        ans.append(w)
    return ans


def controls():
    rng = random.Random(2091124)
    out = {'seed': 2091124, 'source_cases': [], 'flow_contexts': [], 'cycle_catalogues': [], 'selector_cases': []}
    for name, parts, n in [('AP3_UNSAT', AP3, 9), ('SAT12', SAT12, 12)]:
        check(valid_source(parts, n))
        full = models(n, flatten(parts))
        closed, scans = unit_close(nae_cnf(flatten(parts)))
        check(closed == {})
        halves = []
        for half in (parts[:2], parts[2:]):
            V, arcs = network(half, n)
            a, U, ws, stats = acquire_hull(V, arcs, n)
            ref = models(n, flatten(half))
            refbasis = basis([x ^ ref[0] for x in ref])
            check(a in ref and len(U) == len(refbasis))
            check(all(in_span(x ^ a, U) for x in ref))
            check(all(w['word'] in ref for w in ws))
            halves.append({'models': len(ref), 'anchor': a, 'hull_rank': len(U), 'basis': U, 'actual_witnesses': ws,
                           'full_hull_certificate': full_hull_certificate(half, n), **stats})
        out['source_cases'].append({'name': name, 'variables': n, 'partitions': parts, 'models': len(full), 'witness': full[0] if full else None,
                                    'unit_closure_pins': closed, 'unit_closure_scans': scans, 'halves': halves})
        # Every supplied SAT model gets a certified n/3-dimensional chart.
        repairs = 0
        chart_tests = 0
        for x in full if full else models(n, flatten(parts[:2])):
            U, r = chart_for_model(parts[:2], n, x)
            repairs += r
            for s in range(1 << len(U)):
                z = x
                for j, u in enumerate(U):
                    if (s >> j) & 1:
                        z ^= u
                check(nae(z, flatten(parts[:2])))
                chart_tests += 1
        out['source_cases'][-1]['forest_chart_checks'] = chart_tests
        out['source_cases'][-1]['cycle_replacements'] = repairs
    check(out['source_cases'][0]['models'] == 0)
    check(out['source_cases'][1]['models'] == 90)
    check(all(h['models'] == 102 and h['hull_rank'] == 9 for h in out['source_cases'][0]['halves']))
    # A symbolic cap-size proof accompanies these independent finite checks.
    lines = flatten(AP3)
    caps = [x for x in range(512) if not any(all((x >> v) & 1 for v in c) for c in lines)]
    check(max(x.bit_count() for x in caps) == 4)
    out['AP3_cap_maximum'] = 4
    deletions = []
    for i in range(len(lines)):
        ms = models(9, lines[:i] + lines[i + 1:])
        deletions.append({'deleted_clause': i, 'models': len(ms), 'witness': ms[0] if ms else None})
    out['AP3_clause_deletions'] = deletions
    # One signed-literal neighbor, all positions: source enumeration only.
    signed_neighbors = []
    for ci, c in enumerate(lines):
        for vi in c:
            ms = [x for x in range(512) if all(len({((x >> v) & 1) ^ int(j == ci and v == vi) for v in t}) == 2 for j, t in enumerate(lines))]
            signed_neighbors.append({'clause': ci, 'variable': vi, 'models': len(ms), 'witness': ms[0] if ms else None})
    out['AP3_sign_neighbors'] = signed_neighbors
    # Genuine one-CNF-clause SAT/UNSAT neighbors in the residual domain.
    residual_cnf = nae_cnf(lines[1:])
    def cnf_models(cnf):
        return [x for x in range(512) if all(any(((x >> (abs(l) - 1)) & 1) == int(l > 0) for l in cl) for cl in cnf)]
    check(not cnf_models(residual_cnf))
    neighbors = []
    for i in range(len(residual_cnf)):
        cnf = residual_cnf[:i] + residual_cnf[i + 1:]
        ms = cnf_models(cnf)
        closed, scans = unit_close(cnf)
        check(bool(ms))
        check(closed == {})
        neighbors.append({'deleted_CNF_clause': i, 'models': len(ms), 'witness': ms[0], 'closure_scans': scans})
    out['one_CNF_clause_neighbors'] = {'UNSAT_CNF': residual_cnf, 'SAT_neighbors': neighbors}
    out['AP3_two_NAE_deletions'] = []
    for i, j in combinations(range(len(lines)), 2):
        ms = models(9, [c for k, c in enumerate(lines) if k not in (i, j)])
        check(bool(ms))
        out['AP3_two_NAE_deletions'].append({'deleted': [i, j], 'models': len(ms), 'witness': ms[0]})
    # Pairwise projections do not distinguish the AP3 half supports either.
    for half in (AP3[:2], AP3[2:]):
        ref = models(9, flatten(half))
        for i, j in combinations(range(9), 2):
            check(len({((x >> i) & 1, (x >> j) & 1) for x in ref}) == 4)
    out['AP3_all_two_coordinate_projections_full'] = True
    # Pins create both feasible and infeasible circulation instances.
    for k in range(120):
        n, parts = (9, AP3[:2]) if k < 90 else (12, SAT12[:2])
        pins = {v: rng.randrange(2) for v in rng.sample(range(n), rng.randrange(0, min(n, 6) + 1))}
        closed, scans = unit_close(nae_cnf(flatten(parts)), pins)
        ref = models(n, flatten(parts), pins)
        if closed is None:
            check(not ref)
            active = pins
        else:
            check(all(all(((x >> v) & 1) == b for v, b in closed.items()) for x in ref))
            active = closed
        V, arcs = network(parts, n, active)
        a, U, ws, stats = acquire_hull(V, arcs, n)
        check((a is not None) == bool(ref))
        if ref:
            check(a in ref)
            rb = basis([x ^ a for x in ref])
            check(len(U) == len(rb))
            check(all(in_span(x ^ a, U) for x in ref))
            check(all(w['word'] in ref for w in ws))
            # Single parity feasibility is genuinely polynomial via odd cycles.
            f = feasible(V, arcs)
            for _ in range(4):
                w, b = rng.randrange(1 << n), rng.randrange(2)
                possible = parity(w & a) == b or odd_cycle(V, residual(arcs, f), w, stats) is not None
                check(possible == any(parity(w & x) == b for x in ref))
        out['flow_contexts'].append({'variables': n, 'pins': pins, 'closure': closed, 'models': len(ref), 'hull_rank': len(U) if ref else None,
                                     'closure_scans': scans, **stats})
    for parts, n in [(AP3[:2], 9), (AP3[2:], 9), (SAT12[:2], 12)]:
        out['cycle_catalogues'].append(guarded_catalogue_check(parts, n))
    # Generic mixed affine/negative-2CNF hardness reduction controls.
    base = [tuple((v + 1) * (1 if (b >> v) & 1 else -1) for v in range(3)) for b in range(8)]
    cnfs = [base] + [base[:j] + base[j + 1:] for j in range(8)]
    for _ in range(32):
        cnfs.append([tuple((v + 1) * rng.choice((-1, 1)) for v in rng.sample(range(5), 3)) for _ in range(rng.randrange(1, 7))])
    for cnf in cnfs:
        n = max(abs(l) for c in cnf for l in c)
        closed, scans = unit_close(cnf)
        ref = [x for x in range(1 << n) if all(any(((x >> (abs(l) - 1)) & 1) == int(l > 0) for l in c) for c in cnf)]
        got = selector_models(cnf)
        check(bool(got) == bool(ref))
        out['selector_cases'].append({'clauses': cnf, 'source_models': len(ref), 'selector_witnesses': len(got), 'closure': closed, 'closure_scans': scans})
    # Explicit positive/negative closure controls.
    for cnf, expect in [([(1,), (-1, 2), (-2, 3)], {0: 1, 1: 1, 2: 1}), ([(1,), (-1,)], None)]:
        got, scans = unit_close(cnf)
        check(got == expect)
    out['totals'] = {'flow_contexts': len(out['flow_contexts']),
                     'flow_SAT': sum(x['models'] > 0 for x in out['flow_contexts']),
                     'flow_UNSAT': sum(x['models'] == 0 for x in out['flow_contexts']),
                     'selector_controls': len(cnfs),
                     'selector_SAT': sum(x['source_models'] > 0 for x in out['selector_cases']),
                     'selector_UNSAT': sum(x['source_models'] == 0 for x in out['selector_cases'])}
    return out


def circulant(k):
    edges = [(i, (i + d) % k) for i in range(k) for d in (0, 1, 2)]
    p = [tuple(e for e, (u, v) in enumerate(edges) if u == i) for i in range(k)]
    q = [tuple(e for e, (u, v) in enumerate(edges) if v == i) for i in range(k)]
    return [p, q], edges


def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def scaling():
    rows = []
    for k in (3, 4, 5, 6, 8, 10, 12):
        parts, edges = circulant(k)
        n = 3 * k
        V, arcs = network(parts, n)
        base = sum(1 << i for i, (u, v) in enumerate(edges) if u == v)
        f = flow_of_word(parts, n, base)
        check_flow(V, arcs, f)
        res = residual(arcs, f)
        ri = {r[2]: j for j, r in enumerate(res)}
        source_arc = {a.source: i for i, a in enumerate(arcs) if a.source >= 0}
        eindex = {e: i for i, e in enumerate(edges)}
        paths = []
        def visit(path):
            v = path[-1]
            if v == k - 1:
                paths.append(path)
            for d in (1, 2):
                if v + d <= k - 1:
                    visit(path + [v + d])
        visit([0])
        supports = set()
        for path in paths:
            cyc = []
            for u, v in zip(path, path[1:] + [0]):
                cyc.append(ri[source_arc[eindex[(u, v)]]])
                cyc.append(ri[source_arc[eindex[(v, v)]]])
            check(all(res[cyc[i]][1] == res[cyc[(i + 1) % len(cyc)]][0] for i in range(len(cyc))))
            check(len({res[j][0] for j in cyc}) == len(cyc))
            g = apply_cycle(f, res, cyc)
            check_flow(V, arcs, g)
            check(nae(word_of(arcs, g), flatten(parts)))
            supports.add(frozenset(cyc))
        check(len(supports) == fibonacci(k))
        rows.append({'k': k, 'variables': n, 'explicit_distinct_required_cycles': len(supports), 'F_k': fibonacci(k)})
    # Polynomial hull acquisition on a larger explicit family, no exhaustive ref.
    hulls = []
    for k in (3, 6, 12, 24):
        parts, edges = circulant(k)
        n = 3 * k
        V, arcs = network(parts, n)
        a, U, ws, stats = acquire_hull(V, arcs, n)
        check(nae(a, flatten(parts)))
        check(all(nae(w['word'], flatten(parts)) for w in ws))
        hulls.append({'k': k, 'variables': n, 'rank': len(U), 'actual_witnesses': len(ws),
                      'full_hull_certificate': full_hull_certificate(parts, n), **stats})
    return {'fibonacci_family': rows, 'hull_scaling': hulls,
            'note': 'Finite scaling checks do not establish asymptotics; the report supplies symbolic proofs. No all-cycle enumeration is used by hull acquisition.'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stage', choices=['controls', 'scaling'], required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    start = time.perf_counter()
    out = controls() if args.stage == 'controls' else scaling()
    out['execution'] = {'stage': args.stage, 'assertions': CHECKS, 'elapsed_seconds': time.perf_counter() - start,
                        'python': platform.python_version(), 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                        'memory_measurement': 'No physical peak-memory or cumulative-memory measurement; analytic ledger in report.'}
    args.output.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({'output': str(args.output), 'totals': out.get('totals'), 'execution': out['execution']}, indent=2))


if __name__ == '__main__':
    main()
