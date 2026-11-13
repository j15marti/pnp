#!/usr/bin/env python3
"""LSPV-5/527 control: number of RES steps that the LSPV-2/604 DPLL-to-Resolution scheme
(one RES per internal branch node, unit propagation counted as branching) would emit on the
same odd cubic Tseitin sources used by lspv5_527_native386_xor_chain_er_compiler.py.
Static BFS edge order, guard eliminated first. Counts only; each graph < 30 s or skipped.
Usage: python3 lspv5_527_dpll_tree_count.py OUT.json"""
import json, sys, time, importlib.util, os
spec = importlib.util.spec_from_file_location('x', os.path.join(os.path.dirname(__file__), 'lspv5_527_native386_xor_chain_er_compiler.py'))
X = importlib.util.module_from_spec(spec); spec.loader.exec_module(X)
def count(n, edges, budget=25.0):
    occ = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges): occ[u].append(i); occ[v].append(i)
    charge = [1] + [0] * (n - 1); t0 = time.time()
    order = []  # BFS edge order
    for v in X.bfs_order(n, edges):
        for e in sorted(occ[v]):
            if e not in order: order.append(e)
    def rec(a):
        if time.time() - t0 > budget: raise TimeoutError
        # propagate: a vertex with all incident edges assigned and wrong parity = conflict
        for v in range(n):
            vals = [a[e] for e in occ[v]]
            if None not in vals and sum(vals) % 2 != charge[v]: return 0
        for v in range(n):  # unit: two assigned, one free -> forced (branch with one side closed)
            vals = [a[e] for e in occ[v]]
            if vals.count(None) == 1:
                e = occ[v][vals.index(None)]; need = (charge[v] - sum(x for x in vals if x is not None)) % 2
                a[e] = need; r = rec(a); a[e] = None
                return r + 1  # one RES for the closed sibling branch
        e = next(e for e in order if a[e] is None)
        tot = 1
        for b in (0, 1):
            a[e] = b; tot += rec(a); a[e] = None
        return tot
    try: return rec([None] * len(edges)) + 1  # +1 guard resolution
    except TimeoutError: return None
rows = []
for name, n, edges in X.cubic_graphs():
    t = time.time(); c = count(n, edges); rows.append({'case': name, 'V': n, 'E': len(edges), 'dpll_res_upper': c, 'seconds': round(time.time() - t, 2)})
    print(rows[-1], flush=True)
json.dump(rows, open(sys.argv[1], 'w'), indent=1)
