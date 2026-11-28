"""Replay a root parity-relaxation admission prefix against exact original E/B bytes.
Usage: python prefix-check.py INSTANCE.eb.json INSTANCE.prefix.json
"""
import json,hashlib,sys
from pathlib import Path

def check(raw,cert):
 g=json.loads(raw);n=4*len(g['types']);assert g['format']=='STRICT-EB4-v1' and set(g['types'])<=set('EB');assert cert['instance_id']=='STRICT-EB4-v1:sha256:'+hashlib.sha256(raw).hexdigest() and cert['original_N_bits']==len(raw)*8;assert cert['guard_id']=='EMPTY' and cert['residual_id']=='ROOT';assert sorted(x for a,b,s in g['edges'] for x in (a,b))==list(range(n));assert len({tuple(sorted((a//4,b//4))) for a,b,s in g['edges']})==len(g['edges']) and all(a//4!=b//4 and s in (0,1) for a,b,s in g['edges']);adj=[[] for _ in range(n)]
 def link(a,b,s):adj[a].append((b,s));adj[b].append((a,s))
 for a,b,s in g['edges']:link(a,b,s)
 for v,t in enumerate(g['types']):
  if t=='E':
   for j in range(1,4):link(4*v,4*v+j,0)
 p=[None]*n;k=0;reads=0
 for i in range(n):
  if p[i] is not None:continue
  p[i]=(k,0);q=[i];k+=1
  for a in q:
   for b,s in adj[a]:
    reads+=1;z=(p[a][0],p[a][1]^s)
    if p[b] is None:p[b]=z;q.append(b)
    else:assert p[b]==z
 active=set();checks=0
 for st in cert['steps']:
  x=int(st['carrier_word'],16);assert 0<=x<1<<k;v=[(x>>i&1)^s for i,s in p];owners=set(st['owners']);assert owners and not owners&active and all(0<=i<len(g['types']) and g['types'][i]=='B' for i in owners)
  for a,b,s in g['edges']:assert v[a]^v[b]==s;checks+=1
  for i,t in enumerate(g['types']):
   w=sum(v[4*i:4*i+4]);checks+=1
   if t=='E':assert w in (0,4)
   else:assert w%2==0 and (i not in active or w==2)
  assert any(sum(v[4*i:4*i+4])!=2 for i in owners);active|=owners
 return {'checked_steps':len(cert['steps']),'activated_original_B4':len(active),'transport_reads':reads,'constraint_checks':checks}
if __name__=='__main__':print(check(Path(sys.argv[1]).read_bytes(),json.loads(Path(sys.argv[2]).read_bytes())))
