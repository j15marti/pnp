import itertools as it, random, json, networkx as nx
from collections import Counter
R=random.Random(2010420); C=Counter()

def local(edges, masks, K):
    # edges are (u,v,cost); mask sets are raw pair parities; vertices 0..2h-1
    C['matching_calls']+=1
    if any(not a for a in masks): return None
    g=nx.Graph(); req=set(); cost={}; inc=[[] for _ in range(2*len(masks))]
    def node(required=True):
        x=len(g); g.add_node(x)
        if required: req.add(x)
        return x
    def edge(a,b,w=0):
        g.add_edge(a,b); cost[frozenset((a,b))]=w
    cross=[]
    for u,v,w in edges:
        a,b=node(),node(); inc[u].append(a); inc[v].append(b); edge(a,b,w); cross.append(frozenset((a,b)))
    ports=[node() for _ in inc]
    for p,L in zip(ports,inc):
        for a,b in it.combinations(L+[p],2): edge(a,b)
    for j,mask in enumerate(masks):
        shift=(1^(len(inc[2*j])%2))|((1^(len(inc[2*j+1])%2))<<1)
        S={a^shift for a in mask}; S={a|((a.bit_count()%2)<<2) for a in S}
        base=min(S); ext=[ports[2*j],ports[2*j+1],node(False)]; inner=[]
        for k,p in enumerate(ext):
            if (base>>k)&1:
                q=node(); edge(q,p); inner.append(q)
            else: inner.append(p)
        for z in S:
            bits=[k for k in range(3) if ((z^base)>>k)&1]
            if bits: edge(inner[bits[0]],inner[bits[1]])
    B=1+sum(w for _,_,w in edges)
    for a,b in g.edges: g[a][b]['weight']=B*(int(a in req)+int(b in req))-cost[frozenset((a,b))]
    M={frozenset(e) for e in nx.max_weight_matching(g,weight='weight')}
    covered=set().union(*M) if M else set()
    if not req<=covered: return None
    J=[i for i,e in enumerate(cross) if e in M]
    if sum(edges[i][2] for i in J)>K: return None
    x=parity(edges,J,len(masks)); assert all(a in m for a,m in zip(x,masks)); C['verified_local_lifts']+=1
    return J

def parity(edges,J,h):
    z=0
    for i in J:
        u,v,_=edges[i]; z^=(1<<u)^(1<<v)
    return tuple((z>>(2*j))&3 for j in range(h))

def support(edges,K,h):
    return {parity(edges,J,h) for mask in range(1<<len(edges)) for J in [[i for i in range(len(edges)) if (mask>>i)&1]] if sum(edges[i][2] for i in J)<=K}

def hull(xs):
    b={}
    for x in xs:
        while x:
            j=x.bit_length()-1
            if j in b: x^=b[j]
            else: b[j]=x; break
    return b

def inspan(x,b):
    while x:
        j=x.bit_length()-1
        if j not in b:return False
        x^=b[j]
    return True

def close(F,T):
    # exact affine hulls for unconditioned guard supports; delete impossible guards only
    F=[(H,list(G)) for H,G in F]; target=sum(t<<(2*j) for j,t in enumerate(T))
    def pack(H,x): return sum(a<<(2*j) for j,a in zip(H,x))
    def directions(H,g):
        E,O,K=g
        return [pack(H,parity(E,[i],len(H))) for i,(_,_,w) in enumerate(E) if w<=K]
    while True:
        C['closure_passes']+=1
        if any(not G for H,G in F):return None
        offsets=[pack(H,G[0][1]) for H,G in F]
        dirs=[[pack(H,g[1])^o for g in G]+[d for g in G for d in directions(H,g)] for (H,G),o in zip(F,offsets)]
        changed=False
        for i,(H,G) in enumerate(F):
            other=target
            for j,o in enumerate(offsets):
                if j!=i: other^=o
            base=[d for j,D in enumerate(dirs) if j!=i for d in D]
            keep=[g for g in G if inspan(other^pack(H,g[1]),hull(base+directions(H,g)))]
            if len(keep)<len(G):
                C['guards_removed']+=len(G)-len(keep); F[i]=(H,keep); changed=True; break
        if not changed:return F

def solve(F,T):
    F=close(F,T)
    if F is None:return None
    A=nx.Graph(); A.add_nodes_from(('f',i) for i in range(len(F))); A.add_nodes_from(('h',j) for j in range(len(T)))
    for i,(H,G) in enumerate(F): A.add_edges_from((('f',i),('h',j)) for j in H)
    assert nx.is_forest(A)
    def rec(v,p):
        ch=[w for w in A[v] if w!=p]; msgs=[rec(w,v) for w in ch]; out={}
        if v[0]=='h':
            D={0:{}}
            for m in msgs:
                D={a^b:{**x,**y} for a,x in D.items() for b,y in m.items()}
            for a,x in D.items():out[a^T[v[1]]]=x
        else:
            i=v[1]; H,G=F[i]; idx={j:k for k,j in enumerate(H)}
            for a in range(4) if p else [0]:
                masks=[set(range(4)) for j in H]
                for w,m in zip(ch,msgs):masks[idx[w[1]]]=set(m)
                if p:masks[idx[p[1]]]={a}
                for E,O,K in G:
                    J=local(E,[{z^o for z in M} for M,o in zip(masks,O)],K)
                    if J is None:continue
                    raw=parity(E,J,len(H)); vals=tuple(x^y for x,y in zip(raw,O))
                    x={i:(E,O,K,J,vals)}
                    for w,m in zip(ch,msgs):x.update(m[vals[idx[w[1]]]])
                    out[a]=x;break
        return out
    W={}
    for comp in nx.connected_components(A):
        root=min(comp); m=rec(root,None)
        if 0 not in m:return None
        W.update(m[0])
    check=[0]*len(T)
    for i,(E,O,K,J,vals) in W.items():
        assert sum(E[j][2] for j in J)<=K
        assert vals==tuple(a^b for a,b in zip(parity(E,J,len(O)),O))
        for j,v in zip(F[i][0],vals):check[j]^=v
    assert check==T and len(W)==len(F); C['verified_global_lifts']+=1
    return W

def reference(F,T):
    D={0}
    for H,G in F:
        V=set()
        for E,O,K in G:
            for x in support(E,K,len(H)):V.add(sum((a^b)<<(2*j) for j,a,b in zip(H,x,O)))
        D={a^b for a in D for b in V}
    return sum(t<<(2*j) for j,t in enumerate(T)) in D

def randguard(h):
    E=[(u,v,R.randrange(1,4)) for u,v in it.combinations(range(2*h),2) if R.random()<.4][:9]
    return E,tuple(R.randrange(4) for _ in range(h)),R.randrange(6)

def run():
    for h in [1,2,3]:
        for _ in range(80):
            E,O,K=randguard(h); masks=[{a for a in range(4) if R.random()<.6} for j in range(h)]
            expect=any(all(a in m for a,m in zip(x,masks)) for x in support(E,K,h))
            got=local(E,masks,K) is not None; assert got==expect; C['local_tests']+=1; C['local_sat']+=got
    # all nonempty masks, both degree parities and all achievable port assignments checked
    for d in range(4):
        E=[(0,2,1)]*(d&1)+[(1,3,1)]*((d>>1)&1)
        for mask in range(1,16):
            M={a for a in range(4) if mask>>a&1}
            for a in range(4):
                for b in range(4):
                    masks=[M&{a},{b}]; assert (local(E,masks,2) is not None)==any(x[0] in masks[0] and x[1]==b for x in support(E,2,2));C['mask_tests']+=1
    for _ in range(80):
        Hn=2; Hs=[[0,1]]
        for i in range(R.randrange(1,5)):
            H=[R.randrange(Hn)]
            if R.random()<.7:H.append(Hn); Hn+=1
            Hs.append(H)
        F=[(H,[randguard(len(H)) for _ in range(R.randrange(1,5))]) for H in Hs]
        for _ in range(5):
            T=[R.randrange(4) for j in range(Hn)]; want=reference(F,T); got=solve(F,T) is not None
            assert got==want; C['tree_tests']+=1; C['tree_sat']+=got
    small=dict(C); scale=[]
    for h in [8,16,32,64,128]:
        E=[(2*j,2*j+1,1) for j in range(h)]; leaves=[([j],[([], (a,),0) for a in [0,1,2]]) for j in range(h)]
        for K in [h,h-1]:
            F=[(list(range(h)),[(E,(0,)*h,K)])]+leaves; before=C['matching_calls']; result=solve(F,[3]*h)
            assert (result is not None)==(K==h)
            scale.append(dict(h=h,budget=K,sat=result is not None,matching_calls=C['matching_calls']-before))
    return dict(seed=2010420,networkx=nx.__version__,small=small,scale=scale,total=dict(C))
if __name__=='__main__':print(json.dumps(run(),indent=2))
