import itertools as it, random, json, numpy as np
SEED=84522
rng=random.Random(SEED)
P0=[[(0,3,6),(2,4,9),(5,10,11),(1,7,8)],[(3,9,10),(6,7,11),(0,1,4),(2,5,8)],[(4,7,10),(0,5,9),(3,8,11),(1,2,6)],[(4,6,8),(3,5,7),(0,2,10),(1,9,11)]]
def auth(n,P):
 assert len(P)==4 and all(sorted(v for c in p for v in c)==list(range(n)) for p in P)
 pairs=[tuple(sorted(t)) for p in P for c in p for t in it.combinations(c,2)]
 assert len(pairs)==len(set(pairs))
def sat(P,x):return all(0<sum(x[i] for i in c)<3 for p in P for c in p)
def echelon(A,p):
 A=np.array(A,dtype=np.int64).copy()%p;r=0;piv=[]
 for j in range(A.shape[1]):
  ids=np.flatnonzero(A[r:,j])
  if not len(ids):continue
  k=r+int(ids[0]);A[[r,k]]=A[[k,r]];A[r]=A[r]*pow(int(A[r,j]),-1,p)%p
  ids=np.flatnonzero(A[r+1:,j])+r+1
  A[ids]=(A[ids]-A[ids,j,None]*A[r])%p
  piv.append(j);r+=1
  if r==len(A):break
 return A[:r],piv
def rank3(n,cs):
 A=np.zeros((len(cs),n),dtype=np.int64)
 for i,c in enumerate(cs):A[i,list(c)]=1
 return len(echelon(A,3)[1])
def base():
 for trial in range(100000):
  P=[];used=set()
  for j in range(4):
   for _ in range(100):
    l=list(range(12));rng.shuffle(l);p=[tuple(sorted(l[i:i+3])) for i in range(0,12,3)];pairs={t for c in p for t in it.combinations(c,2)}
    if not pairs&used:P.append(p);used|=pairs;break
   else:break
  if len(P)!=4 or rank3(12,sum(P,[]))!=11:continue
  for x in it.product((0,1),repeat=12):
   if sat(P,x):return P,x,trial
 raise RuntimeError('no base')
def lift(P,x,p):
 Q=[]
 for part in P:
  q=[]
  for c in part:
   perms=[rng.sample(range(p),p) for _ in c]
   q.extend(tuple(v*p+perms[j][i] for j,v in enumerate(c)) for i in range(p))
  Q.append(q)
 return Q,[b for b in x for _ in range(p)]
def relabel(n,P,seed):
 R=random.Random(seed);v=list(range(n));R.shuffle(v);Q=[]
 for part in P:
  p=[tuple(v[i] for i in c) for c in part];R.shuffle(p);Q.append(p)
 R.shuffle(Q);return Q
def neighbors(n,P):
 A=np.empty((4,n,2),dtype=np.int64)
 for j,part in enumerate(P):
  for c in part:
   for v in c:A[j,v]=[w for w in c if w!=v]
 return A
# Polynomial x(x-8)(x+1)(x+3)(x^2-3); ascending coefficients.
POLY=np.polynomial.polynomial.polymul(np.polynomial.polynomial.polymul([0,1],[-8,1]),np.polynomial.polynomial.polymul(np.polynomial.polynomial.polymul([1,1],[3,1]),[-3,0,1])).astype(np.int64).tolist()
def null_basis(E,piv,n,p):
 free=sorted(set(range(n))-set(piv));K=np.zeros((n,len(free)),dtype=np.int64);K[free,np.arange(len(free))]=1
 for i,j in reversed(list(enumerate(piv))):K[j]=-(E[i]@K)%p
 return K
def terminal(n,P,p=101,cap=12):
 # no hidden fibers or Boolean target used; fixed polynomial is the only template.
 A=neighbors(n,P);I=np.eye(n,dtype=np.int64)
 def left(M):return sum(M[A[j,:,0]]+M[A[j,:,1]] for j in range(4))%p
 E=POLY[-1]*I
 for c in reversed(POLY[:-1]):E=(left(E)+c*I)%p
 E,piv=echelon(E,p);dims=[n-len(piv)]
 # row-space saturation by partition adjacency operators, equivalent to invariant kernel.
 while True:
  # A_j symmetric, so right multiplication is sparse column gathering.
  rows=[E]+[(E[:,A[j,:,0]]+E[:,A[j,:,1]])%p for j in range(4)]
  F,q=echelon(np.concatenate(rows),p)
  if len(q)==len(piv):break
  E,piv=F,q;dims.append(n-len(piv))
 K=null_basis(E,piv,n,p)
 assert not np.any(E@K%p)
 _,g=np.unique(K,axis=0,return_inverse=True);b=int(g.max())+1 if n else 0
 # Candidate equality grouping only, never exported as forced facts.
 if b>cap:return None,{'dims':dims,'groups':b,'reason':'cap'}
 Q=[tuple(int(g[v]) for v in c) for part in P for c in part]
 for z in it.product((0,1),repeat=b):
  if all(0<sum(z[i] for i in c)<3 for c in Q):
   x=[z[i] for i in g];assert sat(P,x);return x,{'dims':dims,'groups':b,'reason':'witness'}
 return None,{'dims':dims,'groups':b,'reason':'quotient_no_unknown'}
def prop(P,n,pins):
 x=dict(pins)
 while True:
  old=len(x)
  for c in sum(P,[]):
   a=[x[i] for i in c if i in x];u=[i for i in c if i not in x]
   if a and min(a)==max(a):
    if not u:return None
    if len(u)==1:x[u[0]]=1-a[0]
  if len(x)==old:return x
def forced(P,n,pins):
 x=prop(P,n,pins);probes=0
 while x is not None:
  changed=False
  for i in range(n):
   if i in x:continue
   a=prop(P,n,{**x,i:0});b=prop(P,n,{**x,i:1});probes+=2
   if a is None and b is None:return None,probes
   y=b if a is None else a if b is None else {j:v for j,v in a.items() if b.get(j)==v}
   if len(y)>len(x):x=prop(P,n,y);changed=True;break
  if not changed:return x,probes
 return None,probes
P,x,t=base();assert P==P0 and t==586
out={'seed':SEED,'base_trial':t,'polynomial':POLY,'lifts':[]}
for p in [1,2,4,8,16,32,64]:
 Q,y=lift(P,x,p);n=len(y);auth(n,Q);assert sat(Q,y)
 R=relabel(n,Q,991+p);auth(n,R)
 z,probes=forced(R,n,{0:0});assert z is not None
 w,d=terminal(n,R);assert w is not None and sat(R,w)
 if w[0]:w=[1-v for v in w]
 assert all(w[i]==a for i,a in z.items())
 out['lifts'].append({'p':p,'n':n,'m':4*n//3,'guarded_pins':len(z),'probes':probes,**d,'witness_verified':True})
A=[[(3*i,3*i+1,3*i+2) for i in range(3)]]+[[tuple(3*i+(a*i+b)%3 for i in range(3)) for b in range(3)] for a in range(3)]
auth(9,A);assert not any(sat(A,z) for z in it.product((0,1),repeat=9));z,probes=forced(A,9,{0:0});w,d=terminal(9,A);assert w is None
out['AG9']={'forced_reject':z is None,'probes':probes,**d}
# Genuine same-size SAT/UNSAT ring controls from N4ES08, exact H projection.
H=[c for p in A for c in p if c not in [(0,1,2),(3,4,5)]]
HW=[z for z in it.product((0,1),repeat=9) if sat([H],z)]
assert {z[:6] for z in HW}=={(0,0,0,1,1,1),(1,1,1,0,0,0)}
D=[[(1,9,11),(0,2,5),(6,7,8),(3,4,10)],[(0,6,10),(3,7,9),(2,8,11),(1,4,5)],[(3,5,11),(0,4,7),(2,6,9),(1,8,10)],[(5,8,9),(4,6,11),(0,1,3),(2,7,10)]]
DX=[int(i in {0,2,3,4,8}) for i in range(12)]
def ring(k,neighbor):
 Q=[[] for _ in range(4)];w=[0]*(33*k)
 for i in range(k):
  b=33*i;c=i%2 if not neighbor else (i-1)%k%2
  if neighbor and i==0:c=0
  w[b:b+9]=next(z for z in HW if z[0]==c)
  for j,p in enumerate(A):Q[j].extend(tuple(b+v for v in t) for t in p if t not in [(0,1,2),(3,4,5)])
  for a in range(2):
   h=b+9+12*a;w[h:h+12]=[v^a for v in DX]
   for j,p in enumerate(D):Q[j].extend(tuple(h+v for v in t) for t in p if t!=(1,9,11))
  Q[0].extend((b+3+j,b+9+v,b+21+v) for j,v in enumerate((1,9,11)))
 for i in range(k):
  b=33*i;h=33*((i+1)%k);Q[0].append((b,h+1,h+2))
 if neighbor:
  a=len(Q[0])-k;b=a+1;r=list(Q[0][a]);s=list(Q[0][b]);r[0],s[1]=s[1],r[0];Q[0][a]=tuple(r);Q[0][b]=tuple(s)
 auth(len(w),Q);return Q,w
out['rings']=[]
for k in [3,5,17]:
 for yes in [False,True]:
  Q,y=ring(k,yes);n=len(y)
  if yes:assert sat(Q,y)
  else:assert k%2 # exact H projection forces odd cycle inequalities
  z,probes=forced(Q,n,{0:0})
  assert not yes or z is not None
  # apply exact quotient only on the smallest pair to limit run time
  w,d=terminal(n,Q) if k==3 else (None,{'reason':'not_run'})
  assert yes or w is None
  out['rings'].append({'k':k,'SAT':yes,'guarded_pins':None if z is None else len(z),'probes':probes,**d})
print(json.dumps(out,indent=2))
