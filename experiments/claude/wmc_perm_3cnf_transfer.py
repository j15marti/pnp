"""Exact check: the weighted model-count polynomial of an explicit width<=3 CNF
psi_n (perfect matchings of K_{n,n}, sequential prefix-OR exactly-one encoding)
equals perm_n after setting every auxiliary weight to 1, and every x-assignment
has at most one auxiliary extension (exactly one iff x is a permutation matrix).
Deterministic; no randomness.  Usage: python -I wmc_perm_3cnf_transfer.py OUT.json
"""
import itertools, json, sys, hashlib, time

def build(n):
    var = {}
    def v(name):
        if name not in var: var[name] = len(var) + 1
        return var[name]
    for i in range(n):
        for j in range(n): v(('x', i, j))
    clauses, blocks = [], []
    lines = [[('x', i, j) for j in range(n)] for i in range(n)] + \
            [[('x', i, j) for i in range(n)] for j in range(n)]
    for b, lits in enumerate(lines):
        aux = [('s', b, t) for t in range(n)]
        blk = []
        x0, s0 = v(lits[0]), v(aux[0])
        blk += [(-x0, s0), (-s0, x0)]                       # s0 <-> x0
        for t in range(1, n):
            xt, st, sp = v(lits[t]), v(aux[t]), v(aux[t-1])
            blk += [(-sp, st), (-xt, st), (-st, sp, xt)]     # st <-> sp or xt
            blk += [(-sp, -xt)]                               # at most one
        blk += [(v(aux[-1]),)]                                # at least one
        clauses += blk
        blocks.append(([v(a) for a in aux], [v(l) for l in lits], blk))
    return var, clauses, blocks

def sat(cl, a):
    return all(any((a[abs(l)] if l > 0 else 1 - a[abs(l)]) for l in c) for c in cl)

def run(n):
    var, clauses, blocks = build(n)
    assert max(len(c) for c in clauses) <= 3
    xs = [var[('x', i, j)] for i in range(n) for j in range(n)]
    poly = {}   # monomial over x (frozenset of x var ids) -> coefficient
    ext_hist = {}
    for bits in itertools.product((0, 1), repeat=len(xs)):
        a = {xv: b for xv, b in zip(xs, bits)}
        total = 1
        for auxv, litv, blk in blocks:   # aux vars of blocks are disjoint
            cnt = 0
            for ab in itertools.product((0, 1), repeat=len(auxv)):
                aa = dict(a); aa.update(zip(auxv, ab))
                cnt += sat(blk, aa)
            total *= cnt
            if total == 0: break
        ext_hist[total] = ext_hist.get(total, 0) + 1
        if total:
            m = frozenset(xv for xv, b in zip(xs, bits) if b)
            poly[m] = poly.get(m, 0) + total
    perm = {}
    for p in itertools.permutations(range(n)):
        m = frozenset(var[('x', i, p[i])] for i in range(n))
        perm[m] = perm.get(m, 0) + 1
    return {'n': n, 'num_vars': len(var), 'num_x': len(xs), 'num_clauses': len(clauses),
            'max_width': max(len(c) for c in clauses),
            'extension_count_histogram': {str(k): v for k, v in sorted(ext_hist.items())},
            'wmc_monomials': len(poly), 'perm_monomials': len(perm),
            'wmc_equals_perm': poly == perm}

if __name__ == '__main__':
    t0 = time.time()
    res = {'revision': 'CLAUDE_WMC_PERM_TRANSFER_v1', 'seed': None,
           'cases': [run(n) for n in (1, 2, 3, 4)]}
    res['elapsed_s'] = round(time.time() - t0, 2)
    out = json.dumps(res, indent=1, sort_keys=True)
    open(sys.argv[1], 'w').write(out + '\n')
    print(out); print('sha256', hashlib.sha256((out + '\n').encode()).hexdigest())
