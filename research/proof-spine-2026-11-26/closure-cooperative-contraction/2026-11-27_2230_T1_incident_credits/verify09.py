# Independent root certificate verifier; Python 3 standard library only.
import json, hashlib, itertools as I, collections as C, sys
from pathlib import Path
H=lambda b:hashlib.sha256(b).hexdigest()
enc=lambda o:(json.dumps(o,separators=(',',':'))+'\n').encode()
words=lambda n:I.product((0,1),repeat=n)
def chart(raw):
 g=json.loads(raw);P=4*len(g['types']);assert g['format']=='STRICT-EB4-v1' and set(g['types'])<=set('EB')
 assert sorted(x for a,b,s in g['edges'] for x in (a,b))==list(range(P))
 assert all(a//4!=b//4 and s in (0,1) for a,b,s in g['edges']);assert len({tuple(sorted((a//4,b//4))) for a,b,s in g['edges']})==len(g['edges'])
 adj=[[] for _ in range(P)]
 for a,b,s in g['edges']:adj[a].append((b,s));adj[b].append((a,s))
 for v,t in enumerate(g['types']):
  if t=='E':
   for j in (1,2,3):a=4*v;b=a+j;adj[a].append((b,0));adj[b].append((a,0))
 p=[None]*P
 for i in range(P):
  if p[i] is not None:continue
  p[i]=(i,0);q=[i]
  for a in q:
   for b,s in adj[a]:
    z=(i,p[a][1]^s)
    if p[b] is None:p[b]=z;q.append(b)
    else:assert p[b]==z
 F={}
 for v,t in enumerate(g['types']):
  if t=='B':
   obs=p[4*v:4*v+4];xs=tuple(sorted({u for u,s in obs}));rr=tuple(w for w in words(len(xs)) if sum(w[xs.index(u)]^s for u,s in obs)==2);F.setdefault((xs,rr),[]).append(v)
 F=[(v,r,tuple(s)) for (v,r),s in F.items()];tr=[]
 while True:
  inc=C.defaultdict(list)
  for i,(v,r,s) in enumerate(F):
   for x in v:inc[x].append(i)
  cand=[]
  for x,ids in inc.items():
   sc=tuple(sorted({y for i in ids for y in F[i][0]}))
   if len(sc)<=6:cand.append((len(sc),len(ids),x,ids,sc))
  if not cand:break
  _,_,x,ids,sc=min(cand);B=[F[i] for i in ids];keep=tuple(y for y in sc if y!=x);S=tuple(sorted({s for v,r,ss in B for s in ss}));rows=[]
  for w in words(len(keep)):
   a=dict(zip(keep,w))
   for bit in (0,1):
    a[x]=bit
    if all(tuple(a[y] for y in v) in r for v,r,s in B):rows.append(w);break
  tr.append((x,sc,S));F=[f for i,f in enumerate(F) if i not in ids]+[(keep,tuple(rows),S)]
  if not rows:break
 D=sorted({tuple(sorted(x+1 if not b else -x-1 for x,b in zip(v,w))) for v,r,s in F for w in words(len(v)) if w not in r})
 return D,H(enc({'F':F,'trace':tr})),H(enc(p)),p

def rup(D,proof):
 D=list(D);seen=set(D);visits=0
 for cc in proof:
  cc=tuple(cc);assert cc not in seen and len(cc)<=2 and len(set(map(abs,cc)))==len(cc)
  a={abs(l):l<0 for l in cc};conflict=False
  while True:
   changed=False
   for c in D:
    visits+=len(c)+1
    if any(a.get(abs(l))==(l>0) for l in c):continue
    u=[l for l in c if abs(l) not in a]
    if not u:conflict=True;break
    if len(u)==1:a[abs(u[0])]=u[0]>0;changed=True
   if conflict or not changed:break
  assert conflict;D.append(cc);seen.add(cc)
 assert () in seen
 return visits

def verify(raw,cert):
 z=json.loads(cert);ident='STRICT-EB4-v1:sha256:'+H(raw);assert ident==z['instance_id'] and len(raw)*8==z['original_N_bits']
 D,ch,mp,p=chart(raw);a=z['internal'];assert ch==a['chart_sha256'] and mp==a['map_sha256'] and H(enc(D))==a['ungauged_cnf_sha256']
 assert p[10]==(10,0) and a['guard_pins']==[[10,0]];gid='GUARD-v1:sha256:'+H(enc(['PNP-GUARD-v1',ident,'EB-PORT-PINS-v1',H(enc([[10,0]]))]));assert gid==a['guard_id']
 for g,k in [('EMPTY','ungauged_residual_id'),(gid,'guarded_residual_id')]:assert 'RESIDUAL-v1:sha256:'+H(enc(['PNP-RESIDUAL-v1',ident,g,a['chart_schema'],ch,mp]))==a[k]
 # Native edges and E/B are invariant under global complement; chart also checked.
 assert {tuple(sorted(-l for l in c)) for c in D}==set(D)
 DG=sorted({tuple(l for l in c if l!=11) for c in D if -11 not in c});assert H(enc(DG))==a['gauge_cnf_sha256']
 visits=rup(DG,z['proof']);u=z['ungauged_proof'];refusal=z['ungauged_refusal_min_width']
 if u:visits+=rup(D,u)
 else:assert refusal==min(map(len,D)) and refusal>=4 and all(len(set(map(abs,c)))==len(c) for c in D)
 print(z['instance'],'verified root NO; width-two ungauged', 'NO' if u else 'FIXED_POINT','scalar row/literal events',visits,'certificate_id','CERT-v1:sha256:'+H(cert))
if __name__=='__main__':verify(Path(sys.argv[1]).read_bytes(),Path(sys.argv[2]).read_bytes())
