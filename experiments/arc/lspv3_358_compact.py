#!/usr/bin/env python3
"""Deterministic full lifted-K4 ER2 certificate; output is checked separately."""
import itertools,json
from pathlib import Path
E=list(itertools.combinations(range(4),2)); charge=(1,0,0,0)
def norm(ls):
 s=set(ls)
 return None if any(-x in s for x in s) else tuple(sorted(s,key=lambda z:(abs(z),z)))
source=[]
for v in range(4):
 inc=[i for i,e in enumerate(E) if v in e]
 for xs in itertools.product((0,1),repeat=6):
  if sum(xs[2*j]&xs[2*j+1] for j in range(3))%2==charge[v]:continue
  source.append({'v':v,'clause':norm((-1 if xs[2*j+b] else 1)*(2*inc[j]+b+1) for j in range(3) for b in range(2))})
entries={f'S{i}':s['clause'] for i,s in enumerate(source)};idx={v:k for k,v in entries.items()};defs=[];steps=[]
for i in range(6):
 a,b,z=2*i+1,2*i+2,13+i;slots=[norm(x) for x in [(-z,a),(-z,b),(z,-a,-b)]]
 defs.append({'id':f'D{i}','output':z,'a':a,'b':b,'slots':slots})
 for j,s in enumerate(slots):entries[f'D{i}.{j}']=s;idx.setdefault(s,f'D{i}.{j}')
def res(ra,rb,p):
 a=set(entries[ra]);b=set(entries[rb]);assert p in a and -p in b
 c=norm((a-{p})|(b-{-p}))
 if c is None:return None
 if c not in idx:
  r=f'R{len(steps)}';steps.append({'id':r,'left':ra,'right':rb,'pivot':p,'clause':c});entries[r]=c;idx[c]=r
 return idx[c]
parity=[]
for v in range(4):
 inc=[i for i,e in enumerate(E) if v in e]
 active={entries[r]:r for r in [f'S{j}' for j,s in enumerate(source) if s['v']==v]+[f'D{i}.{k}' for i in inc for k in range(3)]}
 for i in inc:
  for p in (2*i+1,2*i+2):
   plus=[r for c,r in active.items() if p in c];minus=[r for c,r in active.items() if -p in c]
   nxt={c:r for c,r in active.items() if p not in c and -p not in c}
   for a in plus:
    for b in minus:
     r=res(a,b,p)
     if r is not None:nxt[entries[r]]=r
   active=nxt
 for xs in itertools.product((0,1),repeat=3):
  if sum(xs)%2==charge[v]:continue
  c=norm((-1 if xs[j] else 1)*(13+inc[j]) for j in range(3));assert c in active
  parity.append(active[c])
queue=list(parity); seen={entries[r] for r in queue};final=None
for i in range(10000):
 if i>=len(queue):break
 a=queue[i]
 for b in queue[:i]:
  for x,y in ((a,b),(b,a)):
   for p in entries[x]:
    if -p not in entries[y]:continue
    r=res(x,y,p)
    if r is not None and entries[r] not in seen:
     seen.add(entries[r]);queue.append(r)
     if not entries[r]:final=r;break
   if final:break
  if final:break
 if final:break
assert final
byid={s['id']:s for s in steps};used=set();stack=[final]
while stack:
 r=stack.pop()
 if r in used or r not in byid:continue
 used.add(r);stack.extend((byid[r]['left'],byid[r]['right']))
retained=[s for s in steps if s['id'] in used]
dids={p.split('.')[0] for s in retained for p in (s['left'],s['right']) if p.startswith('D')}
out={'charges':charge,'edges':E,'sources':source,'definitions':[d for d in defs if d['id'] in dids], 'steps':retained,'final':final,'summary':{'source_clauses':len(source),'definitions':len(dids),'resolution_nodes':len(retained),'logical_nodes':len(dids)+len(retained)}}
assert len(source)==120 and len(dids)==6 and len(retained)==307
Path('lspv3_358_complete_k4.json').write_text(json.dumps(out,indent=1)+'\n')
print(out['summary'])
