import itertools as I, json, random, math
import networkx as nx
from sympy import Matrix

def inc(n,T):
 g=nx.Graph();g.add_nodes_from((c,i) for c in range(3) for i in range(n));g.add_edges_from(((3,j),(c,t[c])) for j,t in enumerate(T) for c in range(3));return g

def close(n,T):
 live=set(range(len(T))); probes=rounds=0
 while True:
  rounds+=1; bad=set()
  for c in range(3):
   for i in range(n):
    L={j for j in live if T[j][c]==i}
    if not L:return None,probes,rounds
    if len(L)==1:
     t=T[next(iter(L))];bad|={j for j in live-L if any(T[j][k]==t[k] for k in range(3))}
  # sound parity forced bits
  m=len(T); rows=[sum(1<<j for j in live if T[j][c]==i)|(1<<m) for c in range(3) for i in range(n)];r=0
  for j in sorted(live):
   k=next((k for k in range(r,len(rows)) if rows[k]>>j&1),None)
   if k is None:continue
   rows[r],rows[k]=rows[k],rows[r]
   for k in range(len(rows)):
    if k!=r and rows[k]>>j&1:rows[k]^=rows[r]
   r+=1
  if (1<<m) in rows:return None,probes,rounds
  for row in rows:
   v=row&((1<<m)-1)
   if v and v.bit_count()==1:
    j=v.bit_length()-1
    if not row>>m:bad.add(j)
    else:bad|={i for i in live-{j} if any(T[i][k]==T[j][k] for k in range(3))}
  for a,b in I.combinations(range(3),2):
   for j in sorted(live):
    probes+=1; g=nx.Graph(); A=[(0,i) for i in range(n)];g.add_nodes_from(A+[(1,i) for i in range(n)])
    g.add_edges_from(((0,T[i][a]),(1,T[i][b])) for i in live if i==j or (T[i][a]!=T[j][a] and T[i][b]!=T[j][b]))
    if len(nx.algorithms.bipartite.maximum_matching(g,top_nodes=A))!=2*n:bad.add(j)
  if not bad:return live,probes,rounds
  live-=bad

def pms(n,T):
 return [frozenset(M) for M in I.product(*[[j for j,t in enumerate(T) if t[0]==x] for x in range(n)]) if len({T[j][1] for j in M})==n]

def sig(T,C):
 v=0
 for j in C:v^=1<<T[j][2]
 return v

class Counter:
 def __init__(self,n,T):
  self.n=n;self.T=T;self.calls=0;self.cache={};g=inc(n,T);assert nx.check_planarity(g)[0];g.remove_nodes_from([(2,i) for i in range(n)])
  # signs on original indexed edges by face equations after smoothing
  self.neg=0
  for V in nx.connected_components(g):
   h=g.subgraph(V);assert sum(v[0]==0 for v in V)==sum(v[0]==1 for v in V)
   _,emb=nx.check_planarity(h);seen=set();rows=[];m=len(T)
   for u,v in emb.edges():
    if (u,v) in seen:continue
    face=emb.traverse_face(u,v,seen);assert len(face)%4==0
    mask=0
    for w in face:
     if w[0]==3:mask^=1<<w[1]
    rows.append(mask|(((len(face)//4+1)%2)<<m))
   r=0; piv=[]
   for j in range(m):
    k=next((k for k in range(r,len(rows)) if rows[k]>>j&1),None)
    if k is None:continue
    rows[r],rows[k]=rows[k],rows[r]
    for k in range(len(rows)):
     if k!=r and rows[k]>>j&1:rows[k]^=rows[r]
    piv.append(j);r+=1
   assert (1<<m) not in rows
   for j,row in zip(piv,rows):self.neg|=(row>>m)<<j
 def count(self,F=frozenset()):
  F=frozenset(F)
  if F in self.cache:return self.cache[F]
  self.calls+=1;n=self.n;T=self.T
  X={T[j][0] for j in F};Y={T[j][1] for j in F}
  if len(X)!=len(F) or len(Y)!=len(F):return 0
  A=[[0]*n for _ in range(n)]
  for j,(x,y,z) in enumerate(T):
   if j in F or (x not in X and y not in Y):A[x][y]+=1-2*((self.neg>>j)&1)
  ans=abs(int(Matrix(A).det(method='bareiss')));self.cache[F]=ans;return ans

def orientations(T,C):
 # two alternating perfect matchings of indexed simple cycle (including digon)
 C=sorted(C);G=nx.Graph();G.add_nodes_from(C)
 for i,j in I.combinations(C,2):
  if T[i][0]==T[j][0] or T[i][1]==T[j][1]:G.add_edge(i,j)
 assert nx.is_connected(G);d=nx.bipartite.color(G);A=frozenset(j for j in C if d[j]);B=frozenset(C)-A
 assert len(A)==len(B) and all(len({T[j][c] for j in L})==len(L) for L in (A,B) for c in (0,1))
 return A,B

def cert(T,Cs,K):
 ori=[orientations(T,C) for C in Cs];total=K.count();mom=[]
 for r in [1,2]:
  mom.append(sum(K.count(frozenset().union(*a)) for S in I.combinations(ori,r) for a in I.product(*S)))
 return total,mom, mom[0]-mom[1]==total

def audit(n,T,Cs):
 assert nx.check_planarity(inc(n,T))[0];M=pms(n,T);K=Counter(n,T);total,mom,ok=cert(T,Cs,K)
 A=[sum(len(m&set(C))*2==len(C) for C in Cs) for m in M]
 assert total==len(M) and mom==[sum(A),sum(math.comb(a,2) for a in A)]
 assert not ok or min(A)>=1
 if ok:
  p=sig(T,Cs[0]);assert p and all(sig(T,C)==p for C in Cs)
  for m in M:
   C=next(frozenset(C) for C in Cs if len(m&set(C))*2==len(C));assert m^C in M and sig(T,m^C)==sig(T,m)^p
 return dict(total=total,moments=mom,certified=ok,determinants=K.calls,activity={a:A.count(a) for a in set(A)},sat=any(sig(T,m)==(1<<n)-1 for m in M))

def main():
 T=[tuple(map(int,t)) for t in '000 001 012 020 110 120 122 200 201 210 211'.split()]
 Cs=[]
 for r in (2,4,6):
  for C in I.combinations(range(len(T)),r):
   if sig(T,C)!=6:continue
   h=nx.Graph();h.add_edges_from(((3,j),(c,T[j][c])) for j in C for c in range(2))
   if nx.is_connected(h) and all(d==2 for v,d in h.degree):Cs.append(C)
 live,pr,rd=close(3,T);assert live==set(range(len(T)))
 A=audit(3,T,Cs);assert A['certified'];A.update(probes=pr,rounds=rd)
 M=pms(3,T);anchor=next(m for m in M if sig(T,m)==1)
 C=next(frozenset(C) for C in Cs if len(anchor&set(C))*2==len(C));lift=anchor^C
 assert sig(T,lift)==7 and all(len({T[j][c] for j in lift})==3 for c in range(3))
 A.update(cycles=Cs,anchor=sorted(anchor),lift=sorted(lift));assert close(3,T)[0]==live
 full=set(range(len(M))); masks=[{i for i,m in enumerate(M) if len(m&set(C))*2==len(C)} for C in Cs]
 for r in range(1,len(Cs)+1):
  for S in I.combinations(range(len(Cs)),r):
   if len(set().union(*(set(Cs[i]) for i in S)))==sum(len(Cs[i]) for i in S):assert set().union(*(masks[i] for i in S))!=full
 # genuine planar UNSAT / SAT neighbors: three projections all support on U
 U=[tuple(map(int,t)) for t in '000 002 010 011 021 022 100 101 111 201 202 221'.split()];neighbors=[]
 for V in [U,U+[(1,1,0)]]:
  live,p,r=close(3,V);assert live==set(range(len(V)));K=Counter(3,V);M=pms(3,V);assert K.count()==len(M);neighbors.append(dict(m=len(V),sat=any(sig(V,m)==7 for m in M),pm=len(M),probes=p))
 assert [a['sat'] for a in neighbors]==[False,True]
 # scale via disconnected copies: independent local certificates lift, no hardness claim
 scale=[]
 for k in [1,4,16,64]:
  V=[tuple(v+3*i for v in t) for i in range(k) for t in T];assert nx.check_planarity(inc(3*k,V))[0]
  W=lift
  chosen=[V[11*i+j] for i in range(k) for j in W];assert all(len({t[c] for t in chosen})==3*k for c in range(3));scale.append(dict(n=3*k,m=len(V),matchings=str(14**k),local_certificates=k))
 # seeded audit, all cycle candidates from finite matching oracle, not production acquisition
 R=random.Random(41);tests=0;certs=0;dets=0
 for _ in range(180):
  V=[t for t in I.product(range(3),repeat=3) if R.random()<.39];g=inc(3,V)
  if not nx.check_planarity(g)[0]:continue
  M=pms(3,V)
  if not M:continue
  Q={}
  for a,b in I.combinations(M,2):
   h=nx.Graph();h.add_edges_from(((3,j),(c,V[j][c])) for j in a^b for c in range(2))
   for C in nx.connected_components(h):
    q=frozenset(v[1] for v in C if v[0]==3);p=sig(V,q)
    if p:Q.setdefault(p,set()).add(q)
  for p,group in sorted(Q.items()):
   Cs=sorted(group,key=lambda q:tuple(sorted(q)))[:12];out=audit(3,V,Cs);tests+=1;certs+=out['certified'];dets+=out['determinants']
 print(json.dumps(dict(fixture=A,neighbors=neighbors,scale=scale,seed=41,random_group_tests=tests,random_certificates=certs,random_determinants=dets),indent=2))
if __name__=='__main__':main()
