import itertools as it, json, collections as co
import networkx as nx

def incidence(n,T):
 g=nx.Graph();g.add_nodes_from((c,v) for c in range(3) for v in range(n));g.add_nodes_from((3,i) for i in range(len(T)))
 g.add_edges_from(((3,i),(c,v)) for i,t in enumerate(T) for c,v in enumerate(t));return g

def pm(T,A,B,a=0,b=1,pins=()):
 A,B=set(A),set(B);p=[]
 for t in pins:
  if t not in T or t[a] not in A or t[b] not in B:return None
  A.remove(t[a]);B.remove(t[b]);p.append(t)
 if len(A)!=len(B):return None
 g=nx.Graph();L={(0,x) for x in A};g.add_nodes_from(L);g.add_nodes_from((1,y) for y in B);rep={}
 for t in T:
  if t[a] in A and t[b] in B:
   x,y=(0,t[a]),(1,t[b]);g.add_edge(x,y);rep[x,y]=t
 M=nx.algorithms.bipartite.maximum_matching(g,top_nodes=L)
 return p+[rep[x,M[x]] for x in L] if all(x in M for x in L) else None

def closure(n,T):
 T=set(T);V=set(range(n));lanes=((0,1),(0,2),(1,2))
 while True:
  occ={(c,v):[t for t in T if t[c]==v] for c in range(3) for v in V}
  if any(not x for x in occ.values()):return None
  # A 2-regular bipartite multigraph is a union of even cycles, including doubled edges.
  if all(len(x)==2 for x in occ.values()):return T
  old=set(T)
  for ts in occ.values():
   if len(ts)==1:
    t=ts[0];T={u for u in T if u==t or all(u[c]!=t[c] for c in range(3))}
  for a,b in lanes:
   if pm(T,V,V,a,b) is None:return None
   T={t for t in T if pm(T,V,V,a,b,(t,)) is not None}
  if T==old:return T

def acquire(n,T,k=2):
 g=nx.Graph();g.add_edges_from(((0,t[0]),(1,t[1])) for t in T);regions=[]
 for C in nx.connected_components(g):
  A={v for c,v in C if c==0};B={v for c,v in C if c==1};R=sorted(t for t in T if t[0] in A);Z={t[2] for t in R}
  if len(A)!=len(B):return 'NO',[]
  regions.append((A,B,R,Z))
 counts=co.Counter(z for A,B,R,Z in regions for z in Z);E={z for z in counts if counts[z]>1};tables=[]
 for A,B,R,Z in regions:
  P=Z-E;S=Z&E;r=len(A)-len(P)
  if not 0<=r<=len(S):return 'NO',[]
  if min(r,len(S)-r)>k:return 'UNKNOWN',[]
  # Certify that every local XY perfect matching uses distinct labels.
  for t,u in it.combinations(R,2):
   if t[2]==u[2] and pm(R,A,B,pins=(t,u)) is not None:return 'UNKNOWN',[]
  table={}
  for small in it.combinations(sorted(S),min(r,len(S)-r)):
   Q=frozenset(small) if r<=len(S)-r else frozenset(S-set(small))
   W=pm([t for t in R if t[2] in P|Q],A,B)
   if W is not None:
    assert len({t[2] for t in W})==len(A) and {t[2] for t in W}==P|Q
    table[Q]=W
  if not table:return 'NO',[]
  tables.append(table)
 return E,tables

def matroid(B):
 return all(any((a-{x})|{y} in B for y in b-a) for a in B for b in B for x in a-b)

def union_alloc(M,E):
 # Standard shortest augmenting path matroid-union algorithm with explicit basis oracles.
 E=set(E);D=[set().union(*B) for B in M]
 if sum(map(len,D))==len(set().union(*D)) if D else True:
  return [set(max(B,key=lambda b:len(b&E))&E) for B in M]
 I=[set() for _ in M]
 def ind(i,S):return any(S<=b for b in M[i])
 while True:
  used=set().union(*I);p={e:None for e in E-used};q=co.deque(p);end=None
  while q and end is None:
   e=q.popleft()
   for i in range(len(M)):
    if e in I[i] or e not in D[i]:continue
    if ind(i,I[i]|{e}):end=(e,i);break
    for f in I[i]:
     if f not in p and ind(i,(I[i]-{f})|{e}):p[f]=(e,i);q.append(f)
  if end is None:return I
  e,i=end;I[i].add(e)
  while p[e] is not None:
   f,i=p[e];I[i].remove(e);I[i].add(f);e=f
  assert all(ind(i,s) for i,s in enumerate(I)) and sum(map(len,I))==len(set().union(*I))

def hybrid(E,tables):
 M=[];B=list(tables)
 # Recompute exact matroid dual after each sound unary mask pruning/promotion.
 while True:
  M.extend(T for T in B if matroid(T));B=[T for T in B if not matroid(T)]
  r=sum(len(next(iter(T))) for T in M);q=sum(len(next(iter(T))) for T in B)
  assert r+q==len(E)
  def rank(A):return sum(map(len,union_alloc(M,A)))
  if rank(E)<r:return 'NO',None
  def di(A):return rank(E-set(A))==r
  C=[{s:w for s,w in T.items() if di(s)} for T in B]
  if any(not T for T in C):return 'NO',None
  if all(len(a)==len(b) for a,b in zip(C,B)):break
  B=C
 if any(len(T)!=2 for T in B):return 'UNKNOWN',None
 U=set().union(*(set().union(*T) for T in B));live={z for z in U if di({z})}
 g=nx.Graph();g.add_nodes_from(live);g.add_edges_from((z,w) for z,w in it.combinations(live,2) if not di({z,w}))
 C=list(nx.connected_components(g));d=len(U)+rank(E-U)-r
 if d<q:return 'NO',None
 if d!=len(C):return 'UNKNOWN',None
 # D restricted to U is now certified a rank-one partition matroid with loops.
 cl={z:i for i,c in enumerate(C) for z in c};opts=[list(T) for T in B];h=nx.DiGraph();h.add_nodes_from((i,b) for i in range(len(B)) for b in (0,1))
 def ban(i,b,j,c):h.add_edge((i,b),(j,1-c));h.add_edge((j,c),(i,1-b))
 classes={}
 for i,O in enumerate(opts):
  for b,S in enumerate(O):
   K={cl[z] for z in S if z in cl};classes[i,b]=K
   if len(K)!=len(S):ban(i,b,i,b)
 for i,j in it.combinations(range(len(B)),2):
  for b,c in it.product((0,1),repeat=2):
   if classes[i,b]&classes[j,c]:ban(i,b,j,c)
 cc=list(nx.strongly_connected_components(h));idx={v:i for i,c in enumerate(cc) for v in c}
 if any(idx[i,0]==idx[i,1] for i in range(len(B))):return 'NO',None
 topo={v:i for i,v in enumerate(nx.topological_sort(nx.condensation(h,cc)))}
 pick=[opts[i][int(topo[idx[i,1]]>topo[idx[i,0]])] for i in range(len(B))];S=set().union(*pick)
 assert len(S)==q and di(S)
 I=union_alloc(M,E-S);assert sum(map(len,I))==r
 return 'YES',[t for T,s in zip(M,I) for t in T[frozenset(s)]]+[t for T,s in zip(B,pick) for t in T[s]]

def ring(k,mixed=True):
 T=[]
 for i in range(k):
  if mixed:L=[4*i,4*i+1];R=[4*i+2,4*i+3]
  else:L=[2*i,2*i+1];R=[2*((i+1)%k),2*((i+1)%k)+1]
  T.extend([(2*i,2*i,L[0]),(2*i,2*i+1,L[1]),(2*i+1,2*i+1,R[0]),(2*i+1,2*i,R[1])])
  if mixed:
   for b in (0,1):
    x=2*k+2*i+b;T.extend([(x,x,R[b]),(x,x,4*((i+1)%k)+b)])
 return (4*k if mixed else 2*k),T

def brute(n,T):
 def go(i,Y,Z):
  if i==n:return True
  return any(go(i+1,Y|{y},Z|{z}) for x,y,z in T if x==i and y not in Y and z not in Z)
 return go(0,set(),set())

def run(n,T):
 assert len(set(T))==len(T) and nx.check_planarity(incidence(n,T))[0]
 C=closure(n,T)
 if C is None:return 'NO',0,0
 E,A=acquire(n,C)
 if isinstance(E,str):return E,0,0
 label,W=hybrid(E,A)
 if label=='YES':assert len(W)==n and set(W)<=set(T) and all(len({t[i] for t in W})==n for i in range(3))
 return label,sum(matroid(t) for t in A),sum(not matroid(t) for t in A)

def main():
 out={'rings':[],'octa_subsets':co.Counter()}
 for mixed in (False,True):
  for k in (2,4,8,16,32,64):
   n,T=ring(k,mixed);v=run(n,T);assert v[0]=='YES';out['rings'].append([mixed,k,n,len(T),*v])
 base=[(0,1,4),(0,0,0),(1,0,3),(1,1,3),(2,3,1),(2,2,2),(3,2,5),(3,3,1),(4,5,0),(4,4,2),(5,4,4),(5,5,5)]
 assert not brute(6,base) and brute(6,base+[(4,4,0)])
 out['neighbors']=[]
 for steps in (0,1,4,16,64):
  for sat in (False,True):
   n=6;T=base+([(4,4,0)] if sat else []);z=2
   for _ in range(steps):
    i=next(i for i,t in enumerate(T) if t[2]==z);x,y,_=T[i];T[i]=(x,y,n);T.extend([(n,n,z),(n,n,n)]);z=n;n+=1
   v=run(n,T);assert v[0]==('YES' if sat else 'NO')
   out['neighbors'].append([sat,steps,n,len(T),*v])
 A=list(it.product(range(2),repeat=3))
 for mask in range(256):
  T=[t for i,t in enumerate(A) if mask>>i&1];v=run(2,T)[0];b=brute(2,T);assert v=='UNKNOWN' or (v=='YES')==b;out['octa_subsets'][v]+=1
 # Generic overlapping matroid union: uniform bases on overlapping sets, exact brute rank.
 import random
 rng=random.Random(4104);out['union_checks']=0
 for _ in range(300):
  E=set(range(6));M=[]
  for i in range(3):
   D={z for z in E if rng.randrange(2)};r=rng.randrange(len(D)+1);M.append({frozenset(a):None for a in it.combinations(sorted(D),r)})
  A={z for z in E if rng.randrange(2)};I=union_alloc(M,A);best=max(len(set().union(*[b&A for b in Q])) for Q in it.product(*M));assert sum(map(len,I))==best;out['union_checks']+=1
 print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
