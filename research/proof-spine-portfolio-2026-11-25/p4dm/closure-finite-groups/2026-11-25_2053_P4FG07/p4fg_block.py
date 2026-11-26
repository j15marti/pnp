from p4fg07 import *
# Block-cut solver for signed exactly-one rows. Reconstruct exact original event word.
def block_match(edges,rows,vmask,rmask):
 occ=defaultdict(list);G=nx.Graph();mandatory=set();ports={};x={};slot={}
 # rows[j] is sign of each edge. rmask gives allowed number of true ports, subset {0,1}.
 for j,A in rmask.items():
  if not A:return None
  if 1 in A:
   slot[j]=('r',j);G.add_node(slot[j])
   if 0 not in A:mandatory.add(slot[j])
 for i,j,c in edges:occ[i].append((j,c))
 for i,L in occ.items():
  if len(L)>2 and len(vmask[i])>1:raise ValueError('nonmatching block')
  if len(vmask[i])==1:
   x[i]=next(iter(vmask[i]))
   for a,(j,c) in enumerate(L):
    if x[i]^(c<0):
     p=('p',i,a);mandatory.add(p);G.add_node(p)
     if j in slot:G.add_edge(p,slot[j])
   continue
  if not vmask[i]:return None
  for a,(j,c) in enumerate(L):
   p=('p',i,a);mandatory.add(p);G.add_node(p)
   if j in slot:G.add_edge(p,slot[j])
  if len(L)==1:G.add_edge(('p',i,0),('optional',i))
  elif L[0][1]==L[1][1]:G.add_edge(('p',i,0),('p',i,1))
  else:
   d=('d',i);mandatory.add(d);G.add_edge(d,('p',i,0));G.add_edge(d,('p',i,1))
 G.add_nodes_from(mandatory)
 for a,b in G.edges():G[a][b]['weight']=int(a in mandatory)+int(b in mandatory)
 M=nx.max_weight_matching(G);mate={a:b for u,v in M for a,b in [(u,v),(v,u)]}
 if not mandatory<=mate.keys():return None
 for i,L in occ.items():
  if i not in x:
   val=[int(mate[('p',i,a)][0]=='r')^(c<0) for a,(j,c) in enumerate(L)];assert len(set(val))==1;x[i]=val[0]
 for j,A in rmask.items():assert sum(x[i]^(c<0) for i,k,c in edges if k==j) in A
 return x

def block_solver(R,k,cap=0):
 # R signed linear row representation. Require exactly-one literal row, after normalization.
 H=nx.Graph();coeff={};rlist={}
 for j,(d,b) in enumerate(R):
  if any(abs(c)!=1 for i,c in d) or b+sum(c<0 for i,c in d)!=1:return 'UNKNOWN',None,{}
  rlist[j]=d
  for i,c in d:H.add_edge(('v',i),('r',j));coeff[i,j]=c
 B=[list(E) for E in nx.biconnected_component_edges(H)];A=set(nx.articulation_points(H));tree=nx.Graph();data={};stats={'blocks':len(B),'articulations':len(A),'max_block_var_degree':0,'matching_calls':0,'max_exceptions':0}
 for b,L in enumerate(B):
  node=('b',b);tree.add_node(node);vs=set();edges=[];occ=Counter()
  for u,v in L:
   if u[0]=='r':u,v=v,u
   i,j=u[1],v[1];vs.update((u,v));edges.append((i,j,coeff[i,j]));occ[i]+=1
  stats['max_block_var_degree']=max(stats['max_block_var_degree'],max(occ.values(),default=0));data[node]=(vs,edges)
  ex=sum(v>2 for v in occ.values());stats['max_exceptions']=max(stats['max_exceptions'],ex)
  if ex>cap:return 'UNKNOWN',None,stats
  for u in vs&A:tree.add_edge(node,u)
 memo={};parents={};orders=[]
 for C in nx.connected_components(tree):
  root=min(u for u in C if u[0]=='b');order=list(nx.dfs_preorder_nodes(tree,root));orders.append(order);parents[root]=None
  for u,v in nx.dfs_edges(tree,root):parents[v]=u
  for u in reversed(order):
   p=parents[u];ch=[v for v in tree[u] if v!=p]
   if u[0]=='v':
    mask={0,1}
    for v in ch:mask&=set(memo[v])
    memo[u]={a:[a]*len(ch) for a in mask}
   elif u[0]=='r':
    # exact total 1 at articulation row; child blocks contribute at most 1 each.
    possible={0:[]}
    for v in ch:
     possible={a+b:w+[b] for a,w in possible.items() for b in memo[v] if a+b<=1}
    memo[u]={1-a:w for a,w in possible.items()}
   else:
    vs,edges=data[u];basev={i:{0,1} for t,i in vs if t=='v'};baser={j:{1} for t,j in vs if t=='r'}
    for v in ch:
     (basev if v[0]=='v' else baser)[v[1]]=set(memo[v])
    memo[u]={}
    for a in ([0,1] if p else [None]):
     vm={i:set(S) for i,S in basev.items()};rm={j:set(S) for j,S in baser.items()}
     if p:(vm if p[0]=='v' else rm)[p[1]]={a}
     if any(not S for S in vm.values()) or any(not S for S in rm.values()):continue
     occ=Counter(i for i,j,c in edges);exc=[i for i in vm if occ[i]>2 and len(vm[i])>1]
     for v in it.product([0,1],repeat=len(exc)):
      vv=vm|{i:{b} for i,b in zip(exc,v)}
      stats['matching_calls']+=1;w=block_match(edges,rlist,vv,rm)
      if w is not None:memo[u][a]=w;break
  if None not in memo[root]:return 'NO',None,stats
 x=[0]*k;assigned={}
 for order in orders:
  arg={order[0]:None}
  for u in order:
   ch=[v for v in tree[u] if v!=parents[u]];a=arg[u];w=memo[u][a]
   if u[0]=='b':
    for i,b in w.items():
     if i in assigned:assert assigned[i]==b
     assigned[i]=b;x[i]=b
    vs,edges=data[u]
    for v in ch:
     arg[v]=w[v[1]] if v[0]=='v' else sum(w[i]^(c<0) for i,j,c in edges if j==v[1])
   else:
    for v,b in zip(ch,w):arg[v]=b
 assert all(sum(c*x[i] for i,c in d)==b for d,b in R)
 return 'YES',x,stats

def solve2(T,n,pins=None):
 G,E=source(T,n);rows,groups,covered=quad(T,n,E);stats={'groups':len(groups),'maxstates':max((len(s) for _,s,_ in groups),default=0),'covered':len(covered)}
 P,A=closure(T,n,rows,pins);stats['pins']=len(P) if P is not None else -1
 if P is None:return 'NO',None,stats|{'stage':'closure'}
 Q=event_quotient(T,n,rows,groups,covered,P,A)
 if Q is None:return 'NO',None,stats|{'stage':'local'}
 R,expr,k=Q;stats['rows']=len(R);stats['vars']=k;stats['maxocc_before']=max(Counter(i for d,b in R for i,c in d).values(),default=0)
 # Rational basis optional. Try unreduced first; then exact row-basis fallback if needed.
 ans,x,st=block_solver(R,k);stats|=st
 if ans=='UNKNOWN':
  S=reduce_rows(R);ans,x,st=block_solver(S,k);stats|=st;stats['basis']=len(S)
 if ans=='YES':
  assert all(sum(c*x[i] for i,c in d)==b for d,b in R)
  W=[j for j,(i,b) in expr.items() if (x[i] if i is not None else 0)^b];assert verify(T,n,W);assert all(int(j in W)==b for j,b in P.items())
  return ans,W,stats|{'stage':'blockmatching'}
 return ans,None,stats|{'stage':'blockmatching'}

def audit2():
 rng=random.Random(318);counts=Counter();samples=[];abstract=Counter();unknown=None
 for label,T,n in [('U',U,6),('V',V,6),('cube',CUBE,2)]:
  a,w,s=solve2(T,n);truth=brute(T,n);assert a=='UNKNOWN' or (a=='YES')==(truth is not None);samples.append({'name':label,'status':a,'witness':w,'stats':s,'truth':truth is not None})
 for k in [2,4,8,16,32]:
  T,n=chain(k);a,w,s=solve2(T,n);assert a=='YES' and verify(T,n,w);samples.append({'name':f'cube-chain-{k}','status':a,'stats':s})
 for T,n in [(U,6),(V,6),(CUBE,2)]:
  for j in range(len(T)):
   for b in [0,1]:
    a,w,s=solve2(T,n,{j:b});truth=any(verify(T,n,list(L)) for L in it.combinations(range(len(T)),n) if (j in L)==bool(b));assert a=='UNKNOWN' or (a=='YES')==truth;counts['guard_'+a]+=1
 # Random signed exact-one rows: arbitrary shared hubs, compare exact matching-block result with brute force.
 for _ in range(500):
  r=rng.randrange(1,8);k=rng.randrange(1,10);R=[]
  for j in range(r):
   d=tuple(sorted((i,rng.choice([-1,1])) for i in rng.sample(range(k),rng.randrange(1,min(k,3)+1))));R.append((d,1-sum(c<0 for i,c in d)))
  a,x,s=block_solver(R,k);truth=any(all(sum(c*y[i] for i,c in d)==b for d,b in R) for y in it.product([0,1],repeat=k));assert a=='UNKNOWN' or (a=='YES')==truth;abstract[a]+=1
 # Planar switch walk on 3 cubes.
 T,n=chain(3)
 for _ in range(600):
  i,j=rng.sample(range(len(T)),2);c=rng.randrange(4);S=swap(T,i,j,c)
  if len(set(S))!=len(S) or not nx.check_planarity(graph(S,n))[0] or not nx.is_connected(graph(S,n)):continue
  T=S;a,w,s=solve2(T,n);truth=brute(T,n) is not None;assert a=='UNKNOWN' or (a=='YES')==truth;counts['source_'+a]+=1
  if a=='UNKNOWN' and unknown is None:unknown={'truth':truth,'T':T,'stats':s}
 # Direct abstract prime obstruction: K3,3 incidence with all 3 event rows identical is deduplicable; instead Fano rows.
 R=[(tuple((i,1) for i in sorted([j,(j+1)%7,(j+3)%7])),1) for j in range(7)]
 a,x,s=block_solver(R,7);assert a=='UNKNOWN';samples.append({'name':'abstract Fano (not P4DM)','status':a,'stats':s,'truth':any(all(sum(c*y[i] for i,c in d)==b for d,b in R) for y in it.product([0,1],repeat=7))})
 print(json.dumps({'networkx':nx.__version__,'samples':samples,'counts':counts,'abstract':abstract,'first_unknown':unknown},indent=2))
if __name__=='__main__':audit2()
