from audit import *
r=random.Random(803);cases=300;counts={k:0 for k in ['simplicial','line','enumerated','queries']}
for t in range(cases):
 n=r.randrange(1,11);G=nx.gnp_random_graph(n,r.random(),seed=r.randrange(1<<30));w={u:r.randrange(-5,11) for u in G};S,s=join(G,w,cap=12);assert S is not None
 brute=max(sum(w[u] for u in a) for k in range(n+1) for a in I.combinations(G,k) if not any(G.has_edge(u,v) for u,v in I.combinations(a,2)))
 assert sum(w[u] for u in S)==brute
 for k in counts:counts[k]+=s[k]
print('abstract',cases,counts)
S,s=join(nx.complete_bipartite_graph(4,4),{u:1 for u in range(8)},cap=0);print('K44',S,s);assert S is None
json.dump(dict(cases=cases,counts=counts,K44=s),open('abstract_results.json','w'),indent=2)
