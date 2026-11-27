from audit29 import *

def gf2(rows):
    bas={}
    for x,b in rows:
        while x:
            p=x.bit_length()-1
            if p in bas:
                u,v=bas[p];x^=u;b^=v
            else:bas[p]=(x,b);break
        if not x and b:return False,len(bas)
    return True,len(bas)

def face_sign(G):
    ok,E=nx.check_planarity(G);assert ok
    visited=set();F=[]
    for u,v in E.edges():
        if (u,v) not in visited:F.append(E.traverse_face(u,v,visited))
    # dual forest, one arbitrary face root per connected component; bridge occurs twice in a face
    sides={};rhs=[]
    for k,w in enumerate(F):
        assert len(w)%2==0;rhs.append((len(w)//2+1)%2)
        for u,v in zip(w,w[1:]+w[:1]):sides.setdefault(tuple(sorted((u,v))),[]).append(k)
    D=nx.Graph();D.add_nodes_from(range(len(F)))
    for e,ij in sides.items():
        assert len(ij)==2
        i,j=ij
        if i!=j:D.add_edge(i,j,edge=e)
    neg=set()
    for C in nx.connected_components(D):
        edges=list(nx.bfs_edges(D,min(C)))
        for u,v in reversed(edges):
            if rhs[v]:neg.add(D[u][v]['edge']);rhs[u]^=1;rhs[v]=0
        assert rhs[min(C)]==0 # every component has an even number of vertices (matching exists)
    for w in F:assert sum(tuple(sorted((u,v))) in neg for u,v in zip(w,w[1:]+w[:1]))%2==(len(w)//2+1)%2
    return neg

def syndrome(V,T,live):
    rows=[(sum(1<<i for i in live if u in T[i]),1) for shore in V for u in shore]
    coeff=0;btotal=0;counts=[];constants=[]
    for a,b in PAIRS:
        G=project(V,T,live,a,b);M=matching(G,V,a,b);assert M
        neg=face_sign(G);k=sign(M,V,a,b)^ (sum(tuple(sorted((u,M[u]))) in neg for u in V[a])%2)
        coeff^=sum(1<<i for i in live if tuple(sorted((T[i][a],T[i][b]))) in neg);btotal^=k;counts.append(len(neg));constants.append(k)
    return dict(base=gf2(rows),augmented=gf2(rows+[(coeff,btotal)]),negative_edges=counts,constants=constants,sign_row_weight=coeff.bit_count(),rhs=btotal)
if __name__=='__main__':
    for s in [9,15,21,27,33,6]:
        V,T=grid(s);live,_,no=closure(V,T);assert not no
        r=syndrome(V,T,live);print(json.dumps(dict(s=s,**r)))
    # Hostile unsigned sign control: K2,2 has matchings with opposite signs, repaired by signing one edge.
    G=nx.complete_bipartite_graph(2,2);neg=face_sign(G);assert len(neg)==1
    assert all((perm_parity(p)+sum(tuple(sorted((i,2+j))) in neg for i,j in enumerate(p)))%2==1 if (0,2) in neg or (1,3) in neg else (perm_parity(p)+sum(tuple(sorted((i,2+j))) in neg for i,j in enumerate(p)))%2==0 for p in itertools.permutations(range(2)))
    # explicit even 6x6 cover, not a research lane
    V,T=grid(6);idx={frozenset(t):i for i,t in enumerate(T)};cover=[]
    for i in range(0,6,2):
        for j in range(0,6,3):
            cover.extend([idx[frozenset(((i,j),(i+1,j),(i,j+1)))],idx[frozenset(((i+1,j+2),(i+1,j+1),(i,j+2)))]] )
    assert len({u for i in cover for u in T[i]})==36
    print(json.dumps({'controls':'K2,2 mixed unsigned signs; exact even-grid cover verified','cover_ids':cover}))
