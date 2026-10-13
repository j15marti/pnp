#!/usr/bin/env python3
"""Exact audit of affine Tseitin projection and nonlinear residual solving.

Python 3.10+, standard library only.
Run: python audit.py --out results.json

Graphs are explicit finite simple undirected graphs; isolated vertices count.
The nonlinear layer is an explicitly supplied CNF over edge variables.
This is not a general polynomial SAT solver or a lower-bound experiment.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import time
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Graph:
    n: int
    edges: tuple[tuple[int, int], ...]

    def validate(self) -> None:
        if self.n < 1:
            raise ValueError('At least one vertex is required.')
        if len(set(tuple(sorted(e)) for e in self.edges)) != len(self.edges):
            raise ValueError('Parallel edges are not supported.')
        for u, v in self.edges:
            if not (0 <= u < self.n and 0 <= v < self.n) or u == v:
                raise ValueError('Invalid endpoint or loop.')

    def rows(self) -> list[int]:
        out = [0] * self.n
        for e, (u, v) in enumerate(self.edges):
            out[u] ^= 1 << e
            out[v] ^= 1 << e
        return out

    def syndrome(self, x: int) -> int:
        return sum(((x & row).bit_count() & 1) << i
                   for i, row in enumerate(self.rows()))


def components(g: Graph, deleted_mask: int = 0) -> list[list[int]]:
    parent = list(range(g.n))
    def find(v: int) -> int:
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v
    for e, (u, v) in enumerate(g.edges):
        if not ((deleted_mask >> e) & 1):
            parent[find(u)] = find(v)
    groups: dict[int, list[int]] = {}
    for v in range(g.n):
        groups.setdefault(find(v), []).append(v)
    return list(groups.values())


def solve_linear(rows: Iterable[int], rhs: Iterable[int], nvars: int
                 ) -> tuple[int, list[int]] | None:
    """RREF over GF(2); returns a particular solution and kernel basis."""
    row_list, bit_list = list(rows), list(rhs)
    if nvars < 0 or len(row_list) != len(bit_list):
        raise ValueError('Incompatible system dimensions.')
    a = [[int(row), int(bit)] for row, bit in zip(row_list, bit_list)]
    if any(row < 0 or row >> nvars or bit not in (0, 1) for row, bit in a):
        raise ValueError('Invalid linear-system row.')
    pivots: list[int] = []
    r = 0
    for col in range(nvars):
        pivot = next((j for j in range(r, len(a)) if (a[j][0] >> col) & 1), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        for j in range(len(a)):
            if j != r and ((a[j][0] >> col) & 1):
                a[j][0] ^= a[r][0]
                a[j][1] ^= a[r][1]
        pivots.append(col)
        r += 1
    if any(row == 0 and bit for row, bit in a):
        return None
    particular = sum(a[j][1] << col for j, col in enumerate(pivots))
    pset = set(pivots)
    basis = []
    for free in range(nvars):
        if free in pset:
            continue
        z = 1 << free
        for j, col in enumerate(pivots):
            if (a[j][0] >> free) & 1:
                z |= 1 << col
        basis.append(z)
    return particular, basis


def affine_solution(g: Graph, charges: int) -> tuple[int, list[int]] | None:
    if charges < 0 or charges >> g.n:
        raise ValueError('Invalid charge vector.')
    return solve_linear(g.rows(), ((charges >> v) & 1 for v in range(g.n)), len(g.edges))


def projection_basis(kernel: list[int], rmask: int) -> list[tuple[int, int]]:
    """Projected independent vectors, each retaining a full kernel lift."""
    pivots: dict[int, tuple[int, int]] = {}
    for full in kernel:
        v, lift = full & rmask, full
        while v:
            pos = v.bit_length() - 1
            if pos not in pivots:
                pivots[pos] = (v, lift)
                break
            old_v, old_lift = pivots[pos]
            v ^= old_v
            lift ^= old_lift
    return list(pivots.values())


def span(basis: list[int]) -> list[int]:
    values = [0]
    for v in basis:
        values += [w ^ v for w in values]
    return values


def quotient_constraints(g: Graph, c: int, rmask: int) -> list[tuple[int, int]]:
    """One parity equation for each component of X-R, including isolates."""
    comps = components(g, rmask)
    label = {}
    for i, comp in enumerate(comps):
        for v in comp:
            label[v] = i
    lhs = [0] * len(comps)
    rhs = [0] * len(comps)
    for i, comp in enumerate(comps):
        for v in comp:
            rhs[i] ^= (c >> v) & 1
    for e, (u, v) in enumerate(g.edges):
        if (rmask >> e) & 1 and label[u] != label[v]:
            lhs[label[u]] ^= 1 << e
            lhs[label[v]] ^= 1 << e
    return list(zip(lhs, rhs))


def cnf_value(clauses: list[tuple[int, ...]], x: int) -> bool:
    return all(any(((x >> (abs(lit) - 1)) & 1) == (lit > 0)
                   for lit in clause) for clause in clauses)


def solve_residual(g: Graph, c: int, clauses: list[tuple[int, ...]]) -> dict:
    """Exact 2^rho * poly(N) search; count models and return one witness.

    Enumerates all projections rather than stop early, allowing exact audits.
    Memory is polynomial except for the small returned witness record.
    """
    m = len(g.edges)
    if any(lit == 0 or abs(lit) > m for clause in clauses for lit in clause):
        raise ValueError('CNF literal not an edge variable.')
    rmask = 0
    for clause in clauses:
        for lit in clause:
            rmask |= 1 << (abs(lit) - 1)
    linear = affine_solution(g, c)
    if linear is None:
        return {'sat': False, 'witness': None, 'projections_tested': 0,
                'models': 0, 'rho': None, 'support_size': rmask.bit_count()}
    a, kernel = linear
    pb = projection_basis(kernel, rmask)
    rho = len(pb)
    current = a
    old_gray = 0
    witness = None
    good = 0
    for i in range(1 << rho):
        gray = i ^ (i >> 1)
        if i:
            changed = (gray ^ old_gray).bit_length() - 1
            current ^= pb[changed][1]
        old_gray = gray
        if cnf_value(clauses, current):
            good += 1
            if witness is None:
                witness = current
    return {'sat': good > 0, 'witness': witness,
            'projections_tested': 1 << rho,
            'models': good * (1 << (len(kernel) - rho)),
            'rho': rho, 'support_size': rmask.bit_count()}


def cotree(g: Graph) -> list[int]:
    parent = list(range(g.n))
    def find(v: int) -> int:
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v
    out = []
    for e, (u, v) in enumerate(g.edges):
        a, b = find(u), find(v)
        if a == b:
            out.append(e)
        else:
            parent[a] = b
    return out


def graph_audit() -> dict:
    start = time.perf_counter()
    out = {'graphs': 0, 'graph_support_pairs': 0, 'rank_checks': 0,
           'consistent_charge_support_cases': 0,
           'boundary_membership_checks': 0, 'lifted_projection_checks': 0}
    for n in range(1, 5):
        universe = list(itertools.combinations(range(n), 2))
        for graph_bits in range(1 << len(universe)):
            g = Graph(n, tuple(e for i, e in enumerate(universe) if (graph_bits >> i) & 1))
            g.validate()
            m = len(g.edges)
            out['graphs'] += 1
            by_charge: dict[int, list[int]] = {}
            for x in range(1 << m):
                by_charge.setdefault(g.syndrome(x), []).append(x)
            zero = affine_solution(g, 0)
            assert zero is not None
            k = len(components(g))
            assert len(zero[1]) == m - n + k
            for rmask in range(1 << m):
                out['graph_support_pairs'] += 1
                pb = projection_basis(zero[1], rmask)
                rho = rmask.bit_count() + k - len(components(g, rmask))
                assert len(pb) == rho
                assert {x & rmask for x in by_charge[0]} == set(span([p for p, _ in pb]))
                out['rank_checks'] += 1
                patterns = span([1 << e for e in range(m) if (rmask >> e) & 1])
                for c in range(1 << n):
                    expected = {x & rmask for x in by_charge.get(c, [])}
                    constraints = quotient_constraints(g, c, rmask)
                    for y in patterns:
                        observed = all(((row & y).bit_count() & 1) == rhs
                                       for row, rhs in constraints)
                        assert observed == (y in expected)
                        out['boundary_membership_checks'] += 1
                    linear = affine_solution(g, c)
                    assert (linear is not None) == bool(expected)
                    if linear is not None:
                        out['consistent_charge_support_cases'] += 1
                        a, kernel = linear
                        lifts = projection_basis(kernel, rmask)
                        full = [a ^ t for t in span([v for _, v in lifts])]
                        assert {x & rmask for x in full} == expected
                        assert len(expected) == 1 << rho
                        multiplicity = 1 << (m - rmask.bit_count() - n + len(components(g, rmask)))
                        for y in expected:
                            assert sum((x & rmask) == y for x in by_charge[c]) == multiplicity
                        for x in full:
                            assert g.syndrome(x) == c
                            out['lifted_projection_checks'] += 1
    out['elapsed_seconds'] = time.perf_counter() - start
    return out


def nonlinear_audit() -> dict:
    start = time.perf_counter()
    g = Graph(6, tuple((u, v) for u in range(3) for v in range(3, 6)))
    free = cotree(g)
    assert len(free) == 4
    support = free[:3]
    clause_pool = [tuple((e + 1) if not ((pattern >> j) & 1) else -(e + 1)
                         for j, e in enumerate(support)) for pattern in range(8)]
    by_charge = {}
    for x in range(1 << len(g.edges)):
        by_charge.setdefault(g.syndrome(x), []).append(x)
    out = {'cotree_formula_cases': 0, 'sat_cases': 0, 'unsat_cases': 0,
           'random_general_support_cases': 0, 'random_renaming_cases': 0,
           'seed': 20261013}
    for c in sorted(by_charge):
        for which in range(256):
            clauses = [cl for j, cl in enumerate(clause_pool) if (which >> j) & 1]
            observed = solve_residual(g, c, clauses)
            expected = [x for x in by_charge[c] if cnf_value(clauses, x)]
            assert observed['sat'] == bool(expected)
            assert observed['models'] == len(expected)
            if expected:
                assert observed['witness'] in expected
            out['cotree_formula_cases'] += 1
            out['sat_cases' if expected else 'unsat_cases'] += 1
    rng = random.Random(out['seed'])
    for _ in range(400):
        c = rng.randrange(1 << g.n)
        clauses = [tuple((i + 1) * rng.choice((-1, 1)) for i in rng.sample(range(9), 3))
                   for _ in range(rng.randrange(1, 25))]
        observed = solve_residual(g, c, clauses)
        expected = [x for x in by_charge.get(c, []) if cnf_value(clauses, x)]
        assert observed['sat'] == bool(expected) and observed['models'] == len(expected)
        out['random_general_support_cases'] += 1
        perm = list(range(9)); rng.shuffle(perm)
        inv = {old: new for new, old in enumerate(perm)}
        g2 = Graph(g.n, tuple(g.edges[i] for i in perm))
        q2 = [tuple((inv[abs(lit) - 1] + 1) * (1 if lit > 0 else -1) for lit in cl)
              for cl in clauses]
        rng.shuffle(q2)
        check = solve_residual(g2, c, q2)
        assert check['sat'] == observed['sat'] and check['models'] == observed['models']
        out['random_renaming_cases'] += 1
    r_all = (1 << len(g.edges)) - 1
    masks = {'empty': 0,
             'star_of_one_vertex': sum(1 << e for e, (u, v) in enumerate(g.edges) if u == 0 or v == 0),
             'cotree': sum(1 << e for e in free), 'all_edges': r_all}
    out['rank_examples'] = [
        {'support': name, 'edges_in_support': mask.bit_count(),
         'components_after_deletion': len(components(g, mask)),
         'rho': len(projection_basis(affine_solution(g, 0)[1], mask))}
        for name, mask in masks.items()]
    out['elapsed_seconds'] = time.perf_counter() - start
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=Path('results.json'))
    parser.add_argument('--chunk', choices=['graph', 'nonlinear', 'all'], default='all')
    args = parser.parse_args()
    results = {'status': 'COMPUTATIONAL', 'independent_review': 'pending',
               'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               'scope': 'Finite audits; symbolic proofs are separate. No P-vs-NP lower bound.'}
    if args.chunk in ('graph', 'all'):
        results['graph_projection'] = graph_audit()
    if args.chunk in ('nonlinear', 'all'):
        results['nonlinear'] = nonlinear_audit()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
