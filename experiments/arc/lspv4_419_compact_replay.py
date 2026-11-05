#!/usr/bin/env python3
"""Compact independent check of source-ID matching cofactors. Requires networkx.
Not a historical R_mix341 verifier or a FLMV native-machine benchmark.
"""
import networkx as nx
from itertools import product

def check(name, graph, odd):
    G=nx.convert_node_labels_to_integers(graph, ordering='sorted')
    H=G.number_of_nodes()
    E=sorted(tuple(sorted(e)) for e in G.edges())
    assert len(E)*2==3*H
    M=[]; used=set()
    for i,(u,v) in enumerate(E):
        if u not in used and v not in used:
            M.append(i);used.update((u,v))
    assert len(M)*2==H  # these four named controls have perfect matchings
    chi=[int(odd)]+[0]*(H-1)
    clauses=[]
    for v in range(H):
        ids=[i for i,(a,b) in enumerate(E) if v in (a,b)]
        assert len(ids)==3
        for bits in product((0,1),repeat=3):
            if sum(bits)%2 != chi[v]:
                clauses.append(tuple((i+1 if b==0 else -i-1) for i,b in zip(ids,bits)))
    assert len(clauses)==4*H
    seen=set(); sat_branches=0
    for values in product((0,1),repeat=len(M)):
        rho=dict(zip(M,values)); child=[]
        for j,c in enumerate(clauses):
            if any(rho[abs(l)-1]==int(l>0) for l in c if abs(l)-1 in rho): continue
            child.append((j+1,tuple(l for l in c if abs(l)-1 not in rho)))
        assert len(child)==2*H and all(len(c)==2 for _,c in child)
        seen.add(tuple(child))
        # Independent linear-system SAT test on unassigned original edges.
        piv={}; consistent=True
        for v in range(H):
            mask=0;rhs=chi[v]
            for i,(a,b) in enumerate(E):
                if v in (a,b):
                    if i in rho:rhs^=rho[i]
                    else:mask^=1<<i
            while mask:
                j=mask.bit_length()-1
                if j not in piv:piv[j]=(mask,rhs);break
                x,r=piv[j];mask^=x;rhs^=r
            if mask==0 and rhs:consistent=False;break
        if consistent:sat_branches+=1
    assert len(seen)==2**len(M)
    assert sat_branches==0 if odd else sat_branches>=1
    return dict(graph=name,odd=odd,H=H,k=len(M),distinct=len(seen),
                residual_clauses=2*H,satisfiable_contexts=sat_branches)

if __name__=='__main__':
    for name,G in [('K4',nx.complete_graph(4)),('Cube',nx.cubical_graph()),
                   ('Petersen',nx.petersen_graph()),('Heawood',nx.heawood_graph())]:
        for odd in [False,True]:print(check(name,G,odd))
