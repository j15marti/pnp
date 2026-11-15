#!/usr/bin/env python3
"""TMR-2 AFFQUOT055: exact affine-query obstruction and fusion controls.

This models public affine constraints and paid coordinate reads of an otherwise
hidden source. It is NOT a SAT solver or native multitape Turing-machine replay.
No external dependencies. Deterministic random seed 20261114.
"""
import json
import random
from fractions import Fraction
from itertools import combinations

SEED = 20261114
rng = random.Random(SEED)
checks = 0

def check(condition):
    global checks
    assert condition
    checks += 1

def basis(rows):
    pivots = {}
    for a in rows:
        x = int(a)
        while x:
            k = x.bit_length() - 1
            if k in pivots:
                x ^= pivots[k]
            else:
                pivots[k] = x
                break
    return tuple(pivots[k] for k in sorted(pivots, reverse=True))

def contained(row, rows):
    return len(basis(tuple(rows) + (row,))) == len(basis(rows))

def sufficient(n, public, outputs, seen):
    observed = [1 << i for i in range(n) if (seen >> i) & 1]
    known = basis(tuple(public) + tuple(observed))
    return all(contained(row, known) for row in outputs)

def min_queries(n, public, outputs, seen=0):
    remaining = [i for i in range(n) if not (seen >> i) & 1]
    for k in range(len(remaining) + 1):
        for c in combinations(remaining, k):
            query = seen
            for i in c:
                query |= 1 << i
            if sufficient(n, public, outputs, query):
                return k, tuple(c)
    raise AssertionError('all source bits should suffice')

def has_separating_pair(n, public, outputs, seen):
    # Nonzero kernel z yields two valid sources x and x^z agreeing on every
    # observed coordinate but producing different output row values.
    for z in range(1, 1 << n):
        if z & seen:
            continue
        if any((z & a).bit_count() & 1 for a in public):
            continue
        if any((z & b).bit_count() & 1 for b in outputs):
            return z
    return None

def renamed(n, rows, permutation):
    def p(a):
        return sum(1 << permutation[i] for i in range(n) if (a >> i) & 1)
    return tuple(p(x) for x in rows)

def cnf_sat(n, clauses):
    return any(all(any(((x >> (abs(l)-1)) & 1) == (l > 0) for l in c)
                       for c in clauses) for x in range(1 << n))

def path_tw1_sat(n, clauses):
    """Exact separator DP for 2-CNF with only path-adjacent binary clauses."""
    for c in clauses:
        inds = [abs(l) for l in c]
        assert len(inds) <= 2 and (len(inds) < 2 or abs(inds[0]-inds[1]) <= 1)
    live = {0, 1}
    for j in range(1, n+1):
        nxt = set()
        for b in (0, 1):
            for prev in live:
                good = True
                for c in clauses:
                    if max(abs(l) for l in c) != j:
                        continue
                    vals = {j:b, j-1:prev}
                    if not any(vals[abs(l)] == (l > 0) for l in c):
                        good = False
                        break
                if good:
                    nxt.add(b)
        live = nxt
    return bool(live)

def xor3_clauses(a, b, c, rhs):
    cls = []
    for v in range(8):
        if (v.bit_count() & 1) == rhs:
            continue
        cls.append(tuple(-j if (v >> k) & 1 else j
                         for k, j in enumerate((a, b, c))))
    return tuple(cls)

def run():
    ex = {}
    B = (0b011, 0b110)
    total = min_queries(3, (), B)[0]
    separate = [min_queries(3, (), (b,))[0] for b in B]
    check((total, sum(separate)) == (3, 4))
    ex['fusion_shared'] = {'fused':total, 'separate':sum(separate)}

    H = (0b101,)
    q = min_queries(3, H, B)[0]
    check(q == 2)
    check(len(basis(H + (B[0],))) == len(basis(H + B)))
    ex['free_equality_gauss'] = {'fused':q, 'equivalent_outputs':True}
    check(min_queries(3,(0b111,),(0b111,))[0] == 0)
    ex['public_affine_solved'] = 0

    m = 6
    base = min_queries(m, (), ((1 << m)-1,))[0]
    Hext = ((1 << (m+1))-1,)
    ext = min_queries(m+1, Hext, ((1 << m)-1,))[0]
    check((base, ext) == (6, 1))
    ex['extension_interface_change'] = {
        'original_reads':base,'with_queryable_parity_bit':ext}

    check(min_queries(1, (), tuple([1] * 100))[0] == 1)
    ex['duplicate_fusion_100'] = 1
    for pad in range(1,5):
        check(min_queries(3+pad,(0b101,),B)[0] == 2)
    ex['padding_no_inflation'] = True

    for rhs in (0,1):
        clauses = xor3_clauses(1,2,3,rhs)
        check(len(clauses)==4 and
              all(len(c)==3 and len({abs(z) for z in c})==3 for c in clauses))
        for x in range(8):
            sat = all(any(((x >> (abs(l)-1)) & 1) == (l>0)
                          for l in c) for c in clauses)
            check(sat == ((x.bit_count() & 1)==rhs))
    ex['tseitin_xor_3cnf_truth_table'] = True

    horn = ((-1,2),(-2,3),(1,))
    krom = ((1,2),(-1,2),(-2,3))
    equality = ((-1,2),(1,-2))
    autarkic_pad = ((4,5,6),)
    check(cnf_sat(3,horn) and cnf_sat(3,krom) and cnf_sat(2,equality))
    check(path_tw1_sat(3,horn)==cnf_sat(3,horn))
    check(path_tw1_sat(3,krom)==cnf_sat(3,krom))
    check(path_tw1_sat(2,equality)==cnf_sat(2,equality))
    check(cnf_sat(6,horn+autarkic_pad)==cnf_sat(3,horn))
    check(cnf_sat(6,krom+autarkic_pad)==cnf_sat(3,krom))
    check(all(((x&1)==((x>>1)&1)) ==
              all(any(((x>>(abs(l)-1))&1)==(l>0)
                      for l in c) for c in equality)
              for x in range(4)))
    ex['cheap_CNF_controls'] = {
       'horn':True, 'krom_2sat':True, 'autarky':True,
       'equality_2sat':True, 'bounded_treewidth_path':True,
       'valid_for_affine_query_tariff':False}

    sampled=paid=free=separating=seen_zero=seen_one=0
    for n in range(1,7):
        for rep in range(15):
            public = tuple(rng.randrange(1 << n)
                           for _ in range(rng.randrange(5)))
            outputs = tuple(rng.randrange(1 << n)
                            for _ in range(1+rng.randrange(3)))
            seen = rng.randrange(1 << n)
            p, _ = min_queries(n,public,outputs,seen)
            check(0 <= p <= n-seen.bit_count())
            p_add = min_queries(n,
                 public+(public[0]^public[-1],) if public else public,
                 outputs+(outputs[0]^outputs[-1],),seen)[0]
            check(p_add == p)
            free += 2
            for i in range(n):
                p2,_ = min_queries(n,public,outputs,seen|(1<<i))
                delta = p-p2
                check(delta in (0,1))
                check(Fraction(1)*delta <= Fraction(1))
                paid += 1
                if delta==0:seen_zero+=1
                else:seen_one+=1
            sep=has_separating_pair(n,public,outputs,seen)
            check((sep is None)==sufficient(n,public,outputs,seen))
            if sep is not None:
                check(all(not ((sep&a).bit_count()&1) for a in public))
                check((sep&seen)==0)
                check(any((sep&b).bit_count()&1 for b in outputs))
                separating+=1
            perm=list(range(n))
            rng.shuffle(perm)
            new_public=renamed(n,public,perm)
            new_outputs=renamed(n,outputs,perm)
            new_seen=renamed(n,(seen,),perm)[0]
            check(min_queries(n,new_public,new_outputs,new_seen)[0]==p)
            sampled+=1
    ex['enumerated'] = dict(random_seed=SEED,profiles=sampled,
        paid_read_rows=paid, free_equiv_operations=free,
        separating_witnesses=separating,read_delta_zero=seen_zero,
        read_delta_one=seen_one)
    ex['symbolic_tariff'] = {
        'READ_i':{'price':1,'delta':'0 or 1'},
        'FREE_ROWSPAN':{'price':0,'delta':0},
        'FREE_FINISH':{'price':0,'delta':0},
        'BAD_INDEX':{'price':1,'delta':0},'lambda_p':'1'}
    ex['status']='PROVED/RESTRICTED symbolic; native finite test COMPUTATIONAL; unrestricted SAT transfer OPEN'
    ex['checks']=checks
    return ex

if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
