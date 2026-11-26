import networkx as nx,itertools as it,random,collections

def oct_chain(n):
 T=set(it.product(range(2),repeat=3)); W={(0,0,0),(1,1,1)}
 for k in range(2,n):
  f=min(T-W); T.remove(f);T.update(t for t in it.product(*[(f[i],k) for i in range(3)]) if t!=f);W.add((k,k,k))
 return T

def incidence(T,n):
 G=nx.Graph(); G.add_nodes_from((i,v) for i in range(3) for v in range(n))
 for t in T:G.add_edges_from((('t',t),(i,v)) for i,v in enumerate(t))
 return G

def oracle(T,n):
 by=[[t for t in T if t[0]==i] for i in range(n)]
 def rec(i,Y,Z):
  if i==n:return []
  for t in by[i]:
   x,y,z=t
   if y not in Y and z not in Z:
    a=rec(i+1,Y|{y},Z|{z})
    if a is not None:return [t]+a
  return None
 return rec(0,set(),set())

def closure(T,n):
 T=set(T);P=set();V={(i,v) for i in range(3) for v in range(n)}
 while True:
  D={v:{t for t in T if t[v[0]]==v[1]} for v in V}
  if any(not s for s in D.values()):return None,None
  one=next((next(iter(s)) for s in D.values() if len(s)==1),None)
  if one is not None:
   P.add(one);V-={(i,x) for i,x in enumerate(one)};T={t for t in T if not any(a==b for a,b in zip(t,one))};continue
  bad=set()
  for i,j in [(0,1),(0,2),(1,2)]:
   A={v for v in V if v[0]==i};B={v for v in V if v[0]==j};G=nx.Graph();G.add_nodes_from(A|B);G.add_edges_from(((i,t[i]),(j,t[j])) for t in T)
   M=nx.algorithms.bipartite.maximum_matching(G,top_nodes=A)
   if len(M)!=len(A|B):return None,None
   H=nx.DiGraph();H.add_nodes_from(G);H.add_edges_from((b,a) if M[a]==b else (a,b) for a in A for b in G[a]);C={v:k for k,c in enumerate(nx.strongly_connected_components(H)) for v in c}
   bad|={t for t in T if M[(i,t[i])]!=(j,t[j]) and C[(i,t[i])]!=C[(j,t[j])]}
  if not bad:return T,P
  T-=bad

def formula(T):
 ts=sorted(T);D=collections.defaultdict(list)
 for k,t in enumerate(ts):
  for i,v in enumerate(t):D[i,v].append(k)
 cs=[]
 for s in D.values():
  for i,j in it.combinations(s,2):cs.append(((i,0),(j,0)))
  if len(s)==2:cs.append(((s[0],1),(s[1],1)))
 G=nx.DiGraph();G.add_nodes_from((k,b) for k in range(len(ts)) for b in (0,1))
 for (i,a),(j,b) in cs:G.add_edge((i,1-a),(j,b));G.add_edge((j,1-b),(i,a))
 return ts,D,cs,G
