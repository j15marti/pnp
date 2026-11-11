"""CLAUDE WORSTCASE-MU-0001 finite control (designed to finish in < 30 s).

For random UNSAT strict 3-CNFs on n<=5 variables:
  * W_tree(F) := exact minimum number of nodes of a tree-like Resolution
    refutation = min over decision trees (DPLL without propagation) of
    2*leaves-1, where a leaf is a partial assignment falsifying a clause of F
    (standard equivalence: tree-like Resolution size = decision-tree size).
  * core(F) := a minimally unsatisfiable subformula (deletion filter).
Checks Lemma 1 (premise monotonicity): W_tree(F) <= W_tree(core(F)),
records deficiency m-n of cores and the largest W_tree over found MU cores.
Hostile control: a corrupted 'refutation' (claimed falsified leaf that is not)
must be rejected by the leaf checker.
"""
import itertools, json, random, sys, time
from functools import lru_cache

def sat(F, n):
    for a in itertools.product([False, True], repeat=n):
        if all(any((l > 0) == a[abs(l)-1] for l in C) for C in F):
            return True
    return False

def wtree(F, n):
    F = [tuple(C) for C in F]
    @lru_cache(maxsize=None)
    def best(rho):  # rho: tuple of 0/1/2 (2 = unassigned)
        for C in F:
            if all(rho[abs(l)-1] != 2 and (rho[abs(l)-1] == 1) != (l > 0) for l in C):
                return 1  # leaf: rho falsifies C
        b = None
        for v in range(n):
            if rho[v] == 2:
                r0 = rho[:v] + (0,) + rho[v+1:]; r1 = rho[:v] + (1,) + rho[v+1:]
                c = 1 + best(r0) + best(r1)
                if b is None or c < b: b = c
        return b if b is not None else float('inf')
    return best((2,) * n)

def core(F, n):
    G = list(F)
    i = 0
    while i < len(G):
        H = G[:i] + G[i+1:]
        if not sat(H, n): G = H
        else: i += 1
    return G

def falsifies(rho, C):
    return all(abs(l) in rho and rho[abs(l)] != (l > 0) for l in C)

def main(seed=20261111, trials_per_n=150, budget=25.0):
    rnd = random.Random(seed); t0 = time.time(); out = {}
    for n in (3, 4, 5):
        clauses = [tuple(s * v for s, v in zip(signs, vs))
                   for vs in itertools.combinations(range(1, n+1), 3)
                   for signs in itertools.product([1, -1], repeat=3)]
        rec = dict(trials=0, unsat=0, violations=0, max_W_core=0, max_W_F=0,
                   core_deficiency_hist={}, max_core_example=None)
        while rec['trials'] < trials_per_n and time.time() - t0 < budget:
            rec['trials'] += 1
            m = rnd.randint(len(clauses)//2, len(clauses))
            F = rnd.sample(clauses, m)
            if sat(F, n): continue
            rec['unsat'] += 1
            K = core(F, n)
            wF, wK = wtree(F, n), wtree(K, n)
            if wF > wK: rec['violations'] += 1
            d = len(K) - len({abs(l) for C in K for l in C})
            rec['core_deficiency_hist'][str(d)] = rec['core_deficiency_hist'].get(str(d), 0) + 1
            rec['max_W_F'] = max(rec['max_W_F'], wF)
            if wK > rec['max_W_core']:
                rec['max_W_core'] = wK; rec['max_core_example'] = sorted(K)
        out[str(n)] = rec
    # hostile control: non-falsifying leaf must be rejected
    ctrl = dict(true_leaf=falsifies({1: False, 2: False, 3: False}, (1, 2, 3)),
                bogus_leaf=falsifies({1: True, 2: False, 3: False}, (1, 2, 3)))
    out['hostile_control'] = ctrl
    out['ok'] = all(out[k]['violations'] == 0 for k in ('3', '4', '5')) and ctrl['true_leaf'] and not ctrl['bogus_leaf']
    out['elapsed_s'] = round(time.time() - t0, 2); out['seed'] = seed
    return out

if __name__ == '__main__':
    res = main()
    path = sys.argv[1] if len(sys.argv) > 1 else 'mu_reduction_check_results.json'
    json.dump(res, open(path, 'w'), indent=1)
    print(json.dumps({k: (v if k in ('ok', 'elapsed_s', 'hostile_control') else {kk: v[kk] for kk in ('trials','unsat','violations','max_W_F','max_W_core','core_deficiency_hist')}) for k, v in res.items() if k != 'seed'}, indent=1))
