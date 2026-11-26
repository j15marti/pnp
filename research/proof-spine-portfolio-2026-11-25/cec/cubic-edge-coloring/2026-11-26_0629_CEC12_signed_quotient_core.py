"""CEC12 signed quotient core, extracted from executed cec12_group.py.
Requires NetworkX. Explicit simple cubic source, integer vertex IDs.
D must contain exactly one edge per odd cycle of the verified old matching's complement.
skip is a fixed set of permitted uncovered edges. None excludes only this guarded query.
The complete original audit, harness and raw results are in the supplied ZIP.
"""
import itertools
import networkx as nx

def e(u,v):return tuple(sorted((u,v)))
def edges(G):return sorted(e(*a) for a in G.edges())
def pm(G,F=(),excluded=()):
    F=set(F); excluded=set(excluded); V=[v for a in F for v in a]
    if len(set(V))!=len(V) or F&excluded or any(not G.has_edge(*a) for a in F):return None
    H=G.copy();H.remove_nodes_from(V);H.remove_edges_from(excluded)
    P={e(*a) for a in nx.max_weight_matching(H,maxcardinality=True)}
    return P|F if len(P)*2==len(H) else None

def factor(G,M):
    H=G.copy();H.remove_edges_from(M);assert all(d==2 for _,d in H.degree()); C=[]
    while H:
        u=min(H);a=[u];prev=-1
        while True:
            v=min(v for v in H[a[-1]] if v!=prev);prev=a[-1]
            if v==u:break
            a.append(v)
        C.append(a);H.remove_nodes_from(a)
    return C

def patterns(C):
    odd=[c for c in C if len(c)%2]
    for D in itertools.product(*[[e(c[i],c[(i+1)%len(c)]) for i in range(len(c))] for c in odd]):
        yield frozenset(D)

def offsets(C,D):
    idx={};off={}
    for i,c in enumerate(C):
        idx.update((v,i) for v in c);off[c[0]]=0
        for u,v in zip(c,c[1:]):off[v]=off[u]^(e(u,v) not in D)
        assert (off[c[-1]]^off[c[0]])==(e(c[-1],c[0]) not in D)
    return idx,off

def signed_solve(q,R):
    """Return either satisfying potentials or an inconsistent circuit, retaining edge IDs."""
    A=[[] for _ in range(q)]
    for u,v,b,a in R:A[u].append((v,b,a));A[v].append((u,b,a))
    val={}; par={}; pe={}
    for s in range(q):
        if s in val:continue
        val[s]=0;par[s]=None;queue=[s]
        for u in queue:
            for v,b,a in A[u]:
                if v not in val:val[v]=val[u]^b;par[v]=u;pe[v]=a;queue.append(v)
                elif val[u]^val[v]!=b:
                    path={u:[]};w=u;L=[]
                    while par[w] is not None:L=L+[pe[w]];w=par[w];path[w]=L
                    w=v;L=[]
                    while w not in path:L.append(pe[w]);w=par[w]
                    return None, list(dict.fromkeys([a]+L+path[w]))
    return val,None

def acquire(G,M,D,skip=frozenset(),full=True,stats=None):
    """Find a cut optimal for old M with at most |skip| defects outside a new PM,
    and every uncovered defect in skip, or prove this guarded instance NO."""
    if stats is None:stats={}
    for k in ['nodes','pm','forced','branches','negative_cycles','affine_nogoods','bundle_nogoods']:stats.setdefault(k,0)
    C=factor(G,M);idx,off=offsets(C,D);q=len(C)
    R=[(idx[u],idx[v],1^off[u]^off[v],(u,v)) for u,v in sorted(M-skip)]
    def match(F,excluded=()):stats['pm']+=1;return pm(G,F,excluded)
    def rec(F,derived=frozenset()):
        derived=set(derived)
        stats['nodes']+=1
        while True:
            P=match(F)
            if P is None:return None
            impossible=set();mandatory=set(F);V={v for a in F for v in a}
            for u,v,b,a in R:
                if a in F:continue
                if set(a)&V:impossible.add(a);continue
                if full:
                    if a not in P and match(F|{a}) is None:impossible.add(a)
                    if a in P and match(F,{a}) is None:mandatory.add(a)
            if mandatory!=F:stats['forced']+=len(mandatory-F);F=mandatory;continue
            hard=[r for r in R if r[3] in impossible or r[3] in derived];val,cyc=signed_solve(q,hard)
            if cyc is not None:stats['affine_nogoods']+=1;return None
            H=nx.Graph();H.add_nodes_from(range(q));H.add_edges_from((u,v) for u,v,_,a in hard)
            comp={u:i for i,K in enumerate(nx.connected_components(H)) for u in K}
            force={a for u,v,b,a in R if a not in F and comp[u]==comp[v] and val[u]^val[v]!=b}
            if force:stats['forced']+=len(force);F=F|force;continue
            bundles={}
            for u,v,b,a in R:
                if a in F or comp[u]==comp[v]:continue
                key=(*sorted((comp[u],comp[v])),b^val[u]^val[v]);bundles.setdefault(key,set()).add(a)
            rejected=[]
            if full:
                for key,B in bundles.items():
                    if len(B)>1 and match(F|B) is None:rejected.append(min(B))
            if rejected:
                stats['bundle_nogoods']+=len(rejected);derived.update(rejected);continue
            q2=len(set(comp.values()));G2=nx.MultiGraph();G2.add_nodes_from(range(q2));G2.add_edges_from((u,v) for u,v,b in bundles)
            rank=G2.number_of_edges()-q2+nx.number_connected_components(G2)
            stats['max_bundle_rank']=max(rank,stats.get('max_bundle_rank',0))
            phase,cyc=signed_solve(q2,[(u,v,b,key) for key in bundles for u,v,b in [key]])
            if phase is not None:
                x={v:off[v]^val[idx[v]]^phase[comp[idx[v]]] for v in G};bad={a for a in edges(G) if x[a[0]]==x[a[1]]}
                assert (bad-M)==set(D) and bad-P<=set(skip)
                return x,P
            stats['negative_cycles']+=1
            for key in cyc:
                stats['branches']+=1
                ans=rec(F|bundles[key],derived)
                if ans is not None:return ans
            return None
    return rec(set(D)-set(skip))

def color(G,P):
    col={a:2 for a in P}
    for c in factor(G,P):
        assert len(c)%2==0
        for i,u in enumerate(c):col[e(u,c[(i+1)%len(c)])]=i%2
    assert set(col)==set(edges(G)) and all(len({col[e(v,w)] for w in G[v]})==3 for v in G)
    return col
