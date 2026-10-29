#!/usr/bin/env python3
"""Finite tests of static boundary plus syntactic 2CNF-backdoor burden.

Every formula is an actual connected proper signed exact-(2,2) 3CNF.
Small cases exhaust ALL boundary sets and compute exact local hitting minima.
Large cases report achieved decompositions, not a global optimum over boundaries.
No SAT runtime lower bound follows from the structural inequalities.
"""
from __future__ import annotations
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from math import ceil, sqrt
from pathlib import Path
import random
import time

HERE = Path(__file__).resolve().parent
SEED = 202610291455


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    obj = importlib.util.module_from_spec(spec); spec.loader.exec_module(obj)
    return obj


CYCLE = module('cycle230', HERE/'inputs/MIXED_PORT_CYCLE230_repro.py')
TORUS = module('torus232', HERE/'inputs/MATCHED_TORUS_BRIDGE232_repro.py')
ORIGINAL = module('original_static', HERE/'inputs/ORIGINAL_CONNECTED_INTERFACE_audit.py')


def validate(clauses):
    n = max(abs(l) for c in clauses for l in c)
    assert all(len(c) == 3 and len(set(map(abs, c))) == 3 for c in clauses)
    occ = Counter(l for c in clauses for l in c)
    assert set(map(abs, occ)) == set(range(1, n+1))
    assert all(occ[v] == occ[-v] == 2 for v in range(1, n+1))
    assert 3*len(clauses) == 4*n
    assert len(clauses) == len(set(tuple(sorted(c)) for c in clauses))
    edge_masks = tuple(sum(1 << (abs(l)-1) for l in c) for c in clauses)
    adjacency = [0]*n
    for edge in edge_masks:
        for v in bits(edge):
            adjacency[v] |= edge ^ (1 << v)
    assert len(components(adjacency, (1 << n)-1)) == 1
    return n, edge_masks, adjacency


def bits(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length()-1
        mask ^= low


def components(adjacency, private):
    remaining, out = private, []
    while remaining:
        frontier, seen = remaining & -remaining, 0
        while frontier:
            v = (frontier & -frontier).bit_length()-1
            frontier &= frontier-1
            if seen >> v & 1:
                continue
            seen |= 1 << v
            frontier |= adjacency[v] & private & ~seen
        out.append(seen); remaining &= ~seen
    return out


def integer_bounds(n):
    # First bound is the user's continuous consequence, rounded upward.
    old_ceil = ceil(sqrt(n/3)-.25-1e-12)
    # Exact minimization over integer pairs satisfying ONLY the old inequality.
    old_integer = ceil(n/3)  # b=0 case is handled separately.
    for b in range(1, old_integer+1):
        q = max(0, (n-3*b+12*b-1)//(12*b))
        old_integer = min(old_integer, b+q)
    s = 0
    while 3*s+9*(s*s//4) < n:
        s += 1
    return {'user_continuous': sqrt(n/3)-.25,
            'user_rounded': old_ceil, 'old_exact_integer_relaxation': old_integer,
            'stronger_continuous': 2/3*(sqrt(n+1)-1), 'stronger_exact_integer': s}


def quotient_check(n, edges, adjacency, boundary, qs):
    comps = components(adjacency, ((1 << n)-1) ^ boundary)
    b, k, q = boundary.bit_count(), len(comps), max(qs, default=0)
    h = sum(edge & ~boundary == 0 for edge in edges)
    assert len(qs) == k
    assert k+h <= 3*b+1
    assert n <= 3*(b+sum(qs))
    assert n <= 3*b+3*(3*b+1-h)*q
    assert n <= 3*(b+q)+9*b*q
    assert 3*(b+q)+9*((b+q)**2//4) >= n
    if b:
        assert k <= 4*b and n <= 3*b+12*b*q
    else:
        assert k == 1 and q >= ceil(n/3)
    return {'b': b, 'q': q, 'burden': b+q, 'components': k,
            'boundary_only_clauses': h, 'component_sizes': [c.bit_count() for c in comps]}


def exact_hitting_engine(edges, n):
    cover = [0]*n
    for i, edge in enumerate(edges):
        for v in bits(edge): cover[v] |= 1 << i
    stats = Counter()
    @lru_cache(None)
    def solve(state):
        stats['hitting_states'] += 1
        if not state:
            return 0, 0
        frequency = [(cover[v] & state).bit_count() for v in range(n)]
        lower = (state.bit_count()+max(frequency)-1)//max(frequency)
        first = (state & -state).bit_length()-1
        best, witness = n+1, 0
        for v in sorted(bits(edges[first]), key=lambda x: -frequency[x]):
            q, hit = solve(state & ~cover[v])
            if q+1 < best:
                best, witness = q+1, hit | (1 << v)
            if best == lower:
                break
        return best, witness
    return solve, stats


def independent_dpll(clauses, node_budget=5000):
    """Ordinary uniform DPLL with paid component factoring and a sound cap."""
    original = tuple(tuple(c) for c in clauses)
    stats = Counter()
    started = time.perf_counter()
    class Budget(Exception):
        pass
    def restrict(cs, variable, value):
        good = variable if value else -variable
        out = []
        for c in cs:
            stats['literal_inspections'] += len(c)
            if good not in c:
                out.append(tuple(l for l in c if l != -good))
        return tuple(out)
    def search(cs, assignment):
        stats['nodes'] += 1
        if stats['nodes'] > node_budget:
            raise Budget()
        stats['peak_assigned_variables'] = max(stats['peak_assigned_variables'],len(assignment))
        while True:
            if any(not c for c in cs):
                return None
            unit = next((c[0] for c in cs if len(c) == 1), None)
            if unit is None:
                break
            variable, value = abs(unit), int(unit > 0)
            if variable in assignment and assignment[variable] != value:
                return None
            assignment = {**assignment,variable:value}
            stats['unit_steps'] += 1
            cs = restrict(cs, variable, value)
        if not cs:
            return assignment
        # Exact AND factoring; selecting a small component does not use its answer.
        graph = {}
        for c in cs:
            vs = set(map(abs,c));stats['component_literal_scans'] += len(c)
            for v in vs:graph.setdefault(v,set()).update(vs-{v})
        remaining, blocks = set(graph), []
        while remaining:
            queue, reached = [min(remaining)], set()
            for v in queue:
                if v not in reached:
                    reached.add(v);queue.extend(graph[v]-reached)
            remaining -= reached;blocks.append(reached)
        if len(blocks) > 1:
            out = dict(assignment)
            for block in sorted(blocks,key=lambda q:(len(q),min(q))):
                sub = tuple(c for c in cs if abs(c[0]) in block)
                answer = search(sub,{})
                if answer is None:return None
                out.update(answer)
            return out
        width = min(map(len,cs))
        counts = Counter(abs(l) for c in cs if len(c)==width for l in c)
        variable = max(counts,key=lambda v:(counts[v],v))
        positives = sum(variable in c for c in cs)
        negatives = sum(-variable in c for c in cs)
        preferred = int(positives >= negatives)
        for value in (preferred,1-preferred):
            stats['decision_branches'] += 1
            result = search(restrict(cs,variable,value),{**assignment,variable:value})
            if result is not None:return result
        return None
    try:
        witness = search(original,{})
    except Budget:
        return {'answer':'UNKNOWN','stats':dict(stats),'seconds':time.perf_counter()-started}
    if witness is not None:
        assert all(any(witness.get(abs(l),0)==int(l>0) for l in c) for c in original)
    return {'answer':'SAT' if witness is not None else 'UNSAT', 'stats':dict(stats),
            'seconds':time.perf_counter()-started}


def all_boundary_audit(name, clauses):
    n, edges, adjacency = validate(clauses)
    assert n <= 15
    solve, stats = exact_hitting_engine(edges, n)
    minima, witnesses = {}, {}
    checks = 0
    minimum = n+1
    best = None
    first_violation = None
    for boundary in range(1 << n):
        comps = components(adjacency, ((1 << n)-1) ^ boundary)
        qs, hits = [], []
        for comp in comps:
            state = sum(1 << i for i, edge in enumerate(edges) if edge & boundary == 0 and edge & comp)
            q, hit = solve(state)
            assert hit & ~comp == 0
            assert all(hit & edges[i] for i in bits(state))
            assert hit.bit_count() == q
            qs.append(q); hits.append(hit)
        row = quotient_check(n, edges, adjacency, boundary, qs)
        b, q = row['b'], row['q']
        checks += 1
        if b not in minima or q < minima[b]:
            minima[b] = q; witnesses[b] = boundary
        if b+q < minimum:
            minimum = b+q
            best = {**row, 'boundary_1based': [v+1 for v in bits(boundary)],
                    'private_hitting_sets_1based': [[v+1 for v in bits(h)] for h in hits]}
    return {'name': name, 'n': n, 'm': len(edges), 'boundary_sets': checks,
            'global_burden_optimum_exact': minimum, 'best': best,
            'q_minimum_by_b': [{'b': b, 'q': minima[b], 'boundary_mask': witnesses[b]}
                               for b in sorted(minima)],
            'bounds': integer_bounds(n), 'exact_hitting_cache_states': stats['hitting_states'],
            'violations': first_violation}


def milp_hitting(edge_masks, time_limit=1.0):
    """Feasible hitting witness, plus a solver-optimal flag; no free oracle."""
    if not edge_masks:
        return {'q': 0, 'mask': 0, 'optimal': True, 'exact_combinatorial': True, 'seconds': 0.0}
    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, milp
    from scipy.sparse import csc_matrix
    variables = sorted(set(v for e in edge_masks for v in bits(e)))
    index = {v: i for i, v in enumerate(variables)}
    rows, columns = [], []
    for i, edge in enumerate(edge_masks):
        for v in bits(edge): rows.append(i); columns.append(index[v])
    matrix = csc_matrix((np.ones(len(rows)), (rows, columns)), shape=(len(edge_masks), len(variables)))
    t0 = time.perf_counter()
    result = milp(np.ones(len(variables)), integrality=np.ones(len(variables)),
                  bounds=Bounds(0, 1), constraints=LinearConstraint(matrix, 1, np.inf),
                  options={'time_limit': time_limit, 'mip_rel_gap': 0.0, 'disp': False})
    if result.x is None:
        # Deterministic greedy incumbent, still a valid finite upper bound.
        remaining, mask = list(edge_masks), 0
        while remaining:
            counts = Counter(v for edge in remaining for v in bits(edge))
            v = min(counts, key=lambda x: (-counts[x], x))
            mask |= 1 << v
            remaining = [e for e in remaining if not e >> v & 1]
    else:
        mask = sum(1 << v for i, v in enumerate(variables) if result.x[i] > .5)
    assert all(mask & edge for edge in edge_masks)
    counts = Counter(v for e in edge_masks for v in bits(e))
    counting_lower = ceil(len(edge_masks)/max(counts.values()))
    # Disjoint clauses provide an independent exact integer lower bound.
    disjoint, occupied = 0, 0
    for edge in edge_masks:
        if not edge & occupied:
            disjoint += 1; occupied |= edge
    lower = max(counting_lower, disjoint)
    return {'q': mask.bit_count(), 'mask': mask, 'optimal': result.status == 0,
            'exact_combinatorial': mask.bit_count() == lower, 'combinatorial_lower': lower,
            'solver_dual_bound': None if getattr(result, 'mip_dual_bound', None) is None else float(result.mip_dual_bound),
            'seconds': time.perf_counter()-t0}


def evaluate_boundary(clauses, boundary, cache):
    n, edges, adjacency = validate(clauses)
    comps = components(adjacency, ((1 << n)-1)^boundary)
    info = []
    for comp in comps:
        local = tuple(e for e in edges if not e & boundary and e & comp)
        if local not in cache:
            cache[local] = milp_hitting(local)
        info.append(cache[local])
    row = quotient_check(n, edges, adjacency, boundary, [q['q'] for q in info])
    return {**row, 'boundary_1based': [v+1 for v in bits(boundary)],
            'hitting_sets_1based': [[v+1 for v in bits(q['mask'])] for q in info],
            'all_local_solver_optimal': all(q['optimal'] for q in info),
            'all_local_exact_combinatorial': all(q['exact_combinatorial'] for q in info),
            'hitting_search_seconds': sum(q['seconds'] for q in info)}


def cycle_case(k):
    sat = CYCLE.build_cycle(k, ['M']*k)
    unsat = CYCLE.build_cycle(k, ['W']+['M']*(k-1))
    n, edges, _ = validate(sat); validate(unsat)
    assert [set(map(abs, c)) for c in sat] == [set(map(abs, c)) for c in unsat]
    # Evaluate chosen static cuts; this is not global boundary optimization.
    candidates = []
    for r in range(k+1):
        boundary = sum(1 << (15*(j*k//r)) for j in range(r)) if r else 0
        candidates.append(boundary)
    cache = {}
    rows = [evaluate_boundary(sat, b, cache) for b in dict.fromkeys(candidates)]
    best = min(rows, key=lambda r: r['burden'])
    # Independently acquired exact local source relations decide both labels.
    profiles = {}
    for typ, source in [('M', CYCLE.SOURCE_M), ('W', CYCLE.SOURCE_W1)]:
        counts, models, unpinned, residual_count = CYCLE.profile_exhaustive(source)
        profiles[typ] = {'counts': counts, 'models': models}
    def ring_sat(types):
        for start in (0, 1):
            reachable = {start}
            for typ in types:
                reachable = {b for a in reachable for b in (0, 1)
                             if profiles[typ]['counts'][a,b]}
            if start in reachable:
                return True
        return False
    assert ring_sat(['M']*k) and not ring_sat(['W']+['M']*(k-1))
    # Original-clause verification of a constructed SAT witness.
    assignment = {}
    for i in range(k):
        mask = profiles['M']['models'][0,0]
        assignment.update({15*i+v+1: (mask >> v) & 1 for v in range(15)})
    assert TORUS.sat_formula(sat, assignment)
    decisions = [independent_dpll(sat),independent_dpll(unsat)]
    assert decisions[0]['answer'] in ('SAT','UNKNOWN')
    assert decisions[1]['answer'] in ('UNSAT','UNKNOWN')
    return {'family': 'matched connected W/M cycle', 'k': k, 'n': n, 'm': len(sat),
            'labels': ['SAT','UNSAT'], 'identical_unsigned_scopes': True,
            'profile_acquisition_source_assignments': 2*(1 << 15),
            'exact_semantic_ring_states': 2, 'bounds': integer_bounds(n),
            'best_tested_decomposition': best, 'all_tested_decompositions': rows,
            'global_boundary_optimum_claimed': False, 'independent_DPLL': decisions}


def torus_case(L):
    torus, known_witness = TORUS.torus(L)
    sat, info = TORUS.connector(torus, TORUS.V)
    unsat, _ = TORUS.connector(torus, TORUS.W1)
    n, _, _ = validate(sat); validate(unsat)
    assert [set(map(abs,c)) for c in sat] == [set(map(abs,c)) for c in unsat]
    candidates = [0]
    for r in sorted({1, 2, max(1, L//3)}):
        columns = set()
        for j in range(r):
            c = (j*L//r) % L
            columns.update((c, (c+1)%L))
        candidates.append(sum(1 << (row*L+col) for row in range(L) for col in columns))
    # The original construction has exactly 45 added variables; removing those
    # is another explicitly paid candidate, not a hidden solution bit.
    candidates.append(((1 << 45)-1) << (L*L))
    cache = {}
    rows = [evaluate_boundary(sat, b, cache) for b in dict.fromkeys(candidates)]
    decisions = [independent_dpll(sat),independent_dpll(unsat)]
    assert decisions[0]['answer'] in ('SAT','UNKNOWN')
    assert decisions[1]['answer'] in ('UNSAT','UNKNOWN')
    return {'family': 'matched torus plus exact22 AND connector', 'L': L, 'n': n, 'm': len(sat),
            'labels_from_source_theorem': ['SAT','UNSAT'], 'identical_unsigned_scopes': True,
            'bounds': integer_bounds(n), 'best_tested_decomposition': min(rows,key=lambda r:r['burden']),
            'all_tested_decompositions': rows, 'global_boundary_optimum_claimed': False,
            'independent_DPLL': decisions,
            'label_validation': 'Source connector theorem plus separately coded capped ordinary DPLL; no exhaustive n-variable assignment claim.'}


def small_case(which):
    if which == 'W1':
        clauses = list(TORUS.W1)
    else:
        clauses = ORIGINAL.canonical_signed(int(which))
    result = all_boundary_audit(which, clauses)
    n = result['n']
    models = [a for a in range(1 << n)
              if all(any(((a >> (abs(l)-1)) & 1) == int(l>0) for l in c) for c in clauses)]
    result['source_models'] = len(models)
    decision=independent_dpll(clauses)
    assert decision['answer'] == ('SAT' if models else 'UNSAT')
    result['independent_DPLL'] = decision
    if which == 'W1':
        other = TORUS.V
        other_models = [a for a in range(1 << n)
                        if all(any(((a >> (abs(l)-1)) & 1) == int(l>0) for l in c) for c in other)]
        assert not models and len(other_models) == 54
        assert [set(map(abs,c)) for c in clauses] == [set(map(abs,c)) for c in other]
        result['matched_sign_mutant_models'] = len(other_models)
        result['all_boundary_structural_results_identical_for_mutant'] = True
    return result


def periodic_scaling():
    rows = []
    for n in (30, 60, 120, 300, 600):
        cs = ORIGINAL.canonical_signed(n)
        validate(cs)
        t0 = time.perf_counter()
        sat, width, peak, transitions = ORIGINAL.frontier_dp(cs,n)
        assert sat and width <= 4 and peak <= 16
        rows.append({'n': n, 'm': len(cs), 'bounds': integer_bounds(n),
                     'global_syntactic_backdoor_exact': n//3, 'SAT': sat,
                     'moving_frontier_width': width, 'peak_states': peak,
                     'transitions': transitions, 'seconds': time.perf_counter()-t0})
    return {'rows': rows, 'runtime_lower_bound_claimed': False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--stage', choices=('small','cycle','torus','periodic'), required=True)
    p.add_argument('--case', default='W1')
    args = p.parse_args()
    t0 = time.perf_counter()
    if args.stage == 'small': result = small_case(args.case)
    elif args.stage == 'cycle': result = cycle_case(int(args.case))
    elif args.stage == 'torus': result = torus_case(int(args.case))
    else: result = periodic_scaling()
    output = {'run_id': 'BOUNDARY_BURDEN1', 'seed': SEED, 'stage': args.stage, 'case': args.case,
              'status': 'COMPUTATIONAL; structural derivation separate; P versus NP OPEN',
              'code_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'source_sha256': {q.name:sha256(q.read_bytes()).hexdigest() for q in (HERE/'inputs').glob('*.py')},
              'elapsed_seconds': time.perf_counter()-t0, 'result': result}
    path = HERE/('BOUNDARY_BURDEN1_'+args.stage+'_'+args.case+'.json')
    path.write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
    summary = {k: result[k] for k in ('n','m','boundary_sets','global_burden_optimum_exact','best_tested_decomposition') if k in result}
    if 'best_tested_decomposition' in summary:
        summary['best_tested_decomposition']={k:v for k,v in summary['best_tested_decomposition'].items() if k in ('b','q','burden','components','all_local_solver_optimal','all_local_exact_combinatorial')}
    print(json.dumps({'output':str(path),'elapsed_seconds':output['elapsed_seconds'],**summary}))


if __name__ == '__main__':
    main()
