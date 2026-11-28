#!/usr/bin/env python3
"""
Grok 4.7 work, 2026-11-28 ~11 KST.  Checks for the T3-07 NEXT target
MIN-COST-RESPONSE-OR-EXACT-REFUTATION (replace a bounded-boundary bucket by its
exact min-cost factor).

(A) T3-07 pivot-cost lemma, exhaustive on random buckets: for every boundary word y,
    local min_v violations == min(P(y),Q(y)) and #falsified (v,-v) clause pairs == P*Q;
    BVE soundness: if every non-tautological resolvent is true then min(P,Q)==0.
(B) Exact min-sum bucket elimination (tables, no width cap) returns exactly the
    brute-force minimum number of violated clauses, and the reverse map rebuilds an
    optimal assignment (random 3-CNF, n<=14).
(C) w-bounded elimination on random 3-CNF primal graphs (density 4.6 = 184/40, the
    RANDOM companion ratio): repeatedly eliminate a vertex whose current neighbourhood
    has size <= w (min-degree first, with fill = torso).  Report residual size / n.
    Theorem in the log: ANY order leaves |residual| >= tw(G)+1 whenever tw(G) > w.
    Also reports networkx min-fill-in treewidth UPPER bound for scale only.
Seeds fixed; output JSON.
"""
import itertools, json, random, sys, time
import networkx as nx
from networkx.algorithms.approximation import treewidth_min_fill_in

def rand3cnf(n, m, rng):
    return [tuple(v if rng.random() < 0.5 else -v for v in rng.sample(range(1, n + 1), 3)) for _ in range(m)]

def lit_true(l, a):  # a: dict var->bool
    return a[abs(l)] == (l > 0)

def part_A(rng, trials=400):
    checks = 0
    for _ in range(trials):
        k = rng.randint(1, 6); bvars = list(range(2, k + 2)); v = 1
        A = []; B = []
        for _ in range(rng.randint(1, 4)):
            r = rng.sample(bvars, min(len(bvars), rng.randint(0, 3)))
            A.append((v,) + tuple(x if rng.random() < .5 else -x for x in r))
        for _ in range(rng.randint(1, 4)):
            r = rng.sample(bvars, min(len(bvars), rng.randint(0, 3)))
            B.append((-v,) + tuple(x if rng.random() < .5 else -x for x in r))
        for bits in itertools.product([False, True], repeat=k):
            a = dict(zip(bvars, bits))
            P = sum(all(not lit_true(l, a) for l in c[1:]) for c in A)
            Q = sum(all(not lit_true(l, a) for l in c[1:]) for c in B)
            m0 = sum(not any(lit_true(l, {**a, v: False}) for l in c) for c in A + B)
            m1 = sum(not any(lit_true(l, {**a, v: True}) for l in c) for c in A + B)
            assert min(m0, m1) == min(P, Q)
            pairs = 0; resolvents_ok = True
            for ca in A:
                for cb in B:
                    rest = set(ca[1:]) | set(cb[1:])
                    taut = any(-l in rest for l in rest)
                    bothfalse = all(not lit_true(l, a) for l in ca[1:]) and all(not lit_true(l, a) for l in cb[1:])
                    if bothfalse:
                        assert not taut
                        pairs += 1
                    if not taut and not any(lit_true(l, a) for l in rest):
                        resolvents_ok = False
            assert pairs == P * Q
            if resolvents_ok:
                assert min(P, Q) == 0
            checks += 1
    return {'bucket_trials': trials, 'boundary_words_checked': checks, 'all_pass': True}

def minsum_eliminate(n, F, order):
    """Exact min-sum bucket elimination over clause-violation costs.
    factors: list of (scope tuple, dict assignment-tuple -> cost)."""
    factors = []
    for c in F:
        sc = tuple(sorted({abs(l) for l in c}))
        tab = {}
        for bits in itertools.product([0, 1], repeat=len(sc)):
            a = dict(zip(sc, bits))
            tab[bits] = 0 if any(a[abs(l)] == (l > 0) for l in c) else 1
        factors.append((sc, tab))
    trace = []; maxb = 0
    for v in order:
        bucket = [f for f in factors if v in f[0]]
        factors = [f for f in factors if v not in f[0]]
        bd = tuple(sorted({u for sc, _ in bucket for u in sc} - {v}))
        maxb = max(maxb, len(bd))
        tab = {}; arg = {}
        for bits in itertools.product([0, 1], repeat=len(bd)):
            a = dict(zip(bd, bits)); best = None
            for x in (0, 1):
                a[v] = x
                s = sum(t[tuple(a[u] for u in sc)] for sc, t in bucket)
                if best is None or s < best:
                    best, bx = s, x
            tab[bits] = best; arg[bits] = bx
        factors.append((bd, tab)); trace.append((v, bd, arg))
    const = sum(t[()] for sc, t in factors)
    a = {}
    for v, bd, arg in reversed(trace):
        a[v] = arg[tuple(a[u] for u in bd)]
    viol = sum(not any(a[abs(l)] == (l > 0) for l in c) for c in F)
    return const, viol, maxb

def part_B(rng, inst=40):
    rec = []
    for t in range(inst):
        n = rng.randint(6, 14); F = rand3cnf(n, int(round(4.6 * n)), rng)
        best = min(sum(not any(((x >> (abs(l) - 1)) & 1) == (l > 0) for l in c) for c in F) for x in range(1 << n))
        order = list(range(1, n + 1)); rng.shuffle(order)
        const, viol, maxb = minsum_eliminate(n, F, order)
        assert const == best == viol, (const, best, viol)
        rec.append({'n': n, 'm': len(F), 'min_violated': best, 'max_boundary': maxb})
    return {'instances': inst, 'all_exact': True, 'examples': rec[:8]}

def primal(n, F):
    G = nx.Graph(); G.add_nodes_from(range(1, n + 1))
    for c in F:
        vs = [abs(l) for l in c]
        for a, b in itertools.combinations(vs, 2):
            if a != b: G.add_edge(a, b)
    return G

def bounded_eliminate(G, w):
    H = G.copy(); elim = 0
    while True:
        cand = [(H.degree(u), u) for u in H.nodes if H.degree(u) <= w]
        if not cand:
            break
        _, u = min(cand)
        nb = list(H.neighbors(u))
        for a, b in itertools.combinations(nb, 2):
            H.add_edge(a, b)
        H.remove_node(u); elim += 1
    if H.number_of_nodes():
        assert min(d for _, d in H.degree()) > w
    return H.number_of_nodes(), elim

def part_C(rng):
    rows = []
    for n in (40, 80, 160, 320):
        for s in range(5):
            F = rand3cnf(n, int(round(4.6 * n)), random.Random(10_000 * n + s))
            G = primal(n, F)
            tw_ub, _ = treewidth_min_fill_in(G)
            row = {'n': n, 'm': len(F), 'seed': 10_000 * n + s, 'tw_upper_minfill': tw_ub}
            for w in (3, 4, 6, 8, 10, 12, 16):
                r, e = bounded_eliminate(G, w)
                row['residual_w%d' % w] = r
            rows.append(row); print(json.dumps(row), flush=True)
    return rows

def main():
    t0 = time.time(); rng = random.Random(2026112811)
    out = {'seed': 2026112811}
    out['A_pivot_lemma'] = part_A(rng); print(json.dumps(out['A_pivot_lemma']), flush=True)
    out['B_minsum_exact'] = part_B(rng); print(json.dumps(out['B_minsum_exact']['instances']), flush=True)
    out['C_bounded_elimination'] = part_C(rng)
    out['seconds'] = round(time.time() - t0, 1)
    json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else 'out.json', 'w'), indent=1)

if __name__ == '__main__':
    main()
