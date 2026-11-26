import itertools as it, json, networkx as nx, sympy as sp
from collections import Counter
NO=[(1,6,11),(0,1,11),(3,4,5),(2,3,5),(0,3,10),(2,4,5),(1,2,6),(7,9,10),(7,8,9),(7,8,10),(4,8,9),(0,6,11)]
YES=NO.copy(); YES[1]=(1,2,11); YES[3]=(0,3,5)
W=(1,1,0,0,1,0,0,1,0,0,0,0)
T=[(0,1,6),(2,3,4),(8,9,10)]
NONTIGHT=[(0,2,7),(1,3,8),(5,6,8),(0,2,3),(1,4,8),(5,6,7),(0,3,6),(1,2,4),(4,5,7)]
V=(1,1,0,0,0,1,0,0,0)

def verify(R):
 n=len(R); assert all(len(set(r))==3 for r in R);assert Counter(x for r in R for x in r)==Counter({i:3 for i in range(n)})
 G=nx.Graph();G.add_nodes_from(range(2*n));G.add_edges_from((x,n+j) for j,r in enumerate(R) for x in r);assert nx.is_connected(G);p,E=nx.check_planarity(G);assert p;E.check_structure();return {str(v):list(E.neighbors_cw_order(v)) for v in G}
def valid(R,w):return all(sum(w[i] for i in r)==1 for r in R)
def models(R):
 n=len(R);out=[]
 for c in it.combinations(range(n),n//3):
  w=tuple(int(i in c) for i in range(n))
  if valid(R,w):out.append(w)
 return out

def close(R,pins=()):
 n=len(R);x=dict(pins)
 while True:
  old=len(x)
  for row in R:
   k=sum(x.get(v,0) for v in row);u=[v for v in row if v not in x]
   if k>1 or (not k and not u):return None
   if k==1:
    for v in u:x[v]=0
   elif len(u)==1:x[u[0]]=1
  for p in (2,3):
   A=[[int(j in row) for j in range(n)]+[1] for row in R]+[[int(j==v) for j in range(n)]+[b] for v,b in x.items()]; k=0
   for j in range(n):
    i=next((i for i in range(k,len(A)) if A[i][j]%p),None)
    if i is None:continue
    A[k],A[i]=A[i],A[k];A[k]=[(a*pow(A[k][j],-1,p))%p for a in A[k]]
    for i in range(len(A)):
     if i!=k and A[i][j]:
      c=A[i][j];A[i]=[(a-c*b)%p for a,b in zip(A[i],A[k])]
    k+=1
   for a in A:
    live=[i for i,z in enumerate(a[:-1]) if z]
    if not live and a[-1]%p:return None
    if len(live)==1:
     j=live[0];b=a[-1]*pow(a[j],-1,p)%p
     if b>1 or (j in x and x[j]!=b):return None
     x[j]=b
  if len(x)==old:return x

def probe(R):
 x=close(R)
 if x is None:return None
 for j in range(len(R)):
  if j in x:continue
  a=close(R,[*x.items(),(j,0)]);b=close(R,[*x.items(),(j,1)])
  if a is None and b is None:return None
  if a is None or b is None:return probe_pins(R,b if a is None else a)
 return x

def probe_pins(R,x):
 while True:
  old=len(x)
  for j in range(len(R)):
   if j in x:continue
   a=close(R,[*x.items(),(j,0)]);b=close(R,[*x.items(),(j,1)])
   if a is None and b is None:return None
   if a is None or b is None:x=b if a is None else a
  if len(x)==old:return x

def scc(R):
 n=len(R);owners={}
 for j,r in enumerate(R):
  for e in it.combinations(sorted(r),2):owners.setdefault(e,[]).append(j)
 ts=[t for t in it.combinations(range(n),3) if t not in R and all(e in owners for e in it.combinations(t,2))]
 A=sp.Matrix([[int(i in r) for i in range(n)] for r in R]);K=A.nullspace(); D=nx.DiGraph();D.add_nodes_from(range(n));arcs=[]
 for a,b in it.combinations(range(n),2):
  if all(k[a]==k[b] for k in K):D.add_edges_from([(a,b),(b,a)])
 for j,t in enumerate(ts):
  for v in t:
   a,b=tuple(x for x in t if x!=v)
   for k in owners[(a,b)]:
    u=next(x for x in R[k] if x not in (a,b));arcs.append((u,v,j));D.add_edge(u,v)
 saturated=set()
 while True:
  c={v:i for i,C in enumerate(nx.strongly_connected_components(D)) for v in C};new={j for u,v,j in arcs if c[u]==c[v]}-saturated
  if not new:return ts,sorted(saturated)
  saturated|=new
  for u,v,j in arcs:
   if j in new:D.add_edge(v,u)

def chain(R,k):
 out=[tuple(x+12*i for x in r) for i in range(k) for r in R]
 for i in range(k-1):
  a,b=12*i+1,12*(i+1)+11;x,y=12*i+11,12*(i+1)+11
  out[a]=tuple(sorted((set(out[a])-{x})|{y}));out[b]=tuple(sorted((set(out[b])-{y})|{x}))
 return out

def certificate(R,k):
 # Three extra conflict triangles are covered by exact-one rows 4,6,10.
 for i in range(k):
  off=12*i; ts=[tuple(off+x for x in t) for t in T]
  rr=[R[off+j] for j in (4,6,10)]
  assert Counter(x for r in ts for x in r)==Counter(x for r in rr for x in r)
  for t in ts:
   for pair in it.combinations(t,2):assert any(set(pair)<=set(r) for r in R)
  # T1 is tight, three original pair rows force equality x2=x3=x4.
  assert [R[off+j] for j in (2,3,5)]==[tuple(off+x for x in NO[j]) for j in (2,3,5)]
 return 3*k

if __name__=='__main__':
 rotations={name:verify(R) for name,R in [('NO',NO),('YES',YES),('NONTIGHT',NONTIGHT)]}
 assert models(NO)==[] and models(YES)==[W] and valid(NONTIGHT,V)
 assert sum(V[i] for i in (2,4,7))==0
 triangles,sat=scc(NO);assert triangles==T and sat==[]
 assert certificate(NO,1)==3
 base={name:probe(R) for name,R in [('NO',NO),('YES',YES),('NONTIGHT',NONTIGHT)]}
 assert base['NO'] is None
 results=[]
 for k in (1,2,4,8,16,32):
  Y=chain(YES,k);Z=chain(NO,k); verify(Y);verify(Z);assert valid(Y,W*k);t=certificate(Z,k)
  # exact baseline on small scales only; no claim of hard postclosure NO
  if k<=2:assert probe(Z) is None
  results.append(dict(k=k,n=12*k,certified_triangles=t,yes_witness=True,no_certificate=True))
 print(json.dumps(dict(base=base,triangles=triangles,scc=sat,results=results,rotations=rotations),indent=2))
