#!/usr/bin/env python3
"""TMR-5/055: exact finite checks of the z-switch composition lemma.

Revision tmr5-switch-composition055.v1, seed 20261115.
For variable-disjoint UNSAT CNFs F(x), G(y) and a fresh variable z,
H = {C or z : C in F} u {D or not z : D in G}.
Checks, by exhaustive computation on small instances:
 (1) H is UNSAT and H|z=0 == F, H|z=1 == G as clause sets;
 (2) exact minimum tree-like resolution size (min leaves of a refuting
     decision tree, a KNOWN equivalence) satisfies T(H) == T(F) + T(G);
 (3) the z-weakened refutation of F (every clause C -> C or z) is a legal
     resolution derivation of the unit clause (z), and likewise for G with
     (not z); one final resolution step on z refutes H (step-checked).
Finite COMPUTATIONAL evidence for an elementary PROVED lemma; it is not a
lower bound for any combined proof system.
"""
import itertools, json, random, sys, time, hashlib
from functools import lru_cache

REV = "tmr5-switch-composition055.v1"; SEED = 20261115
asserts = 0
def check(c, msg):
    global asserts; asserts += 1
    if not c: raise AssertionError(msg)

def php(m):
    v = lambda i, j: i*m + j + 1
    cl = [tuple(v(i, j) for j in range(m)) for i in range(m+1)]
    for j in range(m):
        for i in range(m+1):
            for k in range(i+1, m+1):
                cl.append((-v(i, j), -v(k, j)))
    return (m+1)*m, cl

def tseitin(nv, edges):
    cl = []
    for u in range(nv):
        inc = [e+1 for e, (a, b) in enumerate(edges) if u in (a, b)]
        ch = 1 if u == 0 else 0
        for signs in itertools.product([0, 1], repeat=len(inc)):
            if sum(signs) % 2 != ch:
                cl.append(tuple(-x if s else x for x, s in zip(inc, signs)))
    return len(edges), cl

def sat(a, cl):
    return all(any(((a >> (abs(l)-1)) & 1) == (l > 0) for l in c) for c in cl)
def brute_unsat(n, cl):
    return not any(sat(a, cl) for a in range(1 << n))

def min_treelike(n, cl):
    @lru_cache(maxsize=None)
    def T(pos, neg):
        for c in cl:
            if all(((neg >> (abs(l)-1)) & 1) if l > 0 else ((pos >> (abs(l)-1)) & 1) for l in c):
                return 1
        best = None
        for x in range(n):
            bit = 1 << x
            if (pos | neg) & bit: continue
            a = T(pos, neg | bit)
            if best is not None and a >= best: continue
            s = a + T(pos | bit, neg)
            if best is None or s < best: best = s
        return best
    r = T(0, 0); T.cache_clear(); return r

def rand_unsat(n, m, k, rng):
    while True:
        cl = [tuple(v if rng.random() < .5 else -v for v in rng.sample(range(1, n+1), k)) for _ in range(m)]
        if brute_unsat(n, cl): return cl

def shift(cl, d): return [tuple(l + d if l > 0 else l - d for l in c) for c in cl]

def switch(nF, F, nG, G):
    Gs = shift(G, nF); z = nF + nG + 1
    H = [tuple(c) + (z,) for c in F] + [tuple(d) + (-z,) for d in Gs]
    return nF + nG + 1, H, Gs, z

def restrict(cl, var, val):
    out = []
    for c in cl:
        if (var if val else -var) in c: continue
        out.append(tuple(l for l in c if abs(l) != var))
    return out

# ---- resolution derivation by DPLL tree -> step-checked resolution proof ----
def tree_proof(n, cl):
    """Return list of steps (clause, parents) from a refuting decision tree."""
    steps = []
    def rec(pos, neg):
        for i, c in enumerate(cl):
            if all(((neg >> (abs(l)-1)) & 1) if l > 0 else ((pos >> (abs(l)-1)) & 1) for l in c):
                steps.append((frozenset(c), ('axiom', i))); return len(steps) - 1
        for x in range(n):
            bit = 1 << x
            if (pos | neg) & bit: continue
            a = rec(pos, neg | bit); b = rec(pos | bit, neg)
            ca, cb = steps[a][0], steps[b][0]
            v = x + 1
            if v not in ca: return a          # weakening-free shortcut
            if -v not in cb: return b
            steps.append((frozenset((ca - {v}) | (cb - {-v})), ('res', a, b, v)))
            return len(steps) - 1
    root = rec(0, 0)
    return steps, root

def check_proof(steps, root, axioms, target):
    ax = [frozenset(c) for c in axioms]
    for c, why in steps:
        if why[0] == 'axiom':
            check(c == ax[why[1]], 'axiom mismatch')
        else:
            _, a, b, v = why
            check(v in steps[a][0] and -v in steps[b][0], 'pivot')
            check(c == (steps[a][0] - {v}) | (steps[b][0] - {-v}), 'resolvent')
    check(steps[root][0] <= frozenset(target), 'root not target')

def weaken(steps, lit):
    out = []
    for c, why in steps:
        out.append((c | {lit}, why))
    return out

def main():
    t0 = time.time(); rng = random.Random(SEED)
    fams = {}
    fams['php1'] = php(1); fams['php2'] = php(2)
    fams['ts_K3'] = tseitin(3, [(0, 1), (1, 2), (0, 2)])
    fams['ts_K4m'] = tseitin(4, [(0, 1), (1, 2), (2, 3), (3, 0)])
    for i in range(3):
        fams[f'rand3_n4_{i}'] = (4, rand_unsat(4, 14, 3, rng))
    for k, (n, cl) in fams.items():
        check(brute_unsat(n, cl), f'{k} unsat')
    names = list(fams)
    rows = []
    for a, b in itertools.product(names, names):
        nF, F = fams[a]; nG, G = fams[b]
        if nF + nG + 1 > 11: continue
        nH, H, Gs, z = switch(nF, F, nG, G)
        check(brute_unsat(nH, H), 'H unsat')
        check(sorted(map(sorted, restrict(H, z, 0))) == sorted(map(sorted, F)), 'H|z=0 == F')
        check(sorted(map(sorted, restrict(H, z, 1))) == sorted(map(sorted, Gs)), 'H|z=1 == G')
        tF, tG, tH = min_treelike(nF, F), min_treelike(nG, G), min_treelike(nH, H)
        check(tH == tF + tG, f'additivity {a},{b}: {tH} vs {tF}+{tG}')
        check(tH >= max(tF, tG), 'restriction lower bound')
        # z-weakened refutations and final switch step
        sF, rF = tree_proof(nF, F); check_proof(sF, rF, F, [])
        sG, rG = tree_proof(nG, Gs and G); check_proof(sG, rG, G, [])
        wF = weaken(sF, z)
        HF = [tuple(c) + (z,) for c in F]
        check_proof(wF, rF, HF, [z])
        sG2, rG2 = tree_proof(nF + nG, Gs)
        wG = weaken(sG2, -z); HG = [tuple(d) + (-z,) for d in Gs]
        check_proof(wG, rG2, HG, [-z])
        cz, cnz = wF[rF][0], wG[rG2][0]
        check(z in cz and -z in cnz, 'switch literals present')
        final = (cz - {z}) | (cnz - {-z})
        check(final == frozenset(), 'final empty clause')
        rows.append(dict(F=a, G=b, nH=nH, T_F=tF, T_G=tG, T_H=tH,
                         dag_steps_F=len(sF), dag_steps_G=len(sG2),
                         switch_total=len(sF) + len(sG2) + 1))
    out = dict(revision=REV, seed=SEED, python=sys.version.split()[0],
               families={k: dict(n=v[0], m=len(v[1]), clauses=v[1]) for k, v in fams.items()},
               rows=rows, assertions=asserts, failures=0,
               seconds=round(time.time() - t0, 2),
               scope='finite COMPUTATIONAL checks; tree-like additivity is also PROVED in the report')
    s = json.dumps(out, sort_keys=True, indent=1)
    out['sha256_of_body'] = hashlib.sha256(s.encode()).hexdigest()
    print(json.dumps(out, sort_keys=True, indent=1))

if __name__ == '__main__':
    main()
