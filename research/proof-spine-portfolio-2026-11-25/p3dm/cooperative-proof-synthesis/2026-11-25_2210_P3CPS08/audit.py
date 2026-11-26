# Requires CPS07 audit.py as cps07.py in this directory (exact published prior code).
import itertools as I, math, json, random
import networkx as nx
from cps07 import Solver, auth, verify, reference, ternary_chain, ring, prism, U, V

def alternate(k):
    B=[(0,0,0),(1,1,1),(0,0,1),(1,1,0),(0,1,0),(1,0,1)]
    T=[list(2*i+x for x in t) for i in range(k) for t in B]
    for i in range(k-1):
        h=2*(i%2);a,b=6*i+h+1,6*(i+1)+h
        T[a][1],T[b][1]=T[b][1],T[a][1]
    return list(map(tuple,T))

def bundles(s,S,C,c):
    O=[s.owner[c*s.n+i]&S for i in range(s.n)]
    G=nx.DiGraph();G.add_nodes_from(range(s.n));F={}
    for u,v in I.permutations(G.nodes,2):
        R={a:O[v]&C[a] for a in O[u]}
        if all(len(z)==1 for z in R.values()):
            G.add_edge(u,v);F[u,v]={a:next(iter(z)) for a,z in R.items()}
    Q=nx.condensation(G);roots=sorted(min(Q.nodes[i]['members'],key=lambda v:(len(O[v]),v)) for i in Q if Q.in_degree(i)==0)
    order=roots[:];own={v:v for v in roots};parent={}
    for u in order:
        for v in sorted(G[u]):
            if v not in own:own[v]=own[u];parent[v]=u;order.append(v)
    out={}
    for r in roots:
        out[r]=[]
        for a in sorted(O[r]):
            b={r:a}
            for v in order:
                if v!=r and own[v]==r:b[v]=F[parent[v],v][b[parent[v]]]
            W=tuple(sorted(b.values()))
            if all(len({s.T[j][c] for j in W})==len(W) for c in range(3)):out[r].append(W)
    return out

def graph_formula(D,bad):
    G=nx.DiGraph();opts=[(i,a) for i in D for a in D[i]]
    G.add_nodes_from((p,b) for p in opts for b in (0,1))
    def clause(p,b,q,c):G.add_edge((p,1-b),(q,c));G.add_edge((q,1-c),(p,b))
    for i,A in D.items():
        for a,b in I.combinations(A,2):clause((i,a),0,(i,b),0)
        if len(A)==1:clause((i,A[0]),1,(i,A[0]),1)
        if len(A)==2:clause((i,A[0]),1,(i,A[1]),1)
    for p,q in sorted(bad):clause(p,0,q,0)
    return G

def model(G,pins=()):
    H=G.copy()
    for p in pins:H.add_edge((p,0),(p,1))
    Q=nx.condensation(H);M=Q.graph['mapping'];rank={u:i for i,u in enumerate(nx.topological_sort(Q))}
    P={p for p,b in H.nodes}
    if any(M[p,0]==M[p,1] for p in P):return None
    return {p for p in P if rank[M[p,1]]>rank[M[p,0]]}

def project(D,bad):
    if any(not a for a in D.values()):return None
    G=graph_formula(D,bad)
    if model(G) is None:return None
    W={i:list(A) for i,A in D.items() if len(A)>2}
    reach={p:nx.descendants(G,(p,1)) for i,A in W.items() for a in A for p in [(i,a)]}
    W={i:[a for a in A if ((i,a),0) not in reach[i,a]] for i,A in W.items()}
    if any(not a for a in W.values()):return None
    F={((i,a),(j,b)) for i,j in I.combinations(sorted(W),2) for a in W[i] for b in W[j] if ((j,b),0) in reach[i,a]}
    return W,F,G

def ac(D,F):
    D={i:list(A) for i,A in D.items()}
    while True:
        if any(not A for A in D.values()):return None
        old=sum(map(len,D.values()))
        for i,j in I.permutations(sorted(D),2):
            D[i]=[a for a in D[i] if any(tuple(sorted(((i,a),(j,b)))) not in F for b in D[j])]
        if old==sum(map(len,D.values())):return D

def allowed(F,i,a,j,b):return tuple(sorted(((i,a),(j,b)))) not in F

def forest(D,F):
    G=nx.Graph();G.add_nodes_from(D)
    for (i,a),(j,b) in F:
        if a in D[i] and b in D[j]:G.add_edge(i,j)
    if not D:return 'YES',set(),0,0
    if not nx.is_forest(G):return 'OPEN',None,G.number_of_edges(),0
    picked=set();rows=0
    for comp in nx.connected_components(G):
        r=min(comp);P=dict(nx.bfs_predecessors(G,r));order=[r]+list(P);children={u:[] for u in comp}
        for u,v in P.items():children[v].append(u)
        ok={}
        for u in reversed(order):
            ok[u]=[a for a in D[u] if all(any(allowed(F,u,a,v,b) for b in ok[v]) for v in children[u])];rows+=len(D[u])
        if not ok[r]:return 'NO',None,G.number_of_edges(),rows
        values={r:ok[r][0]}
        for u in order[1:]:v=P[u];values[u]=next(b for b in ok[u] if allowed(F,v,values[v],u,b))
        picked.update(values.items())
    return 'YES',picked,G.number_of_edges(),rows

def equality_matching(D,F):
    D=ac(D,F)
    if D is None:return 'NO',None,0,0
    P=[(i,a) for i,A in D.items() for a in A];uf=nx.utils.UnionFind(P)
    for i,j in I.combinations(sorted(D),2):
        L=[(a,b) for a in D[i] for b in D[j] if allowed(F,i,a,j,b)]
        if not L:return 'NO',None,0,0
        E=[(a,b) for a in D[i] for b in D[j] if all((x==a)==(y==b) for x,y in L)]
        if any(allowed(F,i,x,j,y)!=all((x==a)==(y==b) for a,b in E) for x in D[i] for y in D[j]):return 'OPEN',None,0,0
        for a,b in E:uf.union((i,a),(j,b))
    classes=[sorted(A) for A in uf.to_sets()];G=nx.Graph();G.add_nodes_from(D);big=0
    for h,A in enumerate(classes):
        O=sorted({i for i,a in A})
        if len(O)!=len(A):continue # selecting this class violates exact one
        if len(O)>2:big+=1;continue
        u=O[0];v=O[1] if len(O)==2 else ('dummy',h)
        G.add_edge(u,v,weight=len(O),choice=A)
    if big:return 'OPEN',None,len(classes),big
    M=nx.max_weight_matching(G);weight=sum(G[u][v]['weight'] for u,v in M)
    if weight!=len(D):return 'NO',None,len(classes),0
    chosen={p for u,v in M for p in G[u][v]['choice']}
    assert len(chosen)==len(D) and all((p,q) not in F for p,q in I.combinations(sorted(chosen),2))
    return 'YES',chosen,len(classes),0

def track(s,O):
    D={i:list(range(len(A))) for i,A in O.items()}
    masks={(i,a):[{s.T[t][c] for t in B} for c in range(3)] for i,A in O.items() for a,B in enumerate(A)}
    bad={(p,q) for p,q in I.combinations(sorted(masks),2) if p[0]!=q[0] and any(x&y for x,y in zip(masks[p],masks[q]))}
    wide=math.prod(len(A) for A in D.values() if len(A)>2)
    R=project(D,bad)
    if R is None:return {'roots':len(D),'wide':wide,'status':'NO','stage':'projection'}
    W,F,G=R;stats={'roots':len(D),'wide':wide,'wide_roots':len(W),'projected_product':math.prod(map(len,W.values()))}
    for name,fun in [('forest',forest),('matching',equality_matching)]:
        status,A,c,d=fun(W,F);stats[name]=[status,c,d]
        if status=='YES':
            B=model(G,A);assert B is not None
            ids=[t for i,a in B for t in O[i][a]];assert verify(s.T,s.n,ids)
    return stats

def run(T,n,pins=(),initial=None):
    G=auth(T,n);s=Solver(T,n);S,C=s.acquire(initial,pins)
    if S is None:return {'stage':'closure','status':'NO','matching_calls':s.matchings}
    return {'stage':'quotient','live':len(S),'matching_calls':s.matchings,'lanes':[track(s,bundles(s,S,C,c)) for c in range(3)]}

def phase_witness(k,states):return [6*i+2*p+j for i,p in enumerate(states) for j in (0,1)]

def brute_quotient(D,F):
    return any(all((p,q) not in F for p,q in I.combinations(sorted(zip(D,v)),2)) for v in I.product(*D.values()))

if __name__=='__main__':
    import sys
    out={};mode=sys.argv[1] if len(sys.argv)>1 else 'named'
    if mode=='named':
        for k in [2,4,8,16,32,64]:
            T=alternate(k);n=2*k;G=auth(T,n);assert nx.is_connected(G) and all(d==3 for _,d in G.degree())
            assert nx.edge_connectivity(G)==2
            for i in range(k):
                for h in (0,1):
                    a=[2]*k;a[i]=h
                    for j in (i-1,i+1):
                        if 0<=j<k and min(i,j)%2==h:a[j]=h
                    assert verify(T,n,phase_witness(k,a))
            R=run(T,n);assert any(L.get('matching',[None])[0]=='YES' and L.get('forest',[None])[0]=='YES' for L in R['lanes'])
            d=min(3,k//4);pins=[6*i+4 for i in range(d)]
            B=run(T,n,pins=pins);assert all(L.get('wide_roots',0)>=math.ceil(max(0,k-3*d)/5) for L in B['lanes'])
            out[str(k)]={'root':R,'guarded':B,'d':d}
            if k<=16:
                A=[t for i,t in enumerate(T) if i not in {2,4}];B=[t for i,t in enumerate(T) if i not in {2,4,6}]
                u,v=run(A,n),run(B,n);assert v['status']=='NO';assert any(L.get('matching',[None])[0]=='YES' for L in u['lanes'])
                out[str(k)]['neighbor']=[u,v]
        for name,T,n in [('U',U,3),('V',V,3),('ring16',ring(16),48),('prism48',prism(48),16),('ternary16',ternary_chain(16),32)]:out[name]=run(T,n)
    else:
        rng=random.Random(1108);cnt={'source':0,'projection':0,'matching':0,'forest':0,'mixed':0}
        cube=list(I.product(range(2),repeat=3))
        for mask in range(256):
            T=[t for i,t in enumerate(cube) if mask>>i&1];r=run(T,2);truth=reference(T,2) is not None;cnt['source']+=1
            if r['stage']=='closure':assert not truth;continue
            for L in r['lanes']:
                for t in ['forest','matching']:
                    if t in L and L[t][0]!='OPEN':assert (L[t][0]=='YES')==truth;cnt[t]+=1
                if L.get('status')=='NO':assert not truth
        for rep in range(300):
            D={i:list(range(rng.choice([1,2,2,3]))) for i in range(5)}
            F={(p,q) for p,q in I.combinations([(i,a) for i,A in D.items() for a in A],2) if p[0]!=q[0] and rng.random()<.18}
            truth=brute_quotient(D,F);R=project(D,F);cnt['mixed']+=1
            if R is None:assert not truth;continue
            W,H,G=R;assert brute_quotient(W,H)==truth;cnt['projection']+=1
            for name,f in [('forest',forest),('matching',equality_matching)]:
                st,A,_,_=f(W,H)
                if st!='OPEN':assert (st=='YES')==truth;cnt[name]+=1
                if st=='YES':assert model(G,A) is not None
        out=cnt
    print(json.dumps(out,indent=2))
