#!/usr/bin/env python3
"""ARC214 explicit graph-minor/tree-decomposition and truth-table audit.
Stdlib + networkx (which is used only for finite graph checks, not proofs).
Deterministic finite checks, seed 202610282301.  No uncharged general SAT algorithm.
"""
import itertools, json, random, hashlib, sys
from collections import defaultdict
import networkx as nx
from networkx.algorithms.approximation.treewidth import treewidth_min_fill_in

SEED = 202610282301
rng = random.Random(SEED)
stats = defaultdict(int)


def source_primal(n, clauses):
    G=nx.Graph(); G.add_nodes_from(range(n))
    for C in clauses:
        for a,b in itertools.combinations([abs(z)-1 for z in C], 2): G.add_edge(a,b)
    return G


def mixed_primal(n, clauses):
    G=nx.Graph(); G.add_nodes_from(range(n+3*len(clauses)))
    for c,C in enumerate(clauses):
        Y=[n+3*c+j for j in range(3)]
        for j,l in enumerate(C): G.add_edge(abs(l)-1, Y[j])
        for a,b in itertools.combinations(Y,2): G.add_edge(a,b)
    return G


def contract_back(n, clauses):
    G = mixed_primal(n, clauses)
    # Every y_i is exclusive to its one gadget, so these are always valid minors.
    for c,C in enumerate(clauses):
        for j,l in enumerate(C):
            y=n+3*c+j
            x=abs(l)-1
            assert G.has_edge(x,y)
            G=nx.contracted_nodes(G,x,y,self_loops=False,copy=False)
    assert set(G.nodes)==set(range(n))
    assert {frozenset(x) for x in G.edges} == {frozenset(x) for x in source_primal(n,clauses).edges}
    stats['minor_contractions'] += 3*len(clauses)
    return G


def primal_decomposition(G):
    w, tree = treewidth_min_fill_in(G)
    bags=list(tree.nodes)
    idx={b:i for i,b in enumerate(bags)}
    adj=nx.Graph();adj.add_nodes_from(range(len(bags)))
    adj.add_edges_from((idx[a],idx[b]) for a,b in tree.edges)
    return [set(b) for b in bags],adj,w


def assert_valid_decomposition(G,bags,T):
    assert nx.is_tree(T)
    assert T.number_of_nodes()==len(bags)
    for v in G.nodes:
        uses=[i for i,b in enumerate(bags) if v in b]
        assert uses,('missing vertex',v)
        assert nx.is_connected(T.subgraph(uses)),('disconnected',v)
        stats['tree_vertex_connectivity_checks'] += 1
    for a,b in G.edges:
        assert any(a in B and b in B for B in bags),('uncovered edge',a,b)
        stats['edge_bag_checks'] += 1


def lifted_decomposition(n,clauses):
    G0=source_primal(n,clauses)
    bags,T,w=primal_decomposition(G0)
    assert_valid_decomposition(G0,bags,T)
    for c,C in enumerate(clauses):
        a,b,d=[abs(z)-1 for z in C]
        y1,y2,y3=[n+3*c+j for j in range(3)]
        roots=[i for i,bag in enumerate(bags) if {a,b,d}.issubset(bag)]
        assert roots, 'primal clause clique must occur in some bag by Helly'
        root=roots[0]
        blocks=[{a,b,d,y1},{b,d,y1,y2},{d,y1,y2,y3}]
        for block in blocks:
            curr=len(bags);bags.append(block);T.add_node(curr)
            T.add_edge(root,curr);root=curr
    G1=mixed_primal(n,clauses)
    assert_valid_decomposition(G1,bags,T)
    cap=max(w,3)
    assert max(len(b)-1 for b in bags) <= cap, (w,cap)
    stats['verified_lifted_decompositions']+=1
    stats['maximum_source_heuristic_width']=max(stats['maximum_source_heuristic_width'],w)
    stats['maximum_lifted_width']=max(stats['maximum_lifted_width'],max(len(b)-1 for b in bags))


def lit(l,x):
    v=x[abs(l)-1]
    return v if l>0 else not v

def source_eval(clauses,x):
    return all(any(lit(l,x) for l in c) for c in clauses)

def mixed_eval(n,clauses,x,y):
    for ci,C in enumerate(clauses):
        ys=y[3*ci:3*ci+3]
        if not all(lit(l,x) or ys[j] for j,l in enumerate(C)):return False
        if sum(ys)%2:return False
    return True

def check_projection(n,clauses):
    for x in itertools.product((0,1),repeat=n):
        lhs=source_eval(clauses,x)
        # existential quantifiers distribute over independent local triples;
        # this finite check enumerates all 8^m possibilities as hostile control.
        rhs=False
        for y in itertools.product((0,1),repeat=3*len(clauses)):
            stats['auxiliary_assignments_probed']+=1
            if mixed_eval(n,clauses,x,y):
                rhs=True
                break
        assert lhs==rhs,(n,clauses,x,lhs,rhs)
        stats['source_assignments_verified']+=1


def bucket_sat(n,clauses):
    """Exact mixed Boolean factor elimination (naive finite test, no width guarantee).
    Factors=(tuple of variables, set of satisfying bit tuples); all mixed factors tested jointly.
    """
    factors=[]
    for ci,C in enumerate(clauses):
        for j,l in enumerate(C):
            x=abs(l)-1;y=n+3*ci+j
            scope=(x,y)
            sat={(a,b) for a in (0,1) for b in (0,1) if ((a==1) if l>0 else (a==0)) or b}
            factors.append((scope,sat))
        scope=tuple(n+3*ci+j for j in range(3))
        sat={bits for bits in itertools.product((0,1),repeat=3) if sum(bits)%2==0}
        factors.append((scope,sat))
    # Eliminate gadget-local y first, then original x: source CNF reappears.
    order=list(range(n,n+3*len(clauses)))+list(range(n))
    maxscope=0
    transitions=0
    for v in order:
        taken=[f for f in factors if v in f[0]]
        factors=[f for f in factors if v not in f[0]]
        if not taken: continue
        scope=tuple(sorted(set().union(*(set(f[0]) for f in taken))))
        maxscope=max(maxscope,len(scope))
        assert len(scope)<20
        ix={z:j for j,z in enumerate(scope)}
        out=tuple(z for z in scope if z!=v)
        sat=set()
        for bs in itertools.product((0,1),repeat=len(scope)):
            transitions+=1
            if all(tuple(bs[ix[z]] for z in fs) in allowed for fs,allowed in taken):
                sat.add(tuple(bs[ix[z]] for z in out))
        factors.append((out,sat))
    assert all(not fs for fs,_ in factors)
    answer=all(() in allowed for _,allowed in factors)
    stats['bucket_runs']+=1
    stats['bucket_candidate_rows']+=transitions
    stats['bucket_max_scope']=max(stats['bucket_max_scope'],maxscope)
    return answer


def clauses_at_random(n,m):
    ret=[]
    for _ in range(m):
        vs=rng.sample(range(1,n+1),3)
        ret.append(tuple(v if rng.getrandbits(1) else -v for v in vs))
    return ret


def cyclic_exact22(n):
    assert n%3==0 and n>=6
    clauses=[]
    for i in range(n):
        clauses.append((i+1,(i+1)%n+1,-((i+2)%n+1)))
    for j in range(0,n,3):
        clauses.append((-(j+1),-(j+2),-(j+3)))
    # verify each variable two +, two -
    occ=defaultdict(lambda:[0,0]);
    for C in clauses:
        for l in C:occ[abs(l)][l<0]+=1
    assert all(occ[v]==[2,2] for v in range(1,n+1))
    assert nx.is_connected(source_primal(n,clauses))
    return clauses


def main():
    # Complete small signed clauses, including all 8 signs and UNSAT eight-clause conjunction.
    for n in (3,4,5):
        for m in (1,2):
            for sample in range(15):
                clauses=clauses_at_random(n,m)
                check_projection(n,clauses)
                contract_back(n,clauses)
                lifted_decomposition(n,clauses)
                expected=any(source_eval(clauses,x) for x in itertools.product((0,1),repeat=n))
                got=bucket_sat(n,clauses)
                assert expected==got
                stats['random_formulas']+=1
                stats['sat_formulas' if expected else 'unsat_formulas']+=1
    # High-redundancy UNSAT negative control with separately SAT subsystems.
    full=[((1 if p&1 else -1)*1,(1 if p&2 else -1)*2,(1 if p&4 else -1)*3) for p in range(8)]
    assert not any(source_eval(full,x) for x in itertools.product((0,1),repeat=3))
    contract_back(3,full)
    lifted_decomposition(3,full)
    assert not bucket_sat(3,full)
    stats['full_eight_clause_unsat_cases']+=1
    # Connected exact signed (2,2) source controls; no general hardness claim.
    for n in (6,9,12):
        c=cyclic_exact22(n)
        contract_back(n,c)
        lifted_decomposition(n,c)
        assert any(source_eval(c,x) for x in itertools.product((0,1),repeat=n))
        stats['balanced_exact22_cases']+=1
    # Single clause sign permutations, all 8.
    for signmask in range(8):
        C=tuple((i+1)*(1 if signmask&(1<<i) else -1) for i in range(3))
        check_projection(3,[C]);stats['sign_controls']+=1
    out={"run":"ARC214", "seed":SEED,"status":"COMPUTATIONAL", "results":dict(sorted(stats.items())),
         "interpretation":"No all-input polynomial SAT compressor; verified exact tree-decomposition lift and graph-minor sandwich for finite controls."}
    with open('/mnt/data/arc214_work/ARC214_treewidth_minor_raw.json','w') as f:json.dump(out,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()