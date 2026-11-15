#!/usr/bin/env python3
"""TMR-5/048 exact bilinear rank and counting red-team, standard Python 3.
All instances exhaustive for k<=3; seeded k=4 cases; one identity k=5.
No external dependencies, no floating-point ranks or probabilistic claims.
"""
import itertools
import json
import random
from collections import defaultdict

SEED = 202611151248
MOD = 65521
REVISION = 'tmr5-bilinear048-v1'
checks = 0


def check(condition, label):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(label)


def rank_mod(rows, p):
    if not rows:
        return 0
    a = [[v % p for v in row] for row in rows]
    n, m = len(a), len(a[0]); h = 0
    for j in range(m):
        pivot = next((i for i in range(h, n) if a[i][j]), None)
        if pivot is None:
            continue
        a[h], a[pivot] = a[pivot], a[h]
        inv = pow(a[h][j], -1, p)
        for col in range(j, m):
            a[h][col] = (a[h][col] * inv) % p
        for i in range(h + 1, n):
            coef = a[i][j]
            if coef:
                for col in range(j, m):
                    a[i][col] = (a[i][col] - coef * a[h][col]) % p
        h += 1
        if h == n:
            break
    return h


def rank_b_matrix(b, k):
    return rank_mod([[int((row >> j) & 1) for j in range(k)] for row in b], 2)


def eval_b(b, x, y):
    z = 0
    for i, row in enumerate(b):
        if x >> i & 1:
            z ^= (row & y).bit_count() & 1
    return z


def matrix_b(b, k):
    return [[eval_b(b, x, y) for y in range(1 << k)] for x in range(1 << k)]


def matrix_disj(k):
    return [[int((x & y) == 0) for y in range(1 << k)] for x in range(1 << k)]


def matrix_singleton(k):
    return [[int(x == 1 and y == (1 << k) - 1) for y in range(1 << k)] for x in range(1 << k)]


def ip_interleave_frontiers(k):
    order = [(side, i) for i in range(k) for side in (0, 1)]
    counts = []
    for p in range(2*k + 1):
        residuals = set()
        for ap in range(1 << p):
            truth = 0
            for bs in range(1 << (2*k - p)):
                x = y = 0
                for pos, (side, i) in enumerate(order):
                    bit = ((ap >> pos) & 1) if pos < p else ((bs >> (pos-p)) & 1)
                    if side == 0:
                        x |= bit << i
                    else:
                        y |= bit << i
                if ((x & y).bit_count() & 1):
                    truth |= 1 << bs
            residuals.add(truth)
        counts.append(len(residuals))
    return counts


def rows_for(mask, k):
    return tuple((mask >> j) & 1 for j in range(k))


summary = defaultdict(lambda: defaultdict(int))
examples = []
for k in range(1, 6):
    if k <= 3:
        choices = range(1 << (k*k))
    elif k == 4:
        rng = random.Random(SEED)
        samples = {0, (1 << 16) - 1, sum(1 << (i*4+i) for i in range(4))}
        samples.update(rng.getrandbits(16) for _ in range(128))
        choices = sorted(samples)
    else:
        choices = [sum(1 << (i*5+i) for i in range(5))]
    for enc in choices:
        b = tuple((enc >> (i*k)) & ((1 << k)-1) for i in range(k))
        r = rank_b_matrix(b, k)
        m = matrix_b(b, k)
        f2 = rank_mod(m, 2)
        odd = rank_mod(m, MOD)
        count = sum(map(sum, m))
        rowcount = len({tuple(row) for row in m})
        target = (2**r-1) * 2**(2*k-r-1)
        check(f2 == r, ('GF2', k, enc, f2, r))
        check(odd == (2**r-1), ('odd', k, enc, odd, r))
        check(rowcount == 2**r, ('rows', k, enc, rowcount, r))
        check(count == target, ('count', k, enc, count, target))
        check(bool(count) == bool(r), ('SAT', k, enc, count, r))
        summary[k][r] += 1
        if len(examples) < 18 and (enc == 0 or enc == sum(1 << (i*k+i) for i in range(k))):
            examples.append(dict(k=k, B_rows=list(b),rank_B=r,rank_GF2=f2,rank_F65521=odd,distinct_rows=rowcount,count=count))

controls = {}
for k in range(1, 6):
    disj = matrix_disj(k)
    unique = matrix_singleton(k)
    controls[k] = {'DISJ_rank_GF2': rank_mod(disj,2), 'DISJ_rank_odd': rank_mod(disj,MOD),
                   'singleton_rank_GF2': rank_mod(unique,2),
                   'singleton_rank_odd': rank_mod(unique,MOD)}
    check(controls[k]['DISJ_rank_GF2'] == 2**k, ('DISJ2', k))
    check(controls[k]['DISJ_rank_odd'] == 2**k, ('DISJodd', k))
    check(controls[k]['singleton_rank_GF2'] == 1, ('SINGLE2', k))
    check(controls[k]['singleton_rank_odd'] == 1, ('SINGLEodd', k))

frontiers = {k: ip_interleave_frontiers(k) for k in range(1, 5)}
for k, v in frontiers.items():
    check(max(v) <= 4, ('interleave',k,v))
    check(v[k*2] == 2, ('terminal',k,v))

# Independent TMR-4/052 switch-product reproduction on every six-variable
# order and every nontrivial original-variable cut, both GF(2) and odd prime.
def scalar_function(which, mask):
    k = 3
    x = mask & 7
    y = (mask >> k) & 7
    return int((x & y) == 0) if which == 'DISJ3' else ((x & y).bit_count() & 1)


def matrix_for_partition(which, p_mask):
    xs = [i for i in range(6) if p_mask >> i & 1]
    ys = [i for i in range(6) if not (p_mask >> i & 1)]
    mat = []
    for xbits in range(1 << len(xs)):
        row = []
        for ybits in range(1 << len(ys)):
            m = sum(((xbits >> j) & 1) << i for j,i in enumerate(xs))
            m |= sum(((ybits >> j) & 1) << i for j,i in enumerate(ys))
            row.append(scalar_function(which, m))
        mat.append(row)
    return mat


rank_cache = {}
for which in ('DISJ3', 'IP3'):
    for p_mask in range(1, 63):
        mat = matrix_for_partition(which, p_mask)
        rank_cache[(which, p_mask)] = (rank_mod(mat, 2), rank_mod(mat, MOD))

multicut_checks = 0
multicut_tight = defaultdict(int)
for order in itertools.permutations(range(6)):
    # x_i, y_i interleavings and grouped orders are explicitly included.
    lookup = []
    for posbits in range(64):
        lookup.append(sum(((posbits >> pos) & 1) << orig for pos,orig in enumerate(order)))
    q_by_function = {}
    for which in ('DISJ3', 'IP3'):
        v = [scalar_function(which, lookup[posbits]) for posbits in range(64)]
        q = [1]
        for p in range(1, 6):
            cofactors = {tuple(v[a | (b << p)] for b in range(1 << (6-p)))
                         for a in range(1 << p)}
            q.append(len(cofactors))
        q_by_function[which] = q
    for part in range(1, 63):
        switches = [i for i in range(1, 6)
                    if bool(part & (1 << order[i-1])) != bool(part & (1 << order[i]))]
        check(bool(switches), ('switch_exists', order, part))
        for which in ('DISJ3', 'IP3'):
            product = 1
            for i in switches:
                product *= q_by_function[which][i]
            r2, rp = rank_cache[(which, part)]
            check(r2 <= product and rp <= product,
                  ('switch_product', order, part, which, product, r2, rp))
            multicut_checks += 1
            if rp == product:
                multicut_tight[which] += 1

result = {'version':REVISION,'seed':SEED,'prime':MOD,
          'scope':'exhaustive B all k<=3; deterministic seeded sample k=4; identity k=5',
          'counts_by_k_rank':{str(k):dict(sorted(v.items())) for k,v in summary.items()},
          'examples':examples,'controls':controls,'IP_interleaved_residual_counts':frontiers,
          'multicut_comparisons':multicut_checks, 'multicut_tight_odd':dict(multicut_tight),
          'assertions':checks,'failures':0,
          'theorem':'rank_GF2=r; rank_odd=2^r-1; rows=2^r; #SAT=(2^r-1)*2^(2k-r-1)'}
print(json.dumps(result, indent=2, sort_keys=True))
