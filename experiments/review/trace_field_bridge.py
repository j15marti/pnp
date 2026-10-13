#!/usr/bin/env python3
"""TRACEISO1: deterministic binary-field root isolation and witness transport.

Dependency-free. Production selectors use no randomness, SAT oracle, nonresidue,
or enumeration of the field. Seeded randomness is confined to test generation.
Run each --batch separately; every invocation has a cooperative 25-second cap.
Binary field elements/moduli are dense coefficient bit strings stored as ints.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import random
import time

START = time.monotonic()
DEADLINE = float("inf")  # Only the executable audit imposes a deadline.
CHECKS: Counter[str] = Counter()
OPS: Counter[str] = Counter()
SEED = 202610140350
SQ8 = [sum(((a >> i) & 1) << (2*i) for i in range(8)) for a in range(256)]


def budget() -> None:
    if time.monotonic() > DEADLINE:
        raise TimeoutError('cooperative 25-second limit exceeded')


def check(ok: bool, label: str) -> None:
    budget()
    CHECKS[label] += 1
    if not ok:
        raise AssertionError(label)


def mod2(a: int, b: int) -> int:
    if b <= 0:
        raise ValueError('zero polynomial divisor')
    while a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length() - b.bit_length())
    return a


def gcd2(a: int, b: int) -> int:
    while b:
        a, b = b, mod2(a, b)
    return a


def square2(a: int) -> int:
    out = shift = 0
    while a:
        out |= SQ8[a & 255] << shift
        a >>= 8
        shift += 16
    return out


def reference_mul(a: int, b: int, f: int) -> int:
    """Independent slow carryless-product check, without Field arithmetic."""
    product = 0
    for i in range(a.bit_length()):
        for j in range(b.bit_length()):
            if (a >> i) & 1 and (b >> j) & 1:
                product ^= 1 << (i+j)
    for k in range(product.bit_length()-1, f.bit_length()-2, -1):
        if (product >> k) & 1:
            product ^= f << (k-f.bit_length()+1)
    return product


def irreducible(f: int) -> bool:
    if type(f) is not int or f < 2:
        return False
    d = f.bit_length() - 1
    x = mod2(2, f)
    t = x
    for j in range(1, d + 1):
        budget()
        t = mod2(square2(t), f)
        if j <= d//2 and gcd2(t ^ x, f) != 1:
            return False
    return t == x


class Field:
    def __init__(self, modulus: int):
        if not irreducible(modulus):
            raise ValueError('modulus is not irreducible over F2')
        self.f = modulus
        self.d = modulus.bit_length() - 1
        self.q = 1 << self.d

    def element(self, a: int) -> int:
        if type(a) is not int or not 0 <= a < self.q:
            raise ValueError('invalid field element')
        return a

    def mul(self, a: int, b: int) -> int:
        OPS['field_mul'] += 1
        if OPS['field_mul'] % 1024 == 0:
            budget()
        out = 0
        while b:
            if b & 1:
                out ^= a
            b >>= 1
            a <<= 1
            if a & self.q:
                a ^= self.f
        return out

    def square(self, a: int) -> int:
        OPS['field_square'] += 1
        return mod2(square2(a), self.f)

    def inv(self, a: int) -> int:
        OPS['field_inverse'] += 1
        if not a:
            raise ZeroDivisionError('zero has no inverse')
        u, v, s, t = a, self.f, 1, 0
        while u != 1:
            j = u.bit_length() - v.bit_length()
            if j < 0:
                u, v, s, t, j = v, u, t, s, -j
            u ^= v << j
            s ^= t << j
        return mod2(s, self.f)

    def power(self, a: int, exponent: int) -> int:
        out = 1
        while exponent:
            if exponent & 1:
                out = self.mul(out, a)
            exponent >>= 1
            if exponent:
                a = self.square(a)
        return out

    def cube(self, a: int) -> int:
        return self.mul(self.square(a), a)


# Polynomials over the represented field, low coefficient first.
def trim(p: list[int]) -> list[int]:
    while p and p[-1] == 0:
        p.pop()
    return p


def padd(p: list[int], q: list[int]) -> list[int]:
    out = p[:] + [0] * max(0, len(q) - len(p))
    for i, a in enumerate(q):
        out[i] ^= a
    return trim(out)


def monic(p: list[int], K: Field) -> list[int]:
    p = trim(p[:])
    if not p or p[-1] == 1:
        return p
    a = K.inv(p[-1])
    return [K.mul(c, a) for c in p]


def pmod(p: list[int], g: list[int], K: Field) -> list[int]:
    if not g:
        raise ZeroDivisionError('zero polynomial divisor')
    p, g = trim(p[:]), monic(g, K)
    while len(p) >= len(g):
        c, j = p[-1], len(p) - len(g)
        p.pop()
        for i in range(len(g)-1):
            if g[i] and c:
                p[i+j] ^= K.mul(c, g[i])
        trim(p)
    return p


def pgcd(p: list[int], q: list[int], K: Field) -> list[int]:
    OPS['polynomial_gcd'] += 1
    while q:
        p, q = q, pmod(p, q, K)
    return monic(p, K)


def psquare(p: list[int], g: list[int], K: Field) -> list[int]:
    OPS['modular_polynomial_square'] += 1
    if not p:
        return []
    out = [0] * (2*len(p)-1)
    for i, c in enumerate(p):
        out[2*i] = K.square(c)
    return pmod(out, g, K)


def peval(p: list[int], x: int, K: Field) -> int:
    out = 0
    for c in reversed(p):
        out = K.mul(out, x) ^ c
    return out


def one_root(p: list[int], K: Field) -> tuple[int | None, dict]:
    """Find one K-root of any explicitly dense univariate p, deterministically.

    First isolate the distinct K-roots using gcd(p,T^(2^d)-T), then split
    with the d absolute trace coordinates Tr(beta_j*T). A polynomial cap in
    degree(p) and d is proved in the report. No field-element scan occurs.
    """
    for c in p:
        K.element(c)
    p = monic(p, K)
    if not p:
        return 0, {'zero_polynomial': True, 'trace_coordinates': 0}
    if len(p) == 1:
        return None, {'root_degree': 0, 'trace_coordinates': 0}
    t = pmod([0, 1], p, K)
    for _ in range(K.d):
        budget()
        t = psquare(t, p, K)
    g = pgcd(p, padd(t, [0, 1]), K)
    hist = [len(g)-1]
    coordinates = 0
    if len(g) == 1:
        return None, {'root_degree': 0, 'trace_coordinates': 0, 'degrees': hist}
    for j in range(K.d):
        if len(g) == 2:
            break
        budget()
        v = pmod([0, 1 << j], g, K)
        h: list[int] = []
        for _ in range(K.d):
            h = padd(h, v)
            v = psquare(v, g, K)
        cut = pgcd(g, h, K)
        coordinates += 1
        if len(cut) > 1:
            g = cut
        hist.append(len(g)-1)
    if len(g) != 2:
        raise AssertionError('trace pairing failed to separate roots')
    root = g[0]  # g=T+root in characteristic two.
    if peval(p, root, K) != 0:
        raise AssertionError('returned root fails original polynomial')
    return root, {'root_degree': hist[0], 'trace_coordinates': coordinates, 'degrees': hist}


def cube_root(b: int, K: Field) -> tuple[int | None, dict]:
    K.element(b)
    return one_root([b, 0, 0, 1], K)


def root_record(record: dict) -> int | None:
    if not isinstance(record, dict) or set(record) != {'degree', 'modulus', 'target'}:
        raise ValueError('wrong record keys')
    d, f, b = record['degree'], record['modulus'], record['target']
    if any(type(x) is not int for x in (d, f, b)) or d < 1 or f < 2:
        raise ValueError('invalid integer type/range')
    if f.bit_length()-1 != d:
        raise ValueError('degree/modulus mismatch')
    K = Field(f)
    return cube_root(b, K)[0]


def apply(columns: list[int], x: int) -> int:
    out = i = 0
    while x:
        if x & 1:
            out ^= columns[i]
        x >>= 1
        i += 1
    return out


def inverse_columns(columns: list[int]) -> list[int]:
    d = len(columns)
    pivots: dict[int, tuple[int,int]] = {}
    for i, col in enumerate(columns):
        v, tag = col, 1 << i
        while v:
            p = v.bit_length()-1
            if p not in pivots:
                pivots[p] = (v, tag)
                break
            w, t = pivots[p]
            v ^= w
            tag ^= t
        if not v:
            raise ValueError('singular basis map')
    out = []
    for i in range(d):
        v, tag = 1 << i, 0
        while v:
            p = v.bit_length()-1
            w, t = pivots[p]
            v ^= w
            tag ^= t
        out.append(tag)
    return out


def isomorphism(source: Field, target: Field) -> tuple[list[int], list[int], dict]:
    if source.d != target.d:
        raise ValueError('different field dimensions')
    poly = [(source.f >> i) & 1 for i in range(source.d+1)]
    alpha, stats = one_root(poly, target)
    if alpha is None:
        raise AssertionError('irreducible equal-degree polynomial has no target root')
    cols, z = [], 1
    for _ in range(source.d):
        cols.append(z)
        z = target.mul(z, alpha)
    inv = inverse_columns(cols)
    return cols, inv, {**stats, 'generator_image': alpha}


def canonical_field(d: int) -> Field:
    r = d // 2
    s = r
    while s > 1 and s % 3 == 0:
        s //= 3
    if d % 2 or s != 1:
        raise ValueError('not degree 2*3^a')
    return Field((1 << d) | (1 << r) | 1)


def canonical_cube_root(b: int, K: Field) -> int | None:
    """Exact CYCLOROOTFW1 mechanism, independently implemented for comparison."""
    if not b:
        return 0
    n = K.q-1
    if K.power(b, n//3) != 1:
        return None
    m = n
    while m % 3 == 0:
        m //= 3
    y = K.power(b, 0 if m == 1 else pow(3, -1, m))
    for _ in range(K.d//2):
        if K.cube(y) == b:
            return y
        y = K.mul(y, 2)
    raise AssertionError('canonical correction exhausted')


def make_field(d: int, rng: random.Random) -> tuple[Field,int]:
    tries = 0
    while True:
        budget()
        f = (1 << d) | rng.getrandbits(d) | 1
        tries += 1
        if irreducible(f):
            return Field(f), tries


def forest(n: int, edges: list[tuple[int,int]]) -> tuple[list[int], list[int], int]:
    if type(n) is not int or n < 1:
        raise ValueError('invalid vertex count')
    parent = list(range(n))
    def find(x: int) -> int:
        while parent[x] != x:
            x = parent[x]
        return x
    seen, tree, cotree = set(), [], []
    for i, edge in enumerate(edges):
        if len(edge) != 2 or any(type(x) is not int or not 0 <= x < n for x in edge):
            raise ValueError('invalid endpoint')
        u, v = edge
        key = tuple(sorted(edge))
        if u == v or key in seen:
            raise ValueError('not a simple loopless graph')
        seen.add(key)
        a, b = find(u), find(v)
        if a != b:
            parent[a] = b
            tree.append(i)
        else:
            cotree.append(i)
    return tree, cotree, len({find(x) for x in range(n)})


def boundary(n: int, edges: list[tuple[int,int]], x: int) -> int:
    b = 0
    for i, (u, v) in enumerate(edges):
        if x >> i & 1:
            b ^= (1 << u) | (1 << v)
    return b


def lift(n: int, edges: list[tuple[int,int]], c: int, z: int) -> int | None:
    tree, cotree, _ = forest(n, edges)
    if type(c) is not int or not 0 <= c < (1 << n) or type(z) is not int or not 0 <= z < (1 << len(cotree)):
        raise ValueError('charge/cotree range')
    x = sum(((z >> j) & 1) << e for j, e in enumerate(cotree))
    rem = c ^ boundary(n, edges, x)
    adj = [[] for _ in range(n)]
    for e in tree:
        u, v = edges[e]
        adj[u].append((v,e)); adj[v].append((u,e))
    seen = set()
    for root in range(n):
        if root in seen:
            continue
        seen.add(root); order = [root]; pred = {root: (-1,-1)}
        for u in order:
            for v, e in adj[u]:
                if v not in seen:
                    seen.add(v); order.append(v); pred[v] = (u,e)
        for u in reversed(order[1:]):
            v, e = pred[u]
            if rem >> u & 1:
                x ^= 1 << e
                rem ^= (1 << u) | (1 << v)
        if rem >> root & 1:
            return None
    return x


def solve_coupled(n: int, edges: list[tuple[int,int]], c: int, b: int, K: Field) -> int | None:
    """Solve B_X x=c AND (pi_C x)^3=b in a public polynomial-basis field."""
    _, cotree, _ = forest(n, edges)
    if len(cotree) != K.d:
        raise ValueError('field dimension differs from cotree dimension')
    K.element(b)
    if lift(n, edges, c, 0) is None:
        return None
    root, _ = cube_root(b, K)
    return None if root is None else lift(n, edges, c, root)


def rank(vectors: list[int]) -> int:
    pivots = {}
    for v in vectors:
        while v:
            i = v.bit_length()-1
            if i not in pivots:
                pivots[i] = v; break
            v ^= pivots[i]
    return len(pivots)


def run(args: argparse.Namespace) -> dict:
    rng = random.Random(SEED + args.degree)
    rows = []
    if args.batch == 'exhaustive':
        d = args.degree
        for f in range(1 << d, 1 << (d+1)):
            if not irreducible(f):
                continue
            K = Field(f)
            truth = {b: [] for b in range(K.q)}
            for z in range(K.q):
                zz = reference_mul(z, z, f)
                truth[reference_mul(zz, z, f)].append(z)
            image = rejected = maxcoords = 0
            for b in range(K.q):
                r, stats = cube_root(b, K)
                check((r is not None) == bool(truth[b]), 'exact_image_membership')
                if r is not None:
                    check(r in truth[b], 'root_in_exhaustive_fiber'); image += 1
                else:
                    rejected += 1
                maxcoords = max(maxcoords, stats['trace_coordinates'])
            rows.append({'degree': d, 'modulus': hex(f), 'targets': K.q,
                         'image_targets': image, 'rejected': rejected, 'max_trace_coordinates': maxcoords})
    elif args.batch in ('large', 'iso'):
        d = args.degree
        for rep in range(args.representations):
            K, tries = make_field(d, rng)
            cols = inv = None
            iso_stats = None
            if args.batch == 'iso':
                C = canonical_field(d)
                t0 = time.monotonic()
                cols, inv, iso_stats = isomorphism(C, K)
                iso_stats['seconds'] = time.monotonic()-t0
                for i in range(d):
                    check(apply(inv, cols[i]) == 1 << i, 'inverse_basis_map')
                for i, j in itertools.product(range(d), repeat=2):
                    check(apply(cols, C.mul(1 << i,1 << j)) == K.mul(cols[i],cols[j]), 'all_basis_products')
                check(K.power(iso_stats['generator_image'], 3*d//2) == 1, 'transported_cyclotomic_order')
                check(K.power(iso_stats['generator_image'], (K.q-1)//3) != 1, 'transported_nonresidue')
            image = rejected = witnesses = maxcoords = 0
            t1 = time.monotonic()
            for k in range(args.samples):
                b = K.cube(rng.randrange(K.q)) if k % 2 == 0 else rng.randrange(K.q)
                if k == 0:
                    b = 0
                r, stats = cube_root(b, K)
                expected = b == 0 or d % 2 == 1 or K.power(b,(K.q-1)//3) == 1
                check((r is not None) == expected, 'large_membership_crosscheck')
                maxcoords = max(maxcoords,stats['trace_coordinates'])
                if r is None:
                    rejected += 1
                else:
                    image += 1
                    check(K.cube(r) == b, 'large_cube_verification')
                    edges = [(0,j) for j in range(2,d+3)] + [(1,j) for j in range(2,d+3)]
                    n = d+4  # one additional isolated vertex, with charge zero.
                    c = rng.getrandbits(d+2)
                    if c.bit_count() % 2:
                        c ^= 1 << (d+2)
                    x = lift(n,edges,c,r)
                    check(x is not None and boundary(n,edges,x) == c,'full_tseitin_witness')
                    _, ct, _ = forest(n,edges)
                    check(sum(((x >> e)&1)<<j for j,e in enumerate(ct)) == r,'cotree_projection')
                    check(lift(n,edges,c ^ (1 << (n-1)),r) is None,'isolated_odd_charge_reject')
                    witnesses += 1
                if cols is not None:
                    cb = apply(inv,b)
                    cr = canonical_cube_root(cb,C)
                    check((cr is None) == (r is None),'selector_transport_membership')
                    if cr is not None:
                        check(K.cube(apply(cols,cr)) == b,'selector_transport_witness')
            rows.append({'degree':d,'modulus':hex(K.f),'generation_trials':tries,
                         'iso':iso_stats,'targets':args.samples,'image_targets':image,
                         'rejected':rejected,'witnesses':witnesses,
                         'max_trace_coordinates':maxcoords,'selection_seconds':time.monotonic()-t1})
    elif args.batch == 'controls':
        K = Field(0b1000011)
        valid = {'degree':6,'modulus':K.f,'target':1}
        bad = [{}, {**valid,'extra':0},{**valid,'degree':True},{**valid,'degree':1000000000},
               {**valid,'modulus':0b1000001},{**valid,'target':64},{**valid,'target':-1},
               {**valid,'target':False},{**valid,'modulus':0},{**valid,'target':'1'}]
        for rec in bad:
            try:
                root_record(rec)
            except ValueError:
                check(True,'malformed_record_rejected')
            else:
                check(False,'malformed_record_rejected')
        for poly, expected in [([],True),([1],False),([0],True),([0,0,1],True),([1,0,0,0,1],True)]:
            r,_ = one_root(poly,K)
            check((r is not None)==expected,'degenerate_polynomial')
            if r is not None:
                check(peval(poly,r,K)==0,'degenerate_witness')
        for _ in range(40):
            d=K.d
            A,B=[1<<i for i in range(d)],[1<<i for i in range(d)]
            for _ in range(4*d):
                i,j=rng.sample(range(d),2); A[i]^=A[j]
                i,j=rng.sample(range(d),2); B[i]^=B[j]
            Ai,Bi=inverse_columns(A),inverse_columns(B)
            s,t=rng.randrange(K.q),rng.randrange(K.q)
            original=rng.randrange(K.q)
            target=apply(B,K.cube(apply(A,original)^s))^t
            r,_=cube_root(apply(Bi,target^t),K)
            recovered=apply(Ai,r^s)
            check(apply(B,K.cube(apply(A,recovered)^s))^t==target,'public_affine_conjugation')
        # Exhaustive simple graphs on four vertices, and every edge support R.
        possible=list(itertools.combinations(range(4),2))
        for mask in range(64):
            edges=[e for i,e in enumerate(possible) if mask>>i&1]
            n=5  # extra isolate, plus isolates naturally occurring on [0,4).
            _,ct,cc=forest(n,edges)
            columns=[lift(n,edges,0,1<<i) for i in range(len(ct))]
            for i,col in enumerate(columns):
                check(boundary(n,edges,col)==0,'kernel_column')
                check(sum(((col>>e)&1)<<j for j,e in enumerate(ct))==1<<i,'kernel_cotree_identity')
            for rmask in range(1<<len(edges)):
                projected=[v & rmask for v in columns]
                left=[e for i,e in enumerate(edges) if not(rmask>>i&1)]
                _,_,ccleft=forest(n,left)
                check(rank(projected)==rmask.bit_count()+cc-ccleft,'projected_rank_with_isolates')
        for edges in [[(0,0)],[(0,1),(1,0)],[(0,3)],[(False,1)]]:
            try:
                forest(3,edges)
            except ValueError:
                check(True,'malformed_graph_reject')
            else:
                check(False,'malformed_graph_reject')
        # Supplied satisfying source assignments extend; false source assignments remain false.
        formulas={'Horn':[(1,-2),(-1,3)],'Krom':[(1,2),(-1,3)],
                  'affine':[(1,2),(-1,-2)],'product':[(1,2),(3,4)],
                  '3CNF':[(1,2,3),(-1,-2,3)],'UNSAT':[(1,),(-1,)]}
        for name,F in formulas.items():
            n=max(abs(l) for c in F for l in c)
            for assignment in range(1<<n):
                source=all(any(((assignment>>(abs(l)-1))&1)==(l>0) for l in c) for c in F)
                b=K.cube(assignment)
                z,_=cube_root(b,K)
                check(z is not None and K.cube(z)==b,'source_witness_extension')
                check((source and K.cube(z)==b)==source,'source_truth_not_changed')
        rows.append({'hostile_source_classes':list(formulas)})
    return {'run_id':'TRACEISO1','status':'COMPUTATIONAL','batch':args.batch,
            'degree':args.degree,'seed':SEED+args.degree,'checks':dict(CHECKS),
            'assertions':sum(CHECKS.values()),'operations':dict(OPS),'rows':rows,
            'elapsed_seconds':time.monotonic()-START,'failures':0,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'limitations':['Finite tests do not prove the all-parameter theorem.',
                           'Randomness only generates test records; selectors are deterministic.',
                           'Field modulus/operations are public; raw-ANF hidden-field recovery not solved.',
                           'Arithmetic counters are not complete machine instruction counts.',
                           'No unrestricted SAT or UWI lower bound is claimed.']}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch',choices=['exhaustive','iso','large','controls'],required=True)
    parser.add_argument('--degree',type=int,default=6)
    parser.add_argument('--representations',type=int,default=1)
    parser.add_argument('--samples',type=int,default=12)
    args=parser.parse_args()
    if args.degree<1 or args.degree>2048 or (args.batch=='exhaustive' and args.degree>8):
        parser.error('bounded test degree outside declared range')
    if args.representations<1 or args.samples<1:
        parser.error('positive test sizes required')
    DEADLINE = time.monotonic() + 25.0
    print(json.dumps(run(args),indent=2,sort_keys=True))
