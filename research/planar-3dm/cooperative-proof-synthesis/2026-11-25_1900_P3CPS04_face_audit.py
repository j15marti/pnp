import networkx as nx, json, itertools

def fixture():
    return 7,[(0,0,0),(1,1,3),(0,1,2),(1,0,4),(5,5,3),(5,5,4),(4,4,0),(2,2,1),(3,3,5),(2,3,2),(3,2,6),(6,6,5),(6,6,6),(4,4,1)]

def chain(b):
    n,T=fixture(); out=[tuple(x+n*i for x in t) for i in range(b) for t in T]
    for i in range(b-1):
        j=i*14+13;k=(i+1)*14+6;a,c=out[j],out[k];out[j]=a[:2]+(c[2],);out[k]=c[:2]+(a[2],)
    return n*b,out

def graph(n,T):
    G=nx.Graph();G.add_nodes_from((c,i) for c in range(3) for i in range(n))
    for j,t in enumerate(T): G.add_edges_from(((3,j),(c,v)) for c,v in enumerate(t))
    return G

def reference(n,T):
    inc={(c,i):set() for c in range(3) for i in range(n)}
    for j,t in enumerate(T):
        for c,v in enumerate(t):inc[c,v].add(j)
    def rec(V,J):
        if not V:return []
        v=min(V,key=lambda v:len(inc[v]&J))
        for j in sorted(inc[v]&J):
            vs={(c,x) for c,x in enumerate(T[j])}; nxt=rec(V-vs,J-set().union(*(inc[w] for w in vs)))
            if nxt is not None:return [j]+nxt
        return None
    return rec(set(inc),set(range(len(T))))

def face_chart(n,T):
    G=graph(n,T);ok,E=nx.check_planarity(G);assert ok
    if any(G.degree(v)==0 for v in G):return 'NO',None
    if not nx.is_connected(G):return 'DECLINE',None
    hf={};seen=set();nf=0
    for u in E:
        for v in E[u]:
            if (u,v) not in seen:
                W=E.traverse_face(u,v,seen)
                for a,b in zip(W,W[1:]+W[:1]):hf[a,b]=nf
                nf+=1
    ds=nx.utils.UnionFind(range(nf))
    for j,t in enumerate(T):
        u=(3,j);v=(2,t[2]);ds.union(hf[u,v],hf[v,u])
    zf={i:ds[hf[(2,i),next(iter(G[(2,i)]))]] for i in range(n)}
    H=G.subgraph([v for v in G if v[0]!=2]);cc=list(nx.connected_components(H));cid={v:i for i,C in enumerate(cc) for v in C}
    Q=nx.Graph();Q.add_nodes_from(('c',i) for i in range(len(cc)));Q.add_nodes_from(('f',ds[f]) for f in range(nf))
    for u,v in H.edges:
        for f in (ds[hf[u,v]],ds[hf[v,u]]):Q.add_edge(('c',cid[u]),('f',f))
    assert nx.is_tree(Q)
    demands={('c',i):sum(v[0]==0 for v in C) for i,C in enumerate(cc)}
    if any(sum(v[0]==0 for v in C)!=sum(v[0]==1 for v in C) for C in cc):return 'NO',None
    demands.update({v:sum(f==v[1] for f in zf.values()) for v in Q if v[0]=='f'})
    root=next(iter(Q));parent={root:None};order=[root]
    for u in order:
        for v in Q[u]:
            if v not in parent:parent[v]=u;order.append(v)
    r={};d=demands.copy()
    for u in reversed(order[1:]):
        p=parent[u];r[frozenset((u,p))]=d[u];d[p]-=d[u]
        if d[u]<0:return 'NO',None
    if d[root]!=0:return 'NO',None
    edge_labels={e:set() for e in r};ct={i:[] for i in range(len(cc))}
    for j,t in enumerate(T):
        c=('c',cid[(3,j)]);f=('f',zf[t[2]]);e=frozenset((c,f));assert e in r
        edge_labels[e].add(t[2]);ct[c[1]].append(j)
    if any(r[e]>len(edge_labels[e]) for e in r):return 'NO',None
    return 'OK',(Q,parent,order,r,edge_labels,ct,zf,cid)

def exact_table_solver(n,T):
    status,A=face_chart(n,T)
    if status!='OK':return status,None,{}
    Q,parent,order,r,labels,ct,zf,cid=A
    tables={}; lifts={}; tests=0;maxrank=max(r.values(),default=0);maxrows=0
    for u in reversed(order):
        p=parent[u];children=[v for v in Q[u] if parent.get(v)==u]
        if u[0]=='c':
            J=ct[u[1]]
            if len(J)>12:return 'DECLINE',None,{}
            rows=[]
            for bits in itertools.product((0,1),repeat=len(J)):
                I=[j for j,b in zip(J,bits) if b];tt=[T[j] for j in I]
                if len(I)!=sum(v[0]==0 and cid[v]==u[1] for v in cid):continue
                if any(len({t[c] for t in tt})!=len(I) for c in range(3)):continue
                masks={v:frozenset(t[2] for t in tt if zf[t[2]]==v[1]) for v in Q[u]}
                if any(len(masks[v])!=r[frozenset((u,v))] for v in Q[u]):continue
                rows.append((masks,I))
        else:
            if any(r[frozenset((u,v))]>1 for v in children):return 'DECLINE',None,{}
            if p is None:opts=[frozenset()]
            else:
                e=frozenset((u,p));k=r[e];L=labels[e]
                if min(k,len(L)-k)>2:return 'DECLINE',None,{}
                opts=[frozenset(q) for q in itertools.combinations(sorted(L),k)]
            rows=[]
            for P in opts:
                tests+=1
                G=nx.Graph(); active=[v for v in children if r[frozenset((u,v))]==1]
                Z={z for z,f in zf.items() if f==u[1]}-set(P)
                G.add_nodes_from(active);G.add_nodes_from(('z',z) for z in Z)
                if any(frozenset() not in tables[v] for v in children if v not in active):continue
                for v in active:
                    for M in tables[v]:
                        if len(M)==1 and next(iter(M)) in Z:G.add_edge(v,('z',next(iter(M))))
                m=nx.algorithms.bipartite.maximum_matching(G,top_nodes=set(active))
                if len(Z)!=len(active) or any(v not in m for v in active):continue
                masks={v:frozenset([m[v][1]]) if v in active else frozenset() for v in children}
                if p is not None:masks[p]=P
                rows.append((masks,[]))
        tab={}
        for masks,I in rows:
            if any(masks[v] not in tables[v] for v in children):continue
            P=masks[p] if p is not None else frozenset()
            if P not in tab:tab[P]=(I,[(v,masks[v]) for v in children])
        tables[u]=tab;maxrows=max(maxrows,len(tab))
        if not tab:return 'NO',None,{'maxrank':maxrank,'nodes':len(Q),'tests':tests,'maxrows':maxrows}
    witness=[];stack=[(order[0],frozenset())]
    while stack:
        u,P=stack.pop();I,child=tables[u][P];witness+=I;stack+=child
    assert len(witness)==n and all(len({T[j][c] for j in witness})==n for c in range(3))
    return 'YES',witness,{'maxrank':maxrank,'nodes':len(Q),'tests':tests,'maxrows':maxrows}

if __name__=='__main__':
    res=[]
    for b in (1,2,4,8,16,32,64):
        n,T=chain(b)
        for kind,drop in [('base',[]),('neighbor_yes',[0]),('neighbor_no',[0,2])]:
            U=[t for j,t in enumerate(T) if j not in drop];status,w,stats=exact_table_solver(n,U)
            expected=kind!='neighbor_no'
            if status in ('YES','NO'):assert (status=='YES')==expected
            if b<=4:assert (reference(n,U) is not None)==expected
            res.append({'b':b,'n':n,'m':len(U),'kind':kind,'status':status,**stats})
    print(json.dumps(res,indent=2))

def matching_closure(n,T):
    J=set(range(len(T)));forced=set();rounds=0
    while True:
        rounds+=1;old=J.copy()
        for c in range(3):
            for i in range(n):
                S=[j for j in J if T[j][c]==i]
                if not S:return False,J,forced,rounds
                if len(S)==1:
                    j=S[0];forced.add(j);J={k for k in J if k==j or all(T[k][d]!=T[j][d] for d in range(3))}
        for a,b in [(0,1),(0,2),(1,2)]:
            G=nx.Graph();U={(a,i) for i in range(n)};V={(b,i) for i in range(n)};G.add_nodes_from(U|V);G.add_edges_from(((a,T[j][a]),(b,T[j][b])) for j in J)
            M=nx.algorithms.bipartite.maximum_matching(G,top_nodes=U)
            if len(M)!=2*n:return False,J,forced,rounds
            D=nx.DiGraph();D.add_nodes_from(U|V)
            for j in J:
                u=(a,T[j][a]);v=(b,T[j][b]);D.add_edge(v,u) if M[u]==v else D.add_edge(u,v)
            C={v:i for i,K in enumerate(nx.strongly_connected_components(D)) for v in K}
            J={j for j in J if M[(a,T[j][a])]==(b,T[j][b]) or C[a,T[j][a]]==C[b,T[j][b]]}
        if J==old:return True,J,forced,rounds

def annulus(k):
    T=[]
    for b in (0,1):
        for i in range(k):
            T += [(b*k+i,b*k+i,2*i),(b*k+i,b*k+(i+1)%k,2*i+1)]
    return 2*k,T

if __name__=='__main__':
    for b in (1,4,16,64):
        n,T=chain(b); ok,J,F,R=matching_closure(n,T);assert ok and len(J)==len(T)
        print('closure_base',b,len(J),len(F),R)
        for drop in ([0],[0,2]):
            U=[t for j,t in enumerate(T) if j not in drop];ok,J,F,R=matching_closure(n,U);assert ok==(len(drop)==1);print('closure_neighbor',b,len(drop),ok,len(J),len(F),R)
    for k in (3,8,16,32,64):
        n,T=annulus(k);assert nx.check_planarity(graph(n,T))[0]
        ok,J,F,R=matching_closure(n,T);assert ok and len(J)==len(T)
        status,A=face_chart(n,T);assert status=='OK';Q,par,ord,r,L,*_=A
        largest=max(min(r[e],len(L[e])-r[e]) for e in r);assert largest==k
        for b in (0,1):
            I=[j for j in range(len(T)) if (j%2)==(b if j<2*k else 1-b)];assert len(I)==n and all(len({T[j][c] for j in I})==n for c in range(3))
        print('annulus',k,len(T),largest,len(J))
