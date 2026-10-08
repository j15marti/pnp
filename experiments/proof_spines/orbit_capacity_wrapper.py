#!/usr/bin/env python3
"""ARC-0005: exact matrix/orbit guards for the existing double WRAPPER.

Known transfer: Anders--Codel--Heule (2026), orbitopal fixing, Thm. 3.1.
Project additions: orbit-saturation checking and a charged capacity VALUE gate.
No general-SAT complexity improvement is claimed. All failures are abstentions.
Each invocation has a 25-second cooperative/hard alarm; run suites separately.
"""
from __future__ import annotations
import argparse
import gc
import hashlib
import importlib.util
import itertools as it
import json
import math
import random
import signal
import time
import tracemalloc
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

CNF = tuple[tuple[int, ...], ...]
START = time.monotonic()
DEADLINE = START + 25
SEED = 20261008

class BudgetExceeded(RuntimeError):
    pass

class ResourceAbstention(RuntimeError):
    pass

def tick() -> None:
    if time.monotonic() >= DEADLINE:
        raise BudgetExceeded('25-second cooperative budget')

def alarm_handler(signum: int, frame: Any) -> None:
    raise BudgetExceeded('25-second alarm')

@dataclass
class Meter:
    source_literal_reads: int = 0
    source_clause_visits: int = 0
    signature_comparisons: int = 0
    discovery_cells: int = 0
    orbit_groups: int = 0
    retained_profile_tokens: int = 0
    propagation_rounds: int = 0
    assignments: int = 0
    solver_calls: int = 0
    copied_parent_cnfs: int = 0
    child_bits: int = 0
    max_variable: int = 0
    rows: int = 0
    columns: int = 0
    symmetry_verified: bool = False
    capacity_verified: bool = False
    space_cell_cap: int = 0
    output_bit_cap: int = 0
    propagation_round_cap: int = 8


def canon(f: Any) -> CNF:
    return tuple(sorted(set(tuple(sorted(set(c))) for c in f)))

def encoded_size(f: CNF) -> int:
    n = max((abs(x) for c in f for x in c), default=0)
    w = max(1, n.bit_length())
    return w + sum(w + (w + 1)*len(c) for c in f)

def truth(f: CNF, assignment: dict[int, bool]) -> bool:
    return all(any(assignment.get(abs(x), False) == (x > 0) for x in c) for c in f)

def brute(f: CNF) -> bool:
    variables = sorted({abs(x) for c in f for x in c})
    if len(variables) > 16:
        raise ValueError('reference restricted to at most 16 variables')
    return any(truth(f, dict(zip(variables, a))) for a in it.product((False, True), repeat=len(variables)))

def guard(f: CNF, meter: Meter) -> tuple[int, int] | None:
    """Canonical, distinct clauses/literals; no tautologies or huge sparse IDs.
    Invalid representation makes this partial member abstain, not answer UNSAT.
    """
    previous = None
    literals = 0
    largest = 0
    if not isinstance(f, tuple):
        return None
    for c in f:
        tick()
        meter.source_clause_visits += 1
        if not isinstance(c, tuple) or (previous is not None and previous >= c):
            return None
        last = None
        first_positive = len(c)
        for index, x in enumerate(c):
            meter.source_literal_reads += 1
            literals += 1
            if type(x) is not int or x == 0 or (last is not None and last >= x):
                return None
            if x > 0 and first_positive == len(c):
                first_positive = index
            largest = max(largest, abs(x))
            last = x
        # Complement detection uses two indices, not an unbounded temporary set.
        left, right = first_positive-1, first_positive
        while left >= 0 and right < len(c):
            meter.source_literal_reads += 2
            a, b = -c[left], c[right]
            if a == b:
                return None
            if a < b:
                left -= 1
            else:
                right += 1
        previous = c
    if largest > max(1, literals):
        return None
    meter.max_variable = largest
    return largest, literals


def discover(f: CNF, n: int, meter: Meter) -> tuple[tuple[int, ...], ...] | None:
    """One deterministic candidate, discovered from ULCs and complement conflicts.
    No graph-isomorphism oracle, external matrix, or permutation enumeration.
    """
    counts = [0] * (2*n + 1)
    for c in f:
        meter.source_clause_visits += 1
        for x in c:
            meter.source_literal_reads += 1
            counts[x+n] += 1
    candidates: list[list[tuple[int, ...]]] = [[] for _ in range(n+1)]
    for c in f:
        meter.source_clause_visits += 1
        good = len(c) >= 2
        for x in c:
            meter.source_literal_reads += 1
            good = good and counts[x+n] == 1
        if good:
            candidates[len(c)].append(c)
    eligible = [(r*len(cols), r, cols) for r, cols in enumerate(candidates) if len(cols) >= 2]
    if not eligible:
        return None
    _, r, pool = max(eligible, key=lambda x: (x[0], x[1]))
    # Complementary ULCs can overlap (already on PHP(2,2)). Select one
    # variable-disjoint candidate family; discovery is deliberately partial.
    used = [False]*(n+1)
    cols = []
    for c in pool:
        meter.source_literal_reads += len(c)
        if any(used[abs(x)] for x in c):
            continue
        cols.append(c)
        for x in c:
            used[abs(x)] = True
    if len(cols) < 2:
        return None
    q = len(cols)
    column = [-1]*(n+1)
    orientation = [0]*(n+1)
    cells = []
    for j, col in enumerate(cols):
        for x in col:
            if column[abs(x)] != -1:
                return None
            column[abs(x)] = j
            orientation[abs(x)] = 1 if x > 0 else -1
            cells.append(abs(x))
    parent = list(range(n+1))
    rank = [0]*(n+1)
    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a: int, b: int) -> None:
        a, b = find(a), find(b)
        if a == b:
            return
        if rank[a] < rank[b]:
            a, b = b, a
        parent[b] = a
        if rank[a] == rank[b]:
            rank[a] += 1
    for c in f:
        tick()
        meter.source_clause_visits += 1
        meter.source_literal_reads += len(c)
        if len(c) != 2:
            continue
        x, y = c
        if column[abs(x)] < 0 or column[abs(y)] < 0:
            continue
        if (1 if x > 0 else -1) == -orientation[abs(x)] and (1 if y > 0 else -1) == -orientation[abs(y)]:
            union(abs(x), abs(y))
    buckets: list[list[int]] = [[] for _ in range(n+1)]
    for v in cells:
        buckets[find(v)].append(v)
    groups = [g for g in buckets if g]
    if len(groups) != r:
        return None
    rows = []
    for values in sorted(groups, key=min):
        if len(values) != q:
            return None
        row = [0]*q
        for v in values:
            if row[column[v]]:
                return None
            row[column[v]] = v*orientation[v]
        if not all(row):
            return None
        rows.append(tuple(row))
    meter.discovery_cells = r*q
    meter.rows, meter.columns = r, q
    return tuple(rows)


def position(matrix: tuple[tuple[int, ...], ...], n: int) -> list[tuple[int, int, int] | None]:
    out: list[tuple[int, int, int] | None] = [None]*(n+1)
    if not matrix or not matrix[0]:
        raise ValueError('empty matrix')
    q = len(matrix[0])
    for i, row in enumerate(matrix):
        if len(row) != q:
            raise ValueError('ragged matrix')
        for j, x in enumerate(row):
            if type(x) is not int or not x or abs(x) > n or out[abs(x)] is not None:
                raise ValueError('invalid/repeated matrix variable')
            out[abs(x)] = (i, j, 1 if x > 0 else -1)
    return out


class Node:
    __slots__ = ('key', 'value', 'left', 'right', 'height')
    def __init__(self, key: Any):
        self.key, self.value = key, 1
        self.left = self.right = None
        self.height = 1

class AVLCounts:
    """Exact deterministic balanced comparison tree; no hash-only identity."""
    def __init__(self, meter: Meter):
        self.root = None
        self.meter = meter
        self.size = 0
    @staticmethod
    def h(n: Any) -> int:
        return n.height if n else 0
    def update(self, n: Any) -> None:
        n.height = 1 + max(self.h(n.left), self.h(n.right))
    def right(self, y: Any) -> Any:
        x = y.left
        y.left = x.right
        x.right = y
        self.update(y); self.update(x)
        return x
    def left(self, x: Any) -> Any:
        y = x.right
        x.right = y.left
        y.left = x
        self.update(x); self.update(y)
        return y
    def add(self, key: Any) -> None:
        def put(n: Any) -> Any:
            if n is None:
                outside, profiles = key
                tokens = len(outside) + sum(len(p)+2 for p, multiplicity in profiles) + 3
                if self.meter.space_cell_cap and self.meter.retained_profile_tokens + tokens > self.meter.space_cell_cap:
                    raise ResourceAbstention('orbit-profile-space-cap')
                self.size += 1
                self.meter.retained_profile_tokens += tokens
                return Node(key)
            self.meter.signature_comparisons += 1
            if key == n.key:
                n.value += 1
                return n
            if key < n.key:
                n.left = put(n.left)
            else:
                n.right = put(n.right)
            self.update(n)
            balance = self.h(n.left)-self.h(n.right)
            if balance > 1:
                if key > n.left.key:
                    n.left = self.left(n.left)
                return self.right(n)
            if balance < -1:
                if key < n.right.key:
                    n.right = self.right(n.right)
                return self.left(n)
            return n
        self.root = put(self.root)
    def items(self):
        stack = []
        node = self.root
        while node or stack:
            while node:
                stack.append(node); node = node.left
            node = stack.pop()
            yield node.key, node.value
            node = node.right


def signature(c: tuple[int, ...], pos: list[Any]) -> tuple[Any, Any]:
    outside = []
    active = []
    for x in c:
        data = pos[abs(x)]
        if data is None:
            outside.append(x)
        else:
            i, j, sign = data
            active.append((i, (j+1)*(1 if x > 0 else -1)*sign))
    active.sort()
    profiles = []
    for _, group in it.groupby(active, key=lambda a: a[0]):
        profiles.append(tuple(sorted(x[1] for x in group)))
    profiles.sort()
    compressed = tuple((p, sum(1 for _ in g)) for p, g in it.groupby(profiles))
    return tuple(outside), compressed


def choose_capped(n: int, k: int, cap: int) -> int:
    k = min(k, n-k)
    value = 1
    for i in range(1, k+1):
        value = value*(n-k+i)//i
        if value > cap:
            return cap+1
    return value


def orbit_size(sig: Any, rows: int, cap: int) -> int:
    available, size = rows, 1
    for _, count in sig[1]:
        if count > available:
            return cap+1
        factor = choose_capped(available, count, cap//size)
        size *= factor
        if size > cap:
            return cap+1
        available -= count
    return size


def saturated(f: CNF, matrix: tuple[tuple[int, ...], ...], n: int, meter: Meter) -> bool:
    pos = position(matrix, n)
    counts = AVLCounts(meter)
    for c in f:
        tick()
        meter.source_clause_visits += 1
        meter.source_literal_reads += len(c)
        counts.add(signature(c, pos))
    meter.orbit_groups = counts.size
    for sig, count in counts.items():
        if count != orbit_size(sig, len(matrix), len(f)):
            return False
    meter.symmetry_verified = True
    return True


def capacity(f: CNF, matrix: tuple[tuple[int, ...], ...], n: int, meter: Meter) -> bool:
    """Verify every within-row pair of different columns conflicts.
    Canonical uniqueness makes r exact occurrences equivalent to all r rows.
    Discovery already verified each column is a genuine ULC.
    """
    r, q = len(matrix), len(matrix[0])
    pos = position(matrix, n)
    pair_count = q*(q-1)//2
    if r*pair_count > len(f) or (meter.space_cell_cap and pair_count > meter.space_cell_cap):
        return False
    counts = [0]*pair_count
    for c in f:
        tick()
        meter.source_clause_visits += 1
        meter.source_literal_reads += len(c)
        if len(c) != 2:
            continue
        x, y = c
        a, b = pos[abs(x)], pos[abs(y)]
        if a is None or b is None or a[0] != b[0] or a[1] == b[1]:
            continue
        if (1 if x > 0 else -1) != -a[2] or (1 if y > 0 else -1) != -b[2]:
            continue
        j, k = sorted((a[1], b[1]))
        idx = j*(2*q-j-1)//2 + k-j-1
        counts[idx] += 1
    good = all(x == r for x in counts)
    meter.capacity_verified = good
    return good


def ulc_matrix(f: CNF, matrix: tuple[tuple[int, ...], ...]) -> bool:
    """Independent small-test checker, not the production discovery route."""
    from collections import Counter
    cnt = Counter(x for c in f for x in c)
    return all(tuple(sorted(col)) in f and all(cnt[x] == 1 for x in col) for col in zip(*matrix))


def fixing(matrix: tuple[tuple[int, ...], ...]) -> dict[int, bool]:
    r, q = len(matrix), len(matrix[0])
    assignments = {abs(matrix[-1][0]): matrix[-1][0] > 0}
    for j in range(min(r, q)):
        for i in range(r-j-1):
            x = matrix[i][j]
            assignments[abs(x)] = x < 0
    return assignments


def propagate(f: CNF, assignment: dict[int, bool], meter: Meter) -> tuple[CNF, dict[int, bool]]:
    """Source-scanning unit propagation, followed by one explicit residual.
    Unlike certificate verification, this stage can cost O(n*M). It is charged.
    """
    while True:
        tick()
        if meter.propagation_rounds >= meter.propagation_round_cap:
            raise ResourceAbstention('propagation-round-cap')
        meter.propagation_rounds += 1
        changed = False
        all_satisfied = True
        for c in f:
            meter.source_clause_visits += 1
            satisfied, unit, remaining = False, 0, 0
            for x in c:
                meter.source_literal_reads += 1
                v = abs(x)
                if v not in assignment:
                    unit, remaining = x, remaining+1
                elif assignment[v] == (x > 0):
                    satisfied = True
                    break
            if satisfied:
                continue
            all_satisfied = False
            if remaining == 0:
                meter.assignments = len(assignment)
                return ((),), assignment
            if remaining == 1:
                assignment[abs(unit)] = unit > 0
                changed = True
        if all_satisfied:
            meter.assignments = len(assignment)
            return (), assignment
        if not changed:
            break
    if meter.output_bit_cap:
        w = max(1, meter.max_variable.bit_length())
        upper_bits = w
        for c in f:
            meter.source_clause_visits += 1
            remaining, satisfied = 0, False
            for x in c:
                meter.source_literal_reads += 1
                if abs(x) not in assignment:
                    remaining += 1
                elif assignment[abs(x)] == (x > 0):
                    satisfied = True
                    break
            if not satisfied:
                upper_bits += w + (w+1)*remaining
                if upper_bits > meter.output_bit_cap:
                    raise ResourceAbstention('ordinary-child-output-cap')
    residual = []
    for c in f:
        meter.source_clause_visits += 1
        meter.source_literal_reads += len(c)
        if any(abs(x) in assignment and assignment[abs(x)] == (x > 0) for x in c):
            continue
        residual.append(tuple(x for x in c if abs(x) not in assignment))
    child = canon(residual)
    meter.child_bits = encoded_size(child)
    meter.assignments = len(assignment)
    return child, assignment


def floor_cuberoot(x: int) -> int:
    lo, hi = 0, 1 << ((x.bit_length()+2)//3)
    while lo+1 < hi:
        mid = (lo+hi)//2
        if mid**3 <= x:
            lo = mid
        else:
            hi = mid
    return lo


def _preprocess(f: CNF, use_capacity: bool, meter: Meter) -> dict[str, Any]:
    checked = guard(f, meter)
    def result(kind: str, **kwargs: Any) -> dict[str, Any]:
        return {'kind': kind, 'metrics': asdict(meter), **kwargs}
    if checked is None:
        return result('FAIL', reason='noncanonical-or-unsupported-labels')
    n, _ = checked
    if () in f:
        return result('VALUE', value=False, reason='empty-clause', recursive_children=0)
    if not f:
        return result('VALUE', value=True, reason='empty-formula', recursive_children=0)
    w = max(1, n.bit_length())
    M = w + len(f)*w + (w+1)*checked[1]
    cap = floor_cuberoot(M*M)
    meter.space_cell_cap = meter.output_bit_cap = cap
    if n > cap:
        raise ResourceAbstention('variable-array-space-cap')
    matrix = discover(f, n, meter)
    if matrix is None:
        return result('FAIL', reason='no-certified-matrix-candidate')
    r, q = len(matrix), len(matrix[0])
    if use_capacity and capacity(f, matrix, n, meter):
        if q > r:
            return result('VALUE', value=False, reason='matrix-capacity', recursive_children=0)
        witness = {v: False for v in range(1, n+1)}
        for i, row in enumerate(matrix):
            for j, x in enumerate(row):
                witness[abs(x)] = (i == j) == (x > 0)
        valid = True
        for c in f:
            meter.source_clause_visits += 1
            meter.source_literal_reads += len(c)
            valid = valid and any(witness[abs(x)] == (x > 0) for x in c)
        if valid:
            meter.assignments = len(witness)
            return result('VALUE', value=True, reason='checked-matrix-witness', recursive_children=0, witness=witness)
    if not saturated(f, matrix, n, meter):
        return result('FAIL', reason='incomplete-clause-orbit')
    child, assignment = propagate(f, fixing(matrix), meter)
    if child in ((), ((),)):
        return result('VALUE', value=not child, reason='orbitopal-unit-propagation', recursive_children=0, witness=assignment if not child else None)
    return result('REDUCE', child=child, assignment=assignment, reason='orbitopal-residual', recursive_children=1)


def preprocess(f: CNF, use_capacity: bool = True) -> dict[str, Any]:
    """Bounded partial member: O(M^(2/3)) retained cells, capped ordinary child,
    and at most eight source-scanning propagation rounds. All cap exits FAIL.
    Cell bounds are not a unit-coefficient bit-memory promise.
    """
    meter = Meter()
    try:
        return _preprocess(f, use_capacity, meter)
    except ResourceAbstention as exc:
        return {'kind': 'FAIL', 'reason': str(exc), 'metrics': asdict(meter)}


def php(p: int, h: int) -> CNF:
    v = lambda i,j: i*h+j+1
    return canon([tuple(v(i,j) for j in range(h)) for i in range(p)] + [(-v(i,j),-v(k,j)) for j in range(h) for i in range(p) for k in range(i+1,p)])


def transform(f: CNF, perm: list[int], signs: list[int]) -> CNF:
    return canon(tuple(perm[abs(x)]*signs[abs(x)]*(1 if x > 0 else -1) for x in c) for c in f)


def exact_row_symmetry(f: CNF, matrix: tuple[tuple[int, ...], ...]) -> bool:
    n = max(max((abs(x) for c in f for x in c), default=0), max(abs(x) for row in matrix for x in row))
    for perm in it.permutations(range(len(matrix))):
        images = list(range(n+1)); signs = [1]*(n+1)
        for i, row in enumerate(matrix):
            for j, x in enumerate(row):
                y = matrix[perm[i]][j]
                images[abs(x)] = abs(y)
                signs[abs(x)] = (1 if x > 0 else -1)*(1 if y > 0 else -1)
        if transform(f, images, signs) != f:
            return False
    return True


def load_baseline():
    path = Path(__file__).resolve().parents[1]/'DOUBLE_WRAPPER_2026-10-07'/'double_wrapper.py'
    data = path.read_bytes()
    blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if blob != '04cf06305b5beff2a36f631e4a38b5e09553c1ee':
        raise RuntimeError('baseline source SHA mismatch')
    spec = importlib.util.spec_from_file_location('prior_double_wrapper', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def measured(call):
    gc.collect()
    tracemalloc.start()
    start = time.perf_counter()
    answer = call()
    seconds = time.perf_counter()-start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return answer, {'seconds': seconds, 'incremental_python_peak_bytes': peak}


def enhanced_outer(f: CNF, strategy: str = 'separator_fast', use_capacity: bool = True, baseline: Any = None) -> tuple[bool, dict[str, int]]:
    """Apply the certified partial member at every outer recursive call.
    FAIL falls back to the unchanged exact inner WRAPPER, never to a guessed
    SAT answer. Its full formula cache/plan space remains charged and OPEN.
    """
    from functools import lru_cache
    baseline = load_baseline() if baseline is None else baseline
    totals = {'member_calls': 0, 'VALUE': 0, 'REDUCE': 0, 'FAIL': 0,
              'inner_calls': 0, 'dag_nodes': 0, 'source_literal_reads': 0}
    @lru_cache(None)
    def solve(source: CNF) -> bool:
        tick()
        proposal = preprocess(source, use_capacity)
        totals['member_calls'] += 1
        totals[proposal['kind']] += 1
        totals['source_literal_reads'] += proposal['metrics']['source_literal_reads']
        if proposal['kind'] == 'VALUE':
            return proposal['value']
        if proposal['kind'] == 'REDUCE':
            child = proposal['child']
            assert encoded_size(child) < encoded_size(source)
            return solve(child)
        plan = baseline.inner(source, strategy)
        totals['inner_calls'] += 1
        totals['dag_nodes'] += plan['metrics']['dag_nodes']
        def child_solver(child: CNF) -> bool:
            assert encoded_size(child) < plan['metrics']['N_bits']
            return solve(child)
        return baseline.evaluate(plan, child_solver)
    answer = solve(f)
    totals['cached_answers'] = solve.cache_info().currsize
    return answer, totals


def suite_small(rows: list[dict[str, Any]]) -> None:
    rng = random.Random(SEED)
    cases = []
    cs = [tuple((i+1)*s for i,s in enumerate(signs)) for signs in it.product((-1,1), repeat=3)]
    for mask in range(256):
        cases.append(('exhaustive-3var', canon(c for j,c in enumerate(cs) if mask >> j & 1)))
    for n in range(2,8):
        for _ in range(40):
            f = canon(tuple(v*rng.choice((-1,1)) for v in rng.sample(range(1,n+1),rng.randint(1,min(3,n)))) for _ in range(rng.randint(1,4*n)))
            cases.append(('random', f))
    for p,h in ((2,2),(3,2),(2,3)):
        f = php(p,h)
        cases.append(('php', f))
        for i in range(len(f)):
            cases.append(('one-clause-deleted', f[:i]+f[i+1:]))
    # Connected graph-colouring controls yield genuine nonterminal reductions.
    for mask in range(64):
        edges = [(a,b) for j,(a,b) in enumerate(it.combinations(range(4),2)) if mask>>j&1]
        q,r=4,3
        v=lambda j,i:j*r+i+1
        f=canon([tuple(v(j,i) for i in range(r)) for j in range(q)]+
                [(-v(a,i),-v(b,i)) for a,b in edges for i in range(r)])
        cases.append(('graph-colouring',f))
    for name,f in [('Horn',((-1,2),(-2,3),(1,))),
                   ('dual-Horn',((1,-2),(2,-3),(-1,))),
                   ('2-SAT',((1,2),(-1,2),(1,-2),(-1,-2))),
                   ('XOR-SAT',((1,2),(-1,-2))),
                   ('XOR-UNSAT',((1,2),(-1,-2),(1,), (2,)))]:
        cases.append((name,canon(f)))
    baseline = load_baseline()
    counts = {'formulas': 0, 'semantic_checks': 0, 'VALUE': 0, 'REDUCE': 0, 'FAIL': 0, 'baseline_comparisons': 0, 'recursive_adapter_checks': 0}
    for family,f in cases:
        tick()
        expected = brute(f)
        for capacity_enabled in (False,True):
            out = preprocess(f, capacity_enabled)
            counts[out['kind']] += 1
            if out['kind'] == 'VALUE':
                assert out['value'] == expected
                if expected and out.get('witness'):
                    assert truth(f,out['witness'])
            elif out['kind'] == 'REDUCE':
                assert encoded_size(out['child'])**3 <= encoded_size(f)**2
                assert brute(out['child']) == expected
                for values in it.product((False,True),repeat=max((abs(x) for c in out['child'] for x in c),default=0)):
                    a = {i+1: v for i,v in enumerate(values)}
                    if truth(out['child'],a):
                        a.update(out['assignment'])
                        assert truth(f,a)
            counts['semantic_checks'] += 1
        if counts['formulas'] < 256 or family == 'php':
            result = preprocess(f)
            if result['kind'] == 'VALUE':
                enhanced = result['value']
            else:
                g = result.get('child',f)
                enhanced = baseline.outer(g,'components')[0]
            assert enhanced == expected
            counts['baseline_comparisons'] += 1
        assert enhanced_outer(f, 'components', baseline=baseline)[0] == expected
        counts['recursive_adapter_checks'] += 1
        counts['formulas'] += 1
    rows.append(counts)


def suite_orbits(rows: list[dict[str, Any]]) -> None:
    rng = random.Random(SEED+1)
    checked = 0; accepted = 0; orbit_sizes = 0
    for r,q in ((2,2),(3,2),(2,3)):
        matrix = tuple(tuple(i*q+j+1 for j in range(q)) for i in range(r))
        n = r*q
        for _ in range(100):
            f = canon(tuple(v*rng.choice((-1,1)) for v in rng.sample(range(1,n+1),rng.randint(1,min(4,n)))) for _ in range(rng.randint(1,14)))
            meter = Meter()
            assert saturated(f,matrix,n,meter) == exact_row_symmetry(f,matrix)
            checked += 1
            c = f[0]
            pos = position(matrix,n)
            sig = signature(c,pos)
            orbit = set()
            for p in it.permutations(range(r)):
                images = list(range(n+1))
                for i in range(r):
                    for j in range(q): images[matrix[i][j]] = matrix[p[i]][j]
                orbit.update(transform((c,), images, [1]*(n+1)))
            assert orbit_size(sig,r,10**9) == len(orbit)
            orbit_sizes += 1
            closed = canon(it.chain.from_iterable(transform(f,[0]+[p[(v-1)//q]*q+(v-1)%q+1 for v in range(1,n+1)],[1]*(n+1)) for p in it.permutations(range(r))))
            assert saturated(closed,matrix,n,Meter())
            accepted += 1
        tick()
    rows.append({'orbit_invariance_comparisons':checked,'orbit_size_checks':orbit_sizes,'saturated_closures_accepted':accepted})


def suite_capacity(rows: list[dict[str, Any]], maximum: int) -> None:
    for h in range(2, maximum+1):
        for p in (h-1,h,h+1):
            if p < 2: continue
            f = php(p,h)
            out, perf = measured(lambda: preprocess(f))
            assert out['kind']=='VALUE' and out['value']==(p<=h)
            assert out['metrics']['solver_calls']==0 and out['metrics']['copied_parent_cnfs']==0
            if out['value']: assert truth(f,out['witness'])
            rows.append({'pigeons':p,'holes':h,'input_bits':encoded_size(f),'input_clauses':len(f),'input_literals':sum(map(len,f)),'answer':out['value'],'reason':out['reason'],'metrics':out['metrics'],'performance':perf})
            tick()


def suite_hostile(rows: list[dict[str, Any]]) -> None:
    rng=random.Random(SEED+2)
    checks=0; missing_rejected=0
    for p,h in ((2,2),(3,2),(2,3)):
        f=php(p,h); n=p*h
        for _ in range(25):
            perm=[0]+rng.sample(range(1,n+1),n)
            signs=[1]+[rng.choice((-1,1)) for _ in range(n)]
            g=transform(f,perm,signs)
            out=preprocess(g)
            assert out['kind']=='VALUE' and out['value']==(p<=h)
            checks+=1
        for j in range(len(f)):
            g=f[:j]+f[j+1:]
            out=preprocess(g)
            if out['kind']=='VALUE': assert out['value']==brute(g)
            else: missing_rejected+=1
            checks+=1
    # Duplicate inflation must not imitate a complete orbit.
    matrix=((1,3),(2,4)); bad=((-3,-1),(-3,-1),(1,2),(3,4))
    out=preprocess(bad)
    assert out['kind']=='FAIL'
    checks+=1
    # ULC cannot be dropped merely because the action is a true symmetry.
    nonulc=canon([(1,2),(1,),(2,)])
    assert saturated(nonulc,((1,),(2,)),2,Meter())
    assert brute(nonulc) and not brute(canon(nonulc+((-1,),)))
    assert preprocess(nonulc)['kind']=='FAIL'
    checks+=1
    # A single asymmetry can invalidate arbitrary representative fixing.
    g=canon([(1,2),(1,-2)])
    assert brute(g) and not brute(canon(g+((-1,),)))
    assert preprocess(g)['kind']=='FAIL'
    checks+=1
    # No current SAT bit or digest is accepted as a symmetry certificate.
    assert preprocess(((10**12,),))['kind']=='FAIL'
    checks+=1
    # Independent conjunctions: a satisfiable component does not erase UNSAT.
    a=php(2,2); b=tuple(tuple((abs(x)+4)*(1 if x>0 else -1) for x in c) for c in php(3,2))
    product=canon(a+b)
    out=preprocess(product)
    if out['kind']=='VALUE': assert out['value']==brute(product)
    checks+=1
    # Tautological padding is rejected by the member rather than counted as compression.
    padded=canon(php(3,2)+((1,-1),))
    assert preprocess(padded)['kind']=='FAIL'
    checks+=1
    # Arbitrary external core: exact symmetry remains but the core is not solved for free.
    core=canon([(7,8,9),(-7,-8,9),(7,-8,-9),(-7,8,-9)])
    combo=canon(php(2,3)+core)
    o=preprocess(combo,False)
    assert o['kind'] in ('REDUCE','FAIL','VALUE')
    if o['kind']=='VALUE': assert o['value']==brute(combo)
    if o['kind']=='REDUCE': assert brute(o['child'])==brute(combo)
    checks+=1
    # All-or-nothing asymmetry control for orbit saturation.
    f=php(3,3); n=9
    m=discover(f,n,Meter()); assert m
    assert saturated(f,m,n,Meter())
    for clause in [(-1,),(-1,-2),(1,)]:
        g=canon(f+(clause,))
        assert not saturated(g,m,n,Meter())
        checks+=1
    # Caps are safe FAIL exits, never UNSAT verdicts.
    low_density=tuple((i,) for i in range(1,513))
    capout=preprocess(low_density)
    assert capout['kind']=='FAIL' and capout['reason']=='variable-array-space-cap'
    checks+=1
    capmeter=Meter(space_cell_cap=1)
    try:
        saturated(php(3,2),((1,3,5),(2,4,6)),6,capmeter)
        raise AssertionError('profile cap did not trigger')
    except ResourceAbstention:
        pass
    checks+=1
    chain=canon([(-i,i+1) for i in range(1,20)])
    try:
        propagate(chain,{1:True},Meter(max_variable=20,propagation_round_cap=1))
        raise AssertionError('round cap did not trigger')
    except ResourceAbstention:
        pass
    checks+=1
    # A nonterminal bounded ordinary successor exists on an easy-factor product.
    # The arbitrary core is preserved, not decided from the factor's SAT bit.
    core0=canon([(1,2,3),(-1,-2,3),(1,-2,-3),(-1,2,-3)])
    core6=tuple(tuple((abs(x)+36)*(1 if x>0 else -1) for x in c) for c in core0)
    combined=canon(php(6,6)+core6)
    reduced=preprocess(combined)
    assert reduced['kind']=='REDUCE'
    assert encoded_size(reduced['child'])**3 <= encoded_size(combined)**2
    assert brute(reduced['child'])==brute(core6)
    assert enhanced_outer(combined,'components')[0]==brute(core6)
    assert preprocess(core0)['kind']=='FAIL'
    checks+=4
    rows.append({'bounded_successor_example':{'input_bits':encoded_size(combined),'child_bits':encoded_size(reduced['child']),'metrics':reduced['metrics'],'interpretation':'Certified easy-factor removal; not a compression of the arbitrary core.'}})
    rows.append({'hostile_checks':checks,'incomplete_instances_abstained':missing_rejected,'unsafe_representative_counterexample':g if False else [[1,2],[1,-2]],'controls':['renaming','sign flips','missing clauses','duplicate counts','unsafe representative','sparse labels','independent product','padding','external arbitrary core','broken symmetry'],'oracle_and_algebraic_audit':'No oracle is called; affine/Horn/2-SAT general decisions remain external controls, not hardness evidence.'})


def suite_baseline(rows: list[dict[str, Any]], p: int, h: int) -> None:
    baseline=load_baseline(); f=baseline.php(p,h)
    old,old_perf=measured(lambda:baseline.inner(f,'separator_fast'))
    new,new_perf=measured(lambda:preprocess(f))
    orbital,orb_perf=measured(lambda:preprocess(f,False))
    assert new['kind']=='VALUE' and new['value']==(p<=h)
    assert orbital['kind']=='VALUE' and orbital['value']==(p<=h)
    rows.append({'pigeons':p,'holes':h,'input_bits':encoded_size(f),'old_inner':old['metrics'],'old_performance':old_perf,'new_value':new,'new_performance':new_perf,'orbit_only':orbital,'orbit_only_performance':orb_perf,'comparability':'Same preallocated canonical source. Old result is an unevaluated exact plan; new result already decides. Source-read counters have different conventions; wall time and tracemalloc are separately labeled finite measurements.'})


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('--suite',choices=['small','orbits','capacity','hostile','baseline'],required=True)
    ap.add_argument('--max-holes',type=int,default=12)
    ap.add_argument('--pigeons',type=int,default=7)
    ap.add_argument('--holes',type=int,default=6)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    signal.signal(signal.SIGALRM,alarm_handler); signal.alarm(25)
    rows=[]; status='RUNNING'; error=None
    try:
        if args.suite=='small': suite_small(rows)
        elif args.suite=='orbits': suite_orbits(rows)
        elif args.suite=='capacity': suite_capacity(rows,args.max_holes)
        elif args.suite=='hostile': suite_hostile(rows)
        else: suite_baseline(rows,args.pigeons,args.holes)
        status='COMPUTATIONAL_PASS'
    except Exception as exc:
        status='PARTIAL_TIMEOUT' if isinstance(exc,BudgetExceeded) else 'FAILED'
        error=f'{type(exc).__name__}: {exc}'
    finally:
        signal.alarm(0)
        if tracemalloc.is_tracing(): tracemalloc.stop()
        data={'run_id':'ARC-0005','suite':args.suite,'status':status,'seed':SEED,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'baseline_blob_sha':'04cf06305b5beff2a36f631e4a38b5e09553c1ee','elapsed_seconds':time.monotonic()-START,'rows':rows,'error':error,'limits':['No asymptotic conclusion from timings.','Partial matrix discovery, not all-CNF coverage.','Canonical read-only input excluded from incremental allocation; input validation and all passes charged.','No full SR/VeriPB proof log is emitted; exact guards, constructive proof and independent finite checks are used.','Source propagation is capped at eight rounds; every resource-cap exit is FAIL, not UNSAT. Cell caps translate to bit bounds with logarithmic factors.','No universal implementation compiler or growing-depth ARC inference.']}
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
        print(json.dumps({k:data[k] for k in ('suite','status','elapsed_seconds','error')},indent=2))
        if args.suite in ('small','orbits','hostile'): print(json.dumps(rows,indent=2))
    if status!='COMPUTATIONAL_PASS': raise SystemExit(1)

if __name__=='__main__': main()
