import itertools as I,networkx as nx,json
# Each group selects one of the three edges incident to a cubic vertex.
# Two group states conflict iff their edges intersect but are distinct.
# This is precisely the pairwise-consistent perfect-matching representation.
def check(G):
 D={i:{tuple(sorted(e)) for e in G.edges(i)} for i in G};R={(i,j):{(a,b) for a in D[i] for b in D[j] if a==b or not set(a)&set(b)} for i,j in I.permutations(D,2)}
 rounds=0
 while True:
  rounds+=1;changed=False
  for i in D:
   d={a for a in D[i] if all(any((a,b) in R[i,j] for b in D[j]) for j in D if i!=j)};changed|=d!=D[i];D[i]=d
   if not d:return dict(groups=len(G),reject=True)
  for i,j in I.combinations(D,2):
   r={(a,b) for a,b in R[i,j] if a in D[i] and b in D[j] and all(any((a,c) in R[i,k] and (b,c) in R[j,k] for c in D[k]) for k in D if k not in (i,j))};changed|=r!=R[i,j];R[i,j]=r;R[j,i]={(b,a) for a,b in r}
   if not r:return dict(groups=len(G),reject=True)
  if not changed:break
 obs={}
 for k in D:
  if len(D[k])!=3:continue
  veto={a:[] for a in D[k]}
  for i in D:
   if i==k:continue
   for a in D[i]:
    missing=D[k]-{b for b in D[k] if (a,b) in R[i,k]}
    if len(missing)==1:veto[next(iter(missing))].append((i,a))
  for u,v,w in I.product(*veto.values()):
   if len({u[0],v[0],w[0]})==3 and all((a[1],b[1]) in R[a[0],b[0]] for a,b in I.combinations((u,v,w),2)):
    obs[k]=(u,v,w);break
 return dict(groups=len(G),rounds=rounds,obstructed=len(obs),matching=len(nx.max_weight_matching(G,maxcardinality=True)),examples=obs)
if __name__=='__main__':
 r={k:check(g) for k,g in [('K4',nx.complete_graph(4)),('cube',nx.cubical_graph()),('Petersen',nx.petersen_graph()),('dodecahedron',nx.dodecahedral_graph()),('prism6',nx.convert_node_labels_to_integers(nx.circular_ladder_graph(6))),('Heawood',nx.heawood_graph())]};print(json.dumps(r,indent=2));json.dump(r,open('abstract_results.json','w'),indent=2)
