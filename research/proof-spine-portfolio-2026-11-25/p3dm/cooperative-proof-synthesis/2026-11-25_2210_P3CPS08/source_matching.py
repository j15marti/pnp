# Independent source-equality matching lane; requires cps07.py and audit.py.
import itertools as I, json
import networkx as nx
from audit import Solver, auth, verify, run

def honey(m,n,drop=None):
    H=nx.hexagonal_lattice_graph(m,n)
    if drop is not None:H.remove_node(drop)
    V=sorted(H);idx={u:i for i,u in enumerate(V)}
    T=[list(2*i+x for x in t) for i in range(len(V)) for t in [(0,0,0),(1,1,1),(0,0,1),(1,1,0),(0,1,0),(1,0,1)]]
    for u,v in H.edges():
        x,y=H.nodes[u]['pos'];a,b=H.nodes[v]['pos'];dx,dy=a-x,b-y
        if abs(dy)<1e-6:phase,port,c=1,2,2
        elif dx*dy>0:phase,port,c=0,1,1
        else:phase,port,c=2,4,1
        r,s=6*idx[u]+port,6*idx[v]+port;T[r][c],T[s][c]=T[s][c],T[r][c]
        H[u][v]['phase']=phase;H[u][v]['color']=c
    for c in (1,2):
        Q=nx.Graph();Q.add_nodes_from(H);Q.add_edges_from((u,v) for u,v in H.edges() if H[u][v]['color']==c);assert nx.is_forest(Q)
    return H,list(map(tuple,T))

def source_matching(T,n):
    auth(T,n);s=Solver(T,n);initial=None
    while True:
        S,C=s.acquire(initial)
        if S is None:return ['NO',s.matchings]
        D=nx.DiGraph();D.add_nodes_from(sorted(S))
        for a in sorted(S):
            for O in s.owner:
                Q=O&C[a]
                if len(Q)==1:D.add_edge(a,next(iter(Q)))
        classes=sorted(tuple(sorted(A)) for A in nx.strongly_connected_components(D));idx={a:i for i,A in enumerate(classes) for a in A}
        rows=[tuple(sorted(idx[a] for a in O&S)) for O in s.owner]
        invalid={i for R in rows for i in R if R.count(i)>1}
        if invalid:
            initial=S-{a for i in invalid for a in classes[i]};continue
        rows=sorted(set(rows));occ=[[] for A in classes]
        for j,R in enumerate(rows):
            for i in R:occ[i].append(j)
        big=sum(len(O)>2 for O in occ)
        if big:return ['OPEN',s.matchings,len(classes),len(rows),big]
        G=nx.Graph();G.add_nodes_from(range(len(rows)))
        for i,O in enumerate(occ):
            assert len(O) in (1,2)
            u=O[0];v=O[1] if len(O)==2 else ('dummy',i)
            G.add_edge(u,v,weight=len(O),choice=i)
        M=nx.max_weight_matching(G);weight=sum(G[u][v]['weight'] for u,v in M)
        if weight!=len(rows):return ['NO',s.matchings,len(classes),len(rows),big]
        W=[a for u,v in M for a in classes[G[u][v]['choice']]];assert verify(T,n,W)
        return ['YES',s.matchings,len(classes),len(rows),big]

if __name__=='__main__':
    import sys
    mode=sys.argv[1] if len(sys.argv)>1 else 'small'
    out={}
    for m,n in ([(6,6)] if mode=='large' else [(1,1),(1,2),(2,2),(3,3),(4,4)] if mode=='small' else []):
        H,T=honey(m,n);k=len(H);G=auth(T,2*k)
        for p in range(3):assert verify(T,2*k,[6*i+2*p+j for i in range(k) for j in (0,1)])
        a=source_matching(T,2*k);assert a[0]=='YES'
        if k<=48:
            r=run(T,2*k);q=[[L['wide_roots'],L['forest'][0],L['matching'][0]] for L in r['lanes']];assert all(x[1:]==['OPEN','OPEN'] for x in q)
            extra=[r['matching_calls'],q]
        else:extra=[None,None]
        out[str((m,n))]=[k,len(T),nx.edge_connectivity(G),a,*extra];print(m,n,out[str((m,n))],flush=True)
    out['neighbors']={}
    for m,n in ([(1,1),(2,2),(3,3),(4,4)] if mode=='neighbors' else []):
        H0,_=honey(m,n);M0=nx.max_weight_matching(H0,maxcardinality=True);assert len(M0)*2==len(H0)
        drop=min(H0);partner=next(v if u==drop else u for u,v in M0 if drop in (u,v));p=H0[drop][partner]['phase']
        H,T=honey(m,n,drop);V=sorted(H);k=len(V);idx={u:i for i,u in enumerate(V)}
        absent={6*idx[u]+2*h for u in H for h in range(3) if h not in {H[u][v]['phase'] for v in H[u]}}
        restore=6*idx[partner]+2*p;assert restore in absent
        A=[t for i,t in enumerate(T) if i not in absent-{restore}];B=[t for i,t in enumerate(T) if i not in absent]
        phase={partner:p}
        for u,v in M0:
            if drop not in (u,v):phase[u]=phase[v]=H[u][v]['phase']
        W=[6*idx[u]+2*phase[u]+j for u in H for j in (0,1)];assert verify(T,2*k,W) and not set(W)&(absent-{restore})
        a,b=source_matching(A,2*k),source_matching(B,2*k);assert a[0] in ('YES','OPEN') and b[0]=='NO';print('neighbor',m,n,a,b,flush=True)
        out['neighbors'][str((m,n))]=[len(A),len(B),a,b]
    print(json.dumps(out))
