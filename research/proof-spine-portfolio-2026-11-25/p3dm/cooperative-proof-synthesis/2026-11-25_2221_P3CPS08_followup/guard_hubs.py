import itertools as it, networkx as nx
from source_matching import honey
from cps07 import Solver, auth, verify
from reuse_parent import acquire

def solve(T,n,cap=12):
    auth(T,n)
    s=Solver(T,n); S,C=s.acquire()
    if S is None:return {'status':'NO','stage':'closure','matching_calls':s.matchings}
    D=nx.DiGraph();D.add_nodes_from(S)
    for a in sorted(S):
        for O in s.owner:
            Q=O&C[a]
            if len(Q)==1:D.add_edge(a,next(iter(Q)))
    classes=sorted(tuple(sorted(A)) for A in nx.strongly_connected_components(D));idx={a:i for i,A in enumerate(classes) for a in A}
    raw=[tuple(sorted(idx[a] for a in O&S)) for O in s.owner];invalid={i for R in raw for i in R if R.count(i)>1}
    rows=sorted({tuple(i for i in R if i not in invalid) for R in raw})
    if any(not R for R in rows):return {'status':'NO','stage':'duplicate pin'}
    occ=[set() for A in classes]
    for j,R in enumerate(rows):
        for i in R:occ[i].add(j)
    hubs=[i for i,O in enumerate(occ) if len(O)>2];h=len(hubs);stats={'hubs':h,'rows':len(rows),'classes':len(classes),'matching_calls':s.matchings,'branches':0,'matching_queries':0}
    if h>cap:return dict(stats,status='OPEN')
    for val in it.product((0,1),repeat=h):
        stats['branches']+=1;chosen=[i for i,x in zip(hubs,val) if x];cover=set()
        for i in chosen:
            if cover&occ[i]:break
            cover|=occ[i]
        else:
            active=set(range(len(rows)))-cover;G=nx.Graph();G.add_nodes_from(active)
            for i,O in enumerate(occ):
                if i in hubs or not O or O&cover:continue
                u=min(O);v=max(O) if len(O)==2 else ('d',i)
                G.add_edge(u,v,weight=len(O),choice=i)
            stats['matching_queries']+=1; M=nx.max_weight_matching(G);w=sum(G[u][v]['weight'] for u,v in M)
            if w==len(active):
                ids=[a for i in chosen+[G[u][v]['choice'] for u,v in M] for a in classes[i]]
                assert verify(T,n,ids);return dict(stats,status='YES')
    return dict(stats,status='NO')

if __name__=='__main__':
    for m,n in [(1,1),(2,2),(3,3),(4,4)]:
        H0,_=honey(m,n);M0=nx.max_weight_matching(H0,maxcardinality=True);drop=min(H0);partner=next(v if u==drop else u for u,v in M0 if drop in (u,v));p=H0[drop][partner]['phase'];H,T=honey(m,n,drop);V=sorted(H);k=len(V);idx={u:i for i,u in enumerate(V)};absent={6*idx[u]+2*h for u in H for h in range(3) if h not in {H[u][v]['phase'] for v in H[u]}};restore=6*idx[partner]+2*p
        A=[t for i,t in enumerate(T) if i not in absent-{restore}];B=[t for i,t in enumerate(T) if i not in absent]
        a,b=solve(A,2*k),solve(B,2*k);print(len(A),len(B),a,b,flush=True);assert a['status']=='YES' and b['status']=='NO'
