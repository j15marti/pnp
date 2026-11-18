#!/usr/bin/env python3
"""TMR-2/072 finite independent T5 successor-ring tests, seed 20261117."""
import itertools,json,random
from collections import Counter,defaultdict
SEED=20261117
R=lambda x,y:(y-x)%5 in (1,3)
checks=0
def check(p):
 global checks
 checks+=1
 if not p:raise AssertionError(checks)
def encode(n,E):
 E=sorted(E)
 return f'p t5 {n} {len(E)}\n'+''.join(f'v {i}\n' for i in range(n))+''.join(f'a {u} {v}\n' for u,v in E)
def parse(src):
 a=src.splitlines()
 if not src.endswith('\n') or '\r' in src or len(a)<1:raise ValueError('lines')
 h=a[0].split(' ')
 if len(h)!=4 or h[:2]!=['p','t5'] or not all(s.isdecimal() and str(int(s))==s for s in h[2:]):raise ValueError('header')
 n,m=map(int,h[2:])
 if len(a)!=1+n+m or n>len(src) or m>len(src) or any(a[i+1]!=f'v {i}' for i in range(n)):raise ValueError('vertices')
 E=[]
 for line in a[n+1:]:
  q=line.split(' ')
  if len(q)!=3 or q[0]!='a' or not all(s.isdecimal() and str(int(s))==s for s in q[1:]):raise ValueError('arc')
  u,v=map(int,q[1:]);E.append((u,v))
  if max(u,v)>=n:raise ValueError('range')
 if sorted(set(E))!=E or encode(n,E)!=src:raise ValueError('canonical')
 return n,E
def lift(c,edges,k):
 t=[0]+list(range(c,c+k-1));w=list(range(c+k-1,c+2*k-1));E=list(edges)
 for i in range(k):
  a,b=t[i],t[(i+1)%k];E.extend(((a,b),(a,w[i]),(w[i],b)))
 return c+2*k-1,E

def recognize(n,E):
 E=set(E)
 if any(u==v or (v,u) in E for u,v in E):return None
 nb=[set() for _ in range(n)]
 for u,v in E:nb[u].add(v);nb[v].add(u)
 tri=[];inc=Counter();te=set()
 for a in range(n):
  for b in (z for z in nb[a] if z>a):
   for c in (z for z in nb[b] if z>b and z in nb[a]):
    T=[(s,w,z) for s,w,z in itertools.permutations((a,b,c)) if (s,w) in E and (w,z) in E and (s,z) in E]
    if len(T)!=1:return None
    s,w,z=T[0];tri.append(T[0]);te.update(((s,w),(w,z),(s,z)))
    for v in (s,w,z):inc[v]+=1
 k=len(tri);two={v for v in inc if inc[v]==2};one={v for v in inc if inc[v]==1}
 if k<5 or len(te)!=3*k or len(two)!=k or len(one)!=k or len(inc)!=2*k:return None
 succ={};pred=Counter()
 for s,w,z in tri:
  if s not in two or z not in two or w not in one or s in succ:return None
  succ[s]=z;pred[z]+=1
 if set(succ)!=two or any(pred[v]!=1 for v in two):return None
 x=next(iter(two));seen=set()
 while x not in seen:seen.add(x);x=succ[x]
 if seen!=two:return None
 core=E-te;attached={x for e in core for x in e if x in two}
 if len(attached)!=1 or any(u in one or v in one for u,v in core):return None
 anchor=next(iter(attached));V=set(range(n))-one-(two-{anchor})
 if len(V)<2 or not core or any(u not in V or v not in V for u,v in core):return None
 indeg=Counter(v for u,v in core);outdeg=Counter(u for u,v in core)
 if any(indeg[v] and outdeg[v] for v in V):return None
 adj=defaultdict(set)
 for u,v in core:adj[u].add(v);adj[v].add(u)
 seen={anchor};queue=[anchor]
 while queue:
  for v in adj[queue.pop()]:
   if v not in seen:seen.add(v);queue.append(v)
 if seen!=V:return None
 return dict(k=k,anchor=anchor,successor=succ,tri=tri,core=core,sources={v for v in V if outdeg[v]},sinks={v for v in V if indeg[v]})
def fast(n,E,g):
 if not g:return None
 if g['k']%5:return None
 labels=[-1]*n
 for v in g['sources']:labels[v]=0
 for v in g['sinks']:labels[v]=1
 u=g['anchor'];r=labels[u]
 for i in range(g['k']):
  z=g['successor'][u];w=next(w for s,w,t in g['tri'] if s==u and t==z)
  labels[u]=(r+i)%5;labels[w]=(r+i+3)%5;u=z
 check(all(v>=0 for v in labels) and all(R(labels[u],labels[v]) for u,v in E))
 return labels
def brute(n,E):
 # Unrestricted original five-domain backtracker. No gadget semantics used.
 adj=defaultdict(list)
 for u,v in E:adj[u].append((u,v));adj[v].append((u,v))
 # Small-instance order follows cyclic gadget, but checks only original arcs.
 g=recognize(n,E);order=[g['anchor']];u=g['anchor']
 for i in range(g['k']):
  z=g['successor'][u];w=next(w for s,w,t in g['tri'] if s==u and t==z)
  order.append(w)
  if z!=g['anchor']:order.append(z)
  u=z
 order+=sorted(set(range(n))-set(order));x=[-1]*n
 def go(d):
  if d==n:return 1
  v=order[d];total=0
  for c in range(5):
   x[v]=c
   if all(x[u]<0 or x[w]<0 or R(x[u],x[w]) for u,w in adj[v]):total+=go(d+1)
  x[v]=-1
  return total
 return go(0)
def run():
 rand=random.Random(SEED);records=[]
 for x in range(5):
  for z in range(5):check(sum(R(x,w) and R(w,z) and R(x,z) for w in range(5))==int(z==(x+1)%5))
 for a,b in ((1,1),(2,2),(2,3),(3,3)):
  c=a+b;core=[(u,a+v) for u in range(a) for v in range(b)]
  baseline=sum(all(R(x[u],x[v]) for u,v in core) for x in itertools.product(range(5),repeat=c))
  for k in (5,6,10,11):
   n,E=lift(c,core,k);src=encode(n,E);n,E=parse(src);g=recognize(n,E)
   check(g is not None and g['k']==k and g['core']==set(core))
   w=fast(n,E,g);check((w is not None)==(k%5==0))
   value=brute(n,E);check(value==(baseline if k%5==0 else 0))
   for i in range(2):
    p=list(range(n));rand.shuffle(p);e=[(p[u],p[v]) for u,v in E];gr=recognize(n,parse(encode(n,e))[1]);check(gr is not None and gr['k']==k);check((fast(n,e,gr) is not None)==(k%5==0))
   records.append(dict(core=f'K{a}{b}',k=k,count=value,base=baseline,bytes=len(src)))
 n,E=lift(4,[(0,2),(0,3),(1,2),(1,3)],5)
 for corrupt in ([e for e in E if e!=(0,8)],E+[(2,0)],E+[(4,1)]):check(recognize(n,corrupt) is None)
 for source in (encode(n,E).rstrip('\n'),encode(n,E)+'a 0 1\n',encode(n,E).replace('v 1\n','v 02\n')):
  try:parse(source)
  except ValueError:check(True)
  else:check(False)
 return dict(revision='tmr2-t5-connected-gauge072-compact.v1',seed=SEED,cases=records,checks=checks,failures=0,status='finite COMPUTATIONAL controls, not asymptotic theorem')
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
