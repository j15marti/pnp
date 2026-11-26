import itertools as I, json, random, networkx as nx
Q=[t for t in I.product(range(2),repeat=4) if sum(t)==2]
U=[(3,5,0,0),(2,0,4,2),(1,1,2,2),(0,5,1,3),(1,4,2,4),(5,0,4,5),(3,2,5,0),(0,4,2,2),(5,3,4,1),(4,2,0,0),(4,2,5,1),(0,4,1,4),(5,3,3,5),(2,1,3,3),(3,3,5,3),(2,0,3,5),(4,5,0,1),(1,1,1,4)]
V=[(0,0,5,1),(0,1,0,1),(0,1,1,0),(1,0,0,1),(1,0,1,0),(1,1,0,0),(2,2,3,3),(2,3,2,3),(2,4,3,2),(3,2,2,3),(3,2,3,2),(3,3,2,2),(4,3,5,5),(4,5,4,5),(4,5,5,4),(5,4,4,5),(5,4,1,4),(5,5,4,4)]
def swap(T,a,b,c):
 T=list(T);p,q=list(T[a]),list(T[b]);p[c],q[c]=q[c],p[c];T[a],T[b]=tuple(p),tuple(q);return T
W=swap(U,1,14,3)
def graph(T):
 G=nx.Graph();G.add_edges_from((('t',j),('e',i,v)) for j,t in enumerate(T) for i,v in enumerate(t));return G
def rows(T):return [(c,a,tuple(j for j,t in enumerate(T) if t[c]==a)) for c in range(4) for a in range(len(T)//3)]
def verify(T,S):return all(sum(j in S for j in r)==1 for c,a,r in rows(T))
def ref(T,p):
 rs=[r for c,a,r in rows(T)];by=[set() for t in T];on={j for j,v in p.items() if v};off={j for j,v in p.items() if not v}
 for k,r in enumerate(rs):
  for j in r:by[j].add(k)
 left=set(range(len(rs)))
 for j in on:
  if not by[j]<=left:return None
  left-=by[j]
 def f(left):
  if not left:return set()
  k=min(left,key=lambda k:sum(j not in off and by[j]<=left for j in rs[k]))
  for j in rs[k]:
   if j not in off and by[j]<=left:
    x=f(left-by[j])
    if x is not None:return {j}|x
  return None
 x=f(left);return None if x is None else x|on

def closure(T,guard,weighted=True):
 p=dict(guard);rs=rows(T);uf=nx.utils.UnionFind(range(len(T)));stats=dict(paid=0,unions=0,pins=0)
 def pin(j,v):
  if j in p and p[j]!=v:raise ValueError
  p[j]=v
 try:
  while True:
   old=len(p);same={}
   for j,v in p.items():
    k=uf[j]
    if k in same and same[k]!=v:raise ValueError
    same[k]=v
   for j in range(len(T)):
    if uf[j] in same:pin(j,same[uf[j]])
   active=[]
   for c,a,r in rs:
    ones=sum(p.get(j)==1 for j in r);free=[j for j in r if j not in p]
    if ones>1 or not ones and not free:raise ValueError
    if ones:
     for j in free:pin(j,0)
    elif len(free)==1:pin(free[0],1)
    else:active.append((c,a,free))
   if len(p)>old:continue
   eqrows=[]
   for c,a,r in active:
    roots=[uf[j] for j in r]
    for k in set(roots):
     if roots.count(k)>1:pin(k,0)
    eqrows.append(set(roots))
   if len(p)>old:continue
   # All active exact-one rows have RHS 1. Cancel shared pair, not an arbitrary projection.
   seen={};again=False
   for r in eqrows:
    for pair in I.combinations(sorted(r),2):
     k=next(iter(r-set(pair)),None)
     if pair in seen and seen[pair]!=k:
      z=seen[pair]
      if z is None or k is None:pin(k if z is None else z,0)
      else:uf.union(z,k);stats['unions']+=1
      again=True;break
     seen[pair]=k
    if again:break
   if again:continue
   # Components of actual active incidence. Curvature threshold summed only over these components.
   G=nx.Graph();G.add_edges_from((('t',j),('e',c,a)) for c,a,r in active for j in r)
   for comp in nx.connected_components(G):
    ids=sorted(v[1] for v in comp if v[0]=='t');cr=[(c,a,r) for c,a,r in active if ('e',c,a) in comp];parts=[{a for d,a,r in cr if d==c} for c in range(4)]
    if len({len(q) for q in parts})!=1:raise ValueError
    co={};weights=dict.fromkeys(ids,0)
    for c,a,r in cr:
     for j,k in I.combinations(sorted(r),2):co[j,k]=co.get((j,k),0)+1
    for (j,k),v in co.items():weights[j]+=max(0,v-1);weights[k]+=max(0,v-1)
    thresh=sum(len(r)==3 for c,a,r in cr)//2+4
    def feasible(a,b,on=None,off=None):
     stats['paid']+=1;L=set(parts[a]);R=set(parts[b]);base=0
     if on is not None:L.remove(T[on][a]);R.remove(T[on][b]);base=weights[on]
     H=nx.Graph();H.add_nodes_from((0,x) for x in L);H.add_nodes_from((1,x) for x in R)
     for j in ids:
      x,y=(0,T[j][a]),(1,T[j][b])
      if j!=off and x[1] in L and y[1] in R:
       w=weights[j] if weighted else 0
       if not H.has_edge(x,y) or H[x][y]['weight']<w:H.add_edge(x,y,weight=w)
     if weighted:
      M=nx.max_weight_matching(H,maxcardinality=True);return len(M)==len(L) and base+sum(H[x][y]['weight'] for x,y in M)>=thresh
     M=nx.bipartite.maximum_matching(H,top_nodes={(0,x) for x in L});return len(M)==2*len(L)
    for a,b in I.combinations(range(4),2):
     if not feasible(a,b):raise ValueError
     for j in ids:
      if not feasible(a,b,on=j):pin(j,0);break
      if not feasible(a,b,off=j):pin(j,1);break
     if len(p)>old:break
    if len(p)>old:break
   if len(p)==old:
    stats['pins']=len(p);return p,uf,eqrows,stats
 except ValueError:
  stats['pins']=len(p);return None,uf,[],stats

def make_event(T,p,uf,eqrows):
 classes={}
 for j in range(len(T)):
  if j not in p:classes.setdefault(uf[j],set()).add(j)
 H=nx.Graph();H.add_nodes_from(classes)
 for r in eqrows:
  assert r<=classes.keys();H.add_edges_from(I.combinations(sorted(r),2))
 return H,classes

def decompose(H):
 # Bounded search over cliques <=3 (all singletons, edges, triangles).
 bags=[];edges=[];checks=0
 def rec(V):
  nonlocal checks
  G=H.subgraph(V);S=None;parts=None
  if len(V)>1 and not nx.is_connected(G):S=set();parts=list(nx.connected_components(G))
  elif len(V)>2:
   for clique in I.chain(((v,) for v in sorted(V)),G.edges(),((u,v,w) for u,v in G.edges() for w in set(G[u])&set(G[v]) if u<v<w)):
    checks+=1;c=set(clique);rest=V-c
    if len(rest)>1 and not nx.is_connected(G.subgraph(rest)):
     S=c;parts=list(nx.connected_components(G.subgraph(rest)));break
  if S is None:
   bags.append(set(V));return [len(bags)-1]
  # binary split; each child is proper; duplicated intersection is a clique.
  A=S|parts[0];B=S|set().union(*parts[1:]);a=rec(A);b=rec(B)
  x=next(i for i in a if S<=bags[i]);y=next(i for i in b if S<=bags[i]);edges.append((x,y));return a+b
 if H:rec(set(H))
 tree=nx.Graph();tree.add_nodes_from(range(len(bags)));tree.add_edges_from(edges)
 if bags:
  assert nx.is_tree(tree)
  for v in H:assert nx.is_connected(tree.subgraph([i for i,B in enumerate(bags) if v in B]))
  assert all(any({u,v}<=B for B in bags) for u,v in H.edges())
 return bags,tree,checks

def atom(G,w,stats,cap=12):
 # Exact on a chordal graph via simplicial elimination, on line graphs via matching,
 # or bounded-size enumeration. UNKNOWN otherwise. Negative weights are legitimate.
 w=dict(w);A=G.copy();stack=[]
 while A:
  u=next((u for u in A if w[u]<=0 or all(A.has_edge(a,b) for a,b in I.combinations(A[u],2))),None)
  if u is None:break
  ns=set(A[u]);gain=max(0,w[u]);stack.append((u,ns,gain));A.remove_node(u)
  for v in ns:w[v]-=gain
 if not A:stats['simplicial']+=1;out=set()
 else:
  try:
   R=nx.inverse_line_graph(A);em={}
   for a,b in R.edges():
    z=set(a)&set(b);assert len(z)==1;u=next(iter(z));assert u not in em;em[u]=(a,b);R[a][b]['weight']=w[u]
   assert set(em)==set(A) and all(A.has_edge(a,b)==bool(set(em[a])&set(em[b])) for a,b in I.combinations(A,2))
   M=nx.max_weight_matching(R);out={u for u,(a,b) in em.items() if (a,b) in M or (b,a) in M};stats['line']+=1
  except (nx.NetworkXException,AssertionError,IndexError):
   if len(A)>cap:return None
   stats['enumerated']+=1;out=set();best=0
   for k in range(1,len(A)+1):
    for seq in I.combinations(A,k):
     z=sum(w[u] for u in seq)
     if z>best and not any(A.has_edge(a,b) for a,b in I.combinations(seq,2)):best=z;out=set(seq)
 for u,ns,gain in reversed(stack):
  if gain>0 and not ns&out:out.add(u)
 assert not any(G.has_edge(a,b) for a,b in I.combinations(out,2));return out

def join(H,w,cap=12):
 bags,tree,checks=decompose(H);stats=dict(bags=len(bags),maxbag=max(map(len,bags),default=0),separator_checks=checks,queries=0,simplicial=0,line=0,enumerated=0)
 if not bags:return set(),stats
 def dp(i,parent):
  B=bags[i];P=B&bags[parent] if parent is not None else set();child=[];local={u:w[u] if u not in P else 0 for u in B};base=0
  for j in tree[i]:
   if j==parent:continue
   C=B&bags[j];t=dp(j,i)
   if t is None:return None
   child.append((C,t));v=t[None][0];base+=v
   for u in C:local[u]+=t[u][0]-v
  table={}
  for a in [None]+sorted(P):
   allowed=B-P
   if a is not None:allowed=allowed-set(H[a])
   stats['queries']+=1;S=atom(H.subgraph(allowed),local,stats,cap)
   if S is None:return None
   chosen=S|({a} if a is not None else set());val=base+sum(local[u] for u in chosen);lift=set(chosen-P)
   for C,t in child:
    state=next(iter(C&chosen),None);lift|=t[state][1]
   assert sum(w[u] for u in lift)==val;assert not any(H.has_edge(u,v) for u,v in I.combinations(lift,2));table[a]=(val,lift)
  return table
 t=dp(0,None);return (None if t is None else t[None][1]),stats

def solve(T,guard=None,weighted=True,cap=12):
 guard=guard or {};assert len(T)%3==0 and len(set(T))==len(T) and all(len(r)==3 for c,a,r in rows(T)) and nx.check_planarity(graph(T))[0]
 p,uf,eqrows,stats=closure(T,guard,weighted)
 if p is None:return 'NO',stats,None
 H,classes=make_event(T,p,uf,eqrows);w={k:len(v) for k,v in classes.items()};S,more=join(H,w,cap);stats.update(more);stats.update(events=len(H),maxevent=max(w.values(),default=0))
 if S is None:return 'UNKNOWN',stats,None
 sel={j for j,v in p.items() if v}|set().union(*(classes[k] for k in S));assert len(sel)<=len(T)//3
 if len(sel)==len(T)//3:
  assert verify(T,sel) and all((j in sel)==bool(v) for j,v in guard.items());return 'YES',stats,sorted(sel)
 return 'NO',stats,None

def chain(k,bad=False):
 T=[tuple(v+6*b for v in t) for b in range(k) for t in (U if bad and b==k//2 else V)]
 for b in range(k-1):T=swap(T,18*b,18*(b+1),b%2)
 return T

def run():
 out=[];rng=random.Random(1803)
 for name,T in [('Q',Q),('U',U),('V',V),('W',W)]:
  for p in [{}]+[{j:v} for j in range(len(T)) for v in (0,1)]:
   truth=ref(T,p) is not None;r,s,w=solve(T,p);assert r=='UNKNOWN' or (r=='YES')==truth;out.append(dict(name=name,guard=p,truth=truth,result=r,**s))
 for k in [2,4,8,16,32]:
  for bad in [False,True]:
   T=chain(k,bad);r,s,w=solve(T,weighted=False);assert r=='UNKNOWN' or (r=='YES')==(not bad);out.append(dict(name=f'chain{k}_{bad}',truth=not bad,result=r,**s));print(out[-1],flush=True)
 json.dump(out,open('results.json','w'),indent=2);print('TOTAL',len(out),{r:sum(x['result']==r for x in out) for r in ['YES','NO','UNKNOWN']},'maxbag',max(x.get('maxbag',0) for x in out),'paid',sum(x['paid'] for x in out),flush=True)
if __name__=='__main__':run()
