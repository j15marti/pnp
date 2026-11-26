import itertools as I, json, networkx as nx
from fractions import Fraction as F
from functools import lru_cache
PAIRS=[(0,15),(5,10),(3,12),(6,9)]
def signed(S):
    if not S:return None
    p=min(S).bit_count()%2
    if any(x.bit_count()%2!=p for x in S):return None
    N={x^p for x in S}; A=[(x,y) for x,y in PAIRS[:2] if x in N and y in N]; B=[(x,y) for x,y in PAIRS[2:] if x in N and y in N]
    if len(A)+len(B)==1:return None
    w={x:1 for x in N};twist=bool(A)!=bool(B)
    if twist:
        w={x:(-1 if x&3==3 else 1) for x in N}
    elif A:
        for x,y in A:w[x]=len(B)
        for x,y in B:w[x]=len(A)
    f={x^p:v for x,v in w.items()}
    assert w.get(0,0)*w.get(15,0)+w.get(5,0)*w.get(10,0)==w.get(3,0)*w.get(12,0)+w.get(6,0)*w.get(9,0)
    return f,twist,p

def gadget(w):
    a=min(w);flip=15^a;v={x^flip:F(y,w[a]) for x,y in w.items()};E={};ports=list(range(4));n=10
    def add(i,j,z):
        if z:E[tuple(sorted((i,j)))]=F(z)
    for i,j in [(0,1),(1,2),(2,3),(0,3)]:add(i,j,v.get(15^(1<<i)^(1<<j),0))
    for i,j,z in [(4,5,1),(4,8,1),(5,9,1),(8,9,-1),(8,7,1),(9,6,1),(7,6,1)]:add(i,j,z)
    for i in range(4):add(i,4+i,v.get(15^(1<<i)^(1<<(i+2)),0) if i<2 else 1)
    for i in range(4):
        if flip>>i&1:add(i,n,1);ports[i]=n;n+=1
    add(n,n+1,w[a]);n+=2
    return n,E,ports

def local_check(w):
    n,E,ports=gadget(w)
    @lru_cache(None)
    def pm(mask):
        if not mask:return F(1)
        i=(mask&-mask).bit_length()-1;rem=mask^(1<<i)
        return sum((z*pm(rem^(1<<j)) for (ii,j),z in E.items() if ii==i and rem>>j&1),F(0))
    assert all(pm(((1<<n)-1)^sum(1<<ports[i] for i in range(4) if s>>i&1))==w.get(s,0) for s in range(16))

def gfsolve(rows,n):
    piv={}
    for a,b in rows:
        while a:
            k=a.bit_length()-1
            if k in piv:a^=piv[k][0];b^=piv[k][1]
            else:piv[k]=(a,b);break
        if not a and b:return None
    free=[i for i in range(n) if i not in piv]
    def lift(x,affine):
        for i,(a,b) in sorted(piv.items()):
            if ((a&x).bit_count()%2)^(b if affine else 0):x^=1<<i
        return x
    return lift(0,True),[lift(1<<i,False) for i in free],free

def annihilator(S):
    a=min(S);return [(u,(u&a).bit_count()%2) for u in range(1,16) if all((u&(a^b)).bit_count()%2==0 for b in S)]

def project(v,ids):return sum(((v>>j)&1)<<i for i,j in enumerate(ids))

def compile_net(tables,ports,n):
    sig=[signed(S) for S in tables]
    if any(s is None for s in sig):return None
    rows=[];terms=[]
    for S,ids,(_,tw,p) in zip(tables,ports,sig):
        for u,b in annihilator(S):
            a=0
            for i,j in enumerate(ids):
                if u>>i&1:a^=1<<j
            rows.append((a,b))
        if tw:terms.append((ids[0],ids[1],p))
    z=gfsolve(rows,n)
    if z is None:return 'inconsistent'
    x0,B,free=z
    def q(x):return sum((((x>>i)&1)^p)*((x>>j)&1) for i,j,p in terms)%2
    def polar(a,b):return q(a^b^x0)^q(a^x0)^q(b^x0)^q(x0)
    # symplectic decomposition of the affine direction space, tracking original coordinates
    vec=[(v,1<<i) for i,v in enumerate(B)];pairs=[]
    while True:
        found=next(((i,j) for i in range(len(vec)) for j in range(i+1,len(vec)) if polar(vec[i][0],vec[j][0])),None)
        if found is None:break
        i,j=found;a,ac=vec[i];b,bc=vec[j];rest=[]
        for k,(v,c) in enumerate(vec):
            if k in (i,j):continue
            pa=polar(v,a);pb=polar(v,b)
            rest.append((v^(a if pb else 0)^(b if pa else 0),c^(ac if pb else 0)^(bc if pa else 0)))
        pairs.append((a,b));vec=rest
    # Coordinates of pair directions in original wire space: B(a, x+x0), B(b, x+x0).
    def form(v):
        # directly compute linear derivative with no affine constant
        return sum(1<<i for i in range(n) if polar(v,1<<i))
    L=[(form(a),form(b)) for a,b in pairs]
    # q(x)= q(x0)+linear(x+x0)+sum_j u_j v_j on affine hull.
    ell=0
    for i,b in zip(free,B):
        bit=q(x0^b)^q(x0)
        for u,v in L:bit^=((u&b).bit_count()%2)*((v&b).bit_count()%2)
        if bit:ell^=1<<i
    c=q(x0)^((ell&x0).bit_count()%2)
    # Convert shifted linear forms to wire parity, absorbing shift per factor.
    base=ell;coef=c
    for u,v in L:
        pu=(u&x0).bit_count()%2;pv=(v&x0).bit_count()%2
        if pu:base^=v
        if pv:base^=u
        coef^=pu*pv
    # numerator integer expansion 2^s times quadratic phase
    expansion={base:(-1)**coef}
    for u,v in L:
        nxt={}
        for a,z in expansion.items():
            for b,t in [(0,1),(u,1),(v,1),(u^v,-1)]:nxt[a^b]=nxt.get(a^b,0)+z*t
        expansion={a:z for a,z in nxt.items() if z}
    return sig,len(pairs)*2,expansion,2**len(pairs),q,x0,B

def pfaff(A):
    A=[list(map(F,row)) for row in A];v=F(1);n=len(A)
    if n%2:return F(0)
    for i in range(0,n,2):
        j=next((j for j in range(i+1,n) if A[i][j]),None)
        if j is None:return F(0)
        if j!=i+1:
            A[j],A[i+1]=A[i+1],A[j]
            for row in A:row[j],row[i+1]=row[i+1],row[j]
            v=-v
        p=A[i][i+1];v*=p
        for j in range(i+2,n):
            for k in range(j+1,n):
                A[j][k]-=(A[i][j]*A[i+1][k]-A[i][k]*A[i+1][j])/p;A[k][j]=-A[j][k]
    return v

def planar_sum(G):
    total=F(1)
    for comp in nx.connected_components(G):
        H=nx.convert_node_labels_to_integers(G.subgraph(comp));n=len(H)
        if n%2:return F(0)
        M=nx.max_weight_matching(H,maxcardinality=True,weight='unit')
        if len(M)*2!=n:return F(0)
        ok,emb=nx.check_planarity(H);assert ok
        edges=sorted(tuple(sorted(e)) for e in H.edges);ix={e:i for i,e in enumerate(edges)};seen=set();rows=[]
        for a,b in emb.edges():
            if (a,b) in seen:continue
            face=emb.traverse_face(a,b,seen);mask=0;par=0
            for a,b in zip(face,face[1:]+face[:1]):mask^=1<<ix[tuple(sorted((a,b)))];par^=int(a<b)
            rows.append((mask,par^1))
        orient=gfsolve(rows[:-1],len(edges));assert orient is not None
        z=orient[0];A=[[F(0)]*n for _ in range(n)]
        for i,(a,b) in enumerate(edges):A[a][b]=H[a][b]['weight']*(-1 if z>>i&1 else 1);A[b][a]=-A[a][b]
        # sign of reference matching ignoring all weights
        m=sorted(tuple(sorted(e)) for e in M);flat=[x for e in m for x in e];s=sum(a>b for i,a in enumerate(flat) for b in flat[i+1:])
        s+=sum((z>>ix[e])&1 for e in m)
        total*=(-1)**s*pfaff(A)
    return total

def graph_net(sig,ports,mask):
    G=nx.Graph();nodes={};off=0
    for (w,_,_),ids in zip(sig,ports):
        n,E,pp=gadget(w);G.add_nodes_from(range(off,off+n));G.add_weighted_edges_from((a+off,b+off,z) for (a,b),z in E.items())
        for p,j in zip(pp,ids):nodes.setdefault(j,[]).append(p+off)
        off+=n
    for j,ls in nodes.items():
        assert len(ls)==2;G.add_edge(*ls,weight=F(-1 if mask>>j&1 else 1))
    return G

def net_test(tables,ports,n,fkt=True):
    C=compile_net(tables,ports,n)
    if C is None:return None
    if C=='inconsistent':return {'rank':None,'positive':0,'evaluations':0}
    sig,r,E,d,q,x0,B=C
    vals=[];unsigned=0
    for x in range(1<<n):
        w=1
        for (f,_,_),ids in zip(sig,ports):w*=f.get(project(x,ids),0)
        if w:assert (-1)**q(x)*w>0;unsigned+=abs(w);vals.append((x,w))
    for a in range(1<<len(B)):
        x=x0
        for i,b in enumerate(B):
            if a>>i&1:x^=b
        assert sum(v*(-1)**((u&x).bit_count()%2) for u,v in E.items())==d*(-1)**q(x)
    num=0
    for u,v in E.items():
        expected=sum(w*(-1)**((u&x).bit_count()%2) for x,w in vals)
        if fkt:assert planar_sum(graph_net(sig,ports,u))==expected
        num+=v*expected
    assert num==unsigned*d
    return {'rank':r,'positive':unsigned,'evaluations':len(E),'twists':sum(t for _,t,_ in sig)}

Q=[t for t in I.product(range(2),repeat=3) if t not in [(0,0,0),(1,1,1)]]
S=[(0,0,2),(0,2,0),(0,2,2),(1,0,1),(1,1,0),(1,1,1),(2,0,1),(2,1,0),(2,2,2)]
U=[(0,0,2),(0,1,1),(0,3,0),(1,1,2),(1,1,3),(1,2,3),(2,0,1),(2,2,2),(2,2,3),(3,0,0),(3,3,0),(3,3,1)]
V=[tuple(map(int,t)) for t in '000 002 010 011 021 022 100 101 111 201 202 221'.split()]
def source_graph(T):
    G=nx.Graph();G.add_edges_from((('t',i),(c,v)) for i,t in enumerate(T) for c,v in enumerate(t));return G

def prism(k):
    # Properly 3-edge-coloured prism, each coloured edge is an element.
    cs=[i%2 for i in range(k)]
    if k%2:cs[-1]=2
    g=nx.Graph();colored=[]
    for r in (0,1):
        for i,c in enumerate(cs):colored.append(((r,i),(r,(i+1)%k),c))
    for i in range(k):colored.append(((0,i),(1,i),3-cs[i]-cs[(i-1)%k]))
    ids=[0]*3;T={(r,i):[None]*3 for r in (0,1) for i in range(k)}
    for a,b,c in colored:
        z=ids[c];ids[c]+=1;T[a][c]=T[b][c]=z;g.add_edge(a,b)
    T=[tuple(t) for t in T.values()];G=source_graph(T)
    assert ids==[k]*3 and len(set(T))==2*k and nx.check_planarity(G)[0] and nx.is_connected(G)
    assert all(G.degree(v)==2 for v in G if v[0]!='t')
    for i in range(k):
        a,b=T[i],T[k+i];same=[c for c in range(3) if a[c]==b[c]];assert len(same)==1
        c=same[0];R={('t',i),('t',k+i),(c,a[c])};cut=[(u,v) if u[0]=='t' else (v,u) for u,v in G.edges() if (u in R)!=(v in R)];assert len(cut)==4
        w=sum(1<<j for j,(t,e) in enumerate(cut) if t==('t',i));assert signed({w,w^15}) is None
    sat=nx.is_bipartite(g);assert sat==(k%2==0)
    if sat:
        col=nx.bipartite.color(g);W=[T[i] for i,v in enumerate([(r,j) for r in (0,1) for j in range(k)]) if col[v]];assert len(W)==k and all(len({t[c] for t in W})==k for c in range(3))
    return {'n':k,'triples':2*k,'single_pair_defects':k,'exact_solutions':2 if sat else 0}

def source_audit(T):
    G=source_graph(T);ok,emb=nx.check_planarity(G);assert ok and nx.is_connected(G);n=max(max(t) for t in T)+1
    assert len(set(T))==len(T) and all({t[c] for t in T}==set(range(n)) for c in range(3))
    assert all(G.degree(v)>=2 for v in G if v[0]!='t')
    for c,d in I.combinations(range(3),2):
        for t in T:
            A=[(c,i) for i in range(n) if i!=t[c]];B=[(d,i) for i in range(n) if i!=t[d]];H=nx.Graph();H.add_nodes_from(A+B);H.add_edges_from(((c,u[c]),(d,u[d])) for u in T if u[c]!=t[c] and u[d]!=t[d]);assert len(nx.bipartite.maximum_matching(H,top_nodes=A))==2*(n-1)
    solutions=[p for p in I.combinations(range(len(T)),n) if all(len({T[i][c] for i in p})==n for c in range(3))]
    def table(R,cut):
        ts=sorted(v for v in R if v[0]=='t');out={}
        for vals in I.product((0,1),repeat=len(ts)):
            a=dict(zip(ts,vals))
            for b in I.product((0,1),repeat=4):
                wire=dict(zip(cut,b))
                if any(t in R and a[t]!=wire[t,e] for t,e in cut):continue
                if all(sum(a[w] if w in R else wire[w,v] for w in G[v])==1 for v in R if v[0]!='t'):out[sum(x<<i for i,x in enumerate(b))]=tuple(t[1] for t in ts if a[t])
        return out
    E=sorted((a,b) if a[0]=='t' else (b,a) for a,b in G.edges());vertices=list(G);ix={v:i for i,v in enumerate(vertices)};adj=[[] for v in vertices]
    for i,(a,b) in enumerate(E):adj[ix[a]].append((ix[b],i));adj[ix[b]].append((ix[a],i))
    def component(bad):
        seen={0};stack=[0]
        while stack:
            for b,i in adj[stack.pop()]:
                if i not in bad and b not in seen:seen.add(b);stack.append(b)
        return seen
    counts={'cuts':0,'twist_sides':0,'singleton_pair_sides':0,'mixed_or_empty_sides':0,'joint_admitted':0,'joint_twisted':0};examples=[]
    for ci in I.combinations(range(len(E)),4):
        R=component(set(ci))
        if len(R)==len(vertices):continue
        cut=[E[i] for i in ci];R={vertices[i] for i in R};C=set(G)-R
        if not nx.is_connected(G.subgraph(C)) or not all((t in R)!=(e in R) for t,e in cut):continue
        t,e=cut[0];start=(t,e) if t in R else (e,t);cur=start;order=[]
        for _ in range(2*G.number_of_edges()+5):
            a,b=cur
            if b not in R:order.append((a,b) if a[0]=='t' else (b,a));cur=(b,a)
            else:cur=(b,emb[b][a]['cw'])
            if cur==start:break
        assert len(order)==4;L,H=table(R,order),table(C,order);counts['cuts']+=1
        shared=set(L)&set(H);assert bool(shared)==bool(solutions)
        for x in shared:assert tuple(sorted(L[x]+H[x])) in solutions
        for M in (L,H):
            s=signed(set(M))
            if s is None:
                if M and len({x.bit_count()%2 for x in M})==1:counts['singleton_pair_sides']+=1
                else:counts['mixed_or_empty_sides']+=1
            elif s[1]:counts['twist_sides']+=1;examples.append({'cut':order,'masks':[sorted(L),sorted(H)]})
        if signed(set(L)) and signed(set(H)):
            counts['joint_admitted']+=1
            twisted=signed(set(L))[1] or signed(set(H))[1]
            counts['joint_twisted']+=int(twisted)
            # reverse the second disk order (0,3,2,1) for external incidence orientation
            rev=[0,3,2,1];HR={project(x,rev) for x in H}
            res=net_test([set(L),HR],[[0,1,2,3],rev],4,fkt=twisted)
            assert bool(res['positive'])==bool(solutions)
    return {'triples':len(T),'solutions':len(solutions),**counts,'examples':examples[:2]}

if __name__=='__main__':
    hist=[]
    for p in (0,1):
        W=[x for x in range(16) if x.bit_count()%2==p];h={'ordinary':0,'twist':0,'impossible':0}
        for bits in range(1,256):
            maskset={x for i,x in enumerate(W) if bits>>i&1};a=signed(maskset)
            if a is None:h['impossible']+=1;continue
            h['twist' if a[1] else 'ordinary']+=1;local_check(a[0])
        hist.append(h)
    # opposite four-port rotations, true and false neighbors, and cancellation.
    cross={0,5,10,15};cross_odd={x^1 for x in cross};positive={0,3,12,15};empty_intersection={3}
    networks=[]
    for A,B in [(cross,cross),(cross,{0,3,12,15}),(cross,empty_intersection),(cross_odd,cross_odd),(cross,cross_odd),(cross,set(x for x in range(16) if x.bit_count()%2==0)),(cross,{5,15})]:
        rev=[0,3,2,1];networks.append(net_test([A,{project(x,rev) for x in B}],[[0,1,2,3],rev],4))
    # scalable paired abstract networks: even number of twists on two shared phase classes.
    scale=[]
    for k in (2,4,8,16,32,64,128,256,512):
        # arrange 2k gates around a cycle; each has two adjacent incoming and two adjacent outgoing wires,
        # use cyclic port order (in A,in B,out B,out A) -> crossing transports swap phases.
        # Local cross constraints force two global phase classes for an even cycle.
        P=[[2*i,2*i+1,2*((i+1)%k)+1,2*((i+1)%k)] for i in range(k)]
        C=compile_net([cross]*k,P,2*k);assert C not in (None,'inconsistent');sig,r,E,d,q,x0,B=C;assert r==0 and len(B)==2 and len(E)==1
        for a,b in I.product((0,1),repeat=2):
            x=x0^(B[0] if a else 0)^(B[1] if b else 0);assert q(x)==0 and all(project(x,ids) in cross for ids in P)
        if k<=8:
            # ring embedding is planar after replacing the signed local gates; actual FKT
            assert planar_sum(graph_net(sig,P,next(iter(E))))==4
        scale.append({'gates':k,'wire_bits':2*k,'rank':r,'free_phases':len(B),'evaluations':len(E),'positive_weight':4,'fkt_executed':k<=8})
    print(json.dumps({'masks':hist,'abstract_networks':networks,'scale':scale,'prisms':[prism(k) for k in (4,5,8,9,16,17,32,33,64,65,128,129,256,257)],'source_cuts':[source_audit(t) for t in (Q,S,U,V,V+[(1,1,0)])]},indent=2))
