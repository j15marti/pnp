#!/usr/bin/env python3
"""LSPV-2 330 compact source-authenticated general matching terminal.
Requires networkx. Run `python compact330.py` to replay all 729 coherent Z6 pins.
Full independent verification, generic circuits, source fixtures and raw data are in the 330 archive.
"""
import itertools, collections, networkx as nx
POS=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
F=POS+tuple(tuple(-z for z in c) for c in POS)

def validate(clauses,n):
 assert 3*len(clauses)==4*n and len({tuple(sorted(c)) for c in clauses})==len(clauses)
 for c in clauses:
  assert len(c)==3 and len(set(map(abs,c)))==3
  assert all(type(z) is int and 1<=abs(z)<=n for z in c)
  assert all(z>0 for z in c) or all(z<0 for z in c)
 for i in range(1,n+1):assert sum(i in c for c in clauses)==sum(-i in c for c in clauses)==2

def build(clauses,n,pins):
 validate(clauses,n)
 positive=[tuple(sorted(c)) for c in clauses if c[0]>0]
 negative={tuple(sorted(-z for z in c)) for c in clauses if c[0]<0}
 if set(positive)!=negative:return None,None
 assert all(i in range(1,n+1) and b in (0,1) for i,b in pins.items())
 endpoints={i:[] for i in range(1,n+1)}
 for v,c in enumerate(positive):
  for i in c:endpoints[i].append(v)
 H=nx.Graph();ports=collections.defaultdict(list)
 for i,(a,b) in endpoints.items():
  if i in pins:continue
  x=('p',a,i);y=('p',b,i);H.add_edge(x,y,kind='cross',variable=i)
  ports[a].append(x);ports[b].append(y)
 slack=[];lo_total=0
 for v,c in enumerate(positive):
  true=sum(pins.get(i,-1)==1 for i in c)
  r=sum(i not in pins for i in c)
  lo=max(0,1-true);hi=min(r,2-true)
  if lo>hi:return 'LOCAL',v+1
  lo_total+=lo
  for j in range(r-lo):
   d=('d',v,j)
   for e in ports[v]:H.add_edge(d,e)
   for k in range(hi-lo):H.add_edge(d,('t',v,k))
  for k in range(hi-lo):
   t=('t',v,k)
   for u in slack:H.add_edge(t,u)
   H.add_node(t);slack.append(t)
 if (len(slack)-lo_total)%2:
  H.add_node(('parity',))
  for t in slack:H.add_edge(('parity',),t)
 return H,endpoints

def solve(clauses,n,pins,certificate=False):
 H,info=build(clauses,n,pins)
 if H is None:return 'UNRESOLVED',None
 if H=='LOCAL':return 'UNSAT',{'source_clause_pair':info}
 M=nx.max_weight_matching(H,maxcardinality=True)
 if 2*len(M)==len(H):
  true={data['variable'] for x,y in M if (data:=H.get_edge_data(x,y)).get('kind')=='cross'}
  a={i:pins.get(i,int(i in true)) for i in range(1,n+1)}
  assert all(any(a[abs(z)]==int(z>0) for z in c) for c in clauses)
  return 'SAT',a
 if not certificate:return 'UNSAT',{'matched_pairs':len(M)}
 # Paid Gallai-Edmonds extraction: one additional blossom call per H vertex.
 D=set()
 for v in H:
  G=H.copy();G.remove_node(v)
  if len(nx.max_weight_matching(G,maxcardinality=True))==len(M):D.add(v)
 A=set.union(set(),*(set(H.neighbors(v)) for v in D))-D
 odd=sum(len(c)%2 for c in nx.connected_components(H.subgraph(set(H)-A)))
 assert odd>len(A)
 return 'UNSAT',{'Tutte_barrier':[list(v) for v in sorted(A,key=str)],'odd_components':odd,'barrier_size':len(A)}

def models(p):
 free=[i for i in range(1,7) if i not in p];result=0
 for bits in itertools.product((0,1),repeat=len(free)):
  a={**p,**dict(zip(free,bits))}
  result+=all(any(a[abs(z)]==int(z>0) for z in c) for c in F)
 return result

if __name__=='__main__':
 stats=collections.Counter()
 for pin in itertools.product((-1,0,1),repeat=6):
  p={i+1:x for i,x in enumerate(pin) if x!=-1}
  label,_=solve(F,6,p)
  assert (label=='SAT')==(models(p)>0)
  stats[label]+=1
 assert stats=={'SAT':475,'UNSAT':254}
 p={4:0,5:0,6:0};q={4:1,5:0,6:0}
 print('Z6 all 729 coherent pins',dict(stats))
 print('same-original UNSAT',solve(F,6,p,certificate=True),'models',models(p))
 print('same-original SAT',solve(F,6,q),'models',models(q))
 print('P versus NP OPEN')
