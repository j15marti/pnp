#!/usr/bin/env python3
"""ROOTGLUE1: independent LSPV-5 root-list and shared-constraint audit.

Python 3.10+, standard library only. Production arithmetic and solvers are
uncapped. Only each audit batch has a cooperative 25-second deadline.
Run each batch separately, for example:
  python root_glue_audit.py --batch fields --output fields.json
  python root_glue_audit.py --batch affine --output affine.json
  python root_glue_audit.py --batch graphs --n 5 --output graphs5.json
  python root_glue_audit.py --batch carrier --output carrier.json
All field enumeration and assignment enumeration occurs in test oracles,
not in the trace selector or affine-domain decision algorithm.
"""
from __future__ import annotations
import argparse
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import itertools
import json
from pathlib import Path
import random
import time

SEED = 202610140449

def bmod(a: int, f: int) -> int:
    if f <= 0:
        raise ValueError('nonpositive binary divisor')
    while a.bit_length() >= f.bit_length():
        a ^= f << (a.bit_length() - f.bit_length())
    return a

def bgcd(a: int, b: int) -> int:
    while b:
        a, b = b, bmod(a, b)
    return a

def bsquare(a: int) -> int:
    return sum(((a >> i) & 1) << (2*i) for i in range(a.bit_length()))

def is_irreducible(f: int) -> bool:
    if type(f) is not int or f < 2:
        return False
    d = f.bit_length()-1
    x = bmod(2, f)
    y = x
    for k in range(1, d+1):
        y = bmod(bsquare(y), f)
        if k <= d//2 and bgcd(f, y ^ x) != 1:
            return False
    return y == x

@dataclass(frozen=True)
class Field:
    f: int
    def __post_init__(self) -> None:
        if not is_irreducible(self.f):
            raise ValueError('an explicit irreducible binary modulus is required')
    @property
    def d(self) -> int:
        return self.f.bit_length()-1
    @property
    def order(self) -> int:
        return 1 << self.d
    def validate(self, a: int) -> None:
        if type(a) is not int or not 0 <= a < self.order:
            raise ValueError('invalid field element')
    def mul(self, a: int, b: int) -> int:
        v = 0
        while b:
            if b & 1:
                v ^= a
            b >>= 1
            a <<= 1
            if a & self.order:
                a ^= self.f
        return v
    def power(self, a: int, k: int) -> int:
        if k < 0:
            raise ValueError('negative exponent')
        v = 1
        while k:
            if k & 1:
                v = self.mul(v, a)
            k >>= 1
            if k:
                a = self.mul(a, a)
        return v
    def inv(self, a: int) -> int:
        if not a:
            raise ZeroDivisionError('zero field element')
        return self.power(a, self.order-2)

def trim(p: list[int]) -> list[int]:
    p = p[:]
    while p and not p[-1]:
        p.pop()
    return p

def add(p: list[int], q: list[int]) -> list[int]:
    r = [0] * max(len(p), len(q))
    for i, v in enumerate(p):
        r[i] ^= v
    for i, v in enumerate(q):
        r[i] ^= v
    return trim(r)

def pmul(p: list[int], q: list[int], K: Field) -> list[int]:
    if not p or not q:
        return []
    r = [0] * (len(p)+len(q)-1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i+j] ^= K.mul(a, b)
    return trim(r)

def divrem(p: list[int], q: list[int], K: Field) -> tuple[list[int], list[int]]:
    p, q = trim(p), trim(q)
    if not q:
        raise ZeroDivisionError('zero polynomial divisor')
    quot = [0] * max(0, len(p)-len(q)+1)
    inv = K.inv(q[-1])
    while p and len(p) >= len(q):
        i = len(p)-len(q)
        c = K.mul(p[-1], inv)
        quot[i] ^= c
        for j, b in enumerate(q):
            p[i+j] ^= K.mul(c, b)
        p = trim(p)
    return trim(quot), p

def monic(p: list[int], K: Field) -> list[int]:
    p = trim(p)
    if not p:
        return []
    v = K.inv(p[-1])
    return [K.mul(a, v) for a in p]

def pgcd(p: list[int], q: list[int], K: Field) -> list[int]:
    p, q = trim(p), trim(q)
    while q:
        p, q = q, divrem(p, q, K)[1]
    return monic(p, K)

def square_mod(p: list[int], g: list[int], K: Field) -> list[int]:
    r = [0] * max(0, 2*len(p)-1)
    for i, a in enumerate(p):
        r[2*i] = K.mul(a, a)
    return divrem(r, g, K)[1]

def peval(p: list[int], x: int, K: Field) -> int:
    r = 0
    for a in reversed(p):
        r = K.mul(r, x) ^ a
    return r

def root_factor(p: list[int], K: Field) -> list[int]:
    """Squarefree product of the field-linear factors of nonzero p."""
    p = monic(p, K)
    if not p:
        raise ValueError('zero polynomial is handled separately')
    t = divrem([0, 1], p, K)[1]
    for _ in range(K.d):
        t = square_mod(t, p, K)
    return pgcd(p, add(t, [0, 1]), K)

def isolate_split_root(g: list[int], K: Field) -> int:
    """g is monic, split, squarefree, and nonconstant."""
    g = g[:]
    for j in range(K.d):
        if len(g) == 2:
            return g[0]
        t = divrem([0, 1 << j], g, K)[1]
        trace: list[int] = []
        for _ in range(K.d):
            trace = add(trace, t)
            t = square_mod(t, g, K)
        zero_part = pgcd(g, trace, K)
        if len(zero_part) > 1:
            g = zero_part
    if len(g) != 2:
        raise AssertionError('trace pairing did not isolate one root')
    return g[0]

def list_roots(p: list[int], K: Field) -> list[int] | None:
    """Return all distinct roots. None means the zero polynomial, all of K.

    Repeated trace isolation and exact division is polynomial in explicit
    polynomial degree and field degree. It does not iterate through K.
    """
    for a in p:
        K.validate(a)
    p = trim(p)
    if not p:
        return None
    g = root_factor(p, K)
    roots: list[int] = []
    while len(g) > 1:
        a = isolate_split_root(g, K)
        if peval(p, a, K):
            raise AssertionError('root failed original equation')
        roots.append(a)
        g, r = divrem(g, [a, 1], K)
        if r:
            raise AssertionError('inexact linear factor removal')
    return sorted(roots)

def linear_solve(n: int, equations: list[tuple[int, int]]) -> tuple[int, list[int]] | None:
    """RREF over F2, including all free variables in returned kernel basis."""
    if type(n) is not int or n < 0:
        raise ValueError('invalid variable count')
    for row, rhs in equations:
        if type(row) is not int or not 0 <= row < (1 << n) or type(rhs) is not int or rhs not in (0, 1):
            raise ValueError('invalid binary linear equation')
    a = [row | (rhs << n) for row, rhs in equations]
    pivots: list[int] = []
    k = 0
    for j in range(n):
        i = next((i for i in range(k, len(a)) if (a[i] >> j) & 1), None)
        if i is None:
            continue
        a[k], a[i] = a[i], a[k]
        for i in range(len(a)):
            if i != k and (a[i] >> j) & 1:
                a[i] ^= a[k]
        pivots.append(j)
        k += 1
    mask = (1 << n)-1
    if any(not (row & mask) and ((row >> n) & 1) for row in a):
        return None
    point = sum(((a[i] >> n) & 1) << j for i, j in enumerate(pivots))
    basis = []
    for free in range(n):
        if free not in pivots:
            v = 1 << free
            for i, p in enumerate(pivots):
                v |= ((a[i] >> free) & 1) << p
            basis.append(v)
    return point, basis

@dataclass(frozen=True)
class DomainConstraint:
    rows: tuple[int, ...]
    offset: int
    roots: tuple[int, ...] | None
    def value(self, z: int) -> int:
        return self.offset ^ sum(((row & z).bit_count() & 1) << j for j, row in enumerate(self.rows))

def solve_affine_domains(n: int, constraints: list[DomainConstraint], extra: list[tuple[int, int]] | None = None) -> tuple[str, int | None]:
    """Exact on affine root domains; NONAFFINE means no algorithmic claim."""
    equations = list(extra or [])
    nonlinear = False
    for c in constraints:
        d = len(c.rows)
        if type(c.offset) is not int or not 0 <= c.offset < (1 << d):
            raise ValueError('invalid affine offset')
        if any(type(v) is not int or not 0 <= v < (1 << n) for v in c.rows):
            raise ValueError('invalid affine map')
        if c.roots is None:
            continue
        if any(type(v) is not int or not 0 <= v < (1 << d) for v in c.roots) or len(set(c.roots)) != len(c.roots):
            raise ValueError('invalid root list')
        if not c.roots:
            return 'UNSAT', None
        base = c.roots[0]
        ortho_solution = linear_solve(d, [(r ^ base, 0) for r in c.roots])
        assert ortho_solution is not None
        ortho = ortho_solution[1]
        rank = d-len(ortho)
        if len(c.roots) != (1 << rank):
            nonlinear = True
            continue
        for w in ortho:
            row = 0
            for j, original in enumerate(c.rows):
                if (w >> j) & 1:
                    row ^= original
            rhs = ((w & (base ^ c.offset)).bit_count() & 1)
            equations.append((row, rhs))
    if nonlinear:
        return 'NONAFFINE', None
    result = linear_solve(n, equations)
    if result is None:
        return 'UNSAT', None
    z = result[0]
    if not all(c.roots is None or c.value(z) in c.roots for c in constraints):
        raise AssertionError('affine-domain lifting failed')
    return 'SAT', z

MAGIC = '01011010'
def encode_graph(n: int, edges: list[tuple[int, int]]) -> str:
    if type(n) is not int or n < 1:
        raise ValueError('positive explicit vertex count required')
    if any(type(u) is not int or type(v) is not int or not 0 <= u < v < n for u, v in edges) or len(set(edges)) != len(edges):
        raise ValueError('invalid simple graph')
    s = set(edges)
    return MAGIC + '1'*n + '0' + ''.join('1' if (u, v) in s else '0' for u in range(n) for v in range(u+1, n))

def decode_graph(bits: str) -> tuple[int, list[tuple[int, int]]]:
    if type(bits) is not str or any(c not in '01' for c in bits) or not bits.startswith(MAGIC):
        raise ValueError('invalid bit encoding')
    stop = bits.find('0', len(MAGIC))
    if stop < 0:
        raise ValueError('unterminated unary length')
    n = stop-len(MAGIC)
    tail = bits[stop+1:]
    if n < 1 or len(tail) != n*(n-1)//2:
        raise ValueError('wrong adjacency length')
    pairs = list(itertools.combinations(range(n), 2))
    return n, [edge for bit, edge in zip(tail, pairs) if bit == '1']

def norm4(z: int) -> int:
    a, b = z & 1, (z >> 1) & 1
    return a ^ b ^ (a & b)

def cube_constraints(n: int, edges: list[tuple[int, int]]) -> list[DomainConstraint]:
    out = [DomainConstraint((1 << (2*v), 1 << (2*v+1)), 0, (1, 2, 3)) for v in range(n)]
    out.extend(DomainConstraint(((1 << (2*u)) ^ (1 << (2*v)), (1 << (2*u+1)) ^ (1 << (2*v+1))), 0, (1, 2, 3)) for u, v in edges)
    return out

def carrier(n: int) -> tuple[int, list[tuple[int, int]], list[int], list[int]]:
    if type(n) is not int or n < 1:
        raise ValueError('invalid carrier size')
    k = 2*n
    edges = []
    for j in range(k):
        a, b, c = 3*j, 3*j+1, 3*j+2
        edges.extend([(a, b), (b, c), (a, c)])
    edges.extend((3*j+1, 3*(j+1)) for j in range(k-1))
    chords = [3*j+2 for j in range(k)]
    rows = [0] * (3*k)
    for i, (u, v) in enumerate(edges):
        rows[u] |= 1 << i
        rows[v] |= 1 << i
    return 3*k, edges, chords, rows

def cycle_lift(z: int, n: int) -> int:
    return sum(7 << (3*j) for j in range(2*n) if (z >> j) & 1)

class Audit:
    def __init__(self) -> None:
        self.start = time.monotonic()
        self.counts: Counter[str] = Counter()
    def check(self, condition: bool, name: str) -> None:
        if time.monotonic()-self.start > 25:
            raise TimeoutError('audit batch exceeded cooperative 25-second cap')
        self.counts[name] += 1
        if not condition:
            raise AssertionError(name)


def fields_batch(A: Audit) -> dict:
    presentations = targets = 0
    rows = []
    for d in range(1, 7):
        for f in range(1 << d, 1 << (d+1)):
            brute_irred = all(bmod(f, h) != 0 for k in range(1, d//2+1) for h in range(1 << k, 1 << (k+1)))
            A.check(is_irreducible(f) == brute_irred, 'irreducibility_reference')
            if not brute_irred:
                continue
            presentations += 1
            K = Field(f)
            for b in range(1 << d):
                p = [b, 0, 0, 1]
                got = list_roots(p, K)
                expected = [x for x in range(1 << d) if K.mul(K.mul(x, x), x) == b]
                A.check(got == expected, 'complete_cube_root_list')
                targets += 1
            for p in ([], [1], [0, 0, 1], [1, 0, 1], [0, 1], [1, 1, 1], [1, 1, 0, 0, 1]):
                got = list_roots(p, K)
                expected = [x for x in range(1 << d) if peval(p, x, K) == 0]
                A.check((got is None and len(expected) == (1 << d)) or got == expected, 'general_univariate_controls')
            rows.append({'degree': d, 'modulus': f, 'cube_targets': 1 << d})
    K = Field(7)
    for x in range(4):
        A.check(K.power(x, 3) == norm4(x), 'F4_norm_identity')
    for f in (0, 1, -1, True, 5, 9, 15):
        try:
            Field(f)
        except ValueError:
            A.check(True, 'malformed_or_reducible_field')
        else:
            A.check(False, 'malformed_or_reducible_field')
    return {'presentations': presentations, 'cube_targets': targets, 'fields': rows}


def affine_batch(A: Audit) -> dict:
    rng = random.Random(SEED)
    cases = assignments = nonaffine = 0
    for n in range(0, 8):
        for _ in range(45):
            constraints = []
            polynomial_records = []
            for j in range(rng.randrange(1, 6)):
                d = rng.randrange(1, 4)
                moduli = [f for f in range(1 << d, 1 << (d+1)) if is_irreducible(f)]
                K = Field(rng.choice(moduli))
                base = rng.randrange(K.order)
                span = {0}
                for _ in range(rng.randrange(0, min(d, 2)+1)):
                    v = rng.randrange(K.order)
                    span |= {x ^ v for x in list(span)}
                roots = sorted(base ^ s for s in span)
                if rng.randrange(12) == 0:
                    roots = []
                p = [1]
                for r in roots:
                    p = pmul(p, [r, 1], K)
                extracted = list_roots(p, K)
                A.check(extracted == roots, 'affine_complete_root_extraction')
                c = DomainConstraint(tuple(rng.randrange(1 << n) for _ in range(d)), rng.randrange(K.order), tuple(extracted or []))
                constraints.append(c)
                polynomial_records.append((K, p, c))
            extra = [(rng.randrange(1 << n), rng.randrange(2)) for _ in range(rng.randrange(3))]
            status, selected = solve_affine_domains(n, constraints, extra)
            expected = []
            for z in range(1 << n):
                original = all(peval(p, c.value(z), K) == 0 for K, p, c in polynomial_records) and all(((r & z).bit_count() & 1) == b for r, b in extra)
                if original:
                    expected.append(z)
                assignments += 1
            A.check((status == 'SAT') == bool(expected), 'affine_solver_exact_decision')
            A.check(selected is None or selected in expected, 'affine_solver_witness')
            A.check(status != 'NONAFFINE', 'affine_class_recognition')
            cases += 1
        c = DomainConstraint((0, 0), 0, (1, 2, 3))
        A.check(solve_affine_domains(n, [c])[0] == 'NONAFFINE', 'three_point_scope_guard')
        nonaffine += 1
    # Two roots do not mean arbitrary binary CSP: equations here are affine over F2.
    for n in (1, 2, 3, 8):
        c = DomainConstraint((1, 0), 0, (0, 1))
        A.check(solve_affine_domains(n, [c])[0] == 'SAT', 'two_root_domain_control')
    return {'cases': cases, 'truth_assignments': assignments, 'nonaffine_scope_controls': nonaffine}


def graphs_batch(A: Audit, n: int) -> dict:
    if not 1 <= n <= 5:
        raise ValueError('exhaustive graph batch restricted to 1 <= n <= 5')
    pairs = list(itertools.combinations(range(n), 2))
    rows = []
    total_witnesses = total_assignments = 0
    graph_yes = 0
    for mask in range(1 << len(pairs)):
        edges = [e for j, e in enumerate(pairs) if (mask >> j) & 1]
        code = encode_graph(n, edges)
        A.check(decode_graph(code) == (n, edges), 'graph_encoding_roundtrip')
        expected = sum(all(col[u] != col[v] for u, v in edges) for col in itertools.product((1, 2, 3), repeat=n))
        got = 0
        for z in range(1 << (2*n)):
            col = [(z >> (2*v)) & 3 for v in range(n)]
            polynomial = all(norm4(w) == 1 for w in col) and all(norm4(col[u] ^ col[v]) == 1 for u, v in edges)
            coloring = all(col) and all(col[u] != col[v] for u, v in edges)
            A.check(polynomial == coloring, 'pointwise_color_polynomial_equivalence')
            total_assignments += 1
            got += int(polynomial)
        A.check(got == expected, 'exact_solution_count')
        if got:
            graph_yes += 1
        total_witnesses += got
        rows.append({'edge_mask': mask, 'edges': len(edges), 'solutions': got})
    return {'n': n, 'graphs': len(rows), 'YES': graph_yes, 'NO': len(rows)-graph_yes, 'field_assignments': total_assignments, 'total_solutions': total_witnesses, 'records': rows}


def carrier_batch(A: Audit) -> dict:
    raw_assignments = lifts = 0
    rng = random.Random(SEED+1)
    details = []
    for n in range(1, 6):
        v, edges, chords, B = carrier(n)
        A.check((v, len(edges), len(chords)) == (6*n, 8*n-1, 2*n), 'carrier_size_ledger')
        degree = Counter(t for e in edges for t in e)
        A.check(max(degree.values()) <= 3, 'carrier_max_degree')
        kernel = linear_solve(len(edges), [(r, 0) for r in B])
        A.check(kernel is not None and len(kernel[1]) == 2*n, 'carrier_kernel_dimension')
        for z in range(1 << (2*n)):
            x = cycle_lift(z, n)
            A.check(all((r & x).bit_count() % 2 == 0 for r in B), 'lift_original_incidence')
            A.check(sum(((x >> edge) & 1) << j for j, edge in enumerate(chords)) == z, 'lift_cotree_identity')
            lifts += 1
        # Charge-matched particular solutions a with zero cotree, plus isolates.
        for _ in range(12):
            source_x = rng.randrange(1 << len(edges))
            charges = [(r & source_x).bit_count() & 1 for r in B]
            eq = list(zip(B, charges)) + [(1 << c, 0) for c in chords]
            sol = linear_solve(len(edges), eq)
            A.check(sol is not None and not sol[1], 'unique_zero_cotree_particular')
            a = sol[0]
            z = rng.randrange(1 << (2*n))
            x = a ^ cycle_lift(z, n)
            A.check(all(((r & x).bit_count() & 1) == c for r, c in zip(B, charges)), 'a_plus_Lz_original_equations')
            A.check(linear_solve(len(edges), eq+[(0, 1)]) is None, 'odd_isolate_rejection')
        if n <= 2:
            graph_edges = [(0, 1)] if n == 2 else []
            models = 0
            for x in range(1 << len(edges)):
                parity = all((r & x).bit_count() % 2 == 0 for r in B)
                z = sum(((x >> edge) & 1) << j for j, edge in enumerate(chords))
                col = [(z >> (2*j)) & 3 for j in range(n)]
                residual = all(norm4(c) == 1 for c in col) and all(norm4(col[u] ^ col[w]) == 1 for u, w in graph_edges)
                expected = (x == cycle_lift(z, n)) and all(col) and all(col[u] != col[w] for u, w in graph_edges)
                A.check((parity and residual) == expected, 'full_original_edge_truth_table')
                models += int(parity and residual)
                raw_assignments += 1
            details.append({'n': n, 'original_edge_assignments': 1 << len(edges), 'coupled_models': models})
    # Smallest complete-graph obstruction: every local equation has three roots.
    for n, expected in ((3, 6), (4, 0)):
        edges = list(itertools.combinations(range(n), 2))
        constraints = cube_constraints(n, edges)
        A.check(all(len(c.roots or ()) == 3 for c in constraints), 'local_three_roots')
        count = sum(all(c.value(z) in c.roots for c in constraints) for z in range(1 << (2*n)))
        A.check(count == expected, 'K3_K4_coupled_control')
        # Arc consistency preserves all three colors at every vertex in K4.
        A.check(all(any(a != b for b in (1, 2, 3)) for a in (1, 2, 3)), 'arc_consistency_does_not_decide_K4')
    good = encode_graph(3, [(0, 1)])
    malformed = ['', '2', good+'0', good[:-1], MAGIC+'0', MAGIC+'111', good.replace('0', 'x', 1), None, 12, MAGIC+'10'+'1']
    for bad in malformed:
        try:
            decode_graph(bad)
        except ValueError:
            A.check(True, 'invalid_graph_rejection')
        else:
            A.check(False, 'invalid_graph_rejection')
    return {'full_edge_assignments': raw_assignments, 'zero_charge_lifts': lifts, 'charged_lifts': 60, 'original_truth_tables': details, 'K3_solutions': 6, 'K4_solutions': 0, 'malformed_controls': len(malformed)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', choices=['fields', 'affine', 'graphs', 'carrier'], required=True)
    parser.add_argument('--n', type=int, default=4)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    audit = Audit()
    result = {'status': 'COMPUTATIONAL', 'run_id': 'ROOTGLUE1', 'batch': args.batch, 'seed': SEED, 'timestamp_utc': datetime.now(timezone.utc).isoformat(), 'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'limitations': 'Finite exact/seeded tests; not an asymptotic lower bound. Independent author review still required for new ROOTGLUE1 transfer.'}
    try:
        if args.batch == 'fields':
            result['data'] = fields_batch(audit)
        elif args.batch == 'affine':
            result['data'] = affine_batch(audit)
        elif args.batch == 'graphs':
            result['data'] = graphs_batch(audit, args.n)
        else:
            result['data'] = carrier_batch(audit)
        result['failures'] = 0
    except Exception as exc:
        result['failures'] = 1
        result['error'] = f'{type(exc).__name__}: {exc}'
        raise
    finally:
        result['counts'] = dict(audit.counts)
        result['assertions'] = sum(audit.counts.values())
        result['elapsed_seconds'] = time.monotonic()-audit.start
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2)+'\n')
        print(json.dumps({k: result[k] for k in ('batch', 'assertions', 'failures', 'elapsed_seconds')}, indent=2))

if __name__ == '__main__':
    main()
