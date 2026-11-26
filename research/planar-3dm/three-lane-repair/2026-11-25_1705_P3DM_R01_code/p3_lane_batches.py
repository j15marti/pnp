import itertools as it, collections, random, json, networkx as nx
from p3_lane_explore import incidence,oct_chain,oracle,closure,formula
from p3_lane_terminal import solve

def lane_matchings(T,n,i,j):
    D=[sorted(t for t in T if t[i]==v) for v in range(n)]
    def rec(v,used,A):
        if v==n:yield frozenset(A);return
        for t in D[v]:
            if t[j] not in used:yield from rec(v+1,used|{t[j]},A+[t])
    return list(rec(0,set(),[]))

def mismatch(M):return set.union(*(set(a) for a in M))-set.intersection(*(set(a) for a in M))

def repair(M,Q):
    lanes=[(0,1),(0,2),(1,2)];nodes=[];links=collections.defaultdict(list)
    for k,(i,j) in enumerate(lanes):
        D=set(M[k])^Q;G=nx.MultiGraph()
        for t in D:G.add_edge((i,t[i]),(j,t[j]),key=t)
        assert all(d==2 for _,d in G.degree())
        for S in nx.connected_components(G):
            cycle={t for u,v,t in G.subgraph(S).edges(keys=True)};a=len(nodes);nodes.append((k,cycle))
            for t in cycle:links[t].append(a)
    H=nx.Graph();H.add_nodes_from(range(len(nodes)))
    for L in links.values():H.add_edges_from((L[0],b) for b in L[1:])
    current=[set(a) for a in M];D0=mismatch(current);steps=0;maxcycles=0
    for S in nx.connected_components(H):
        ids=set().union(*(nodes[a][1] for a in S));affected=ids&D0
        if not affected:continue
        before=mismatch(current)
        for a in S:k,C=nodes[a];current[k]^=C
        for k,(i,j) in enumerate(lanes):assert len(current[k])==len(Q) and len({t[i] for t in current[k]})==len(Q) and len({t[j] for t in current[k]})==len(Q)
        assert mismatch(current)==before-affected
        steps+=1;maxcycles=max(maxcycles,len(S))
    assert not mismatch(current) and len(current[0])==len(Q) and all(len({t[i] for t in current[0]})==len(Q) for i in range(3)) and steps<=len(D0)
    if len(D0)==2:assert steps==1
    return len(D0),steps,maxcycles

def main():
    rng=random.Random(20261125);counts=collections.Counter();jobs=0;examples={};maxcycles=0
    for n in (2,3,4,5):
        U=sorted(oct_chain(n))
        for k in range(60):
            p=rng.uniform(.5,1);T={t for t in U if rng.random()<p};Q=oracle(T,n)
            if Q is None:continue
            lanes=[lane_matchings(T,n,i,j) for i,j in [(0,1),(0,2),(1,2)]]
            for _ in range(8):
                M=[rng.choice(L) for L in lanes];a,b,c=repair(M,set(Q));counts[a,b]+=1;jobs+=1;maxcycles=max(maxcycles,c)
                if a==2 and 'minimal' not in examples:examples['minimal']=dict(n=n,T=sorted(T),anchors=[sorted(L) for L in M],target=Q,steps=b,cycles=c)
    T={(0,0,0),(0,0,1),(0,1,0),(0,1,1),(1,0,0),(1,1,1)};S,P=closure(T,2);assert not P and S==T
    D=collections.Counter((i,v) for t in S for i,v in enumerate(t));assert all(max(d for (i,v),d in D.items() if i==c)>2 for c in range(3));assert solve(T,2)[:2]==('YES','invariant')
    B={(0,0,0),(0,0,1),(0,1,0),(1,0,1),(1,1,0),(1,1,1)};assert nx.check_planarity(incidence(B,2))[0] and closure(B,2)==(B,set()) and solve(B,2)[0]=='UNKNOWN' and oracle(B,2) is not None
    U={(0,0,0),(0,0,2),(0,1,0),(0,1,1),(0,2,1),(0,2,2),(1,0,0),(1,0,1),(1,1,1),(2,0,1),(2,0,2),(2,2,1)}
    assert nx.check_planarity(incidence(U,3))[0] and closure(U,3)==(U,set()) and solve(U,3)[0]=='UNKNOWN' and oracle(U,3) is None
    add=next(t for t in sorted(oct_chain(3)-U) if oracle(U|{t},3) is not None);assert nx.check_planarity(incidence(U|{add},3))[0]
    rows=[]
    for k in (1,4,16,64):
        for kind,base,n0 in [('positive_terminal',T,2),('regular_obstruction',B,2),('negative_obstruction',U,3)]:
            A={tuple(x+i*n0 for x in t) for i in range(k) for t in base};n=k*n0;assert nx.check_planarity(incidence(A,n))[0];r,m,w,_=solve(A,n);assert r==('YES' if kind=='positive_terminal' else 'UNKNOWN');rows.append(dict(kind=kind,copies=k,n=n,triples=len(A),result=r,method=m))
    print(json.dumps(dict(seed=20261125,repair_jobs=jobs,counts={str(k):v for k,v in sorted(counts.items())},max_cycles_in_batch=maxcycles,examples=examples,positive_terminal=sorted(T),regular_obstruction=sorted(B),negative_obstruction=sorted(U),neighbor_add=add,scaled=rows),indent=2))
if __name__=='__main__':main()
