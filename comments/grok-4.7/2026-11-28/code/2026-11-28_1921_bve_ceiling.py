#!/usr/bin/env python3
"""Grok 4.7 work 2026-11-28 (KST): elimination under a representation ceiling
simulates resolution.  Computational companion (COMPUTATIONAL label).

Tseitin formulas (single odd vertex => UNSAT) on
  (a) random 3-regular graphs (expanders whp), seeds 1000+n;
  (b) cylinders C_k x P_3 (treewidth <= 6).
For each instance:
  1. T2 strict admission (eliminate only if literal+row measure does not increase):
     events before stall.
  2. Davis-Putnam elimination (all non-tautological resolvents, duplicate removal,
     forward subsumption by clauses of the same bucket's exterior) along a
     min-fill order of the variable-interaction graph; peak measure recorded.
  3. Independent trace check: each derived clause is the resolvent on the recorded
     pivot of two clauses available earlier; the empty clause is derived;
     proof size <= events*peak + |F|.
"""
import itertools, json, sys, time
from collections import defaultdict
import networkx as nx
from networkx.algorithms.approximation import treewidth_min_fill_in

def tseitin(G, odd_vertex):
    eid = {tuple(sorted(e)): i + 1 for i, e in enumerate(sorted(tuple(sorted(e)) for e in G.edges()))}
    cls = []
    for x in sorted(G.nodes()):
        inc = sorted(eid[tuple(sorted((x, y)))] for y in G.neighbors(x))
        charge = 1 if x == odd_vertex else 0
        for bits in itertools.product((0, 1), repeat=len(inc)):
            if sum(bits) % 2 != charge:
                cls.append(frozenset(v if b == 0 else -v for v, b in zip(inc, bits)))
    return eid, cls

def measure_of(clauses):
    return sum(len(c) + 1 for c in clauses)

class Formula:
    def __init__(self, clauses):
        self.cl = set(clauses); self.occ = defaultdict(set)
        for c in self.cl:
            for l in c: self.occ[l].add(c)
        self.meas = measure_of(self.cl)
    def add(self, c):
        if c in self.cl: return False
        self.cl.add(c); self.meas += len(c) + 1
        for l in c: self.occ[l].add(c)
        return True
    def remove(self, c):
        self.cl.discard(c); self.meas -= len(c) + 1
        for l in c: self.occ[l].discard(c)
    def resolvents(self, v):
        pos = list(self.occ[v]); neg = list(self.occ[-v]); out = {}
        for p in pos:
            for q in neg:
                r = (p - {v}) | (q - {-v})
                if any(-l in r for l in r): continue
                r = frozenset(r)
                if r not in out: out[r] = (p, q)
        return pos, neg, out
    def delta(self, v):
        pos, neg, out = self.resolvents(v)
        return sum(len(r) + 1 for r in out if r not in self.cl) - measure_of(pos + neg)
    def eliminate(self, v):
        pos, neg, out = self.resolvents(v)
        for c in pos + neg: self.remove(c)
        kept = []
        for r, (p, q) in out.items():
            # forward subsumption: skip r if an existing clause sharing a literal subsumes it
            lit = min(r, key=lambda l: len(self.occ[l])) if r else None
            if lit is not None and any(c <= r for c in self.occ[lit]): continue
            if self.add(r): kept.append((r, p, q, v))
        return kept
    def vars(self):
        return sorted({abs(l) for l, s in self.occ.items() if s})

def strict_admission(clauses):
    F = Formula(clauses); events = 0
    while True:
        cand = [(F.delta(v), v) for v in F.vars()]
        cand = [x for x in cand if x[0] <= 0]
        if not cand: return events, len(F.vars())
        F.eliminate(min(cand)[1]); events += 1
        if frozenset() in F.cl: return events, 0

def dp_order(G, eid):
    # variable interaction graph = line graph (two edge-vars share a vertex constraint)
    L = nx.Graph(); L.add_nodes_from(eid.values())
    for x in G.nodes():
        inc = [eid[tuple(sorted((x, y)))] for y in G.neighbors(x)]
        L.add_edges_from(itertools.combinations(inc, 2))
    width, decomp = treewidth_min_fill_in(L)
    # recover a min-fill elimination order (greedy) explicitly
    H = L.copy(); order = []
    while H.number_of_nodes():
        def fill(u):
            nb = list(H.neighbors(u))
            return sum(1 for a, b in itertools.combinations(nb, 2) if not H.has_edge(a, b))
        u = min(H.nodes(), key=lambda u: (fill(u), H.degree(u), u))
        nb = list(H.neighbors(u)); H.add_edges_from(itertools.combinations(nb, 2)); H.remove_node(u)
        order.append(u)
    return width, order

def dp_run(clauses, order, cap_measure=5_000_000, time_limit=300):
    F = Formula(clauses); trace = []; peak = F.meas; ev = 0; t0 = time.time()
    for v in order:
        if frozenset() in F.cl: break
        trace += F.eliminate(v); ev += 1; peak = max(peak, F.meas)
        if peak > cap_measure: return "CAP_EXCEEDED", ev, peak, trace
        if time.time() - t0 > time_limit: return "TIME", ev, peak, trace
    return ("REFUTED" if frozenset() in F.cl else "SAT"), ev, peak, trace

def check_trace(F0, trace):
    avail = set(F0)
    for r, p, q, v in trace:
        if p not in avail or q not in avail: return False
        if v not in p or -v not in q: return False
        if frozenset((p - {v}) | (q - {-v})) != r: return False
        avail.add(r)
    return frozenset() in avail

def run(name, G):
    eid, F = tseitin(G, min(G.nodes()))
    N = measure_of(F)
    se, left = strict_admission(F)
    tw, order = dp_order(G, eid)
    t0 = time.time()
    st, ev, peak, tr = dp_run(F, order)
    ok = check_trace(F, tr) if st == "REFUTED" else None
    return dict(family=name, vertices=G.number_of_nodes(), vars=len(eid), clauses=len(F), N_measure=N,
                strict_events=se, strict_vars_left=left, minfill_width_linegraph=tw,
                dp_status=st, dp_events=ev, dp_peak=peak, peak_over_N=round(peak / N, 2),
                proof_size=len(tr) + len(F), bound_events_x_peak_plus_N=ev * peak + N,
                trace_check=ok, seconds=round(time.time() - t0, 2))

def main():
    res = []
    for n in [8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 56, 64]:
        G = nx.random_regular_graph(3, n, seed=1000 + n); assert nx.is_connected(G)
        res.append(run("random-3-regular", G)); print(json.dumps(res[-1]), flush=True)
    for k in [4, 8, 16, 32, 64, 128]:
        G = nx.convert_node_labels_to_integers(nx.cartesian_product(nx.cycle_graph(k), nx.path_graph(3)))
        res.append(run("C_k x P_3", G)); print(json.dumps(res[-1]), flush=True)
    json.dump(res, open(sys.argv[1], "w"), indent=1)

if __name__ == "__main__":
    main()
