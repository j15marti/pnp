"""Stdlib only: python verify_compact36.py native.eb.json compact36.json"""
import json,hashlib,itertools as it,collections as co,base64,zlib,sys,math
from pathlib import Path
J=lambda a:(json.dumps(a,separators=(',',':'))+'\n').encode()
H=lambda a:hashlib.sha256(a).hexdigest()
def reconstruct(raw):
 G=json.loads(raw);assert G['format']=='STRICT-EB4-v1';T=G['types'];n=len(T);assert all(t in ('E','B') for t in T);P=list(range(4*n));S=[0]*len(P);used=set();edges=set()
 def find(x):
  z=0;y=x
  while P[y]!=y:z^=S[y];y=P[y]
  while x!=y:
   nxt=P[x];a=S[x];P[x]=y;S[x]=z;z^=a;x=nxt
  return y
 def get(x):
  r=find(x);return r,S[x] if r!=x else 0
 def union(x,y,b):
  r,a=get(x);s,c=get(y);b^=a^c
  if r==s:assert not b;return
  if r>s:r,s=s,r
  P[s]=r;S[s]=b
 for x,y,b in G['edges']:
  assert 0<=x<4*n and 0<=y<4*n and x//4!=y//4 and b in (0,1) and x not in used and y not in used
  e=tuple(sorted((x//4,y//4)));assert e not in edges;edges.add(e);used.update((x,y));union(x,y,b)
 assert len(used)==4*n
 for v,t in enumerate(T):
  if t=='E':
   for j in (1,2,3):union(4*v,4*v+j,0)
 roots=[get(i) for i in range(4*n)];count=co.Counter(roots[4*v+j][0] for v,t in enumerate(T) if t=='B' for j in range(4));g=min(count,key=lambda v:(-count[v],v));assert g==10
 def group(F):
  D={}
  for q in F:
   V=tuple(q['vs'])
   if V not in D:D[V]=dict(vs=list(V),cost=q['cost'][:],ids=q['ids'][:])
   else:
    r=D[V];r['cost']=[a+b for a,b in zip(r['cost'],q['cost'])];r['ids']+=q['ids']
  return list(D.values())
 F=[]
 for v,t in enumerate(T):
  if t!='B':continue
  W=roots[4*v:4*v+4];V=sorted({x for x,s in W}-{g});A=[]
  for k in range(2**len(V)):
   h={x:(k>>j)&1 for j,x in enumerate(V)};A.append(int(sum(h.get(x,0)^s for x,s in W)!=2))
  F.append(dict(vs=V,cost=A,ids=[v]))
 F=group(F);trace=[];checks=0
 while True:
  O=co.defaultdict(list)
  for j,q in enumerate(F):
   for x in q['vs']:O[x].append(j)
  candidates=[]
  for x,I in O.items():
   if len(I)>2:continue
   V=sorted({v for i in I for v in F[i]['vs']}-{x})
   if len(V)<=8:candidates.append((len(V),x,I,V))
  if not candidates:break
  _,x,I,V=min(candidates);A=[];arg=[]
  for k in range(2**len(V)):
   h={v:(k>>j)&1 for j,v in enumerate(V)};c=[]
   for b in (0,1):
    h[x]=b;c.append(sum(F[i]['cost'][sum(h[v]<<j for j,v in enumerate(F[i]['vs']))] for i in I));checks+=len(I)
   A.append(min(c));arg.append(int(c[1]<c[0]))
  ids=sorted(o for i in I for o in F[i]['ids']);trace.append(dict(v=x,S=V,cost=A,arg=arg,ids=ids));F=group([q for i,q in enumerate(F) if i not in I]+[dict(vs=V,cost=A,ids=ids)])
 assert sorted(o for q in F for o in q['ids'])==[v for v,t in enumerate(T) if t=='B']
 return F,{'gauge':g,'trace':trace},checks
def verify(raw,cert):
 C=json.loads(cert);h=H(raw);instance='STRICT-EB4-v1:sha256:'+h;assert C['instance_id']==instance and C['original_N_bits']==len(raw)*8
 F,M,pre=reconstruct(raw);ch=H(J(F));mh=H(J(M));gh=H(J([[10,0]]));assert (ch,mh,gh)==(C['chart_sha256'],C['map_sha256'],C['guard_sha256']);gid='GUARD-v1:sha256:'+H(J(['PNP-GUARD-v1',instance,'EB-PORT-PINS-v1',gh]));assert gid==C['guard_id'];assert C['residual_id']=='RESIDUAL-v1:sha256:'+H(J(['PNP-RESIDUAL-v1',instance,gid,'FP51-ENERGY-TABLE-v1',ch,mh]))
 a=json.loads(zlib.decompress(base64.b64decode(C['dual_b64'])));assert len(a)==C['proof_rows'] and len({i for i,x,y in a})==len(a) and all(y>0 for i,x,y in a);L=math.lcm(*(y for i,x,y in a));Y={i:x*(L//y) for i,x,y in a};S=[set(q['vs']) for q in F];scopes={tuple(sorted(s)) for s in S}
 for A,B in it.combinations(S,2):
  if A&B and len(A|B)<=5:scopes.add(tuple(sorted(A|B)))
 scopes=sorted(scopes,key=lambda x:(len(x),x));ref={};W=co.defaultdict(lambda:co.defaultdict(int));total=0;row=0
 for V in scopes:
  if row in Y:w=Y.pop(row);W[V][((),0)]+=w;total+=w
  row+=1
  for k in range(1,len(V)+1):
   for T in it.combinations(V,k):
    if T not in ref:ref[T]=V;continue
    B=ref[T]
    for z in range(2**k):
     if row in Y:w=Y.pop(row);W[V][(T,z)]+=w;W[B][(T,z)]-=w
     row+=1
 assert not Y and total<0;checks=rows=0
 for V,Q in W.items():
  I=[i for i,s in enumerate(S) if s<=set(V)];assert set(V)=={v for i in I for v in S[i]}
  for b in it.product((0,1),repeat=len(V)):
   h=dict(zip(V,b))
   for i in I:
    q=F[i];checks+=1
    if q['cost'][sum(h[v]<<j for j,v in enumerate(q['vs']))]:break
   else:
    rows+=1;checks+=len(Q);assert sum(w for (T,z),w in Q.items() if sum(h[v]<<j for j,v in enumerate(T))==z)>=0
 return dict(status='NO under guard; global complement discharges',regions=len(W),rows=rows,checks=checks,negative_constant=total,projection_checks=pre,certificate_sha256=H(cert))
if __name__=='__main__':print(verify(*(Path(x).read_bytes() for x in sys.argv[1:])))
