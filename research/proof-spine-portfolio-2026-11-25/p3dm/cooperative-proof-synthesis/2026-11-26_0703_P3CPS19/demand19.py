"""Exact Boolean support projection by contextual exclusion of opposing demands."""
import itertools as it, random, json, sys
import networkx as nx

def words(k): return it.product((0,1),repeat=k)
def evalF(F,a): return all(tuple(a[v] for v in P) in R for P,R in F)
def norm(F):
    D={}
    for P,R in F:
        if P in D:D[P]&=R
        else:D[P]=set(R)
    if any(not R for R in D.values()):return None
    return [(P,R) for P,R in D.items() if len(R)!=2**len(P)]
def binary_hull(F):
    V={v for P,R in F for v in P};G=nx.DiGraph();G.add_nodes_from((v,b) for v in V for b in (0,1))
    for P,R in F:
        for i,v in enumerate(P):
            B={w[i] for w in R}
            for b in (0,1):
                if b not in B:G.add_edge((v,b),(v,1-b))
        for i,j in it.combinations(range(len(P)),2):
            B={(w[i],w[j]) for w in R};v,u=P[i],P[j]
            for a,b in words(2):
                if (a,b) not in B:G.add_edge((v,a),(u,1-b));G.add_edge((u,b),(v,1-a))
    C=nx.condensation(G);M=C.graph['mapping'];bad=any(M[v,0]==M[v,1] for v in V)
    return G,C,M,bad

def try_elim(F,x,stats=None):
    # Projections of all x-factors and exact forced-value contexts.
    D=[[],[]];G=[];k=0
    for P,R in F:
        if x not in P:G.append((P,R));continue
        k+=1;i=P.index(x);Q=P[:i]+P[i+1:];A={}
        for w in R:A.setdefault(w[:i]+w[i+1:],set()).add(w[i])
        G.append((Q,set(A)))
        for w,B in A.items():
            if len(B)==1:D[next(iter(B))].append(tuple(zip(Q,w)))
    G=norm(G)
    if G is None:return 'NO',None,None
    # Every completion of G must avoid simultaneously demanding 0 and 1.
    # First check direct conflicts, then exact 2SAT consequence of necessary projections.
    H,C,M,bad=binary_hull(G)
    if bad:return 'NO',None,None
    reach={}
    def conflict(P,Q):
        if stats is not None:stats['pairs']+=1
        A=dict(P)
        if any(v in A and A[v]!=b for v,b in Q):return True
        A.update(Q);lits=list(A.items())
        # Exact local support exclusion; this may use a non-bijunctive table.
        for U,R in G:
            pins=[(i,A[v]) for i,v in enumerate(U) if v in A]
            if pins and not any(all(w[i]==b for i,b in pins) for w in R):
                if stats is not None:stats['table_pairs']=stats.get('table_pairs',0)+1
                return True
        for v,b in lits:
            s=M.get((v,b))
            if s is None:continue
            if s not in reach:reach[s]=nx.descendants(C,s)|{s}
            if any(M.get((u,1-c)) in reach[s] for u,c in lits):
                if stats is not None:stats['hull_pairs']+=1
                return True
        return False
    if any(not conflict(P,Q) for P in D[0] for Q in D[1]):return 'OPEN',None,None
    # Retain only demand-1 patterns: if none matches choose zero.
    return 'OK',G,(x,D[1])

def restore(a,trace):
    a=dict(a)
    for x,D in reversed(trace):a[x]=int(any(all(a.get(v,0)==b for v,b in P) for P in D))
    return a

def fixed_closure(F):
    # exact table pins + SCC-derived unary forced bits from binary hull.
    F=norm(F);trace=[]
    while F is not None:
        H,C,M,bad=binary_hull(F)
        if bad:return None,trace
        forced={}
        for v,b in sorted(M):
            if nx.has_path(C,M[v,b],M[v,1-b]):forced[v]=1-b
        if not forced:return F,trace
        # demand trace encodes constants, reverse order immaterial.
        trace.extend((v,[()] if b else []) for v,b in forced.items())
        Q=[]
        for P,R in F:
            I=[i for i,v in enumerate(P) if v not in forced]
            A={tuple(w[i] for i in I) for w in R if all(v not in forced or w[i]==forced[v] for i,v in enumerate(P))}
            Q.append((tuple(P[i] for i in I),A))
        F=norm(Q)
    return None,trace

def solve(F,terminal=None):
    F,trace=fixed_closure(F);stats={'pairs':0,'hull_pairs':0,'attempts':0,'eliminated':0,'max_scope':0,'trace_bits':0,'table_pairs':0,'geometric_calls':0}
    if F is None:return 'NO',None,stats
    while F:
        V={v for P,R in F for v in P}
        if all(len(P)<=2 for P,R in F):
            H,C,M,bad=binary_hull(F)
            if bad:return 'NO',None,stats
            rank={v:i for i,v in enumerate(nx.topological_sort(C))};a={v:int(rank[M[v,1]]>rank[M[v,0]]) for v in V};assert evalF(F,a)
            return 'YES',restore(a,trace),stats
        if terminal is not None:
            stats['geometric_calls']+=1
            s,a=terminal(F)
            if s=='NO':return s,None,stats
            if s=='YES':return s,restore(a,trace),stats
        # try high fanout nonquadratic modes first, then all others; order acquired from factors.
        counts={v:sum(v in P and len(P)>=3 and len(R)==2**len(P)-1 for P,R in F) for v in V}
        order=sorted(V,key=lambda v:(-counts[v],v))
        for x in order:
            stats['attempts']+=1;scope={v for P,R in F if x in P for v in P}-{x}
            s,G,D=try_elim(F,x,stats)
            if s=='NO':return 'NO',None,stats
            if s=='OK':
                stats['eliminated']+=1;stats['max_scope']=max(stats['max_scope'],len(scope));stats['trace_bits']+=sum(len(p) for p in D[1]);trace.append(D);F,t=fixed_closure(G);trace+=t
                if F is None:return 'NO',None,stats
                break
        else:return 'OPEN',(F,trace),stats
    return 'YES',restore({},trace),stats

def audit():
    rng=random.Random(26112619);checks=admitted=hull_only=table_only=0;counts={}
    for trial in range(1000):
        n=rng.randrange(2,8);F=[]
        for j in range(rng.randrange(1,9)):
            P=tuple(sorted(rng.sample(range(n),rng.randrange(1,min(n,4)+1))))
            R={w for w in words(len(P)) if rng.random()<0.65}
            if not R:R={next(words(len(P)))}
            F.append((P,R))
        x=rng.randrange(n);st={'pairs':0,'hull_pairs':0,'table_pairs':0};s,G,D=try_elim(F,x,st);counts[s]=counts.get(s,0)+1
        Y=tuple(v for v in range(n) if v!=x)
        for w in words(len(Y)):
            a=dict(zip(Y,w));truth=any(evalF(F,dict(a,**{})|{x:b}) for b in (0,1));checks+=1
            if s=='NO':assert not truth
            if s=='OK':
                assert evalF(G,a)==truth
                if truth:assert evalF(F,restore(a,[D]));admitted+=1
        hull_only+=s=='OK' and st['hull_pairs']>0
        table_only+=s=='OK' and st['table_pairs']>0
    # Independent simple counterexample to separate projections.
    F=[((0,1),{(0,0),(1,1)}),((0,2),{(0,0),(1,1)})]
    assert try_elim(F,0)[0]=='OPEN'
    print(json.dumps({'trials':1000,'assignments':checks,'valid_lifts':admitted,'hull_admitted':hull_only,'table_admitted':table_only,'status':counts},sort_keys=True))
if __name__=='__main__':audit()
