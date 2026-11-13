#!/usr/bin/env python3
"""Independent unpruned recomputation (dict over full ternary assignments) for 6-9 var instances."""
import sys, json, itertools
sys.path.insert(0, __file__.rsplit('/',1)[0])
from wcd0001_treelike_exact import build
def run(name):
    n, cl, _ = build(name)
    memo = {}
    def fals(a):
        return any(all(a[v] is not None and a[v] != r for v, r in c) for c in cl)
    def D(a):
        if a in memo: return memo[a]
        if fals(a): memo[a] = 1; return 1
        best = min(D(a[:x]+(0,)+a[x+1:]) + D(a[:x]+(1,)+a[x+1:]) for x in range(n) if a[x] is None)
        memo[a] = best; return best
    return D((None,)*n)
out = {nm: run(nm) for nm in sys.argv[1:]}
print(json.dumps(out)); json.dump(out, open("results/raw/claude_wcd/wcd0001_independent_check.json","w"))
