import json, itertools as I
from audit import *
from honey import honey

def splice(blocks):
    T=[];n=0;starts=[]
    for R,k in blocks:
        starts.append(len(T));T.extend(tuple(n+v for v in t) for t in R);n+=k
    # join two edge-disjoint blocks by exchanging the Y endpoints of one incidence each
    for j in range(len(blocks)-1):
        a=starts[j]+(1 if j else 0);b=starts[j+1];u=list(T[a]);v=list(T[b]);u[1],v[1]=v[1],u[1];T[a]=tuple(u);T[b]=tuple(v)
    return T,n

def acquire_groups(T,n):
    G=source(T,n);P=[sorted(v-3*n for v in S if v>=3*n) for S in nx.k_edge_components(G,k=3)];P=[S for S in P if S];assert sorted(i for S in P for i in S)==list(range(len(T)))
    H=nx.Graph();H.add_nodes_from(range(len(P)));O=defaultdict(set)
    for j,S in enumerate(P):
        for i in S:
            for c,v in enumerate(T[i]):O[c,v].add(j)
    for S in O.values():H.add_edges_from(I.combinations(S,2))
    assert nx.is_connected(H);order=list(nx.bfs_tree(H,min(H,key=lambda j:(H.degree(j),j))))
    return [P[j] for j in order]

if __name__=='__main__':
    a=json.load(open('medial96.json'));M=list(map(tuple,a['T']));h,hn=honey(2,2);out=[]
    for sat in (False,True):
        T,n=splice([(V if sat else U,3),(h,hn),(M,a['n'])]);G=source(T,n);assert nx.is_connected(G);A,calls=close(T,n);assert A==list(range(len(T)));P=acquire_groups(T,n);print('groups',list(map(len,P)),flush=True);r=seam_solver(T,n,P);print(r['status'],r['leaf_methods'],flush=True);assert r['status']==('YES' if sat else 'NO');out.append({'m':len(T),'sat':sat,'groups':list(map(len,P)),'closure_calls':calls,**r})
    json.dump(out,open('hybrid_results.json','w'),indent=2)
