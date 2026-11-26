import itertools as it, collections as C, random, json, math
import networkx as nx
import audit as old
from p4fg11_audit import src,verify,closure
from fg18 import local
INF=math.inf
T0=[(1,0,0,1),(0,0,1,1),(3,0,1,0),(0,1,0,1),(9,1,0,0),(0,1,1,0),(2,5,4,2),(4,2,3,4),(9,5,2,3),(5,4,3,4),(2,3,4,5),(4,4,2,4),(2,3,5,2),(3,3,5,5),(5,4,2,3),(4,7,4,5),(3,5,5,2),(5,2,3,3),(6,6,6,7),(7,6,7,7),(1,7,7,7),(7,7,7,6),(6,2,6,6),(7,6,6,6),(9,8,8,9),(8,8,9,9),(1,8,9,8),(8,9,8,9),(6,9,8,8),(8,9,9,8)]
PORT=[28,26,4,8]
def enumerate_words(rows,vars,pins):
    def rec(p):
        p=p.copy()
        while True:
            n=len(p)
            for row in rows:
                a=sum(p.get(j)==1 for j in row);u=[j for j in row if j not in p]
                if a>1 or not a and not u:return
                if a:p.update((j,0) for j in u)
                elif len(u)==1:p[u[0]]=1
            if n==len(p):break
        j=next((j for j in vars if j not in p),None)
        if j is None:yield p;return
        for b in (0,1):yield from rec({**p,j:b})
    yield from rec(pins)
def rows(T):return [[j for j,t in enumerate(T) if t[c]==v] for c in range(4) for v in range(len(T)//3)]
def region(inner,P,W):
    # actual RC12 certified 24/6 tuple shores; external stubs retain physical IDs.
    X=set(range(24) if inner else range(24,30));R=rows(T0);rids=[c*10+v for c in range(4) for v in (range(8) if inner else range(8,10))]
    R=[R[i] for i in rids];f={};lifts={}
    for w in range(16):
        p={j:b for j,b in P.items() if j in X};ok=True
        for i,j in enumerate(PORT):
            b=w>>i&1
            if j in p and p[j]!=b:ok=False
            p[j]=b
        if not ok:continue
        for z in enumerate_words(R,sorted(X),p):
            c=sum(W[j]*z[j] for j in X)
            if w not in f or c<f[w]:f[w]=c;lifts[w]={j:z[j] for j in X}
    return f,lifts

def binary_fiber(f,p,b):
    return {w:c for w,c in f.items() if ((w>>p ^ w>>(p+1))&1)==b}

def to_binary(f):
    # Find exact within-factor constant/literal classes from actual support, not hull.
    L=[];maps=[];A=list(f)
    for j in range(4):
        s=tuple(w>>j&1 for w in A)
        if len(set(s))==1:maps.append((-1,s[0]));continue
        t=tuple(1-x for x in s)
        if s in L:maps.append((L.index(s),0))
        elif t in L:maps.append((L.index(t),1))
        else:maps.append((len(L),0));L.append(s)
    if len(L)>2:return None
    g={tuple(s[i] for s in L):f[w] for i,w in enumerate(A)}
    assert len(g)==len(f)
    return maps,g

def compile_binary(F):
    # F: four indexed ports with exact masks; signed equality graph, then binary cost terms.
    G=nx.Graph();G.add_node(-1);data=[]
    for E,f in F:
        if not f:return 'NO',None
        z=to_binary(f)
        if z is None:return 'UNKNOWN',None
        maps,g=z;rep={};G.add_nodes_from(E)
        for e,(i,b) in zip(E,maps):
            if i==-1:v=-1;d=b
            elif i in rep:v,c=rep[i];d=b^c
            else:rep[i]=(e,b);continue
            if G.has_edge(e,v) and G[e][v]['b']!=d:return 'NO',None
            G.add_edge(e,v,b=d)
        data.append((rep,g))
    Q={}
    for root in [-1]+sorted(v for v in G if v!=-1):
        if root in Q:continue
        Q[root]=(root,0);todo=[root]
        for u in todo:
            for v,d in G[u].items():
                t=Q[u][1]^d['b']
                if v in Q and Q[v]!=(root,t):return 'NO',None
                if v not in Q:Q[v]=(root,t);todo.append(v)
    terms=[]
    for rep,g in data:
        V=sorted(set(Q[e][0] for e,b in rep.values())-{-1});h={}
        for x in it.product((0,1),repeat=len(V)):
            z=dict(zip(V,x));z[-1]=0
            a=tuple(z[Q[e][0]]^Q[e][1]^b for i,(e,b) in sorted(rep.items()))
            if a in g:h[x]=g[a]
        if not h:return 'NO',None
        terms.append((V,h))
    return 'OK',(Q,terms)

def sat2(terms):
    G=nx.DiGraph();V=sorted({v for L,f in terms for v in L});G.add_nodes_from((v,b) for v in V for b in (0,1))
    for L,f in terms:
        for x in it.product((0,1),repeat=len(L)):
            if x in f:continue
            if not L:return None
            a=(L[0],x[0]);b=(L[-1],x[-1]);G.add_edge(a,(b[0],1-b[1]));G.add_edge(b,(a[0],1-a[1]))
    S=list(nx.strongly_connected_components(G));idx={u:i for i,s in enumerate(S) for u in s}
    if any(idx[v,0]==idx[v,1] for v in V):return None
    z={v:int(idx[v,1]<idx[v,0]) for v in V};assert all(tuple(z[v] for v in L) in f for L,f in terms);return z

def planar_xor(G):
    # exact dual T-join, including negative XOR weights, components and bridges
    z={}
    for V in nx.connected_components(G):
        H=G.subgraph(V).copy();ok,E=nx.check_planarity(H)
        if not ok:return None
        D={};seen=set();n=0
        for u,v in E.edges():
            if (u,v) in seen:continue
            C0=E.traverse_face(u,v,seen)
            for a,b in zip(C0,C0[1:]+C0[:1]):D[a,b]=n
            n+=1
        A=nx.Graph();A.add_nodes_from(range(n));odd=set();pref={}
        for u,v,d in H.edges(data=True):
            e=tuple(sorted((u,v)));w=d['w'];p=int(w<0);pref[e]=p;a,b=D[u,v],D[v,u]
            if a==b:continue
            if p:odd.symmetric_difference_update((a,b))
            if not A.has_edge(a,b) or A[a][b]['weight']>abs(w):A.add_edge(a,b,weight=abs(w),e=e)
        K=nx.Graph();K.add_nodes_from(odd);paths={}
        for a in sorted(odd):
            dist,ps=nx.single_source_dijkstra(A,a)
            for b in sorted(odd):
                if b>a:K.add_edge(a,b,weight=-dist[b]);paths[a,b]=ps[b]
        M=nx.max_weight_matching(K,maxcardinality=True);assert 2*len(M)==len(odd)
        for a,b in M:
            p=paths[tuple(sorted((a,b)))]
            for u,v in zip(p,p[1:]):pref[A[u][v]['e']]^=1
        root=-1 if -1 in V else min(V);z[root]=0;todo=[root]
        for u in todo:
            for v in H[u]:
                b=z[u]^pref[tuple(sorted((u,v)))];assert v not in z or z[v]==b
                if v not in z:z[v]=b;todo.append(v)
    return z

def weighted(terms):
    # test feasibility independently first; finite penalty paid and verified
    wit=sat2(terms)
    if wit is None:return INF,None,'2SAT NO'
    lo=sum(min(f.values()) for _,f in terms);hi=sum(max(f.values()) for _,f in terms);M=hi-lo+1
    G=nx.Graph();G.add_node(-1);constant=0
    def add(u,v,w):
        if u==v:return
        G.add_edge(u,v,w=w+(G[u][v]['w'] if G.has_edge(u,v) else 0))
    for L,f in terms:
        G.add_nodes_from(L);a=min(f.values());g=lambda *x:f.get(tuple(x),a+M)
        if not L:constant+=2*g();continue
        if len(L)==1:constant+=2*g(0);add(-1,L[0],2*(g(1)-g(0)));continue
        a,b,c,d=g(0,0),g(0,1),g(1,0),g(1,1);u,v=L;constant+=2*a
        add(-1,u,c+d-a-b);add(-1,v,b+d-a-c);add(u,v,b+c-a-d)
    G.remove_edges_from([(u,v) for u,v,d in G.edges(data=True) if d['w']==0]);z=planar_xor(G)
    if z is None:return None,None,'nonplanar apex'
    val=sum(f.get(tuple(z[v] for v in L),INF) for L,f in terms);assert val!=INF
    assert 2*val==constant+sum(d['w']*(z[u]^z[v]) for u,v,d in G.edges(data=True));return val,z,'dual matching'

def solve(F):
    s,data=compile_binary(F)
    if s!='OK':return (INF if s=='NO' else None),None,s
    Q,terms=data;v,z,stage=weighted(terms)
    if z is None:return v,None,stage
    z[-1]=0;w={e:z.get(r,0)^b for e,(r,b) in Q.items() if e!=-1}
    assert v==sum(f[sum(w[e]<<j for j,e in enumerate(E))] for E,f in F);return v,w,stage

def run():
    rng=random.Random(26112619);localcount=0;matchfail=0;weighted_admitted=0
    for parity in (0,1):
        S=[w for w in range(16) if w.bit_count()%2==parity]
        for mask in range(1,256):
            f={w:rng.randrange(-9,10) for i,w in enumerate(S) if mask>>i&1}
            for p in (0,1):
                for b in (0,1):
                    g=binary_fiber(f,p,b)
                    if not g:continue
                    # p=1 is cyclic adjacent (1,2); fg18 checks actual cyclic order.
                    assert to_binary(g) is not None
                    assert any(local(g,s) for s in it.product((1,-1),repeat=4))
                    localcount+=1;matchfail+=not old.wick(g);weighted_admitted+=1
    # abstract signed planar graphs with fields, including frustrated triangles; independent exhaustive optimum
    counts=C.Counter();cases=[]
    for k in range(200):
        n=3+k%7;edges=list(nx.cycle_graph(n).edges());terms=[]
        for u,v in edges:
            f={x:rng.randrange(-7,8) for x in it.product((0,1),repeat=2) if rng.random()<.86}
            if not f:f={(0,0):0}
            terms.append(([u,v],f))
        ref=min(sum(f.get(tuple(x[v] for v in L),INF) for L,f in terms) for x in it.product((0,1),repeat=n));v,z,stage=weighted(terms);assert v==ref;counts[stage]+=1
    # Hostile arbitrary-size frustrated signed zero-field triangular mesh: all couplings positive for equal, no fields.
    for k in (4,8,12,16):
        H=nx.grid_2d_graph(k,k);H.add_edges_from(((i,j),(i+1,j+1)) for i in range(k-1) for j in range(k-1));H=nx.convert_node_labels_to_integers(H);terms=[([u,v],{(0,0):1,(1,1):1,(0,1):0,(1,0):0}) for u,v in H.edges()];v,z,stage=weighted(terms);assert v is not None;cases.append({'grid':k,'vertices':len(H),'edges':H.number_of_edges(),'cost':v,'stage':stage})
    # Native RC12, full source closure on 24 weighted guarded controls, same original IDs and cap rotation.
    src(T0,10);R=rows(T0);native=[]
    for k in range(24):
        W=[rng.randrange(-7,8) for _ in T0];P={} if k==0 else ({28:1,8:k%2} if k<5 else {rng.randrange(30):rng.randrange(2) for _ in range(k%5)})
        allz=list(enumerate_words(R,list(range(30)),P));ref=min((sum(W[j]*z[j] for j in range(30)) for z in allz),default=INF);Q=closure(T0,10,P)
        if Q is None:assert ref==INF;native.append({'stage':'source closure NO','cost':None});continue
        f,L=region(True,Q,W);g,K=region(False,Q,W);best=INF;st=[]
        for b in (0,1):
            a,h=binary_fiber(f,0,b),binary_fiber(g,0,b);v,w,s=solve([(list(range(4)),a),(list(range(4)),h)]);st.append(s)
            assert v is not None
            if v<best:
                m=sum(w[i]<<i for i in range(4));zz={**L[m],**K[m]};assert verify(T0,10,P,[j for j in zz if zz[j]]) and sum(W[j]*zz[j] for j in zz)==v;best=v
        assert best==ref;native.append({'stage':'binary fibers','cost':best,'branches':st})
    # genuine connected source chain with shared parity. Structural proof checks actual GF2 implication.
    chains=[]
    for k in (1,2,4,8,16):
        T=[tuple(v+10*i for v in t) for i in range(k) for t in T0];T=list(map(list,T))
        for i in range(k-1):
            c=1+i%2;a=30*i+29;b=a+30;T[a][c],T[b][c]=T[b][c],T[a][c]
        T=list(map(tuple,T));src(T,10*k);GG=nx.Graph();GG.add_nodes_from(range(70*k));GG.add_edges_from((j,30*k+c*10*k+v) for j,t in enumerate(T) for c,v in enumerate(t));assert nx.is_connected(GG)
        A={};assert all(old.add(A,sum(1<<j for j in r),1) for r in rows(T))
        assert all(old.norm(A,(1<<(30*i+28))^(1<<(30*i+26))^(1<<29),1)==(0,0) for i in range(k))
        W=[rng.randrange(-7,8) for _ in T];best=INF;st=[]
        for b in (0,1):
            tot=0;Z=[]
            for i in range(k):
                w=W[30*i:30*i+30];f,L=region(True,{},w);g,K=region(False,{29:b},w);v,z,s=solve([(list(range(4)),binary_fiber(f,0,1^b)),(list(range(4)),binary_fiber(g,0,1^b))]);assert v not in (INF,None);st.append(s);m=sum(z[j]<<j for j in range(4));q={**L[m],**K[m]};Z.extend(30*i+j for j in q if q[j]);tot+=v
                ref=min(sum(w[j]*q[j] for j in range(30)) for q in enumerate_words(R,list(range(30)),{29:b}));assert ref==v
            assert verify(T,10*k,{},Z) and sum(W[j] for j in Z)==tot;best=min(best,tot)
        chains.append({'tuples':len(T),'rank':1,'weighted_optimum':best,'fiber_solves':len(st)})
    out={'seed':26112619,'local_fibers':localcount,'weighted_matching_declines':matchfail,'abstract':dict(counts),'mesh':cases,'native':native,'chains':chains};print(json.dumps(out,indent=2));return out
if __name__=='__main__':
    out=run();open('fg19_results.json','w').write(json.dumps(out,indent=2)+'\n')
