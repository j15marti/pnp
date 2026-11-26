import itertools as I, random, json
import networkx as nx

def incidence(n,T):
    G=nx.Graph(); G.add_nodes_from((c,i) for c in range(3) for i in range(n)); G.add_edges_from(((3,j),(c,t[c])) for j,t in enumerate(T) for c in range(3)); return G

def pm(n,T,a=0,b=1):
    G=nx.Graph(); G.add_nodes_from((0,i) for i in range(n)); G.add_nodes_from((1,i) for i in range(n)); G.add_edges_from(((0,t[a]),(1,t[b])) for t in T)
    M=nx.algorithms.bipartite.maximum_matching(G,top_nodes=[(0,i) for i in range(n)])
    return None if len(M)!=2*n else [next(t for t in T if t[a]==i and t[b]==M[0,i][1]) for i in range(n)]

def parity(n,T):
    # Augmented GF(2) RREF; last bit is RHS.
    m=len(T); rows=[sum(1<<j for j,t in enumerate(T) if t[c]==i)|(1<<m) for c in range(3) for i in range(n)]; r=0
    for j in range(m):
        k=next((k for k in range(r,len(rows)) if rows[k]>>j&1),None)
        if k is None:continue
        rows[r],rows[k]=rows[k],rows[r]
        for k in range(len(rows)):
            if k!=r and rows[k]>>j&1:rows[k]^=rows[r]
        r+=1
    if (1<<m) in rows:return None
    fixed={}
    for row in rows:
        a=row&((1<<m)-1)
        if a and not a&(a-1):fixed[T[a.bit_length()-1]]=row>>m
    return fixed

def closure(n,T):
    # Keep original IDs (tuples); support via forced-edge projection tests.
    live=set(T); rounds=probes=0
    while True:
        rounds+=1; bad=set(); fixed=parity(n,sorted(live))
        if fixed is None:return None,rounds,probes
        for t,b in fixed.items():
            if not b:bad.add(t)
            else:bad.update(u for u in live if u!=t and any(u[j]==t[j] for j in range(3)))
        for a,b in I.combinations(range(3),2):
            probes+=1
            if pm(n,sorted(live),a,b) is None:return None,rounds,probes
            for t in sorted(live):
                probes+=1
                # Reserve t and isolate its endpoints from all other choices.
                U=[u for u in live if u[a]!=t[a] and u[b]!=t[b]]+[t]
                if pm(n,sorted(U),a,b) is None:bad.add(t)
        for c in range(3):
            for i in range(n):
                L=[t for t in live if t[c]==i]
                if not L:return None,rounds,probes
                if len(L)==1:
                    t=L[0]; bad.update(u for u in live if u!=t and any(u[j]==t[j] for j in range(3)))
        if not bad:return sorted(live),rounds,probes
        live-=bad

def matchings(n,T):
    E=[[t for t in T if t[0]==x] for x in range(n)]
    return [m for m in I.product(*E) if len({t[1] for t in m})==n]

def sig(M):
    x=0
    for t in M:x^=1<<t[2]
    return x

def squares(T):
    E={}
    for t in T:E.setdefault(t[:2],[]).append(t)
    A=sorted({t[0] for t in T});B=sorted({t[1] for t in T})
    for a,b in I.combinations(A,2):
        for c,d in I.combinations(B,2):
            for q in I.product(*(E.get(p,[]) for p in [(a,c),(a,d),(b,c),(b,d)])):
                yield q

def avoid_flow(n,T,groups):
    G=nx.DiGraph(); s=('s',);r=('r',);G.add_nodes_from([s,r]); used=set()
    for i in range(n):G.add_edge(s,('x',i),capacity=1);G.add_edge(('y',i),r,capacity=1)
    for j,q in enumerate(groups):
        assert not used.intersection(q);used.update(q)
        A={t[0] for t in q};B={t[1] for t in q};assert len(A)==len(B)==len(q)//2
        for a in A:G.add_edge(('x',a),('in',j),capacity=1)
        for b in B:G.add_edge(('out',j),('y',b),capacity=1)
        G.add_edge(('in',j),('out',j),capacity=len(A)-1)
    for t in T:
        if t not in used:G.add_edge(('x',t[0]),('e',t),capacity=1);G.add_edge(('e',t),('y',t[1]),capacity=1)
    return nx.maximum_flow_value(G,s,r,flow_func=nx.algorithms.flow.edmonds_karp)

def reduce(x,basis):
    for p in basis:x=min(x,x^p)
    return x

def basis_cycles(T):
    G=nx.Graph()
    for t in T:G.add_edge(('x',t[0]),('e',t));G.add_edge(('e',t),('y',t[1]))
    return [tuple(sorted(v[1] for v in C if v[0]=='e')) for C in nx.cycle_basis(G)]

def terminal(n,T,long=False):
    T,rounds,probes=closure(n,T)
    if T is None:return 'NO',0,0,probes
    M=pm(n,T);target=(1<<n)-1;basis=[];steps=[];calls=0;Q=list(squares(T))+(basis_cycles(T) if long else [])
    while True:
        by={}
        for q in Q:
            p=reduce(sig(q),basis)
            if p:by.setdefault(p,[]).append(q)
        found=False
        for p,qs in sorted(by.items()):
            used=set();groups=[]
            for q in qs:
                if not used.intersection(q):groups.append(q);used.update(q)
            calls+=1
            if avoid_flow(n,T,groups)<n:
                steps.append((list(basis),p,groups));basis.append(p);basis.sort(reverse=True);found=True;break
        if not found:break
    L,_,extra=closure(n,T);probes+=extra;assert L==T # recheck closure at stagnation
    if reduce(sig(M)^target,basis):return 'UNKNOWN',len(basis),calls,probes
    for old,p,groups in reversed(steps):
        if reduce(sig(M)^target,old):
            assert reduce(sig(M)^target,old)==p
            S=set(M);q=next(q for q in groups if len(S.intersection(q))==len(q)//2)
            S.symmetric_difference_update(q);M=sorted(S)
    assert sig(M)==target and all(len({t[c] for t in M})==n for c in range(3))
    return 'YES',len(basis),calls,probes

def ring(k):
    return [t for j in range(k) for a,b in [(2*j,2*((j-1)%k))] for t in [(a,a,a),(a,a+1,a+1),(a+1,a,b),(a+1,a+1,b+1)]]

def prism(k):
    G=nx.circular_ladder_graph(2*k); ed=[[],[],[]]
    for layer in range(2):
        for i in range(2*k):ed[(i+layer)%2].append((layer*2*k+i,layer*2*k+(i+1)%(2*k)))
    ed[2]=[(i,i+2*k) for i in range(2*k)]
    D=[{v:i for i,e in enumerate(L) for v in e} for L in ed]
    return [tuple(D[c][v] for c in range(3)) for v in G]

def main():
    R=random.Random(721); tests=0; positive=0; exact=0; relaxed=0; false_admissions=0
    for i in range(200):
        n=4;T=[t for t in I.product(range(n),repeat=3) if R.random()<.24];Q=list(squares(T));R.shuffle(Q);groups=[];used=set()
        for q in Q:
            if not used.intersection(q):groups.append(q);used.update(q)
        M=matchings(n,T);a=any(all(len(set(m).intersection(q))<=1 for q in groups) for m in M);b=avoid_flow(n,T,groups)==n
        assert a==b;tests+=1;exact+=bool(groups);positive+=bool(M) and not a
        groups=[];used=set()
        for q in basis_cycles(T):
            if not used.intersection(q):groups.append(q);used.update(q)
        a=any(all(len(set(m).intersection(q))<len(q)//2 for q in groups) for m in M);b=avoid_flow(n,T,groups)==n
        assert not a or b;relaxed+=1;false_admissions+=b and not a
    # Abstract collective case: 3 squares, center can touch only one leaf.
    E=[(2*j+a,2*j+b,0) for j in range(3) for a in range(2) for b in range(2)]+[(0,2,0),(2,0,0),(0,4,0),(4,0,0)]
    E[4]=(2,2,1);E[8]=(4,4,1); Q=[tuple(E[4:8]),tuple(E[8:12])]
    assert sig(Q[0])==sig(Q[1])==3
    assert all(avoid_flow(6,E,[q])==6 for q in Q) and avoid_flow(6,E,Q)==5
    assert len(matchings(6,E))==12
    # Long-cycle filling is only a relaxation: both leaf squares can be
    # externally touched only by leaving the central pair (0,2), absent in C.
    C=[(0,0,0),(0,1,0),(1,1,0),(1,2,0),(2,2,0),(2,0,0)]
    B=[(a,b,0) for a in (3,4) for b in (3,4)];D=[(a,b,0) for a in (5,6) for b in (5,6)]
    E=C+B+D+[(1,3,0),(3,0,0),(2,5,0),(5,1,0)];groups=[C,B,D]
    assert matchings(7,E) and not any(all(len(set(m).intersection(q))<len(q)//2 for q in groups) for m in matchings(7,E))
    assert avoid_flow(7,E,groups)==7
    fixtures=[]
    U=[tuple(map(int,t)) for t in ['000','002','010','011','021','022','100','101','111','201','202','221']]
    for n,T,name in [(3,U,'peer_U'),(3,U+[(1,1,0)],'peer_V'),(2,[(0,0,0),(1,1,0),(1,0,1),(0,1,1)],'tetra_U'),(2,[(0,0,0),(1,1,0),(1,0,1),(0,1,1),(0,0,1)],'tetra_V')]+[(2*k,ring(k),'ring'+str(k)) for k in [2,3,4,8,16]]+[(2*k,prism(k),'prism'+str(k)) for k in [3,4,8,16]]:
        G=incidence(n,T);assert len(set(T))==len(T) and nx.check_planarity(G)[0] and nx.is_connected(G)
        out=terminal(n,T); ext=terminal(n,T,True); ref=None
        if n<=8:
            ref=any(sig(m)==(1<<n)-1 for m in matchings(n,T));assert all(o[0]=='UNKNOWN' or (o[0]=='YES')==ref for o in [out,ext])
        if name.startswith('ring'):assert all(len({t[c] for t in T[::4]+T[3::4]})==n for c in range(3))
        if name.startswith('prism'):
            W=[t for i,t in enumerate(T) if (i%(2*(n//2))+i//(2*(n//2)))%2==0];assert all(len({t[c] for t in W})==n for c in range(3))
        if name.startswith('prism'):
            assert all(not list(squares([tuple(t[c] for c in p) for t in T])) for p in [(0,1,2),(0,2,1),(1,2,0)])
            assert closure(n,T)[0]==sorted(T)
        fixtures.append(dict(name=name,n=n,m=len(T),status=out[0],rank=out[1],flow_calls=out[2],closure_probes=out[3],reference=ref,extended_status=ext[0],extended_rank=ext[1],extended_flow_calls=ext[2],extended_closure_probes=ext[3]))
    print(json.dumps(dict(seed=721,flow_equivalence_tests=tests,nonempty_group_tests=exact,unavoidable_group_tests=positive,cycle_relaxation_tests=relaxed,cycle_relaxation_false_admissions=false_admissions,abstract_collective_single_caps=[6,6],abstract_collective_joint_cap=5,long_fill_counterexample=True,fixtures=fixtures),indent=2))
if __name__=='__main__':main()
