import itertools as I, json, random, math
import networkx as nx

def graph(T,n):
    G=nx.Graph();G.add_nodes_from((c,i) for c in range(3) for i in range(n));G.add_edges_from((('t',j),(c,v)) for j,t in enumerate(T) for c,v in enumerate(t));return G

def solve_ref(T,n):
    if n==0:return []
    for p in I.combinations(range(len(T)),n):
        if all(len({T[j][c] for j in p})==n for c in range(3)):return list(p)
    return None

def close(T,n):
    S=set(range(len(T)));pins=set();owners={(c,i) for c in range(3) for i in range(n)}
    def pm(A,c,d):
        X=[(c,i) for cc,i in owners if cc==c];Y=[(d,i) for cc,i in owners if cc==d];G=nx.Graph();G.add_nodes_from(X+Y);G.add_edges_from(((c,T[j][c]),(d,T[j][d])) for j in A);return len(nx.bipartite.maximum_matching(G,top_nodes=X))==2*len(X)
    # Keep all owners, use singleton selection to delete competitors, then exact pairwise support.
    while True:
        old=set(S)
        for c,i in owners:
            L=[j for j in S if T[j][c]==i]
            if not L:return None
            if len(L)==1:
                j=L[0];pins.add(j);S={k for k in S if k==j or all(T[k][d]!=T[j][d] for d in range(3))}
        for c,d in I.combinations(range(3),2):
            if not pm(S,c,d):return None
            X=[(c,i) for i in range(n)];Y=[(d,i) for i in range(n)]
            for j in list(S):
                G=nx.Graph();A=[v for v in X if v[1]!=T[j][c]];B=[v for v in Y if v[1]!=T[j][d]];G.add_nodes_from(A+B);G.add_edges_from(((c,T[k][c]),(d,T[k][d])) for k in S if T[k][c]!=T[j][c] and T[k][d]!=T[j][d]);
                if len(nx.bipartite.maximum_matching(G,top_nodes=A))!=2*(n-1):S.remove(j)
        if S==old:return sorted(S)

def chart(T,n,c,d):
    z=3-c-d; G=graph(T,n);G.remove_nodes_from([(z,i) for i in range(n)])
    X=[(c,i) for i in range(n)];H=nx.Graph();H.add_nodes_from(X+[(d,i) for i in range(n)]);H.add_edges_from(((c,t[c]),(d,t[d])) for t in T)
    M=nx.bipartite.maximum_matching(H,top_nodes=X);assert len(M)==2*n
    base=set(next(j for j,t in enumerate(T) if (c,t[c])==a and (d,t[d])==M[a]) for a in X)
    ok,emb=nx.check_planarity(G);assert ok
    faces={};F=0;seen=set();roots=[]
    for C in nx.connected_components(G):
        roots.append(F)
        for a in C:
            for b in emb.neighbors_cw_order(a):
                if (a,b) in seen:continue
                w=emb.traverse_face(a,b,seen)
                for u,v in zip(w,w[1:]+w[:1]):faces[u,v]=F
                F+=1
    edge=[];D=nx.DiGraph();D.add_nodes_from(range(F));
    for j,t in enumerate(T):
        a=(c,t[c]);b=('t',j);v=(d,t[d]);l,r=faces[a,b],faces[b,a];assert faces[b,v]==l and faces[v,b]==r
        m=int(j in base);edge.append((l,r,m))
        for u,w,k in [(r,l,1-m),(l,r,m)]:
            if not D.has_edge(u,w) or D[u][w]['weight']>k:D.add_edge(u,w,weight=k)
    ds=dict(nx.all_pairs_dijkstra_path_length(D));lo={};hi={}
    for root in roots:
        for f in ds[root]:lo[f]=-ds[f][root];hi[f]=ds[root][f]
    ids={};
    for f in range(F):
        for t in range(lo[f]+1,hi[f]+1):ids[f,t]=len(ids)
    # literals 2*i true, 2*i+1 false; constants represented by -1 True, -2 False
    def neg(a):return (-3-a) if a<0 else a^1
    def bit(f,t):return -1 if t<=lo[f] else -2 if t>hi[f] else 2*ids[f,t]
    def clause(a,b):
        if -1 in (a,b):return []
        if a==-2 and b==-2:return [(-2,-2)]
        if a==-2:a=b
        if b==-2:b=a
        if a==neg(b):return []
        return [(a,b)]
    def diff(u,v,k): # h_u <= h_v+k
        return [p for t in range(lo[u],hi[u]+1) for p in clause(neg(bit(u,t)),bit(v,t-k))]
    B=[]
    for (f,t),i in ids.items():B+=clause(neg(bit(f,t)),bit(f,t-1))
    P=[]
    for l,r,m in edge:
        B+=diff(l,r,1-m)+diff(r,l,m)
        P.append([diff(l,r,-m)+diff(r,l,m),diff(l,r,1-m)+diff(r,l,m-1)])
    L=[[] for _ in range(n)]
    for j,t in enumerate(T):L[t[z]].append(j)
    return len(ids),B,P,L,edge,lo,ids

def hull(B,k):
    # all semantically entailed literal implications for satisfiable 2CNF, or None
    q=2*k;full=(1<<q)-1;r=[1<<i for i in range(q)]
    for a,b in B:
        if a==-2:return None
        r[a^1]|=1<<b;r[b^1]|=1<<a
    for j in range(q):
        b=1<<j;w=r[j]
        for i in range(q):
            if r[i]&b:r[i]|=w
    if any((r[i]>>(i^1)&1) and (r[i^1]>>i&1) for i in range(0,q,2)):return None
    forced=sum(1<<(i^1) for i in range(q) if r[i]>>(i^1)&1)
    return tuple(full if r[i]>>(i^1)&1 else r[i]|forced for i in range(q))

def clauses(R):return [(i^1,j) for i,r in enumerate(R) for j in range(len(R)) if (r>>j)&1 and i!=j]

def model(B,k):
    B=list(B);out=[]
    for i in range(k):
        a=2*i;v=hull(B+[(a,a)],k) is not None;out.append(int(v));a^=int(not v);B.append((a,a))
    return out

def run(T,n,c,d,cap=2):
    k,B,P,L,edge,lo,ids=chart(T,n,c,d);R=hull(B,k);assert R is not None;rounds=0;calls=0
    # process one label or all label pairs, enumerate exact 2-CNF branches, intersect hulls
    groups=[g for a in range(1,cap+1) for g in I.combinations(range(n),a)]
    while True:
        old=R
        for g in groups:
            A=None;base=clauses(R)
            for choice in I.product(*(L[z] for z in g)):
                extra=[]
                for z,j in zip(g,choice):
                    for e in L[z]:extra+=P[e][int(e==j)]
                Q=hull(base+extra,k);calls+=1
                if Q is not None:A=Q if A is None else tuple(x&y for x,y in zip(A,Q))
            if A is None:return {'status':'NO','bits':k,'rounds':rounds+1,'calls':calls}
            R=A
        rounds+=1
        if R==old:break
    B=clauses(R);E=[]
    for z,Lz in enumerate(L):
        for i,j in I.combinations(Lz,2):
            calls+=1
            if hull(B+P[i][1]+P[j][1],k) is not None:E.append(z);break
    product=math.prod(len(L[z]) for z in E);exact=not E
    # Enumerate only those omitted labels whose exact occupancy is not certified by the global count.
    final=None;branches=0
    if product<=len(T)**2:
        for choice in I.product(*(L[z] for z in E)):
            extra=[]
            for z,j in zip(E,choice):
                for e in L[z]:extra+=P[e][int(e==j)]
            branches+=1;calls+=1
            if hull(B+extra,k) is not None:final=B+extra;break
        if final is None:return {'status':'NO','bits':k,'rounds':rounds,'calls':calls,'exact_hull':exact,'exception_labels':E,'branch_product':product,'branches':branches}
    a=model(final if final is not None else B,k);h={f:v for f,v in lo.items()}
    for (f,t),i in ids.items():h[f]+=a[i]
    W=[j for j,(l,r,m) in enumerate(edge) if m+h[l]-h[r]==1]
    assert len(W)==n and len({T[j][c] for j in W})==n and len({T[j][d] for j in W})==n
    yes=len({T[j][3-c-d] for j in W})==n
    if final is not None:assert yes
    return {'status':'YES' if yes else 'UNKNOWN','bits':k,'rounds':rounds,'calls':calls,'exact_hull':exact,'exception_labels':E,'branch_product':product,'branches':branches,'witness':W if yes else None}

U=[tuple(map(int,t)) for t in '000 002 010 011 021 022 100 101 111 201 202 221'.split()]
V=U+[(1,1,0)]
B0=[tuple(map(int,t)) for t in '000 002 012 111 121 202 210 222'.split()]
def ring(k):
    T=[tuple(3*i+v for v in t) for i in range(k) for t in B0]
    for i in range(k-1):
        a=8*i+2;b=8*(i+1)+5;x=list(T[a]);y=list(T[b]);x[1],y[1]=y[1],x[1];T[a]=tuple(x);T[b]=tuple(y)
    return T

def test(T,n,cap=2):
    assert len(set(T))==len(T) and nx.check_planarity(graph(T,n))[0]
    S=close(T,n)
    if S is None:return {'closure':'NO'}
    R=[T[j] for j in S];jobs=[run(R,n,c,d,cap) for c,d in I.combinations(range(3),2)]
    for q in jobs:
        if q.get('witness') is not None:q['witness']=[S[j] for j in q['witness']];assert all(len({T[j][c] for j in q['witness']})==n for c in range(3))
    return {'closure':'stagnant' if len(S)==len(T) else 'reduced','jobs':jobs}

if __name__=='__main__':
    result={}
    for name,T in [('U',U),('V',V),('B',B0)]:
        result[name]={'reference':solve_ref(T,3),'k1':test(T,3,1),'k2':test(T,3,2)}
    for k in [2,4,8]:
        T=ring(k);result['ring'+str(k)]={'k1':test(T,3*k,1)}
    print(json.dumps(result,indent=2))
