import itertools as I, json, networkx as nx
from fractions import Fraction as F
from functools import lru_cache
P=[(0,15,0),(5,10,0),(3,12,1),(6,9,1)]
def parity(x):return x.bit_count()%2
def solve(rows,n):
 piv={}
 for a,b in rows:
  while a:
   k=a.bit_length()-1
   if k not in piv:piv[k]=(a,b);break
   a^=piv[k][0];b^=piv[k][1]
  if not a and b:return None
 free=[i for i in range(n) if i not in piv]
 def lift(x,aff):
  for i,(a,b) in sorted(piv.items()):
   if parity(a&x)^(b if aff else 0):x^=1<<i
  return x
 return lift(0,True),[lift(1<<i,False) for i in free]
def feat(x):
 a,b,c=[(x>>i)&1 for i in range(3)]
 return 1|a<<1|b<<2|c<<3|(a*b)<<4|(a*c)<<5|(b*c)<<6
def pr(x,ids):return sum(((x>>j)&1)<<i for i,j in enumerate(ids))
def local(S):
 if not S:return None
 p=parity(min(S))
 if any(parity(x)!=p for x in S):return None
 W={x^p for x in S};A=[(a,b,c) for a,b,c in P if a in W and b in W]
 if len(A)==1:return None
 if not A:return p,None
 # Choose one anchor from each side if possible, otherwise first two.
 u=A[0];v=next((v for v in A if v[2]!=u[2]),A[1]);a,b,c=u;d,e,f=v
 return p,(feat(a)^feat(b)^feat(d)^feat(e),1^c^f)
def local_weights(S,q):
 p,_=local(S);W={x^p for x in S};sign={x:parity(q&feat(x)) for x in W}
 A=[(a,b,(-1)**(c^sign[a]^sign[b])) for a,b,c in P if a in W and b in W]
 plus=sum(s==1 for _,_,s in A);minus=len(A)-plus
 assert not A or plus and minus
 w={x:(-1)**s for x,s in sign.items()}
 for a,b,s in A:w[a]*=minus if s==1 else plus
 assert w.get(0,0)*w.get(15,0)+w.get(5,0)*w.get(10,0)==w.get(3,0)*w.get(12,0)+w.get(6,0)*w.get(9,0)
 return {x^p:v for x,v in w.items()}
def gauge(S,ports,n):
 info=[local(s) for s in S]
 if any(x is None for x in info):return 'decline',None
 rows=[]
 for s,ids in zip(S,ports):
  a=min(s)
  for u in range(1,16):
   if all(not parity(u&(a^x)) for x in s):rows.append((sum(1<<j for i,j in enumerate(ids) if u>>i&1),parity(u&a)))
 ans=solve(rows,n)
 if ans is None:return 'inconsistent',None
 b0,B=ans;rows=[]
 for i,(p,anchor) in enumerate(info):
  if anchor:rows.append((anchor[0]<<(7*i),anchor[1]))
 def vector(x):return sum(feat(pr(x,ids)^p)<<(7*i) for i,(ids,(p,_)) in enumerate(zip(ports,info)))
 v0=vector(b0);v=[vector(b0^b) for b in B]
 for i,j in I.combinations(range(len(B)),2):rows.append((v0^v[i]^v[j]^vector(b0^B[i]^B[j]),0))
 ans=solve(rows,7*len(S))
 if ans is None:return 'decline',None
 q=ans[0];weights=[local_weights(s,(q>>(7*i))&127) for i,s in enumerate(S)]
 # On affine space total phase is affine; every actual word has corresponding sign.
 linear=[parity(q&(v0^a)) for a in v];const=parity(q&v0)
 if len(B)<=12:
  for k in range(1<<len(B)):
   x=b0
   for i,b in enumerate(B):
    if k>>i&1:x^=b
   s=const^sum(linear[i] for i in range(len(B)) if k>>i&1)%2
   assert s==parity(q&vector(x))
   w=1
   for f,ids in zip(weights,ports):w*=f.get(pr(x,ids),0)
   assert not w or w*(-1)**s>0
 return 'admit',{'free':len(B),'phase_coefficients':q.bit_count(),'weights':weights}
def gadget(w):
 a=min(w);flip=15^a;v={x^flip:F(y,w[a]) for x,y in w.items()};E={};ports=list(range(4));n=10
 def add(i,j,z):
  if z:E[tuple(sorted((i,j)))]=F(z)
 for i,j in [(0,1),(1,2),(2,3),(0,3)]:add(i,j,v.get(15^(1<<i)^(1<<j),0))
 for i,j,z in [(4,5,1),(4,8,1),(5,9,1),(8,9,-1),(8,7,1),(9,6,1),(7,6,1)]:add(i,j,z)
 for i in range(4):add(i,4+i,v.get(15^(1<<i)^(1<<(i+2)),0) if i<2 else 1)
 for i in range(4):
  if flip>>i&1:add(i,n,1);ports[i]=n;n+=1
 add(n,n+1,w[a]);n+=2
 return n,E,ports

def weighted_sum(E,n):
 adj=[[] for _ in range(n)]
 for (i,j),z in E.items():adj[i].append((j,z));adj[j].append((i,z))
 @lru_cache(None)
 def pm(mask):
  if not mask:return F(1)
  i=(mask&-mask).bit_length()-1;rem=mask^(1<<i)
  return sum((z*pm(rem^(1<<j)) for j,z in adj[i] if rem>>j&1),F(0))
 return pm((1<<n)-1)

def strict_graph(weights,rev):
 n,E,p=gadget(weights[0]);m,H,r=gadget(weights[1]);E.update({(a+n,b+n):z for (a,b),z in H.items()})
 expected={x:weights[0].get(x,0)*weights[1].get(pr(x,rev),0) for x in range(16)}
 q,c=next((q,c) for q in range(16) for c in range(2) if all(not w or (-1)**(parity(q&x)^c)*w>0 for x,w in expected.items()))
 for i,j in enumerate(rev):E[tuple(sorted((p[j],n+r[i])))]=F((-1)**((q>>j)&1))
 G=nx.Graph();G.add_nodes_from(range(n+m));G.add_edges_from(E);assert nx.check_planarity(G)[0]
 z=weighted_sum(E,n+m)*(-1)**c;assert z==sum(abs(w) for w in expected.values())
 return {'graph_vertices':n+m,'linear_character':q,'constant_sign':c,'positive_weighted_sum':int(z)}
Q=[(0,0,1),(0,1,0),(0,1,1),(1,0,0),(1,0,1),(1,1,0)]
def source(k):
 T=[list(2*i+x for x in t) for i in range(k) for t in Q]
 for i in range(k):
  a=6*i+1;b=6*((i+1)%k);T[a][0],T[b][0]=T[b][0],T[a][0]
 return list(map(tuple,T))
def acquire(k,pins):
 T=source(k);G=nx.Graph();G.add_edges_from((('t',i),(c,v)) for i,t in enumerate(T) for c,v in enumerate(t));ok,emb=nx.check_planarity(G);assert ok and nx.is_connected(G) and len(T)==len(set(T))
 assert all({t[c] for t in T}==set(range(2*k)) for c in range(3))
 tabs=[];ports=[]
 for i in range(k):
  R={('t',6*i+j) for j in range(6)}|{(c,2*i+j) for c in range(3) for j in range(2)}
  cut=[(u,v) if u[0]=='t' else (v,u) for u,v in G.edges() if (u in R)!=(v in R)];assert len(cut)==4
  t,e=cut[0];start=(t,e) if t in R else (e,t);cur=start;order=[]
  for _ in range(2*G.number_of_edges()+5):
   a,b=cur
   if b not in R:order.append((a,b) if a[0]=='t' else (b,a));cur=(b,a)
   else:cur=(b,emb[b][a]['cw'])
   if cur==start:break
  assert len(order)==4;ports.append([t[1] for t,e in order]);tab={}
  for x in range(64):
   if any((x>>(j%6)&1)!=v for j,v in pins.items() if j//6==i):continue
   for b in range(16):
    w=dict(zip(order,[(b>>a)&1 for a in range(4)]))
    if any(t in R and w[t,e]!=(x>>(t[1]%6)&1) for t,e in order):continue
    if any(t[1] in pins and w[t,e]!=pins[t[1]] for t,e in order):continue
    if all(sum((x>>(t[1]%6)&1) if t in R else w[t,v] for t in G[v])==1 for v in R if v[0]!='t'):tab[b]=[6*i+j for j in range(6) if x>>j&1]
  tabs.append(tab)
 return T,tabs,ports

def closure(T,n,deleted):
 # Exact-one propagation and indexed pairwise matching-support via SCC.
 state={j:0 for j in deleted};m=len(T);calls=0
 while True:
  old=len(state)
  for c in range(3):
   for v in range(n):
    ids=[j for j,t in enumerate(T) if t[c]==v];one=[j for j in ids if state.get(j)==1];free=[j for j in ids if j not in state]
    if len(one)>1 or not one and not free:return 'NO',calls,state
    if one:
     for j in free:state[j]=0
    elif len(free)==1:state[free[0]]=1
  for a,b in I.combinations(range(3),2):
   # Selected triple pins remove conflicting candidates before projections.
   one=[j for j,v in state.items() if v==1]
   for j,t in enumerate(T):
    if j in state:continue
    if any(any(t[c]==T[i][c] for c in range(3)) for i in one):state[j]=0
   L=[(a,v) for v in range(n)];R=[(b,v) for v in range(n)];H=nx.Graph();H.add_nodes_from(L+R);H.add_edges_from(((a,t[a]),(b,t[b])) for j,t in enumerate(T) if state.get(j)!=0)
   M=nx.bipartite.maximum_matching(H,top_nodes=L);calls+=1
   if len(M)!=2*n:return 'NO',calls,state
   D=nx.DiGraph();D.add_nodes_from(L+R)
   for u,v in H.edges:
    if u[0]!=a:u,v=v,u
    D.add_edge(u,v)
    if M[u]==v:D.add_edge(v,u)
   comp={v:i for i,C in enumerate(nx.strongly_connected_components(D)) for v in C}
   for j,t in enumerate(T):
    if state.get(j)==0:continue
    u,v=(a,t[a]),(b,t[b])
    if comp[u]!=comp[v]:
     if state.get(j)==1:return 'NO',calls,state
     state[j]=0
  if len(state)==old:return ('YES' if len(state)==m else 'OPEN'),calls,state

def ring(k,deleted):
 T=source(k);cl,calls,pins=closure(T,2*k,deleted)
 # Independently evaluate the originally guarded masks even when closure rejects.
 T,tabs,ports=acquire(k,{j:0 for j in deleted} if cl=='NO' else pins)
 def pair(i):return (6*(i%k)+1,6*((i+1)%k))
 witness=None
 for s in range(4):
  states={s:[]}
  for i in range(k):
   new={}
   for b,w in tabs[i].items():
    z={t:(b>>j)&1 for j,t in enumerate(ports[i])};left=sum(z[t]<<j for j,t in enumerate(pair(i-1)));right=sum(z[t]<<j for j,t in enumerate(pair(i)))
    if left in states:new[right]=states[left]+w
   states=new
  if s in states:witness=states[s];break
 if witness is not None:assert len(witness)==2*k and all(len({T[j][c] for j in witness})==2*k for c in range(3)) and not set(witness)&set(deleted)
 assert cl!='NO' or witness is None
 # compress global wire IDs to remove unused free bits
 wires=sorted({j for p in ports for j in p});ids=[[wires.index(j) for j in p] for p in ports]
 status,data=gauge([set(t) for t in tabs],ids,len(wires))
 if status=='inconsistent':assert witness is None
 return {'k':k,'triples':len(T),'deleted':list(deleted),'closure':cl,'matching_calls':calls,'closure_pins':len(pins),'gauge':status,'witness':witness is not None,'free':None if data is None else data['free']}
if __name__=='__main__':
 # all fixed-parity local masks and all quadratic phases: anchor satisfaction iff the selected two terms have opposite signs.
 tested=admitted=0
 for p in (0,1):
  W=[x for x in range(16) if parity(x)==p]
  for m in range(1,256):
   S={x for i,x in enumerate(W) if m>>i&1};v=local(S)
   if v is None:continue
   admitted+=1
   for q in range(128):
    if v[1] and parity(q&v[1][0])!=v[1][1]:continue
    local_weights(S,q);tested+=1
 # Strict rank-zero improvement over canonical twist for five-word mask (full affine hull).
 S={0,3,5,10,15};E={x for x in range(16) if not parity(x)};rev=[0,3,2,1]
 s,data=gauge([S,{pr(x,rev) for x in E}],[[0,1,2,3],rev],4);assert s=='admit' and data['free']==3
 assert all((sum(1 for x in S if x==y)>0) for y in S)
 # Verify the explicit canonical sign nonaffine on the full 3-dimensional parity chart.
 assert parity(3)==0 and ((0&3)==3)^((5&3)==3)^((10&3)==3)^((15&3)==3)
 out={'local_masks_admitted':admitted,'anchored_signatures_checked':tested,'abstract_strict_control':{'status':s,'free':data['free'],'weights':data['weights'],'canonical_rank':2,'selected_rank':0,**strict_graph(data['weights'],rev)},'source':[]}
 for k in (2,4,8,16,32,64):
  for d in ((),(0,1),(0,1,2)):
   r=ring(k,d);assert r['witness']==(len(d)<3);out['source'].append(r)
 print(json.dumps(out,indent=2))
