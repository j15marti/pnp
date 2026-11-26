import itertools as I, json, networkx as nx
from collections import Counter
Q=[t for t in I.product(range(2),repeat=4) if sum(t)==2]
U=[(3,5,0,0),(2,0,4,2),(1,1,2,2),(0,5,1,3),(1,4,2,4),(5,0,4,5),(3,2,5,0),(0,4,2,2),(5,3,4,1),(4,2,0,0),(4,2,5,1),(0,4,1,4),(5,3,3,5),(2,1,3,3),(3,3,5,3),(2,0,3,5),(4,5,0,1),(1,1,1,4)]
V=[(0,0,5,1),(0,1,0,1),(0,1,1,0),(1,0,0,1),(1,0,1,0),(1,1,0,0),(2,2,3,3),(2,3,2,3),(2,4,3,2),(3,2,2,3),(3,2,3,2),(3,3,2,2),(4,3,5,5),(4,5,4,5),(4,5,5,4),(5,4,4,5),(5,4,1,4),(5,5,4,4)]
W=U[:];a,b=list(W[1]),list(W[14]);a[3],b[3]=b[3],a[3];W[1],W[14]=tuple(a),tuple(b)
def setup(T):
 n=len(T)//3;assert len(T)==3*n==len(set(T));R={(c,i):tuple(j for j,t in enumerate(T) if t[c]==i) for c in range(4) for i in range(n)};assert all(len(r)==3 for r in R.values())
 G=nx.Graph((j,e) for e,r in R.items() for j in r);ok,E=nx.check_planarity(G);assert ok;return n,R,G,E
def exact(T,R):
 n=len(T)//3;return [set(s) for s in I.combinations(range(len(T)),n) if all(len(set(s).intersection(r))==1 for r in R.values())]
def opt(T,L,cs,w,c,d,force=None):
 L=set(L);a=set(cs[c]);b=set(cs[d]);z=0
 if force is not None:
  j,v=force;L.remove(j)
  if v:a.remove(T[j][c]);b.remove(T[j][d]);z=w[j]
 G=nx.Graph();G.add_nodes_from((0,i) for i in a);G.add_nodes_from((1,i) for i in b)
 for j in L:
  u,v=(0,T[j][c]),(1,T[j][d])
  if u[1] in a and v[1] in b and (not G.has_edge(u,v) or G[u][v]['weight']<w[j]):G.add_edge(u,v,weight=w[j])
 M=nx.max_weight_matching(G,maxcardinality=True);return z+sum(G[u][v]['weight'] for u,v in M) if len(M)==len(a)==len(b) else -1

def close(T,R,guard,curvature,stats):
 p=dict(guard)
 while True:
  old=len(p)
  for r in R.values():
   z=sum(p.get(j)==1 for j in r);f=[j for j in r if j not in p]
   if z>1 or not z and not f:return None
   if z:p.update((j,0) for j in f)
   elif len(f)==1:p[f[0]]=1
  if len(p)>old:continue
  L=set(range(len(T)))-p.keys()
  if not L:return p
  A={e:tuple(j for j in r if j in L) for e,r in R.items() if any(j in L for j in r)}
  G=nx.Graph((j,e) for e,r in A.items() for j in r)
  for C in nx.connected_components(G):
   B={j for j in C if isinstance(j,int)};rows={e:A[e] for e in C if isinstance(e,tuple)};cs=[{i for c,i in rows if c==d} for d in range(4)]
   if len({len(z) for z in cs})>1:return None
   dup=Counter(tuple(sorted(pair)) for r in rows.values() for pair in I.combinations(r,2));w={j:0 for j in B}
   for (i,j),k in dup.items():
    assert k<=2
    w[i]+=k-1;w[j]+=k-1
   r3=sum(len(r)==3 for r in rows.values());bound=(r3+1)//2+4
   if not curvature:w={j:0 for j in B};bound=0
   for c,d in I.combinations(range(4),2):
    stats['matching_calls']+=1
    if opt(T,B,cs,w,c,d)<bound:return None
    for j in sorted(B):
     for v in (0,1):
      stats['matching_calls']+=1
      if opt(T,B,cs,w,c,d,(j,v))<bound:p[j]=1-v;break
     if len(p)>old:break
    if len(p)>old:break
   if len(p)>old:break
  if len(p)==old:return p

def density(T,R,E,s):
 n=len(T)//3;G=nx.Graph();G.add_nodes_from(range(len(T)));H=nx.MultiGraph();H.add_nodes_from(G)
 for e,r in R.items():
  a=next(j for j in r if j in s)
  for j in r:
   if j!=a:H.add_edge(a,j)
  G.add_edges_from(I.combinations(r,2))
 assert nx.check_planarity(G)[0] and nx.check_planarity(nx.Graph(H))[0] and nx.is_bipartite(H)
 assert H.number_of_edges()==8*n and H.number_of_edges()-nx.Graph(H).number_of_edges()>=2*n+4*nx.number_connected_components(H)
 seen=set();fac=[E.traverse_face(u,v,seen) for u,v in E.edges if (u,v) not in seen];assert sum(len(f)==4 for f in fac)>=3*n+6
 if nx.node_connectivity(nx.Graph((j,e) for e,r in R.items() for j in r))>=3:
  P={tuple(sorted(j for j in f if isinstance(j,int))) for f in fac if len(f)==4};D={tuple(pair) for pair,k in Counter(tuple(sorted(pair)) for r in R.values() for pair in I.combinations(r,2)).items() if k==2};assert P==D

def chain(k,mid=None):
 T=[tuple(x+6*b for x in t) for b in range(k) for t in (mid if mid is not None and b==k//2 else V)]
 for b in range(k-1):
  i,j=b*18,(b+1)*18;c=b%2;p,q=list(T[i]),list(T[j]);p[c],q[c]=q[c],p[c];T[i],T[j]=tuple(p),tuple(q)
 return T

def main():
 out={'fixtures':[],'scale':[]}
 for name,T in [('Q',Q),('U',U),('V',V),('W',W)]:
  n,R,G,E=setup(T);S=exact(T,R);D=Counter(tuple(sorted(pair)) for r in R.values() for pair in I.combinations(r,2));assert max(D.values())<=2
  for s in S:density(T,R,E,s)
  guards=[{}]+[{j:v} for j in range(len(T)) for v in (0,1)]+[{i:a,j:b} for (i,j),k in D.items() if k==2 for a,b in I.product((0,1),repeat=2)]
  z={'name':name,'covers':len(S),'jobs':len(guards),'plain_no':0,'curv_no':0,'extra_no':0,'extra_pin_jobs':0,'extra_pins':0,'matching_calls':0,'cover_branches':0}
  for g in guards:
   sols=[s for s in S if all((j in s)==bool(v) for j,v in g.items())];p=close(T,R,g,False,z);q=close(T,R,g,True,z)
   for a in (p,q):
    if a is None:assert not sols
    else:assert all(all((j in s)==bool(v) for j,v in a.items()) for s in sols)
   z['plain_no']+=p is None;z['curv_no']+=q is None;z['extra_no']+=p is not None and q is None
   if p is not None and q is not None:z['extra_pin_jobs']+=len(q)>len(p);z['extra_pins']+=max(0,len(q)-len(p))
  B=nx.Graph();B.add_edges_from(pair for pair,k in D.items() if k==2);K=set(j for e in nx.maximal_matching(B) for j in e)
  # Enumerate distinct patterns only for small reference controls. Closure-only terminal after hitting all repeated pairs.
  for bits in I.product((0,1),repeat=len(K)):
   p=dict(zip(sorted(K),bits));t=close(T,R,p,True,z);sols=[s for s in S if all((j in s)==bool(v) for j,v in p.items())];assert (t is not None)==bool(sols)
   if t is not None:assert len(t)==len(T) and {j for j in t if t[j]} in sols
   z['cover_branches']+=1
  out['fixtures'].append(z)
 for k in (2,4,8,16,32):
  T=chain(k);n,R,G,E=setup(T);s0=exact(V,setup(V)[1])[0];s={18*b+j for b in range(k) for j in s0};assert all(len(s.intersection(r))==1 for r in R.values());H=nx.MultiGraph();H.add_nodes_from(range(len(T)))
  for r in R.values():
   a=next(j for j in r if j in s);H.add_edges_from((a,j) for j in r if j!=a)
  excess=H.number_of_edges()-nx.Graph(H).number_of_edges();assert nx.is_connected(H) and nx.check_planarity(nx.Graph(H))[0] and excess>=2*n+4
  N=chain(k,U);setup(N) # NO by the one-color swap conservation proof, not brute force.
  out['scale'].append({'tuples':len(T),'active_repeat_edges':excess,'threshold':2*n+4,'neighbor_no_by_seam':True})
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
