"""Independent T1-11 replay. No discovery implementation imported. Run without -O."""
import json,itertools as I,hashlib,sys
from pathlib import Path
H=lambda b:hashlib.sha256(b).hexdigest()
enc=lambda x:(json.dumps(x,separators=(',',':'))+'\n').encode()

def check_chart(raw,q,maps):
 g=json.loads(raw);root=maps['root'];phase=maps['phase'];n=4*len(g['types']);assert g['format']=='STRICT-EB4-v1' and set(g['types'])<=set('EB') and len(root)==len(phase)==n
 assert sorted(x for a,b,s in g['edges'] for x in (a,b))==list(range(n)) and all(a//4!=b//4 and s in (0,1) for a,b,s in g['edges']) and len({tuple(sorted((a//4,b//4))) for a,b,s in g['edges']})==len(g['edges'])
 par=list(range(n));ops=0
 def find(a):
  while par[a]!=a:par[a]=par[par[a]];a=par[a]
  return a
 def edge(a,b,s):
  nonlocal ops;ops+=1;assert root[a]==root[b] and phase[a]^phase[b]==s;u,v=find(a),find(b);par[max(u,v)]=min(u,v)
 for a,b,s in g['edges']:edge(a,b,s)
 for i,t in enumerate(g['types']):
  if t=='E':
   for j in range(1,4):edge(4*i,4*i+j,0)
 for i in range(n):ops+=1;assert root[i]==find(i) and phase[root[i]]==0
 def truth(f,a):return sum(a[v]<<i for i,v in enumerate(f['s'])) in f['a']
 seen=set();live={}
 for f in q['raw']:
  assert f['id'] not in live
  for v in f['B']:
   assert g['types'][v]=='B' and v not in seen;seen.add(v);s=sorted(set(root[4*v:4*v+4]));assert s==f['s'];allowed=[]
   for b in range(1<<len(s)):
    ops+=1;a={x:b>>i&1 for i,x in enumerate(s)}
    if sum(a[root[p]]^phase[p] for p in range(4*v,4*v+4))==2:allowed.append(b)
   assert allowed==f['a']
  live[f['id']]=f
 assert seen=={v for v,t in enumerate(g['types']) if t=='B'}
 anchor=q['anchor'];assert anchor==10
 # global complement is exact by edge XOR and B4 sum=2, E4 equality. Guard restriction then existential projection.
 for z in q['cond']:
  f=live.pop(z['input']);o=z['out'];assert anchor in f['s'] and o['id'] not in live and o['s']==[v for v in f['s'] if v!=anchor];A=[]
  for w in range(1<<len(o['s'])):
   a={v:w>>j&1 for j,v in enumerate(o['s'])};a[anchor]=0;ops+=1
   if truth(f,a):A.append(w)
  assert A==o['a'];live[o['id']]=o
 assert all(anchor not in f['s'] for f in live.values())
 for z in q['steps']:
  x=z['v'];ids=z['inputs'];o=z['out'];assert sorted(ids)==sorted(i for i,f in live.items() if x in f['s']) and o['id'] not in live
  fs=[live[i] for i in ids];B=sorted({v for f in fs for v in f['s']}-{x});assert o['s']==B;A=[];W=[]
  for w in range(1<<len(B)):
   a={v:w>>i&1 for i,v in enumerate(B)};good=[]
   for bit in (0,1):
    a[x]=bit;ops+=len(fs)
    if all(truth(f,a) for f in fs):good.append(bit)
   if good:A.append(w);W.append(min(good))
  assert A==o['a'] and W==z['w'];[live.pop(i) for i in ids];live[o['id']]=o
 assert list(live.values())==q['final'];C=set()
 for f in live.values():
  for w in range(1<<len(f['s'])):
   ops+=1
   if w not in f['a']:C.add(frozenset((v+1)*(-1 if w>>i&1 else 1) for i,v in enumerate(f['s'])))
 assert C==set(map(frozenset,q['clauses']));return ops

def check_tree(F,t):
 count=[0,0]
 def rec(t,a):
  count[0]+=1
  while True:
   forced={};bad=False
   for c in F:
    count[1]+=len(c)
    if any(a.get(abs(l))==int(l>0) for l in c):continue
    u=[l for l in c if abs(l) not in a]
    if not u:return
    if len(u)==1:
     l=u[0];v=abs(l);b=int(l>0)
     if v in forced and forced[v]!=b:return
     forced[v]=b
   if not forced:break
   a={**a,**forced}
  assert len(t)==3;v,L,R=t;assert v in {abs(l) for c in F for l in c}
  if v in a:rec(L if a[v]==0 else R,a)
  else:rec(L,{**a,v:0});rec(R,{**a,v:1})
 rec(t,{});return count

def check_cert(name,z):
 raw=Path(name+'.eb.json').read_bytes();qraw=Path(name+'.T111.chart.json').read_bytes();mraw=Path(name+'.T111.maps.json').read_bytes();assert z['instance_id']=='STRICT-EB4-v1:sha256:'+H(raw) and len(raw)*8==z['original_N_bits'];assert H(qraw)==z['chart_sha256'] and H(mraw)==z['map_sha256'];q=json.loads(qraw);m=json.loads(mraw);op=check_chart(raw,q,m);F=q['clauses'];x=z['pivot'];assert z['omitted_clause_indices']==[i for i,c in enumerate(F) if x in c or -x in c];D=[c for i,c in enumerate(F) if i not in set(z['omitted_clause_indices'])];return op,check_tree(D,z['proof_tree'])
if __name__=='__main__':
 name=sys.argv[1];z=json.loads(Path(name+'.T111.cert.json').read_bytes());print(name,check_cert(name,z),H(Path(name+'.T111.cert.json').read_bytes()))
