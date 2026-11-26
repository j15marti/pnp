import itertools as it, random, json
import networkx as nx

def parity(x): return x.bit_count() & 1

def equations(n,T):
    return [(sum(1<<i for i,t in enumerate(T) if t[c]==v),1) for c in range(3) for v in range(n)]

def chart(m,E):
    B={}
    for a,b in E:
        for j in sorted(B):
            if a>>j&1: a^=B[j][0]; b^=B[j][1]
        if not a:
            if b:return None
            continue
        j=(a&-a).bit_length()-1
        for k,(u,v) in list(B.items()):
            if u>>j&1:B[k]=(u^a,v^b)
        B[j]=(a,b)
    F=[i for i in range(m) if i not in B]
    P=[(1<<i,0) for i in range(m)]
    for j,(a,b) in B.items():P[j]=(a^(1<<j),b)
    return P,F

def source_ok(n,T,s):return all(sum((s>>i)&1 for i,t in enumerate(T) if t[c]==v)==1 for c in range(3) for v in range(n))

def planar(n,T):
    G=nx.Graph();G.add_nodes_from(range(3*n+len(T)))
    for i,t in enumerate(T):G.add_edges_from((3*n+i,c*n+t[c]) for c in range(3))
    return nx.check_planarity(G)[0]

def close(n,T,pins,probe=True):
    m=len(T); E=equations(n,T); pins=dict(pins)
    while True:
        old=len(pins)
        for a,_ in E:
            I=[i for i in range(m) if a>>i&1]; yes=[i for i in I if pins.get(i)==1]; free=[i for i in I if i not in pins]
            if len(yes)>1 or not yes and not free:return None
            if yes:
                for i in free:pins[i]=0
            elif len(free)==1:pins[free[0]]=1
        for c,d in [(0,1),(0,2),(1,2)]:
            G=nx.Graph();G.add_nodes_from(range(2*n))
            for i,t in enumerate(T):
                if pins.get(i)!=0:G.add_edge(t[c],n+t[d])
            M=nx.bipartite.maximum_matching(G,top_nodes=list(range(n)))
            if len(M)!=2*n:return None
        C=chart(m,E+[(1<<i,b) for i,b in pins.items()])
        if C is None:return None
        for i,(a,b) in enumerate(C[0]):
            if not a:pins[i]=b
        if len(pins)>old:continue
        if probe:
            for i in range(m):
                if i in pins:continue
                for b in (0,1):
                    if close(n,T,{**pins,i:b},False) is None:
                        pins[i]=1-b;break
                if len(pins)>old:break
        if len(pins)==old:return pins

def compress(P):
    G={};base=0
    for a,b in P:
        if not a:base+=b
        else:G.setdefault(a,[0,0])[b]+=1
    L=[];W=[];D=[]
    for a,(p,q) in sorted(G.items()):
        base+=min(p,q)
        if p==q:continue
        L.append(a);W.append(abs(p-q));D.append(int(p<q))
    # y_i = L_i z XOR D_i; relations on y from row dependencies
    B={};H=[]
    for i,a in enumerate(L):
        u=a; mask=1<<i
        for j in sorted(B):
            if u>>j&1:u^=B[j][0];mask^=B[j][1]
        if u:B[(u&-u).bit_length()-1]=(u,mask)
        else:H.append((mask,parity(mask & sum(b<<i for i,b in enumerate(D)))))
    return base,L,W,D,H

def tjoin(W,H):
    # sufficient certificate: each column has <=2 nonzero entries in these rows
    r=len(H); target={i for i,(_,b) in enumerate(H) if b}
    if len(target)%2:target.add(r)
    G=nx.Graph();G.add_nodes_from(range(r+1))
    for j,w in enumerate(W):
        u=[i for i,(a,b) in enumerate(H) if a>>j&1]
        if len(u)>2:return 'UNKNOWN',None
        if not u:continue
        if len(u)==1:u.append(r)
        a,b=u
        if not G.has_edge(a,b) or w<G[a][b]['weight']:G.add_edge(a,b,weight=w,j=j)
    sol=0
    for C in nx.connected_components(G):
        Q=sorted(C&target)
        if len(Q)%2:return 'INFEASIBLE',None
        K=nx.Graph();K.add_nodes_from(Q);paths={}
        for a,b in it.combinations(Q,2):
            p=nx.shortest_path(G,a,b,weight='weight');paths[a,b]=p
            K.add_edge(a,b,weight=sum(G[u][v]['weight'] for u,v in zip(p,p[1:])))
        for a,b in nx.min_weight_matching(K):
            p=paths[tuple(sorted((a,b)))]
            for u,v in zip(p,p[1:]):sol^=1<<G[u][v]['j']
    assert all(parity(a&sol)==b for a,b in H)
    return 'OK',sol

def terminal(n,T,pins):
    C=chart(len(T),equations(n,T)+[(1<<i,b) for i,b in pins.items()])
    if C is None:return 'NO',None,None
    P,F=C;base,L,W,D,H=compress(P)
    status,y=tjoin(W,H)
    if status!='OK':return status,None,None
    Q=chart(len(T),[(a,((y>>i)&1)^D[i]) for i,a in enumerate(L)])
    assert Q is not None
    z=sum(b<<i for i,(a,b) in enumerate(Q[0]))
    s=sum((parity(a&z)^b)<<i for i,(a,b) in enumerate(P))
    cost=base+sum(w for i,w in enumerate(W) if y>>i&1)
    assert s.bit_count()==cost and all(parity(a&s)==b for a,b in equations(n,T)) and all((s>>i&1)==b for i,b in pins.items())
    if cost==n:assert source_ok(n,T,s)
    return ('YES' if cost==n else 'NO'),cost,s

def run():
    rng=random.Random(20261125);stats={};examples={}
    def inc(k):stats[k]=stats.get(k,0)+1
    def test(n,T):
        assert planar(n,T);m=len(T); E=equations(n,T)
        for pins in [{}, *({i:b} for i in range(min(m,2)) for b in (0,1))]:
            W=[s for s in range(1<<m) if all(parity(a&s)==b for a,b in E) and all(s>>i&1==b for i,b in pins.items())]
            truth=any(source_ok(n,T,s) for s in W);inc('SAT' if truth else 'UNSAT')
            for mode,p in [('raw',pins),('closed',close(n,T,pins))]:
                if p is None:
                    assert not truth;inc('closure_NO');continue
                label,cost,s=terminal(n,T,p);inc(mode+'_'+label)
                if label in ('YES','NO'):
                    assert (label=='YES')==truth
                    if cost is not None:
                        WW=[s for s in W if all(s>>i&1==b for i,b in p.items())]
                        assert cost==min(s.bit_count() for s in WW);inc('minimum_checks')
                        if mode=='raw' and label=='NO':examples.setdefault('raw_minimum_NO',{'n':n,'T':T,'pins':pins,'min':cost})
    all2=list(it.product(range(2),repeat=3))
    for mask in range(1,256):test(2,[t for i,t in enumerate(all2) if mask>>i&1])
    all3=list(it.product(range(3),repeat=3))
    for _ in range(120):
        T=sorted(rng.sample(all3,rng.randint(5,11)))
        if planar(3,T):test(3,T)
        else:inc('nonplanar_skipped')
    # Scalable planar cycle: X,Y pair i; two possible Z labels i and i+1. All variables linked by degree-two equations.
    for n in (16,64,256):
        T=[(i,i,j) for i in range(n) for j in (i,(i+1)%n)]
        assert planar(n,T)
        label,cost,s=terminal(n,T,{})
        assert label=='YES' and cost==n;inc('large_cycle_YES')
        T=T[:-1];assert planar(n,T)
        assert terminal(n,T,{})[0]=='YES';inc('large_neighbor_YES')
        T=T[:-1];assert planar(n,T)
        assert close(n,T,{}) is None;inc('large_neighbor_NO')
    print(json.dumps({'seed':20261125,'stats':stats,'examples':examples},sort_keys=True))
if __name__=='__main__':run()
