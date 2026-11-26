import itertools as it,json,random
import networkx as nx
import numpy as np
Q=[t for t in it.product(range(2),repeat=4) if sum(t)==2]
U=[(3,5,0,0),(2,0,4,2),(1,1,2,2),(0,5,1,3),(1,4,2,4),(5,0,4,5),(3,2,5,0),(0,4,2,2),(5,3,4,1),(4,2,0,0),(4,2,5,1),(0,4,1,4),(5,3,3,5),(2,1,3,3),(3,3,5,3),(2,0,3,5),(4,5,0,1),(1,1,1,4)]
W=U[:];a,b=list(W[1]),list(W[14]);a[3],b[3]=b[3],a[3];W[1],W[14]=tuple(a),tuple(b)
def rank(A):
 A=np.array(A,dtype=np.int16).copy()%3;r=0
 for j in range(A.shape[1]):
  p=np.flatnonzero(A[r:,j])
  if not len(p):continue
  p=int(p[0])+r;A[[p,r]]=A[[r,p]];A[r]=A[r]*A[r,j]%3
  v=A[:,j].copy();v[r]=0;A=(A-v[:,None]*A[r])%3;r+=1
  if r==len(A):break
 return r
def basis(cols,d):
 B={}
 for v in cols:
  v=np.array(v,dtype=np.int16).copy()%3
  for j,w in sorted(B.items()):v=(v-v[j]*w)%3
  nz=np.flatnonzero(v)
  if len(nz):j=int(nz[0]);B[j]=v*v[j]%3
 return B
def contains(B,v):
 v=np.array(v,dtype=np.int16).copy()%3
 for j,w in sorted(B.items()):v=(v-v[j]*w)%3
 return not np.any(v)
def dp(H,b):
 d,m=H.shape;stats={'width':0,'max_rows':0,'pairs':0,'nodes':0}
 def go(S):
  C=[i for i in range(m) if i not in S];O=basis(H[:,C].T,d);L=basis(H[:,S].T,d)
  stats['width']=max(stats['width'],len(O)+len(L)-rankH);stats['nodes']+=1
  if len(S)==1:raw=[(np.zeros(d,dtype=np.int16),0,1),(H[:,S[0]],1<<S[0],1)]
  else:
   h=len(S)//2;P=go(S[:h]);R=go(S[h:]);stats['pairs']+=len(P)*len(R)
   raw=[((np.array(u)+v)%3,p|q,c*k) for u,(p,c) in P.items() for v,(q,k) in R.items()]
  out={}
  for v,w,c in raw:
   if contains(O,b-v):
    key=tuple(map(int,v));out[key]=(w,c+out.get(key,(0,0))[1])
  stats['max_rows']=max(stats['max_rows'],len(out));assert len(out)<=3**(len(O)+len(L)-rankH)
  return out
 rankH=rank(H);table=go(list(range(m)));w,c=table.get(tuple(b),(0,0))
 if c:assert np.array_equal(H@np.array([(w>>i)&1 for i in range(m)])%3,b)
 return c,stats
def rows(T):
 n=len(T)//3;return {(c,i):[j for j,t in enumerate(T) if t[c]==i] for c in range(4) for i in range(n)}
def exact(T):
 R=rows(T);n=len(T)//3
 return [set(s) for s in it.combinations(range(len(T)),n) if all(len(set(s).intersection(r))==1 for r in R.values())]
def sourcecheck(T):
 n=len(T)//3;R=rows(T);assert len(T)==3*n==len(set(T));assert all(len(r)==3 for r in R.values());assert all(all(0<=i<n for i in t) for t in T)
 G=nx.Graph((j,e) for e,r in R.items() for j in r);assert nx.check_planarity(G)[0] and nx.is_connected(G)
 return R
def grid(k):
 B=nx.grid_2d_graph(k,k);G=nx.Graph();ports={};dirs=[(-1,0),(0,1),(1,0),(0,-1)]
 for u in B:
  N=[(u[0]+a,u[1]+b) for a,b in dirs if (u[0]+a,u[1]+b) in B];C=[]
  for v in N:
   p=(u,v,0);q=(u,v,1);ports[u,v]=p,q;C.extend([p,q])
  G.add_edges_from(zip(C,C[1:]+C[:1]))
 for u,v in B.edges:
  a,b=ports[u,v];c,d=ports[v,u];G.add_edges_from([(a,d),(b,c)])
 L=sorted(u for u in G if u[2]==0);R=sorted(set(G)-set(L));assert all(G.degree(u)==3 for u in G);assert nx.is_bipartite(G) and nx.check_planarity(G)[0]
 return G,L,R
def compile_grid(k,special=None):
 G,L,R=grid(k);loc={};portmap={};T=[];offset=0
 for i,u in enumerate(L):
  B=special if i==0 and special is not None else Q;n=len(B)//3
  P=[j for j,t in enumerate(B) if t[0]==0];N=sorted(G[u]);assert len(P)==3
  loc[u]=(B,len(T));portmap[u]=dict(zip(N,P))
  for j,t in enumerate(B):
   s=[(0,c,i,t[c]) for c in range(4)]
   if j in P:s[0]=(1,0,R.index(N[P.index(j)]),0)
   T.append(s)
 for c in range(4):
  D={a:i for i,a in enumerate(sorted({t[c] for t in T}))}
  for t in T:t[c]=D[t[c]]
 T=list(map(tuple,T));A=sourcecheck(T);return G,L,R,loc,portmap,T,A
def solve_grid(k,special=None):
 G,L,R,loc,P,T,A=compile_grid(k,special);local={u:exact(B) for u,(B,o) in loc.items()};m=len(T)
 if any(not s for s in local.values()):return {'tuples':m,'yes':False,'local_conservation_no':True}
 force=None
 if special is not None:
  u=L[0];force=next(v for v,j in P[u].items() if any(j in s for s in local[u]))
  G2=G.copy();G2.remove_nodes_from([u,force]);M=nx.bipartite.maximum_matching(G2,top_nodes=set(L)-{u});M[u]=force
 else:M=nx.bipartite.maximum_matching(G,top_nodes=set(L))
 S=set()
 for u in L:
  B,o=loc[u];j=P[u][M[u]];s=next(s for s in local[u] if j in s);S.update(o+i for i in s)
 assert len(S)==m//3 and all(len(S.intersection(r))==1 for r in A.values())
 out={'tuples':m,'yes':True,'grid_side':k,'macro_vertices':len(G),'macro_edges':G.number_of_edges(),'verified_selected':len(S)}
 if special is None and k<=4:
  H=np.array([[i in r for i in range(m)] for r in A.values()],dtype=np.int16);hidden=[o+j for u,(B,o) in loc.items() for j in range(len(B)) if B[j][0]!=0]
  rr=rank(H);rh=rank(H[:,hidden]);assert rr==5*len(L)-1 and rh==3*len(L);out.update(rank=rr,contracted_rank=rr-rh,projective_rank=len(L)+1,projective_excess=2*len(L)-1,edge_connectivity=nx.edge_connectivity(G))
 return out
def acquire_matching(T,R):
 m=len(T);H=np.array([[j in r for j in range(m)] for r in R.values()],dtype=np.int16);A=np.column_stack([H,np.ones(len(H),dtype=np.int16)]);piv=[];r=0
 for j in range(m):
  ps=np.flatnonzero(A[r:,j])
  if not len(ps):continue
  p=int(ps[0])+r;A[[p,r]]=A[[r,p]];A[r]=A[r]*A[r,j]%3
  v=A[:,j].copy();v[r]=0;A=(A-v[:,None]*A[r])%3;piv.append(j);r+=1
 assert not np.any(A[r:,-1]);free=[j for j in range(m) if j not in piv];F=np.zeros((m,len(free)+1),dtype=np.int16)
 for k,j in enumerate(free):F[j,k+1]=1
 for i,j in enumerate(piv):F[j,0]=A[i,-1];F[j,1:]=-A[i,free]%3
 D={};groups=[];idx=[]
 for i,v in enumerate(F):
  key=tuple(v)
  if key not in D:D[key]=len(groups);groups.append([])
  j=D[key];groups[j].append(i);idx.append(j)
 distinct=sorted({tuple(sorted(idx[j] for j in row)) for row in R.values()});assert all(len(set(row))==3 for row in distinct)
 occ=[[] for _ in groups]
 for i,row in enumerate(distinct):
  for j in row:occ[j].append(i)
 assert all(len(o)==2 for o in occ);G=nx.Graph();G.add_nodes_from(range(len(distinct)));edge={}
 for j,(a,b) in enumerate(occ):G.add_edge(a,b);edge[frozenset((a,b))]=j
 assert nx.is_bipartite(G);M=nx.max_weight_matching(G,maxcardinality=True);assert 2*len(M)==len(distinct)
 S={i for e in M for i in groups[edge[frozenset(e)]]};assert all(len(S.intersection(row))==1 for row in R.values())
 return {'classes':len(groups),'rows':len(distinct),'verified_selected':len(S),'nullity':len(free)}
def main():
 random.seed(2148);results={'random':{'jobs':0,'yes':0,'no':0,'pairs':0,'max_width':0},'small':{},'mesh':[],'neighbors':[]}
 for _ in range(200):
  d=random.randint(1,6);m=random.randint(1,10);H=np.array([[random.randrange(3) for i in range(m)] for j in range(d)],dtype=np.int16);b=np.array([random.randrange(3) for j in range(d)],dtype=np.int16)
  want=sum(np.array_equal(H@np.array(x)%3,b) for x in it.product((0,1),repeat=m));got,s=dp(H,b);assert got==want
  z=results['random'];z['jobs']+=1;z['yes' if got else 'no']+=1;z['pairs']+=s['pairs'];z['max_width']=max(z['max_width'],s['width'])
 for name,T in [('Q',Q),('U',U),('W',W)]:
  R=sourcecheck(T);H=np.array([[j in r for j in range(len(T))] for r in R.values()],dtype=np.int16);b=np.ones(len(R),dtype=np.int16);c,s=dp(H,b);assert c==len(exact(T));results['small'][name]={'covers':c,**s}
 for k in (2,3,4,6,8,12,16):
  z=solve_grid(k)
  if k<=4:
   *_,T,R=compile_grid(k);z['acquired_matching']=acquire_matching(T,R)
  results['mesh'].append(z)
 for k in (2,4,8):
  u=solve_grid(k,U);v=solve_grid(k,W);assert not u['yes'] and v['yes'] and u['tuples']==v['tuples'];results['neighbors'].append({'side':k,'no':u,'yes':v})
 print(json.dumps(results,indent=2))
if __name__=='__main__':main()
