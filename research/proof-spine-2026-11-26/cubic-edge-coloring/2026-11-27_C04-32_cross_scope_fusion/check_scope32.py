"""Independent source-level replay of local contextual contraction certificate."""
import json,hashlib,itertools as it,sys,collections as co
from pathlib import Path

def check(raw,c):
 d=json.loads(raw); assert d['format']=='STRICT-EB4-v1'; n=len(d['types']);assert c['instance_id']=='STRICT-EB4-v1:sha256:'+hashlib.sha256(raw).hexdigest() and c['original_N_bits']==8*len(raw);assert c['guard_id']=='EMPTY' and c['residual_id']=='ROOT'
 adj=[[] for _ in range(4*n)];ports=set();pairs=set()
 def link(a,b,s):adj[a].append((b,s));adj[b].append((a,s))
 for a,b,s in d['edges']:
  assert 0<=a<4*n and 0<=b<4*n and a//4!=b//4 and a not in ports and b not in ports and s in (0,1)
  uv=tuple(sorted([a//4,b//4]));assert uv not in pairs;pairs.add(uv);ports.update((a,b));link(a,b,s)
 assert len(ports)==4*n
 for v,t in enumerate(d['types']):
  assert t in ('B','E')
  if t=='E':
   for j in range(1,4):link(4*v,4*v+j,0)
 root=[None]*(4*n);par=[0]*(4*n);arcs=0
 for r in range(4*n):
  if root[r] is not None:continue
  root[r]=r;Q=[r]
  for a in Q:
   for b,s in adj[a]:
    arcs+=1
    if root[b] is None:root[b]=r;par[b]=par[a]^s;Q.append(b)
    else:assert root[b]==r and par[b]==par[a]^s
 rows={v:[(root[4*v+j],par[4*v+j]) for j in range(4)] for v,t in enumerate(d['types']) if t=='B'};occ=co.defaultdict(set)
 for v,w in rows.items():
  for r,s in w:occ[r].add(v)
 tabs=[];vis=0;witness=[]
 for g in c['groups']:
  ids=g['B_ids'];scope=g['scope'];private=g['private'];assert sorted(set(scope+private))==sorted({r for v in ids for r,s in rows[v]});assert not set(scope)&set(private);assert all(occ[r]<=set(ids) for r in private)
  T=[];W=[]
  for z in it.product((0,1),repeat=len(scope)):
   # table indexing is little-endian, not itertools order
   pass
  for z in range(1<<len(scope)):
   h={r:z>>j&1 for j,r in enumerate(scope)};w0=None
   for y in range(1<<len(private)):
    h.update({r:y>>j&1 for j,r in enumerate(private)});vis+=len(ids)
    if all(sum(h[r]^s for r,s in rows[v])==2 for v in ids):w0=y;break
   T.append(w0 is not None);W.append(w0)
  assert T==g['table'];tabs.append((scope,T));witness.append(W)
 A,R=tabs[0];B,S=tabs[1];C=c['replacement']['scope'];T=c['replacement']['table'];assert set(C)<set(B);U=sorted(set(A)|set(B));checks=0
 for z in range(1<<len(U)):
  m={r:z>>j&1 for j,r in enumerate(U)};v=lambda X,Y:Y[sum(m[r]<<j for j,r in enumerate(X))];assert (v(A,R) and v(B,S))==(v(A,R) and v(C,T));checks+=1
 assert set(c['groups'][0]['B_ids']).isdisjoint(c['groups'][1]['B_ids']);return {'arcs':arcs,'private_row_checks':vis,'equivalence_checks':checks,'witness_private_bitmasks':witness,'status':'PASS'}
if __name__=='__main__':print(json.dumps(check(Path(sys.argv[1]).read_bytes(),json.loads(Path(sys.argv[2]).read_bytes())),sort_keys=True))
