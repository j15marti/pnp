# Standalone certificate checker, no dependency on discovery code.
import json,hashlib,itertools as I,collections as C,sys
from pathlib import Path
H=lambda b:hashlib.sha256(b).hexdigest()
def enc(x):return (json.dumps(x,separators=(',',':'))+'\n').encode()
def words(n):return I.product((0,1),repeat=n)
def check(path,native):
 c=json.loads(Path(path).read_bytes());raw=Path(native).read_bytes();assert H(raw)==c['instance_id'].split(':')[-1] and 8*len(raw)==c['N'];g=json.loads(raw);V=len(g['types']);P=4*V;assert g['format']=='STRICT-EB4-v1' and all(t in ('E','B') for t in g['types']);adj=[[] for _ in range(P)];seen=set();pairs=set();work=C.Counter()
 for a,b,s in g['edges']:
  assert 0<=a<P and 0<=b<P and a//4!=b//4 and s in (0,1) and a not in seen and b not in seen;seen.update((a,b));k=tuple(sorted((a//4,b//4)));assert k not in pairs;pairs.add(k);adj[a].append((b,s));adj[b].append((a,s));work['edges']+=1
 assert len(seen)==P
 for v,t in enumerate(g['types']):
  if t=='E':
   for j in (1,2,3):a=4*v;b=a+j;adj[a].append((b,0));adj[b].append((a,0))
 p=[None]*P
 for root in range(P):
  if p[root] is not None:continue
  p[root]=(root,0);q=[root]
  for a in q:
   for b,s in adj[a]:
    y=(root,p[a][1]^s);work['transport_checks']+=1
    if p[b] is None:p[b]=y;q.append(b)
    else:assert p[b]==y
 D={}
 for v,t in enumerate(g['types']):
  if t=='B':
   obs=p[4*v:4*v+4];X=tuple(sorted({x for x,s in obs}));R=[]
   for w in words(len(X)):
    a=dict(zip(X,w));work['native_rows']+=1
    if sum(a[x]^s for x,s in obs)==2:R.append(w)
   D.setdefault((X,tuple(R)),[]).append(v)
 F=[(v,r,tuple(s)) for (v,r),s in D.items()]
 # Recompute exact width-six elimination, same deterministic pivot choice, different kept-row enumeration.
 while True:
  inc=C.defaultdict(list)
  for i,(v,r,s) in enumerate(F):
   for x in v:inc[x].append(i);work['index']+=1
  cand=[]
  for x,ids in inc.items():
   sc=tuple(sorted(set().union(*(set(F[i][0]) for i in ids))))
   if len(sc)<=6:cand.append((len(sc),len(ids),x,ids,sc))
  if not cand:break
  _,_,x,ids,sc=min(cand);keep=tuple(y for y in sc if y!=x);B=[F[i] for i in ids];S=tuple(sorted(set().union(*(set(f[2]) for f in B))));R=[]
  for w in words(len(keep)):
   a=dict(zip(keep,w))
   for b in (0,1):
    a[x]=b;work['projection_checks']+=1
    if all(tuple(a[y] for y in v) in r for v,r,s in B):R.append(w);break
  F=[f for i,f in enumerate(F) if i not in set(ids)]+[(keep,tuple(R),S)]
  if not R:break
 X=sorted({x for v,r,s in F for x in v});assert X==c['X'];assert H(enc(F))==c['factor_sha'] and H(enc(p))==c['map_sha'];n=len(X)
 def propagate(T,G):
  a=dict(G)
  while True:
   req=C.defaultdict(set)
   for v,r,s in T:
    R=[]
    for w in r:
     work['support_rows']+=1
     if all(x not in a or a[x]==b for x,b in zip(v,w)):R.append(w)
    if not R:return None
    for j,x in enumerate(v):
     if all(w[j]==R[0][j] for w in R):req[x].add(R[0][j])
   if any(len(b)>1 or x in a and a[x] not in b for x,b in req.items()):return None
   new={x:next(iter(b)) for x,b in req.items() if x not in a}
   if not new:return a
   a.update(new)
 good=[]
 for item in c['guards']:
  G=dict(item['pins']);gid='GUARD-v1:sha256:'+H(enc(['PNP-GUARD-v1',c['instance_id'],'EB-PORT-PINS-v1',H(enc(item['pins']))]));assert gid==item['guard_id'];assert item['residual_id']=='RESIDUAL-v1:sha256:'+H(enc(['PNP-RESIDUAL-v1',c['instance_id'],gid,'EB-FACTOR-TABLE-v1',c['factor_sha'],c['map_sha']]))
  T=list(F);terminal=False
  for x,kind,rows in item['trace']:
   assert x in X and x not in G;assert propagate(T,G) is not None;A=[propagate(T,{**G,x:b}) for b in (0,1)]
   if kind=='both':assert A==[None,None] and not rows;terminal=True;break
   for e in rows:
    assert 0<e<1<<(n+1);v=tuple(y for i,y in enumerate(X) if e>>i&1);b=e>>n;assert 1<=len(v)<=2
    for a in A:
     if a is not None:assert all(y in a for y in v) and sum(a[y] for y in v)%2==b
    T.append((v,tuple(w for w in words(len(v)) if sum(w)%2==b),()))
  assert terminal or propagate(T,G) is None;good.append(G)
 if c['claim']=='ROOT_NO':
  union=0
  for j in range(1,len(good)+1):
   for J in I.combinations(good,j):
    a={};ok=True
    for G in J:
     for x,b in G.items():
      if x in a and a[x]!=b:ok=False
      a[x]=b
    union+=(-1)**(j+1)*(2**(n-len(a)) if ok else 0)
  assert union==2**n
 else:assert c['claim']=='EXCLUDE_LISTED_GUARDS'
 print(c['claim'],len(good),dict(work),'certificate_sha',H(Path(path).read_bytes()))
 return work
if __name__=='__main__':check(sys.argv[1],sys.argv[2])
