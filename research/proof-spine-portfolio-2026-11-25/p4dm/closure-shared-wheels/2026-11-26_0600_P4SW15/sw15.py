"""Construct word-specific native planar P4DM caps for every conservation-legal cyclic boundary.
Requires the archived SW13 catalog and helpers. No SAT oracle; fixed four-port local witnesses.
"""
from glue_audit import *
import random, time
CAT=[decode(a) for a in json.load(open('catalog_results.json'))['caps']]

def cap4(t,w):
 B,o,c=getcap(t,w,CAT)
 U,Z,P,ww,ss=B
 # validate exact matching of physical ports
 assert all(typ(P)[o[i]][1]==-t[i][1] and c[typ(P)[o[i]][0]]==t[i][0] and ww[o[i]]==w[i] for i in range(4))
 return B,o,c

def make_cap(t,w):
 k=len(t);assert len(w)==k and all(x in (0,1) for x in w)
 d=[sum(s for c,s in t if c==j) for j in range(4)]
 b=[sum(s*x for (c,s),x in zip(t,w) if c==j) for j in range(4)]
 assert len({z%3 for z in d})==1 and len({d[j]-3*b[j] for j in range(4)})==1
 out=[[sum(c==j and s==1 and x==v for (c,s),x in zip(t,w)) for v in (0,1)] for j in range(4)]
 inc=[sum(c==j and s==-1 for c,s in t) for j in range(4)]
 n=d[0]%3
 while True:
  r=[(n-z)//3 for z in d];a=r[0]+b[0]
  if min(r)>=0 and all(r[j]>=inc[j] and a>=out[j][1] and n-a>=out[j][0] for j in range(4)) and 0<=a<=n:break
  n+=3
 assert n<=6*k+6
 G=nx.Graph();val={};sgn={};color={};stubs=co.defaultdict(list);N=0
 def node(s,c=None,v=None):
  nonlocal N
  u=N;N+=1;G.add_node(u);sgn[u]=s;color[u]=c
  if v is not None:val[u]=v
  return u
 dummy=[node(-s,c,x) for (c,s),x in zip(t,w)]
 T=[node(1,v=int(i<a)) for i in range(n)]
 R=[[node(-1,j) for _ in range(r[j])] for j in range(4)]
 # each abstract edge represented by two unique lanes with identical color and bit
 lane=[];mate={}
 def edge(u,v,c,x):
  assert sgn[u]==-sgn[v];i=len(lane);lane.extend([(u,c,x),(v,c,x)]);mate[i]=i+1;mate[i+1]=i;stubs[u].append(i);stubs[v].append(i+1)
 for c in range(4):
  tt={x:[u for u in T if val[u]==x] for x in (0,1)}
  rr={0:[u for u in R[c] for _ in range(2)],1:R[c][:]};ri=iter(R[c])
  for i,((j,s),x) in enumerate(zip(t,w)):
   if j!=c:continue
   if s==1:u=tt[x].pop();edge(u,dummy[i],c,x)
   else:u=next(ri);rr[x].remove(u);edge(dummy[i],u,c,x)
  for x in (0,1):
   assert len(tt[x])==len(rr[x]);
   for u,v in zip(tt[x],rr[x]):edge(u,v,c,x)
 # top boundary vertices, all non-dummy vertices have slots on same horizontal line
 order=[i for u in range(N) for i in stubs[u]];target=[];seen=set()
 for i in order:
  if i not in seen:target.extend([i,mate[i]]);seen.update([i,mate[i]])
 current={i:u for i,(u,c,x) in enumerate(lane)};cross=0;capnodes=0
 def connect(u,v):
  assert sgn[u]==-sgn[v] and not G.has_edge(u,v),(u,v);G.add_edge(u,v)
 def swap(i,j):
  nonlocal cross,capnodes
  u,c,x=lane[i];v,e,y=lane[j];typ0=((c,sgn[u]),(e,sgn[v]),(c,-sgn[u]),(e,-sgn[v]));w0=(x,y,x,y)
  B,o,cm=cap4(typ0,w0);U,Z,P,ww,ss=B
  zmap={a:node(1,v=int(a[1] in ss)) if a[0]=='t' else node(-1,cm[a[1]]) for a in sorted(Z)}
  missing={frozenset((a,b)) for a,b in P};
  for a in Z:
   if a[0]!='t':continue
   for c0,r0 in enumerate(U[a[1]]):
    b0=('e',c0,r0)
    if b0 in Z and frozenset((a,b0)) not in missing:
     # paircaps have synthetic outside endpoints; their removed edge has two real endpoints listed separately
     if any(p==a and q[1]==c0 for p,q in P if p[0]=='t'):continue
     connect(zmap[a],zmap[b0])
  ports=[zmap[P[o[h]][0]] for h in range(4)]
  connect(current[i],ports[0]);connect(current[j],ports[1]);current[i]=ports[2];current[j]=ports[3];cross+=1;capnodes+=len(Z)
 for p,want in enumerate(target):
  q=order.index(want,p)
  while q>p:
   i,j=order[q-1:q+1];swap(i,j);order[q-1:q+1]=[j,i];q-=1
 assert order==target
 for i,j in zip(order[::2],order[1::2]):connect(current[i],current[j])
 # remove irrelevant closed components, keep only components touching original boundary
 for C0 in list(nx.connected_components(G)):
  if not set(dummy)&C0:G.remove_nodes_from(C0)
 # verify whole open native region and explicit word witness
 for u in G:
  if u in dummy:assert G.degree(u)==1;continue
  if sgn[u]==1:
   assert G.degree(u)==4 and sorted(color[v] for v in G[u])==list(range(4)),(u,list(G[u]))
  else:
   assert G.degree(u)==3 and sum(val[v] for v in G[u])==1,(u,list(G[u]))
 for i,u in enumerate(dummy):
  v=next(iter(G[u]));assert sgn[v]==t[i][1];
  if sgn[v]==1:assert val[v]==w[i]
  else:assert color[v]==t[i][0]
 H=G.copy()
 if k>=3:
  H.add_edges_from(zip(dummy,dummy[1:]+dummy[:1]));H.add_edges_from((N,u) for u in dummy)
 elif k==2:H.add_edge(*dummy)
 assert nx.check_planarity(H)[0]
 return G,sgn,color,val,dummy,dict(initial_tuples=n,crossings=cross,cap_vertices=capnodes,tuples=sum(sgn[u]==1 and u not in dummy for u in G),vertices=len(G))

def compile_shore(T,S,P,w,guard={}):
 # cap is complementary, reverse port signs, same list order (reflection allowed)
 t=typ(P);G,sgn,col,val,dummy,stats=make_cap(tuple((c,-s) for c,s in t),w)
 # native closure with original IDs mapped to final tuple list
 old={a:('old',a) for a in S};new={u:('cap',u) for u in G if u not in dummy};H=nx.Graph();H.add_nodes_from(old.values());H.add_nodes_from(new.values());
 for a in S:
  if a[0]=='t':
   for c,r in enumerate(T[a[1]]):
    b=('e',c,r)
    if b in S:H.add_edge(old[a],old[b])
 for u,v in G.edges:
  if u in new and v in new:H.add_edge(new[u],new[v])
 for i,(a,b) in enumerate(P):H.add_edge(old[a],new[next(iter(G[dummy[i]]))])
 rowcolor={old[a]:a[1] for a in S if a[0]=='e'}|{new[u]:col[u] for u in new if sgn[u]==-1}
 tu=[old[a] for a in sorted(S) if a[0]=='t']+[new[u] for u in sorted(new) if sgn[u]==1];ids={a:i for i,a in enumerate(tu)};word={new[u]:val[u] for u in new if sgn[u]==1};g={ids[old[a]]:guard[a[1]] for a in S if a[0]=='t' and a[1] in guard};g.update({ids[a]:v for a,v in word.items()});bad=False
 for i,(a,b) in enumerate(P):
  if a[0]=='t':
   j=ids[old[a]];bad|=j in g and g[j]!=w[i];g[j]=w[i]
 X=[]
 for a in tu:
  rr=sorted(H[a],key=lambda b:rowcolor[b]);assert len(rr)==4 and [rowcolor[b] for b in rr]==list(range(4));X.append(tuple(rr))
 X=normalize(X);R,_=incidence(X);assert len(set(X))==len(X);assert nx.check_planarity(H)[0] and nx.is_connected(H);return X,R,g,bad,[a[1][1] for a in tu if a[0]=='old'],stats|dict(closed_tuples=len(X))

def close_shore(T,S,P,w,sel):
 X,R,g,bad,ids,stats=compile_shore(T,S,P,w);assert not bad;W={j for j,v in g.items() if v and j>=len(ids)}|{i for i,j in enumerate(ids) if j in sel};verify(X,W);assert all((j in W)==bool(v) for j,v in g.items());return stats

def main():
 rng=random.Random(26112615);results=[]
 # every distinct four-port crossover type for both signal bits and lane directions
 for c,e,s,z,x,y in it.product(range(4),range(4),(-1,1),(-1,1),(0,1),(0,1)):
  cap4(((c,s),(e,z),(c,-s),(e,-z)),(x,y,x,y))
 # sample arbitrary conservation-legal boundaries by type, including deliberately interleaved long interfaces
 for k in [2,3,4,5,6,7,8,10,12]:
  done=0;tries=0
  while done<3 and tries<100000:
   tries+=1;t=tuple((rng.randrange(4),rng.choice([-1,1])) for _ in range(k));d=[sum(s for c,s in t if c==j) for j in range(4)]
   if len({v%3 for v in d})!=1:continue
   w=legal(t)
   if not w:continue
   w=rng.choice(w);*_,st=make_cap(t,w);results.append(dict(kind='abstract',t=t,w=w,**st));done+=1
  print('arity',k,'done',done,flush=True)
 # actual native source bonds >4; same source local words, exact capped lifts
 for name,T in [('D',D),('C',C),('Q',Q)]:
  seen=set()
  for S,P in bonds(T,6):
   if len(P)<5 or len(P) in seen:continue
   W,_=local(T,S,P)
   if not W:continue
   w,sel=next(iter(W.items()));st=close_shore(T,S,P,w,sel);results.append(dict(kind='native',source=name,arity=len(P),**st));seen.add(len(P));print(name,len(P),st,flush=True)
   if len(seen)==2:break
 json.dump(results,open('sw15_results.json','w'),indent=2);print('jobs',len(results),'max',max(x['tuples'] for x in results),'crossings',sum(x['crossings'] for x in results))
if __name__=='__main__':main()
