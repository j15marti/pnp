import itertools as it, json, random
import networkx as nx

def graph(T,n):
    G=nx.Graph();G.add_nodes_from((i,a) for i in range(3) for a in range(n))
    for j,t in enumerate(sorted(T)):
        for i,a in enumerate(t): G.add_edge((3,j),(i,a))
    return G

def pm(edges,A,B):
    G=nx.Graph();G.add_nodes_from((0,a) for a in A);G.add_nodes_from((1,b) for b in B)
    G.add_edges_from(((0,a),(1,b)) for a,b in sorted(edges) if a in A and b in B)
    M=nx.algorithms.bipartite.maximum_matching(G,top_nodes={(0,a) for a in A})
    return {a:M[0,a][1] for a in A} if all((0,a) in M for a in A) else None

def lexpm(E,A,B):
    A=set(A); B=set(B); f={}
    if pm(E,A,B) is None:return None
    for a in sorted(A):
        b=next(b for b in sorted(B) if (a,b) in E and pm(E,A-{a},B-{b}) is not None)
        f[a]=b;A.remove(a);B.remove(b)
    return f

def closure(T,n):
    T=set(T); U=[set(range(n)) for _ in range(3)]; chosen=[]
    while True:
        if not U[0]: return T,U,chosen,'YES'
        for i in range(3):
            d={a:[t for t in T if t[i]==a] for a in U[i]}
            if any(not v for v in d.values()): return T,U,chosen,'NO'
            s=next((v[0] for v in d.values() if len(v)==1),None)
            if s is not None: break
        if s is not None:
            chosen.append(s); T={t for t in T if all(t[i]!=s[i] for i in range(3))}
            for i in range(3): U[i].remove(s[i])
            continue
        bad=set()
        for i,j in [(0,1),(0,2),(1,2)]:
            E={(t[i],t[j]) for t in T}
            if pm(E,U[i],U[j]) is None: return T,U,chosen,'NO'
            for a,b in E:
                if pm(E,U[i]-{a},U[j]-{b}) is None: bad.update(t for t in T if (t[i],t[j])==(a,b))
        if not bad: return T,U,chosen,'UNKNOWN'
        T-=bad

def cover(T,n):
    return next((q for q in it.product(*[[t for t in sorted(T) if t[0]==a] for a in range(n)]) if all(len({t[i] for t in q})==n for i in (1,2))),None)

def verify(T,n,W):
    return len(W)==n and set(W)<=set(T) and all({t[i] for t in W}==set(range(n)) for i in range(3))

def lane(T,U,order,context=True):
    i,j,k=order; A,B,Z=map(set,(U[i],U[j],U[k])); N={}
    for t in T: N.setdefault((t[i],t[k]),set()).add(t[j])
    E=set(N); P={(a,b) for (a,z),bs in N.items() for b in bs}; f=lexpm(P,A,B); g=pm(E,A,Z)
    if f is None or g is None:return 'NO',None,0
    L={a:sorted(z for x,z in E if x==a) for a in A}
    def admitted(Q):
        D={f[a] for a in Q}
        for zz in it.product(*(L[a] for a in Q)):
            if len(set(zz))<len(Q):continue
            Pq={(a,b) for a,z in zip(Q,zz) for b in N[a,z]&D}
            if pm(Pq,set(Q),D) is not None:continue
            if not context or pm(E,A-set(Q),Z-set(zz)) is not None:return False
        return True
    good={a for a in A if admitted((a,))}
    G=nx.Graph();G.add_nodes_from(A)
    for a,b in it.combinations(sorted(A),2):
        w=int(a not in good)+int(b not in good)
        if w and admitted((a,b)):G.add_edge(a,b,weight=w)
    pairs=nx.max_weight_matching(G); used={a for p in pairs for a in p}
    if A-good-used:return 'UNKNOWN',None,len(A-good)
    W=[]
    for Q in list(pairs)+[(a,) for a in A-used]:
        D={f[a] for a in Q}; h=pm({(a,b) for a in Q for b in N[a,g[a]]&D},set(Q),D)
        assert h is not None
        for a in Q:
            t=[None]*3;t[i]=a;t[j]=h[a];t[k]=g[a];W.append(tuple(t))
    return 'YES',W,len(A-good)

def scaffold(T,U,order):
    i,j,k=order; A,B=U[i],U[j]; N={}
    for t in T:N.setdefault((t[i],t[k]),set()).add(t[j])
    H={(a,b) for a in A for b in B if all(b in v for (x,z),v in N.items() if x==a)}
    return pm(H,A,B) is not None

ORD=list(it.permutations(range(3)))
U0={tuple(map(int,s)) for s in '000 002 010 011 021 022 100 101 111 201 202 221'.split()}
V0=U0|{(1,1,0)}

def sat2(q,clauses):
    G=nx.DiGraph();G.add_nodes_from((v,b) for v in range(q) for b in (0,1))
    for C in clauses:
        if not C:return None
        a,b=C[0],C[-1];G.add_edge((a[0],1-a[1]),b);G.add_edge((b[0],1-b[1]),a)
    S=nx.condensation(G); p=S.graph['mapping']; order={c:i for i,c in enumerate(nx.topological_sort(S))}
    if any(p[v,0]==p[v,1] for v in range(q)):return None
    x={v:int(order[p[v,1]]>order[p[v,0]]) for v in range(q)}
    assert all(any(x[v]==b for v,b in C) for C in clauses)
    return x

def guarded(T,U,order):
    i,j,k=order;A,B,Z=map(set,(U[i],U[j],U[k]));N={}
    for t in T:N.setdefault((t[i],t[k]),set()).add(t[j])
    E=set(N);P={(a,b) for (a,z),bs in N.items() for b in bs};f=lexpm(P,A,B);g=lexpm(E,A,Z)
    if f is None or g is None:return 'NO',None,0
    G=nx.Graph();G.add_edges_from(((0,a),(1,z)) for a,z in E);vmap={};options={};q=0
    for C in nx.connected_components(G):
        if len(C)==2:continue
        if any(G.degree(a)!=2 for a in C):return 'UNKNOWN',None,0
        for _,a in sorted(x for x in C if x[0]==0):
            vmap[a]=q;options[a]=next(z for _,z in G[0,a] if z!=g[a])
        q+=1
    def label(a,bits):return options[a] if a in vmap and bits[vmap[a]] else g[a]
    def examine(Q):
        D={f[a] for a in Q}; vs=sorted({vmap[a] for a in Q if a in vmap}); clauses=[]
        for vals in it.product((0,1),repeat=len(vs)):
            bits=dict(zip(vs,vals)); pin={a:label(a,bits) for a in Q}
            if pm({(a,b) for a in Q for b in N[a,pin[a]]&D},set(Q),D) is not None:continue
            F={(a,b) for a,b in P if a not in pin or b in N[a,pin[a]]}
            if pm(F,A,B) is not None:return None
            clauses.append(tuple((v,1-b) for v,b in bits.items()))
        return clauses
    singles={a:examine((a,)) for a in A};G=nx.Graph();G.add_nodes_from(A);P2={}
    for a,b in it.combinations(sorted(A),2):
        w=int(singles[a] is None)+int(singles[b] is None)
        if w:
            r=examine((a,b))
            if r is not None:G.add_edge(a,b,weight=w);P2[a,b]=r
    pairs=[tuple(sorted(p)) for p in nx.max_weight_matching(G)]; used={a for p in pairs for a in p}
    if any(singles[a] is None for a in A-used):return 'UNKNOWN',None,q
    clauses=[c for p in pairs for c in P2[p]]+[c for a in A-used for c in singles[a]];x=sat2(q,clauses)
    if x is None:return 'NO',None,q
    W=[]
    for Q in pairs+[(a,) for a in A-used]:
        D={f[a] for a in Q};h=pm({(a,b) for a in Q for b in N[a,label(a,x)]&D},set(Q),D);assert h is not None
        for a in Q:
            t=[0]*3;t[i]=a;t[j]=h[a];t[k]=label(a,x);W.append(tuple(t))
    return 'YES',W,q


def old(T):
    for i,j,k in [(0,1,2),(0,2,1),(1,2,0)]:
        G=nx.Graph();G.add_edges_from(((i,t[i]),(j,t[j])) for t in T)
        ok=True
        for C in nx.connected_components(G):
            Q={t for t in T if (i,t[i]) in C};V=[{t[a] for t in Q} for a in range(3)]
            if not (scaffold(Q,V,(i,j,k)) or scaffold(Q,V,(j,i,k))):ok=False;break
        if ok:return True
    return False

def bad_labels(T,order):
    i,j,k=order;N={}
    for t in T:N.setdefault((t[i],t[k]),set()).add(t[j])
    A={t[i] for t in T};B={t[j] for t in T};Z={t[k] for t in T}
    gs=[g for g in it.permutations(sorted(Z)) if all((a,z) in N for a,z in zip(sorted(A),g))]
    bad=[g for g in gs if pm({(a,b) for a,z in zip(sorted(A),g) for b in N[a,z]},A,B) is None]
    return [len(gs),len(bad),list(bad[0]) if bad else None]

BASE={tuple(map(int,s)) for s in '000 002 012 111 121 202 210 222'.split()}
SMALL_U={tuple(map(int,s)) for s in '001 010 100 111'.split()};SMALL_V=SMALL_U|{(1,0,1)}
def chain(k):
    T={tuple(x+3*i for x in t) for i in range(k) for t in BASE}
    for i in range(k-1):
        t=(3*i,3*i+1,3*i+2);u=(3*(i+1)+2,3*(i+1),3*(i+1)+2);T-={t,u};T|={(t[0],u[1],t[2]),(u[0],t[1],u[2])}
    return T

def neighbor(k,seed):
    T={tuple(x+2 for x in t) for t in chain(k)}|seed
    t=(0,0,1);a=3*(k-1)+2;u=(a,a+1,a+2);T-={t,u};T|={(t[0],u[1],t[2]),(u[0],t[1],u[2])}
    return T

def run():
    rng=random.Random(251125);stats={};extra=[];controls=[];scales=[];neighbors=[]
    for rep in range(1300):
        n=rng.choice([2,3,4]);cand=list(it.product(range(n),repeat=3));rng.shuffle(cand);T=set()
        for t in cand[:rng.randint(n*2,n*4)]:
            if nx.check_planarity(graph(T|{t},n))[0]:T.add(t)
        R,U,F,d=closure(T,n);truth=cover(T,n)
        if d!='UNKNOWN':
            assert (d=='YES')==bool(truth)
            if d=='YES':assert verify(T,n,F)
            key=d
        else:
            cs=old(R);ans=[lane(R,U,o) for o in ORD];gs=[guarded(R,U,o) for o in ORD]
            for v,W,q in ans+gs:
                if v=='YES':assert truth and verify(T,n,F+W)
                if v=='NO':assert not truth
            robust=any(v=='YES' for v,W,q in ans);gresult=next((v for v,W,q in gs if v!='UNKNOWN'),'UNKNOWN')
            key=f'CS={int(cs)},RB={int(robust)},guarded={gresult}'
            if not cs and (robust or gresult!='UNKNOWN'):extra.append([rep,n,sorted(T),key])
        stats[key]=stats.get(key,0)+1
    for T in (U0,V0,SMALL_U,SMALL_V):
        n=3 if T in (U0,V0) else 2
        assert nx.check_planarity(graph(T,n))[0]
        R,U,F,d=closure(T,n);assert d=='UNKNOWN'
        controls.append({'T':sorted(T),'truth':bool(cover(T,n)),'closure':d,'lanes':[{'order':o,'label_matchings':bad_labels(R,o),'RB':lane(R,U,o)[0],'guarded':guarded(R,U,o)[0]} for o in ORD]})
    for k in (1,2,4,8,16,32,64):
        T=chain(k);n=3*k;G=graph(T,n);assert nx.check_planarity(G)[0] and nx.is_connected(G)
        R,U,F,d=closure(T,n);assert d=='UNKNOWN' and R==T and not F and not old(R)
        v,W,q=lane(R,U,(0,1,2));assert v=='YES' and verify(T,n,W)
        scales.append({'k':k,'n':n,'m':len(T),'log2_label_matchings':k,'old':False,'RB':v,'bad_singletons':q,'verified':True})
    for k in (1,2,4,8,16,32):
        for seed in (SMALL_U,SMALL_V):
            T=neighbor(k,seed);n=2+3*k;G=graph(T,n);assert nx.check_planarity(G)[0] and nx.is_connected(G)
            R,U,F,d=closure(T,n);assert d=='UNKNOWN' and R==T and not F
            v,W,q=guarded(R,U,(0,1,2));expected='YES' if seed==SMALL_V else 'NO';assert v==expected
            if W is not None:assert verify(T,n,W)
            neighbors.append({'k':k,'m':len(T),'expected':expected,'result':v,'phases':q,'witness_verified':W is not None})
    return {'seed':251125,'random_jobs':1300,'stats':stats,'extra':extra,'controls':controls,'scales':scales,'neighbors':neighbors}

if __name__=='__main__':
    from pathlib import Path
    R=run();Path(__file__).with_name('results.json').write_text(json.dumps(R,indent=2)+'\n');print(R['stats']);print('extra',len(R['extra']));print(R['scales']);print(R['neighbors'])
