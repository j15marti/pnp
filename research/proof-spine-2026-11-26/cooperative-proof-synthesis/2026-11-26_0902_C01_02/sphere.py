import itertools as I, networkx as nx
from collections import Counter,defaultdict
from cps07 import auth,verify,Solver
from native19 import native_closure

def make(k,full=False):
    faces=set()
    for s in I.product([-1,1],repeat=3):
        def v(a,b): return (s[0]*a,s[1]*b,s[2]*(k-a-b))
        for a in range(k):
            for b in range(k-a):
                faces.add(tuple(sorted([v(a,b),v(a+1,b),v(a,b+1)])))
                if a+b+2<=k:faces.add(tuple(sorted([v(a+1,b),v(a,b+1),v(a+1,b+1)])))
    faces=sorted(faces); ed=defaultdict(list)
    for i,f in enumerate(faces):
        for e in I.combinations(f,2):ed[e].append(i)
    D=nx.Graph();D.add_nodes_from(range(len(faces)))
    for e,vv in ed.items():assert len(vv)==2;D.add_edge(*vv)
    b=nx.bipartite.color(D)
    V=[sorted({v for f in faces for v in f if (abs(v[1])+2*abs(v[2]))%3==c}) for c in range(3)]
    ix=[{v:i for i,v in enumerate(W)} for W in V]
    assert len(set(map(len,V)))==1,(k,list(map(len,V)))
    T=[tuple(ix[c][next(v for v in f if v in ix[c])] for c in range(3)) for j,f in enumerate(faces) if full or b[j]==0]
    return T,len(V[0]),V
if __name__=='__main__':
    for k in [1,2,4,5,7,8]:
        T,n,V=make(k); G=auth(T,n); print(k,len(T),n,Counter(dict(G.degree()).values()),nx.edge_connectivity(G),flush=True)
        L,c=native_closure(T,n); print(' closure',None if L is None else len(L),c,flush=True)
        if L is not None and k<=5:
            s=Solver(T,n).terminal(cap=4096,initial=L);print('functional',s['status'],[a['wide_product'] for a in s.get('lanes',[])],flush=True)
