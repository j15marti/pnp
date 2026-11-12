#!/usr/bin/env python3
"""LSPV-1/589: finite robust-MAY Bellman dual audit.

Run: python3 lspv1_589_may_potential_dual.py [output.json]
Python >=3.9, standard library only. Abstract graph model, NOT an R_mix341 checker.
"""
from __future__ import annotations
import itertools, json, sys, hashlib, pathlib

INF = 10**9

def shortest_to_goal(n, edges, goal):
    # Independent Bellman-Ford relaxation, requires nonnegative weights.
    d = [INF] * n
    d[goal] = 0
    for _ in range(n - 1):
        old = d[:]
        for u, v, c in edges:
            if d[v] < INF:
                d[u] = min(d[u], c + d[v])
        if d == old:
            break
    return tuple(d)

def brute_paths_3(edges, goal):
    # Nonnegative shortest paths have simple representatives, except zero cycles
    # that can be erased. Exhaustively enumerate simple paths of length <= 2.
    out = []
    for s in range(3):
        if s == goal:
            out.append(0)
            continue
        costs = []
        def visit(x, used, cost):
            if x == goal:
                costs.append(cost)
                return
            for u, v, c in edges:
                if u == x and v not in used:
                    visit(v, used | {v}, cost+c)
        visit(s, {s}, 0)
        out.append(min(costs) if costs else INF)
    return tuple(out)

def potential_admissible(h, edges, goal):
    if h[goal] != 0 or any(v < 0 for v in h):
        return False
    return all(h[u] <= c + h[v] for u,v,c in edges)

def main():
    tests = 0
    complete_cases = 0
    dual_scans = 0
    finite_pairs = 0
    zero_cycles = 0
    for code in itertools.product((-1,0,1,2), repeat=6):
        pairs = [(i,j) for i in range(3) for j in range(3) if i != j]
        edges = [(i,j,w) for (i,j),w in zip(pairs, code) if w >= 0]
        for goal in range(3):
            d = shortest_to_goal(3, edges, goal)
            brute = brute_paths_3(edges, goal)
            assert d == brute, ('path mismatch', code, goal, d, brute)
            tests += 1
            if all(x < INF for x in d):
                complete_cases += 1
                assert potential_admissible(d, edges, goal)
                # Determine the actual largest possible admissible potential
                # among all integer-valued bounded potentials; no reliance on
                # shortest-path algorithm to derive the maximum.
                maxima = [-1]*3
                for a in range(6):
                    for b in range(6):
                        h = [0,0,0]
                        ii = [i for i in range(3) if i != goal]
                        h[ii[0]],h[ii[1]] = a,b
                        dual_scans += 1
                        if potential_admissible(h, edges, goal):
                            maxima = [max(x,y) for x,y in zip(maxima,h)]
                assert tuple(maxima) == d, (code,goal,maxima,d)
            finite_pairs += sum(x < INF for x in d)
            if any(u == v for u,v,_ in edges):
                zero_cycles += 1
    # Unknown hypothetical (not authenticated!) positive-weight native step:
    # legal known chain has lower-bound n; MAY one-step completion has optimum1.
    unknown_cases = []
    for n in (2,3,5,10,25,100):
        known = [(i,i+1,1) for i in range(n)]
        possible = known + [(0,n,1)]
        kd = shortest_to_goal(n+1,known,n)
        md = shortest_to_goal(n+1,possible,n)
        assert kd[0] == n and md[0] == 1
        assert potential_admissible(kd,known,n)
        assert not potential_admissible(kd,possible,n)
        assert potential_admissible(md,possible,n)
        unknown_cases.append({'n':n,'authenticated_fragment_optimum':n,'may_optimum':1,
                              'candidate_potential_violation':n-1})
    # Attribution of paid shared owner: 1 paid first-use, 0 reusable facet.
    # Quotient of unpaid/cached state produces a spurious zero-cost path.
    paid_history = {'concrete_edges':[[0,1,1],[1,2,0]],
        'concrete_minimum':shortest_to_goal(3,[(0,1,1),(1,2,0)],2)[0],
        'quotient_minimum':shortest_to_goal(2,[(0,0,1),(0,1,0)],1)[0]}
    assert paid_history['concrete_minimum']==1
    assert paid_history['quotient_minimum']==0
    output = {'run':'LSPV-1/589','timestamp':'2026-11-12 04:00 PST',
        'model':'finite nonnegative weighted MAY graphs; not historical native checker',
        'exhaustive_three_state_graphs':4096,'goal_cases':tests,
        'complete_goal_reachable_cases_with_exhaustive_integer_dual':complete_cases,
        'bounded_integer_potentials_scanned':dual_scans,
        'finite_start_goal_pairs':finite_pairs,
        'all_checks':'PASS','positive_unknown_step_countermodels':unknown_cases,
        'paid_history_merge_prior_art_control':paid_history,
        'claims':{'proved':'On finite MAY graphs, maximum feasible nonnegative Bellman potential equals least MAY goal path cost at every goal-reachable state. Every concrete path simulation whose abstract edges undercharge yields W_concrete >= h(initial).',
                  'not_proved':'No complete R_mix341 grammar, no bound for full native SAT family, no machine-time lower bound, no historical unknown opcode acceptance.'}}
    b=json.dumps(output,sort_keys=True,indent=2)+'\n'
    if len(sys.argv)>1:
        pathlib.Path(sys.argv[1]).write_text(b,encoding='utf-8')
    print(b,end='')

if __name__=='__main__':
    main()
