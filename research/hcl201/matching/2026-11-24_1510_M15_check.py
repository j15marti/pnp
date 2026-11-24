import itertools as it, json, random, math
import networkx as nx
R=random.Random(20115)

def gadget(G,d,k):
    # All ports appear left-to-right at the bottom boundary.
    if not 0<=k<=d: raise ValueError('bad demand')
    def node():
        v=len(G); G.add_node(v); return v
    def pair():
        a,b=node(),node(); G.add_edge(a,b); return a,b
    grid=[[pair() for _ in range(d)] for _ in range(k)]
    ports=[pair() for _ in range(d)]
    for i in range(k):
        s=node(); G.add_edge(s,grid[i][0][0])
        for j in range(d):
            a,b=grid[i][j]
            if j+1<d: G.add_edge(b,grid[i][j+1][0])
            G.add_edge(b,grid[i+1][j][0] if i+1<k else ports[j][0])
    return [b for a,b in ports]

def matching(G):
    if nx.is_bipartite(G):
        top={v for v,c in nx.bipartite.color(G).items() if c==0}
        mm=nx.bipartite.maximum_matching(G,top_nodes=top)
        return {(u,v) for u,v in mm.items() if u<v} if len(mm)==len(G) else None
    M=nx.max_weight_matching(G,maxcardinality=True)
    return M if 2*len(M)==len(G) else None

def sign_orientation(G):
    ok,emb=nx.check_planarity(G); assert ok
    orient={tuple(sorted(e)):1 for e in G.edges()}
    # Each connected component must have even order if feasible.
    for comp in nx.connected_components(G):
        seen=set(); faces=[]; which={}
        for u in comp:
            for v in emb.neighbors_cw_order(u):
                if (u,v) in seen: continue
                f=emb.traverse_face(u,v,seen); j=len(faces)
                arcs=list(zip(f,f[1:]+f[:1])); faces.append(arcs)
                for a in arcs: which[a]=j
        if not faces: continue
        dual=nx.Graph(); dual.add_nodes_from(range(len(faces)))
        for u,v in G.subgraph(comp).edges():
            a,b=which[u,v],which[v,u]
            if a!=b: dual.add_edge(a,b,edge=tuple(sorted((u,v))))
        tree=nx.bfs_tree(dual,0); assert len(tree)==len(faces)
        for j in reversed(list(tree.nodes())[1:]):
            c=sum(orient[tuple(sorted((u,v)))]*(1 if u<v else -1)==1 for u,v in faces[j])
            if c%2==0:
                p=next(tree.predecessors(j)); e=dual[j][p]['edge']; orient[e]*=-1
    return orient

def pf(A):
    A=[r[:] for r in A]; n=len(A); prev=1; s=1
    if not n:return 1
    if n%2:return 0
    for k in range(0,n-1,2):
        j=next((j for j in range(k+1,n) if A[k][j]),None)
        if j is None:return 0
        if j!=k+1:
            A[j],A[k+1]=A[k+1],A[j]
            for r in A:r[j],r[k+1]=r[k+1],r[j]
            s=-s
        p=A[k][k+1]
        for i in range(k+2,n):
            for j in range(i+1,n):
                z=p*A[i][j]-A[k][i]*A[k+1][j]+A[k][j]*A[k+1][i]
                v,rem=divmod(z,prev); assert not rem
                A[i][j]=v; A[j][i]=-v
        prev=p
    return s*prev

def spectrum(G):
    # S14 one integer row + two syndrome bits. All weights exact.
    if matching(G) is None:return {}
    orient=sign_orientation(G); vs=list(G); ix={v:i for i,v in enumerate(vs)}
    h=len(vs)//2; E=list(G.edges(data=True)); base=1<<(len(E)+1)
    lo=min([0]+[a.get('w',0) for _,_,a in E]); hi=max([0]+[a.get('w',0) for _,_,a in E]); L=h*(hi-lo)
    def calc(lam,unit=False):
        A=[[0]*len(vs) for _ in vs]
        for u,v,a in E:
            i,j=ix[u],ix[v]; e=tuple(sorted((u,v)))
            w=1 if unit else base**(a.get('w',0)-lo)*(-1 if (lam&a.get('tag',0)).bit_count()%2 else 1)
            A[i][j]+=orient[e]*(1 if u<v else -1)*w; A[j][i]=-A[i][j]
        return pf(A)
    ref=calc(0,True); assert ref
    sg=1 if ref>0 else -1
    vals=[sg*calc(lam) for lam in range(4)]; out={}
    for t in range(4):
        z,rem=divmod(sum(v*(-1 if (t&lam).bit_count()%2 else 1) for lam,v in enumerate(vals)),4)
        assert not rem and z>=0
        for j in range(L+1):
            z,c=divmod(z,base)
            if c:out[j+h*lo,t]=c
        assert z==0
    assert sum(out.values())==abs(ref)
    return out

def compile_graph(n,edges,b,lo,hi):
    # edges: u,v,sign_u,sign_v,quota coefficient,tag. Distinct endpoints here.
    base=nx.Graph(); base.add_nodes_from(range(n)); base.add_edges_from((e[0],e[1]) for e in edges)
    ok,emb=nx.check_planarity(base); assert ok
    G=nx.Graph(); slots={}; groups={}; bb=list(b); w0=0;t0=0
    for j,(u,v,s,t,w,g) in enumerate(edges):
        bb[u]-=s*lo[j];bb[v]-=t*lo[j];w0+=w*lo[j];t0^=g if lo[j]%2 else 0
        for a in range(hi[j]-lo[j]):
            groups.setdefault((u,v),[]).append((j,a,0,s));groups.setdefault((v,u),[]).append((j,a,1,t))
    for u in range(n):
        order=[]
        for v in emb.neighbors_cw_order(u):
            g=groups.get((u,v),[]);order+=g if u<v else list(reversed(g))
        k=bb[u]+sum(s==-1 for j,a,p,s in order)
        if not 0<=k<=len(order):return None
        ports=gadget(G,len(order),k)
        for (j,a,p,s),v in zip(order,ports):slots[j,a,p]=v
    for j,(u,v,s,t,w,g) in enumerate(edges):
        for a in range(hi[j]-lo[j]):
            p,q=slots[j,a,0],slots[j,a,1]
            if s==t:
                G.add_edge(p,q,w=w*s,tag=g,j=j,delta=s)
                if s==-1:w0+=w;t0^=g
            else:
                z=len(G);G.add_node(z);positive,negative=(p,q) if s==1 else (q,p)
                G.add_edge(z,positive,w=w,tag=g,j=j,delta=1);G.add_edge(z,negative)
    return G,w0,t0

def values(n,edges,x):
    b=[0]*n; w=0;t=0
    for (u,v,s,r,c,g),a in zip(edges,x):
        b[u]+=s*a;b[v]+=r*a;w+=c*a;t^=g if a%2 else 0
    return b,(w,t)

def closure(n,edges,b,lo,hi):
    lo=lo[:];hi=hi[:];pins=0; scans=0
    while True:
        scans+=1;change=False
        for u in range(n):
            coeff=[(s if a==u else 0)+(t if v==u else 0) for a,v,s,t,_,_ in edges]
            mn=sum(min(c*l,c*h) for c,l,h in zip(coeff,lo,hi));mx=sum(max(c*l,c*h) for c,l,h in zip(coeff,lo,hi))
            if not mn<=b[u]<=mx:return None,pins,scans
            for j,c in enumerate(coeff):
                if not c or lo[j]==hi[j]:continue
                a=mn-min(c*lo[j],c*hi[j]);d=mx-max(c*lo[j],c*hi[j]); poss=[v for v in range(lo[j],hi[j]+1) if a<=b[u]-c*v<=d]
                if not poss:return None,pins,scans
                if len(poss)==1:
                    lo[j]=hi[j]=poss[0];pins+=1;change=True;break
            if change:break
        if not change:return (lo,hi),pins,scans

def main():
    stats=dict(seed=20115,local_masks=0,local_sat=0,local_unsat=0,random_systems=0,sat=0,unsat=0,targets=0,target_sat=0,target_unsat=0,pins=0,closure_scans=0,planarity_checks=0,pfaffian_blocks=0,verified_lifts=0,max_vertices=0,max_edges=0)
    for d in range(7):
        for k in range(d+1):
            G=nx.Graph();p=gadget(G,d,k);assert nx.check_planarity(G)[0];stats['planarity_checks']+=1
            for mask in range(1<<d):
                H=G.copy();H.remove_nodes_from(p[i] for i in range(d) if mask>>i&1)
                ok=matching(H) is not None;assert ok==(mask.bit_count()==k)
                stats['local_masks']+=1;stats['local_sat' if ok else 'local_unsat']+=1
    G=nx.Graph();p=gadget(G,4,2);counts=[]
    for i,j in it.combinations(range(4),2):
        H=G.copy();H.remove_nodes_from([p[i],p[j]]);counts.append(spectrum(H)[0,0])
    assert counts[0]*counts[5]-counts[1]*counts[4]+counts[2]*counts[3]==0
    stats['exact2_counts_12_13_14_23_24_34']=counts
    for case in range(60):
        n=4;pool=list(it.combinations(range(n),2)); edges=[]
        for j in range(R.randint(3,6)):
            u,v=R.choice(pool);edges.append((u,v,R.choice([-1,1]),R.choice([-1,1]),R.randint(-2,2),R.randrange(4)))
        lo=[R.randrange(-1,2) for e in edges];hi=[a+R.randint(1,2) for a in lo]
        x=[R.randint(a,d) for a,d in zip(lo,hi)];b,_=values(n,edges,x)
        if case%2:b[R.randrange(n)]+=R.choice([-1,1])
        ref={}
        for x in it.product(*(range(a,d+1) for a,d in zip(lo,hi))):
            bb,t=values(n,edges,x)
            if bb==b:ref[t]=x
        c,pins,scans=closure(n,edges,b,lo,hi);stats['pins']+=pins;stats['closure_scans']+=scans
        stats['random_systems']+=1;stats['sat' if ref else 'unsat']+=1
        got={}
        if c is not None:
            l,u=c;out=compile_graph(n,edges,b,l,u)
            if out is not None:
                G,w0,t0=out;assert nx.check_planarity(G)[0];stats['planarity_checks']+=1
                stats['max_vertices']=max(stats['max_vertices'],len(G));stats['max_edges']=max(stats['max_edges'],G.number_of_edges())
                sp=spectrum(G);stats['pfaffian_blocks']+=bool(sp)
                got={(w+w0,t^t0):v for (w,t),v in sp.items()}
                M=matching(G)
                if M is not None:
                    xx=l[:]
                    for j,e in enumerate(edges):
                        if e[2]==e[3]==-1:xx[j]+=u[j]-l[j]
                    for a,d in M:
                        e=G[a][d]
                        if 'j' in e:xx[e['j']]+=e['delta']
                    bb,t=values(n,edges,xx);assert bb==b and t in ref and all(a<=x<=d for a,x,d in zip(lo,xx,hi));stats['verified_lifts']+=1
        assert set(got)==set(ref),(case,edges,b,lo,hi,got,ref)
        for w in range(-5,6):
            for t in range(4):
                stats['targets']+=1;stats['target_sat' if (w,t) in got else 'target_unsat']+=1
                assert ((w,t) in got)==((w,t) in ref)
    stats['scales']=[]
    for d,k in [(16,8),(32,16),(64,32)]:
        G=nx.Graph();p=gadget(G,d,k);assert nx.check_planarity(G)[0];stats['planarity_checks']+=1
        for j in [k,k-1,k+1]:
            H=G.copy();H.remove_nodes_from(p[:j]);assert (matching(H) is not None)==(j==k)
        stats['scales'].append(dict(d=d,k=k,vertices=len(G),edges=G.number_of_edges(),controls=3))
    print(json.dumps(stats,sort_keys=True))
if __name__=='__main__':main()
