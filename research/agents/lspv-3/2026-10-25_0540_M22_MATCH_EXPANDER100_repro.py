#!/usr/bin/env python3
"""M22-MATCH-EXPANDER100: deterministic source-aware matching and frontier audit.
Standard Python 3 only. Synthetic graphs are finite controls, NOT an
asymptotic expander construction and NOT FLMV bit-TM measurements.
"""
import itertools
import json
import math
import random
import hashlib
from collections import Counter

SEED = 202610241327


def regular_bipartite(h):
    """Two cycle matchings plus a third rotation, simple connected cubic."""
    assert h >= 4
    shifts = (0, 1, h // 2)
    edges = []
    for shift in shifts:
        for i in range(h):
            edges.append((i, h + (i + shift) % h))
    assert len(set(edges)) == 3 * h
    return 2 * h, edges


def make_formula(v, edges):
    incidence = [[] for _ in range(v)]
    for number, (u, w) in enumerate(edges, 1):
        incidence[u].append(number)
        incidence[w].append(number)
    assert all(len(x) == 3 and len(set(x)) == 3 for x in incidence)
    u, w = edges[0]
    e = 1
    a = next(x for x in incidence[u] if x != e)
    b = next(x for x in incidence[w] if x != e)
    pos = [tuple(sorted(c)) for c in incidence]
    neg = [list(c) for c in incidence]
    neg[u].remove(a)
    neg[w].remove(b)
    neg[u].append(b)
    neg[w].append(a)
    neg = [tuple(sorted(c)) for c in neg]
    formula = [tuple(c) for c in pos] + [tuple(-x for x in c) for c in neg]
    return formula, pos, neg, (e, a, b), incidence


def grammar(formula):
    cseen = set()
    plus, minus = Counter(), Counter()
    for clause in formula:
        if len(clause) != 3 or len(set(abs(x) for x in clause)) != 3:
            return False
        if not (all(z > 0 for z in clause) or all(z < 0 for z in clause)):
            return False
        if clause in cseen:
            return False
        cseen.add(clause)
        for z in clause:
            (plus if z > 0 else minus)[abs(z)] += 1
    return all(plus[x] == minus[x] == 2 for x in (plus.keys() | minus.keys()))


def defect(formula):
    p = {tuple(sorted(abs(z) for z in c)) for c in formula if c[0] > 0}
    n = {tuple(sorted(abs(z) for z in c)) for c in formula if c[0] < 0}
    return len(p - n), len(p & n)


def satisfied(formula, bits):
    return all(any(bool((bits >> (abs(z)-1)) & 1) == (z > 0) for z in c)
               for c in formula)


def bit_length(k, m):
    return (4 * m + 2) * math.ceil(math.log2(64 * (k + m + 1)))


def bisection(v, edges):
    """Exact finite edge bisection, v<=16 only; fix vertex 0 to avoid duplicates."""
    assert v <= 16 and v % 2 == 0
    best = len(edges)
    for other in itertools.combinations(range(1, v), v//2 - 1):
        left = set(other) | {0}
        value = sum((u in left) != (w in left) for u, w in edges)
        best = min(best, value)
    return best


def pin_gadget(x, value, next_var):
    """Four proper ternary clauses enforce x=value with two new variables."""
    assert value in (0, 1)
    lit = x if value else -x
    u, v = next_var + 1, next_var + 2
    return [(lit, s*u, t*v) for s in (1, -1) for t in (1, -1)]


def check_gadget():
    for val in (0, 1):
        for x in (0, 1):
            has_completion = False
            for u in (0, 1):
                for v in (0, 1):
                    bits = x | (u << 1) | (v << 2)
                    has_completion |= satisfied(pin_gadget(1, val, 1), bits)
            assert has_completion == (x == val)


def test():
    assert grammar(Y)
    assert defect(Y) == (4, 0)
    assert sum(satisfied(Y, x) for x in range(64)) == 20
    paired = [c for c in Y if c[0] > 0]
    paired += [tuple(-z for z in c) for c in paired]
    assert grammar(paired) and defect(paired) == (0, 4)
    assert sum(satisfied(paired, x) for x in range(64)) == 18
    assert not grammar(Y + [Y[0]])
    check_gadget()
    data = []
    rng = random.Random(SEED)
    for h in (4, 6, 8, 10, 12, 16):
        v, edges = regular_bipartite(h)
        F, pos, neg, (e, a, b), incid = make_formula(v, edges)
        k, m = len(edges), len(F)
        assert grammar(F) and defect(F) == (2, v - 2)
        assert len(set(pos)) == len(set(neg)) == v
        assert (3*m == 4*k and m == 2*v)
        # The first rotation (first h edges) is a displayed perfect matching.
        match = set(range(1, h+1))
        assert len(match) == h
        assert all(sum(x in match for x in c) == 1 for c in pos)
        bits = sum(1 << (x-1) for x in match)
        assert satisfied(F, bits)
        # Every negative clause contains two positive-graph edges sharing a vertex.
        endp = {j+1: set(edge) for j, edge in enumerate(edges)}
        indep = 0
        for clause in neg:
            independent = all(endp[x].isdisjoint(endp[y]) for x,y in itertools.combinations(clause,2))
            indep += int(independent)
        assert indep == 0
        # Disjoint erroneous source aliasing is not part of this grammar.
        nsrc = bit_length(k, m)
        n1 = bit_length(k + 2, m + 4)
        n2 = bit_length(k + 4, m + 8)
        assert nsrc < n1 < n2
        # Pin gadget is proper ordinary 3CNF and leaves C_star syntax.
        child = F + pin_gadget(e, 0, k)
        assert all(len(set(abs(z) for z in c)) == 3 for c in child)
        assert not grammar(child)
        # A bisection in the positive clauses remains a frontier regardless
        # of the order in which the interspersed negative clauses are scanned.
        bw = bisection(v, edges) if v <= 16 else None
        least = 10**9
        for t in range(20):
            order = list(range(2*v)); rng.shuffle(order)
            processed = []
            cutoff = None
            for p, j in enumerate(order):
                if j < v:
                    processed.append(j)
                    if len(processed) == v//2:
                        cutoff = p
                        break
            assert cutoff is not None
            prefix = set(processed)
            frontier = sum((u in prefix) != (w in prefix) for u,w in edges)
            least = min(least, frontier)
            assert bw is None or frontier >= bw
        modelcount = None
        twolevel = None
        if k <= 18:
            modelcount = 0
            twolevel = [0,0,0,0]
            for trial in range(1 << k):
                if satisfied(F, trial):
                    modelcount += 1
                    i = (((trial>>(e-1))&1)<<1) | ((trial>>(a-1))&1)
                    twolevel[i] += 1
            assert sum(twolevel) == modelcount and modelcount > 0
        data.append(dict(v=v,k=k,m=m,q=2,paired=v-2,bisection=bw,
                         min_sampled_frontier=least,encoded_bits=nsrc,
                         pin_one_bits=n1,pin_two_bits=n2,
                         certified_matching_size=h,model_count=modelcount,
                         two_level_branch_model_counts=twolevel,
                         independent_negative_clauses=indep))
    return {'seed':SEED,'status':'COMPUTATIONAL','tested_graphs':len(data),
            'shuffled_orders_per_graph':20,'graph_tests':data,
            'Y_models':20,'paired_Y_models':18,'failed_assertions':0,
            'limitations':'finite rotations are NOT asymptotic expanders; word counts are NOT FLMV bit-TM traces; U UNSAT is imported from Doecker, not brute solved'}

Y = [(1,2,3),(1,4,5),(2,4,6),(3,5,6),
     (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]

if __name__ == '__main__':
    result = test()
    raw = json.dumps(result, indent=2, sort_keys=True) + '\n'
    open('M22_MATCH_EXPANDER100_raw.json','w',encoding='utf-8').write(raw)
    print(raw)
    print('JSON_SHA256', hashlib.sha256(raw.encode()).hexdigest())
