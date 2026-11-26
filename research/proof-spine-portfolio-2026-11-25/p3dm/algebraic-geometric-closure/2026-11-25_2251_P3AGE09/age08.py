import itertools as I, networkx as nx

def graph(T,n):
 G=nx.Graph();G.add_nodes_from((c,i) for c in range(3) for i in range(n));G.add_edges_from((('t',j),(c,v)) for j,t in enumerate(T) for c,v in enumerate(t));return G

def solve_ref(T,n):
 return next((list(p) for p in I.combinations(range(len(T)),n) if all(len({T[j][c] for j in p})==n for c in range(3))),None)

def close(T,n):
 S=set(range(len(T)));owners=[(c,i) for c in range(3) for i in range(n)]
 while True:
  old=S.copy()
  for c,i in owners:
   L=[j for j in S if T[j][c]==i]
   if not L:return None
   if len(L)==1:
    j=L[0];S={k for k in S if k==j or all(T[k][d]!=T[j][d] for d in range(3))}
  for c,d in I.combinations(range(3),2):
   X=[(c,i) for i in range(n)];Y=[(d,i) for i in range(n)]
   for j in list(S):
    G=nx.Graph();A=[v for v in X if v[1]!=T[j][c]];B=[v for v in Y if v[1]!=T[j][d]];G.add_nodes_from(A+B);G.add_edges_from(((c,T[k][c]),(d,T[k][d])) for k in S if T[k][c]!=T[j][c] and T[k][d]!=T[j][d]);
    if len(nx.bipartite.maximum_matching(G,top_nodes=A))!=2*(n-1):S.remove(j)
  if S==old:return sorted(S)

def chart(T,n,c,d):
 z=3-c-d;G=graph(T,n);G.remove_nodes_from([(z,i) for i in range(n)])
 X=[(c,i) for i in range(n)];H=nx.Graph();H.add_nodes_from(X+[(d,i) for i in range(n)]);H.add_edges_from(((c,t[c]),(d,t[d])) for t in T)
 M=nx.bipartite.maximum_matching(H,top_nodes=X);assert len(M)==2*n
 base=set(next(j for j,t in enumerate(T) if (c,t[c])==a and (d,t[d])==M[a]) for a in X)
 ok,emb=nx.check_planarity(G);assert ok
 faces={};F=0;seen=set();roots=[]
 for C in nx.connected_components(G):
  roots.append(F)
  for a in C:
   for b in emb.neighbors_cw_order(a):
    if (a,b) in seen:continue
    w=emb.traverse_face(a,b,seen)
    for u,v in zip(w,w[1:]+w[:1]):faces[u,v]=F
    F+=1
 edge=[];D=nx.DiGraph();D.add_nodes_from(range(F))
 for j,t in enumerate(T):
  a=(c,t[c]);b=('t',j);v=(d,t[d]);l,r=faces[a,b],faces[b,a];assert faces[b,v]==l and faces[v,b]==r
  m=int(j in base);edge.append((l,r,m))
  for u,w,k in [(r,l,1-m),(l,r,m)]:
   if not D.has_edge(u,w) or D[u][w]['weight']>k:D.add_edge(u,w,weight=k)
 ds=dict(nx.all_pairs_dijkstra_path_length(D));lo={};hi={}
 for root in roots:
  for f in ds[root]:lo[f]=-ds[f][root];hi[f]=ds[root][f]
 ids={}
 for f in range(F):
  for t in range(lo[f]+1,hi[f]+1):ids[f,t]=len(ids)
 def neg(a):return (-3-a) if a<0 else a^1
 def bit(f,t):return -1 if t<=lo[f] else -2 if t>hi[f] else 2*ids[f,t]
 def clause(a,b):
  if -1 in (a,b):return []
  if a==-2 and b==-2:return [(-2,-2)]
  if a==-2:a=b
  if b==-2:b=a
  if a==neg(b):return []
  return [(a,b)]
 def diff(u,v,k):return [p for t in range(lo[u],hi[u]+1) for p in clause(neg(bit(u,t)),bit(v,t-k))]
 B=[]
 for (f,t),i in ids.items():B+=clause(neg(bit(f,t)),bit(f,t-1))
 P=[]
 for l,r,m in edge:
  B+=diff(l,r,1-m)+diff(r,l,m)
  P.append([diff(l,r,-m)+diff(r,l,m),diff(l,r,1-m)+diff(r,l,m-1)])
 L=[[] for _ in range(n)]
 for j,t in enumerate(T):L[t[z]].append(j)
 return len(ids),B,P,L,edge,lo,ids

def hull(B,k):
 q=2*k;full=(1<<q)-1;r=[1<<i for i in range(q)]
 for a,b in B:
  if a==-2:return None
  r[a^1]|=1<<b;r[b^1]|=1<<a
 for j in range(q):
  b=1<<j;w=r[j]
  for i in range(q):
   if r[i]&b:r[i]|=w
 if any((r[i]>>(i^1)&1) and (r[i^1]>>i&1) for i in range(0,q,2)):return None
 forced=sum(1<<(i^1) for i in range(q) if r[i]>>(i^1)&1)
 return tuple(full if r[i]>>(i^1)&1 else r[i]|forced for i in range(q))

def clauses(R):return [(i^1,j) for i,r in enumerate(R) for j in range(len(R)) if (r>>j)&1 and i!=j]
def model(B,k):
 B=list(B);out=[]
 for i in range(k):
  a=2*i;v=hull(B+[(a,a)],k) is not None;out.append(int(v));a^=int(not v);B.append((a,a))
 return out
U=[tuple(map(int,t)) for t in '000 002 010 011 021 022 100 101 111 201 202 221'.split()]
V=U+[(1,1,0)]
B0=[tuple(map(int,t)) for t in '000 002 012 111 121 202 210 222'.split()]
def ring(k):
 T=[tuple(3*i+v for v in t) for i in range(k) for t in B0]
 for i in range(k-1):
  a=8*i+2;b=8*(i+1)+5;x=list(T[a]);y=list(T[b]);x[1],y[1]=y[1],x[1];T[a]=tuple(x);T[b]=tuple(y)
 return T
