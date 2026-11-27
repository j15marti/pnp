"""Independent scalar checker for C04-29 certificates. Usage: python check_compact.py source.eb.json cert.json"""
import sys,json,hashlib,itertools as it,collections as co
from pathlib import Path

def check(raw,cert):
 d=json.loads(raw);assert d['format']=='STRICT-EB4-v1';types=d['types'];E=d['edges'];n=len(types);assert cert['instance_id']=='STRICT-EB4-v1:sha256:'+hashlib.sha256(raw).hexdigest() and cert['original_N_bits']==8*len(raw)
 assert cert['guard_id']=='EMPTY' and cert['residual_id']=='ROOT' and all(t in ('E','B') for t in types)
 # Parity union-find with minimum original port representative. Independent of discovery BFS.
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
 # Derive *all* prime local forbidden partial words by independent scalar enumeration. Signed clauses use min-port+1.
 C=set();tablechecks=0
 for S,A in F:
  minimal=[]
  for k in range(len(S)+1):
   for I in it.combinations(range(len(S)),k):
    for z in it.product((0,1),repeat=k):
     tablechecks+=1
     H=dict(zip(I,z))
     if any(all(w[i]==b for i,b in H.items()) for w in A):continue
     if any(all(H.get(i)==b for i,b in h.items()) for h in minimal):continue
     minimal.append(H);C.add(tuple(sorted((S[i]+1)*(1-2*b) for i,b in H.items())))
  for z in it.product((0,1),repeat=len(S)):
   assert (z in A)==(not any(all(z[i]==b for i,b in h.items()) for h in minimal))
 # Every constraint is complement symmetric, so fixing root 10 to zero is WLOG. Exact projection preserves symmetry.
 g=cert['gauge_root'];assert any(g in S for S,A in F);assert all(tuple(1-b for b in w) in A for S,A in F for w in A)
 C=sorted(C,key=lambda c:(len(c),c));C.append((-g-1,));vis=0
 for cl in cert['proof']:
  assert len(set(cl))==len(cl) and all(-l not in cl for l in cl) and all(abs(l)-1 in set().union(*(set(S) for S,A in F)) for l in cl)
  h={abs(l):l<0 for l in cl};conf=False
  while True:
   changed=False
   for c in C:
    vis+=len(c)
    if any(h.get(abs(l))==(l>0) for l in c if abs(l) in h):continue
    rem=[l for l in c if abs(l) not in h]
    if not rem:conf=True;break
    if len(rem)==1:
     l=rem[0];h[abs(l)]=l>0;changed=True
   if conf or not changed:break
  assert conf,cl;C.append(tuple(cl))
 assert cert['proof'][-1]==[]
 return {'status':'PASS','source_bytes':len(raw),'eliminations':steps,'scope_scans':scans,'table_reads':reads,'prime_table_tests':tablechecks,'proof_steps':len(cert['proof']),'literal_visits':vis}
if __name__=='__main__':
 raw=Path(sys.argv[1]).read_bytes();c=Path(sys.argv[2]).read_bytes();print('CERT-v1:sha256:'+hashlib.sha256(c).hexdigest(),check(raw,json.loads(c)))
