import itertools as it, random, json, collections, sys
import networkx as nx
SEED=20261126
rng=random.Random(SEED)

def planar(n,T):
    G=nx.Graph();G.add_nodes_from((a,i) for a in range(3) for i in range(n))
    for j,t in enumerate(T):G.add_edges_from(((3,j),(a,t[a])) for a in range(3))
    return nx.check_planarity(G)[0]

def oracle(n,T):
    by=[[t for t in T if t[0]==x] for x in range(n)]
    def f(i,Y,Z):
        if i==n:return True
        return any(f(i+1,Y|{t[1]},Z|{t[2]}) for t in by[i] if t[1] not in Y and t[2] not in Z)
    return f(0,set(),set())

def close(n,T):
    T=set(T)
    while True:
        old=T.copy()
        for a in range(3):
            for v in range(n):
                A=[t for t in T if t[a]==v]
                if not A:return None
                if len(A)==1:
                    t=A[0];T={u for u in T if u==t or all(u[b]!=t[b] for b in range(3))}
        for a,b in [(0,1),(0,2),(1,2)]:
            L=[(a,i) for i in range(n)];G=nx.Graph();G.add_nodes_from(L+[(b,i) for i in range(n)])
            G.add_edges_from(((a,t[a]),(b,t[b])) for t in T)
            M=nx.bipartite.maximum_matching(G,top_nodes=L)
            if len(M)!=2*n:return None
            D=nx.DiGraph();D.add_nodes_from(L);D.add_edges_from(((a,t[a]),M[(b,t[b])]) for t in T)
            C={v:i for i,A in enumerate(nx.strongly_connected_components(D)) for v in A}
            T={t for t in T if C[(a,t[a])]==C[M[(b,t[b])]]}
        if T==old:return T

def tables(T,cap=3):
    G=nx.Graph();G.add_edges_from(((0,t[0]),(1,t[1])) for t in T);A=[]
    for C in nx.connected_components(G):
        X=sorted(v for a,v in C if a==0);r=len(X)
        if r>cap:return None
        W=collections.defaultdict(list)
        for Q in it.product(*[sorted(t for t in T if t[0]==x) for x in X]):
            if len({t[1] for t in Q})==r and len({t[2] for t in Q})==r:W[frozenset(t[2] for t in Q)].append(Q)
        A.append((r,dict(W)))
    return A

def ismat(W):
    return bool(W) and all(any((a-{x})|{y} in W for y in b-a) for a,b in it.product(W,repeat=2) for x in a-b)

def mi(E,I1,I2):
    J=set()
    while True:
        O=set(E)-J;starts=[x for x in sorted(O) if I1(J|{x})];ends={x for x in O if I2(J|{x})}
        Q=collections.deque(starts);prev={x:None for x in starts};end=None
        while Q:
            x=Q.popleft()
            if x in ends:end=x;break
            nxt=[y for y in sorted(J) if I2((J-{y})|{x})] if x in O else [y for y in sorted(O) if I1((J-{x})|{y})]
            for y in nxt:
                if y not in prev:prev[y]=x;Q.append(y)
        if end is None:return J
        path=set()
        while end is not None:path.add(end);end=prev[end]
        K=J^path;assert len(K)==len(J)+1 and I1(K) and I2(K);J=K

def direct_intersection(G,ind):
    E=[(i,z) for i,(r,W) in enumerate(G) for z in sorted(set().union(*W))]
    def I1(J):return all(any({z for j,z in J if j==i}<=B for B in W) for i,(r,W) in enumerate(G))
    return mi(E,I1,ind)

def alloc(G,S):
    return direct_intersection(G,lambda J:len({z for i,z in J})==len(J) and all(z in S for i,z in J))

def core(Z,H,rank):
    # H list of (quota, collection of equal-size tag rows), known individually independent.
    C=set();k=0;quot=[];drops=[];maxcore=0
    for i,(r,W) in enumerate(H):
        common={z for z in Z if all(rank(B|{z})==r for B in W)}
        K=set()
        for z in sorted(common):
            if rank(K|{z})>len(K):K.add(z)
        maxcore=max(maxcore,len(K));C|=K;k+=len(K)
        V=collections.defaultdict(list)
        for B in W:
            E=set()
            for z in sorted(B):
                if rank(K|E|{z})>len(K)+len(E):E.add(z)
            assert len(E)==r-len(K)
            V[frozenset(E)].append(B)
        quot.append((r-len(K),dict(V)))
    if rank(C)!=k:return False,'core_conflict',None,maxcore,[]
    for i,(d,V) in enumerate(quot):
        for E,Bs in V.items():
            if rank(C|E)!=k+d:drops += [(i,B) for B in Bs]
    if drops:return None,'drop',None,maxcore,drops
    if any(not ismat(V) for d,V in quot):return None,'quotient_nonmatroid',None,maxcore,[]
    J=direct_intersection(quot,lambda J:rank(C|{z for i,z in J})==k+len(J))
    if len(J)!=sum(d for d,V in quot):return False,'intersection',None,maxcore,[]
    B=[V[frozenset(z for j,z in J if i==j)][0] for i,(d,V) in enumerate(quot)]
    assert rank(set().union(*B) if B else set())==sum(r for r,W in H)
    return True,'core',B,maxcore,[]

def solve(n,T):
    S=close(n,T)
    if S is None:return False,'closure',0,0,None
    A=tables(S)
    if A is None:return None,'table_cap',0,0,None
    deleted=0;mx=0
    while True:
        if any(not W for r,W in A):return False,'empty',mx,deleted,None
        S=close(n,{t for r,W in A for Qs in W.values() for Q in Qs for t in Q})
        if S is None:return False,'reclosure',mx,deleted,None
        for r,W in A:
            for B in list(W):
                W[B]=[Q for Q in W[B] if set(Q)<=S]
                if not W[B]:del W[B];deleted+=1
        if any(not W for r,W in A):return False,'empty',mx,deleted,None
        if {t for r,W in A for Qs in W.values() for Q in Qs for t in Q}!=S:continue
        G=[a for a in A if ismat(a[1])];H=[a for a in A if not ismat(a[1])]
        R=sum(r for r,W in G);Z=set(range(n))
        if len(alloc(G,Z))<R:return False,'alloc',mx,deleted,None
        memo={}
        def rank(B):
            B=frozenset(B)
            if B not in memo:memo[B]=len(B)-R+len(alloc(G,Z-B))
            return memo[B]
        drops=[(i,B) for i,(r,W) in enumerate(H) for B in W if rank(B)!=r]
        if drops:
            for i,B in drops:del H[i][1][B];deleted+=1
            continue
        a,m,B,c,drops=core(Z,H,rank);mx=max(mx,c)
        if drops:
            for i,b in drops:del H[i][1][b];deleted+=1
            continue
        if a is not True:return a,m,mx,deleted,None
        used=set().union(*B) if B else set();J=alloc(G,Z-used);assert len(J)==R
        Q=[t for (r,W),b in zip(H,B) for t in W[b][0]]+[t for i,(r,W) in enumerate(G) for t in W[frozenset(z for j,z in J if j==i)][0]]
        assert len(Q)==n and all(len({t[a] for t in Q})==n for a in range(3)) and set(Q)<=set(T)
        return True,m,mx,deleted,Q

def parse(s):return [tuple(map(int,t)) for t in s.split()]
F=parse('002 003 110 111 221 230 323 332')
U=parse('000 003 111 112 221 230 323 332')
J=parse('003 000 010 102 111 113 220 222 332 331')

def source_audit(jobs=3000):
    stats=collections.Counter();examples={};skips=0;fixed=[]
    for name,n,T in [('F',4,F),('U',4,U),('Uplus',4,U+[(2,2,0)]),('J',4,J)]:
        assert planar(n,T);o=oracle(n,T);a=solve(n,T);assert a[0]==o
        fixed.append(dict(name=name,oracle=o,closed=len(close(n,T) or []),result=a))
    for job in range(jobs):
        n=rng.randrange(4,9);T=[];i=0
        while i<n:
            r=min(n-i,rng.choice([1,1,2,2,3]));
            if r==1:T += [(i,i,z) for z in rng.sample(range(n),rng.choice([2,3,4]))]
            elif r==2:
                for x,y in it.product(range(i,i+2),repeat=2):
                    for z in rng.sample(range(n),rng.choice([1,1,1,2])):T.append((x,y,z))
            else:
                for x in range(r):
                    for d in (0,1):T.append((i+x,i+(x+d)%r,rng.randrange(n)))
            i+=r
        if not planar(n,T):skips+=1;continue
        a,m,c,d,Q=solve(n,T);o=oracle(n,T);assert a is None or a==o
        key=str((a,m,c>0,d>0,o));stats[key]+=1
        if c or d or a is None:examples.setdefault(key,dict(n=n,T=T,answer=a,method=m,core=c,deleted=d,witness=Q))
    return dict(stats=stats,examples=examples,skips=skips,fixed=fixed)

def abstract_audit():
    # Oracle controls only, not claimed incidence-planar P3DM instances.
    results=[]
    for k in (4,8,16,32,64):
        # Private rank-one pairs + one large uniform circuit and a two-tag free block.
        # k-1 phases must use k-1 tags in A, last phase uses B.
        A=set(range(2*k,3*k-1));B={3*k-1,3*k};Z=set(range(3*k+1))
        H=[(2,[frozenset({2*i,2*k+i}),frozenset({2*i+1,2*k+(i+1)%(k-1)})]) for i in range(k-1)]
        H.append((2,[frozenset({2*k-2,3*k-1}),frozenset({2*k-1,3*k})]))
        for yes in (True,False):
            def rank(S):return sum(bool({2*i,2*i+1}&S) for i in range(k))+min(len(S&A),k-1 if yes else k-2)+min(len(S&B),1 if yes else 2)
            a,m,W,c,drop=core(Z,H,rank);assert a==yes and not drop
            # Initial pairs of chosen rows have no dependence for all first options.
            assert all(rank(x|y)==4 for x,y in it.combinations([V[0] for r,V in H],2))
            results.append(dict(k=k,answer=a,method=m,maxcore=c,rank=rank(Z),active=len(Z)))
    # Random linear-matroid controls: general arbitrary rows and planted virtual cores.
    counts=collections.Counter()
    def binary_rank(xs):
        b={}
        for x in xs:
            while x:
                j=x.bit_length()-1
                if j in b:x^=b[j]
                else:b[j]=x;break
        return len(b)
    for job in range(400):
        n=rng.randrange(4,11);Z=set(range(n));v=[rng.randrange(1,16) for _ in Z]
        rank=lambda S:binary_rank(v[z] for z in S)
        H=[]
        for i in range(rng.randrange(1,4)):
            r=rng.choice([1,2,3]);W=[frozenset(B) for B in it.combinations(Z,r) if rank(set(B))==r]
            if W:H.append((r,rng.sample(W,min(len(W),rng.randrange(1,5)))))
        if not H:continue
        expected=any(rank(set().union(*B))==sum(r for r,W in H) for B in it.product(*(W for r,W in H)))
        while True:
            if any(not W for r,W in H):a=False;m='empty';break
            a,m,B,c,drops=core(Z,H,rank)
            if not drops:break
            for i,b in drops:H[i][1].remove(b)
        assert a is None or a==expected;counts[str((a,m,expected))]+=1
    return dict(scale=results,random=counts)

def scale_source():
    R=[]
    for name,T in [('F',F),('U',U)]:
        for k in (1,4,8):
            Q=[tuple(v+4*i for v in t) for i in range(k) for t in T]
            Q += [(4*i,4*i,4*(i+1)) for i in range(k-1)]
            assert planar(4*k,Q)
            S=close(4*k,Q);assert S=={tuple(v+4*i for v in t) for i in range(k) for t in T}
            # After paid closure all bridges are absent; use actual component copies.
            a=[solve(4,[tuple(v-4*i for v in t) for t in S if t[0]//4==i])[0] for i in range(k)]
            assert all(x==(name=='F') for x in a)
            R.append(dict(name=name,k=k,triples=len(Q),retained=len(S),answer=all(a)))
    return R

if __name__=='__main__':
    mode=sys.argv[1] if len(sys.argv)>1 else 'source'
    print(json.dumps({'seed':SEED,'mode':mode,'results':source_audit() if mode=='source' else abstract_audit() if mode=='abstract' else scale_source()},sort_keys=True))
