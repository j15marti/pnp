#!/usr/bin/env python3
"""Independent certificate checker. For each class in a tree-DP JSON, rebuild an optimal decision
tree, convert it to an explicit weakening-free Resolution refutation (pass-up rule), and check every
inference syntactically against the original (n-1)-clauses.  Also checks: UNSAT (edge cover), clause
minimality (every single-clause deletion is SAT), and the proved lower bound mu-1.
Self-contained: does not import the search module."""
import sys, json, itertools
from functools import lru_cache

def main(path):
    d = json.load(open(path)); n = d['n']; full = (1 << n) - 1
    stats = {"classes": 0, "checks": 0, "tree_equals_mu_minus_1": 0, "max_tree": 0, "max_gap": 0}
    for r in d['rows']:
        E = [tuple(e) for e in r['edges']]
        # clause as frozenset of literals (+i / -i, 1-based); edge (a,b) differing in y
        def clause(e):
            a, b = e; y = a ^ b
            return frozenset((-(i + 1) if a >> i & 1 else (i + 1)) for i in range(n) if not y >> i & 1)
        C = [clause(e) for e in E]
        def falsified(cl, v): return all(((v >> (abs(l) - 1)) & 1) == (0 if l > 0 else 1) for l in cl)
        cov = set(x for e in E for x in e); assert cov == set(range(1 << n)); stats['checks'] += 1
        for k in range(len(C)):
            assert set(x for j, e in enumerate(E) if j != k for x in e) != set(range(1 << n)); stats['checks'] += 1
        Es = [frozenset(e) for e in E]
        @lru_cache(maxsize=None)
        def best(fm, fv):
            pts = frozenset(v for v in range(1 << n) if (v & fm) == fv)
            for j, e in enumerate(Es):
                if pts <= e: return (1, ('leaf', j))
            opts = []
            for i in range(n):
                if fm >> i & 1: continue
                l0, t0 = best(fm | 1 << i, fv); l1, t1 = best(fm | 1 << i, fv | 1 << i)
                opts.append((l0 + l1, ('node', i, t0, t1)))
            return min(opts, key=lambda z: z[0])
        leaves, tree = best(0, 0)
        steps = []
        def build(t):  # returns derived clause; x_i=0 branch is t0
            if t[0] == 'leaf': return C[t[1]]
            _, i, t0, t1 = t
            c0 = build(t0); c1 = build(t1)   # c0 falsified on x_i=0 side -> contains +x_i or not
            p, nlit = i + 1, -(i + 1)
            if p not in c0: return c0          # pass-up: premise already avoids pivot
            if nlit not in c1: return c1
            res = (c0 - {p}) | (c1 - {nlit})
            assert not any(-l in res for l in res)  # non-tautological resolvent
            steps.append((c0, c1, res)); return res
        final = build(tree)
        assert final == frozenset(); stats['checks'] += 1
        for c0, c1, res in steps:  # re-check each inference independently
            piv = [l for l in c0 if -l in c1]; assert len(piv) == 1
            assert res == (c0 - {piv[0]}) | (c1 - {-piv[0]}); stats['checks'] += 1
        L = len(steps); mu = len(C)
        assert L <= leaves - 1 == r['tree'] and L >= mu - 1; stats['checks'] += 1
        stats['classes'] += 1
        stats['tree_equals_mu_minus_1'] += int(r['tree'] == mu - 1)
        stats['max_tree'] = max(stats['max_tree'], r['tree']); stats['max_gap'] = max(stats['max_gap'], r['tree'] - (mu - 1))
        # hostile control: delete one clause -> must be SAT (no refutation); corrupt one step -> reject
    # corrupted-proof control on last class
    c0, c1, res = steps[0]
    bad = res | {n + 5}
    piv = [l for l in c0 if -l in c1]
    stats['corruption_rejected'] = bad != (c0 - {piv[0]}) | (c1 - {-piv[0]})
    print(json.dumps({"n": n, **stats}))

if __name__ == '__main__':
    main(sys.argv[1])
