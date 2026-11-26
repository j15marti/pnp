import itertools as it, networkx as nx
from p3ps03_audit import faces
base=[t for t in it.product(range(2),repeat=3) if t not in [(0,0,0),(1,1,1)]]
for b in [1,2,4,8,16,32,64]:
    T=[tuple(x+2*i for x in t) for i in range(b) for t in base]
    for i in range(b-1):
        u=tuple(x+2*i for x in (0,0,1));v=tuple(x+2*(i+1) for x in (0,1,0))
        T.remove(u);T.remove(v);T.extend([(v[0],u[1],u[2]),(u[0],v[1],v[2])])
    n=2*b
    I=nx.Graph();I.add_edges_from((t,(c,t[c])) for t in T for c in range(3))
    G=nx.Graph();G.add_nodes_from(T)
    for v in [(c,i) for c in range(3) for i in range(n)]:
        A=[t for t in T if t[v[0]]==v[1]];assert len(A)==3
        G.add_edges_from(it.combinations(A,2))
    assert nx.check_planarity(I)[0] and nx.is_connected(I)
    _,F=faces(G);U=set(T);k=0
    while U:
        f=max((set(f)&U for f in F),key=len);U-=f;k+=1
    W=[tuple(x+2*i for x in t) for i in range(b) for t in [(0,1,1),(1,0,0)]]
    assert set(W)<=set(T) and all(len(set(t[c] for t in W))==n for c in range(3))
    bad=set()
    for c,d in it.combinations(range(3),2):
        L={(c,i) for i in range(n)};R={(d,i) for i in range(n)}
        P=nx.Graph();P.add_nodes_from(L|R);P.add_edges_from(((c,t[c]),(d,t[d])) for t in T)
        M=nx.bipartite.maximum_matching(P,top_nodes=L);assert len(M)==2*n
        D=nx.DiGraph();D.add_nodes_from(P)
        D.add_edges_from((v,u) if M[u]==v else (u,v) for u in L for v in P[u])
        S={v:i for i,C in enumerate(nx.strongly_connected_components(D)) for v in C}
        for t in T:
            u,v=(c,t[c]),(d,t[d])
            if M[u]!=v and S[u]!=S[v]:bad.add(t)
    print(b,len(T),max(map(len,F)),k,len(bad))
