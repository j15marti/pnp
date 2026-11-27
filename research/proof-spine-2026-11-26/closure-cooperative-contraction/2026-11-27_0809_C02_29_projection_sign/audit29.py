import json, hashlib, itertools
from collections import Counter
import networkx as nx
from sympy.polys.matrices import DomainMatrix
from sympy import ZZ
PAIRS=((0,1),(1,2),(0,2))
def grid(s):
    V=[[(i,j) for i in range(s) for j in range(s) if (i-j)%3==c] for c in range(3)]
    T=[tuple(sorted(t,key=lambda p:(p[0]-p[1])%3)) for i in range(s-1) for j in range(s-1) for t in [((i,j),(i+1,j),(i,j+1)),((i+1,j+1),(i+1,j),(i,j+1))]]
    return V,T

def perm_parity(p):
    return sum(x>y for i,x in enumerate(p) for y in p[i+1:])%2

def project(V,T,live,a,b):
    G=nx.Graph(); G.add_nodes_from(V[a]+V[b]);G.add_edges_from((T[i][a],T[i][b]) for i in live);return G

def matching(G,V,a,b):
    M=nx.bipartite.maximum_matching(G,top_nodes=V[a]);return M if len(M)==len(V[a])+len(V[b]) else None

def sign(M,V,a,b):
    idx={v:i for i,v in enumerate(V[b])};return perm_parity([idx[M[u]] for u in V[a]])

def closure(V,T):
    live=set(range(len(T)));calls=0
    while True:
        old=live.copy()
        for a,b in PAIRS:
            G=project(V,T,live,a,b); M=matching(G,V,a,b);calls+=1
            if M is None:return live,calls,True
            D=nx.DiGraph();D.add_nodes_from(V[a]);D.add_edges_from((u,M[v]) for u in V[a] for v in G[u]);comp={u:k for k,C in enumerate(nx.strongly_connected_components(D)) for u in C}
            live={i for i in live if comp[T[i][a]]==comp[M[T[i][b]]]}
        # force singleton owners while retaining forced row and all vertices
        owners={u:[] for shore in V for u in shore}
        for i in live:
            for u in T[i]:owners[u].append(i)
        if any(not x for x in owners.values()):return live,calls,True
        forced={x[0] for x in owners.values() if len(x)==1};used=Counter(u for i in forced for u in T[i])
        if max(used.values(),default=0)>1:return live,calls,True
        live={i for i in live if i in forced or not any(u in used for u in T[i])}
        if live==old:return live,calls,False

# cyclic directions in original (i,j) coordinate plane, determinant positive
DIR=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1));order={d:i for i,d in enumerate(DIR)}
def faces(G):
    rot={u:sorted(G[u],key=lambda v:order[(v[0]-u[0],v[1]-u[1])]) for u in G};seen=set();out=[]
    for u in G:
        for v in rot[u]:
            if (u,v) in seen:continue
            w=[];a,b=u,v
            while (a,b) not in seen:
                seen.add((a,b));w.append(a);c=rot[b][(rot[b].index(a)-1)%len(rot[b])];a,b=b,c
            assert (a,b)==(u,v)
            area=sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(w,w[1:]+w[:1]))
            if area>0:out.append(w)
    return out
def determinant(G,V,a,b):
    B=V[b];ix={v:i for i,v in enumerate(B)};n=len(B);rows={i:{ix[v]:ZZ(1) for v in G[u]} for i,u in enumerate(V[a])}
    return int(DomainMatrix(rows,(n,n),ZZ).det())

def run(s,det=True):
    V,T=grid(s);live,calls,no=closure(V,T);assert not no or s==3
    graphs=[project(V,T,range(len(T)),a,b) for a,b in PAIRS];hist=[dict(Counter(map(len,faces(G)))) for G in graphs];assert all(set(h)<={6} for h in hist)
    M=[matching(G,V,a,b) for G,(a,b) in zip(graphs,PAIRS)];assert all(M);p=[sign(m,V,a,b) for m,(a,b) in zip(M,PAIRS)]
    # independent exact determinants, no cancellation because face lemma; verify against matching sign
    ds=[determinant(G,V,a,b) for G,(a,b) in zip(graphs,PAIRS)] if det else []
    assert all(d and (d<0)==bool(x) for d,x in zip(ds,p))
    # After closure import same original signs, not new face-sign assumptions.
    closed=[]
    if not no:
        for a,b in PAIRS:
            G=project(V,T,live,a,b);m=matching(G,V,a,b);assert m;closed.append(sign(m,V,a,b))
        assert closed==p
    return dict(s=s,n=len(V[0]),m=len(T),live=len(live),matching_calls=calls,closure_no=no,faces=hist,signs=p,closed_signs=closed,determinants=[str(d) for d in ds],parity_no=bool(sum(p)%2),local_sha256=hashlib.sha256(json.dumps([V,T],separators=(',',':')).encode()).hexdigest())
if __name__=='__main__':
    for s in [3,9,15,21,27,33,6]: print(json.dumps(run(s,det=s<=21)),flush=True)
