import itertools as I, hashlib, json, math
T=[[2,0,4,6],[1,4,7,5],[6,0,1,7],[0,3,2,1],[14,10,4,12],[2,12,7,4],[2,14,9,4],[2,1,0,11],[14,12,0,6],[10,8,4,1],[12,7,11,9],[3,11,0,10],[2,10,14,6],[7,2,6,14],[15,3,10,7],[2,10,11,3]]
K=4; p=[]; ids={}; pins={}
for r,c in I.product(range(K),repeat=2):
 v=r*K+c;q=[]
 for d,(dr,dc) in enumerate([(-1,0),(0,1),(1,0),(0,-1)]):
  rr,cc=r+dr,c+dc;inside=0<=rr<K and 0<=cc<K
  key=tuple(sorted((v,rr*K+cc))) if inside else (v,v,d)
  e=ids.setdefault(key,len(ids));q.append(e)
  if not inside:pins[e]=int(d==2)
 p.append(q)
n=len(ids); W=lambda a:tuple((a>>(3-j))&1 for j in range(4))
assert hashlib.sha256(b''.join(sum(1<<a for a in t).to_bytes(2,'little') for t in T)).hexdigest()=='6efd19c11888af7bd3fe88cbfcb7c60f212a0e4e8bf3516a1e7dd831fa69cb50'
# A: arc closure and bounded frontier, independent of polynomial basis.
def arc():
 t=[a[:] for a in T]; dom=[{0,1} for _ in range(n)]
 for e,b in pins.items():dom[e]={b}
 rounds=0
 while True:
  rounds+=1;old=[a[:] for a in t];old_dom=[d.copy() for d in dom]
  for q,a in zip(p,t):
   a[:]=[w for w in a if all(b in dom[e] for e,b in zip(q,W(w)))]
   if not a:return t,rounds,True
   for j,e in enumerate(q):dom[e]&={W(w)[j] for w in a}
  if t==old and dom==old_dom:return t,rounds,False
cl,rounds,no=arc(); assert cl==T and not no

def frontier():
 s={tuple(sorted(pins.items()))}; attempts=0; sizes=[]
 for i,(q,t) in enumerate(zip(p,T)):
  nxt=set();future=set(sum(p[i+1:],[]))
  for a in s:
   d=dict(a)
   for w in t:
    attempts+=1; z=dict(zip(q,W(w)))
    if all(d.get(e,b)==b for e,b in z.items()):nxt.add(tuple(sorted((e,b) for e,b in (d|z).items() if e in future)))
  s=nxt;sizes.append(len(s))
  if not s:break
 return dict(no=not s,attempts=attempts,sizes=sizes)
# B: exact local basis obtained by enumerating monomials and column nullspace.
def mons(v,d):return [sum(1<<i for i in s) for k in range(d+1) for s in I.combinations(v,k)]
def mul(a,b):
 out=set()
 for x in a:
  for y in b:out.symmetric_difference_update([x|y])
 return out

def local(q,t,d):
 b={};out=[]
 for m in mons(q,d):
  ev=sum(int(all(not (m>>e&1) or bit for e,bit in zip(q,W(w))))<<j for j,w in enumerate(t));row={m}
  while ev:
   k=ev.bit_length()-1
   if k not in b:b[k]=(ev,row);break
   y,z=b[k];ev^=y;row=row^z
  if not ev:out.append(row)
 return out
L=[{1<<e,0} if b else {1<<e} for e,b in pins.items()]+sum([local(q,t,1) for q,t in zip(p,T)],[])
Q=sum([local(q,t,2) for q,t in zip(p,T)],[])
def basis(rows):
 b={}
 for rr in rows:
  r=set(rr)
  while r:
   j=max(r,key=lambda m:(m.bit_count(),m))
   if j not in b:b[j]=r;break
   r^=b[j]
 return b

def subst(r,forms):
 out=set()
 for m in r:
  z={0}
  for i in range(n):
   if m>>i&1:z=mul(z,forms[i])
  out^=z
 return out
b=basis(L);assert 0 not in b
forms={i:{1<<i} for i in range(n)}
for m,row in sorted(b.items()):forms[m.bit_length()-1]=subst(row^{m},forms)
free=[i for i in range(n) if 1<<i not in b]; qchart=[subst(r,forms) for r in Q];assert all(not subst(r,forms) for r in L)
# Dense indexed row elimination with proof provenance. Fixed D<=3. All rows, not only until refutation.
def macaulay(v,gens,D):
 mm=mons(v,D); index={m:j for j,m in enumerate(mm)}; piv={}; generated=[]; provenance={}; xor_count=0;cert=None
 for gi,g in enumerate(gens):
  if not g:continue
  deg=max(m.bit_count() for m in g)
  for a in mons(v,D-deg):
   rr=mul(g,{a});row=sum(1<<index[m] for m in rr);j0=len(generated);generated.append((gi,a,row));pr=1<<j0
   while row:
    j=row.bit_length()-1
    if j not in piv:piv[j]=row;provenance[j]=pr;break
    row^=piv[j];pr^=provenance[j];xor_count+=1
   if 0 in piv and cert is None:cert=provenance[0]
 if cert is not None:
  replay=0;count=0
  for j,(gi,a,r) in enumerate(generated):
   if cert>>j&1:replay^=r;count+=1
  assert replay==1
 else:count=0
 return dict(degree=D,columns=len(mm),rows=len(generated),rank=len(piv),xor_count=xor_count,no=cert is not None,certificate_rows=count,certificate=[(gi,a) for j,(gi,a,_) in enumerate(generated) if cert is not None and cert>>j&1])
# C: independent DFS, original edge ids and guard; no algebra.
def dfs():
 attempts=0
 def rec(i,d):
  nonlocal attempts
  if i==len(T):return True
  for a in T[i]:
   attempts+=1;z=dict(zip(p[i],W(a)))
   if all(d.get(e,b)==b for e,b in z.items()) and rec(i+1,d|z):return True
  return False
 return dict(no=not rec(0,pins.copy()),attempts=attempts)
res=dict(n=n,affine_rank=len(b),free=len(free),arc_rounds=rounds,frontier=frontier(),dfs=dfs(),raw=[],chart=[])
for D in (2,3):
 res['raw'].append(macaulay(list(range(n)),L+Q,D));res['chart'].append(macaulay(free,qchart,D))
# independent evaluation of exact local quadratic representation on all 16 words
for q,t in zip(p,T):
 for a in range(16):
  assignment=sum(b<<e for e,b in zip(q,W(a)))
  assert (all(sum((m&assignment)==m for m in r)%2==0 for r in local(q,t,2)))==(a in t)
print(json.dumps(res,indent=2))
