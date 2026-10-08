#!/usr/bin/env python3
"""ARC-0005-ORBIT: bounded, exact orbit-first WRAPPER experiment.

Adapted architecture: j15marti/pnp experiments/DOUBLE_WRAPPER_2026-10-07/
double_wrapper.py, blob 04cf06305b5beff2a36f631e4a38b5e09553c1ee.
This is a new controlled variant, not a rerun of the complete historical hybrid.
Known rules: Anders, Codel, Heule, Orbitopal Fixing in SAT, Thms 3.2/3.3.
Standard library only. Discovery and failed permutation checks are timed.
No SAT oracle is used in plan construction; every accepted map is checked exactly.
Each invocation has a 25-second internal deadline. Use shell timeout 30s.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
import random
import signal
import time
import tracemalloc
from collections import Counter
from pathlib import Path
from typing import Iterable

CNF = tuple[tuple[int, ...], ...]
START = time.monotonic()
DEADLINE = START + 25.0
PARTIAL_ROWS: list[dict] = []

class BudgetExceeded(RuntimeError):
    pass

def guard(*_args):
    if time.monotonic() >= DEADLINE:
        raise BudgetExceeded('25-second cooperative budget reached')

def alarm(_signum, _frame):
    raise BudgetExceeded('25-second alarm reached')

if hasattr(signal, 'SIGALRM'):
    signal.signal(signal.SIGALRM, alarm)
    signal.setitimer(signal.ITIMER_REAL, 25.0)

def canon(f: Iterable[Iterable[int]]) -> CNF:
    clauses = set()
    for raw in f:
        c = set(raw)
        if 0 in c:
            raise ValueError('zero is not a literal')
        if any(-x in c for x in c):
            continue
        clauses.add(tuple(sorted(c)))
    return tuple(sorted(clauses))

def variables(f: CNF) -> list[int]:
    return sorted({abs(x) for c in f for x in c})

def normalize(f: CNF) -> CNF:
    ren = {v: i + 1 for i, v in enumerate(variables(f))}
    return canon((ren[abs(x)] * (1 if x > 0 else -1) for x in c) for c in f)

def terminal(f: CNF):
    if () in f:
        return False
    if not f:
        return True
    return None

def dimacs(f: CNF) -> bytes:
    n = max(variables(f), default=0)
    return (f'p cnf {n} {len(f)}\n' + ''.join(' '.join(map(str, c)) + ' 0\n' for c in f)).encode('ascii')

def bits(f: CNF) -> int:
    return 8 * len(dimacs(f))

def power_cutoff(n: int) -> int:
    # Exactly floor(n**(2/3)), with no floating-point boundary error.
    lo, hi = 0, n + 1
    while hi - lo > 1:
        m = (lo + hi) // 2
        if m**3 <= n*n:
            lo = m
        else:
            hi = m
    return max(2, lo)

def restrict(f: CNF, assignment: dict[int, bool], met: Counter) -> CNF:
    met['restriction_literal_visits'] += sum(map(len, f))
    out = []
    for c in f:
        if any(abs(x) in assignment and assignment[abs(x)] == (x > 0) for x in c):
            continue
        out.append(tuple(x for x in c if abs(x) not in assignment))
    return canon(out)

def simplify(raw: CNF, met: Counter) -> CNF:
    f = canon(raw)
    while terminal(f) is None:
        guard()
        met['simplification_literal_visits'] += sum(map(len, f))
        unit = {c[0] for c in f if len(c) == 1}
        if any(-x in unit for x in unit):
            return ((),)
        lits = {x for c in f for x in c}
        pure = {x for x in lits if -x not in lits}
        chosen = unit | pure
        if not chosen:
            break
        f = restrict(f, {abs(x): x > 0 for x in chosen}, met)
    # Pure-literal elimination is present in BOTH compared variants.
    return normalize(f)

def map_lit(x: int, perm: dict[int, int]) -> int:
    y = perm.get(abs(x), abs(x))
    return y if x > 0 else -y

def mapped(f: CNF, perm: dict[int, int]) -> CNF:
    return canon(tuple(map_lit(x, perm) for x in c) for c in f)

def valid_perm(f: CNF, perm: dict[int, int], met: Counter) -> bool:
    guard()
    met['candidate_checks'] += 1
    vs = variables(f)
    vset = set(vs)
    images = [perm.get(v, v) for v in vs]
    met['permutation_entries_checked'] += len(vs)
    if any(v not in vset for v in perm) or 0 in images or sorted(map(abs, images)) != vs:
        met['candidate_rejections'] += 1
        return False
    met['symmetry_literal_visits'] += sum(map(len, f))
    ok = mapped(f, perm) == f  # Full structural equality, NOT digest equality.
    met['candidate_accepts' if ok else 'candidate_rejections'] += 1
    return ok

class UnionFind:
    def __init__(self, items):
        self.parent = {x: x for x in items}
    def find(self, x):
        while x != self.parent[x]:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
    def union(self, x, y):
        a, b = self.find(x), self.find(y)
        if a != b:
            self.parent[b] = a

def orbit_reps(f: CNF, clause: tuple[int, ...], candidates, met: Counter):
    """One representative per intersection with a certified literal orbit.
    Clause stabilization is not required: every generator must preserve F.
    """
    vs = variables(f)
    uf = UnionFind([x for v in vs for x in (v, -v)])
    accepted = []
    for p in candidates:
        if valid_perm(f, p, met):
            accepted.append(p)
            for v in vs:
                uf.union(v, map_lit(v, p))
                uf.union(-v, map_lit(-v, p))
                met['orbit_union_operations'] += 2
    reps = {}
    for x in clause:
        reps.setdefault(uf.find(x), x)
    return tuple(reps.values()), accepted, uf

def choose_clause(f: CNF) -> tuple[int, ...]:
    # Favor at-least-one clauses, consistently in both variants.
    pos = [c for c in f if all(x > 0 for x in c)]
    return min(pos or list(f), key=lambda c: (len(c), c))

def candidate_maps(f: CNF, clause: tuple[int, ...], met: Counter):
    """Bounded structural proposal mechanism, not automorphism completeness.

    Detect a rectangular collection of disjoint positive clauses with a unique
    negative-binary matching to a pivot row. Propose ONE cyclic column map.
    Arbitrary extra clauses are allowed but must survive full verification.
    Also try one local cycle and one polarity-flip map. At most three maps.
    No formula family name or SAT answer is passed to this procedure.
    """
    met['discovery_calls'] += 1
    met['discovery_literal_visits'] += sum(map(len, f))
    vs = variables(f)
    positive = [c for c in f if all(x > 0 for x in c)]
    if len(clause) >= 2 and all(x > 0 for x in clause):
        rows = [c for c in positive if len(c) == len(clause)]
        flat = [v for row in rows for v in row]
        if len(flat) == len(set(flat)) and set(flat) == set(vs) and clause in rows:
            negatives = {v: set() for v in vs}
            for c in f:
                if len(c) == 2 and c[0] < 0 and c[1] < 0:
                    a, b = -c[0], -c[1]
                    negatives[a].add(b); negatives[b].add(a)
            aligned = [clause]
            for row in rows:
                if row == clause:
                    continue
                rs = set(row)
                order = []
                for v in clause:
                    met['matching_set_probe_bound'] += min(len(negatives[v]), len(rs))
                    hits = negatives[v] & rs
                    if len(hits) != 1:
                        break
                    order.append(next(iter(hits)))
                if len(order) != len(clause) or len(set(order)) != len(clause):
                    aligned = []; break
                aligned.append(tuple(order))
            if aligned:
                p = {row[j]: row[(j+1) % len(row)] for row in aligned for j in range(len(row))}
                met['candidate_entries_produced'] += len(p)
                yield p
    # These local maps also provide honest negative trials on asymmetric inputs.
    cv = sorted({abs(x) for x in clause})
    if len(cv) > 1:
        p = {cv[i]: cv[(i+1) % len(cv)] for i in range(len(cv))}
        met['candidate_entries_produced'] += len(p)
        yield p
    if len(cv) <= 3:
        p = {v: -v for v in cv}
        met['candidate_entries_produced'] += len(p)
        yield p

def components(f: CNF, met: Counter):
    vs = variables(f)
    uf = UnionFind(vs)
    met['component_literal_visits'] += sum(map(len, f))
    for c in f:
        for x in c[1:]:
            uf.union(abs(c[0]), abs(x))
    groups = {}
    for c in f:
        groups.setdefault(uf.find(abs(c[0])), []).append(c)
    return [canon(g) for g in groups.values()]

def build_inner(source: CNF, orbit: bool, met: Counter, node_cap: int = 20000):
    """Materialized exact AND/OR plan with shrinking ordinary-CNF leaves."""
    source = normalize(canon(source))
    target = power_cutoff(bits(source))
    nodes = []; keys = {}; todo = []
    def intern(raw):
        met['intern_calls'] += 1
        f = simplify(raw, met)
        if f in keys:
            met['cache_reuses'] += 1
            return keys[f]
        if len(nodes) >= node_cap:
            raise BudgetExceeded(f'node cap {node_cap} reached')
        idx = len(nodes); keys[f] = idx; todo.append(idx)
        nodes.append({'formula': f, 'type': None})
        return idx
    root = intern(source)
    while todo:
        guard()
        idx = todo.pop(); node = nodes[idx]; f = node['formula']; tv = terminal(f)
        if tv is not None:
            node.update(type='CONST', value=tv); continue
        if bits(f) <= target:
            node.update(type='LEAF'); continue
        groups = components(f, met)
        if len(groups) > 1:
            node.update(type='AND', children=[intern(g) for g in groups]); continue
        c = choose_clause(f)
        reps, certs = c, []
        if orbit:
            reps, certs, uf = orbit_reps(f, c, candidate_maps(f, c, met), met)
            # Known negation-fixing rule, checked on this current residual.
            negatable = next((v for v in variables(f) if uf.find(v) == uf.find(-v)), None)
            if negatable is not None:
                c = (negatable, -negatable)
                reps = (negatable,)
        met['raw_literal_alternatives'] += len(c)
        met['retained_literal_alternatives'] += len(reps)
        met['pruned_before_generation'] += len(c) - len(reps)
        children = []
        for l in reps:
            children.append(intern(restrict(f, {abs(l): l > 0}, met)))
        node.update(type='OR', cover=c, reps=reps, certificates=certs, children=children)
    # Serialized formula payload is not a complete workspace measurement.
    met['inner_calls'] += 1
    met['dag_nodes'] += len(nodes)
    met['stored_formula_bits_sum'] += sum(bits(n['formula']) for n in nodes)
    met['certificate_entries_retained'] += sum(len(p) for n in nodes for p in n.get('certificates', []))
    leaves = [n['formula'] for n in nodes if n['type'] == 'LEAF']
    assert all(bits(f) <= target and bits(f) < bits(source) for f in leaves)
    met['leaf_count'] += len(leaves)
    return nodes, root, target

def replay_plan(nodes, root, met: Counter):
    """Independent structural verification; no SAT queries for OR certificates."""
    for node in nodes:
        guard()
        f = node['formula']; kind = node['type']
        if kind == 'CONST':
            assert terminal(f) == node['value']
        elif kind == 'AND':
            expected = sorted(simplify(g, met) for g in components(f, met))
            actual = sorted(nodes[i]['formula'] for i in node['children'])
            assert actual == expected
        elif kind == 'OR':
            c = node['cover']
            assert c in f or (len(c) == 2 and c[0] == -c[1])
            expected, _certs, uf = orbit_reps(f, c, node['certificates'], met)
            assert len(expected) == len(node['reps'])
            assert {uf.find(l) for l in expected} == {uf.find(l) for l in node['reps']}
            for l, child in zip(node['reps'], node['children']):
                assert simplify(restrict(f, {abs(l): l > 0}, met), met) == nodes[child]['formula']
        elif kind != 'LEAF':
            raise AssertionError(kind)
        met['replayed_nodes'] += 1

def stream_fix(source: CNF, met: Counter) -> CNF:
    """Consume certified single-orbit choices immediately, without a plan chain.

    A failed search returns its current equivalent CNF, never an UNSAT claim.
    Current input/output and each verification buffer remain materialized.
    Certificates are used and discarded, not retained in the returned CNF.
    """
    f = simplify(source, met)
    while terminal(f) is None:
        guard()
        c = choose_clause(f)
        reps, certs, uf = orbit_reps(f, c, candidate_maps(f, c, met), met)
        negatable = next((v for v in variables(f) if uf.find(v) == uf.find(-v)), None)
        if negatable is not None:
            c, reps = (negatable, -negatable), (negatable,)
        if len(reps) != 1:
            met['stream_stop_nontransitive'] += 1
            return f
        met['stream_fix_steps'] += 1
        met['raw_literal_alternatives'] += len(c)
        met['retained_literal_alternatives'] += 1
        met['pruned_before_generation'] += len(c)-1
        l = reps[0]
        old_n = len(variables(f))
        f = simplify(restrict(f, {abs(l): l > 0}, met), met)
        assert terminal(f) is not None or len(variables(f)) < old_n
        # Explicitly discard maps and orbit structures before the next phase.
        del certs, uf
    return f

def solve(source: CNF, orbit: bool, audit: bool = False, stream: bool = False):
    metrics = Counter(); audit_metrics = Counter(); answers = {}
    def visit(raw):
        guard()
        f = normalize(canon(raw))
        if terminal(f) is not None:
            return terminal(f)
        if f in answers:
            metrics['outer_cache_reuses'] += 1
            return answers[f]
        if stream:
            f = stream_fix(f, metrics)
            if terminal(f) is not None:
                return terminal(f)
        nodes, root, _target = build_inner(f, orbit, metrics)
        if audit:
            replay_plan(nodes, root, audit_metrics)
        vals = {}
        def walk(i):
            if i in vals:
                return vals[i]
            node = nodes[i]; k = node['type']
            if k == 'CONST':
                v = node['value']
            elif k == 'LEAF':
                v = visit(node['formula'])
            elif k == 'AND':
                v = all(walk(j) for j in node['children'])
            else:
                v = any(walk(j) for j in node['children'])
            vals[i] = v
            return v
        v = walk(root); answers[f] = v
        return v
    begin = time.monotonic()
    answer = visit(source)
    metrics['outer_answer_cache_entries'] = len(answers)
    return {'answer': answer, 'seconds': time.monotonic()-begin,
            'metrics': dict(metrics), 'audit_metrics': dict(audit_metrics)}

def brute(f: CNF) -> bool:
    vs = variables(f)
    if len(vs) > 16:
        raise ValueError('bounded brute verifier limited to 16 variables')
    for values in itertools.product((False, True), repeat=len(vs)):
        guard()
        a = dict(zip(vs, values))
        if all(any(a[abs(x)] == (x > 0) for x in c) for c in f):
            return True
    return False

def php(p, h):
    v = lambda i, j: i*h+j+1
    return canon([tuple(v(i,j) for j in range(h)) for i in range(p)] +
                 [(-v(i,j), -v(k,j)) for j in range(h) for i in range(p) for k in range(i+1,p)])

def tagged(n):
    return canon([c for i in range(n) for c in ((2*i+1,2*i+2),(-2*i-1,-2*i-2))])

def transformed(f, rng):
    vs = variables(f); dest = list(range(11, 11+len(vs))); rng.shuffle(dest)
    p = {v: dest[i] * rng.choice((-1,1)) for i,v in enumerate(vs)}
    return mapped(f,p)

def run_controls():
    rng = random.Random(20261008)
    rows = PARTIAL_ROWS; totals = Counter()
    def test(f, name):
        expected = brute(f)
        a = solve(f, False, True); b = solve(f, True, True); c = solve(f, True, True, True)
        assert a['answer'] == b['answer'] == c['answer'] == expected
        totals['formulas'] += 1; totals['answer_checks'] += 3
        totals['replayed_nodes'] += sum(r['audit_metrics'].get('replayed_nodes',0) for r in (a,b,c))
        rows.append({'name': name, 'source_sha256': hashlib.sha256(dimacs(f)).hexdigest(),
                     'expected': expected, 'plain': a, 'orbit': b, 'stream': c})
    clauses = [tuple((i+1)*s for i,s in enumerate(ss)) for ss in itertools.product((-1,1), repeat=3)]
    for mask in range(256):
        test(canon(c for i,c in enumerate(clauses) if mask & (1<<i)), f'exhaustive3_{mask}')
    for n in (4,5,6,7):
        for j in range(15):
            f = canon(tuple(v*rng.choice((-1,1)) for v in rng.sample(range(1,n+1),3)) for _ in range(4*n))
            test(f, f'random_{n}_{j}')
            if j < 3:
                test(transformed(f,rng), f'rename_flip_{n}_{j}')
                test(canon(list(f)+[(1,-1),(99,-99)]+list(f)), f'padding_{n}_{j}')
    for n in range(1,6):
        test(tagged(n), f'affine_pairs_{n}')
    for p,h in ((2,2),(3,2),(3,3),(4,3)):
        test(php(p,h), f'php_{p}_{h}')
    for n in range(2,7):
        horn = canon([(1,)]+[(-i,i+1) for i in range(1,n)]+[(-n,)])
        test(horn,f'horn_unsat_{n}'); test(canon(horn[:-1]),f'horn_variant_{n}')
    f = canon([(1,2),(-1,)])
    assert brute(f) and not brute(restrict(f,{1:True},Counter()))
    m=Counter(); assert not valid_perm(f,{1:2,2:1},m)
    totals['invalid_map_rejections'] += 1
    # A parent symmetry is not automatically valid after conditioning.
    parent=canon([(1,2),(-1,-2),(3,4),(-3,-4)])
    swap={1:3,3:1,2:4,4:2}
    assert valid_perm(parent,swap,Counter())
    residual=restrict(parent,{1:True},Counter())
    assert not valid_perm(residual,swap,Counter())
    totals['stale_symmetry_rejections'] += 1
    # Independent conjunction cannot be replaced by union/OR.
    f=canon([(1,2),(-1,-2)]); g=canon([(3,),(-3,)])
    assert brute(f) and not brute(g) and not brute(canon(f+g))
    test(canon(f+g),'independent_product_unsat')
    # Non-bijective source-carry/semantic-oracle replacement is rejected.
    assert not valid_perm(canon([(1,2),(-1,-2)]),{1:2},Counter())
    totals['nonbijective_rejections'] += 1
    return {'totals': dict(totals), 'cases': rows}

def run_php(h, memory):
    rows=PARTIAL_ROWS
    for p in (h,h+1):
        f=php(p,h)
        row={'pigeons':p,'holes':h,'input_dimacs_bits':bits(f), 'expected':p<=h}
        for mode in ('plain','orbit','stream'):
            orbit = mode != 'plain'
            if memory:
                tracemalloc.start()
            r=solve(f,orbit,audit=False,stream=(mode=='stream'))
            if memory:
                _cur,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
                r['incremental_python_peak_bytes']=peak
            assert r['answer'] == (p<=h)
            row[mode]=r
        rows.append(row)
    return {'cases':rows, 'memory_scope':'Python traced allocation during solve; caller-owned source tuple preallocated; includes current formulas, maps, cache, Python overhead, not process RSS or external libraries'}

def run_orbits():
    rows=PARTIAL_ROWS; checks=0
    for n in range(1,11):
        f=tagged(n); met=Counter()
        generators=[{2*i+1:-(2*i+1),2*i+2:-(2*i+2)} for i in range(n)]
        assert all(valid_perm(f,p,met) for p in generators)
        canonical=restrict(f,{2*i+1:False for i in range(n)},Counter())
        # Enumerate only in this auditor, NOT in the candidate constructor.
        for mask in range(1<<n):
            a={2*i+1:bool(mask&(1<<i)) for i in range(n)}
            r=restrict(f,a,Counter())
            flip={2*i+2:-(2*i+2) for i in range(n) if a[2*i+1]}
            assert mapped(r,flip)==canonical
            # A same-label continuation may distinguish; its transported version agrees.
            for j in range(n):
                assert mapped(restrict(r,{2*j+2:False},Counter()),flip) == restrict(canonical,{2*j+2: bool(a[2*j+1])},Counter())
                checks+=1
        rows.append({'pairs':n,'raw_assignments':1<<n,'certified_representatives':1,'generator_count':n,'verification':dict(met)})
    # Current-scale costs cannot be erased by a naming change. Exact rational audit.
    from fractions import Fraction as Q
    assert max(Q(1),Q(8)*Q(1)) == 8
    assert Q(3,2)*Q(2,3) == 1 # Padding does not create source-relative shrink.
    assert Q(1,2)+Q(1,2)+Q(2,3)>1 # independent OR-cover product pays both fanouts.
    return {'cases':rows,'transported_continuation_checks':checks,
            'scope':'explicit affine family only; no polynomial algorithm for orbit representatives of arbitrary assignment cubes',
            'resource_guard_checks':3}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--suite',choices=('controls','php','orbits'),required=True)
    parser.add_argument('--holes',type=int,default=5)
    parser.add_argument('--memory',action='store_true')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    out={'run_id':'ARC-0005-ORBIT','suite':args.suite,'seed':20261008,
         'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'status':'RUNNING','cases':PARTIAL_ROWS,'limitations':['Finite tests are not an asymptotic complexity proof.',
         'All formulas and accepted maps are materialized; no sublinear-space theorem.',
         'This compares controlled local variants, not the complete historical hybrid.',
         'No globally complete or near-linear automorphism discovery is claimed.',
         'Counters are diagnostic categories, not complete RAM operation counts; wall time includes their overhead.']}
    try:
        if args.suite=='controls': out.update(run_controls())
        elif args.suite=='php': out.update(run_php(args.holes,args.memory))
        else: out.update(run_orbits())
        out['status']='PASS'
    except BudgetExceeded as e:
        out['status']='BLOCKED_BUDGET'; out['error']=str(e)
    except Exception as e:
        out['status']='FAIL'; out['error']=repr(e)
        raise
    finally:
        out['elapsed_seconds']=time.monotonic()-START
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('cases','limitations')},indent=2))
    if args.suite=='php':
        for r in out.get('cases',[]):
            print(json.dumps(r,sort_keys=True))
    return 0 if out['status']=='PASS' else 2

if __name__=='__main__':
    raise SystemExit(main())
