"""Independent T1-10 checker; Python stdlib, no discovery solver imported.
Usage: python verify10.py INPUT.eb.json CERT.json (do not use -O).
Exact chart policy matches the prior pinned verify09.py, with factor rows retained.
"""
import json,hashlib,itertools as I,collections as C,sys
from pathlib import Path
H=lambda b:hashlib.sha256(b).hexdigest()
enc=lambda o:(json.dumps(o,separators=(',',':'))+'\n').encode()
words=lambda n:I.product((0,1),repeat=n)

def project(raw):
 g=json.loads(raw);n=4*len(g['types']);assert g['format']=='STRICT-EB4-v1' and set(g['types'])<=set('EB');assert sorted(p for a,b,s in g['edges'] for p in (a,b))==list(range(n));assert all(a//4!=b//4 and s in (0,1) for a,b,s in g['edges']);assert len({tuple(sorted((a//4,b//4))) for a,b,s in g['edges']})==len(g['edges']);adj=[[] for _ in range(n)]
 for a,b,s in g['edges']:adj[a].append((b,s));adj[b].append((a,s))
 for v,t in enumerate(g['types']):
  if t=='E':
   for j in (1,2,3):a=4*v;b=a+j;adj[a].append((b,0));adj[b].append((a,0))
 p=[None]*n;ops=0
 for i in range(n):
  if p[i] is not None:continue
  p[i]=(i,0);queue=[i]
  for a in queue:
   for b,s in adj[a]:
    ops+=1;z=(i,p[a][1]^s)
    if p[b] is None:p[b]=z;queue.append(b)
    else:assert p[b]==z
 D={}
 for v,t in enumerate(g['types']):
  if t!='B':continue
  obs=p[4*v:4*v+4];xs=tuple(sorted({u for u,s in obs}));rr=[]
  for w in words(len(xs)):
   ops+=1
   if sum(w[xs.index(u)]^s for u,s in obs)==2:rr.append(w)
  D.setdefault((xs,tuple(rr)),[]).append(v)
 F=[(v,r,tuple(s)) for (v,r),s in D.items()];tr=[]
 while True:
  inc=C.defaultdict(list)
  for i,(v,r,s) in enumerate(F):
   for x in v:inc[x].append(i);ops+=1
  cand=[]
  for x,ids in inc.items():
   sc=tuple(sorted({y for i in ids for y in F[i][0]}));ops+=sum(len(F[i][0]) for i in ids)
   if len(sc)<=6:cand.append((len(sc),len(ids),x,ids,sc))
  if not cand:break
  _,_,x,ids,sc=min(cand);B=[F[i] for i in ids];keep=tuple(y for y in sc if y!=x);S=tuple(sorted({s for v,r,ss in B for s in ss}));rows=[]
  for w in words(len(keep)):
   a=dict(zip(keep,w));possible=False
   for bit in (0,1):
    a[x]=bit;ok=True
    for v,r,s in B:
     ops+=1
     if tuple(a[y] for y in v) not in r:ok=False;break
    possible|=ok
   if possible:rows.append(w)
  tr.append((x,sc,S));F=[f for i,f in enumerate(F) if i not in ids]+[(keep,tuple(rows),S)]
  if not rows:break
 return F,p,tr,ops

def replay(F,guard,tree,stats):
 a=dict(guard);stats[0]+=1
 while True:
  prop=C.defaultdict(set)
  for v,r,s in F:
   keep=[]
   for w in r:
    stats[1]+=1
    if all(x not in a or a[x]==b for x,b in zip(v,w)):keep.append(w)
   if not keep:return True
   for i,x in enumerate(v):
    vals={w[i] for w in keep}
    if len(vals)==1:prop[x].update(vals)
  if any(len(b)!=1 or (x in a and a[x] not in b) for x,b in prop.items()):return True
  new={x:next(iter(b)) for x,b in prop.items() if x not in a}
  if not new:break
  a.update(new)
 if not isinstance(tree,list) or len(tree)!=3:return False
 x,L,R=tree
 if x not in {y for v,r,s in F for y in v}:return False
 if x in a:return replay(F,a,L if a[x]==0 else R,stats)
 return replay(F,{**a,x:0},L,stats) and replay(F,{**a,x:1},R,stats)

def verify(raw,cert):
 z=json.loads(cert);iid='STRICT-EB4-v1:sha256:'+H(raw);assert iid==z['instance_id'] and len(raw)*8==z['original_N_bits'];assert z['guard_id']=='EMPTY' and z['residual_id']=='ROOT';F,p,tr,ops=project(raw);ch=H(enc({'F':F,'trace':tr}));mh=H(enc(p));assert ch==z['chart_sha256'] and mh==z['map_sha256'];rid='RESIDUAL-v1:sha256:'+H(enc(['PNP-RESIDUAL-v1',iid,'EMPTY','EB-WIDTH6-FACTOR-v1',ch,mh]));assert rid==z['internal_residual_id'];ids=z['omitted_factor_ids'];assert len(ids)==len(set(ids)) and all(type(x)==int and 0<=x<len(F) for x in ids);assert sorted({s for i in ids for s in F[i][2]})==z['omitted_balance_ids'];A=[f for i,f in enumerate(F) if i not in set(ids)];stats=[0,0];assert replay(A,{},z['proof_tree'],stats);print(z['instance'],'VERIFIED UNSAT by subset',len(A),'of',len(F),'factors; projection logical operations',ops,'tree visits',stats[0],'row checks',stats[1],'certificate_id','CERT-v1:sha256:'+H(cert));return F

if __name__=='__main__':verify(Path(sys.argv[1]).read_bytes(),Path(sys.argv[2]).read_bytes())
