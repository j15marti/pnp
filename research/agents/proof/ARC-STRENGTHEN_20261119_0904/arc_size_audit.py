#!/usr/bin/env python3
import itertools,json,hashlib
from collections import Counter
from pathlib import Path
R=lambda a,b:(b-a)%5 in (1,3)
words=['BBB','FBB','FFF','BB']
edges=[]; groups=[];nv=2
for w in words:
 vs=[0]+list(range(nv,nv+len(w)-1))+[1];nv+=len(w)-1;group=[]
 for a,b,d in zip(vs,vs[1:],w):
  group.append(len(edges));edges.append((a,b) if d=='F' else (b,a))
 groups.append(group)
counts=[0]*len(edges);witnesses={};full=0
for tail in itertools.product(range(5),repeat=nv-1):
 x=(0,)+tail;bad=[]
 for j,(u,v) in enumerate(edges):
  if not R(x[u],x[v]):
   bad.append(j)
   if len(bad)>1:break
 if not bad:full+=1
 if len(bad)==1:
  j=bad[0];counts[j]+=5;witnesses.setdefault(j,x)
assert full==0 and all(counts)
rels=[]
weights=[]
for w in words:
 d={0}
 weight=Counter({0:1})
 for c in w:d={(x+y)%5 for x in d for y in ((1,3) if c=='F' else (2,4))}
 for c in w:
  nxt=Counter()
  for x,count in weight.items():
   for y in ((1,3) if c=='F' else (2,4)):nxt[(x+y)%5]+=count
  weight=nxt
 rels.append(d)
 weights.append(weight)
for t,g in enumerate(groups):
 core=[d for d in range(5) if all(d in s for j,s in enumerate(rels) if j!=t)]
 weighted=0
 for d in core:
  term=1
  for j,weight in enumerate(weights):
   if j!=t:term*=weight[d]
  weighted+=term
 expect=5*weighted*2**(len(words[t])-1)
 assert all(counts[j]==expect for j in g)
 for j in g:assert all(R(witnesses[j][u],witnesses[j][v]) for k,(u,v) in enumerate(edges) if k!=j)
# A second deletion with the same designation destroys its critical promise.
for e in range(len(edges)):
 for f in range(len(edges)):
  if f==e:continue
  assert all(R(witnesses[f][u],witnesses[f][v]) for k,(u,v) in enumerate(edges) if k!=f)
src=Path('source079.t5').read_bytes()
assert hashlib.sha256(src).hexdigest()=='0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac'
E=[tuple(map(int,l.split()[1:])) for l in src.decode().splitlines() if l.startswith('a ')]
adj=[[] for _ in range(33)]
for j,(u,v) in enumerate(E):adj[u].append((v,j));adj[v].append((u,j))
B={v for v in range(33) if len(adj[v])!=2};seen=set();threads=[]
for u in sorted(B):
 for v,j in adj[u]:
  if j in seen:continue
  length=1;seen.add(j);previous=u;current=v
  while current not in B:
   nxt,k=next((w,k) for w,k in adj[current] if w!=previous)
   seen.add(k);length+=1;previous,current=current,nxt
  threads.append((u,current,length))
b=len(B);q=len(threads);m=len(E);n=33
assert len(seen)==m and max(t[2] for t in threads)<=3
assert n==b+sum(l-1 for _,_,l in threads) and m==sum(l for _,_,l in threads)
assert q<=4*b*(b-1)//2 and n<=4*b*b-3*b
result={"fixture9":{"n":nv,"m":len(edges),"b":2,"q":4,"deletion_counts":counts,"witnesses":witnesses,
"double_deletion_same_designation_checks":110},
"source079":{"sha256":hashlib.sha256(src).hexdigest(),"n":n,"m":m,"b":b,"q":q,
"thread_lengths":dict(Counter(l for _,_,l in threads)),"original_records":n+m,"core_records":b+q},
"scope":"n9 exhaustive; source079 structure only, not a fresh UNSAT certificate replay"}
print(json.dumps(result,indent=2))
