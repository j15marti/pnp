import itertools as it, math, random, json
from fractions import Fraction as F
import networkx as nx
from collections import Counter
ST=Counter()
def add(g,u,v,w):
 if u!=v:g.add_edge(u,v,w=g.get_edge_data(u,v,{}).get('w',0)+w)
def energy(g,x):return sum(d['w']*x[u]*x[v] for u,v,d in g.edges(data=True))
def words(B):
 B=tuple(B)
 return [()] if not B else [(1,)+z for z in it.product((-1,1),repeat=len(B)-1)]
def planar_min(g):
 ST['dual_calls']+=1; x={}
 for C in nx.connected_components(g):
  h=g.subgraph(C);root=min(C)
  if len(C)==1:x[root]=1;continue
  ok,e=nx.check_planarity(h);assert ok
  seen=set();face={};nf=0
  for u,v in e.edges():
   if (u,v) not in seen:
    p=e.traverse_face(u,v,seen)
    for a,b in zip(p,p[1:]+p[:1]):face[a,b]=nf
    nf+=1
  d=nx.Graph();d.add_nodes_from(range(nf));odd=set();pref={}
  for u,v,w in h.edges(data='w'):
   uv=tuple(sorted((u,v)));pref[uv]=-1 if w>0 else 1
   a,b=face[u,v],face[v,u]
   if a==b:continue
   if w>0:odd.symmetric_difference_update({a,b})
   if not d.has_edge(a,b) or abs(w)<d[a][b]['weight']:d.add_edge(a,b,weight=abs(w),uv=uv)
  K=nx.Graph();K.add_nodes_from(odd);paths={}
  for a in sorted(odd):
   ds,ps=nx.single_source_dijkstra(d,a)
   for b in sorted(odd):
    if a<b:K.add_edge(a,b,weight=ds[b]);paths[a,b]=ps[b]
  den=math.lcm(*(F(d["weight"]).denominator for _,_,d in K.edges(data=True)));
  for _,_,kd in K.edges(data=True):kd["weight"]=int(F(kd["weight"])*den)
  chosen=set();M=nx.min_weight_matching(K);assert len(M)*2==len(odd)
  for a,b in M:
   p=paths[tuple(sorted((a,b)))];chosen.symmetric_difference_update(d[i][j]['uv'] for i,j in zip(p,p[1:]))
  x[root]=1
  for u,v in nx.bfs_edges(h,root):
   uv=tuple(sorted((u,v)));x[v]=x[u]*pref[uv]*(-1 if uv in chosen else 1)
  assert all(x[u]*x[v]==pref[tuple(sorted((u,v)))]*(-1 if tuple(sorted((u,v))) in chosen else 1) for u,v in h.edges())
 return energy(g,x),x

def leaf(g,B,planar):
 out={}
 for w in words(B):
  if planar:
   h=g.copy();L=1+sum(abs(d['w']) for _,_,d in g.edges(data=True))
   for i in range(1,len(B)):add(h,B[0],B[i],-L*w[i])
   _,x=planar_min(h)
   if B and x[B[0]]<0:x={u:-v for u,v in x.items()}
   assert tuple(x[u] for u in B)==w
   out[w]=(energy(g,x),x)
  else:
   D=dict(zip(B,w));V=sorted(set(g)-set(B));best=None
   for vals in it.product((-1,1),repeat=len(V)):
    x=D|dict(zip(V,vals));z=energy(g,x)
    if best is None or z<best[0]:best=z,x
   out[w]=best
 return out

def separator(g,B,apex):
 # Find apex-containing cuts first, then ordinary cuts. General enumeration is polynomial.
 V=sorted(g)
 if apex in g:
  W=g.copy();W.remove_node(apex)
  if not nx.is_connected(W):return (apex,)
  for a in nx.articulation_points(W):return tuple(sorted((apex,a)))
  for a in W:
   H=W.copy();H.remove_node(a)
   for b in nx.articulation_points(H):return tuple(sorted((apex,a,b)))
 for k in range(1,4):
  for S in it.combinations(V,k):
   if apex in S:continue
   H=g.subgraph(set(g)-set(S))
   if len(H)>1 and not nx.is_connected(H):return S
 return None

def solve(g,B=(),apex=-1,cap=9):
 ST['nodes']+=1;assert all(g.has_edge(u,v) for u,v in it.combinations(B,2))
 p=nx.check_planarity(g)[0]
 if p or len(g)<=cap:
  ST['planar_leaves' if p else 'small_leaves']+=1;ST['max_small']=max(ST['max_small'],0 if p else len(g))
  return leaf(g,B,p)
 S=separator(g,B,apex)
 if S is None:return None
 C=next(C for C in nx.connected_components(g.subgraph(set(g)-set(S))) if not (C&set(B)))
 h=g.subgraph(C|set(S)).copy();r=g.subgraph(set(g)-C).copy()
 for u,v in it.combinations(S,2):
  h.add_edge(u,v,w=0);add(r,u,v,0)
 a=solve(h,S,apex,cap)
 if a is None:return None
 # Flip-invariant table on at most three ports: constant plus pair products.
 vals={w:a[w][0] for w in a};q=len(vals);c=sum(vals.values())/F(q)
 for i,j in it.combinations(range(len(S)),2):add(r,S[i],S[j],sum(z*w[i]*w[j] for w,z in vals.items())/F(q))
 b=solve(r,B,apex,cap)
 if b is None:return None
 out={}
 for w,(z,x) in b.items():
  s=x[S[0]];key=tuple(s*x[u] for u in S);y={u:s*v for u,v in a[key][1].items()};assert all(x[u]==y[u] for u in S)
  X=x|y;assert energy(g,X)==z+c;out[w]=(z+c,X)
 return out

def source(T,n,cap=9):
 I=nx.Graph();I.add_nodes_from(range(3*n+len(T)))
 R=[[] for _ in range(3*n)]
 for i,t in enumerate(T):
  for c,v in enumerate(t):R[c*n+v].append(i);I.add_edge(c*n+v,3*n+i)
 assert len(set(T))==len(T) and nx.check_planarity(I)[0] and all(2<=len(r)<=3 for r in R)
 # paid pair support (one perfect matching and SCC per lane)
 for a,b in it.combinations(range(3),2):
  P=nx.Graph();L=[(0,i) for i in range(n)];Q=[(1,i) for i in range(n)];P.add_nodes_from(L+Q);P.add_edges_from(((0,t[a]),(1,t[b])) for t in T)
  M=nx.algorithms.bipartite.maximum_matching(P,top_nodes=L);assert len(M)==2*n
  D=nx.DiGraph();D.add_nodes_from(range(n));D.add_edges_from((t[a],M[1,t[b]][1]) for t in T)
  ss={v:i for i,S in enumerate(nx.strongly_connected_components(D)) for v in S}
  assert all(ss[t[a]]==ss[M[1,t[b]][1]] for t in T)
 # phase contraction
 H=nx.Graph();H.add_nodes_from(range(len(T)));H.add_edges_from(r for r in R if len(r)==2)
 if not nx.is_bipartite(H):return None
 ids={};sg={}
 for j,C in enumerate(nx.connected_components(H)):
  for i,b in nx.bipartite.color(H.subgraph(C)).items():ids[i]=j;sg[i]=1-2*b
 g=nx.Graph();g.add_nodes_from(set(ids.values())|{-1});const=0
 for r in R:
  if len(r)==2:continue
  const+=4
  for i in r:add(g,-1,ids[i],2*sg[i])
  for i,j in it.combinations(r,2):
   if ids[i]==ids[j]:const+=2*sg[i]*sg[j]
   else:add(g,ids[i],ids[j],2*sg[i]*sg[j])
 g.remove_edges_from([(u,v) for u,v,w in g.edges(data='w') if not w])
 assert nx.check_planarity(g.subgraph(set(g)-{-1}))[0]
 ans=solve(g,cap=cap)
 if ans is None:return None
 z,x=ans[()];selected=[t for i,t in enumerate(T) if sg[i]*x[ids[i]]*x[-1]==1];occ=[sum(t[c]==v for t in selected) for c in range(3) for v in range(n)]
 assert sum(4*(u-1)**2 for u in occ)==z+const
 if z+const==0:assert len(selected)==n and set(occ)=={1}
 return int(z+const)

def chain(b):
 base=[t for t in it.product(range(2),repeat=3) if t not in [(0,0,0),(1,1,1)]]
 T=[tuple(x+2*i for x in t) for i in range(b) for t in base]
 for i in range(b-1):
  u=tuple(x+2*i for x in (0,0,1));v=tuple(x+2*(i+1) for x in (0,1,0))
  T.remove(u);T.remove(v);T.extend([(v[0],u[1],u[2]),(u[0],v[1],v[2])])
 return T

if __name__=='__main__':
 rng=random.Random(4404);checks=0
 for k in range(100):
  g=nx.grid_2d_graph(3,3);g=nx.convert_node_labels_to_integers(g)
  for u,v in list(g.edges()):
   if rng.random()<.2:g.remove_edge(u,v)
   else:g[u][v]['w']=rng.randrange(-7,8)
  z,x=planar_min(g);assert z==min(energy(g,dict(zip(g,w))) for w in it.product((-1,1),repeat=len(g)));checks+=1
 # General nonplanar pieces (K5) attached on 3-cliques, test exact all boundary modes.
 for k in range(60):
  g=nx.Graph();g.add_edges_from(it.combinations(range(5),2));g.add_edges_from(it.combinations((0,1,2,5,6),2));g.add_edges_from(it.combinations((2,5,6,7,8),2))
  for u,v in g.edges():g[u][v]['w']=rng.randrange(-9,10)
  B=(0,1,2);a=solve(g,B,cap=5);b=leaf(g,B,False);assert a is not None and {w:z for w,(z,x) in a.items()}=={w:z for w,(z,x) in b.items()};checks+=4
 chain_results=[]
 for b in (1,2,4,8,16,32,64):
  T=chain(b);before=ST.copy();z=source(T,2*b);assert z==0;chain_results.append(dict(blocks=b,triples=len(T),minimum=z,counters=dict(ST-before)))
 # Both-label small actual sources; U max degree 5 so use only degree-2/3 examples.
 # Search restricted controls with known exact brute-force labels and stable pair support.
 sources=Counter()
 for k in range(2500):
  n=rng.choice([2,3,4]);T=rng.sample(list(it.product(range(n),repeat=3)),rng.randint(2*n,min(3*n,n**3)))
  if not all(2<=sum(t[c]==v for t in T)<=3 for c in range(3) for v in range(n)):continue
  I=nx.Graph();I.add_edges_from(((c,t[c]),('t',i)) for i,t in enumerate(T) for c in range(3))
  if not nx.check_planarity(I)[0]:continue
  try:z=source(T,n)
  except AssertionError as e:
   # Explicit filter for failed pair support, not a swallowed solver disagreement.
   # Check it independently before skipping.
   supported=True
   for c,d in it.combinations(range(3),2):
    pool=[S for S in it.combinations(T,n) if len({t[c] for t in S})==n and len({t[d] for t in S})==n]
    if set().union(*map(set,pool))!=set(T):supported=False
   if supported:raise
   sources['pair_prune_required']+=1;continue
  if z is None:sources['declined_or_phase_inconsistent']+=1;continue
  sat=any(all(len({t[c] for t in S})==n for c in range(3)) for S in it.combinations(T,n));assert (z==0)==sat;sources['SAT' if sat else 'UNSAT']+=1
 # Guard graft is RC01's exact zero pin; all source degrees remain three.
 guard_results=[]
 for b in (1,2,4,8,16):
  for h in (2,3):
   T=chain(b);n=2*b
   for t in [u for u in T if u[0]==0][:h]:
    a,c,d=t;T=[u for u in T if u!=t]+[(n,n,n),(a,n,n),(n,c,n),(n,n,d)];n+=1
   z=source(T,n,cap=16);assert z is not None and (z==0)==(h==2)
   guard_results.append(dict(blocks=b,pins=h,triples=len(T),minimum=z))
 # Fourth-order obstruction and exact sibling cancellation.
 B=(0,1,2,3);modes=words(B)
 f=lambda w:-abs(sum(w));g=lambda w:-abs(-w[0]+sum(w[1:]))
 q=lambda fn:sum(fn(w)*math.prod(w) for w in modes)/F(len(modes))
 assert q(f)==F(1,2) and q(g)==-F(1,2)
 H={w:f(w)+g(w) for w in modes};const=sum(H.values())/F(8)
 J={(i,j):sum(z*w[i]*w[j] for w,z in H.items())/F(8) for i,j in it.combinations(range(4),2)}
 assert all(H[w]==const+sum(z*w[i]*w[j] for (i,j),z in J.items()) for w in modes)
 print(json.dumps(dict(seed=4404,abstract_checks=checks,chain=chain_results,source=dict(sources),guard_neighbors=guard_results,quartic=[str(q(f)),str(q(g)),str(q(lambda w:H[w]))],total=dict(ST)),indent=2))
