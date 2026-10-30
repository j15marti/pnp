#!/usr/bin/env python3
"""Finite signed-incidence graph witness-transport test. NetworkX VF2 is only
an experimental checker; polynomial guarantee uses Luks's bounded-degree GI.
"""
from pathlib import Path
import sys,random,json,time
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher,categorical_node_match
sys.path.insert(0,str(Path(__file__).resolve().parent))
from arc_linear22_projection_firewall import formula
from arc_mixed_projection_test import source_sat

def incidence(n,clauses):
    G=nx.Graph()
    for v in range(1,n+1):
        G.add_node(('v',v),kind='v')
        for sign in (1,-1):
            G.add_node(('p',v,sign),kind='p')
            G.add_edge(('v',v),('p',v,sign))
    for j,c in enumerate(clauses):
        G.add_node(('c',j),kind='c')
        for z in c:G.add_edge(('c',j),('p',abs(z),1 if z>0 else -1))
    assert max(dict(G.degree()).values())==3
    return G

def scramble(n,clauses,seed):
    rng=random.Random(seed)
    perm=list(range(1,n+1));rng.shuffle(perm)
    flips={i:rng.choice((-1,1)) for i in range(1,n+1)}
    out=[]
    for c in clauses:
        d=[(1 if z>0 else -1)*flips[abs(z)]*perm[abs(z)-1] for z in c]
        rng.shuffle(d);out.append(tuple(d))
    rng.shuffle(out)
    return out

def transport(n,clauses,changed):
    src=incidence(n,clauses);dst=incidence(n,changed)
    gm=GraphMatcher(src,dst,node_match=categorical_node_match('kind',''))
    t0=time.perf_counter()
    assert gm.is_isomorphic()
    mapping=gm.mapping
    # Original known satisfying assignment: A_i=1, B,C=0.
    k=n//3; witness=[1]*k+[0]*(2*k)
    transported=[None]*n
    for v in range(1,n+1):
        new=mapping[('v',v)][1]
        sign=mapping[('p',v,1)][2]
        assert mapping[('p',v,-1)]==('p',new,-sign)
        transported[new-1]=witness[v-1] if sign==1 else 1-witness[v-1]
    assert all(x is not None for x in transported)
    assert source_sat(changed,transported)
    return dict(nodes=src.number_of_nodes(),edges=src.number_of_edges(),max_degree=3,
                source_sat=True,transported_sat=True,seconds=round(time.perf_counter()-t0,5))

if __name__=='__main__':
    n,clauses=formula(7)
    out=[]
    for seed in (101,102,103,104,105,106):
        c=scramble(n,clauses,seed)
        out.append(dict(seed=seed,**transport(n,clauses,c)))
    print(json.dumps(out,indent=2))
    with open(str(Path(__file__).resolve().parent / 'arc_signed22_gi_control_results.json'),'w') as f:json.dump(out,f,indent=2)
