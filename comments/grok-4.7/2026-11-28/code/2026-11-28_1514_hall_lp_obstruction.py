#!/usr/bin/env python3
"""Grok 4.7, 2026-11-28 (KST). Hall-certificate obstruction checks.

A Hall certificate (T1 multi-demand Hall, bbd8aa65): pairwise literal-disjoint demand clauses S,
a partition of their literals into bins that are cliques of the exclusion graph
(complementary pairs + explicit binary clauses (-a v -b)), with #bins touched < |S|.

This script
 (1) builds Tseitin 3-CNF on the T3 toroidal cubic family (k x k cells, 4-cycle per cell),
     plus girth-3 cubic controls (K4, prism, triangle-replaced torus) and functional PHP(n+1,n);
 (2) for random guards rho, computes UP closure, the exclusion graph, triangle test,
     the half-integral LP point, an exact Hall search by 0/1 ILP (scipy.optimize.milp / HiGHS),
     and optionally width-2 RUP saturation followed by the same tests;
 (3) prints a JSON summary.
Deterministic seeds. No claim beyond the stated finite instances.
"""
import itertools, json, random, sys
import numpy as np
import networkx as nx
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix

# ---------------- formulas ----------------
def torus_graph(k):
    """T3 construction: each cell of the k x k torus -> 4-cycle with ports N,E,S,W;
    E port of (i,j) joined to W port of (i,j+1); S port of (i,j) to N port of (i+1,j)."""
    G = nx.Graph()
    v = lambda i, j, p: (i % k, j % k, p)
    for i in range(k):
        for j in range(k):
            for a, b in [('N', 'E'), ('E', 'S'), ('S', 'W'), ('W', 'N')]:
                G.add_edge(v(i, j, a), v(i, j, b))
            G.add_edge(v(i, j, 'E'), v(i, j + 1, 'W'))
            G.add_edge(v(i, j, 'S'), v(i + 1, j, 'N'))
    return G

def triangle_replaced_torus(k):
    """girth-3 control: replace every vertex of the k x k torus 4-regular grid? no -- use
    truncation of the cubic torus graph: every vertex -> triangle (still cubic, simple)."""
    H = torus_graph(k)
    G = nx.Graph()
    for u in H.nodes():
        nb = sorted(H.neighbors(u))
        for a, b in itertools.combinations(nb, 2):
            G.add_edge((u, a), (u, b))
    for u, w in H.edges():
        G.add_edge((u, w), (w, u))
    return G

def tseitin_cnf(G, charge):
    """edge variables 1..|E|; for each vertex all clauses forbidding wrong-parity assignments."""
    edges = sorted(G.edges(), key=str)
    eid = {}
    for t, (a, b) in enumerate(edges):
        eid[frozenset((a, b))] = t + 1
    clauses = []
    for v in G.nodes():
        inc = [eid[frozenset((v, w))] for w in G.neighbors(v)]
        for bits in itertools.product([0, 1], repeat=len(inc)):
            if sum(bits) % 2 != charge.get(v, 0):
                # forbid this assignment: clause is OR of literals false at it
                clauses.append(tuple(sorted((x if b == 0 else -x) for x, b in zip(inc, bits))))
    return len(edges), sorted(set(clauses))

def php_functional(n):
    """PHP(n+1,n) with pigeon clauses, hole exclusions and functional exclusions."""
    var = lambda i, j: i * n + j + 1
    C = []
    for i in range(n + 1):
        C.append(tuple(var(i, j) for j in range(n)))
        for j, jj in itertools.combinations(range(n), 2):
            C.append((-var(i, j), -var(i, jj)))
    for j in range(n):
        for i, ii in itertools.combinations(range(n + 1), 2):
            C.append((-var(i, j), -var(ii, j)))
    return (n + 1) * n, sorted(set(tuple(sorted(c)) for c in C))

# ---------------- propagation ----------------
def restrict(clauses, assign):
    out = []
    for c in clauses:
        if any(assign.get(abs(l)) == (l > 0) for l in c):
            continue
        r = tuple(l for l in c if abs(l) not in assign)
        out.append(r)
    return out

def unit_propagate(clauses, assign):
    """returns (assign', conflict, visits). simple full-scan UP (counted literal visits)."""
    assign = dict(assign); visits = 0
    while True:
        changed = False
        for c in clauses:
            free = []; sat = False
            for l in c:
                visits += 1
                a = assign.get(abs(l))
                if a is None: free.append(l)
                elif a == (l > 0): sat = True; break
            if sat: continue
            if not free: return assign, True, visits
            if len(free) == 1:
                assign[abs(free[0])] = free[0] > 0; changed = True
        if not changed: return assign, False, visits

def width2_rup_saturate(clauses, nvars, cap=10**8):
    """deterministic width<=2 RUP saturation (units then pairs, lex), repeat until no admission.
    Returns (clauses', conflict, admitted, visits)."""
    cur = list(clauses); have = set(cur); admitted = 0; visits = 0
    vs = sorted({abs(l) for c in cur for l in c})
    while True:
        new = False
        cands = [(l,) for v in vs for l in (v, -v)]
        cands += [tuple(sorted(p)) for a, b in itertools.combinations(vs, 2)
                  for p in [(a, b), (a, -b), (-a, b), (-a, -b)]]
        for cand in cands:
            if cand in have: continue
            if len(cand) == 2 and ((cand[0],) in have or (cand[1],) in have): continue
            a0 = {abs(l): (l < 0) for l in cand}
            _, conf, vis = unit_propagate(cur, a0); visits += vis
            if conf:
                cur.append(cand); have.add(cand); admitted += 1; new = True
                if () in have: return cur, True, admitted, visits
                # empty test
                _, c2, vis2 = unit_propagate(cur, {}); visits += vis2
                if c2: return cur + [()], True, admitted, visits
            if visits > cap: return cur, None, admitted, visits
        if not new: return cur, False, admitted, visits

# ---------------- Hall tests ----------------
def exclusion_graph(clauses):
    X = nx.Graph()
    lits = {l for c in clauses for l in c}
    for l in lits:
        X.add_node(l)
        if -l in lits: X.add_edge(l, -l)
    for c in clauses:
        if len(c) == 2:
            X.add_edge(-c[0], -c[1])  # (a v b) excludes {-a,-b}
            for l in (-c[0], -c[1]): X.add_node(l)
    return X

def has_triangle(X):
    return any(t > 0 for t in nx.triangles(X).values())

def half_point_feasible(clauses, X):
    """y = 1/2 on all free literals: demands need >=2 literals, cliques size <= 2."""
    if any(len(c) < 2 for c in clauses): return False
    return not has_triangle(X)

def exact_hall(clauses, X, time_limit=60):
    """0/1 ILP: max sum s_C - sum z_K s.t. literal-disjoint demands, every used literal covered
    by a chosen maximal clique. Hall certificate exists iff optimum >= 1."""
    C = [c for c in clauses if len(c) >= 1]
    K = [tuple(sorted(q)) for q in nx.find_cliques(X)] if X.number_of_nodes() else []
    lits = sorted({l for c in C for l in c})
    if not C: return False, 0, None
    nC, nK = len(C), len(K)
    rows = []; lb = []; ub = []
    idx_c = {l: [i for i, c in enumerate(C) if l in c] for l in lits}
    idx_k = {l: [nC + j for j, q in enumerate(K) if l in q] for l in lits}
    A = lil_matrix((len(lits) + sum(len(c) for c in C), nC + nK))
    r = 0
    for l in lits:  # disjointness
        for i in idx_c[l]: A[r, i] = 1
        lb.append(-np.inf); ub.append(1); r += 1
    for i, c in enumerate(C):  # coverage: sum_{K ni l} z_K - s_C >= 0
        for l in c:
            for j in idx_k[l]: A[r, j] = 1
            A[r, i] = -1
            lb.append(0); ub.append(np.inf); r += 1
    obj = np.concatenate([-np.ones(nC), np.ones(nK)])  # minimize -(sum s - sum z)
    res = milp(obj, constraints=LinearConstraint(A.tocsr(), lb, ub),
               integrality=np.ones(nC + nK), bounds=Bounds(0, 1),
               options={'time_limit': time_limit})
    if res.status not in (0,):
        return None, None, res.message
    val = -res.fun
    cert = None
    if val > 0.5:
        S = [C[i] for i in range(nC) if res.x[i] > 0.5]
        Z = [K[j] for j in range(nK) if res.x[nC + j] > 0.5]
        cert = {'demands': S, 'bins': Z}
    return val > 0.5, round(val), cert

def verify_hall(cert, clauses, X):
    S, Z = cert['demands'], cert['bins']
    cs = set(clauses)
    assert all(tuple(sorted(d)) in cs for d in S)
    used = [l for d in S for l in d]
    assert len(used) == len(set(used))
    for q in Z:
        for a, b in itertools.combinations(q, 2): assert X.has_edge(a, b)
    touched = [q for q in Z if any(l in q for l in used)]
    assert all(any(l in q for q in Z) for l in used)
    assert len(touched) < len(S)
    return True

# ---------------- experiment ----------------
def run_family(name, nvars, clauses, n_guards, sizes, seed, do_rup=True, do_exact=True):
    rng = random.Random(seed)
    stats = dict(name=name, nvars=nvars, nclauses=len(clauses), trials=0, up_conflict=0,
                 up_open=0, up_open_triangle=0, up_open_halfpoint=0, up_open_exact_hall=0,
                 exact_skipped=0, rup_runs=0, rup_conflict=0, rup_open=0, rup_open_triangle=0,
                 rup_open_halfpoint=0, rup_open_exact_hall=0, rup_admitted_total=0,
                 visits_up=0, visits_rup=0, examples=[])
    X0 = exclusion_graph(clauses)
    stats['root_triangle'] = has_triangle(X0)
    stats['root_halfpoint'] = half_point_feasible(clauses, X0)
    h, val, cert = exact_hall(clauses, X0)
    stats['root_exact_hall'] = h
    if cert:
        verify_hall(cert, clauses, X0)
        stats['root_cert'] = {'demands': len(cert['demands']), 'bins': len(cert['bins'])}
    for t in sizes:
        for _ in range(n_guards):
            stats['trials'] += 1
            vs = rng.sample(range(1, nvars + 1), t)
            rho = {v: rng.random() < 0.5 for v in vs}
            a, conf, vis = unit_propagate(clauses, rho); stats['visits_up'] += vis
            if conf: stats['up_conflict'] += 1; continue
            stats['up_open'] += 1
            R = restrict(clauses, a)
            X = exclusion_graph(R)
            tri = has_triangle(X); hp = half_point_feasible(R, X)
            stats['up_open_triangle'] += tri; stats['up_open_halfpoint'] += hp
            if do_exact:
                h, val, cert = exact_hall(R, X)
                if h is None: stats['exact_skipped'] += 1
                elif h:
                    stats['up_open_exact_hall'] += 1; verify_hall(cert, R, X)
                    if len(stats['examples']) < 2:
                        stats['examples'].append({'guard_size': t, 'stage': 'UP',
                            'demands': cert['demands'], 'bins': cert['bins']})
            if do_rup:
                stats['rup_runs'] += 1
                R2, c2, adm, v2 = width2_rup_saturate(R, nvars)
                stats['visits_rup'] += v2; stats['rup_admitted_total'] += adm
                if c2: stats['rup_conflict'] += 1; continue
                if c2 is None: continue
                stats['rup_open'] += 1
                X2 = exclusion_graph(R2)
                stats['rup_open_triangle'] += has_triangle(X2)
                stats['rup_open_halfpoint'] += half_point_feasible(R2, X2)
                if do_exact:
                    h2, _, cert2 = exact_hall(R2, X2)
                    if h2:
                        stats['rup_open_exact_hall'] += 1; verify_hall(cert2, R2, X2)
                        if len(stats['examples']) < 4:
                            stats['examples'].append({'guard_size': t, 'stage': 'W2RUP',
                                'demands': cert2['demands'], 'bins': cert2['bins']})
    return stats

def main():
    out = []
    # torus family, both labels
    for k, ng, sizes, rup in [(3, 40, [0, 2, 4, 6, 8, 10, 12, 16, 20], True),
                              (4, 25, [0, 4, 8, 12, 16, 24, 32], True),
                              (5, 12, [0, 6, 12, 20, 30, 40], False)]:
        G = torus_graph(k)
        assert all(d == 3 for _, d in G.degree()) and nx.girth(G) == 4
        for label, ch in [('NO', {sorted(G.nodes())[0]: 1}), ('YES', {})]:
            n, C = tseitin_cnf(G, ch)
            out.append(run_family(f'torus-k{k}-{label}', n, C, ng, sizes, 1000 + k, do_rup=rup))
            print(json.dumps({x: out[-1][x] for x in out[-1] if x != 'examples'}), flush=True)
    # girth-3 controls
    for name, G in [('K4', nx.complete_graph(4)),
                    ('prism', nx.circular_ladder_graph(3)),
                    ('truncated-torus-k3', triangle_replaced_torus(3))]:
        assert all(d == 3 for _, d in G.degree()) and nx.girth(G) == 3
        n, C = tseitin_cnf(G, {sorted(G.nodes(), key=str)[0]: 1})
        sizes = [0, 1, 2, 3] if n <= 9 else [0, 4, 8, 12, 16, 24, 32]
        out.append(run_family(f'{name}-NO', n, C, 30, sizes, 77, do_rup=(n <= 60)))
        print(json.dumps({x: out[-1][x] for x in out[-1] if x != 'examples'}), flush=True)
    # positive control: functional PHP
    for m in [3, 4, 5]:
        n, C = php_functional(m)
        out.append(run_family(f'PHP({m+1},{m})-functional', n, C, 5, [0, 2], 5, do_rup=(m <= 4)))
        print(json.dumps({x: out[-1][x] for x in out[-1] if x != 'examples'}), flush=True)
    json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else 'hall_lp_obstruction.out.json', 'w'),
              indent=1, default=str)

if __name__ == '__main__':
    main()
