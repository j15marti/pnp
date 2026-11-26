import itertools as I
import collections as C
import json
import networkx as nx


def mesh(k):
    faces=[]
    for s in I.product((-1,1),repeat=3):
        def v(i,j):return (s[0]*i,s[1]*j,s[2]*(k-i-j))
        for i in range(k):
            for j in range(k-i):
                for f in [(v(i,j),v(i+1,j),v(i,j+1))]+([(v(i+1,j),v(i+1,j+1),v(i,j+1))] if i+j<k-1 else []):
                    # All octants consistently oriented outward.
                    faces.append(f if s[0]*s[1]*s[2]==1 else (f[0],f[2],f[1]))
    return faces


def flags(k):
    F=mesh(k);edge=C.defaultdict(list)
    for i,f in enumerate(F):
        for a,b in zip(f,f[1:]+f[:1]):edge[frozenset((a,b))].append(i)
    assert all(len(z)==2 for z in edge.values())
    B=[];W=[]
    for i,f in enumerate(F):
        for j in range(3):
            a,b,c=f[j:]+f[:j];B.append((i,a,b));W.append((i,b,a))
    Wset=set(W)
    def color(v):return (abs(v[0])+2*abs(v[1]))%3
    T=[]
    for i,a,b in B:
        c=next(v for v in F[i] if v not in (a,b));j=next(j for j in edge[frozenset((a,b))] if j!=i)
        N=[(i,b,a),(i,a,c),(j,a,b)];assert all(w in Wset for w in N)
        t=tuple(sorted(N,key=lambda w:color(w[2])));assert [color(w[2]) for w in t]==[0,1,2];T.append(t)
    return T,[color(b) for i,a,b in B]


def graph(T, universe=None):
    G=nx.Graph();G.add_nodes_from(('e',w) for w in (universe if universe is not None else {w for t in T for w in t}));G.add_nodes_from(('t',i) for i in range(len(T)));G.add_edges_from((('t',i),('e',w)) for i,t in enumerate(T) for w in t);return G


def faces(emb):
    seen=set();return [emb.traverse_face(a,b,seen) for a,b in emb.edges() if (a,b) not in seen]


def reconstruct(T):
    # Only the encoded triples are used. No mesh coordinates or witness colors.
    G=graph(T);ok,emb=nx.check_planarity(G);assert ok
    F=faces(emb);at=C.defaultdict(list)
    for i,f in enumerate(F):
        for v in f:at[v].append(i)
    original={i for i,f in enumerate(F) if len(f) in (8,12)};edge={i for i,f in enumerate(F) if len(f)==4};tri={i for i,f in enumerate(F) if len(f)==6}
    def one(v,S):
        z=set(at[v])&S;assert len(z)==1;return next(iter(z))
    H=nx.Graph();H.add_nodes_from(original);ends={}
    for e in edge:
        z={one(v,original) for v in F[e]};assert len(z)==2;ends[e]=z;H.add_edge(*z)
    tris={i:{one(v,original) for v in F[i]} for i in tri};assert all(len(t)==3 for t in tris.values())
    adj=C.defaultdict(list)
    for i,t in tris.items():
        for e in I.combinations(sorted(t),2):adj[e].append(i)
    assert all(len(z)==2 for z in adj.values())
    i=min(tris);col=dict(zip(sorted(tris[i]),range(3)));q=[i];done={i}
    while q:
        i=q.pop()
        for e in I.combinations(sorted(tris[i]),2):
            j=next(j for j in adj[e] if j!=i);v=next(iter(tris[j]-set(e)));c=3-col[e[0]]-col[e[1]]
            if v in col:assert col[v]==c
            else:col[v]=c
            if j not in done:done.add(j);q.append(j)
    assert len(done)==len(tris) and len(col)==len(original) and all(col[a]!=col[b] for a,b in H.edges())
    out=[]
    for i in range(len(T)):
        v=('t',i);e=one(v,edge);a=one(v,original);b=next(iter(ends[e]-{a}));out.append(col[b])
    return out


def check_cover(T,Cs):
    U={w for t in T for w in t};assert len(Cs)==len(U)//3 and C.Counter(w for i in Cs for w in T[i])==C.Counter({w:1 for w in U})


def closure(T,U):
    A=set(range(len(T)));U=set(U);forced=[];calls=0
    while True:
        occ={w:[] for w in U}
        for i in A:
            for w in T[i]:occ[w].append(i)
        if any(not z for z in occ.values()):return 'NO',len(A),calls
        unit=next((z[0] for z in occ.values() if len(z)==1),None)
        if unit is not None:
            A-=set(i for w in T[unit] for i in occ[w]);U-=set(T[unit]);forced.append(unit);continue
        dead=set()
        for a,b in I.combinations(range(3),2):
            L={T[i][a] for i in A};R={T[i][b] for i in A};H=nx.Graph();H.add_nodes_from(L|R);H.add_edges_from((T[i][a],T[i][b]) for i in A);M=nx.algorithms.bipartite.maximum_matching(H,top_nodes=L);calls+=1
            if len(M)!=len(L)+len(R) or len(L)!=len(R):return 'NO',len(A),calls
            D=nx.DiGraph();D.add_nodes_from(L|R);D.add_edges_from((T[i][a],T[i][b]) for i in A);D.add_edges_from((M[v],v) for v in L);idx={v:j for j,S in enumerate(nx.strongly_connected_components(D)) for v in S};dead|={i for i in A if idx[T[i][a]]!=idx[T[i][b]]}
        if not dead:return ('YES' if not A else 'OPEN'),len(A),calls
        A-=dead


def run(k):
    T,truth=flags(k);m=len(T);assert m==24*k*k and len(set(T))==m
    U={w for t in T for w in t};assert all(len({t[c] for t in T})==m//3 for c in range(3));G=graph(T);assert set(dict(G.degree()).values())=={3};assert nx.check_planarity(G)[0]
    # Independent source-only reconstruction and direct exact witness validation.
    col=reconstruct(T)
    for c in range(3):
        check_cover(T,[i for i,x in enumerate(truth) if x==c]);check_cover(T,[i for i,x in enumerate(col) if x==c])
    H=nx.Graph();H.add_nodes_from(range(m));occ=C.defaultdict(list)
    for i,t in enumerate(T):
        for w in t:occ[w].append(i)
    for z in occ.values():H.add_edges_from(I.combinations(z,2))
    ok,emb=nx.check_planarity(H);assert ok;hist=C.Counter(map(len,faces(emb)));assert max(hist)<=6
    # 3-connectivity checked on smaller instances, theorem covers all sizes.
    conn=nx.node_connectivity(H) if k<=2 else None
    if conn is not None:assert conn>=3
    st=closure(T,U);assert st[:2]==('OPEN',m)
    # Genuine neighboring inputs, keep original universe. Single deletion leaves two known covers.
    deleted=0;S=[t for i,t in enumerate(T) if i!=deleted];assert nx.check_planarity(graph(S,U))[0]
    check_cover(S,[j for j,i in enumerate(range(1,m)) if col[i]!=col[deleted] and col[i]==(col[deleted]+1)%3]);ss=closure(S,U);assert ss[0]!='NO'
    # Two conflicting triples forced by distinct element owners, no empty owner initially.
    bad=None
    for z in occ.values():
        for a,b in I.combinations(z,2):
            for x in set(T[a])-set(T[b]):
                for y in set(T[b])-set(T[a]):
                    drop=(set(occ[x])-{a})|(set(occ[y])-{b});assert a not in drop and b not in drop
                    if all(set(z)-drop for z in occ.values()):bad=drop;break
                if bad is not None:break
            if bad is not None:break
        if bad is not None:break
    assert bad is not None;N=[t for i,t in enumerate(T) if i not in bad];assert nx.check_planarity(graph(N,U))[0];ns=closure(N,U);assert ns[0]=='NO'
    return {'k':k,'triples':m,'n_per_color':m//3,'phase_faces':dict(sorted(hist.items())),'face_cover_lower':(m+5)//6,'phase_connectivity_checked':conn,'closure':st,'sat_neighbor_deleted':1,'sat_neighbor_closure':ss,'unsat_neighbor_deleted':len(bad),'unsat_neighbor_closure':ns,'reconstructed_covers':3}


if __name__=='__main__':
    print(json.dumps([run(k) for k in (1,2,4,8,16)],indent=2))
