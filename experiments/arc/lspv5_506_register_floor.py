#!/usr/bin/env python3
"""LSPV-5/506: exact register-floor test, independent of execution count.
Plain reachability over resident sets (|S|<=cap) in the recomputation model of
lspv5_506_recompute_frontier.py; if the sink is unreachable the cap is infeasible
for EVERY number of executions. Also reports RES fan-out (tree-likeness).
Run: python3 <this> <packet.json> [<packet.json> ...]"""
import json, sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from lspv5_506_recompute_frontier import dag, subsets
def reach(par, size, cap):
    n = len(par); pm = [sum(1 << p for p in ps) for ps in par]
    seen = {0}; todo = [0]
    while todo:
        S = todo.pop()
        for j in range(n):
            if pm[j] & ~S: continue
            for keep in subsets(S):
                if keep >> j & 1: continue
                peak = bin(keep | pm[j]).count("1") + 1
                if peak > cap and (peak > cap + 1 or not any(
                        not keep >> p & 1 and size[p] >= size[j] for p in par[j])):
                    continue
                post = keep | 1 << j
                if post >> (n - 1) & 1: return True, len(seen)
                if post not in seen: seen.add(post); todo.append(post)
    return False, len(seen)
out = []
for path in sys.argv[1:]:
    par, size = dag(path); n = len(par)
    fan = [sum(j in ps for ps in par) for j in range(n)]
    row = {"packet": path, "paid_res": n, "max_res_fanout": max(fan),
           "shared_res_nodes": [j for j in range(n) if fan[j] > 1],
           "tree_like_over_res": max(fan) <= 1}
    for cap in (1, 2, 3, 4):
        ok, st = reach(par, size, cap); row["cap%d" % cap] = {"feasible": ok, "states_explored": st}
    out.append(row)
print(json.dumps(out, indent=1))
