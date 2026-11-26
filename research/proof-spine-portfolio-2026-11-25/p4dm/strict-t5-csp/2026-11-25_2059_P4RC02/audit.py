import itertools as I, json, random, networkx as nx
Q=[t for t in I.product(range(2),repeat=4) if sum(t)==2]
U=[(3,5,0,0),(2,0,4,2),(1,1,2,2),(0,5,1,3),(1,4,2,4),(5,0,4,5),(3,2,5,0),(0,4,2,2),(5,3,4,1),(4,2,0,0),(4,2,5,1),(0,4,1,4),(5,3,3,5),(2,1,3,3),(3,3,5,3),(2,0,3,5),(4,5,0,1),(1,1,1,4)]
V=[(0,0,5,1),(0,1,0,1),(0,1,1,0),(1,0,0,1),(1,0,1,0),(1,1,0,0),(2,2,3,3),(2,3,2,3),(2,4,3,2),(3,2,2,3),(3,2,3,2),(3,3,2,2),(4,3,5,5),(4,5,4,5),(4,5,5,4),(5,4,4,5),(5,4,1,4),(5,5,4,4)]
def swap(T,a,b,c):
 T=list(T);p,q=list(T[a]),list(T[b]);p[c],q[c]=q[c],p[c];T[a],T[b]=tuple(p),tuple(q);return T
W=swap(U,1,14,3)
def graph(T):
 G=nx.Graph();G.add_edges_from((('t',j),('e',i,v)) for j,t in enumerate(T) for i,v in enumerate(t));return G
def clauses(T):return [tuple(j for j,t in enumerate(T) if t[c]==a) for c in range(4) for a in range(len(T)//3)]
def verify(T,sel):return all(sum(j in sel for j in c)==1 for c in clauses(T))
def ref(T):
 cs=clauses(T);by=[set() for t in T]
 for k,c in enumerate(cs):
  for j in c:by[j].add(k)
 def f(left):
  if not left:return []
  k=min(left,key=lambda k:sum(by[j]<=left for j in cs[k]))
  for j in cs[k]:
   if by[j]<=left:
    x=f(left-by[j]);
    if x is not None:return [j]+x
  return None
 return f(set(range(len(cs))))
def closure(T,p=None):
 p=dict(p or {});cs=clauses(T);calls=0;n=len(T)//3
 while True:
  old=len(p)
  for c in cs:
   ones=sum(p.get(j)==1 for j in c);free=[j for j in c if j not in p]
   if ones>1 or (not ones and not free):return None,calls
   if ones:p.update((j,0) for j in free)
   elif len(free)==1:p[free[0]]=1
  if len(p)>old:continue
  free=[j for j in range(len(T)) if j not in p];selected=[j for j in p if p[j]]
  for a,b in I.combinations(range(4),2):
   L=set(range(n))-{T[j][a] for j in selected};R=set(range(n))-{T[j][b] for j in selected}
   def match(force=None):
    nonlocal calls
    calls+=1;l=set(L);r=set(R)
    if force is not None:l.remove(T[force][a]);r.remove(T[force][b])
    g=nx.Graph();g.add_nodes_from((0,x) for x in l);g.add_nodes_from((1,x) for x in r);g.add_edges_from(((0,T[j][a]),(1,T[j][b])) for j in free if T[j][a] in l and T[j][b] in r)
    return len(nx.bipartite.maximum_matching(g,top_nodes={(0,x) for x in l}))==2*len(l)
   if not match():return None,calls
   for j in free:
    if not match(j):p[j]=0;break
   if len(p)>old:break
  if len(p)==old:return p,calls

def acquire(T,p,E):
 seen=set();faces=[]
 for u,v in E.edges():
  if (u,v) not in seen:
   f=E.traverse_face(u,v,seen)
   if len(f)==4 and len(set(f))==4:faces.append(f)
 G=graph(T);q=nx.Graph();q.add_nodes_from(range(len(faces)));own={}
 for i,f in enumerate(faces):
  for a,b in zip(f,f[1:]+f[:1]):
   e=frozenset((a,b))
   if e in own:q.add_edge(i,own[e])
   own[e]=i
 cs={v:tuple(sorted(w[1] for w in G[v])) for v in G if v[0]=='e'};parts=[{v for i in comp for v in faces[i] if v[0]=='e'} for comp in nx.connected_components(q)];covered=set().union(*parts) if parts else set();parts += [{v} for v in cs if v not in covered];rows=[]
 for els in parts:
  C=[cs[e] for e in sorted(els)];scope=set().union(*map(set,C));group=[]
  for j in C[0]:
   d={k:int(k==j) for k in C[0]}
   if any(p.get(k,v)!=v for k,v in d.items()):continue
   d.update({k:v for k,v in p.items() if k in scope});bad=False
   while True:
    old=len(d)
    for c in C:
     ones=sum(d.get(k)==1 for k in c);free=[k for k in c if k not in d]
     if ones>1 or not ones and not free:bad=True;break
     if ones:d.update((k,0) for k in free)
     elif len(free)==1:d[free[0]]=1
    if bad or old==len(d):break
   if not bad:
    assert set(d)==scope;group.append(d)
  rows.append(group)
 return rows

def solve(T,guard=None, use_matching=True):
 G=graph(T);ok,E=nx.check_planarity(G);assert ok and len(set(T))==len(T) and all(len(c)==3 for c in clauses(T))
 p,calls=closure(T,guard) if use_matching else (dict(guard or {}),0)
 stat=dict(matching=calls,groups=0,deleted=0,pruned=0,rainbow_checks=0,pc_checks=0,pins=0,blocked=0,core=0)
 if p is None:return 'NO',stat,None
 stat['pins']=len(p);rows=acquire(T,p,E);stat['groups']=len(rows);n=len(rows)
 if any(not r for r in rows):return 'NO',stat,None
 # Direct exact binary CSP: all groups, with equality on actual shared tuple IDs.
 D={i:set(range(len(r))) for i,r in enumerate(rows)};R={}
 for i,j in I.permutations(D,2):
  R[i,j]={(a,b) for a in D[i] for b in D[j] if all(rows[j][b].get(k,v)==v for k,v in rows[i][a].items())}
 # path consistency with domain pruning and retained pair relations, all under same guard
 def pc():
  while True:
   changed=False
   for i in D:
    for a in tuple(D[i]):
     if any(not any((a,b) in R[i,j] for b in D[j]) for j in D if j!=i):D[i].remove(a);stat['pruned']+=1;changed=True
    if not D[i]:return False
   for i,j in I.combinations(D,2):
    r=R[i,j];keep=set()
    for a,b in r:
     if a not in D[i] or b not in D[j]:continue
     good=True
     for k in D:
      if k==i or k==j:continue
      stat['pc_checks']+=1
      if not any((a,c) in R[i,k] and (b,c) in R[j,k] for c in D[k]):good=False;break
     if good:keep.add((a,b))
    if keep!=r:stat['pruned']+=len(r)-len(keep);changed=True;R[i,j]=keep;R[j,i]={(b,a) for a,b in keep}
    if not keep:return False
   if not changed:return True
 stack=[]
 while D:
  if not pc():return 'NO',stat,None
  # Every retained source model must use a live row. Pay for source reclosure.
  inferred={}
  for i,ds in D.items():
   for j in rows[i][next(iter(ds))]:
    vals={rows[i][a][j] for a in ds}
    if len(vals)==1 and j not in p:
     v=next(iter(vals));assert inferred.get(j,v)==v;inferred[j]=v
  if inferred:
   p.update(inferred);p,newcalls=closure(T,p);stat['matching']+=newcalls
   if p is None:return 'NO',stat,None
   stat['pins']=len(p)
   for i,ds in D.items():
    ds.intersection_update(a for a in tuple(ds) if all(p.get(j,v)==v for j,v in rows[i][a].items()))
    if not ds:return 'NO',stat,None
   continue
  # exact safe-elimination test: pairwise compatible triple of singleton vetoes
  chosen=None;obstructions={}
  for k in D:
   if len(D[k])<=2:chosen=k;break
   veto={a:[] for a in D[k]}
   for i in D:
    if i==k:continue
    for a in D[i]:
     missing=D[k]-{b for b in D[k] if (a,b) in R[i,k]}
     if len(missing)==1:veto[next(iter(missing))].append((i,a))
   obstruction=None
   for u,v,w in I.product(*veto.values()):
    stat['rainbow_checks']+=1
    if len({u[0],v[0],w[0]})==3 and all((a[1],b[1]) in R[a[0],b[0]] for a,b in I.combinations((u,v,w),2)):
     obstruction=(u,v,w);break
   if obstruction is None:chosen=k;break
   obstructions[k]=obstruction;stat['blocked']+=1
  if chosen is None:stat['core']=len(D);return 'UNKNOWN',stat,dict(core={str(k):sorted(v) for k,v in D.items()},obstructions=obstructions)
  k=chosen;stack.append((k,set(D[k]),{i:set(R[k,i]) for i in D if i!=k}));del D[k];stat['deleted']+=1
  for i in D:del R[i,k];del R[k,i]
 sel={}
 for k,ds,rs in reversed(stack):
  sel[k]=next(a for a in ds if all((a,b) in rs[i] for i,b in sel.items()))
 decoded=dict(p)
 for k,a in sel.items():
  for j,v in rows[k][a].items():assert decoded.get(j,v)==v;decoded[j]=v
 witness=[j for j,v in decoded.items() if v];assert verify(T,witness) and all(decoded[j]==v for j,v in (guard or {}).items())
 return 'YES',stat,witness

def chain(k,mid=False):
 T=[tuple(v+6*b for v in t) for b in range(k) for t in (U if mid and b==k//2 else V)]
 for b in range(k-1):T=swap(T,18*b,18*(b+1),b%2)
 return T
def star():
 T=[tuple(v+2*b for v in t) for b in range(4) for t in Q]
 for i in range(3):T=swap(T,i,6*(i+1),i)
 return T
if __name__=='__main__':
 tests=[];rng=random.Random(105)
 for name,T in [('Q',Q),('U',U),('V',V),('W',W),('star',star())]+[(f'{kind}{k}',chain(k,kind=='NO')) for k in [2,4,8,16] for kind in ['YES','NO']]:
  truth=ref(T) is not None if len(T)<=24 else not name.startswith('NO');out,s,cert=solve(T);assert out=='UNKNOWN' or (out=='YES')==truth;tests.append(dict(name=name,tuples=len(T),truth=truth,out=out,**s));print(tests[-1],flush=True)
 # random walk of planar degree-preserving swaps on known genuine inputs
 sample=[];T=list(V);accepted=0;unknown=None
 for trial in range(5000):
  a,b=rng.sample(range(len(T)),2);S=swap(T,a,b,rng.randrange(4))
  if S==T or len(set(S))!=len(S) or not nx.check_planarity(graph(S))[0]:continue
  T=S;accepted+=1
  if accepted%3:continue
  truth=ref(T) is not None;out,s,cert=solve(T);assert out=='UNKNOWN' or (out=='YES')==truth;sample.append(dict(trial=trial,truth=truth,out=out,**s))
  if out=='UNKNOWN' and unknown is None:unknown=dict(T=T,truth=truth,cert=cert)
 print('walk',accepted,len(sample),'unknown',unknown,flush=True)
 json.dump(dict(tests=tests,random=sample,accepted=accepted,unknown=unknown),open('results.json','w'),indent=2)
