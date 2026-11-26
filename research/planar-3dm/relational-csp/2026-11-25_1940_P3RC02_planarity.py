import itertools,networkx as nx
Q=[p for p in itertools.product(range(2),repeat=3) if sum(p) not in (0,3)]
count=0
for k in [3,4,5,8,9,16,17,32,33,64,65]:
 for relax in [0,1]:
  cs=[i%2 for i in range(k)];cs[-1]=2 if k%2 else 1;T=[]
  for i in range(k):
   a,b=cs[i-1],cs[i];perm=[a,b,3-a-b]
   for t in Q:
    u=[0]*3
    for j,c in enumerate(perm):u[c]=2*i+t[j]
    T.append(u)
  for i,c in enumerate(cs):
   j=(i+1)%k;u,v=6*i+3,6*j;T[u][c],T[v][c]=T[v][c],T[u][c]
  T=[t for i,t in enumerate(T) if i%6!=1 or (relax and i==1)]
  G=nx.Graph();G.add_nodes_from(('e',c,v) for c in range(3) for v in range(2*k));G.add_edges_from((('t',i),('e',c,v)) for i,t in enumerate(T) for c,v in enumerate(t));assert nx.check_planarity(G)[0] and nx.is_connected(G) and len(set(map(tuple,T)))==len(T) and set(dict(G.degree()).values())=={2,3};count+=1
print(nx.__version__,count,'planar connected distinct degree-2/3 controls')
T=[list(v+2*i for v in t) for i in range(2) for t in Q]
for j in [0,1]: T[j][0],T[6+j][0]=T[6+j][0],T[j][0]
g=nx.Graph();g.add_edges_from((('t',i),('e',c,v)) for i,t in enumerate(T) for c,v in enumerate(t));assert nx.check_planarity(g)[0] and nx.is_connected(g)
mask=set()
for out0,out1,in0,in1 in itertools.product(range(2),repeat=4):
 for s in itertools.product(range(2),repeat=6):
  if s[:2]!=(out0,out1):continue
  counts={(c,v):0 for c in range(3) for v in range(2)}
  for i in range(6):
   if s[i]:
    for c,v in enumerate(T[i]):
     if v<2:counts[c,v]+=1
  counts[0,0]+=in0+in1
  if all(v==1 for v in counts.values()):mask.add((out0,out1,in0,in1));break
print(sorted(mask))
assert mask=={(0,0,0,0),(0,1,0,1),(0,1,1,0),(1,0,0,1),(1,0,1,0)}
