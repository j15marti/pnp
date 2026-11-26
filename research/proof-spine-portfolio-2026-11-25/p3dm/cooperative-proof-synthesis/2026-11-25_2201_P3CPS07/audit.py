import itertools as I, json, math, random
import networkx as nx

LANES=list(I.combinations(range(3),2))
U=[tuple(map(int,t)) for t in '000 002 010 011 021 022 100 101 111 201 202 221'.split()]
V=U+[(1,1,0)]
BASE=[tuple(map(int,t)) for t in '000 002 012 111 121 202 210 222'.split()]

def ring(k):
    T=[tuple(3*i+v for v in t) for i in range(k) for t in BASE]
    for i in range(k-1):
        a,b=8*i+2,8*(i+1)+5
        x,y=list(T[a]),list(T[b]);x[1],y[1]=y[1],x[1];T[a],T[b]=tuple(x),tuple(y)
    return T

def ternary_chain(k):
    base=[(0,0,0),(1,1,1),(0,0,1),(1,1,0),(0,1,0),(1,0,1)]
    T=[list(2*i+a for a in t) for i in range(k) for t in base]
    for i in range(k-1):
        a,b=6*i+1,6*(i+1);T[a][1],T[b][1]=T[b][1],T[a][1]
    return list(map(tuple,T))

def prism(m):
    return [tuple(next((j%m)//3 for j in (i-1,i,i+1) if j%3==c) for c in range(3)) for i in range(m)]

def auth(T,n):
    assert len(T)==len(set(T)) and all(len(t)==3 and all(0<=a<n for a in t) for t in T)
    G=nx.Graph();G.add_nodes_from((c,i) for c in range(3) for i in range(n));G.add_edges_from((('t',j),(c,v)) for j,t in enumerate(T) for c,v in enumerate(t))
    assert nx.check_planarity(G)[0]
    return G

def verify(T,n,S):
    return len(S)==n and all({T[j][c] for j in S}==set(range(n)) for c in range(3))

def reference(T,n):
    groups=[[j for j,t in enumerate(T) if t[0]==i] for i in range(n)]
    return next((list(s) for s in I.product(*groups) if verify(T,n,s)),None)

class Solver:
    def __init__(self,T,n):
        self.T=T;self.n=n;self.owner=[{j for j,t in enumerate(T) if t[c]==i} for c in range(3) for i in range(n)]
        self.conf=[set().union(*(self.owner[c*n+t[c]] for c in range(3)))-{j} for j,t in enumerate(T)]
        self.calls=0;self.matchings=0
    def close(self,S,pins=()):
        self.calls+=1;S=set(S)
        for j in pins:
            if j not in S:return None
            S-=self.conf[j]
        while True:
            before=len(S)
            for O in self.owner:
                L=S&O
                if not L:return None
                if len(L)==1:S-=self.conf[next(iter(L))]
            for c,d in LANES:
                G=nx.Graph();A=[(c,i) for i in range(self.n)];G.add_nodes_from(A+[(d,i) for i in range(self.n)])
                G.add_edges_from(((c,self.T[j][c]),(d,self.T[j][d])) for j in S)
                self.matchings+=1;M=nx.bipartite.maximum_matching(G,top_nodes=A)
                if any(a not in M for a in A):return None
                D=nx.DiGraph();D.add_nodes_from(G)
                for a,b in G.edges:
                    if a[0]!=c:a,b=b,a
                    D.add_edge(b,a) if M[a]==b else D.add_edge(a,b)
                comp={v:i for i,C in enumerate(nx.strongly_connected_components(D)) for v in C}
                S={j for j in S if M[(c,self.T[j][c])]==(d,self.T[j][d]) or comp[(c,self.T[j][c])]==comp[(d,self.T[j][d])]}
            if len(S)==before:return S
    def acquire(self,initial=None,pins=()):
        S=self.close(range(len(self.T)) if initial is None else initial,pins)
        if S is None:return None,None
        # Failed selection closure. Repeat until no certified deletion.
        while True:
            C={j:self.close(S,[j]) for j in sorted(S)}
            bad={j for j,R in C.items() if R is None}
            if not bad:return S,C
            S=self.close(S-bad)
            if S is None:return None,None
    def terminal(self,cap=4096,initial=None,pins=()):
        S,C=self.acquire(initial,pins)
        if S is None:return dict(status='NO',stage='closure',calls=self.calls,matchings=self.matchings)
        out=[]
        for c in range(3):
            O=[self.owner[c*self.n+i]&S for i in range(self.n)]
            D=nx.DiGraph();D.add_nodes_from(range(self.n));maps={}
            for u in range(self.n):
                for v in range(self.n):
                    if u==v:continue
                    R={a:O[v]&C[a] for a in O[u]}
                    if all(len(b)==1 for b in R.values()):
                        D.add_edge(u,v);maps[u,v]={a:next(iter(b)) for a,b in R.items()}
            Q=nx.condensation(D);roots=[min(Q.nodes[i]['members'],key=lambda v:(len(O[v]),v)) for i in Q if Q.in_degree(i)==0]
            # Assign each owner to a particular root along a directed functional path.
            # True source solutions respect every path; extra edges need not be tested
            # because the final exact cover is checked, not a relaxation.
            own={v:v for v in roots};parent={};order=list(roots)
            for u in order:
                for v in sorted(D[u]):
                    if v not in own:own[v]=own[u];parent[v]=u;order.append(v)
            assert len(own)==self.n
            opts={}
            for root in roots:
                A=[]
                for a in sorted(O[root]):
                    sel={root:a}
                    for v in order:
                        if own[v]==root and v!=root:sel[v]=maps[parent[v],v][sel[parent[v]]]
                    W=tuple(sorted(sel.values()))
                    if all(len({self.T[j][d] for j in W})==len(W) for d in range(3)):A.append(W)
                opts[root]=A
            prod=math.prod(len(O[v]) for v in roots);raw=math.prod(map(len,O));branches=0;wit=None
            wide=[v for v in roots if len(opts[v])>2];small=[v for v in roots if len(opts[v])<=2]
            wideprod=math.prod(len(opts[v]) for v in wide)
            if any(not opts[v] for v in roots):wideprod=0
            if 0<wideprod<=cap:
                # Conflict test between bundles of actual indexed triples.
                def clash(A,B):
                    return any({self.T[j][d] for j in A}&{self.T[j][d] for j in B} for d in range(3))
                for choice in I.product(*(opts[v] for v in wide)):
                    branches+=1
                    if any(clash(a,b) for a,b in I.combinations(choice,2)):continue
                    G=nx.DiGraph();G.add_nodes_from((v,b) for v in small for b in (0,1))
                    for v in small:
                        for b in (0,1):
                            if b>=len(opts[v]) or any(clash(opts[v][b],a) for a in choice):G.add_edge((v,b),(v,1-b))
                    for v,w in I.combinations(small,2):
                        for a,A in enumerate(opts[v]):
                            for b,B in enumerate(opts[w]):
                                if clash(A,B):G.add_edge((v,a),(w,1-b));G.add_edge((w,b),(v,1-a))
                    K=nx.condensation(G);M=K.graph['mapping'];rank={v:i for i,v in enumerate(nx.topological_sort(K))}
                    if any(M[v,0]==M[v,1] for v in small):continue
                    W=[j for A in choice for j in A]
                    for v in small:
                        b=int(rank[M[v,1]]>rank[M[v,0]]);W.extend(opts[v][b])
                    assert verify(self.T,self.n,W);wit=W;break
            out.append(dict(lane=c,root_count=len(roots),raw_product=raw,root_product=prod,wide_product=wideprod,arcs=D.number_of_edges(),branches=branches,status='YES' if wit is not None else 'NO' if wideprod<=cap else 'OPEN',witness=wit))
        return dict(status='YES' if any(a['status']=='YES' for a in out) else 'NO' if any(a['status']=='NO' for a in out) else 'OPEN',stage='root',live=len(S),calls=self.calls,matchings=self.matchings,lanes=out)

def run(T,n,ref=None):
    auth(T,n);a=Solver(T,n).terminal()
    if ref is not None:assert a['status']=='OPEN' or (a['status']=='YES')==ref
    return a

if __name__=='__main__':
    out={}
    for name,T in [('U',U),('V',V),('base',BASE)]:out[name]=run(T,3,reference(T,3) is not None)
    for k in [1,2,4,8,16,32]:
        T=ring(k);out['ring'+str(k)]=run(T,3*k,True)
        if k<=8:
            # One-tuple deletion neighbor. Exact reference for small only; no hardness claim.
            R=T[1:];out['ringdel'+str(k)]=run(R,3*k,reference(R,3*k) is not None if k<=2 else None)
    for m in [12,24,48,96]:
        T=prism(m);out['prism'+str(m)]=run(T,m//3,True)
        out['prismNO'+str(m)]=run([t for i,t in enumerate(T) if i not in (0,1,2)],m//3,False)
    for k in [2,4,8,16,32]:
        T=ternary_chain(k);n=2*k;auth(T,n);assert verify(T,n,[6*i+j for i in range(k) for j in (0,1)])
        for i in range(k):
            for choice in ((2,3),(4,5)):
                assert verify(T,n,[6*u+j for u in range(k) for j in (choice if u==i else (2,3))])
        S=Solver(T,n);a=S.terminal();f=Solver(T,n).terminal(initial=set(range(len(T)))-{0});g=Solver(T,n).terminal(pins=[0]);assert f["status"]==g["status"]=="YES"
        assert all(x["wide_product"]==3**k for x in a["lanes"]) and all(x["wide_product"]==1 for x in f["lanes"]+g["lanes"])
        out["ternary"+str(k)]={"unguarded":a,"guard_false":f,"guard_true":g}
    stats={"tested":0,"nonplanar":0,"YES":0,"NO":0,"OPEN":0};rng=random.Random(251125)
    universe=list(I.product(range(2),repeat=3));U3=list(I.product(range(3),repeat=3))
    jobs=[(2,[t for j,t in enumerate(universe) if mask>>j&1]) for mask in range(256)]+[(3,rng.sample(U3,rng.randint(6,15))) for _ in range(200)]
    for n,T in jobs:
        try:auth(T,n)
        except AssertionError:stats["nonplanar"]+=1;continue
        a=run(T,n,reference(T,n) is not None);stats["tested"]+=1;stats[a["status"]]+=1
    out["small_audit"]=stats
    print(json.dumps(out,indent=2))
