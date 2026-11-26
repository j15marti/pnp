import networkx as nx
from source_matching import honey
from cps07 import Solver,auth,verify

def acquire(T,n):
    s=Solver(T,n); S,C=s.acquire(); assert S is not None
    D=nx.DiGraph();D.add_nodes_from(S)
    for a in sorted(S):
        for O in s.owner:
            Q=O&C[a]
            if len(Q)==1:D.add_edge(a,next(iter(Q)))
    classes=sorted(tuple(sorted(A)) for A in nx.strongly_connected_components(D));idx={a:i for i,A in enumerate(classes) for a in A}
    rows=[tuple(sorted(idx[a] for a in O&S)) for O in s.owner]
    assert all(len(set(r))==len(r) for r in rows)
    rows=sorted(set(rows)); occ=[[] for A in classes]
    for j,R in enumerate(rows):
        for i in R:occ[i].append(j)
    return classes,rows,occ,s.matchings

def guarded(T,n,chart,deleted):
    classes,rows,occ,_=chart
    G=nx.Graph();G.add_nodes_from(range(len(rows)))
    for i,O in enumerate(occ):
        assert len(O) in (1,2)
        if set(classes[i])&deleted:continue
        u=O[0];v=O[1] if len(O)==2 else ('d',i)
        G.add_edge(u,v,weight=len(O),choice=i)
    M=nx.max_weight_matching(G);w=sum(G[u][v]['weight'] for u,v in M)
    if w!=len(rows):return 'NO',w
    ids=[a for u,v in M for a in classes[G[u][v]['choice']]]
    assert verify(T,n,ids) and not (set(ids)&deleted)
    return 'YES',w

if __name__=='__main__':
    for m,n in [(1,1),(2,2),(3,3),(4,4)]:
        H0,_=honey(m,n); M0=nx.max_weight_matching(H0,maxcardinality=True); drop=min(H0)
        partner=next(v if u==drop else u for u,v in M0 if drop in (u,v));p=H0[drop][partner]['phase']
        H,T=honey(m,n,drop);V=sorted(H);k=len(V);idx={u:i for i,u in enumerate(V)};auth(T,2*k)
        absent={6*idx[u]+2*h for u in H for h in range(3) if h not in {H[u][v]['phase'] for v in H[u]}}
        restore=6*idx[partner]+2*p;assert restore in absent
        chart=acquire(T,2*k);print(m,n,'parent',len(T),len(chart[0]),len(chart[1]),max(map(len,chart[2])),chart[3],flush=True)
        if max(map(len,chart[2]))<=2:
            a=guarded(T,2*k,chart,absent-{restore});b=guarded(T,2*k,chart,absent);assert a[0]=='YES' and b[0]=='NO';print('SAT/UNSAT',len(T)-len(absent)+1,len(T)-len(absent),a,b,flush=True)
