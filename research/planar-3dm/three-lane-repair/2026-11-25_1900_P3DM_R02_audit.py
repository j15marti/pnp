import itertools as it, random, json, networkx as nx

def graph(n,T,a,b):
 g=nx.Graph();g.add_nodes_from((a,i) for i in range(n));g.add_nodes_from((b,i) for i in range(n));g.add_edges_from(((a,t[a]),(b,t[b])) for t in T);return g

def planar(n,T):
 g=nx.Graph();g.add_nodes_from((c,i) for c in range(3) for i in range(n))
 for j,t in enumerate(T):g.add_edges_from(((3,j),(c,v)) for c,v in enumerate(t))
 return nx.check_planarity(g)[0]

def pm(n,T,a,b,force=None):
 g=graph(n,T,a,b);left={(a,i) for i in range(n)}
 if force is not None:
  u,v=(a,force[a]),(b,force[b]);g.remove_nodes_from([u,v]);left.remove(u)
 return len(nx.bipartite.maximum_matching(g,top_nodes=left))==2*len(left)

def closure(n,T):
 T=list(T)
 while True:
  before=len(T)
  for a,b in [(0,1),(0,2),(1,2)]:
   if not pm(n,T,a,b):return None
   T=[t for t in T if pm(n,T,a,b,t)]
  forced=[]
  for c in range(3):
   for v in range(n):
    ts=[t for t in T if t[c]==v]
    if not ts:return None
    if len(ts)==1:forced.append(ts[0])
  T=[t for t in T if all(t==s or all(x!=y for x,y in zip(t,s)) for s in forced)]
  if len(T)==before:return T

def oracle(n,T):
 by=[[t for t in T if t[0]==i] for i in range(n)]
 def rec(i,y,z):
  if i==n:return True
  return any(rec(i+1,y|{b},z|{c}) for _,b,c in by[i] if b not in y and c not in z)
 return rec(0,set(),set())

def blocks(n,T,a,b):
 c=3-a-b;out=[]
 for C in nx.connected_components(graph(n,T,a,b)):
  xs=sorted(i for k,i in C if k==a);ys={i for k,i in C if k==b}
  if len(xs)!=len(ys):return False
  if len(xs)>2:return None
  B={}
  for ts in it.product(*[[t for t in T if t[a]==x] for x in xs]):
   if len({t[b] for t in ts})!=len(xs):continue
   tags=frozenset(t[c] for t in ts)
   if len(tags)==len(xs):B[tags]=ts
  if not B:return False
  out.append((len(xs),B))
 return out

def flow(n,bs):
 G=nx.DiGraph();S='s';T='t';G.add_nodes_from([S,T])
 for z in range(n):G.add_edge(('z',z),T,capacity=1)
 for i,(r,B) in enumerate(bs):
  active=set().union(*B);G.add_edge(S,('b',i),capacity=r)
  # Rank two: nonadjacency among nonloops must be an equivalence relation.
  if r==1:classes=[active]
  else:
   H=nx.Graph();H.add_nodes_from(active);H.add_edges_from((u,v) for u,v in it.combinations(active,2) if frozenset([u,v]) not in B)
   classes=list(nx.connected_components(H))
   if any(not all(frozenset([u,v]) not in B for u,v in it.combinations(C,2)) for C in classes):return None,None
  for j,C in enumerate(classes):
   G.add_edge(('b',i),('p',i,j),capacity=1)
   for z in C:G.add_edge(('p',i,j),('z',z),capacity=1)
 v,f=nx.maximum_flow(G,S,T)
 if v<n:return False,None
 word=[]
 for i,(r,B) in enumerate(bs):
  tags=frozenset(z[1] for p,k in f[('b',i)].items() if k for z,h in f[p].items() if h)
  assert len(tags)==r and tags in B;word.extend(B[tags])
 assert len(word)==n and all(len({t[c] for t in word})==n for c in range(3))
 return True,word

def solve(n,T):
 assert planar(n,T)
 R=closure(n,T)
 if R is None:return False,'closure',None
 for a,b in [(0,1),(0,2),(1,2)]:
  B=blocks(n,R,a,b)
  if B is False:return False,'empty_local',None
  if B is None:continue
  ans,w=flow(n,B)
  if ans is not None:return ans,'flow',w
 return None,'unknown',None

S=[(0,0,1),(0,1,1),(0,1,2),(1,0,0),(1,0,2),(1,1,2),(2,2,0),(2,2,1)]
U=[(0,0,0),(0,1,1),(1,0,1),(1,1,2),(2,2,0),(2,2,2)]
F=[(0,0,2),(0,0,3),(1,1,0),(1,1,1),(2,2,1),(2,3,0),(3,2,3),(3,3,2)]
if __name__=='__main__':
 rng=random.Random(20261125);stats={};nchecks=0;planar_reject=0
 for n in range(2,6):
  groups=[list(range(i,min(i+2,n))) for i in range(0,n,2)];pool=[(a,b,c) for g in groups for a in g for b in g for c in range(n)]
  for _ in range(300):
   T=sorted(rng.sample(pool,rng.randint(n,min(len(pool),3*n+2))))
   if not planar(n,T):planar_reject+=1;continue
   ans,method,w=solve(n,T);truth=oracle(n,T)
   assert ans is None or ans==truth;nchecks+=1
   k=f'{method}:{ans}:{truth}';stats[k]=stats.get(k,0)+1
 samples=[]
 for name,n,T in [('S',3,S),('U',3,U),('U_plus',3,U+[(0,0,1)]),('F',4,F),('AGE_U',3,[(0,0,0),(0,0,2),(0,1,0),(0,1,1),(0,2,1),(0,2,2),(1,0,0),(1,0,1),(1,1,1),(2,0,1),(2,0,2),(2,2,1)])]:
  R=closure(n,T);B=blocks(n,R,0,1) if R else None
  ans,method,w=solve(n,T);samples.append(dict(name=name,closure=len(R) if R is not None else None,base_sizes=[len(b) for _,b in B] if B else None,xy_flow=flow(n,B)[0] if B else None,answer=ans,method=method,oracle=oracle(n,T),witness=w))
 scale=[]
 for k in [1,4,16,32]:
  for name,T in [('S',S),('U',U)]:
   ts=[tuple(x+3*i for x in t) for i in range(k) for t in T];a,m,w=solve(3*k,ts);assert a==(name=='S');scale.append(dict(name=name,k=k,triples=len(ts),answer=a,method=m))
 print(json.dumps(dict(seed=20261125,random_controls=nchecks,nonplanar_skips=planar_reject,stats=stats,samples=samples,scale=scale)))
