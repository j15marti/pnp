#!/usr/bin/env python3
"""Exhaustive companion check (Grok 4.7, 2026-11-28 KST): for Tseitin on K4 and on the
triangular prism (both girth 3; three charge vectors: odd, even, odd3), enumerate
EVERY partial assignment rho of the edge variables (3^|E|). For each rho with conflict-free UP
closure, decide existence of a Hall certificate: if the half-integral point is feasible
(Theorem 1 => no certificate) record that; otherwise run the exact 0/1 ILP. States whose
exclusion graph has a triangle are counted (triangle_states).
Also checks PHP(5,4) functional: root width<=2 RUP admits nothing (T1 claim)."""
import itertools, json, sys
import networkx as nx
import importlib.util, os
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '2026-11-28_1514_hall_lp_obstruction.py')
_spec = importlib.util.spec_from_file_location('hall_lp_obstruction', _p)
_m = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_m)
sys.modules['hall_lp_obstruction'] = _m
from hall_lp_obstruction import (tseitin_cnf, unit_propagate, restrict, exclusion_graph,
    has_triangle, half_point_feasible, exact_hall, verify_hall, php_functional,
    width2_rup_saturate)

def run(name, G, charge):
    n, C = tseitin_cnf(G, charge)
    st = dict(name=name, nvars=n, assignments=0, up_conflict=0, open=0, open_halfpoint=0,
              open_ilp=0, open_ilp_hall=0, triangle_states=0)
    for vals in itertools.product([None, False, True], repeat=n):
        rho = {i + 1: v for i, v in enumerate(vals) if v is not None}
        st['assignments'] += 1
        a, conf, _ = unit_propagate(C, rho)
        if conf: st['up_conflict'] += 1; continue
        st['open'] += 1
        R = restrict(C, a); X = exclusion_graph(R)
        if has_triangle(X): st['triangle_states'] += 1
        if half_point_feasible(R, X): st['open_halfpoint'] += 1; continue
        st['open_ilp'] += 1
        h, val, cert = exact_hall(R, X)
        assert h is not None
        if h: st['open_ilp_hall'] += 1; verify_hall(cert, R, X)
    return st

out = []
for gname, G in [('K4', nx.complete_graph(4)), ('prism', nx.circular_ladder_graph(3))]:
    nodes = sorted(G.nodes())
    for label, ch in [('odd', {nodes[0]: 1}), ('even', {}), ('odd3', {nodes[0]: 1, nodes[1]: 1, nodes[2]: 1})]:
        s = run(f'{gname}-{label}', G, ch); out.append(s); print(json.dumps(s), flush=True)
n, C = php_functional(4)
R2, conf, adm, vis = width2_rup_saturate(C, n)
s = dict(name='PHP(5,4) root width2 RUP', admitted=adm, conflict=conf, visits=vis)
out.append(s); print(json.dumps(s))
json.dump(out, open('exhaustive.out.json', 'w'), indent=1)
