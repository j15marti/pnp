#!/usr/bin/env python3
"""Standalone original-byte checker for C04-29. Usage: python check29.py input.eb.json cert.json."""
import json,sys,hashlib,itertools as it,collections as co,zlib,base64
from pathlib import Path

def normalize_project(G):
 T=G['types'];n=len(T);assert all(t in ('E','B') for t in T)
 adj=[[] for _ in range(4*n)];used=set();seen=set()
 def link(a,b,s):adj[a].append((b,s));adj[b].append((a,s))
 for a,b,s in G['edges']:
  k=tuple(sorted((a//4,b//4)));assert 0<=a<4*n and 0<=b<4*n and s in (0,1) and k[0]!=k[1] and k not in seen and a not in used and b not in used
  seen.add(k);used.update((a,b));link(a,b,s)
 assert len(used)==4*n
 for v,t in enumerate(T):
  if t=='E':
   for j in (1,2,3):link(4*v,4*v+j,0)
 root=[-1]*(4*n);p=[0]*(4*n)
 for i in range(4*n):
  if root[i]>=0:continue
  root[i]=i;Q=[i]
  for a in Q:
   for b,s in adj[a]:
    z=p[a]^s
    if root[b]<0:root[b]=i;p[b]=z;Q.append(b)
    else:assert root[b]==i and p[b]==z
 rows={}
 for v,t in enumerate(T):
  if t=='B':
   w=tuple(sorted((root[x],p[x]) for x in range(4*v,4*v+4)));w=min(w,tuple(sorted((r,1-s) for r,s in w)));rows.setdefault(w,[]).append(v)
 F=[]
 for w in rows:
  U=tuple(sorted({r for r,s in w}));A=set()
  for z in range(1<<len(U)):
   if sum(((z>>U.index(r))&1)^s for r,s in w)==2:A.add(z)
  F.append((U,A))
 while True:
  occ=co.defaultdict(list)
  for i,(U,A) in enumerate(F):
   for r in U:occ[r].append(i)
  choose=None
  for r,L in sorted(occ.items(),key=lambda x:(len(x[1]),x[0])):
   if len(L)>2:break
   U=tuple(sorted(set().union(*(set(F[i][0]) for i in L))-{r}))
   if len(U)<=4:choose=(r,L,U);break
  if choose is None:break
  r,L,U=choose;W=tuple(sorted(U+(r,)));A=set()
  for z in range(1<<len(W)):
   d={x:(z>>j)&1 for j,x in enumerate(W)}
   if all(sum(d[x]<<j for j,x in enumerate(F[i][0])) in F[i][1] for i in L):A.add(sum(d[x]<<j for j,x in enumerate(U)))
  F=[f for i,f in enumerate(F) if i not in L]+[(U,A)]
 return F

def clauses(F):return [tuple((r+1)*(-1 if z>>i&1 else 1) for i,r in enumerate(U)) for U,A in F for z in range(1<<len(U)) if z not in A]
def up(C,assumptions):
 a={};visits=0
 for l in assumptions:
  if abs(l) in a and a[abs(l)]!=(l>0):return True,visits
  a[abs(l)]=l>0
 while True:
  changed=False
  for c in reversed(C):
   visits+=len(c)
   if any(abs(l) in a and a[abs(l)]==(l>0) for l in c):continue
   R=[l for l in c if abs(l) not in a]
   if not R:return True,visits
   if len(R)==1:a[abs(R[0])]=R[0]>0;changed=True
  if not changed:return False,visits

def chart(F):
 K=[]
 for U,A in F:
  assert all((z in A)==(((1<<len(U))-1-z) in A) for z in range(1<<len(U)))
  V=tuple(x for x in U if x!=10);B=set()
  for z in A:
   d={x:(z>>j)&1 for j,x in enumerate(U)}
   if not d.get(10,0):B.add(sum(d[x]<<j for j,x in enumerate(V)))
  K.append((V,B))
 vs=sorted({r+1 for U,A in K for r in U});idx={r:i for i,r in enumerate(vs)};P=[]
 for U,A in K:
  p=set()
  for z in range(1<<len(U)):
   if sum(w not in A for w in range(1<<len(U)) if w&z==w)%2:p.add(sum(1<<idx[r+1] for j,r in enumerate(U) if z>>j&1))
  P.append(p)
 return vs,P

def mul(p,x):
 q=set()
 for m in p:q.symmetric_difference_update({m|x})
 return q

def cpoly(c,idx):
 p={0}
 for l in c:
  q=mul(p,1<<idx[abs(l)]);p=q if l<0 else p^q
 return p

def dag(P,ops,n,d):
 D=[];terms=0
 for i,op in enumerate(ops):
  t=op[0]
  if t=='input':assert 0<=op[1]<len(P);q=P[op[1]].copy()
  elif t=='xor':assert all(0<=j<i for j in op[1:]);q=D[op[1]]^D[op[2]]
  else:assert t=='mul' and 0<=op[1]<i and 0<=op[2]<n;q=mul(D[op[1]],1<<op[2])
  assert all(m.bit_count()<=d and m<(1<<n) for m in q);terms+=len(q);D.append(q)
 assert D[-1]=={0};return terms

def invariant(P,n,pair,d=3):
 M=[sum(1<<i for i in S) for k in range(d+1) for S in it.combinations(range(n),k)];I={m:i for i,m in enumerate(M)};B={};checks=0
 def emit(p):return sum(1<<I[m] for m in p)
 def terms(v):
  while v:
   z=v&-v;yield M[z.bit_length()-1];v^=z
 def reduce(v,insert=False):
  nonlocal checks
  while v:
   checks+=1;k=v.bit_length()-1
   if k not in B:
    if insert:B[k]=v
    return v
   v^=B[k]
  return 0
 q=P[pair[0]]^P[pair[1]];assert max(m.bit_count() for m in q)<=2
 for p in P+[q]+[mul(q,1<<j) for j in range(n)]+[{0,16,1024,274877906944,1040,274877906960,274877907968,274877906961}]:reduce(emit(p),True)
 assert reduce(1)!=0
 bs=list(B.values());kernels=0
 for j in range(n):
  mask=sum(1<<k for k,m in enumerate(M) if m.bit_count()==d and not m>>j&1);A={}
  for i,v in enumerate(bs):
   u=v&mask;c=1<<i
   while u:
    checks+=1;k=u.bit_length()-1
    if k not in A:A[k]=(u,c);break
    y,a=A[k];u^=y;c^=a
   if not u:
    w=0
    while c:
     z=c&-c;w^=bs[z.bit_length()-1];c^=z
    assert reduce(emit(mul(terms(w),1<<j)))==0;kernels+=1
 return {'rank':len(B),'columns':len(M),'kernel_images':kernels,'checks':checks}

def check(raw,cert):
 G=json.loads(raw);C=json.loads(cert);assert G['format']==C['problem_id']=='STRICT-EB4-v1' and C['guard_id']=='EMPTY' and C['residual_id']=='ROOT';assert C['original_N_bits']==len(raw)*8 and C['instance_id']=='STRICT-EB4-v1:sha256:'+hashlib.sha256(raw).hexdigest()
 F=normalize_project(G);vs,P=chart(F);assert vs==C['chart_root_ids_plus_one'];assert len(P)==C['factor_count'];D=clauses(F)+[(-11,)];assert not up(D,[])[0]
 out={}
 if 'invariant_pair' in C:
  out['invariant']=invariant(P,len(vs),C['invariant_pair']);assert out['invariant']['rank']==222
 idx={r:i for i,r in enumerate(vs)};visits=0;reclose=0
 for c in C.get('peer_trace',[]):
  ok,v=up(D,[-l for l in c]);assert ok;visits+=v;D.append(tuple(c));_,v=up(D,[]);reclose+=v
  if c:assert all(abs(l) in idx for l in c);P.append(cpoly(c,idx))
 if 'proof_zlib_base64' in C:
  ops=json.loads(zlib.decompress(base64.b64decode(C['proof_zlib_base64'])));out['proof_nodes']=len(ops);out['proof_terms']=dag(P,ops,len(vs),3)
 out.update({'peer_replay_visits':visits,'peer_reclosure_visits':reclose,'certificate_id':'CERT-v1:sha256:'+hashlib.sha256(cert).hexdigest()});return out
if __name__=='__main__':print(json.dumps(check(Path(sys.argv[1]).read_bytes(),Path(sys.argv[2]).read_bytes()),indent=2))
