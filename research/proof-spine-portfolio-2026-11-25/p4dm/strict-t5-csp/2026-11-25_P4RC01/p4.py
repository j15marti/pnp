import networkx as nx,itertools as it,random
Q=[t for t in it.product(range(2),repeat=4) if sum(t)==2]
def graph(T):
 G=nx.Graph();G.add_edges_from((('t',j),('e',i,v)) for j,t in enumerate(T) for i,v in enumerate(t));return G
def covers(T):
 n=len(T)//3; groups={v:set() for v in it.product(range(4),range(n))}
 for j,t in enumerate(T):
  for i,v in enumerate(t):groups[i,v].add(j)
 def rec(left,sel):
  if not left:return sel
  v=min(left,key=lambda v:len([j for j in groups[v] if all((i,w) in left for i,w in enumerate(T[j]))]))
  for j in groups[v]:
   vs={(i,w) for i,w in enumerate(T[j])}
   if vs<=left:
    ans=rec(left-vs,sel+[j])
    if ans is not None:return ans
  return None
 return rec(set(groups),[])
def blocks(k):return [tuple(v+2*b for v in t) for b in range(k) for t in Q]
def mutate(T,r):
 a,b=r.sample(range(len(T)),2); i=r.randrange(4);U=list(T);p,q=list(U[a]),list(U[b]);p[i],q[i]=q[i],p[i];U[a],U[b]=tuple(p),tuple(q);return U
if __name__=='__main__':
 r=random.Random(321);T=blocks(3); seen={};count=0
 for k in range(25000):
  U=mutate(T,r)
  if U==T or len(set(U))!=len(U):continue
  G=graph(U)
  if not nx.check_planarity(G)[0]:continue
  T=U;count+=1
  if nx.is_connected(G):
   ans=covers(T);tag=ans is not None
   if tag not in seen:seen[tag]=(T,ans);print('FOUND',tag,T,ans,flush=True)
   if len(seen)==2:break
 print('accepted',count, 'iter',k)
