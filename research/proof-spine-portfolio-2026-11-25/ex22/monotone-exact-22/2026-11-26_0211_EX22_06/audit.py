import itertools as it, json, networkx as nx
F=[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
def chain(k, bad):
    # identify point 1 of block j with point 0 of block j+1
    H=[]; B=[]; n=0
    for j in range(k):
        ids=list(range(n,n+7)); n+=7
        if j: ids[0]=B[-1][1]
        B.append(ids)
        H.extend(tuple(ids[i] for i in c) for c in (F if bad and j==0 else F[1:]))
    used=sorted(set(it.chain.from_iterable(B))); mp={v:i for i,v in enumerate(used)}
    return len(used),[tuple(mp[i] for i in c) for c in H],[[mp[i] for i in b] for b in B]
def lift(x,H): return tuple(x)+tuple(2-sum(x[i] for i in c) for c in H)
def valid(x,C): return all(v in (0,1) for v in x) and all(sum(x[i] for i in c)==2 for c in C)
def gf_rank(rows):
    basis={}
    for row in rows:
        v=[x%3 for x in row]
        for p,b in sorted(basis.items()):
            if v[p]:
                a=v[p]; v=[(x-a*y)%3 for x,y in zip(v,b)]
        p=next((j for j,x in enumerate(v) if x),None)
        if p is not None: basis[p]=[(v[p]*x)%3 for x in v]
    return len(basis)
def guard_poly(C,pins):
    # sign coordinates, f=1+ab+ac+bc; keys are monomial supports
    p={():1}
    for a,b in it.combinations(C,2):
        key=tuple(i for i in (a,b) if i not in pins); key=tuple(sorted(key))
        coef=pins.get(a,1)*pins.get(b,1)
        p[key]=(p.get(key,0)+coef)%3
    return {k:v for k,v in p.items() if v}
def unique_pivot_certificate(H,pins):
    polys=[guard_poly(c,pins) for c in H]; P=[p for p in polys if p]
    active={}
    for p in P:
        for k in p:
            if len(k)==2: active[k]=active.get(k,0)+1
    low=[p for p in P if not any(len(k)==2 for k in p)]
    assert all(any(len(k)==2 and active[k]==1 for k in p) for p in P if p not in low)
    assert len(low)<=1 and all(any(len(k)==1 for k in p) for p in low)
    # Thus no linear combination equals nonzero constant.
    return len(low)
def split_graph(C,n):
    G=nx.Graph(); occ=[[] for _ in range(n)]; E=[[] for _ in range(n)]; dummy=[]
    for j,c in enumerate(C):
        for i,v in enumerate(c):
            p=('p',j,i);occ[v].append(p)
            for a in range(2):G.add_edge(p,('a',j,a))
    for v,L in enumerate(occ):
        for i in range(0,len(L)-1,2):
            e=(L[i],L[i+1]);G.add_edge(*e);E[v].append(e)
        if len(L)%2:
            d=('d',v);dummy.append(d);e=(L[-1],d);G.add_edge(*e);E[v].append(e)
    G.add_edges_from(it.combinations(dummy,2));return G,E
def matching_pin(G,E,v,b):
    H=G.copy(); edges=E[v]
    if b:
        H.remove_nodes_from([p for e in edges for p in e])
    else: H.remove_edges_from(edges)
    M=nx.max_weight_matching(H,maxcardinality=True)
    assert all(H.has_edge(a,b) for a,b in M)
    return len(M)*2==len(H)
def fractional_pin(n,H,v,b):
    # scaled by 6; exact integer arithmetic
    x=[3]*n
    if v<n: x[v]=0
    else:
        for i in H[v-n]:x[i]=4
    y=x+[12-sum(x[i] for i in c) for c in H]
    if b:y=[6-z for z in y]
    assert y[v]==6*b and all(0<=z<=6 for z in y)
    assert all(sum(y[i] for i in c)+y[n+j]==12 for j,c in enumerate(H))
def run():
    out=[]; basis_tests=0; guard_tests=0; rank_tests=0; matching_calls=0; lp_calls=0
    # Exhaustively verify all physical-coordinate bases on the small SAT neighbor.
    n,H,_=chain(1,False);C=[c+(n+j,) for j,c in enumerate(H)]
    S=[lift(x,H) for x in it.product((0,1),repeat=n) if valid(lift(x,H),C)]
    d=gf_rank([[2*z-1 for z in x] for x in S]); assert len(S)==10
    for I in it.combinations(range(len(S[0])),d):
        if gf_rank([[2*x[i]-1 for i in I] for x in S])!=d:continue
        R={tuple(x[i] for i in I) for x in S};assert len(R)==len(S)
        assert any(tuple(int(a+b+c>=2) for a,b,c in zip(*t)) not in R for t in it.combinations(R,3));basis_tests+=1
    for k in (1,2,4,8,16):
        for bad in (False,True):
            n,H,B=chain(k,bad);C=[c+(n+j,) for j,c in enumerate(H)];N=n+len(H)
            assert all(len(set(c))==4 for c in C)
            assert len({tuple(sorted(p)) for c in H for p in it.combinations(c,2)})==3*len(H)
            G,E=split_graph(C,N)
            # initial and stagnation exact-two unary closure: no saturation under one pin;
            # LP and actual matching support checked for each polarity on k<=4, LP all sizes.
            for v in range(N):
                for b in (0,1):
                    fractional_pin(n,H,v,b);lp_calls+=1
                    if k<=4:
                        assert matching_pin(G,E,v,b);matching_calls+=1
            # Exhaustive pair probes by symbolic pivot certificate. Larger cases use theorem.
            if k<=4:
                for r in (0,1,2):
                    for J in it.combinations(range(n),r):
                        for vals in it.product((-1,1),repeat=r):
                            pins=dict(zip(J,vals));unique_pivot_certificate(H,pins);guard_tests+=1
                            if k==1:
                                ps=[guard_poly(c,pins) for c in H];keys=[()]+sorted({j for p in ps for j in p if j})
                                mat=[[p.get(j,0) for j in keys] for p in ps]
                                assert gf_rank(mat+[ [1]+[0]*(len(keys)-1)])==gf_rank(mat)+1;rank_tests+=1
            if not bad:
                x=[0]*n
                for b in B:
                    for j in (3,4,5,6):x[b[j]]=1
                assert valid(lift(x,H),C)
            # integer clique lane: find 7-vertex pair-complete Fano block (for small cases source-only enumeration).
            edges={tuple(sorted(p)) for c in H for p in it.combinations(c,2)}
            if k<=2:
                found=any(all(tuple(p) in edges for p in it.combinations(J,2)) and sum(set(c)<=set(J) for c in H)==7 for J in it.combinations(range(n),7))
                assert found==bad
            if k<=2:
                count=sum(valid(lift(x,H),C) for x in it.product((0,1),repeat=n));assert count==(0 if bad else 2*5**k)
            out.append(dict(k=k,bad=bad,physical=N,clauses=len(C),exact_count=0 if bad else 2*5**k,matching_executed=k<=4,pair_probes_executed=k<=4))
    return dict(networkx=nx.__version__,basis_tests=basis_tests,full_span_dim=d,guard_tests=guard_tests,rank_tests=rank_tests,matching_calls=matching_calls,lp_calls=lp_calls,controls=out)
if __name__=='__main__': print(json.dumps(run(),indent=2))
