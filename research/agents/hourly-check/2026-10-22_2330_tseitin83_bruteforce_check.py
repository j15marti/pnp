"""Brute-force sanity check of TSEITIN-EXPANDER-PAIR83 Lemmas 83A/83B on small connected cubic graphs.
For each graph and every charge b in F_2^V: SAT iff sum(b)=0 (83A); for odd b, every
proper subset of vertex gadgets is satisfiable (83B, block-minimal UNSAT). Runs in a few seconds."""
import itertools, json, networkx as nx

def graphs():
    yield "K4", nx.complete_graph(4)
    yield "K33", nx.complete_bipartite_graph(3,3)
    yield "prism3", nx.circular_ladder_graph(3)
    yield "cube", nx.hypercube_graph(3)
    yield "petersen", nx.petersen_graph()

def sat(G, edges, b, verts):
    idx = {e:i for i,e in enumerate(edges)}
    inc = {v:[idx[e] for e in edges if v in e] for v in verts}
    for x in range(1<<len(edges)):
        if all((sum((x>>i)&1 for i in inc[v])&1)==b[v] for v in verts): return True
    return False

res = {}
for name,G in graphs():
    G = nx.convert_node_labels_to_integers(G)
    assert all(d==3 for _,d in G.degree()) and nx.is_connected(G)
    V = list(G.nodes); E = [tuple(sorted(e)) for e in G.edges]
    ok83a = ok83b = True; nb=0; ns=0
    for b in itertools.product([0,1], repeat=len(V)):
        if len(E) > 15 and nb % 7: nb+=1; continue   # sample for Petersen/cube (15/12 edges)
        nb+=1
        s = sat(G,E,b,V)
        ok83a &= (s == (sum(b)%2==0))
        if sum(b)%2==1:
            for v in V:
                ns+=1
                ok83b &= sat(G,E,b,[u for u in V if u!=v])
    res[name]={"V":len(V),"E":len(E),"83A":ok83a,"83B":ok83b,"charges":nb,"subset_checks":ns}
print(json.dumps(res,indent=1))
json.dump(res,open("research/agents/hourly-check/2026-10-22_2330_tseitin83_bruteforce_results.json","w"),indent=1)
