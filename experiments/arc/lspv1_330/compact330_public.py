#!/usr/bin/env python3
"""LSPV1 BROOKS-K9 BATCH330 compact executable. Requires networkx>=3.
Production all-input stdlib Tarjan/colour implementation and independent Node
verifier are separately preserved in LSPV1_BROOKS_K9_DECISION_BATCH330 ZIP.
All returned colouring certificates are source-verified. No P-vs-NP claim.
"""
import itertools,json,math,collections
import networkx as nx

F9P=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
F9N=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
Z6=[(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
B9P=[(1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9)]
B9N=[(1,5,9),(2,6,7),(3,4,8),(1,6,8),(2,4,9),(3,5,7)]
def source(p,n):return list(p)+[tuple(-x for x in c) for c in n]
def product(a,b,k):return list(a)+[tuple((1 if x>0 else -1)*(abs(x)+k) for x in c) for c in b]
def valid(F):
 if not F:return False
 names={abs(x) for c in F for x in c}
 if names!=set(range(1,max(names)+1)):return False
 if any(len(c)!=3 or len(set(map(abs,c)))!=3 or len({x>0 for x in c})!=1 for c in F):return False
 if len({tuple(sorted(c)) for c in F})!=len(F):return False
 v=collections.Counter((abs(x),x>0) for c in F for x in c)
 return all(v[i,True]==2 and v[i,False]==2 for i in names)
def primal(F):
 G=nx.Graph();G.add_nodes_from(abs(x) for c in F for x in c)
 for c in F:G.add_edges_from(itertools.combinations(map(abs,c),2))
 return G
def block_color(B):
 """Constructive 8-colouring on a connected biconnected block, non-K9."""
 vs=set(B); d=dict(B.degree)
 if min(d.values())<8:
  root=min(v for v in vs if d[v]<8)
  dist=nx.single_source_shortest_path_length(B,root)
  order=sorted(vs,key=lambda v:(-dist[v],v));color={}
 else:
  triple=None
  for v in sorted(vs):
   for u,w in itertools.combinations(sorted(B[v]),2):
    if not B.has_edge(u,w) and nx.is_connected(B.subgraph(vs-{u,w})):
     triple=v,u,w;break
   if triple:break
  if triple is None:raise ValueError("Brooks triple missing: K9 or invalid block")
  v,u,w=triple; color={u:0,w:0}
  T=B.subgraph(vs-{u,w})
  dist=nx.single_source_shortest_path_length(T,v)
  order=[x for x in sorted(T,key=lambda x:(-dist[x],x)) if x!=v]+[v]
 for x in order:
  used={color[y] for y in B[x] if y in color}
  color[x]=next(i for i in range(8) if i not in used)
 assert len(color)==len(vs) and all(color[u]!=color[v] for u,v in B.edges)
 return color
def color_component(G):
 blocks=[set(b) for b in nx.biconnected_components(G)]
 if not blocks:return {next(iter(G)):0}
 result={};remain=set(range(len(blocks)))
 while remain:
  if not result:k=min(remain)
  else:
   choices=[i for i in sorted(remain) if len(blocks[i]&set(result))==1]
   assert choices,"block-cut tree stitching"
   k=choices[0]
  b=blocks[k]; local=block_color(G.subgraph(b))
  if result:
   v=next(iter(b&set(result)));old=local[v];new=result[v]
   aa=[x for x in range(8) if x!=old]
   bb=[x for x in range(8) if x!=new]
   perm={old:new,**dict(zip(aa,bb))}
   local={x:perm[y] for x,y in local.items()}
   assert result[v]==local[v]
  result.update(local);remain.remove(k)
 assert all(result[u]!=result[v] for u,v in G.edges)
 return result
def batch(F):
 assert valid(F)
 G=primal(F);assert max(dict(G.degree).values())<=8
 cliques=[];others=[]
 for vset in nx.connected_components(G):
  H=G.subgraph(vset)
  (cliques if len(H)==9 and H.number_of_edges()==36 else others).append(vset)
 for vset in cliques:
  cs=[c for c in F if abs(c[0]) in vset]
  assert len(cs)==12 and models(cs,sorted(vset))>0
 if not others:return dict(k9=len(cliques),ncore=0,independent=[],decision=True)
 colors={}
 for comp in others:colors.update(color_component(G.subgraph(comp)))
 ncore=len(colors)
 classes=[[v for v in colors if colors[v]==c] for c in range(8)]
 I=max(classes,key=len)
 assert len(I)>=math.ceil(ncore/8)
 assert all(not(G.has_edge(u,v)) for u,v in itertools.combinations(I,2))
 mcore=len([c for c in F if abs(c[0]) in colors])
 return dict(k9=len(cliques),ncore=ncore,independent=I,colors=colors,
   restricted_gates=dict(forward=3*mcore-1,factored=3*mcore-4*len(I)-1,raw=3*mcore+4*len(I)-1))
def evals(F,a):
 return all(any((a.get(abs(x),False))==(x>0) for x in c) for c in F)
def models(F,V):
 return sum(evals(F,dict(zip(V,b))) for b in itertools.product([False,True],repeat=len(V)))
def independently_check_projection(F,I,colors):
 V=set(colors);J=sorted(V-set(I))
 H=[c for c in F if abs(c[0]) in V]
 groups={x:[c for c in H if x in list(map(abs,c))] for x in I}
 for x in I:assert len(groups[x])==4
 N=[c for c in H if not set(map(abs,c))&set(I)]
 count=0
 for z in itertools.product([False,True],repeat=len(J)):
  a=dict(zip(J,z))
  q=evals(N,a)
  for x,cs in groups.items():
   pos=[tuple(y for y in c if abs(y)!=x) for c in cs if x in c]
   neg=[tuple(y for y in c if abs(y)!=x) for c in cs if -x in c]
   q=q and (evals(pos,a) or evals(neg,a))
  brute=any(evals(H,{**a,**dict(zip(I,b))}) for b in itertools.product([False,True],repeat=len(I)))
  assert q==brute
  count+=q
 return count
def main():
 f9=source(F9P,F9N);z6=source(Z6,Z6);b9=source(B9P,B9N)
 records=[]
 for name,F in [('F9',f9),('Z6',z6),('B9',b9),('H15',product(f9,z6,9)),('B18',product(b9,b9,9))]:
  b=batch(F);n=len({abs(x) for c in F for x in c})
  b.update(name=name,n=n,models=models(F,list(range(1,n+1))))
  if b['ncore']:b['projectedModels']=independently_check_projection(F,b['independent'],b['colors'])
  records.append(b)
 pins={3:False,5:True,6:False,7:False,8:False}
 srcout={}
 for xb in (False,True):
  p={**pins,1:xb};free=[2,4,9]
  srcout[int(xb)]=sum(evals(f9,{**p,**dict(zip(free,a))}) for a in itertools.product([False,True],repeat=3))
 assert srcout=={0:2,1:0}
 print(json.dumps(dict(status="PASS",sourceModels=records,sameOriginalF9=srcout),indent=2))
if __name__=="__main__":main()
