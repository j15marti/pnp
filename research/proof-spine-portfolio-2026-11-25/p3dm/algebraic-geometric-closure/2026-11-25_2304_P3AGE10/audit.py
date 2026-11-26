"""Exact three-track source-preserving rank seams. Requires AGE09 age08.py and age09.py and networkx."""
import itertools as I, json, math, sys
from collections import Counter,defaultdict
import networkx as nx
from age09 import solve as anchor, octsplice
from age08 import U,V

def bits(x):
    while x:
        b=x&-x;yield b.bit_length()-1;x^=b

def xor(xs):
    a=0
    for x in xs:a^=x
    return a

def basis(cols):
    B={};K=[]
    for i,x in enumerate(cols):
        w=1<<i
        while x:
            j=x.bit_length()-1
            if j not in B:B[j]=(x,w);break
            y,z=B[j];x^=y;w^=z
        if not x:K.append(w)
    return B,K

def reduce(B,x):
    w=0
    for j in sorted(B,reverse=True):
        if x>>j&1:y,z=B[j];x^=y;w^=z
    return x,w

def source(T,n):
    G=nx.Graph();G.add_nodes_from(range(3*n));G.add_nodes_from(range(3*n,3*n+len(T)))
    G.add_edges_from((3*n+i,c*n+t[c]) for i,t in enumerate(T) for c in range(3))
    assert len(set(T))==len(T) and all(0<=v<n for t in T for v in t) and nx.check_planarity(G)[0]
    return G

def cols(T,n):return [sum(1<<(c*n+t[c]) for c in range(3)) for t in T]

def verify(C,W,target):
    v=0
    for i in W:
        if v&C[i]:return False
        v|=C[i]
    return v==target

def close(T,n):
    A=set(range(len(T)));calls=0
    while True:
        old=A.copy();O=[[] for _ in range(3*n)]
        for i in A:
            for c,v in enumerate(T[i]):O[c*n+v].append(i)
        if any(not L for L in O):return None,calls
        for L in O:
            if len(L)==1 and L[0] in A:
                i=L[0];A-={j for c,v in enumerate(T[i]) for j in O[c*n+v] if j!=i}
        for c,d in I.combinations(range(3),2):
            L=[(c,i) for i in range(n)];R=[(d,i) for i in range(n)];G=nx.Graph();G.add_nodes_from(L+R)
            G.add_edges_from(((c,T[i][c]),(d,T[i][d])) for i in A);M=nx.bipartite.maximum_matching(G,top_nodes=L);calls+=1
            if len(M)!=2*n:return None,calls
            D=nx.DiGraph();D.add_nodes_from(L+R);D.add_edges_from(((c,T[i][c]),(d,T[i][d])) for i in A);D.add_edges_from((M[v],v) for v in L)
            idx={v:j for j,S in enumerate(nx.strongly_connected_components(D)) for v in S};A={i for i in A if idx[c,T[i][c]]==idx[d,T[i][d]]}
        if A==old:return sorted(A),calls

def algebra(T,n,cap):
    C=cols(T,n);B,K=basis(C);r,w=reduce(B,(1<<(3*n))-1)
    if r:return 'NO',None,{'nullity':len(K)}
    if len(K)>cap:return 'UNKNOWN',None,{'nullity':len(K)}
    for a in range(1<<len(K)):
        W=list(bits(w^xor(K[j] for j in bits(a))))
        if verify(C,W,(1<<(3*n))-1):return 'YES',W,{'nullity':len(K),'tests':a+1}
    return 'NO',None,{'nullity':len(K),'tests':1<<len(K)}

def boolean(T,n):
    C=cols(T,n);m=len(T);B,K=basis(C);r,w=reduce(B,(1<<(3*n))-1)
    if r:return 'NO',None,{'reason':'parity'}
    # Exact native 2-CNF consequences and Gaussian equal events; no approximate equality.
    O=[set(i for i,t in enumerate(C) if t>>j&1) for j in range(3*n)]
    D=nx.DiGraph();D.add_nodes_from(range(2*m))
    def clause(a,b):D.add_edge(a^1,b);D.add_edge(b^1,a)
    for S in O:
        for a,b in I.combinations(S,2):clause(2*a+1,2*b+1)
        if len(S)==2:a,b=sorted(S);clause(2*a,2*b)
        if len(S)==1:a=next(iter(S));clause(2*a,2*a)
    sig=defaultdict(list)
    for i in range(m):sig[(w>>i&1,tuple(j for j,z in enumerate(K) if z>>i&1))].append(i)
    for (a,b),L in sig.items():
        if not b:
            for i in L:clause(2*i+(1-a),2*i+(1-a))
        for i in L[1:]:
            j=L[0];clause(2*i+1,2*j);clause(2*j+1,2*i)
    # Conditional exact-one propagation on actual tuple IDs.  If a is selected,
    # eliminate conflicting tuples and iteratively propagate every unit owner.
    # A surviving singleton b certifies a => b, never a global pin without its guard.
    for a in range(m):
        A=set(range(m))
        A-={j for j in A if j!=a and C[j]&C[a]}
        while True:
            old=A.copy();rows=[S&A for S in O]
            if any(not S for S in rows):clause(2*a+1,2*a+1);break
            unit={next(iter(S)) for S in rows if len(S)==1}
            for b in unit:
                if b not in A:continue
                A-={j for j in A if j!=b and C[j]&C[b]}
            if A==old:
                for b in unit:clause(2*a+1,2*b)
                break
    scc={a:j for j,S in enumerate(nx.strongly_connected_components(D)) for a in S}
    if any(scc[2*i]==scc[2*i+1] for i in range(m)):return 'NO',None,{'reason':'2CNF'}
    cl=defaultdict(list)
    for i in range(m):cl[scc[2*i]].append(i)
    event={i:k for k,L in cl.items() for i in L};bad=set()
    R=[]
    for S in O:
        cnt=Counter(event[i] for i in S);bad|={k for k,v in cnt.items() if v>1};R.append(set(cnt))
    forced=set()
    while True:
        R=[S-bad for S in R]
        if any(not S for S in R):return 'NO',None,{'reason':'row'}
        unit={next(iter(S)) for S in R if len(S)==1}
        if unit==forced:break
        forced=unit
        bad|={k for S in R if S&forced for k in S-forced}
    # Rows are duplicate exactly-one constraints after exact event identification.
    R=list(set(map(frozenset,R)));occ=defaultdict(list)
    for j,S in enumerate(R):
        for k in S:occ[k].append(j)
    high=sum(len(L)>2 for L in occ.values())
    if high:return 'UNKNOWN',None,{'classes':len(cl),'rows':len(R),'high':high}
    G=nx.Graph();G.add_nodes_from(range(len(R)))
    for k,L in occ.items():
        a=L[0];b=L[1] if len(L)==2 else ('dummy',k)
        G.add_edge(a,b,weight=len(L),event=k)
    M=nx.max_weight_matching(G);Ksel={G[a][b]['event'] for a,b in M}
    if sum(len(occ[k]) for k in Ksel)!=len(R):return 'NO',None,{'classes':len(cl),'rows':len(R),'high':0}
    W=sorted(i for k in Ksel for i in cl[k]);assert verify(C,W,(1<<(3*n))-1)
    return 'YES',W,{'classes':len(cl),'rows':len(R),'high':0}

def geometric(T,n,cap):
    for c,d in I.combinations(range(3),2):
        r=anchor(T,n,c,d,cap=cap,saturated=False)
        if r['status']!='UNKNOWN':return r['status'],r.get('witness'),{'lane':[c,d],'work':r.get('work',0)}
    return 'UNKNOWN',None,{}

def targets(C,S,target,cap):
    left=sorted(S);right=[i for i in range(len(C)) if i not in S];L=[C[i] for i in left];R=[C[i] for i in right];B,K=basis(L+R);r,w=reduce(B,target)
    if r:return [],0
    mask=(1<<len(L))-1
    proj=lambda x:xor(L[i] for i in bits(x&mask))
    a=proj(w);D,_=basis([proj(k) for k in K]);k=len(D)
    if k>cap:return None,k
    V=[x for x,_ in D.values()]
    return [a^xor(V[i] for i in bits(z)) for z in range(1<<k)],k

def comp_groups(T,n,c,d):
    G=nx.Graph();G.add_edges_from(((c,t[c]),(d,t[d])) for t in T);idx={v:j for j,S in enumerate(nx.connected_components(G)) for v in S};L=[[] for _ in set(idx.values())]
    for i,t in enumerate(T):L[idx[c,t[c]]].append(i)
    H=nx.Graph();H.add_nodes_from(range(len(L)));O=defaultdict(set);e=3-c-d
    for j,S in enumerate(L):
        for i in S:O[T[i][e]].add(j)
    for S in O.values():H.add_edges_from(I.combinations(S,2))
    order=[];unseen=set(H)
    while unseen:
        start=min(unseen,key=lambda j:(H.degree(j),j));part=list(nx.bfs_tree(H,start));order+=part;unseen-=set(part)
    return [L[j] for j in order]

def hierarchy(groups):
    if len(groups)==1:return (set(groups[0]),None,None)
    a=hierarchy(groups[:len(groups)//2]);b=hierarchy(groups[len(groups)//2:]);return (a[0]|b[0],a,b)

def solve_leaf(T,C,n,S,b,cap,mode='all'):
    U=[sorted(v for v in range(n) if b>>(c*n+v)&1) for c in range(3)]
    if len(set(map(len,U)))!=1:return 'NO',None,{'reason':'unbalanced'}
    if not U[0]:return 'YES',[],{'reason':'empty'}
    maps=[{v:i for i,v in enumerate(L)} for L in U];J=sorted(i for i in S if C[i]&b==C[i]);R=[tuple(maps[c][v] for c,v in enumerate(T[i])) for i in J];q=len(U[0]);A,calls=close(R,q)
    if A is None:return 'NO',None,{'reason':'closure','calls':calls}
    R=[R[i] for i in A];J=[J[i] for i in A];source(R,q)
    methods=[('geometry',lambda:geometric(R,q,cap=2000)),('algebra',lambda:algebra(R,q,cap)),('boolean',lambda:boolean(R,q))]
    results={};known=[]
    for name,f in methods:
        if mode!='all' and name not in ([mode] if isinstance(mode,str) else mode):continue
        # Chart construction in the audit is only attempted on small subproblems.
        if name=='geometry' and len(R)>40:results[name]={'status':'UNKNOWN','reason':'audit size cap'};continue
        s,W,meta=f();results[name]={'status':s,**meta}
        if s=='YES':W=[J[i] for i in W];assert verify(C,W,b)
        if s!='UNKNOWN':known.append((s,W))
    assert len({s for s,W in known})<=1
    return (*known[0],results) if known else ('UNKNOWN',None,results)

def seam_solver(T,n,groups,width=6,cap=4,mode='all'):
    C=cols(T,n);full=(1<<(3*n))-1;root=hierarchy(groups);stats={'states':0,'leaf_calls':0,'joins':0,'max_rank':0,'max_boundary':0,'leaf_methods':Counter(),'leaves':len(groups)}
    def visit(node):
        S,L,R=node;A,k=targets(C,S,full,width);stats['max_rank']=max(stats['max_rank'],k);inside=0;outside=0
        for i,v in enumerate(C):
            if i in S:inside|=v
            else:outside|=v
        stats['max_boundary']=max(stats['max_boundary'],(inside&outside).bit_count())
        if A is None:raise OverflowError
        A=set(A);stats['states']+=len(A)
        if L is None:
            out={}
            for b in A:
                s,W,meta=solve_leaf(T,C,n,S,b,cap,mode(S) if callable(mode) else mode);stats['leaf_calls']+=1
                for method,x in meta.items():
                    if isinstance(x,dict) and 'status' in x:stats['leaf_methods'][method+':'+x['status']]+=1
                if s!='NO':out[b]=(s,W)
            return out
        a=visit(L);b=visit(R);out={}
        for x,(sx,wx) in a.items():
            for y,(sy,wy) in b.items():
                stats['joins']+=1
                if x&y or x|y not in A:continue
                z=x|y;s='YES' if sx==sy=='YES' else 'UNKNOWN';W=wx+wy if s=='YES' else None
                if z not in out or s=='YES':out[z]=(s,W)
        return out
    try:s,W=visit(root).get(full,('NO',None))
    except OverflowError:s,W='UNKNOWN',None
    if s=='YES':assert verify(C,W,full)
    return {'status':s,'witness':W,**stats,'leaf_methods':dict(stats['leaf_methods'])}

def neighbor(k,sat):
    T=list(V if sat else U);R=[tuple(v+3 for v in t) for t in octsplice(k)];a=list(T[0]);b=list(R[0]);a[1],b[1]=b[1],a[1];T[0]=tuple(a);R[0]=tuple(b);return T+R,3+2*k

def prism(k):
    cs=[i%2 for i in range(k)]
    if k%2:cs[-1]=2
    edges=[]
    for r in (0,1):
        for i,c in enumerate(cs):edges.append(((r,i),(r,(i+1)%k),c))
    for i in range(k):edges.append(((0,i),(1,i),3-cs[i]-cs[(i-1)%k]))
    ids=[0]*3;T={(r,i):[None]*3 for r in (0,1) for i in range(k)};G=nx.Graph()
    for a,b,c in edges:
        z=ids[c];ids[c]+=1;T[a][c]=T[b][c]=z;G.add_edge(a,b)
    return [tuple(t) for t in T.values()],k,G

def run():
    out={'neighbors':[],'prisms':[],'small':[]}
    for T,n in [(U,3),(V,3),(list(I.product(range(2),repeat=3)),2)]:
        source(T,n);C=cols(T,n);s,W,m=solve_leaf(T,C,n,set(range(len(T))),(1<<(3*n))-1,4);ref=any(verify(C,W,(1<<(3*n))-1) for W in I.combinations(range(len(T)),n));assert (s=='YES')==ref;out['small'].append({'m':len(T),'status':s,'methods':m})
    for k in (1,2,4,8,16,32,64):
        for sat in (False,True):
            T,n=neighbor(k,sat);G=source(T,n);assert nx.is_connected(G);S,calls=close(T,n);assert S==list(range(len(T)))
            groups=comp_groups(T,n,0,2);r=seam_solver(T,n,groups);assert r['status']==('YES' if sat else 'NO');out['neighbors'].append({'m':len(T),'sat':sat,'closure_calls':calls,**r})
    for k in (4,8,16,32,64,128):
        T,n,G=prism(k);source(T,n);S,calls=close(T,n);assert S==list(range(len(T)));color=nx.bipartite.color(G);groups=[[i for i,v in enumerate(G0) if color[v]==b] for b in (0,1) for G0 in [[(r,i) for r in (0,1) for i in range(k)]]];r=seam_solver(T,n,groups);assert r['status']=='YES' and r['max_rank']==1 and r['max_boundary']==3*k;out['prisms'].append({'m':len(T),**r})
    print(json.dumps(out,indent=2))
if __name__=='__main__':run()
