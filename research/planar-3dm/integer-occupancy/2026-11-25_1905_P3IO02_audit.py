from itertools import product, combinations
from collections import Counter
import json, random, networkx as nx
Q=[p for p in product(range(2),repeat=3) if p not in [(0,0,0),(1,1,1)]]
U=[tuple(map(int,w)) for w in '000 002 010 011 021 022 100 101 111 201 202 221'.split()]
V=U+[(1,1,0)]
# Fractional certificate uses numerator over 4; integer witness uses 0/1.
uf=[0,0,2,0,0,2,2,0,2,0,2,2]
def covers(T,n):
 return [p for p in combinations(range(len(T)),n) if all(len({T[i][c] for i in p})==n for c in range(3))]
def validate(T,n):
 assert len(set(T))==len(T) and all(len(t)==3 and all(0<=v<n for v in t) for t in T)
 G=nx.Graph();G.add_nodes_from((c,j) for c in range(3) for j in range(n));G.add_edges_from((('t',i),(c,v)) for i,t in enumerate(T) for c,v in enumerate(t))
 assert nx.is_connected(G) and nx.check_planarity(G)[0]
 return G
# Each original incidence becomes a chain of L copies of Q minus the X0--001 edge, permuted by color.
def expand(T,n,L,weights,den=4):
 W=[list(t) for t in T]; x=list(weights); blocks=[]; terminals={}; ports=[]
 for i,t in enumerate(T):
  for c,v in enumerate(t):
   r=i;q=weights[i]
   for j in range(L):
    perm=[c]+[k for k in range(3) if k!=c];ids={}
    W[r][c]=n
    for p in Q:
     a=[None]*3
     for k in range(3):a[perm[k]]=n+p[k]
     ids[p]=len(W);W.append(a)
     x.append(q if p in [(0,0,1),(1,1,0)] else (den-q)//2)
    assert (den-q)%2==0
    blocks.append([r]+list(ids.values()));r=ids[(0,0,1)];ports.append(r);n+=2
   W[r][c]=v;terminals.setdefault((c,v),[]).append(r)
 W=list(map(tuple,W));blocks+=list(terminals.values());return W,n,x,blocks
# Actual integer lift, with deterministic selection of one of the two q=0 orientations.
def lift(T,n,L,w):
 W=[list(t) for t in T];s=set(w)
 for i,t in enumerate(T):
  for c,v in enumerate(t):
   r=i
   for j in range(L):
    perm=[c]+[k for k in range(3) if k!=c];ids={};W[r][c]=n
    for p in Q:
     a=[None]*3
     for k in range(3):a[perm[k]]=n+p[k]
     ids[p]=len(W);W.append(a)
     if p in ([(0,0,1),(1,1,0)] if i in w else [(0,1,0),(1,0,1)]):s.add(ids[p])
    r=ids[(0,0,1)];n+=2
   W[r][c]=v
 return list(map(tuple,W)),n,s
def occupancy(T,n,x,den):
 a=Counter((c,v) for i,t in enumerate(T) for c,v in enumerate(t) for _ in range(x[i]));assert all(a[c,v]==den for c in range(3) for v in range(n))
def conflict(G):
 H=nx.Graph();H.add_nodes_from(i for c,i in G if c=='t');H.add_edges_from((a[1],b[1]) for e in G if e[0]!='t' for a,b in combinations(G[e],2));return H
# Paid exact-one, affine forced-bit, and per-index projection support checks. These controls stagnate at root.
def closure_probe(T,n,G):
 m=len(T);rows=[sum(1<<i for _,i in G[e]) for e in G if e[0]!='t'];assert min(map(int.bit_count,rows))>=2
 basis={}
 for a in rows:
  while a:
   p=a.bit_length()-1
   if p not in basis:basis[p]=a;break
   a^=basis[p]
 def reduce(a):
  while a:
   p=a.bit_length()-1
   if p not in basis:return a
   a^=basis[p]
  return a
 # Consistency separately on augmented rows.
 b={}
 for a in rows:
  a|=1<<m
  while a & ((1<<m)-1):
   p=(a&((1<<m)-1)).bit_length()-1
   if p not in b:b[p]=a;break
   a^=b[p]
  else:assert a==0
 assert all(reduce(1<<i) for i in range(m))
 calls=0
 for c,d in combinations(range(3),2):
  L={(c,j) for j in range(n)};R={(d,j) for j in range(n)};P=nx.Graph();P.add_nodes_from(L|R);P.add_edges_from(((c,t[c]),(d,t[d])) for t in T)
  def perfect(H,left):
   nonlocal calls;calls+=1;return len(nx.algorithms.bipartite.maximum_matching(H,top_nodes=left))==2*len(left)
  assert perfect(P,L)
  for i,t in enumerate(T):
   a=(c,t[c]);z=(d,t[d]);H=P.copy();H.remove_nodes_from([a,z]);assert perfect(H,L-{a})
 return calls
# Exact shortest odd closed walk separation using parity double cover, integer lengths.
def odd_min(H,x,den,h=None):
 W=H if h is None else H.subgraph(list(H[h]));q=0 if h is None else x[h];D=nx.Graph();D.add_nodes_from((v,p) for v in W for p in (0,1))
 for a,b in W.edges:
  w=den-x[a]-x[b]-q;assert w>=0
  D.add_edge((a,0),(b,1),weight=w);D.add_edge((a,1),(b,0),weight=w)
 best=None
 for v in W:
  z=nx.single_source_dijkstra_path_length(D,(v,0)).get((v,1))
  if z is not None:best=z if best is None else min(best,z)
 return best
# Verify every clique with NetworkX enumerator (audit only), all odd cycles and simple odd wheels by exact separation.
def cuts(G,x,den):
 H=conflict(G);cl=list(nx.find_cliques(H));assert all(sum(x[i] for i in C)<=den for C in cl)
 z=odd_min(H,x,den);assert z is None or z>=den
 for h in H:
  w=odd_min(H,x,den,h);assert w is None or w>=den-x[h]
 return len(cl),z
# Independent local-block consistency: each small random vertex subset has a forest of shared interfaces.
def local_audit(blocks,m,L):
 rng=random.Random(1905);count=0
 for k in [1,2,3,4,5,6]:
  if k>=L:continue
  for _ in range(20):
   S=set(rng.sample(range(m),k));B=nx.Graph()
   for j,C in enumerate(blocks):B.add_edges_from((('b',j),('v',v)) for v in set(C)&S)
   assert nx.is_forest(B);count+=1
 return count
assert covers(U,3)==[];vw=covers(V,3);assert vw
occupancy(U,3,uf,4);vf=[4*int(i in vw[0]) for i in range(len(V))]
# Q relay truth table: append external bit at removed element and check exact integer occupancies on internal elements.
qstates=[]
for r in (0,1):
 for s in product((0,1),repeat=6):
  if all(sum(s[i] for i,t in enumerate(Q) if t[c]==v and not (c==0 and t==(0,0,1)))+(r if (c,v)==(0,0) else 0)==1 for c in range(3) for v in range(2)):
   assert s[Q.index((0,0,1))]==r;qstates.append([r,list(s)])
assert len(qstates)==3
out=[]
for name,T,f in [('U',U,uf),('V',V,vf)]:
 G=validate(T,3);initial=closure_probe(T,3,G)
 for L in (1,2):
  W,n,x,B=expand(T,3,L,f);G=validate(W,n);occupancy(W,n,x,4);nc,z=cuts(G,x,4);calls=closure_probe(W,n,G);again=closure_probe(W,n,G)
  if name=='V':
   WW,nn,s=lift(T,3,L,vw[0]);assert (WW,nn)==(W,n);occupancy(W,n,[int(i in s) for i in range(len(W))],1)
  out.append(dict(source=name,L=L,n=n,m=len(W),cliques=nc,min_odd=z,matching_calls=calls+again,initial_matching_calls=initial,local_tests=local_audit(B,len(W),L),reference='NO by relay theorem' if name=='U' else 'YES verified lift'))
print(json.dumps(dict(networkx=nx.__version__,base_U=U,base_V=V,base_U_fraction_numerator=uf,base_V_witness=list(vw[0]),base_V_count=len(vw),relay_states=qstates,results=out),sort_keys=True))
