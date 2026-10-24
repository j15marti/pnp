#!/usr/bin/env python3
"""DEGREE-MATCH-LADDER132, reproducible restricted positive exact-one SAT tests.
Requires networkx>=3. Checks are finite and do NOT establish unrestricted SAT bounds.
"""
import collections
import hashlib
import itertools
import json
import random
from pathlib import Path
import networkx as nx

SEED = 202610240800
RNG = random.Random(SEED)
CHECKS = 0

def check(p, message='check failed'):
    global CHECKS
    CHECKS += 1
    if not p:
        raise AssertionError(message)

def valid_source(clauses):
    return all(len(c)==3 and len(set(c))==3 and min(c)>=0 for c in clauses)

def holds(clauses, true_vars):
    true_vars = set(true_vars)
    return all(sum(v in true_vars for v in c) == 1 for c in clauses)

def brute(clauses):
    vs = sorted({v for c in clauses for v in c})
    for b in range(1 << len(vs)):
        trues = {v for j, v in enumerate(vs) if (b >> j) & 1}
        if holds(clauses, trues):
            return trues
    return None

def dpll_exact1(clauses):
    """Independent exact-one DPLL with deterministic unit-cardinality propagation."""
    allvars = sorted({v for c in clauses for v in c})
    def go(values):
        values = dict(values)
        changed = True
        while changed:
            changed = False
            for c in clauses:
                one = sum(values.get(v, -1)==1 for v in c)
                unknown = [v for v in c if v not in values]
                if one>1 or (one==0 and not unknown):
                    return None
                need = 0 if one == 1 else (1 if len(unknown)==1 else None)
                if need is not None:
                    for v in unknown:
                        if v in values and values[v]!=need:
                            return None
                        if v not in values:
                            values[v]=need
                            changed = True
        if all(v in values for v in allvars):
            return {v for v in allvars if values[v] == 1}
        remaining = collections.Counter(v for c in clauses for v in c if v not in values)
        v = max(remaining, key=lambda x:(remaining[x],-x))
        for bit in (1,0):
            answer=go({**values,v:bit})
            if answer is not None:
                return answer
        return None
    return go({})

def degree(clauses):
    return collections.Counter(x for c in clauses for x in c)

def matching_core(clauses):
    """Solve EXACTLY-ONE clauses with each remaining variable of degree <=2.
    Returns one exact assignment (true-variable set), or None.
    Maximum-weight matching is Edmonds-type polynomial matching, via networkx.
    """
    d = degree(clauses)
    if max(d.values(), default=0) > 2:
        raise ValueError('source degree exceeds two')
    g = nx.Graph()
    g.add_nodes_from(range(len(clauses)))
    occ = collections.defaultdict(list)
    for i, c in enumerate(clauses):
        for x in c:
            occ[x].append(i)
    for x, where in occ.items():
        if len(where) == 1:
            a = where[0]
            g.add_edge(a, ('leaf', x), weight=1, source_var=x)
        elif len(where) == 2:
            a, b = where
            if not g.has_edge(a, b):
                g.add_edge(a, b, weight=2, source_var=x)
        else:
            raise AssertionError('unexpected occurrence count')
    matching = nx.max_weight_matching(g, weight='weight')
    covered = sum(g.edges[u, v]['weight'] for u, v in matching)
    if covered != len(clauses):
        return None
    out = {g.edges[u, v]['source_var'] for u, v in matching}
    check(holds(clauses, out), 'wrong reconstructed matching witness')
    return out

def adaptive_degree_solver(clauses):
    """FPT algorithm 2^k poly(N), k=#source vars with degree >=3."""
    check(valid_source(clauses), 'invalid source grammar')
    high = sorted(x for x, count in degree(clauses).items() if count > 2)
    counts = {'k': len(high), 'branches': 0, 'matching_calls': 0}
    for bits in range(1 << len(high)):
        counts['branches'] += 1
        high_true = {v for j, v in enumerate(high) if (bits >> j) & 1}
        high_set = set(high)
        forced_false = set()
        todo = []
        viable = True
        for c in clauses:
            ntrue = sum(v in high_true for v in c)
            if ntrue > 1:
                viable = False
                break
            remaining = [v for v in c if v not in high_set]
            if ntrue == 1:
                forced_false.update(remaining)
            else:
                todo.append(remaining)
        if not viable:
            continue
        residual = [tuple(v for v in c if v not in forced_false) for c in todo]
        if any(not c for c in residual):
            continue
        counts['matching_calls'] += 1
        witness = matching_core(residual)
        if witness is not None:
            sol = high_true | witness
            check(holds(clauses, sol), 'false SAT result')
            return sol, counts
    return None, counts

def clauses_from_cubic_graph(g):
    check(nx.is_connected(g), 'source graph must be connected')
    check(all(deg==3 for _, deg in g.degree()), 'graph must be cubic')
    ans = collections.defaultdict(list)
    for i, (u, v) in enumerate(sorted(tuple(sorted(e)) for e in g.edges())):
        ans[u].append(i)
        ans[v].append(i)
    return [tuple(ans[v]) for v in sorted(g.nodes())]

def balloon_three_bridge():
    # Known prior project cubic bridge obstruction, repurposed here for E-SAT.
    g = nx.Graph()
    g.add_node(0)
    for k in range(3):
        offset = 1 + 5*k
        a, b, c, d, z = range(offset, offset+5)
        for u, v in itertools.combinations((a,b,c,d),2):
            if (u,v)!=(a,b):
                g.add_edge(u,v)
        g.add_edges_from([(a,z),(z,b),(0,z)])
    return g

def compile_proper3cnf(clauses):
    """Exactly-one source E(a,b,c) => six proper signed 3-CNF clauses and one aux."""
    fresh = max((x for c in clauses for x in c), default=-1)+1
    out = []
    for a,b,c in clauses:
        x,y,z = a+1,b+1,c+1
        aux = fresh+1
        fresh += 1
        for vals in ((0,0,0),(0,1,1),(1,0,1),(1,1,0)):
            out.append(tuple((v if bit==0 else -v) for v, bit in zip((x,y,z), vals)))
        out.extend([(-x,-y,aux),(-x,-y,-aux)])
    check(all(len(c)==3 and len({abs(v) for v in c})==3 for c in out))
    check(len(out)==6*len(clauses))
    return out

def cnf_exists_for_source_assignment(source_clause, source_assignment):
    src = tuple(bool((source_assignment >> j)&1) for j in range(3))
    c = compile_proper3cnf([source_clause])
    aux_id = max(abs(v) for cl in c for v in cl)
    original = sorted(source_clause)
    for aux in (False, True):
        amap = {v+1: src[j] for j,v in enumerate(source_clause)}
        amap[aux_id] = aux
        if all(any((amap[abs(lit)] == (lit>0)) for lit in cl) for cl in c):
            return True
    return False

def random_degree3(n):
    for _ in range(1000):
        perms=[RNG.sample(range(n),n) for _ in range(3)]
        c=[tuple(sorted(perms[j][i] for j in range(3))) for i in range(n)]
        if valid_source(c) and len(set(c))==n:
            check(set(degree(c).values())=={3})
            return c
    raise RuntimeError('failed to draw regular instance')

def main():
    stats={'test':'DEGREE-MATCH-LADDER132','seed':SEED,'networkx':nx.__version__,'sources':0,
           'SAT':0,'UNSAT':0,'k0_cases':0,'kpositive_cases':0,'max_branches':0,
           'matched_cubic_order16':[], 'degree3_opposite_examples':{},
           'proper3cnf_clause_check':0}
    sat16 = clauses_from_cubic_graph(nx.circular_ladder_graph(8))
    unsat16 = clauses_from_cubic_graph(balloon_three_bridge())
    check(len(sat16)==len(unsat16)==16)
    check(len(degree(sat16))==len(degree(unsat16))==24)
    for label,clauses,truth in [('prism',sat16,True),('three_bridge',unsat16,False)]:
        witness,counts=adaptive_degree_solver(clauses)
        check((witness is not None)==truth)
        check((dpll_exact1(clauses) is not None)==truth)
        check(counts['k']==0 and counts['branches']==1)
        check(len(compile_proper3cnf(clauses))==96)
        stats['matched_cubic_order16'].append({'name':label,'clauses':16,'variables':24,
            'cycle_rank':24-16+1,'sat':truth,'proper_3cnf_clauses':96})
        stats['sources']+=1;stats['SAT' if truth else 'UNSAT']+=1;stats['k0_cases']+=1
    deg3_sat=[(0,3,5),(0,1,2),(1,3,5),(2,4,5),(1,2,4),(0,3,4)]
    deg3_unsat=[(0,1,5),(1,2,3),(3,4,5),(0,2,3),(2,4,5),(0,1,4)]
    for name,clauses,truth in [('cubic_sat',deg3_sat,True),('cubic_unsat',deg3_unsat,False)]:
        w,c=adaptive_degree_solver(clauses)
        check((w is not None)==truth)
        check((dpll_exact1(clauses) is not None)==truth)
        check(c['k']==6)
        stats['degree3_opposite_examples'][name]={'source_n':6,'source_m':6,'SAT':truth,'clauses':clauses}
        stats['sources']+=1;stats['SAT' if truth else 'UNSAT']+=1;stats['kpositive_cases']+=1
    # Exhaust the 8 source triples on three distinct variables for the gadget relation.
    for v in range(8):
        eq = sum((v>>j)&1 for j in range(3))==1
        out=cnf_exists_for_source_assignment((0,1,2),v)
        check(eq==out, 'proper CNF gadget mismatch')
        stats['proper3cnf_clause_check']+=1
    # Random genuinely different k=0 positive E instances (varying one/two occurrences).
    for m in (4,6,8,10,12,14):
        for j in range(22):
            g=nx.Graph();g.add_nodes_from(range(m))
            pairs=list(itertools.combinations(range(m),2));RNG.shuffle(pairs)
            for u,v in pairs:
                if g.degree(u)<3 and g.degree(v)<3 and RNG.random()<0.5:g.add_edge(u,v)
            c=[[] for _ in range(m)]
            z=0
            for u,v in g.edges():c[u].append(z);c[v].append(z);z+=1
            for i in range(m):
                while len(c[i])<3:c[i].append(z);z+=1
            clauses=[tuple(x) for x in c]
            w,counts=adaptive_degree_solver(clauses)
            check((w is not None)==(brute(clauses) is not None))
            check(counts['k']==0)
            stats['sources']+=1;stats['SAT' if w is not None else 'UNSAT']+=1;stats['k0_cases']+=1
    # General 3-regular positive 1-in-3 source (independent exhaustive controls).
    for n,tries in ((6,100),(9,60)):
        for _ in range(tries):
            c=random_degree3(n)
            w,counts=adaptive_degree_solver(c)
            check((w is not None)==(brute(c) is not None))
            check(counts['k']==n)
            stats['sources']+=1;stats['SAT' if w is not None else 'UNSAT']+=1;stats['kpositive_cases']+=1
            stats['max_branches']=max(stats['max_branches'],counts['branches'])
    stats['checks']=CHECKS
    stats['status']='COMPUTATIONAL PASS'
    stats['limits']='networkx matching proves tests only; proof uses Edmonds and Moore-Robson; no unrestricted SAT runtime/FLMV transfer'
    stats['code_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    dest=Path(__file__).with_name('degree_ladder132_results.json')
    dest.write_text(json.dumps(stats,sort_keys=True,indent=2)+'\n')
    print(json.dumps(stats,sort_keys=True,indent=2))

if __name__=='__main__':
    main()
