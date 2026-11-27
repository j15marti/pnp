"""Independent native chart reconstruction, bounded DFS, and exact learned-guard checks.
Does not import the primary solver or the archived chart acquirer."""
import itertools as I, json, collections as C, hashlib, networkx as nx

def reconstruct(T,n,live,cap=1000000):
    # B-C projection, independently enumerate edge-perfect matchings on each degree <=2 component.
    D=C.defaultdict(list);G=nx.Graph();G.add_nodes_from((c,i) for c in (1,2) for i in range(n));checks=0
    for j in live:
        x,y,z=T[j];D[y,z].append(j);G.add_edge((1,y),(2,z))
    assert max(dict(G.degree()).values())<=2
    mode={};nextmode=0
    for block in sorted(nx.connected_components(G),key=min):
        Y=sorted(y for c,y in block if c==1);Z={z for c,z in block if c==2};M=[]
        assert len(Y)==len(Z)
        # Degree<=2 graph connected; use propagation from first Y, never enumerate 2^|Y| words.
        def walk(A,U,V):
            nonlocal checks
            while U:
                opts=[(len(Q),y,Q) for y in U for Q in [{z for _,z in G[1,y]}&V]]
                _,y,Q=min(opts);checks+=len(opts)
                if checks>cap:raise TimeoutError
                if not Q:return
                if len(Q)==1:
                    z=next(iter(Q));A=A+[(y,z)];U=U-{y};V=V-{z}
                else:
                    for z in sorted(Q):walk(A+[(y,z)],U-{y},V-{z})
                    return
            if not V:M.append(tuple(sorted(A)))
        walk([],set(Y),Z);M=sorted(set(M));assert len(M) in (1,2)
        if len(M)==1:
            for e in M[0]:mode[e]=None
        else:
            assert not set(M[0])&set(M[1]);
            for b in (0,1):
                for e in M[b]:mode[e]=(nextmode,b)
            nextmode+=1
    H=nx.Graph();H.add_nodes_from(('x',x) for x in range(n));H.add_nodes_from(('e',e) for e in mode)
    for e in mode:
        for j in D[e]:H.add_edge(('e',e),('x',T[j][0]))
    chart=[];witnesses=[]
    for C0 in nx.connected_components(H):
        E=sorted(e for typ,e in C0 if typ=='e');X={x for typ,x in C0 if typ=='x'};P=tuple(sorted({mode[e][0] for e in E if mode[e] is not None}));assert len(P)<=3
        R={}
        for w in I.product((0,1),repeat=len(P)):
            a=dict(zip(P,w));A=[e for e in E if mode[e] is None or a[mode[e][0]]==mode[e][1]]
            if len(A)!=len(X):continue
            def match(i,left,trace):
                nonlocal checks
                checks+=1
                if checks>cap:raise TimeoutError
                if i==len(A):return trace if not left else None
                for j in D[A[i]]:
                    x=T[j][0]
                    if x in left:
                        p=match(i+1,left-{x},trace+[j])
                        if p is not None:return p
                return None
            ans=match(0,X,[])
            if ans is not None:R[w]=ans
        chart.append((P,set(R)));witnesses.append(R)
    return chart,checks

def exact(F,pins=(),cap=1000000):
    # An independently implemented exact table search using restriction and all local singleton consequences.
    work=0;nodes=0
    def solve(a):
        nonlocal work,nodes
        nodes+=1
        while True:
            possible={};new=dict(a)
            for P,R in F:
                work+=len(R)
                if work>cap:raise TimeoutError
                S=[w for w in R if all(v not in a or a[v]==b for v,b in zip(P,w))]
                if not S:return False
                for i,v in enumerate(P):
                    if v in a:continue
                    poss={w[i] for w in S};possible[v]=possible.get(v,{0,1})&poss
                    if not possible[v]:return False
                    if len(possible[v])==1:new[v]=next(iter(possible[v]))
            if new==a:break
            a=new
        if not possible:return True
        v=min(possible,key=lambda v:(len(possible[v]),-sum(v in P for P,R in F),v));return any(solve(a|{v:b}) for b in sorted(possible[v]))
    return solve(dict(pins)),work,nodes

def canon(F):return C.Counter((tuple(P),tuple(sorted(R))) for P,R in F)
if __name__=='__main__':
    results=[]
    for k in (0,1):
        obj=json.load(open(f'context12_k{k}.json'));T=obj['T'];n=obj['n'];live=obj['live'];assert hashlib.sha256(json.dumps([n,T,[]],separators=(',',':')).encode()).hexdigest()==obj['fingerprint']
        assert len({tuple(t) for t in T})==len(T) and all(len(t)==3 and all(0<=v<n for v in t) for t in T)
        G=nx.Graph();G.add_nodes_from((c,v) for c in range(3) for v in range(n));G.add_edges_from((('t',j),(c,v)) for j,t in enumerate(T) for c,v in enumerate(t));assert nx.is_connected(G) and nx.check_planarity(G)[0]
        F,c=reconstruct(T,n,live);original,c0=reconstruct(T,n,range(len(T)))
        assert canon(F)==canon([(P,{tuple(w) for w in R}) for P,R in obj['chart']])
        s,w,nodes=exact(original);assert not s
        out=[]
        for g in obj['hybrid']['learned']:
            sat,work,nn=exact(F,g);assert not sat;out.append([g,work,nn])
        assert {tuple(tuple(q) for q in g) for g in obj['hybrid']['learned']}=={((0,a),(1,b)) for a,b in I.product((0,1),repeat=2)}
        R={'k':k,'full_native_acquisition_checks':c0,'closed_native_acquisition_checks':c,'full_native_NO_reference_rows':w,'full_native_NO_reference_nodes':nodes,'guard_checks':out,'verified':True};results.append(R);print(R)
    json.dump(results,open('independent12_results.json','w'),indent=2)
