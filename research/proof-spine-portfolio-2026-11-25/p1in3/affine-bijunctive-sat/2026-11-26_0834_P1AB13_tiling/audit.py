import itertools as it
import json, random
import networkx as nx

SEED = 20261126
RNG = random.Random(SEED)

def native(C):
    n = len(C)
    assert all(len(set(c)) == 3 for c in C)
    assert all(sum(i in c for c in C) == 3 for i in range(n))
    G = nx.Graph()
    G.add_edges_from((('c', j), ('v', i)) for j, c in enumerate(C) for i in c)
    ok, emb = nx.check_planarity(G)
    assert ok
    emb.check_structure()
    F = nx.Graph()
    F.add_nodes_from(range(n))
    F.add_edges_from(e for c in C for e in it.combinations(c, 2))
    assert nx.check_planarity(F)[0]
    return F

def pack(F, P):
    return not any(u in P and v in P for u, v in F.edges())

def fuse(F, P, Q):
    assert pack(F, P) and pack(F, Q)
    L, R = P-Q, Q-P
    H = F.subgraph(L|R).copy()
    M = nx.bipartite.maximum_matching(H, top_nodes=L)
    K = nx.bipartite.to_vertex_cover(H, M, top_nodes=L)
    I = (P&Q)|((L|R)-K)
    assert pack(F, I) and I <= P|Q and len(K) == len(M)//2
    assert len(I) == len(P|Q)-len(M)//2
    S = I & R
    neighbors = {p for q in S for p in H[q]}
    assert len(I)-len(P) == len(S)-len(neighbors)
    return I

def allpack(F):
    V=list(F)
    return [set(s) for k in range(len(V)+1) for s in it.combinations(V,k) if pack(F,set(s))]

def closure(C, guard):
    p=dict(guard)
    while True:
        old=len(p)
        for c in C:
            a=sum(p.get(i,0) for i in c); free=[i for i in c if i not in p]
            if a>1 or (a==0 and not free): return None
            if a==1: p.update((i,0) for i in free)
            elif len(free)==1: p[free[0]]=1
        if old==len(p): break
    # Necessary capacity-three assignment of uncovered clauses to available variables.
    L={('c',j) for j,c in enumerate(C) if not any(p.get(i)==1 for i in c)}
    G=nx.Graph();G.add_nodes_from(L)
    for _,j in L:
        for i in C[j]:
            if i not in p:
                G.add_edges_from((('c',j),('slot',i,k)) for k in range(3))
    M=nx.bipartite.maximum_matching(G,top_nodes=L)
    return p if all(c in M for c in L) else None

out={'seed':SEED,'prisms':[],'native_neighbors':[],'small_fusion_checks':0,'guard_checks':0}
for r in (1,3,5,7,11,21,43,85):
    n=9*r+3
    C=[((i-1)%n,i,(i+1)%n) for i in range(n)]
    F=native(C)
    P={j*(3*r+1)+3*i for j in range(3) for i in range(r)}
    assert len(P)==3*r and pack(F,P)
    assert sum(not (P&set(c)) for c in C)==3
    models=[set(range(j,n,3)) for j in range(3)]
    assert all(all(len(S&set(c))==1 for c in C) for S in models)
    assert {len(P^S) for S in models}=={4*r+1}
    assert closure(C,{})=={}
    # Translation symmetry reduces all shift-pair tests to one fixed packing.
    shifts=list(range(n)) if n<=102 else sorted({0,1,2,3,n-1,*RNG.sample(range(n),12)})
    for j in shifts:
        Q={(i+j)%n for i in P}
        assert len(fuse(F,P,Q))==3*r
    out['prisms'].append({'n':n,'holes':3,'minimum_repair':4*r+1,'shift_pair_checks':len(shifts),'models_symbolic':3})

NO=[(1,6,11),(0,1,11),(3,4,5),(2,3,5),(0,3,10),(2,4,5),(1,2,6),(7,9,10),(7,8,9),(7,8,10),(4,8,9),(0,6,11)]
YES=NO.copy();YES[1]=(1,2,11);YES[3]=(0,3,5)
for label,C in [('SAT',YES),('UNSAT',NO)]:
    F=native(C);P=allpack(F);opt=max(map(len,P));n=len(C)
    models=[S for S in P if len(S)==n//3]
    assert bool(models)==(label=='SAT')
    for i,v in it.product(range(n),(0,1)):
        a=closure(C,{i:v});ref=[S for S in models if (i in S)==bool(v)]
        if a is None: assert not ref
        else: assert all(all((j in S)==bool(b) for j,b in a.items()) for S in ref)
        out['guard_checks']+=1
    for _ in range(200):
        A,B=RNG.choice(P),RNG.choice(P);S=fuse(F,A,B)
        assert len(S)==max(len(R) for R in P if R<=A|B)
        out['small_fusion_checks']+=1
    out['native_neighbors'].append({'label':label,'n':n,'all_packings':len(P),'opt_tiles':opt,'exact_models':len(models),'holes_at_opt':n-3*opt})
print(json.dumps(out,indent=2,sort_keys=True))
