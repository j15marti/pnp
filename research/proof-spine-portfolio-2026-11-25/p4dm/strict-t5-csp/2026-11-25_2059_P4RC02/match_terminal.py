from audit import *

def normalize(D,R):
 while True:
  changed=False
  for i in D:
   d={a for a in D[i] if all(any((a,b) in R[i,j] for b in D[j]) for j in D if i!=j)};changed|=d!=D[i];D[i]=d
   if not d:return False
  for i,j in I.combinations(D,2):
   r={(a,b) for a,b in R[i,j] if a in D[i] and b in D[j] and all(any((a,c) in R[i,k] and (b,c) in R[j,k] for c in D[k]) for k in D if k not in (i,j))};changed|=r!=R[i,j];R[i,j]=r;R[j,i]={(b,a) for a,b in r}
   if not r:return False
  if not changed:return True

def terminal(D,R):
 # Source-independent certificate acquisition, no supplied grouping.
 states=[(i,a) for i in D for a in D[i]];uf=nx.utils.UnionFind(states)
 for i,j in I.combinations(D,2):
  for a,b in R[i,j]:
   if {c for c in D[j] if (a,c) in R[i,j]}=={b} and {c for c in D[i] if (c,b) in R[i,j]}=={a}:uf.union((i,a),(j,b))
 classes={}
 for u in states:classes.setdefault(uf[u],[]).append(u)
 footprint={k:{i for i,a in vs} for k,vs in classes.items()}
 if any(len(vs)!=len(footprint[k]) or len(vs)>2 for k,vs in classes.items()):return 'UNKNOWN',None,len(classes)
 for i,j in I.combinations(D,2):
  for a,b in I.product(D[i],D[j]):
   u,v=uf[i,a],uf[j,b];expected=u==v or not footprint[u]&footprint[v]
   if expected!=((a,b) in R[i,j]):return 'UNKNOWN',None,len(classes)
 G=nx.Graph();G.add_nodes_from(('g',i) for i in D)
 for z,(k,vs) in enumerate(classes.items()):
  a=('g',vs[0][0]);b=('g',vs[1][0]) if len(vs)==2 else ('d',z)
  G.add_edge(a,b,weight=len(vs),event=k)
 M=nx.max_weight_matching(G,weight='weight');out={}
 for a,b in M:
  for i,x in classes[G[a][b]['event']]:out[i]=x
 if len(out)!=len(D):return 'NO',None,len(classes)
 assert all((out[i],out[j]) in R[i,j] for i,j in I.combinations(D,2))
 return 'YES',out,len(classes)

def source(T):
 ok,E=nx.check_planarity(graph(T));assert ok and len(set(T))==len(T) and all(len(c)==3 for c in clauses(T));p,calls=closure(T)
 if p is None:return dict(out='NO',groups=0,events=0,matching=calls)
 rows=acquire(T,p,E);D={i:set(range(len(r))) for i,r in enumerate(rows)}
 if any(not x for x in D.values()):return dict(out='NO',groups=len(D),events=0,matching=calls)
 R={(i,j):{(a,b) for a in D[i] for b in D[j] if all(rows[j][b].get(k,v)==v for k,v in rows[i][a].items())} for i,j in I.permutations(D,2)}
 if not normalize(D,R):return dict(out='NO',groups=len(D),events=0,matching=calls)
 out,sel,e=terminal(D,R)
 if sel is not None:
  x=dict(p)
  for i,a in sel.items():
   for j,v in rows[i][a].items():assert x.get(j,v)==v;x[j]=v
  assert verify(T,[j for j,v in x.items() if v])
 return dict(out=out,groups=len(D),events=e,matching=calls)

if __name__=='__main__':
 result={}
 for k,T in [('Q',Q),('U',U),('V',V),('W',W),('star',star())]+[(f'{kind}{k}',chain(k,kind=='NO')) for k in [2,4,8,16] for kind in ['YES','NO']]:
  result[k]=source(T);truth=ref(T) is not None if len(T)<=24 else not k.startswith('NO');assert result[k]['out']=='UNKNOWN' or (result[k]['out']=='YES')==truth
  print(k,result[k],flush=True)
 for k,G in [('K4',nx.complete_graph(4)),('cube',nx.cubical_graph()),('Petersen',nx.petersen_graph()),('dodecahedron',nx.dodecahedral_graph()),('prism6',nx.circular_ladder_graph(6)),('Heawood',nx.heawood_graph())]:
  D={i:{tuple(sorted(e)) for e in G.edges(i)} for i in G};R={(i,j):{(a,b) for a in D[i] for b in D[j] if a==b or not set(a)&set(b)} for i,j in I.permutations(D,2)}
  assert normalize(D,R);out,sel,e=terminal(D,R);assert out!='NO';result['abstract_'+k]=dict(out=out,groups=len(D),events=e);print(k,result['abstract_'+k],flush=True)
 json.dump(result,open('matching_results.json','w'),indent=2)
