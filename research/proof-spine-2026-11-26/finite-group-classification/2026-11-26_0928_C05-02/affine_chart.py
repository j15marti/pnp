"""Exact XOR-sum of binary projected PM chart responses. Python 3. NetworkX.
Every bit vector represents attained parity of actual owner occupancies, not a hull.
A restricted chart's NO is not a native NO unless its simple pairs exhaust source.
"""
import itertools as it, random, json
from collections import defaultdict,Counter
import networkx as nx
from prev17 import close
from prior import graph,owners,rows,verify,cover
from prev16 import pairs,pm

def basis(vs):
    p={}
    for x in vs:
        while x:
            k=x.bit_length()-1
            if k in p:x^=p[k]
            else:p[k]=x;break
    return list(p.values())

def solve_span(vs,t):
    p={}
    for i,x in enumerate(vs):
        a=1<<i
        while x:
            k=x.bit_length()-1
            if k in p:y,b=p[k];x^=y;a^=b
            else:p[k]=(x,a);break
    a=0
    while t:
        k=t.bit_length()-1
        if k not in p:return None
        x,b=p[k];t^=x;a^=b
    return a

def combination(vs,mask):
    z=0
    while mask:
        b=mask&-mask;mask^=b;z^=vs[b.bit_length()-1]
    return z

def intersection(U,V):
    U=basis(U);V=basis(V);p={};out=[]
    for i,x in enumerate(U+V):
        a=1<<i
        while x:
            k=x.bit_length()-1
            if k in p:y,b=p[k];x^=y;a^=b
            else:p[k]=(x,a);break
        else:out.append(combination(U,a&((1<<len(U))-1)))
    return basis(out)

def affine_union(W,modes):
    # Return base + direction space if W+union of one or two affine cosets is EXACT affine.
    a,U=modes[0];P=basis(W+U)
    if len(modes)==1:return a,P
    b,V=modes[1];Q=basis(W+V);S=basis(P+Q);d=a^b
    meet=solve_span(S,d) is not None
    H=basis(S+[d]);size=(1<<len(P))+(1<<len(Q))-(1<<(len(P)+len(Q)-len(S)) if meet else 0)
    if size==1<<len(H):return a,H
    return None

def join(F,target,cap=8):
    """Each F[i] has one or two (offset,directions). Return exact witness per factor.
    Absorption may be repeated after W grows; branch only on capped unresolved factors.
    """
    common=[basis(f[0][1]) if len(f)==1 else intersection(f[0][1],f[1][1]) for f in F]
    baseW=basis([v for C in common for v in C]);W=baseW;shift=0
    pending=list(range(len(F)));history=[];st=Counter(initial_common_rank=len(W))
    while True:
        changed=False
        for i in pending[:]:
            st['union_checks']+=1;z=affine_union(W,F[i])
            if z is None:continue
            a,V=z;history.append((i,W,shift));W=V;shift^=a;pending.remove(i);changed=True
        if not changed:break
    st.update(absorbed=len(history),kernel=len(pending),final_rank=len(W))
    if len(pending)>cap:return 'UNKNOWN',None,dict(st)
    for choices in it.product(*(range(len(F[i])) for i in pending)):
        st['branches']+=1;v=target^shift;cols=W[:];ends=[]
        for i,b in zip(pending,choices):
            a,U=F[i][b];v^=a;ends.append((len(cols),len(U)));cols+=U
        sol=solve_span(cols,v)
        if sol is None:continue
        chosen={};p=target
        for i,b,(j,l) in zip(pending,choices,ends):
            a,U=F[i][b];r=a^combination(U,(sol>>j)&((1<<l)-1));chosen[i]=(b,r);p^=r
        for i,V,s in reversed(history):
            for b,(a,U) in enumerate(F[i]):
                sol=solve_span(V+U,p^s^a)
                if sol is not None:
                    r=a^combination(U,sol>>len(V));chosen[i]=(b,r);p^=r;break
            else:raise AssertionError('reverse absorption')
        cols=[v for C in common for v in C];sol=solve_span(cols,p);assert sol is not None
        pos=0
        for i,C in enumerate(common):
            b,r=chosen[i];chosen[i]=(b,r^combination(C,(sol>>pos)&((1<<len(C))-1)));pos+=len(C)
        assert combination([r for b,r in chosen.values()],(1<<len(chosen))-1)==target
        assert all(solve_span(F[i][b][1],r^F[i][b][0]) is not None for i,(b,r) in chosen.items())
        return 'YES',chosen,dict(st)
    return 'NO',None,dict(st)

def chart(D,M0,M1,X):
    M0=set(M0);M1=set(M1);G=nx.Graph();G.add_edges_from((('y',y),('z',z)) for y,z in M0|M1)
    groups=[];F=[];lifts=[]
    bits={x:1<<j for j,x in enumerate(sorted(X))}
    for C in sorted(nx.connected_components(G),key=min):
        a=sorted(e for e in M0 if ('y',e[0]) in C);b=sorted(e for e in M1 if ('y',e[0]) in C)
        modes=[a] if a==b else [a,b];groups.append(modes);local=[];lift=[]
        for M in modes:
            base=0;U=[];ids=[];alternates=[]
            for e in M:
                L=sorted(D[e]);assert 1<=len(L)<=2
                base^=bits[L[0]];ids.append(D[e][L[0]])
                if len(L)==2:U.append(bits[L[0]]^bits[L[1]]);alternates.append((len(ids)-1,D[e][L[1]]))
            local.append((base,U));lift.append((ids,alternates))
        F.append(local);lifts.append(lift)
    return F,lifts,groups

def lift_chart(F,lifts,chosen):
    W=[]
    for i,(b,r) in sorted(chosen.items()):
        a,U=F[i][b];sol=solve_span(U,a^r);assert sol is not None
        ids,alt=lifts[i][b];ids=ids[:]
        for j,(p,t) in enumerate(alt):
            if sol>>j&1:ids[p]=t
        W+=ids
    return W

def fixed_hall(D,M,X):
    G=nx.Graph();L=[('p',e) for e in M];G.add_nodes_from(L+[('x',x) for x in X]);G.add_edges_from((('p',e),('x',x)) for e in M for x in D[e]);m=nx.bipartite.maximum_matching(G,top_nodes=L)
    return len(L)-len(m)//2

def exhaustive_modes(D,groups,X):
    for modes in it.product(*groups):
        M=sum(modes,[])
        if not fixed_hall(D,M,X):return True
    return False

def sphere(k):
    # Independent reconstruction of C01-02 face set, IDs sorted by geometry then colored labels.
    vertices=sorted((a,b,c) for a in range(-k,k+1) for b in range(-k,k+1) for c in range(-k,k+1) if abs(a)+abs(b)+abs(c)==k)
    C=lambda v:(abs(v[1])+2*abs(v[2]))%3
    ids={};n=[0]*3
    for v in vertices:ids[v]=n[C(v)];n[C(v)]+=1
    assert len(set(n))==1
    faces=set()
    for signs in it.product((-1,1),repeat=3):
        def v(a,b):return (signs[0]*a,signs[1]*b,signs[2]*(k-a-b))
        for a in range(k):
            for b in range(k-a):
                faces.add(tuple(sorted((v(a,b),v(a+1,b),v(a,b+1)))))
                if a+b+2<=k:faces.add(tuple(sorted((v(a+1,b),v(a,b+1),v(a+1,b+1)))))
    T={}
    for i,f in enumerate(sorted(faces)):
        z=sorted(f,key=C);assert [C(v) for v in z]==[0,1,2];T[i]=tuple(ids[v] for v in z)
    assert len(T)==8*k*k and len(set(T.values()))==len(T)
    return T,owners(n[0])

def dual_defect(D,M,X):
    # Full face chart: every pair has exactly 2 distinct X domains. Multigraph edges are original pairs.
    G=nx.MultiGraph();G.add_nodes_from(X)
    for e in M:
        a,b=D[e];G.add_edge(a,b,key=e)
    sizes=[]
    for C in nx.connected_components(G):sizes.append((len(C),G.subgraph(C).number_of_edges()))
    return sum(e==v-1 for v,e in sizes),sizes

def trial(T,R,rng,trials=10):
    assert nx.check_planarity(graph(T,R))[0]
    A,B,W,closure=close(T,R)
    if A is None:return {'closure':'NO','stats':closure}
    if not B:assert verify(T,R,W);return {'closure':'YES','witness':W,'stats':closure}
    D=pairs(A);X={v for c,v in B if c==0};target=(1<<len(X))-1
    if any(len(v)>2 for v in D.values()):return {'closure':'LIVE','decline':'domain>2','stats':closure}
    rec=[]
    for j in range(trials):
        M0=pm(D,{e:rng.randrange(1000000) for e in sorted(D)});M1=pm(D,{e:rng.randrange(1000000) for e in sorted(D)})
        assert M0 is not None and M1 is not None
        F,lifts,groups=chart(D,M0,M1,X);s,C,st=join(F,target,cap=8)
        full=set(M0)|set(M1)==set(D)
        delta=[fixed_hall(D,M,X) for M in (M0,M1)]
        if all(len(D[e])==2 for e in D.values()):
            for d,M in zip(delta,(M0,M1)):assert dual_defect(D,M,X)[0]==d
        if sum(len(g)==2 for g in groups)<=10:
            exact=exhaustive_modes(D,groups,X);assert s=='UNKNOWN' or (s=='YES')==exact
        witness=None
        if s=='YES':witness=W+lift_chart(F,lifts,C);assert verify(T,R,witness)
        rec.append(dict(status=s,exhaustive_chart=full,deficiencies=delta,st=st,mode_groups=sum(len(g)==2 for g in groups),witness=witness))
    return dict(closure='LIVE',closure_stats=closure,live=len(A),trials=rec)

def main():
    rng=random.Random(261126052);stats=Counter();examples={}
    for _ in range(800):
        n=rng.randrange(2,8);F=[]
        for i in range(rng.randrange(1,7)):
            F.append([(rng.randrange(1<<n),[rng.randrange(1<<n) for _ in range(rng.randrange(4))]) for _ in range(rng.randrange(1,3))])
        target=rng.randrange(1<<n)
        # Actual full support via XOR convolution for independent small reference.
        S={0}
        for f in F:
            R=set()
            for a,U in f:R|={a^combination(U,m) for m in range(1<<len(U))}
            S={x^y for x in S for y in R}
        s,w,st=join(F,target,cap=6);assert (s=='YES')==(target in S)
        stats[s]+=1;stats['absorbed']+=st['absorbed'];stats['branches']+=st['branches']
        if st['kernel']==0 and any(len(f)==2 and affine_union([],f) is None for f in F):stats['cooperative_affine']+=1;examples.setdefault('cooperative',dict(n=n,F=F,target=target,status=s,st=st))
    native=[]
    for k in [1,2,4,5,7,8,13]:
        T,R=sphere(k);z=trial(T,R,rng,12 if k<9 else 5);native.append(dict(k=k,m=len(T),n=len(R)//3,**z));print(k,len(T),Counter(t['status'] for t in z.get('trials',[])),flush=True)
    # All 256 cube subinstances; exact chart is exhaustive whenever live projected degree<=2.
    cubes=[];T=dict(enumerate(it.product(range(2),repeat=3)));R=owners(2)
    for mask in range(256):
        A={i:t for i,t in T.items() if mask>>i&1};truth=cover(A,R) is not None;z=trial(A,R,rng,1)
        if z['closure']!='LIVE':assert (z['closure']=='YES')==truth
        else:
            for r in z.get('trials',[]):
                assert r['status']!='YES' or truth
                if r['exhaustive_chart'] and r['status']=='NO':assert not truth
        cubes.append(dict(mask=mask,truth=truth,**z))
    # Native SAT/UNSAT deletion neighbors by deleting all but one witness then deleting one witness tuple.
    # Explicitly easy negative closure controls, not hard neighbors.
    neighbors=[]
    for a in native:
        hit=next((t['witness'] for t in a.get('trials',[]) if t['witness'] is not None),None)
        if hit is None:continue
        T,R=sphere(a['k']);P={i:T[i] for i in hit};Q=P.copy();Q.pop(hit[0]);assert verify(T,R,hit)
        s=trial(P,R,rng,1);u=trial(Q,R,rng,1);assert s['closure']=='YES' and u['closure']=='NO';neighbors.append(dict(k=a['k'],SAT_ids=hit,deleted=hit[0],sat=s,no=u))
    out=dict(seed=261126052,abstract=dict(stats),examples=examples,native=native,cubes=cubes,neighbors=neighbors)
    json.dump(out,open('results.json','w'),indent=2);print('abstract',stats,'neighbors',len(neighbors))
if __name__=='__main__':main()
