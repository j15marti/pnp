import itertools as it, random, json, collections
import networkx as nx
SEED=20261125
rng=random.Random(SEED)
checks=0
def ck(p):
    global checks
    checks+=1
    assert p

def planar(n,T):
    G=nx.Graph();G.add_nodes_from((a,v) for a in range(3) for v in range(n))
    for i,t in enumerate(T): G.add_edges_from(((3,i),(a,t[a])) for a in range(3))
    return nx.check_planarity(G)[0]

def oracle(n,T):
    X=[[t for t in T if t[0]==i] for i in range(n)]
    def rec(i,Y,Z):
        if i==n:return True
        return any(rec(i+1,Y|{t[1]},Z|{t[2]}) for t in X[i] if t[1] not in Y and t[2] not in Z)
    return rec(0,set(),set())

def close(n,T):
    T=set(T)
    while True:
        old=T.copy()
        for a in range(3):
            for v in range(n):
                S=[t for t in T if t[a]==v]
                if not S:return None
                if len(S)==1:
                    t=S[0];T={u for u in T if u==t or all(u[b]!=t[b] for b in range(3))}
        for a,b in [(0,1),(0,2),(1,2)]:
            L=[(a,i) for i in range(n)];H=nx.Graph();H.add_nodes_from(L+[(b,i) for i in range(n)])
            H.add_edges_from(((a,t[a]),(b,t[b])) for t in T)
            M=nx.bipartite.maximum_matching(H,top_nodes=L)
            if len(M)!=2*n:return None
            D=nx.DiGraph();D.add_nodes_from(L);D.add_edges_from(((a,t[a]),M[(b,t[b])]) for t in T)
            C={v:i for i,S in enumerate(nx.strongly_connected_components(D)) for v in S}
            T={t for t in T if C[(a,t[a])]==C[M[(b,t[b])]]}
        if T==old:return T

def tables(n,T,cap=2):
    G=nx.Graph();G.add_edges_from(((0,t[0]),(1,t[1])) for t in T);out=[]
    for C in nx.connected_components(G):
        X=sorted(v for a,v in C if a==0);r=len(X)
        if r>cap:return None
        W=collections.defaultdict(list)
        for q in it.product(*[sorted(t for t in T if t[0]==x) for x in X]):
            if len({t[1] for t in q})==r and len({t[2] for t in q})==r:W[frozenset(t[2] for t in q)].append(q)
        out.append((r,dict(W)))
    return out

def tags(W):return set().union(*W) if W else set()
def classes(r,W):
    U=tags(W)
    if not W:return None
    if r==1:return [U]
    if r!=2:return None
    G=nx.Graph();G.add_nodes_from(U);G.add_edges_from((a,b) for a,b in it.combinations(U,2) if frozenset((a,b)) not in W)
    C=list(nx.connected_components(G))
    return C if all(G.subgraph(S).number_of_edges()==len(S)*(len(S)-1)//2 for S in C) else None

def allocation(groups,S):
    # groups = (quota, parallel classes); uniform relaxation has singleton classes.
    G=nx.DiGraph();G.add_nodes_from(['s','t'])
    for i,(r,C) in enumerate(groups):
        G.add_edge('s',('r',i),capacity=r)
        for j,A in enumerate(C):
            G.add_edge(('r',i),('c',i,j),capacity=1)
            for z in A&S:G.add_edge(('c',i,j),('z',z),capacity=1);G.add_edge(('z',z),'t',capacity=1)
    f,F=nx.maximum_flow(G,'s','t');B=[set() for _ in groups]
    for i,(r,C) in enumerate(groups):
        for j,A in enumerate(C):
            for v,x in F[('c',i,j)].items():
                if x:B[i].add(v[1])
    return f,B

def guard_filter(n,A):
    removed=0;Z=set(range(n))
    while True:
        if any(not W for _,W in A):return False,removed
        # Exact-one / all three lane closure on all still-supported tuple IDs.
        support={t for _,W in A for Q in W.values() for q in Q for t in q}
        T=close(n,support)
        if T is None:return False,removed
        change=False
        for r,W in A:
            for B in list(W):
                W[B]=[q for q in W[B] if set(q)<=T]
                if not W[B]:del W[B];removed+=1;change=True
        if change:continue
        # A single base guard, with exact matroid or relaxed uniform allocation elsewhere.
        found=False
        for i,(r,W) in enumerate(A):
            groups=[(s,classes(s,V) or [{z} for z in tags(V)]) for j,(s,V) in enumerate(A) if j!=i]
            for B in list(W):
                if allocation(groups,Z-set(B))[0]!=n-r:
                    del W[B];removed+=1;found=True;break
            if found:break
        if not found:return True,removed

def majority_closed(W):
    return all((a&b)|(b&c)|(a&c) in W for a,b,c in it.combinations(W,3))

def sat2(k,C):
    G=nx.DiGraph();G.add_nodes_from([x for i in range(1,k+1) for x in (i,-i)])
    for a,b in C:G.add_edge(-a,b);G.add_edge(-b,a)
    H=nx.condensation(G);D=H.graph['mapping'];order={v:i for i,v in enumerate(nx.topological_sort(H))}
    if any(D[i]==D[-i] for i in range(1,k+1)):return None
    P={i for i in range(1,k+1) if order[D[i]]>order[D[-i]]}
    ck(all((a>0)==(abs(a) in P) or (b>0)==(abs(b) in P) for a,b in C))
    return P

def hybrid(n,A):
    Z=set(range(n));good=[];bad=[];groups=[]
    for r,W in A:
        if not W:return False,'empty',None
        C=classes(r,W)
        if C is None:bad.append((r,W))
        else:good.append((r,W));groups.append((r,C))
    R=sum(r for r,W in good)
    if allocation(groups,Z)[0]!=R:return False,'matroid_capacity',None
    if any(not majority_closed(W) for r,W in bad):return None,'nonbijunctive',None
    U=tags([B for _,W in bad for B in W]);queries=0
    def dual(S):
        nonlocal queries
        queries+=1
        return len(S)-R+allocation(groups,Z-set(S))[0]
    loops={z for z in U if dual({z})==0};P=nx.Graph();P.add_nodes_from(U-loops)
    for a,b in it.combinations(sorted(U-loops),2):
        if dual({a,b})==1:P.add_edge(a,b)
    C=list(nx.connected_components(P));full=dual(U)==len(C)
    I={};cl=[]
    for i,(_,W) in enumerate(bad):
        for z in sorted(tags(W)):I[i,z]=len(I)+1
        V=sorted(tags(W))
        for z in V:
            for a in (0,1):
                if not any((z in B)==a for B in W):v=I[i,z] if a==0 else -I[i,z];cl.append((v,v))
        for z,w in it.combinations(V,2):
            for a,b in it.product((0,1),repeat=2):
                if not any((z in B)==a and (w in B)==b for B in W):cl.append((I[i,z] if a==0 else -I[i,z],I[i,w] if b==0 else -I[i,w]))
    for (i,z),v in I.items():
        if z in loops:cl.append((-v,-v))
    for A0 in C:
        for v,w in it.combinations([v for (i,z),v in I.items() if z in A0],2):cl.append((-v,-w))
    S=sat2(len(I),cl)
    if S is None:return False,'hybrid_2sat',None
    B=[frozenset(z for (j,z),v in I.items() if j==i and v in S) for i in range(len(bad))]
    ck(all(b in W for b,(_,W) in zip(B,bad)))
    used=tags(B);ck(len(used)==sum(map(len,B)))
    f,V=allocation(groups,Z-used)
    if f!=R:
        ck(not full);return None,'higher_circuit',None
    Q=[t for b,(_,W) in zip(B,bad) for t in W[b][0]]+[t for b,(_,W) in zip(V,good) for t in W[frozenset(b)][0]]
    ck(len(Q)==n and all(len({t[a] for t in Q})==n for a in range(3)))
    return True,('hybrid' if bad else 'matroid'),Q

def run(n,T,filter_=False):
    S=close(n,T)
    if S is None:return False,'closure',None,0
    A=tables(n,S)
    if A is None:return None,'cap',None,0
    d=0
    if filter_:
        ok,d=guard_filter(n,A)
        if not ok:return False,'guard',None,d
    x,m,Q=hybrid(n,A);return x,m,Q,d

def parse(s):return [tuple(map(int,t)) for t in s.split()]
F=parse('002 003 110 111 221 230 323 332');U=parse('000 003 111 112 221 230 323 332')
S=parse('001 011 012 100 102 112 220 221');AGE=parse('000 002 010 011 021 022 100 101 111 201 202 221')
fixed=[]
for name,n,T in [('F',4,F),('U',4,U),('S',3,S),('AGE_U',3,AGE)]:
    ck(planar(n,T));o=oracle(n,T);a=run(n,T);b=run(n,T,True)
    ck(all(x[0] is None or x[0]==o for x in [a,b]));fixed.append(dict(name=name,oracle=o,before=a,after=b))
scale=[]
for name,T in [('F',F),('U',U)]:
    for k in (1,4,16):
        Q=[tuple(x+4*i for x in t) for i in range(k) for t in T]+[(4*i,4*i,4*(i+1)) for i in range(k-1)]
        ck(planar(4*k,Q));a=run(4*k,Q);ck(a[0]==(name=='F'));scale.append(dict(name=name,k=k,triples=len(Q),result=a[0],method=a[1]))
stat=collections.Counter();removed=0;skip=0;new=0
for job in range(500):
    n=rng.randrange(3,7);T=[]
    for i in range(0,n,2):
        for x,y,z in it.product(range(i,min(n,i+2)),range(i,min(n,i+2)),range(n)):
            if rng.random()<0.22:T.append((x,y,z))
    if not planar(n,T):skip+=1;continue
    o=oracle(n,T);a=run(n,T);b=run(n,T,True);removed+=b[3]
    for name,v in [('raw',a),('guarded',b)]:
        ck(v[0] is None or v[0]==o);stat[f'{name}:{v[1]}:{v[0]}:{o}']+=1
        if v[2] is not None:ck(set(v[2])<=set(T))
    new+=a[0] is None and b[0] is not None
print(json.dumps(dict(seed=SEED,checks=checks,fixed=fixed,scale=scale,stats=stat,skipped=skip,removed=removed,guard_new=new),sort_keys=True))
