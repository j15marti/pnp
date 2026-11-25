import itertools, random, json
from fractions import Fraction as Q
import networkx as nx

def pf(A):
    A=[list(map(Q,r)) for r in A]; z=Q(1); n=len(A)
    for i in range(0,n,2):
        j=next((j for j in range(i+1,n) if A[i][j]),None)
        if j is None:return Q(0)
        if j!=i+1:
            A[j],A[i+1]=A[i+1],A[j]
            for r in A:r[j],r[i+1]=r[i+1],r[j]
            z=-z
        p=A[i][i+1]; z*=p
        for j in range(i+2,n):
            for k in range(j+1,n):
                A[j][k]-=(A[i][j]*A[i+1][k]-A[i][k]*A[i+1][j])/p
                A[k][j]=-A[j][k]
    return z

def even_sum(G):
    # Edges carry nonzero integer A,B: unselected, selected.
    ok,emb=nx.check_planarity(G); assert ok
    H=nx.Graph(); ports={}; pairs=[]
    for v in G:
        ns=list(emb.neighbors_cw_order(v)); d=len(ns)
        if not d:continue
        groups=[ns] if d<=3 else [ns[:2]]+[[a] for a in ns[2:-2]]+[ns[-2:]]
        local=[]
        for i,grp in enumerate(groups):
            P=[]
            for w in grp:
                p=len(ports)+len(pairs)*0 # actual label is a tuple
                p=('p',v,w);ports[v,w]=p;P.append(p)
            if i:P.append(('a',v,i-1,1))
            if i+1<len(groups):P.append(('a',v,i,0))
            H.add_nodes_from(P)
            for a,b in itertools.combinations(P,2):H.add_edge(a,b,w=Q(1))
            if i:
                a,b=('a',v,i-1,0),('a',v,i-1,1)
                H.add_edge(a,b,w=Q(1));pairs.append((a,b))
    scale=1
    for u,v,d in G.edges(data=True):
        a,b=ports[u,v],ports[v,u]; A,B=d['ab']; assert B
        H.add_edge(a,b,w=Q(A,B));pairs.append((a,b));scale*=B
    order=[p for pair in pairs for p in pair]; assert len(order)==len(H)
    idx={p:i for i,p in enumerate(order)}
    orientation={tuple(sorted((idx[a],idx[b]))):1 for a,b in H.edges()}
    def arrow(a,b):
        i,j=idx[a],idx[b];return orientation[tuple(sorted((i,j)))]*(1 if i<j else -1)
    for comp in nx.connected_components(H):
        ok,em=nx.check_planarity(H.subgraph(comp));assert ok
        faces=[]; lookup={}; seen=set()
        for a,b in em.edges():
            if (a,b) in seen:continue
            f=em.traverse_face(a,b,seen); e=list(zip(f,f[1:]+f[:1]))
            for edge in e:lookup[edge]=len(faces)
            faces.append(e)
        D=nx.Graph();D.add_nodes_from(range(len(faces)))
        for a,b in H.subgraph(comp).edges():
            i,j=lookup[a,b],lookup[b,a]
            if i!=j:D.add_edge(i,j,edge=(a,b))
        if faces:
            tree=nx.bfs_tree(D,0); assert len(tree)==len(faces)
            for i in reversed(list(tree)[1:]):
                if sum(arrow(a,b)==1 for a,b in faces[i])%2==0:
                    par=next(tree.predecessors(i));a,b=D[i][par]['edge'];key=tuple(sorted((idx[a],idx[b])));orientation[key]*=-1
            assert all(sum(arrow(a,b)==1 for a,b in faces[i])%2==1 for i in range(1,len(faces)))
    M=[[Q(0) for p in order] for p in order]
    for a,b,d in H.edges(data=True):
        i,j=idx[a],idx[b];M[i][j]=arrow(a,b)*d['w'];M[j][i]=-M[i][j]
    sign=1
    for a,b in pairs:sign*=arrow(a,b)
    ans=sign*scale*pf(M);assert ans.denominator==1
    return int(ans)

def core_sum(n,edges,T):
    G=nx.Graph();G.add_nodes_from(range(n));scale=1
    for u,v,w0,w1 in edges:
        A,B=w0+w1,w0-w1
        if not B:scale*=A
        else:G.add_edge(u,v,ab=(A,B))
    for comp in nx.connected_components(G):
        ts=[v for v in sorted(comp) if T>>v&1]
        if len(ts)%2:return 0
        for a,b in zip(ts[::2],ts[1::2]):
            p=nx.shortest_path(G,a,b)
            for u,v in zip(p,p[1:]):G[u][v]['ab']=G[u][v]['ab'][::-1]
    ans=Q(scale*even_sum(G)*2**n,2**len(edges));assert ans.denominator==1
    return int(ans)

def weighted(n,edges,guards):
    # Deterministic greedy planar core; all removed pair factors share a row span with guards.
    G=nx.Graph();G.add_nodes_from(range(n));core=[];rest=[]
    for u,v,w0,w1 in edges:
        G.add_edge(u,v)
        if nx.check_planarity(G)[0]:core.append((u,v,w0,w1))
        else:G.remove_edge(u,v);rest.append((u,v,w0,w1))
    basis=[];piv={}
    def coords(x):
        y=0
        while x:
            p=x.bit_length()-1
            if p not in piv:
                j=len(basis);basis.append(x);piv[p]=(x,j)
            v,j=piv[p];x^=v;y^=1<<j
        return y
    re=[(coords((1<<u)^(1<<v)),a,b) for u,v,a,b in rest]
    gu=[(coords(a),b) for a,b in guards];r=len(basis)
    if r>10:return None, len(rest),r
    h=[]
    for z in range(1<<r):
        val=1
        for a,b in gu:
            if (a&z).bit_count()%2!=b:val=0;break
        if val:
            for a,b,c in re:val*=c if (a&z).bit_count()%2 else b
        h.append(val)
    for i in range(r):
        for j in range(1<<r):
            if not j>>i&1:
                a,b=h[j],h[j|1<<i];h[j],h[j|1<<i]=a+b,a-b
    z=0
    for l,v in enumerate(h):
        if v:
            T=0
            for i,b in enumerate(basis):
                if l>>i&1:T^=b
            z+=v*core_sum(n,core,T)
    assert z%(1<<r)==0
    return z//(1<<r),len(rest),r

def edge_registry(n,owners):
    base=1<<(n+1);D={}
    for vs,sign in owners:
        for i,j in itertools.combinations(range(3),2):
            u,v=sorted((vs[i],vs[j]));a,b=D.get((u,v),(1,1));p=1^((sign>>i)&1)^((sign>>j)&1)
            D[u,v]=(a*(base if p==0 else 1),b*(base if p==1 else 1))
    return [(u,v,a,b) for (u,v),(a,b) in sorted(D.items())],base

def brute(n,edges,guards):
    z=0
    for x in range(1<<n):
        if any((x&a).bit_count()%2!=b for a,b in guards):continue
        p=1
        for u,v,a,b in edges:p*=b if ((x>>u)^(x>>v))&1 else a
        z+=p
    return z

def closure(owners,guards):
    # Exact affine support of each actual ternary owner under current necessary equations.
    piv={}; added=0; scans=0
    def reduce(a,b,P):
        while a:
            j=a.bit_length()-1
            if j not in P:break
            v,w=P[j];a^=v;b^=w
        return a,b
    def push(a,b,P):
        a,b=reduce(a,b,P)
        if not a:return -1 if b else 0
        P[a.bit_length()-1]=(a,b);return 1
    for a,b in guards:
        if push(a,b,piv)<0:return False,added,scans
    while True:
        changed=False
        for vs,sign in owners:
            scans+=1;live=[]
            for w in range(8):
                if w^sign in (0,7):continue
                P=piv.copy()
                if all(push(1<<v,w>>i&1,P)>=0 for i,v in enumerate(vs)):live.append(w)
            if not live:return False,added,scans
            for m in range(1,8):
                values={(m&w).bit_count()%2 for w in live}
                if len(values)!=1:continue
                a=sum(1<<v for i,v in enumerate(vs) if m>>i&1)
                k=push(a,next(iter(values)),piv)
                if k<0:return False,added,scans
                if k:added+=1;changed=True;break
            if changed:break
        if not changed:return True,added,scans

def run():
    rng=random.Random(20261125); jobs=0;labels=[0,0];maxrank=0;maxdeleted=0;fano=[]; deductions=0; closure_scans=0; closure_conflicts=0
    F=[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
    cases=[(7,[(v,0) for v in F],[])]
    for i in range(7):
        for s in (1,2,4):cases.append((7,[(v,s if i==j else 0) for j,v in enumerate(F)],[]))
    for _ in range(24):
        n=rng.randrange(3,8);owners=[(tuple(rng.sample(range(n),3)),rng.randrange(8)) for j in range(rng.randrange(1,8))];guards=[(rng.randrange(1,1<<n),rng.randrange(2)) for j in range(rng.randrange(3))];cases.append((n,owners,guards))
    for j,(n,owners,guards) in enumerate(cases):
        live,d,s=closure(owners,guards);deductions+=d;closure_scans+=s;closure_conflicts+=not live
        edges,base=edge_registry(n,owners);a,k,r=weighted(n,edges,guards);b=brute(n,edges,guards);assert a==b
        count=(a//base**(2*len(owners)))%base;assert live or count==0;labels[bool(count)]+=1;jobs+=1;maxrank=max(maxrank,r);maxdeleted=max(maxdeleted,k)
        if j<22:fano.append(count)
    # high-degree planar wheel, negative signed factors and arbitrary spin insertion
    for n in range(4,9):
        G=nx.wheel_graph(n);E=[(u,v,2+(u+v)%3,1+(u*v)%4) for u,v in G.edges()];
        for T in (0,3,7,(1<<n)-1):
            a=core_sum(n,E,T);b=sum((-1)**((x&T).bit_count()%2)*__import__('math').prod(w1 if ((x>>u)^(x>>v))&1 else w0 for u,v,w0,w1 in E) for x in range(1<<n));assert a==b;jobs+=1
    BW=[[0,8,22],[9,4,15],[5,21,18],[10,23,16],[19,6,17],[12,14,2],[7,11,13],[3,1,20],[0,17,21],[19,7,20],[22,6,15],[12,3,5],[16,13,8],[1,11,14],[9,2,10],[18,23,4],[0,6,7],[14,16,3],[21,22,9],[19,11,15],[5,23,13],[18,8,12],[1,10,4],[17,2,20],[0,5,9],[1,2,13],[11,6,8],[21,7,10],[12,15,16],[18,22,20],[14,23,17],[3,4,19]]
    assert closure([(v,0) for v in BW],[])==(True,0,32)
    E,_=edge_registry(24,[(v,0) for v in BW]);a,k,r=weighted(24,E,[]);assert a is None
    w=12130883;assert all(len({w>>v&1 for v in t})==2 for t in BW)
    print(json.dumps(dict(jobs=jobs,closure_deductions=deductions,closure_scans=closure_scans,closure_conflicts=closure_conflicts,guarded_nae_labels=labels,maxrank=maxrank,maxdeleted=maxdeleted,fano=fano,bw17=dict(edges=len(E),deleted=k,rank=r,source_witness=w,root_guard=[],local_singleton_closure='stagnant')),indent=2))
if __name__=='__main__':run()
