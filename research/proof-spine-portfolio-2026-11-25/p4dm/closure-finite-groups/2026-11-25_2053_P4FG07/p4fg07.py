import itertools as it,random,json,networkx as nx
from fractions import Fraction
from collections import Counter,defaultdict
CUBE=[(0,0,0,0),(1,1,1,1),(0,0,1,1),(1,1,0,0),(0,1,0,1),(1,0,1,0)]
U=[(0,2,3,0),(1,3,4,5),(0,2,0,4),(3,5,3,3),(3,5,0,4),(1,1,4,2),(2,1,2,2),(5,3,1,1),(2,1,4,3),(1,0,2,2),(2,0,2,3),(3,0,0,5),(4,4,1,1),(5,3,5,0),(4,4,5,0),(0,5,3,4),(4,2,1,5),(5,4,5,1)]
def swap(T,i,j,c):
 A=list(T);a,b=list(A[i]),list(A[j]);a[c],b[c]=b[c],a[c];A[i],A[j]=tuple(a),tuple(b);return A
V=swap(U,0,11,1)
def graph(T,n):
 G=nx.Graph();G.add_nodes_from(range(4*n+len(T)));G.add_edges_from((4*n+j,c*n+v) for j,t in enumerate(T) for c,v in enumerate(t));return G
def source(T,n):
 assert len(T)==3*n and len(set(T))==len(T)
 G=graph(T,n);assert all(G.degree(v)==3 for v in range(4*n));assert all(G.degree(v)==4 for v in range(4*n,len(G)))
 ok,E=nx.check_planarity(G);assert ok;E.check_structure();return G,E
def brute(T,n):
 groups=[[j for j,t in enumerate(T) if t[0]==i] for i in range(n)]
 def rec(i,used):
  if i==n:return []
  for j in groups[i]:
   t=T[j]
   if all(not(used[k]>>t[k+1]&1) for k in range(3)):
    r=rec(i+1,[used[k]|1<<t[k+1] for k in range(3)])
    if r is not None:return [j]+r
  return None
 return rec(0,[0]*3)
def verify(T,n,w):return len(w)==n and all({T[j][c] for j in w}==set(range(n)) for c in range(4))
def quad(T,n,E):
 m=len(T);faces=[];seen=set()
 for u,v in E.edges():
  if (u,v) not in seen:
   f=E.traverse_face(u,v,seen)
   if len(f)==4:faces.append(f)
 Q=nx.Graph();Q.add_nodes_from(range(len(faces)));own=defaultdict(list)
 for i,f in enumerate(faces):
  for a,b in zip(f,f[1:]+f[:1]):own[tuple(sorted((a,b)))].append(i)
 for L in own.values():Q.add_edges_from(it.combinations(L,2))
 rows=[tuple(j for j,t in enumerate(T) if t[c]==v) for c in range(4) for v in range(n)]
 groups=[];covered=set()
 for C in nx.connected_components(Q):
  R=sorted({v for i in C for v in faces[i] if v<4*n});covered.update(R);L=[rows[i] for i in R];scope=sorted(set().union(*map(set,L)));a=L[0];states=[]
  for pick in a:
   s={v:int(v==pick) for v in a}
   while True:
    old=len(s);bad=False
    for r in L:
     q=sum(s.get(v,0) for v in r);z=[v for v in r if v not in s]
     if q>1 or (not z and q!=1):bad=True;break
     if q==1:s.update((v,0) for v in z)
     elif len(z)==1:s[z[0]]=1
    if bad or len(s)==old:break
   if not bad:
    assert set(s)==set(scope);states.append(s)
  assert all(sum(s[v] for s in states)<=1 for v in scope)
  groups.append((scope,states,R))
 return rows,groups,covered
# Affine GF2 full tuple closure with pair support and exact-one propagation.
def affine(m,eq):
 B={}
 for a,b in eq:
  while a:
   p=a.bit_length()-1
   if p not in B:B[p]=(a,b);break
   x,y=B[p];a^=x;b^=y
  if not a and b:return None
 sig=[]
 for i in range(m):
  a=1<<i;b=0
  for p in sorted(B,reverse=True):
   if a>>p&1:x,y=B[p];a^=x;b^=y
  sig.append((a,b))
 return sig
def pair_support(T,n,pins):
 L=[j for j in range(len(T)) if pins.get(j)!=0];bad=set()
 for a,b in it.combinations(range(4),2):
  G=nx.Graph();G.add_nodes_from(range(2*n));G.add_edges_from((T[j][a],n+T[j][b]) for j in L)
  M=nx.algorithms.bipartite.maximum_matching(G,top_nodes=set(range(n)))
  if len(M)!=2*n:return None
  D=nx.DiGraph();D.add_nodes_from(range(n));D.add_edges_from((T[j][a],M[n+T[j][b]]) for j in L)
  comp={v:i for i,C in enumerate(nx.strongly_connected_components(D)) for v in C}
  bad.update(j for j in L if comp[T[j][a]]!=comp[M[n+T[j][b]]])
 return bad
def closure(T,n,rows,initial=None):
 pins=dict(initial or {});m=len(T)
 def put(j,b):
  if j in pins and pins[j]!=b:return False
  pins[j]=b;return True
 while True:
  old=len(pins);A=affine(m,[(sum(1<<j for j in r),1) for r in rows]+[(1<<j,b) for j,b in pins.items()])
  if A is None:return None,None
  for j,(a,b) in enumerate(A):
   if not a and not put(j,b):return None,None
  for r in rows:
   if sum(pins.get(j,0) for j in r)>1:return None,None
   if any(pins.get(j)==1 for j in r):
    for j in r:
     if pins.get(j)!=1 and not put(j,0):return None,None
   else:
    K=[j for j in r if pins.get(j)!=0]
    if not K:return None,None
    if len(K)==1 and not put(K[0],1):return None,None
    # Same/opposite affine classes in a row give exact integer forced bits.
    for i,j in it.combinations(r,2):
     if A[i][0] and A[i][0]==A[j][0]:
      k=next(v for v in r if v not in (i,j))
      if A[i][1]==A[j][1]:
       if not(put(i,0) and put(j,0) and put(k,1)):return None,None
      elif not put(k,0):return None,None
  B=pair_support(T,n,pins)
  if B is None:return None,None
  for j in B:
   if not put(j,0):return None,None
  if len(pins)==old:return pins,A
# Exact component state variables, link via affine equalities and source closure.
# Build group one-hot rows and residual original rows, using one representative per event signature.
def event_quotient(T,n,rows,groups,covered,pins,A):
 expr={};sig_to_var={};constraints=[];nextid=0
 def event(a,b):
  nonlocal nextid
  if a==0:return (None,b)
  if a not in sig_to_var:sig_to_var[a]=nextid;nextid+=1
  return (sig_to_var[a],b)
 for j,(a,b) in enumerate(A):expr[j]=event(a,b)
 # A state of a nontrivial face component is represented by the literal of one member true in that state.
 # If a surviving state is not visible anywhere, allocate a private one-hot selector.
 for scope,states,R in groups:
  # Actual rows on full scope, consistency with current pins and affine pair equalities.
  S=[s for s in states if all(j not in pins or s[j]==pins[j] for j in scope) and all(A[i][0]!=A[j][0] or (s[i]^s[j])==(A[i][1]^A[j][1]) for i,j in it.combinations(scope,2))]
  if not S:return None
  # We include full-scope original rows for the guarded event quotient; all face-state rows implied by them.
  # Choose an anchor original exact-one row: it is a state selector, no auxiliary required.
  constraints.append(tuple(expr[j] for j in rows[R[0]]))
  # Any other row in this component is identical as an exact-one constraint after verified affine equality.
  for r in R:
   # Keep all rows here and deduplicate; this protects against any unproved equivalence.
   constraints.append(tuple(expr[j] for j in rows[r]))
 for r in range(len(rows)):
  if r not in covered:constraints.append(tuple(expr[j] for j in rows[r]))
 # Exact signed linear equations: sum (x XOR sign) = 1.
 eq=[]
 for r in constraints:
  d=defaultdict(int);rhs=1
  for i,b in r:
   rhs-=b
   if i is not None:d[i]+=1-2*b
  d={i:c for i,c in d.items() if c}
  if not d:
   if rhs:return None
  else:eq.append((tuple(sorted(d.items())),rhs))
 return sorted(set(eq)),expr,nextid
# Deterministic exact row redundancy deletion. Rational row span of augmented rows.
def rank(rows):
 B={}
 for d,b in rows:
  a={i:Fraction(c) for i,c in d};a[-1]=Fraction(b)
  while a:
   a={i:v for i,v in a.items() if v}
   if not a:break
   i=max(a);v=a[i]
   if i not in B:B[i]={j:c/v for j,c in a.items()};break
   for j,c in B[i].items():a[j]=a.get(j,0)-v*c
 return len(B)
def reduce_rows(R):
 R=list(R);r=rank(R)
 while len(R)>r:
  occ=Counter(i for d,b in R for i,c in d)
  cand=sorted(range(len(R)),key=lambda j:(-sum(max(0,occ[i]-2) for i,c in R[j][0]),j))
  for j in cand:
   S=R[:j]+R[j+1:]
   if rank(S)==r:R=S;break
  else:raise AssertionError('basis')
 return R
# Exact matching reduction for arbitrary signed +/-1 integer row quotas, <=2 occurrences per variable.
# Each variable is a gadget with ports at its rows. Equal signs select both or neither; opposite select exactly one.
def matching(R,k):
 occ=defaultdict(list);q=[]
 for j,(d,b) in enumerate(R):
  if any(abs(c)!=1 for i,c in d):return 'UNKNOWN',None
  q.append(b+sum(c<0 for i,c in d))
  if not 0<=q[-1]<=len(d):return 'NO',None
  for i,c in d:occ[i].append((j,c))
 if any(len(L)>2 for L in occ.values()):return 'UNKNOWN',None
 G=nx.Graph();mandatory=set();ports={}
 for j,n in enumerate(q):
  for z in range(n):mandatory.add(('r',j,z))
 for i,L in occ.items():
  for a,(j,c) in enumerate(L):
   p=('p',i,a);mandatory.add(p);ports[p]=(j,c)
   for z in range(q[j]):G.add_edge(p,('r',j,z))
  if len(L)==2:
   if L[0][1]==L[1][1]:G.add_edge(('p',i,0),('p',i,1))
   else:
    d=('d',i);mandatory.add(d);G.add_edge(d,('p',i,0));G.add_edge(d,('p',i,1))
  else:G.add_edge(('p',i,0),('optional',i))
 G.add_nodes_from(mandatory)
 for a,b in G.edges():G[a][b]['weight']=int(a in mandatory)+int(b in mandatory)
 M=nx.max_weight_matching(G);mate={a:b for u,v in M for a,b in [(u,v),(v,u)]}
 if not mandatory<=mate.keys():return 'NO',None
 x=[0]*k
 for i,L in occ.items():
  values=[int(mate[('p',i,a)][0]=='r')^(c<0) for a,(j,c) in enumerate(L)];assert len(set(values))==1;x[i]=values[0]
 assert all(sum(c*x[i] for i,c in d)==b for d,b in R)
 return 'YES',x

def solve(T,n,pins=None):
 G,E=source(T,n);rows,groups,covered=quad(T,n,E);stats={'groups':len(groups),'maxstates':max((len(s) for _,s,_ in groups),default=0),'covered':len(covered)}
 P,A=closure(T,n,rows,pins);stats['pins']=len(P) if P is not None else -1
 if P is None:return 'NO',None,stats|{'stage':'closure'}
 Q=event_quotient(T,n,rows,groups,covered,P,A)
 if Q is None:return 'NO',None,stats|{'stage':'local'}
 R,expr,k=Q;stats['rows']=len(R);stats['vars']=k;stats['maxocc_before']=max(Counter(i for d,b in R for i,c in d).values(),default=0)
 S=reduce_rows(R);stats['basis']=len(S);stats['maxocc_after']=max(Counter(i for d,b in S for i,c in d).values(),default=0)
 # Inconsistent augmented system may have a row 0=1 not directly present: matching handles exact retained equations.
 ans,x=matching(S,k)
 if ans=='YES':
  assert all(sum(c*x[i] for i,c in d)==b for d,b in R)
  W=[j for j,(i,b) in expr.items() if (x[i] if i is not None else 0)^b];assert verify(T,n,W);assert all(int(j in W)==b for j,b in P.items())
  return ans,W,stats|{'stage':'matching'}
 return ans,None,stats|{'stage':'matching'}

def chain(k,base=CUBE):
 n0=max(max(t) for t in base)+1;T=[tuple(x+n0*i for x in t) for i in range(k) for t in base]
 # one-edge swap across disjoint planar blocks creates a two-edge cut. Separate distinct end ports.
 for i in range(k-1):T=swap(T,len(base)*i+1,len(base)*(i+1),0)
 return T,n0*k

def audit():
 rng=random.Random(318);counts=Counter();samples=[];abstract=Counter()
 for label,T,n in [('U',U,6),('V',V,6),('cube',CUBE,2)]:
  a,w,s=solve(T,n);truth=brute(T,n);assert a=='UNKNOWN' or (a=='YES')==(truth is not None);samples.append({'name':label,'status':a,'witness':w,'stats':s,'truth':truth is not None})
 for k in [2,4,8,16,32]:
  T,n=chain(k);a,w,s=solve(T,n);assert a=='YES' and verify(T,n,w);samples.append({'name':f'cube-chain-{k}','status':a,'stats':s})
 # Genuine planar source neighbors under guards: arbitrary original tuple pins, exact independent enumeration.
 for T,n in [(U,6),(V,6),(CUBE,2)]:
  for j in range(len(T)):
   for b in [0,1]:
    a,w,s=solve(T,n,{j:b});G,E=source(T,n)
    truth=any(verify(T,n,list(L)) for L in it.combinations(range(len(T)),n) if (j in L)==bool(b))
    assert a=='UNKNOWN' or (a=='YES')==truth;counts['guard_'+a]+=1
 # Abstract signed quota rows, compare matching against exhaustive Boolean solutions, including sign conflicts.
 for _ in range(300):
  r=rng.randrange(1,8);k=rng.randrange(1,9);R=[[] for _ in range(r)]
  for i in range(k):
   for j in rng.sample(range(r),rng.randrange(1,min(r,2)+1)):R[j].append((i,rng.choice([-1,1])))
  S=[(tuple(d),rng.randrange(-sum(c<0 for i,c in d),sum(c>0 for i,c in d)+1)) for d in R]
  a,x=matching(S,k);truth=any(all(sum(c*y[i] for i,c in d)==b for d,b in S) for y in it.product([0,1],repeat=k));assert (a=='YES')==truth;abstract[a]+=1
 # Random planar same-degree switch walks on 3 cubes; only accept authenticated sources.
 T,n=chain(3)
 for _ in range(600):
  i,j=rng.sample(range(len(T)),2);c=rng.randrange(4);S=swap(T,i,j,c)
  if len(set(S))!=len(S) or not nx.check_planarity(graph(S,n))[0] or not nx.is_connected(graph(S,n)):continue
  T=S;a,w,s=solve(T,n);truth=brute(T,n) is not None;assert a=='UNKNOWN' or (a=='YES')==truth;counts['source_'+a]+=1
  if a=='UNKNOWN' and len(samples)<12:samples.append({'name':'unknown','truth':truth,'T':T,'stats':s})
 print(json.dumps({'networkx':nx.__version__,'samples':samples,'counts':counts,'abstract':abstract},indent=2))
if __name__=='__main__':audit()
