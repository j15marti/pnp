"""Expander control for EQUALITY-LOCALIZATION-MINOR-BARRIER65.
Min-fill treewidth UPPER bounds (heuristic) for clause-variable incidence graphs of
random 3-CNF (ratio 4.26) vs. 2*c*log2(N) bound of Lemma 65B. Runtime <30s per call."""
import random, math, json, sys
import networkx as nx
from networkx.algorithms.approximation import treewidth_min_fill_in
def inc(n, ratio, rng):
    G = nx.Graph()
    for j in range(int(ratio*n)):
        for v in rng.sample(range(n), 3): G.add_edge(('c', j), ('v', v))
    return G
out = []
for n in [20, 40, 80, 160, 320]:
    rng = random.Random(n)
    G = inc(n, 4.26, rng); tw, _ = treewidth_min_fill_in(G)
    N = G.number_of_edges()
    out.append(dict(n=n, N_edges=N, tw_ub=tw, bound_2clogN=round(2*0.1*math.log2(N), 2), ratio=round(tw/n, 3)))
    print(out[-1], flush=True)
json.dump(out, open('research/code/2026-10-22_1500_expander_tw_control66.json', 'w'), indent=1)
