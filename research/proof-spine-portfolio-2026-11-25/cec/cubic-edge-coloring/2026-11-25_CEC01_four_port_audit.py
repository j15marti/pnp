import itertools as it, json, random
import networkx as nx

PATS=((0,0,0,0),(0,0,1,1),(0,1,0,1),(0,1,1,0))
PAIR=(((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2)))
ST=dict(queries=0,kempe=0,diamond=0,backtrack=0,matching=0)
def edge(u,v): return tuple(sorted((u,v)))
def normalize(w):
    d={}; return tuple(d.setdefault(x,len(d)) for x in w)
def check(g,w,cubic=True):
    assert set(w)=={edge(*e) for e in g.edges}
    for v in g:
        s=[w[edge(v,u)] for u in g[v]]
        assert len(s)==len(set(s)) and set(s)<=set(range(3))
        if cubic: assert len(s)==3

def source(g):
    assert not g.is_multigraph() and nx.number_of_selfloops(g)==0
    assert all(d==3 for _,d in g.degree())
def brute(g,pins=None):
    w=dict(pins or {}); used={v:0 for v in g}
    for (u,v),c in w.items():
        b=1<<c
        if used[u]&b or used[v]&b: return None
        used[u]|=b; used[v]|=b
    es={edge(*e) for e in g.edges}
    def visit():
        ST['backtrack']+=1
        if len(w)==len(es): return w.copy()
        k,m=min(((e,7&~(used[e[0]]|used[e[1]])) for e in es-w.keys()),key=lambda z:(z[1].bit_count(),z[0]))
        u,v=k
        for c in range(3):
            b=1<<c
            if m&b:
                w[k]=c; used[u]|=b; used[v]|=b
                ans=visit()
                if ans is not None: return ans
                used[u]^=b; used[v]^=b; del w[k]
        return None
    return visit()
def diamond(g,u,v):
    z=max(g.nodes,default=-1)+1; x,y,a,b=range(z,z+4)
    g.add_edges_from([(u,x),(v,y),(x,a),(x,b),(y,a),(y,b),(a,b)])
    return edge(u,x),edge(v,y)
def solve(g):
    source(g)
    if nx.number_of_nodes(g)==0: return {}
    if any(nx.bridges(g)): return None
    for u,v in sorted(edge(*e) for e in g.edges):
        ab=sorted(set(g[u])&set(g[v]))
        if len(ab)!=2: continue
        x,y=ab
        if g.has_edge(x,y): continue
        s,=set(g[x])-{u,v}; t,=set(g[y])-{u,v}
        if s==t or g.has_edge(s,t): continue
        h=g.copy(); h.remove_nodes_from([u,v,x,y]); h.add_edge(s,t)
        ST['diamond']+=1; w=solve(h)
        if w is None: return None
        c=w.pop(edge(s,t)); i,j=(c+1)%3,(c+2)%3
        for a,b,z in [(s,x,c),(t,y,c),(u,v,c),(u,x,i),(v,x,j),(u,y,j),(v,y,i)]: w[edge(a,b)]=z
        check(g,w); return w
    w=brute(g)
    if w is not None: check(g,w)
    return w

def closure(g):
    source(g)
    if any(nx.bridges(g)): return False
    for u,v in g.edges:
        h=g.copy(); h.remove_nodes_from([u,v]); ST['matching']+=1
        if len(nx.max_weight_matching(h,maxcardinality=True))*2!=len(h): return False
        h=g.copy(); h.remove_edge(u,v); ST['matching']+=1
        if len(nx.max_weight_matching(h,maxcardinality=True))*2!=len(h): return False
    return True

def cap(mask):
    mask=set(mask); g=nx.Graph(); p=[None]*4
    if len(mask)==3:
        return nx.cycle_graph(4),tuple(range(4))
    assert len(mask)==2
    if 0 in mask:
        i=next(iter(mask-{0})); g.add_edges_from([(0,2),(0,3),(1,2),(1,3),(2,3),(4,6),(4,7),(5,6),(5,7),(6,7)])
        for j,pp in enumerate(PAIR[i-1]):
            for k,l in enumerate(pp): p[l]=4*j+k
    else:
        i=next(iter({1,2,3}-mask)); g.add_edge(0,1)
        for j,pp in enumerate(PAIR[i-1]):
            for l in pp: p[l]=j
    return g,tuple(p)

def attach(P,Q):
    g,p=P; h,q=Q; z=max(g.nodes,default=-1)+1
    ren={v:v+z for v in h}; G=nx.compose(g,nx.relabel_nodes(h,ren)); L=[]; R=[]
    for u,v0 in zip(p,q):
        v=ren[v0]
        if G.has_edge(u,v):
            a,b=diamond(G,u,v)
        else:
            G.add_edge(u,v); a=b=edge(u,v)
        L.append(a); R.append(b)
    source(G); return G,L,R,ren

def polegraph(P):
    g,p=P; h=g.copy(); z=max(g.nodes,default=-1)+1; L=[]
    for i,v in enumerate(p): h.add_edge(v,z+i); L.append(edge(v,z+i))
    return h,L

def project(P,w,L):
    h,k=polegraph(P); r={edge(*e):w[edge(*e)] for e in P[0].edges}
    r.update({a:w[b] for a,b in zip(k,L)}); check(h,r,False); return r

def pattern(P,w):
    _,L=polegraph(P); return PATS.index(normalize([w[e] for e in L]))

def query(P,mask):
    ST['queries']+=1; G,L,_,_=attach(P,cap(mask)); w=solve(G)
    if w is None: return None
    a=project(P,w,L); assert pattern(P,a) in mask; return a

def alternate(P,w):
    g,L=polegraph(P); t=pattern(P,w)
    for e in L:
        for c in range(3):
            b=w[e]
            if b==c: continue
            h=nx.Graph(); h.add_edges_from(k for k,v in w.items() if v in (b,c))
            comp=nx.node_connected_component(h,e[1]); d=w.copy()
            for k in h.subgraph(comp).edges:
                k=edge(*k); d[k]=b+c-w[k]
            if pattern(P,d)!=t:
                check(g,d,False); ST['kempe']+=1; return d
    raise AssertionError('no alternative')

def classify(P):
    a=query(P,{0,1})
    if a is None: a=query(P,{2,3})
    if a is None: return 'empty',{}
    b=alternate(P,a); W={pattern(P,a):a,pattern(P,b):b}
    c=query(P,set(range(4))-W.keys())
    if c is None: return 'pair',W
    W[pattern(P,c)]=c; return 'universal',W

def masks(P):
    g,L=polegraph(P); return {i for i,t in enumerate(PATS) if brute(g,dict(zip(L,t))) is not None}

def contract(A,B):
    start=ST['queries']; typ,W=classify(A)
    if typ=='empty': return dict(yes=False,typ=typ,calls=ST['queries']-start)
    H,L,_,_=attach(B,cap(W.keys())); ST['queries']+=1; w=solve(H)
    if w is None: return dict(yes=False,typ=typ,calls=ST['queries']-start)
    b=project(B,w,L); switched=pattern(B,b) not in W
    if switched: b=alternate(B,b)
    a=W[pattern(B,b)]; _,p=polegraph(A); _,q=polegraph(B)
    wa=[a[k] for k in p]; wb=[b[k] for k in q]; perm=dict(zip(wb,wa))
    perm.update(zip(sorted(set(range(3))-perm.keys()),sorted(set(range(3))-set(perm.values()))))
    G,L,R,ren=attach(A,B); r={edge(*e):a[edge(*e)] for e in A[0].edges}
    r.update({edge(ren[u],ren[v]):perm[b[edge(u,v)]] for u,v in B[0].edges})
    for i,k in enumerate(L):
        r[k]=wa[i]; r[R[i]]=wa[i]
        if k!=R[i]:
            # Find four private diamond vertices, with the two terminal vertices known.
            x=next(v for v in k if v not in A[0]); y=next(v for v in R[i] if v not in ren.values())
            u,v=sorted(set(G[x])&set(G[y])); c=wa[i]; j,l=(c+1)%3,(c+2)%3
            r.update({edge(u,v):c,edge(x,u):j,edge(x,v):l,edge(y,u):l,edge(y,v):j})
    check(G,r); return dict(yes=True,typ=typ,switched=switched,calls=ST['queries']-start)

def remove_pair(g,u,v):
    p=tuple(sorted(set(g[u])-{v})+sorted(set(g[v])-{u})); h=g.copy(); h.remove_nodes_from([u,v]); return h,p

def remove_edges(g,e,f):
    h=g.copy(); h.remove_edges_from([e,f]); return h,e+f

def inflate(P,k):
    h,p=P[0].copy(),P[1]; u,v=next(iter(h.edges))
    for _ in range(k):
        h.remove_edge(u,v); a,_=diamond(h,u,v); u,v=a
    return h,p

def run():
    P=nx.petersen_graph(); A=remove_pair(P,0,5); assert masks(A)=={0,1}
    H=next(remove_edges(P,e,f) for e,f in it.combinations(P.edges,2) if len(set(e+f))==4 and masks(remove_edges(P,e,f))=={2,3})
    rng=random.Random(3819); poles=[A,H,cap({0,1,3}),cap({0,1}),cap({2,3})]
    for n in (6,8,10,12):
        for _ in range(8):
            g=nx.random_regular_graph(3,n,seed=rng.randrange(2**31)); u,v=next(iter(g.edges)); poles.append(remove_pair(g,u,v))
    table=[]
    for X in poles:
        typ,W=classify(X); actual=masks(X)
        assert set(W)<=actual and (typ=='empty' and not actual or typ=='pair' and len(actual)==2 or typ=='universal' and len(actual)>=3)
        table.append(sorted(actual))
    out=[]
    for i,X in enumerate(poles):
        for j in (0,1,2,3,4):
            Y=poles[j]; g,*_=attach(X,Y); truth=solve(g) is not None; r=contract(X,Y)
            assert r['yes']==truth and r['yes']==bool(set(table[i])&set(table[j]))
            out.append(dict(i=i,j=j,n=len(g),**r))
    scale=[]
    for k in (0,8,16,32):
        for perm in ((0,1,2,3),(0,2,1,3)):
            X=inflate(A,k); Y=inflate((H[0],tuple(H[1][i] for i in perm)),k); g,*_=attach(X,Y)
            # Actual necessary matching closure on compact and first expanded neighbors.
            stable=closure(g) if k<=8 else None
            r=contract(X,Y); expected=perm!=(0,1,2,3)
            assert r['yes']==expected and (stable is not False)
            assert (solve(g) is not None)==expected
            scale.append(dict(k=k,n=len(g),perm=perm,closure=stable,**r))
    print(json.dumps(dict(seed=3819,stats=ST,poles=len(poles),masks=table,comparisons=len(out),sat=sum(x['yes'] for x in out),unsat=sum(not x['yes'] for x in out),switches=sum(x.get('switched',False) for x in out),scale=scale,rows=out),indent=2))
if __name__=='__main__': run()
