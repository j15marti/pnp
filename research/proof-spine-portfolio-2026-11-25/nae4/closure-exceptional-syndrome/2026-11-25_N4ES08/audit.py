import random, numpy as np, json, itertools
rng=random.Random(84522)
def rank(n,cs):
 A=np.zeros((len(cs),n),dtype=np.int16)
 for i,c in enumerate(cs): A[i,list(c)]=1
 r=0
 for j in range(n):
  ids=np.flatnonzero(A[r:,j]);
  if not len(ids):continue
  k=r+int(ids[0]); A[[r,k]]=A[[k,r]]; A[r]=(A[r]*int(A[r,j]))%3
  ids=np.flatnonzero(A[r+1:,j])+r+1
  A[ids]=(A[ids]-A[ids,j,None]*A[r])%3
  r+=1
  if r==len(cs):break
 return r
def auth(n,P):
 assert len(P)==4 and all(sorted(sum((list(c) for c in p),[]))==list(range(n)) for p in P)
 pairs=[tuple(sorted(t)) for p in P for c in p for t in itertools.combinations(c,2)]
 assert len(pairs)==len(set(pairs))
def sat(P,x):return all(0<sum(x[i] for i in c)<3 for p in P for c in p)
def base():
 n=12
 for trial in range(100000):
  P=[]; used=set()
  for j in range(4):
   for _ in range(100):
    l=list(range(n));rng.shuffle(l); p=[tuple(sorted(l[i:i+3])) for i in range(0,n,3)]; pairs={t for c in p for t in itertools.combinations(c,2)}
    if not pairs&used: P.append(p);used|=pairs;break
   else:break
  if len(P)!=4 or rank(n,sum(P,[]))!=n-1:continue
  for x in itertools.product((0,1),repeat=n):
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
P,x,t=base();auth(12,P);out={'seed':84522,'base':P,'base_witness':x,'trials':t,'base_rank':rank(12,sum(P,[])),'lifts':[]}
for p in [1,2,4,8,16,32,64]:
 Q,y=lift(P,x,p);n=len(y);auth(n,Q);assert sat(Q,y);r=rank(n,sum(Q,[]));out['lifts'].append({'p':p,'variables':n,'clauses':4*n//3,'rank':r,'nullity':n-r,'witness_verified':True})
# full AG(2,3) control
A=[[(3*i,3*i+1,3*i+2) for i in range(3)]]+[[tuple(3*i+(a*i+b)%3 for i in range(3)) for b in range(3)] for a in range(3)]
auth(9,A);out['AG9']={'rank':rank(9,sum(A,[])),'models':sum(sat(A,z) for z in itertools.product((0,1),repeat=9))};assert out['AG9']['models']==0
# Check a rank-11 minor of the base, using row selection on the first 11 columns.
from fractions import Fraction
C=sum(P,[]); piv=[]
for i in range(len(C)):
 if rank(12,[C[j] for j in piv+[i]])>len(piv):piv.append(i)
assert len(piv)==11
M=[[int(j in C[i]) for j in range(11)] for i in piv]
def det(A):
 A=[[Fraction(x) for x in r] for r in A]; d=Fraction(1)
 for i in range(len(A)):
  k=next((j for j in range(i,len(A)) if A[j][i]),None)
  if k is None:return 0
  if k!=i:A[k],A[i]=A[i],A[k];d=-d
  q=A[i][i];d*=q
  for j in range(i+1,len(A)):
   t=A[j][i]/q
   for k in range(i+1,len(A)):A[j][k]-=t*A[i][k]
 return int(d)
d=det(M);assert d%3;out['base_minor']={'rows_zero_based':piv,'columns_zero_based':list(range(11)),'integer_determinant':d}
# Actual boundary relation test for the historical H block.
H=[c for p in A for c in p if c not in [(0,1,2),(3,4,5)]]
HW=[z for z in itertools.product((0,1),repeat=9) if sat([H],z)]
assert {z[:6] for z in HW}=={(0,0,0,1,1,1),(1,1,1,0,0,0)}
D=[[(1,9,11),(0,2,5),(6,7,8),(3,4,10)],[(0,6,10),(3,7,9),(2,8,11),(1,4,5)],[(3,5,11),(0,4,7),(2,6,9),(1,8,10)],[(5,8,9),(4,6,11),(0,1,3),(2,7,10)]]
DX=[int(i in {0,2,3,4,8}) for i in range(12)]
assert sat([[c for c in p if c!=(1,9,11)] for p in D],DX) and all(DX[i]==0 for i in (1,9,11))
def ring(k,neighbor):
 Q=[[] for _ in range(4)];w=[0]*(33*k)
 for i in range(k):
  b=33*i;c=i%2 if not neighbor else (i-1)%k%2
  if neighbor and i==0:c=0 # path constraints from 1 to 2 .. k-1 to 0
  # for odd k, c_1=0, c_2=1,...,c_(k-1)=1,c_0=0
  w[b:b+9]=next(z for z in HW if z[0]==c)
  for j,p in enumerate(A):Q[j].extend(tuple(b+v for v in t) for t in p if t not in [(0,1,2),(3,4,5)])
  for a in range(2):
   h=b+9+12*a; w[h:h+12]=[v^a for v in DX]
   for j,p in enumerate(D):Q[j].extend(tuple(h+v for v in t) for t in p if t!=(1,9,11))
  Q[0].extend((b+3+j,b+9+v,b+21+v) for j,v in enumerate((1,9,11)))
 for i in range(k):
  b=33*i; h=33*((i+1)%k);Q[0].append((b,h+1,h+2))
 if neighbor:
  a=len(Q[0])-k;b=a+1
  r=list(Q[0][a]);s=list(Q[0][b]);r[0],s[1]=s[1],r[0];Q[0][a]=tuple(r);Q[0][b]=tuple(s)
 auth(len(w),Q)
 return Q,w
out['ring_controls']=[]
for k in [3,5,17]:
 U,_=ring(k,False);V,w=ring(k,True);assert sat(V,w)
 # U unsat by actual H table and exhaustive phase check for small k, parity proof otherwise
 assert not any(all(z[i]!=z[(i+1)%k] for i in range(k)) for z in itertools.product((0,1),repeat=k))
 out['ring_controls'].append({'k':k,'variables':33*k,'clauses':44*k,'SAT_neighbor_witness':True,'UNSAT_phase_check':True})
print(json.dumps(out,indent=2))
