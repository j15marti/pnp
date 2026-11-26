"""Extracted core from executed c01.py. Requires networkx.
F: list of (distinct-variable scope, set of distinct Boolean words).
Full native dispatcher, tests and raw inputs in companion archive.
"""
import networkx as nx

def eligibility(F):
    eligible={};inc={}
    for i,(P,R) in enumerate(F):
        for j,v in enumerate(P):
            inc.setdefault(v,set()).add(i)
            b=next((b for b in (0,1) if sum(w[j]==b for w in R)==2**(len(P)-1)),None)
            if b is not None:eligible[i,v]=b
    return eligible,inc

def autarky(F):
    """Greatest matching-autarkic factor set, including noneligible incidences."""
    eligible,inc=eligibility(F);C=set(range(len(F))); rounds=[]
    while C:
        B=nx.Graph();left=[('f',i) for i in sorted(C)];B.add_nodes_from(left)
        B.add_edges_from((('f',i),('v',v)) for i,v in eligible if i in C and inc[v]<=C)
        M=nx.bipartite.maximum_matching(B,top_nodes=left)
        roots=[f for f in left if f not in M]
        if not roots:
            a={M[f][1]:eligible[f[1],M[f][1]] for f in left}
            break
        D=nx.DiGraph();D.add_nodes_from(B)
        for f,v in B.edges:
            if f[0]!='f':f,v=v,f
            D.add_edge(f,v)
            if M.get(f)==v:D.add_edge(v,f)
        Z=set(roots)
        todo=list(roots)
        while todo:
            for u in D[todo.pop()]:
                if u not in Z:Z.add(u);todo.append(u)
        bad={i for tag,i in Z if tag=='f'}
        assert bad and bad<=C
        rounds.append({'candidate':len(C),'matching':len(M)//2,'removed':sorted(bad)})
        C-=bad
    else:a={}
    keep=[(P,R) for i,(P,R) in enumerate(F) if i not in C]
    assert not(set(a)&{v for P,R in keep for v in P})
    for i in C:
        P,R=F[i];assert any(v in a and (i,v) in eligible and eligible[i,v]==a[v] for v in P)
    return keep,a,{'removed':len(C),'core_factors':len(keep),'rounds':rounds,'matching_calls':len(rounds)+bool(C),'autarkic_ids':sorted(C)}
