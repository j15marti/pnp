# Load shared routines from sibling audit.
from pathlib import Path
exec(Path(__file__).with_name('p3r03.py').read_text().split('def parse(s):')[0])
def face_prune(n,T):
    T=sorted(T);G=nx.Graph();G.add_nodes_from((a,v) for a in range(3) for v in range(n))
    for i,t in enumerate(T):G.add_edges_from(((3,i),(a,t[a])) for a in range(3))
    keep=set();bundles=0;maxbundle=0
    for V in nx.connected_components(G):
        g=G.subgraph(V).copy();sizes=[sum(a==b for a,i in V) for b in range(3)]
        if len(set(sizes))!=1:return None,0,0
        ok,E=nx.check_planarity(g);ck(ok)
        darts={};seen=set();nf=0
        for v in E:
            for w in E[v]:
                if (v,w) not in seen:
                    F=E.traverse_face(v,w,mark_half_edges=seen)
                    for a,b in zip(F,F[1:]+F[:1]):darts[a,b]=nf
                    nf+=1
        uf=nx.utils.UnionFind(range(nf))
        for z in (v for v in V if v[0]==2):
            for t in g[z]:uf.union(darts[z,t],darts[t,z])
        H=g.subgraph([v for v in V if v[0]!=2]);C={v:i for i,A in enumerate(nx.connected_components(H)) for v in A}
        Q=nx.Graph();need=collections.Counter();L=collections.defaultdict(set);Tface={}
        for v in H:
            c=('c',C[v]);Q.add_node(c)
            if v[0]==0:need[c]+=1
            if v[0]==3:
                for w in H[v]:
                    for a,b in [(v,w),(w,v)]:Q.add_edge(c,('f',uf[darts[a,b]]))
        for z in (v for v in V if v[0]==2):
            fs={uf[darts[z,t]] for t in g[z]};ck(len(fs)==1);f=('f',next(iter(fs)));need[f]+=1
            for t in g[z]:
                c=('c',C[t]);ck(Q.has_edge(c,f));L[c,f].add(z[1]);Tface[t]=(c,f)
        ck(nx.is_tree(Q));quota={};q=collections.deque(v for v in Q if Q.degree(v)<=1);qg=Q.copy()
        while q:
            v=q.popleft()
            if v not in qg:continue
            if not qg.degree(v):
                if need[v]!=0:return None,0,0
                qg.remove_node(v);continue
            if qg.degree(v)!=1:continue
            w=next(iter(qg[v]));r=need[v];key=(v,w) if v[0]=='c' else (w,v)
            if r<0 or r>len(L[key]):return None,0,0
            quota[key]=r;need[w]-=r;qg.remove_node(v)
            if qg.degree(w)<=1:q.append(w)
        for t,key in Tface.items():
            if quota[key]>0:keep.add(T[t[1]])
        for c in {('c',i) for i in C.values()}:
            if sum(v[0]==0 and C[v]==c[1] for v in C)==1:
                k=sum(key[0]==c and quota[key]>0 for key in Tface.values());ck(k<=2);bundles+=1;maxbundle=max(maxbundle,k)
    return keep,bundles,maxbundle

def cycle_terminal(n,T):
    original=set(T);rounds=0;nb=0;mx=0
    while True:
        S=close(n,T)
        if S is None:return False,'closure',0,nb,mx,None
        U,b,k=face_prune(n,S);nb+=b;mx=max(mx,k);rounds+=1
        if U is None:return False,'quota',0,nb,mx,None
        if U==S:break
        T=U
    G=nx.Graph();G.add_edges_from(((0,t[0]),(1,t[1])) for t in U);A=[]
    for C in nx.connected_components(G):
        L=sorted(v for a,v in C if a==0);E=[t for t in U if t[0] in L];r=len(L);W=[]
        if r==1:W=[(t,) for t in E]
        else:
            H=G.subgraph(C)
            if len(E)!=2*r or H.number_of_edges()!=2*r or any(H.degree(v)!=2 for v in C):return None,'class',len(U),nb,mx,None
            # Enumerate the two alternations by fixing an edge at the first X.
            for t in sorted(e for e in E if e[0]==L[0]):
                J=H.copy();J.remove_nodes_from([(0,t[0]),(1,t[1])]);M=nx.bipartite.maximum_matching(J,top_nodes=[(0,x) for x in L[1:]])
                ck(len(M)==2*(r-1));W.append(tuple([t]+[next(e for e in E if e[0]==x and e[1]==M[(0,x)][1]) for x in L[1:]]))
        W=[q for q in W if len({t[2] for t in q})==r]
        if not W:return False,'rainbow',len(U),nb,mx,None
        ck(len(W)<=2);A.append(W)
    clauses=[]
    for i,W in enumerate(A,1):
        if len(W)==1:clauses.append((-i,-i))
    for i,j in it.combinations(range(len(A)),2):
        for a,q in enumerate(A[i]):
            for b,r in enumerate(A[j]):
                if {t[2] for t in q}&{t[2] for t in r}:clauses.append((i+1 if a==0 else -(i+1),j+1 if b==0 else -(j+1)))
    P=sat2(len(A),clauses)
    if P is None:return False,'2sat',len(U),nb,mx,None
    Q=[t for i,W in enumerate(A,1) for t in W[int(i in P)]]
    ck(set(Q)<=original and len(Q)==n and all(len({t[a] for t in Q})==n for a in range(3)))
    return True,'2sat',len(U),nb,mx,Q

stats=collections.Counter();skips=0;bundles=0;maxb=0
for job in range(1200):
    n=rng.randrange(4,9);T=[];i=0
    while i<n:
        if i+1<n and rng.random()<.5:
            V=rng.sample(range(n),4);T += [(i,i,V[0]),(i,i+1,V[1]),(i+1,i,V[2]),(i+1,i+1,V[3])];i+=2
        else:
            T += [(i,i,z) for z in rng.sample(range(n),rng.choice([2,2,3]))];i+=1
    if not planar(n,T):skips+=1;continue
    o=oracle(n,T);a=cycle_terminal(n,T);ck(a[0]==o);stats[f'{a[1]}:{a[0]}']+=1;bundles+=a[3];maxb=max(maxb,a[4])
scale=[]
for k in [3,8,16,32,64]:
    T=[(b*k+i,b*k+(i+d)%k,2*i+d) for b in (0,1) for i in range(k) for d in (0,1)]
    ck(planar(2*k,T));a=cycle_terminal(2*k,T);ck(a[0] is True);scale.append(dict(k=k,triples=len(T),result=a[0],method=a[1],remaining=a[2]))
print(json.dumps(dict(seed=SEED,checks=checks,stats=stats,skips=skips,bundles=bundles,maxbundle=maxb,scale=scale),sort_keys=True))
