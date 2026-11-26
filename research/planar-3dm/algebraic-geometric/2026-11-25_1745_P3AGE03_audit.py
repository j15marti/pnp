import itertools as it, json, networkx as nx
from functools import lru_cache

def oct_chain(n):
    assert n>=2
    T=set(it.product(range(2),repeat=3)); W={(0,0,0),(1,1,1)}
    for k in range(2,n):
        f=min(T-W); T.remove(f)
        T.update(t for t in it.product(*[(f[i],k) for i in range(3)]) if t!=f)
        W.add((k,k,k))
    return T,W

def incidence(T,n):
    G=nx.Graph(); G.add_nodes_from((i,v) for i in range(3) for v in range(n))
    for t in T:
        G.add_edges_from((('t',t),(i,v)) for i,v in enumerate(t))
    return G

def proj_support(T,n,i,j):
    G=nx.Graph(); A=[(i,v) for v in range(n)]; B=[(j,v) for v in range(n)]
    G.add_nodes_from(A+B); G.add_edges_from(((i,t[i]),(j,t[j])) for t in T)
    M=nx.algorithms.bipartite.maximum_matching(G,top_nodes=A)
    if len(M)!=2*n:return None
    D=nx.DiGraph();D.add_nodes_from(G)
    for a in A:
        for b in G[a]:D.add_edge(b,a) if M[a]==b else D.add_edge(a,b)
    comp={v:k for k,c in enumerate(nx.strongly_connected_components(D)) for v in c}
    return {t for t in T if M[(i,t[i])]==(j,t[j]) or comp[(i,t[i])]==comp[(j,t[j])]}

def count(T,n):
    by=[[] for _ in range(n)]
    for x,y,z in T:by[x].append((y,z))
    @lru_cache(None)
    def f(x,Y,Z):
        if x==n:return 1
        return sum(f(x+1,Y|1<<y,Z|1<<z) for y,z in by[x] if not(Y>>y&1 or Z>>z&1))
    return f(0,0,0)

def stats(T,n):
    G=incidence(T,n); p,_=nx.check_planarity(G); deg=min(G.degree((i,v)) for i in range(3) for v in range(n)); supports=[proj_support(T,n,i,j) for i,j in [(0,1),(0,2),(1,2)]]
    return dict(n=n,triples=len(T),planar=p,connected=nx.is_connected(G),min_degree=deg,projection_unsupported=[None if s is None else len(T-s) for s in supports])

def main():
    rows=[]
    for n in [2,3,4,8,16,32,64,128]:
        T,W=oct_chain(n); s=stats(T,n); assert s['planar'] and s['connected'] and s['min_degree']>=4 and W<=T and all(len({t[i] for t in W})==n for i in range(3)); s['witness_verified']=True
        if n<=8:s['count']=count(T,n)
        rows.append(s)
    neighbor=None; examined=0
    for n in [3,4]:
        T,_=oct_chain(n); ts=sorted(T)
        for k in range(1, min(7,len(ts))):
            for rem in it.combinations(ts,k):
                S=T-set(rem); G=incidence(S,n)
                if min(G.degree((i,v)) for i in range(3) for v in range(n))<3:continue
                if any(proj_support(S,n,i,j)!=S for i,j in [(0,1),(0,2),(1,2)]):continue
                examined+=1
                if count(S,n):continue
                for t in rem:
                    if count(S|{t},n):
                        neighbor={'unsat':sorted(S),'add':t,'unsat_stats':stats(S,n),'sat_stats':stats(S|{t},n),'sat_count':count(S|{t},n),'unsat_count':0};break
                if neighbor:break
            if neighbor:break
        if neighbor:break
    print(json.dumps({'family':rows,'neighbor':neighbor,'eligible_subinstances_examined':examined},indent=2))
if __name__=='__main__':main()
