import itertools as it, collections as co, fractions as fr, json, hashlib, networkx as nx
F=fr.Fraction
ROWS=[[(3,0),(4,0),(2,0)],[(2,0),(1,0),(0,0)],[(3,0),(0,0),(5,0)],[(1,0),(0,0),(4,0)],[(1,0),(3,0),(0,1)],[(0,1),(5,0),(4,0)],[(5,0),(0,1),(2,0)]]
# Exact physical arrays recovered from C08-30; offsets and owner IDs preserved.
CAP=[[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[1,5,6],[2,3,7],[0,5,7],[1,3,8],[2,4,6]]
GAD=[[0,4,11],[1,5,7],[2,6,8],[3,9,10],[0,1,6],[2,7,10],[3,4,5],[1,8,10],[4,6,9],[2,5,11],[0,3,7],[4,7,8],[5,6,10],[1,3,11],[0,2,9]]
CUT=[[41,53,29],[30,17,0],[42,1,65],[18,2,54],[20,44,3],[4,66,56],[68,5,32]]
C=CAP+[[9+12*j+v for v in row] for j in range(5) for row in GAD]+CUT
P=[1,0,0,0,2,2,2,3,3,3]+[0]*0+([0]*4+[1]*3+[2]*4+[3]*4)*5+[1]*7
stats=co.Counter()
def nae(row,x): return len({x[v]^s for v,s in row})>1
def direct(rows,n,guards=()):
    counts=co.Counter()
    for x in it.product((0,1),repeat=n):
        stats['direct_words']+=1
        if all((x[u]^x[v])==s for u,v,s in guards): counts[sum(not nae(r,x) for r in rows)]+=1
    return dict(sorted(counts.items()))
def authenticate():
    assert len(C)==92 and len(P)==92
    for p in range(4): assert sorted(v for i,row in enumerate(C) if P[i]==p for v in row)==list(range(69))
    assert len({tuple(sorted(e)) for r in C for e in it.combinations(r,2)})==276
    portmap={};tables=[]
    for j,(off,n,rs,ports) in enumerate([(0,9,CAP,[0,1,2,3,4,5])]+[(9+12*k,12,GAD,[8,9,11]) for k in range(5)]):
        tab=co.Counter()
        for x in it.product((0,1),repeat=n):
            stats['native_local_words']+=1
            if all(len({x[v] for v in r})>1 for r in rs): tab[tuple(x[v] for v in ports)]+=1
        assert dict(tab)==({(0,0,0,1,1,1):6,(1,1,1,0,0,0):6} if j==0 else {(0,0,0):7,(1,1,1):7})
        for v in ports:portmap[off+v]=(j,int(j==0 and v>=3))
        tables.append({''.join(map(str,k)):v for k,v in tab.items()})
    assert [[portmap[v] for v in row] for row in CUT]==ROWS
    return tables

def pair_data(rows):
    d=co.defaultdict(lambda:[0,0]); const=0
    for row in rows:
        for (u,a),(v,b) in it.combinations(row,2):
            if u==v: const+=int(a==b)
            else:d[tuple(sorted((u,v)))][a^b]+=1
    edges={}
    for e,(a,b) in d.items():
        if a==b:const+=a
        else:edges[e]=(a,b)
    return const,edges

def planar_core(n,edges):
    G=nx.Graph();G.add_nodes_from(range(n));G.add_edges_from(sorted(edges));stats['planarity_tests']+=1
    if nx.check_planarity(G)[0]:return G,[]
    for e in sorted(edges):
        G.remove_edge(*e);stats['planarity_tests']+=1
        if nx.check_planarity(G)[0]:return G,[e]
        G.add_edge(*e)
    H=nx.Graph();H.add_nodes_from(range(n));deleted=[]
    for e in sorted(edges):
        H.add_edge(*e);stats['planarity_tests']+=1
        if not nx.check_planarity(H)[0]:H.remove_edge(*e);deleted.append(e)
    return H,deleted

def pf(A):
    A=[r[:] for r in A];n=len(A);out=F(1);stats['pfaffians']+=1
    for i in range(0,n,2):
        j=next((j for j in range(i+1,n) if A[i][j]),None)
        if j is None:return F(0)
        if j!=i+1:
            A[j],A[i+1]=A[i+1],A[j]
            for r in A:r[j],r[i+1]=r[i+1],r[j]
            out=-out
        p=A[i][i+1];out*=p
        for j in range(i+2,n):
            for k in range(j+1,n):
                A[j][k]-=(A[i][j]*A[i+1][k]-A[i][k]*A[i+1][j])/p
                A[k][j]=-A[j][k];stats['pf_updates']+=1
    return out

def dimer_sum(H,w):
    # Split high-degree vertices in rotation order into parity trees of max degree 3.
    ok,emb=nx.check_planarity(H);assert ok;stats['planarity_tests']+=1
    L=nx.Graph();port={};weights={}
    for v in H:
        ns=list(emb.neighbors_cw_order(v));d=len(ns)
        if not d:continue
        for i,u in enumerate(ns):
            node=(v,i);port[v,u]=node;L.add_node(node)
            if i:
                a=(v,i-1);L.add_edge(a,node);weights[frozenset((a,node))]=F(1)
    for u,v in H.edges:
        a,b=port[u,v],port[v,u];L.add_edge(a,b);weights[frozenset((a,b))]=w[tuple(sorted((u,v)))]
    assert max(dict(L.degree).values(),default=0)<=3
    # Each edge has two ports, each vertex's ports form K_d, d<=3.
    D=nx.Graph();dw={};external=[];scale=F(1)
    for a,b in L.edges:
        i,j=len(D),len(D)+1;D.add_edge(i,j);external.append((i,j));dw[tuple(sorted((i,j)))]=1/weights[frozenset((a,b))];scale*=weights[frozenset((a,b))]
        L[a][b]['ports']={a:i,b:j}
    for a in L:
        ports=[L[a][b]['ports'][a] for b in L[a]]
        for i,j in it.combinations(ports,2):D.add_edge(i,j);dw[tuple(sorted((i,j)))]=F(1)
    # Process each connected component; use a face-equation orientation, calibrated on the all-positive matrix.
    for cc in nx.connected_components(D):
        Q=D.subgraph(cc).copy();ok,E=nx.check_planarity(Q);assert ok;stats['planarity_tests']+=1
        ids=sorted(Q);edges=sorted(tuple(sorted(e)) for e in Q.edges);idx={e:i for i,e in enumerate(edges)}
        visited=set();eq=[]
        for a,b in E.edges():
            if (a,b) in visited:continue
            face=E.traverse_face(a,b,visited);mask=0;rhs=1
            for u,v in zip(face,face[1:]+face[:1]):
                mask^=1<<idx[tuple(sorted((u,v)))];rhs^=int(u<v)
            eq.append((mask,rhs))
        basis={}
        for mask,rhs in eq[1:]:
            while mask:
                i=mask.bit_length()-1
                if i not in basis:basis[i]=(mask,rhs);break
                m,r=basis[i];mask^=m;rhs^=r
            if not mask:assert rhs==0
        sol=0
        for i,(mask,rhs) in sorted(basis.items()):
            if ((mask&sol).bit_count()&1)!=rhs:sol|=1<<i
        # explicit check all bounded faces, including bridge walks
        assert all(((mask&sol).bit_count()&1)==rhs for mask,rhs in eq[1:])
        pos={v:i for i,v in enumerate(ids)};A=[[F(0) for _ in ids] for _ in ids];U=[[F(0) for _ in ids] for _ in ids]
        for e,k in idx.items():
            i,j=map(pos.get,e);sgn=-1 if (sol>>k)&1 else 1
            A[i][j]=sgn*dw[e];A[j][i]=-A[i][j];U[i][j]=F(sgn);U[j][i]=-U[i][j]
        ref=pf(U);assert ref;scale*=pf(A)*(1 if ref>0 else -1)
    return scale

def parity_sum(H,w,T):
    T=set(T);J=set()
    for cc in nx.connected_components(H):
        a=sorted(T&cc)
        if len(a)%2:return F(0)
        for u,v in zip(a[::2],a[1::2]):
            path=nx.shortest_path(H,u,v)
            for x,y in zip(path,path[1:]): J.symmetric_difference_update([tuple(sorted((x,y)))])
    assert all(w[e] for e in J)
    z=F(1);ww=w.copy()
    for e in J:z*=w[e];ww[e]=1/w[e]
    return z*dimer_sum(H,ww)

def count(rows,n,guards=(),cap=12):
    # Base larger than total number of assignments, so no carries between violation counts.
    b=2**n+1;const,edges=pair_data(rows);H,deleted=planar_core(n,edges)
    if len(deleted)+len(guards)>cap:return None
    al={};be={}
    for e,(a,c) in edges.items():al[e]=F(b**a+b**c,2);be[e]=F(b**a-b**c,2)
    w={tuple(sorted(e)):be[tuple(sorted(e))]/al[tuple(sorted(e))] for e in H.edges};factor=F(2**n*b**const)
    for e in w:factor*=al[e]
    ext=[(e,al[e],be[e]) for e in deleted]+[((u,v),F(1,2),F((-1)**s,2)) for u,v,s in guards]
    Z=F(0)
    for bits in it.product((0,1),repeat=len(ext)):
        T=set();a=F(1);stats['fourier_terms']+=1
        for bit,(e,x,y) in zip(bits,ext):
            a*=y if bit else x
            if bit:
                for v in e:T.symmetric_difference_update([v])
        Z+=a*parity_sum(H,w,T)
    Z*=factor;assert Z.denominator==1 and Z>=0;Z=int(Z)
    # Each NAE owner contributes 1 equal pair when feasible, 3 otherwise.
    hist={j:(Z//b**(len(rows)+2*j))%b for j in range(len(rows)+1)}
    assert Z==sum(c*b**(len(rows)+2*j) for j,c in hist.items())
    return {'hist':{j:c for j,c in hist.items() if c},'q':len(deleted),'deleted':deleted,'constant_exponent':const,'interaction_edges':len(edges),'base':b,'Z':Z}

def run():
    tab=authenticate();a=direct(ROWS,6);r=count(ROWS,6);assert r['hist']==a and a.get(0,0)==0
    # Adversarial check: all ten split relaxations and restored equality. Only the zero-violation controls are needed.
    ids=[i for i,row in enumerate(ROWS) if any(v==0 for v,s in row)];spl=[]
    for comb in it.combinations(ids,3):
        if ids[0] not in comb:continue
        rows=[[(6 if v==0 and i in comb else v,s) for v,s in row] for i,row in enumerate(ROWS)]
        un=direct(rows,7);gu=direct(rows,7,[(0,6,0)]);assert un[0]>0 and gu==a
        rr=count(rows,7,[(0,6,0)]);assert rr['hist']==gu;spl.append({'split':comb,'relaxed_count':un[0],'guarded_count':rr['hist'].get(0,0),'q':rr['q']})
    # Hostile minimal SAT control: delete one owner, not a research target.
    control=direct(ROWS[1:],6);rc=count(ROWS[1:],6);assert rc['hist']==control and control[0]>0
    # Gaussian/parity control: impossible opposite guards, disconnected core control, repeated literals.
    for rows,n,guards in [([],2,[(0,1,0),(0,1,1)]),([],2,[(0,1,0)]),([[(0,0),(0,1),(1,0)]],2,[]),([[(0,0),(1,0),(2,0)]],3,[(0,1,0),(1,2,0)])]:
        assert count(rows,n,guards)['hist']==direct(rows,n,guards)
    # Native all-positive AG9 obstruction has 12 owners, dense effective graph: capped terminal must decline rather than label NO.
    ag=CAP+[[0,1,2],[3,4,5]];ag=[[(v,0) for v in row] for row in ag];assert direct(ag,9).get(0,0)==0;assert count(ag,9,cap=3) is None
    out={'source_fingerprint_sha256':hashlib.sha256(json.dumps([C,P],separators=(',',':')).encode()).hexdigest(),'local_tables':tab,'direct':a,'hybrid':r,'splits':spl,'owner_deletion_control':control,'dense_control':'UNKNOWN at q cap 3','counters':dict(stats),'networkx_version':nx.__version__}
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':run()
