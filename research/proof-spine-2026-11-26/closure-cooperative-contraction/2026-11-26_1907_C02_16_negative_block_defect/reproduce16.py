#!/usr/bin/env python3
"""Standalone scoped block-defect reproduction. Python 3, NetworkX. No SAT oracle."""
import itertools as it, collections as co, json, hashlib, random
import networkx as nx
CORE=[[2,2,0],[0,1,2],[4,1,0],[1,1,2],[2,0,1],[1,2,2],[0,1,0],[0,2,2],[0,2,1],[0,0,0],[6,5,3],[3,4,5],[4,4,3],[1,4,5],[5,3,4],[4,5,5],[3,4,3],[3,5,5],[3,5,4],[3,3,3],[8,8,6],[6,7,8],[7,7,6],[7,7,8],[8,6,7],[7,8,8],[6,7,6],[5,8,8],[6,8,7],[11,6,6],[11,11,9],[9,10,11],[10,10,9],[10,10,11],[6,9,10],[10,11,11],[12,10,9],[9,11,11],[9,11,10],[9,9,9],[14,14,12],[12,13,14],[13,13,12],[13,13,14],[14,12,13],[13,14,14],[12,13,12],[12,14,14],[12,14,13],[9,12,12]]
BASE=[[2,2,0],[0,1,2],[1,1,0],[1,1,2],[2,0,1],[1,2,2],[0,1,0],[0,2,2],[0,2,1],[0,0,0]]
def mask(s):return sum(1<<v for v in s)
def words(s):return (sum(b<<v for v,b in zip(s,z)) for z in it.product((0,1),repeat=len(s)))
def instance(k):
    T=[x[:] for x in CORE]
    for l in range(k):
        T.extend([[v+15+3*l for v in x] for x in BASE]);i=4 if l==0 else 45+10*l;j=54+10*l;T[i][0],T[j][0]=T[j][0],T[i][0]
    return T,15+3*k

def native_reference(T,n,cap=5000):
    owners={(c,v):set() for c in range(3) for v in range(n)};cols=[set(enumerate(t)) for t in T];g=nx.Graph();g.add_nodes_from(owners)
    assert len(set(map(tuple,T)))==len(T)
    for i,cs in enumerate(cols):
        for o in cs:owners[o].add(i);g.add_edge(o,('t',i))
    assert nx.is_connected(g) and nx.check_planarity(g)[0]
    calls=0
    def rec(A,U):
        nonlocal calls
        calls+=1;assert calls<=cap
        if not U:return True
        o=min(U,key=lambda o:(len(owners[o]&A),o))
        return any(rec(A-set.union(*(owners[q] for q in cols[i])),U-cols[i]) for i in sorted(owners[o]&A))
    return rec(set(range(len(T))),set(owners)),calls

def signed_chart(T,n):
    G=nx.Graph();G.add_nodes_from(range(2*n));G.add_edges_from((t[1],n+t[2]) for t in T);R=sorted(nx.connected_components(G),key=min);ix={v:j for j,s in enumerate(R) for v in s};I=[[] for _ in R]
    for i,t in enumerate(T):I[ix[t[1]]].append(i)
    occ=[[] for _ in range(n)];S=[]
    for j,ids in enumerate(I):
        s=sorted({T[i][0] for i in ids});S.append(s)
        for v in s:occ[v].append(j)
    F=[];lookup={};idx=0;extra=[];acq=0
    for v,J in enumerate(occ):
        if len(J)==2:lookup[J[0],v]=(idx,0);lookup[J[1],v]=(idx,1);idx+=1
        elif len(J)>2:
            sc=[]
            for j in J:lookup[j,v]=(idx,0);sc.append(idx);idx+=1
            assert len(sc)<=10;extra.append((tuple(sc),{w for w in words(sc) if w.bit_count()%2}))
    for j,ids in enumerate(I):
        B={T[i][1] for i in ids};C={T[i][2] for i in ids};assert len(B)==len(C) and len(ids)<=10
        shared=[v for v in S[j] if len(occ[v])>1];priv=[v for v in S[j] if len(occ[v])==1];sc=tuple(sorted(lookup[j,v][0] for v in shared));rows=set()
        for q in range(1<<len(ids)):
            acq+=1;W=[i for b,i in enumerate(ids) if q>>b&1]
            if len(W)!=len(B) or len({T[i][1] for i in W})!=len(B) or len({T[i][2] for i in W})!=len(C):continue
            a=0
            for i in W:a^=1<<T[i][0]
            if any(not(a>>v&1) for v in priv):continue
            rows.add(sum(((a>>v&1)^lookup[j,v][1])<<lookup[j,v][0] for v in shared))
        F.append((sc,rows))
    return F+extra,acq

def graph(F):
    G=nx.Graph();G.add_nodes_from(range(len(F)));index=co.defaultdict(list)
    for i,(s,R) in enumerate(F):
        for v in s:index[v].append(i)
    for I in index.values():
        for i,j in it.combinations(I,2):
            if G.has_edge(i,j):G[i][j]['weight']+=1
            else:G.add_edge(i,j,weight=1)
    return G,index

def defect(F):
    G,index=graph(F);T=nx.Graph();T.add_nodes_from(G);uf=nx.utils.UnionFind(G)
    for i,j,e in sorted(G.edges(data=True),key=lambda e:(-e[2]['weight'],min(e[0],e[1]),max(e[0],e[1]))):
        if uf[i]!=uf[j]:uf.union(i,j);T.add_edge(i,j)
    D=[]
    for v,I in sorted(index.items()):
        if T.subgraph(I).number_of_edges()!=len(I)-1:D.append(v)
    return T,D

def terminal(F,T,D,counts):
    assert len(D)<=16
    m=mask(D)
    for w in words(D):
        counts['guard_branches']+=1;H=[(mask(s)&~m,{r&~m for r in R if (r^w)&mask(s)&m==0}) for s,R in F]
        if any(not R for s,R in H):continue
        ok=True;seen=set()
        for root in sorted(T):
            if root in seen:continue
            order=[root];P={root:None};seen.add(root)
            for u in order:
                for v in sorted(T[u]):
                    if v!=P[u]:assert v not in seen;seen.add(v);P[v]=u;order.append(v)
            for u in reversed(order):
                v=P[u]
                if v is None:continue
                s,R=H[u];t,S=H[v];p=s&t;J={r&p for r in R};counts['row_scans']+=len(R)+len(S);H[v]=(t,{r for r in S if r&p in J})
                if not H[v][1]:ok=False;break
            if not ok:break
        if ok:return True
    return False

def solve(F):
    G,_=graph(F);B=sorted(tuple(sorted(b)) for b in nx.biconnected_components(G));B.extend((v,) for v in nx.isolates(G));B.sort();occ=co.defaultdict(list)
    for i,bs in enumerate(B):
        for v in bs:occ[v].append(i)
    Q=nx.Graph();Q.add_nodes_from(('b',i) for i in range(len(B)))
    for v,I in occ.items():
        if len(I)>1:Q.add_edges_from((('a',v),('b',i)) for i in I)
    assert not Q or nx.is_forest(Q)
    Pp=[defect([F[v] for v in bs]) for bs in B];mx=max((len(D) for T,D in Pp),default=0);counts=co.Counter();H={};seen=set()
    def out(ans):return dict(satisfiable=ans,blocks=len(B),max_defect=mx,counts=dict(counts))
    for i in range(len(B)):
        root=('b',i)
        if root in seen:continue
        order=[root];P={root:None};seen.add(root)
        for u in order:
            for v in sorted(Q[u]):
                if v!=P[u]:assert v not in seen;seen.add(v);P[v]=u;order.append(v)
        for u in reversed(order):
            par=P[u];kids=[v for v in Q[u] if v!=par]
            if u[0]=='a':
                R=set(F[u[1]][1])
                for v in kids:R.intersection_update(H[v])
                if not R:return out(False)
                H[u]=R;continue
            j=u[1];bs=B[j];L=[(F[v][0],H[('a',v)] if ('a',v) in kids else F[v][1]) for v in bs];T,D=Pp[j]
            if par is None:
                if not terminal(L,T,D,counts):return out(False)
                continue
            p=bs.index(par[1]);R=set()
            for w in sorted(L[p][1]):
                counts['parent_rows']+=1;M=L[:];M[p]=(L[p][0],{w})
                if terminal(M,T,D,counts):R.add(w)
            if not R:return out(False)
            H[u]=R
    return out(True)

def chain(k):
    F=[]
    for i in range(k):
        a,b,c=3*i,3*i+1,3*i+2;l,r=3*k+i,3*k+i+1
        for s,p,q,t in [((a,b,l),a,b,0),((b,c,r),b,c,0),((a,c),a,c,int(i==0))]:F.append((s,{w for w in words(s) if ((w>>p&1)^(w>>q&1))==t}))
    return F

def main():
    R=[];A=[]
    for k in (0,1,5,10,20,35):
        T,n=instance(k);ref,calls=native_reference(T,n);assert not ref;F,a=signed_chart(T,n);x=solve(F);assert not x['satisfiable'];raw=json.dumps({'T':T,'n':n,'pins':[]},separators=(',',':')).encode();R.append(dict(triples=len(T),sha=hashlib.sha256(raw).hexdigest(),local_words=a,reference_calls=calls,**x))
    for k in (4,16,64,256,1024):
        x=solve(chain(k));assert not x['satisfiable'] and x['max_defect']==1;A.append(dict(k=k,**x))
    rng=random.Random(2611261616)
    for _ in range(300):
        n=rng.randint(1,7);F=[]
        for j in range(rng.randint(1,8)):
            s=tuple(sorted(rng.sample(range(n),rng.randint(1,min(n,4)))));F.append((s,{w for w in words(s) if rng.randrange(3)}))
        ref=any(all(w&mask(s) in R for s,R in F) for w in range(1<<n));assert solve(F)['satisfiable']==ref
    print(json.dumps(dict(native=R,abstract=A,random_seed=2611261616,random_checks=300),indent=2))
if __name__=='__main__':main()
