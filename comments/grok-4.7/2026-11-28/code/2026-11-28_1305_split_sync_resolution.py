#!/usr/bin/env python3
"""Grok 4.7, 2026-11-28 12:49 KST.
Mini-bucket split-copy plans with exhaustive synchronization guards (FP58 Sec.3 semantics,
threshold K=1, i.e. zero-energy decision) are converted into explicit resolution refutations
of the ORIGINAL CNF, checked by an independent checker.  Theorem in the GROK_WORK log:
width <= max(k, w-1) + |S|,  size <= sum_b (#derived clauses under guard b) + 2^|S| + |F|.
Also computes, by width-bounded saturation, the minimum resolution width W(F) of each instance,
so that every successful plan must satisfy max(k,w-1)+|S| >= W(F).
Deterministic: all randomness from random.Random(seed)."""
import itertools, random, json, sys

# ---------------- instances ----------------
def tseitin(edges, nverts, odd_vertex=0):
    var = {e: i + 1 for i, e in enumerate(edges)}
    cls = []
    for v in range(nverts):
        inc = [var[e] for e in edges if v in e]
        charge = 1 if v == odd_vertex else 0
        for signs in itertools.product([0, 1], repeat=len(inc)):
            if sum(signs) % 2 != charge:        # forbid assignments with wrong parity
                cls.append(frozenset(-x if s else x for x, s in zip(inc, signs)))
    return len(edges), cls

def K4():
    return [(a, b) for a in range(4) for b in range(a + 1, 4)], 4
def K33():
    return [(a, b) for a in range(3) for b in range(3, 6)], 6
def cube():
    E = []
    for a in range(8):
        for i in range(3):
            b = a ^ (1 << i)
            if a < b: E.append((a, b))
    return E, 8
def petersen():
    E = [(i, (i + 1) % 5) for i in range(5)] + [(i, i + 5) for i in range(5)] + [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    return [tuple(sorted(e)) for e in E], 10

def php(p, h):  # p pigeons, h holes
    v = lambda i, j: i * h + j + 1
    cls = [frozenset(v(i, j) for j in range(h)) for i in range(p)]
    for j in range(h):
        for a in range(p):
            for b in range(a + 1, p):
                cls.append(frozenset([-v(a, j), -v(b, j)]))
    return p * h, cls

def fano_nae():
    L = [(1,2,3),(1,4,5),(1,6,7),(2,4,6),(2,5,7),(3,4,7),(3,5,6)]
    cls = []
    for t in L:
        cls.append(frozenset(t)); cls.append(frozenset(-x for x in t))
    return 7, cls

def is_sat(n, cls):
    for a in itertools.product([0, 1], repeat=n):
        if all(any((l > 0) == bool(a[abs(l) - 1]) for l in c) for c in cls):
            return True
    return False

def random3(n, m, seed):
    R = random.Random(seed)
    while True:
        cls = []
        for _ in range(m):
            vs = R.sample(range(1, n + 1), 3)
            cls.append(frozenset(x if R.random() < .5 else -x for x in vs))
        if not is_sat(n, cls):
            return n, cls

# ---------------- plan evaluation under one guard ----------------
def falsified(clause, asg):  # asg: dict var->0/1 over (at least) vars of clause
    return all((asg[abs(l)] == 0) if l > 0 else (asg[abs(l)] == 1) for l in clause)

def run_plan(n, cls, S, b, order, w, seed, extreme=False):
    """Returns (refuted, lines) for F|_b.  lines: list of ('ax', orig_index, clause) or
    ('res', p, q, pivot, clause).  Clauses are over non-S variables."""
    R = random.Random(seed)
    lines = []; key = {}
    def add(entry):
        c = entry[-1]
        if c in key: return key[c]
        lines.append(entry); key[c] = len(lines) - 1; return key[c]
    factors = []   # (scope frozenset, [line ids])
    for i, c in enumerate(cls):
        if any((abs(l) in b) and ((l > 0) == (b[abs(l)] == 1)) for l in c):
            continue  # satisfied by guard
        r = frozenset(l for l in c if abs(l) not in b)
        lid = add(('ax', i, r))
        if not r: return True, lines
        factors.append((frozenset(abs(l) for l in r), [lid]))
    for v in order:
        if v in b: continue
        inc = [f for f in factors if v in f[0]]
        rest = [f for f in factors if v not in f[0]]
        R.shuffle(inc)
        groups = []
        for f in inc:
            placed = False
            if not extreme:
                for g in groups:
                    if len(g[0] | f[0]) <= w:
                        g[0] |= f[0]; g[1].append(f); placed = True; break
            if not placed:
                groups.append([set(f[0]), [f]])
        new = []
        for U, fs in groups:
            lids = sorted({l for f in fs for l in f[1]})
            others = sorted(U - {v})
            out = set()
            for t in itertools.product([0, 1], repeat=len(others)):
                asg = dict(zip(others, t))
                pick = []
                for val in (0, 1):
                    asg[v] = val; hit = None
                    for l in lids:
                        if falsified(lines[l][-1], asg): hit = l; break
                    pick.append(hit)
                if pick[0] is None or pick[1] is None: continue
                c0, c1 = lines[pick[0]][-1], lines[pick[1]][-1]
                if v not in c0: out.add(pick[0]); continue      # c0 subset of not-t
                if -v not in c1: out.add(pick[1]); continue
                res = (c0 - {v}) | (c1 - {-v})
                lid = add(('res', pick[0], pick[1], v, frozenset(res)))
                if not res: return True, lines
                out.add(lid)
            if out:
                new.append((frozenset(others), sorted(out)))
        factors = rest + new
    return False, lines

# ---------------- lifting and combination ----------------
def lift_and_combine(n, cls, S, per_guard):
    """per_guard: dict tuple(b) -> lines.  Returns global proof lines (clause, how)."""
    proof = []; idx = {}
    def emit(c, how):
        if c in idx: return idx[c]
        proof.append((c, how)); idx[c] = len(proof) - 1; return idx[c]
    final = {}
    for bt, lines in per_guard.items():
        lifted = []
        for e in lines:
            if e[0] == 'ax':
                c = cls[e[1]]; lifted.append(emit(c, ('ax',)))
            else:
                _, p, q, piv, _ = e
                cp, cq = proof[lifted[p]][0], proof[lifted[q]][0]
                c = frozenset((cp - {piv}) | (cq - {-piv}))
                lifted.append(emit(c, ('res', lifted[p], lifted[q], piv)))
        final[bt] = lifted[-1] if lines[-1][-1] == frozenset() else None
        assert final[bt] is not None
    # combine along the full binary tree on S (order = S list)
    def comb(prefix):
        if len(prefix) == len(S): return final[tuple(prefix)]
        y = S[len(prefix)]
        d0 = comb(prefix + [0]); d1 = comb(prefix + [1])
        c0, c1 = proof[d0][0], proof[d1][0]
        if y not in c0: return d0
        if -y not in c1: return d1
        c = frozenset((c0 - {y}) | (c1 - {-y}))
        return emit(c, ('res', d0, d1, y))
    root = comb([])
    return proof, root

def check_refutation(cls, proof, root):
    """Independent checker: every line is an axiom of F or the resolvent of two EARLIER lines on
    one pivot with no other complementary pair; root line is the empty clause."""
    F = set(cls)
    for i, (c, how) in enumerate(proof):
        if any(-l in c for l in c): return False, f'tautology at {i}'
        if how[0] == 'ax':
            if c not in F: return False, f'non-axiom {i}'
        else:
            _, p, q, piv = how
            if not (p < i and q < i): return False, f'order {i}'
            a, bq = proof[p][0], proof[q][0]
            if piv not in a or -piv not in bq: return False, f'pivot {i}'
            r = (a - {piv}) | (bq - {-piv})
            if any(-l in r for l in r): return False, f'double clash {i}'
            if frozenset(r) != c: return False, f'bad resolvent {i}'
    if proof[root][0] != frozenset(): return False, 'root not empty'
    return True, 'ok'

# ---------------- minimum resolution width by saturation ----------------
def min_width(n, cls, cap=8, budget=60_000_000):
    """Smallest W such that width-W resolution (with forward subsumption pruning, which preserves
    width-W refutability) derives the empty clause.  Returns None if cap/budget exceeded."""
    k = max(len(c) for c in cls)
    work = 0
    for W in range(k, cap + 1):
        have = set(); bylit = {}
        def subsumed(r):
            # r subsumed by an existing clause?  check all subsets (|r|<=W small)
            rl = sorted(r)
            for size in range(len(rl) + 1):
                for sub in itertools.combinations(rl, size):
                    if frozenset(sub) in have: return True
            return False
        queue = []
        for c in sorted(set(cls), key=len):
            if len(c) <= W and not subsumed(c):
                have.add(c); queue.append(c)
                for l in c: bylit.setdefault(l, set()).add(c)
        i = 0
        while i < len(queue):
            c = queue[i]; i += 1
            if c not in have: continue
            for l in c:
                for d in list(bylit.get(-l, ())):
                    work += 1
                    if work > budget: return None
                    r = (c - {l}) | (d - {-l})
                    if len(r) > W or any(-x in r for x in r): continue
                    r = frozenset(r)
                    if subsumed(r): continue
                    if not r: return W
                    have.add(r); queue.append(r)
                    for x in r: bylit.setdefault(x, set()).add(r)
    return None

# ---------------- experiment driver ----------------
def experiment(name, n, cls, ws, seeds, max_s=9, extreme_too=True, compute_w=True):
    k = max(len(c) for c in cls)
    Wmin = min_width(n, cls) if compute_w else None
    rows = []
    for w in ws:
        for seed in seeds:
            for extreme in ([False, True] if extreme_too else [False]):
                R = random.Random(1000 * seed + w + (7 if extreme else 0))
                order = list(range(1, n + 1)); R.shuffle(order)
                S = []; pool = order[:]; R.shuffle(pool)
                while True:
                    per = {}; ok = True
                    for bt in itertools.product([0, 1], repeat=len(S)):
                        b = dict(zip(S, bt))
                        refuted, lines = run_plan(n, cls, S, b, order, w, seed, extreme)
                        if not refuted: ok = False; break
                        per[bt] = lines
                    if ok: break
                    if len(S) >= max_s or not pool: per = None; break
                    S.append(pool.pop())
                if per is None:
                    rows.append(dict(w=w, seed=seed, extreme=extreme, s=None)); continue
                proof, root = lift_and_combine(n, cls, S, per)
                good, msg = check_refutation(cls, proof, root)
                width = max(len(c) for c, _ in proof)
                guard_lines = sum(len(l) for l in per.values())
                bound_w = max(k, w - 1) + len(S)
                rows.append(dict(w=w, seed=seed, extreme=extreme, s=len(S), checked=good, msg=msg,
                                 proof_lines=len(proof), guard_lines_total=guard_lines,
                                 width=width, width_bound=bound_w,
                                 width_ok=width <= bound_w, Wmin=Wmin,
                                 necessary_ok=(Wmin is None) or bound_w >= Wmin))
    return dict(instance=name, vars=n, clauses=len(cls), k=k, Wmin=Wmin, rows=rows)

if __name__ == '__main__':
    out = []
    E, nv = K4(); n, c = tseitin(E, nv); out.append(experiment('Tseitin-K4', n, c, [3, 4, 5], [1, 2, 3]))
    E, nv = K33(); n, c = tseitin(E, nv); out.append(experiment('Tseitin-K33', n, c, [3, 4, 5], [1, 2, 3]))
    E, nv = cube(); n, c = tseitin(E, nv); out.append(experiment('Tseitin-Q3', n, c, [3, 4, 5, 6], [1, 2, 3], compute_w=False))
    E, nv = petersen(); n, c = tseitin(E, nv); out.append(experiment('Tseitin-Petersen', n, c, [3, 4, 5, 6], [1, 2], compute_w=False))
    n, c = php(4, 3); out.append(experiment('PHP-4-3', n, c, [3, 4, 5, 6], [1, 2, 3]))
    n, c = fano_nae(); out.append(experiment('Fano-NAE', n, c, [3, 4, 5], [1, 2, 3]))
    n, c = random3(14, 100, 5); out.append(experiment('Random3CNF-14-100', n, c, [3, 4, 5, 6], [1, 2]))
    viol = 0; tot = 0
    for o in out:
        print(f"{o['instance']}: vars={o['vars']} clauses={o['clauses']} k={o['k']} Wmin={o['Wmin']}")
        for r in o['rows']:
            tot += 1
            if r['s'] is None:
                print(f"   w={r['w']} seed={r['seed']} extreme={r['extreme']}: no success with s<=9"); continue
            if not (r['checked'] and r['width_ok'] and r['necessary_ok']): viol += 1
            print(f"   w={r['w']} seed={r['seed']} extreme={r['extreme']}: s={r['s']} checked={r['checked']} "
                  f"lines={r['proof_lines']} width={r['width']}<=bound {r['width_bound']} (>=Wmin {r['Wmin']}: {r['necessary_ok']})")
    print('rows', tot, 'violations', viol)
    json.dump(out, open('split_sync_resolution.out.json', 'w'), indent=1, default=str)
