import itertools as it, json, random, time
import networkx as nx

def allmatch(G):
    def rec(V,M):
        if not V:yield tuple(M);return
        u=min(V,key=lambda x:len(set(G[x])&V))
        for v in sorted(set(G[u])&V):yield from rec(V-{u,v},M+[(u,v)])
    yield from rec(set(G),[])
def basis(G,E):
    ids={frozenset(e):i for i,e in enumerate(E)}
    return [sum(1<<ids[frozenset((u,v))] for u,v in zip(C,C[1:]+C[:1])) for C in nx.cycle_basis(G)]
def span(B):
    v=[0]
    for x in B:v += [y^x for y in v]
    return v
def tjoin(G,E,a):
    S=nx.Graph();S.add_nodes_from(G);S.add_edges_from(e for i,e in enumerate(E) if a>>i&1)
    ids={v:i for i,C in enumerate(nx.connected_components(S)) for v in C}
    H=nx.MultiGraph();H.add_nodes_from(ids.values());H.add_edges_from((ids[u],ids[v]) for i,(u,v) in enumerate(E) if not(a>>i&1))
    q=0
    for C in nx.connected_components(H):
        T=[u for u in C if H.degree(u)%2];K=nx.Graph();K.add_nodes_from(T)
        for u,v in it.combinations(T,2):K.add_edge(u,v,weight=nx.shortest_path_length(H,u,v))
        M=nx.min_weight_matching(K);assert 2*len(M)==len(T)
        q+=sum(K[u][v]['weight'] for u,v in M)
    return q
if __name__=='__main__':
    rng=random.Random(20261126);rows=[]
    for name,G in [('K4',nx.complete_graph(4)),('cube',nx.cubical_graph()),('Petersen',nx.petersen_graph()),('Heawood',nx.heawood_graph()),('Desargues',nx.desargues_graph()),('disjoint K4 pair',nx.disjoint_union(nx.complete_graph(4),nx.complete_graph(4)))]:
        E=list(G.edges);B=basis(G,E);flows=span(B);Ms=list(allmatch(G));even=0
        for M in Ms:
            H=G.copy();H.remove_edges_from(M)
            if all(len(C)%2==0 for C in nx.connected_components(H)):even+=1
        for a in rng.sample(flows,min(20,len(flows))):
            v=min(len(E)-(a|b).bit_count() for b in flows);assert v==tjoin(G,E,a)
        rows.append(dict(name=name,n=len(G),m=len(E),basis=len(B),matchings=len(Ms),even_complements=even,projection_checks=min(20,len(flows))))
    print(json.dumps(rows,indent=2));open('/mnt/data/c03_08_controls_results.json','w').write(json.dumps(rows,indent=2)+'\n')
