"""Independent scalar checker for C04-33 sparse certificates. Usage: python check33.py source.eb.json cert.json"""
import sys,json,hashlib,itertools as it,collections as co
from pathlib import Path

def check(raw,cert):
 d=json.loads(raw);assert d['format']=='STRICT-EB4-v1';types=d['types'];E=d['edges'];n=len(types);assert cert['instance_id']=='STRICT-EB4-v1:sha256:'+hashlib.sha256(raw).hexdigest() and cert['original_N_bits']==8*len(raw)
 assert cert['guard_id']=='EMPTY' and cert['residual_id']=='ROOT' and all(t in ('E','B') for t in types)
 p=list(range(4*n));s=[0]*(4*n)
 def find(i):
  if p[i]==i:return i,0
  r,z=find(p[i]);s[i]^=z;p[i]=r;return r,s[i]
 def union(a,b,z):
  a,aa=find(a);b,bb=find(b);z^=aa^bb
  if a==b:assert z==0;return
  if a>b:a,b=b,a
  p[b]=a;s[b]=z
 ports=set();edges=set()
 for a,b,z in E:
  assert 0<=a<4*n and 0<=b<4*n and a//4!=b//4 and a not in ports and b not in ports and z in (0,1)
  uv=tuple(sorted((a//4,b//4)));assert uv not in edges;edges.add(uv);ports.update((a,b));union(a,b,z)
 assert len(ports)==4*n
 for v,t in enumerate(types):
  if t=='E':
   for j in (1,2,3):union(4*v,4*v+j,0)
 rows={}
 for v,t in enumerate(types):
  if t!='B':continue
  w=tuple(sorted(find(4*v+j) for j in range(4)));w=min(w,tuple(sorted((r,1-z) for r,z in w)));rows[w]=None
 F=[]
 for w in rows:
  S=tuple(sorted({r for r,z in w}));A=set()
  for z in it.product((0,1),repeat=len(S)):
   h=dict(zip(S,z))
   if sum(h[r]^a for r,a in w)==2:A.add(z)
  F.append((S,A))
 steps=0;reads=0;scans=0
 while True:
  occ=co.defaultdict(list)
  for i,(S,A) in enumerate(F):
   for x in S:occ[x].append(i);scans+=1
  pick=None
  for x,I in sorted(occ.items(),key=lambda t:(len(t[1]),t[0])):
   if len(I)>2:break
   U=tuple(sorted(set().union(*(set(F[i][0]) for i in I))-{x}))
   if len(U)<=4:pick=(x,I,U);break
  if pick is None:break
  x,I,U=pick;A=set()
  for z in it.product((0,1),repeat=len(U)):
   h=dict(zip(U,z))
   for b in (0,1):
    h[x]=b;ok=True
    for i in I:
     S,R=F[i];reads+=1;ok &= tuple(h[y] for y in S) in R
    if ok:A.add(z);break
  F=[f for i,f in enumerate(F) if i not in I]+[(U,A)];steps+=1
 assert steps==cert['initial_eliminations']
 g=cert['gauge_root'];assert any(g in S for S,A in F);assert all(tuple(1-b for b in w) in A for S,A in F for w in A)
 L=[]
 for S,A in F:
  if g in S:
   j=S.index(g);A={w[:j]+w[j+1:] for w in A if w[j]==0};S=S[:j]+S[j+1:]
  if S or not A:L.append((S,A))
 F=L;checks=0
 for x,order,sizes,projected in cert['trace']:
  I=[j for j,(S,A) in enumerate(F) if x in S];assert I and sorted(order)==I and len(order)==len(sizes)
  S,A=F[order[0]];assert len(A)==sizes[0]
  for j,size in zip(order[1:],sizes[1:]):
   T,B=F[j];U=tuple(sorted(set(S)|set(T)));I1=tuple(S.index(v) for v in S if v in T);I2=tuple(T.index(v) for v in S if v in T);p=[(0,S.index(v)) if v in S else (1,T.index(v)) for v in U];Q=set()
   checks+=len(A)*len(B)
   for a in A:
    for b in B:
     if all(a[i]==b[k] for i,k in zip(I1,I2)):Q.add(tuple((a,b)[h][i] for h,i in p))
   S,A=U,Q;assert len(A)==size
  j=S.index(x);T=S[:j]+S[j+1:];A={a[:j]+a[j+1:] for a in A};assert len(A)==projected
  F=[f for j,f in enumerate(F) if j not in I]+[(T,A)]
 assert any(not A for S,A in F)
 return {'status':'PASS','source_bytes':len(raw),'initial_eliminations':steps,'scope_scans':scans,'initial_table_reads':reads,'coarse_eliminations':len(cert['trace']),'scalar_pair_checks':checks}
if __name__=='__main__':
 raw=Path(sys.argv[1]).read_bytes();c=Path(sys.argv[2]).read_bytes();print('CERT-v1:sha256:'+hashlib.sha256(c).hexdigest(),check(raw,json.loads(c)))
