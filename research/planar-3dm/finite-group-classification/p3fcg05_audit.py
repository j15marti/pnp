import itertools as it, json, random
import networkx as nx

LANES=((0,1,2),(0,2,1),(1,2,0))
def incidence(T,V):
    g=nx.Graph();g.add_nodes_from((j,v) for j in range(3) for v in V[j])
    for i,t in T.items():
        g.add_edges_from(((3,i),(j,t[j])) for j in range(3))
    return g

def supported(T,V,a,b):
    g=nx.Graph(); L=[(a,x) for x in V[a]]; R=[(b,y) for y in V[b]]
    g.add_nodes_from(L+R);g.add_edges_from(((a,t[a]),(b,t[b])) for t in T.values())
    M=nx.algorithms.bipartite.maximum_matching(g,top_nodes=L)
    if any(x not in M for x in L+R):return None
    d=nx.DiGraph();d.add_nodes_from(L);d.add_edges_from((x,M[y]) for x,y in g.edges if x in L for _ in [0])
    # NetworkX emits edges with left vertices first because all L were inserted first.
    c={v:i for i,C in enumerate(nx.strongly_connected_components(d)) for v in C}
    return {i for i,t in T.items() if c[(a,t[a])]==c[M[(b,t[b])]]}

def closure(n,T):
    T=dict(enumerate(T)); V=[set(range(n)) for _ in range(3)]; chosen=[]
    while True:
        occ={(j,v):[] for j in range(3) for v in V[j]}
        for i,t in T.items():
            for j,v in enumerate(t):occ[j,v].append(i)
        if any(not z for z in occ.values()):return None
        one=next((z[0] for z in occ.values() if len(z)==1),None)
        if one is not None:
            t=T[one];chosen.append(t)
            for j,v in enumerate(t):V[j].remove(v)
            T={i:q for i,q in T.items() if all(q[j]!=t[j] for j in range(3))};continue
        if not T:return T,V,chosen
        keep=set(T)
        for a,b,_ in LANES:
            s=supported(T,V,a,b)
            if s is None:return None
            keep &= s
        if keep==set(T):return T,V,chosen
        T={i:t for i,t in T.items() if i in keep}

def pm(T,a,b,ids):
    rows=sorted({T[i][a] for i in ids});out=[]
    def rec(k,used,word):
        if k==len(rows):out.append(frozenset(word));return
        for i in ids:
            t=T[i]
            if t[a]==rows[k] and t[b] not in used:rec(k+1,used|{t[b]},word+[i])
    rec(0,set(),[]);return out

def exact(n,T):
    return any(len({T[i][2] for i in M})==n for M in pm(dict(enumerate(T)),0,1,list(range(len(T)))) if len(M)==n)

def components(T,V,a,b,z):
    g=nx.Graph();g.add_nodes_from((a,x) for x in V[a]);g.add_nodes_from((b,x) for x in V[b]);g.add_edges_from(((a,t[a]),(b,t[b])) for t in T.values())
    I=incidence(T,V)
    for C in nx.connected_components(g):
        ids=[i for i,t in T.items() if (a,t[a]) in C]
        outside=I.copy();outside.remove_nodes_from(C|{(3,i) for i in ids})
        owner={v:k for k,B in enumerate(nx.connected_components(outside)) for v in B}
        groups={}
        for i in ids:groups.setdefault(owner[(z,T[i][z])],[]).append(i)
        yield C,ids,list(groups.values())

def certificate(T,C,ids,a,b,S):
    g=nx.Graph();g.add_nodes_from(C)
    for i in ids:
        if i not in S:g.add_edge((a,T[i][a]),(b,T[i][b]))
    owner={v:k for k,B in enumerate(nx.connected_components(g)) for v in B}
    Q=nx.Graph();Q.add_nodes_from(('v',k) for k in set(owner.values())); arcs={};loops=[]
    for i in S:
        u,v=owner[a,T[i][a]],owner[b,T[i][b]];arcs[i]=(u,v)
        if u==v:loops.append(i);continue
        Q.add_edge(('v',u),('e',i));Q.add_edge(('e',i),('v',v))
    blocks=[]
    for B in nx.biconnected_components(Q):
        if len(B)>2:
            H=Q.subgraph(B);assert all(d==2 for _,d in H.degree())
            blocks.append({i for typ,i in B if typ=='e'})
    # Constant occupancy iff edge weights are vertex potential differences.
    D=nx.Graph();D.add_nodes_from(C);adj={v:[] for v in C}
    for i in ids:
        u,v=(a,T[i][a]),(b,T[i][b]);w=int(i in S)
        adj[u].append((v,-w));adj[v].append((u,w))
    p={next(iter(C)):0};todo=list(p);ok=True
    while todo:
        u=todo.pop()
        for v,w in adj[u]:
            if v in p:ok &= p[v]==p[u]+w
            else:p[v]=p[u]+w;todo.append(v)
    return ok,blocks,loops

def double(k):
    return [(off+i,off+j,2*i+h) for off in [0,k] for i in range(k) for h,j in [(0,i),(1,(i+1)%k)]]
def star(k):
    return [(i,j,2*i+h) for i in range(k) for h,j in [(0,i),(1,(i+1)%k)]]+[(k+i,k+i,2*i+h) for i in range(k) for h in range(2)]

def run():
    rng=random.Random(5505);stats={k:0 for k in ['planar','sat','unsat','closure_no','residual','subset_tests','constant','constant_one','constant_multi','correlated_switch_examples']};example=None
    cases=[(2,[t for j,t in enumerate(it.product(range(2),repeat=3)) if mask>>j&1]) for mask in range(256)]
    for n in [3,4]:
        universe=list(it.product(range(n),repeat=3))
        for _ in range(500):
            T=set(rng.sample(universe,rng.randint(n,min(len(universe),3*n))))
            if rng.randrange(2):T.update(zip(range(n),rng.sample(range(n),n),rng.sample(range(n),n)))
            cases.append((n,sorted(T)))
    for n,T in cases:
        V=[set(range(n)) for _ in range(3)]
        if not nx.check_planarity(incidence(dict(enumerate(T)),V))[0]:continue
        stats['planar']+=1;truth=exact(n,T);stats['sat' if truth else 'unsat']+=1
        R=closure(n,T)
        if R is None:assert not truth;stats['closure_no']+=1;continue
        U,V,chosen=R;assert (not U and len(chosen)==n)==(not U and truth)
        if not U:continue
        stats['residual']+=1
        for a,b,z in LANES:
            for C,ids,groups in components(U,V,a,b,z):
                M=pm(U,a,b,ids);assert M and set().union(*M)==set(ids)
                for G in groups:
                    for bits in range(1,1<<len(G)):
                        S={i for j,i in enumerate(G) if bits>>j&1};stats['subset_tests']+=1
                        ok,blocks,loops=certificate(U,C,ids,a,b,S)
                        masks={frozenset(S&m) for m in M};counts={len(x) for x in masks};assert ok==(len(counts)==1)
                        base=next(iter(masks))
                        for m in masks:
                            diff=base^m
                            assert diff==((diff&set(loops))|set().union(*(B for B in blocks if B<=diff)))
                        if ok:
                            r=next(iter(counts));assert not loops and len(S)<=2*r
                            stats['constant']+=1;stats['constant_one' if r==1 else 'constant_multi']+=1
                            flex=[B for B in blocks if any(B<=base^m for m in masks)]
                            if len(masks)<2**len(flex):
                                stats['correlated_switch_examples']+=1
                                if example is None:example={'n':n,'T':T,'lane':[a,b,z],'S':[U[i] for i in S],'masks':[[U[i] for i in m] for m in masks]}
    scales=[]
    for k in [2,4,8,16,32,64,128]:
        row={'k':k}
        for name,fn in [('double',double),('star',star)]:
            T=fn(k);V=[set(range(2*k)) for _ in range(3)];assert nx.check_planarity(incidence(dict(enumerate(T)),V))[0]
            R=closure(2*k,T);assert R is not None and len(R[0])==len(T)
            U,V,_=R;C,ids,groups=max(components(U,V,0,1,2),key=lambda v:len(v[1]));M=pm(U,0,1,ids);assert len(M)==2
            for G in groups:
                ok,B,L=certificate(U,C,ids,0,1,set(G));assert ok and not L and len(G)==2*len(M[0]&set(G))
            if name=='double':
                witness=[t for t in T if (t[0]<k and t[2]%2==0) or (t[0]>=k and t[2]%2==1)]
            else:witness=[t for t in T if (t[0]<k and t[2]%2==0) or (t[0]>=k and t[2]%2==1)]
            assert len(witness)==2*k and all(len({t[j] for t in witness})==2*k for j in range(3))
            # Remove a non-witness edge, then remove one edge of the other phase too.
            bad=next(t for t in T if t not in witness and t[0]<k);good=witness[0]
            assert closure(2*k,[t for t in T if t!=bad]) is not None
            assert closure(2*k,[t for t in T if t not in (bad,good)]) is None
            row[name]={'triples':len(T),'exterior_groups':len(groups),'max_group':max(map(len,groups)),'remaining':len(U),'pm':len(M),'neighbor_sat_no':True}
        scales.append(row)
    print(json.dumps({'seed':5505,'small':stats,'correlated_example':example,'scales':scales},indent=2))
if __name__=='__main__':run()
