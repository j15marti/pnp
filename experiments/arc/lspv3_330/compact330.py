#!/usr/bin/env python3
"""LSPV-3 GATE330 independent compact reproducibility, source-bound tests only."""
from itertools import product
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
P6=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
Z6=P6+tuple(tuple(-u for u in c) for c in P6)
def valid(F,n):
 if len(F)*3!=4*n or n%3:return False
 cnt={(i,s):0 for i in range(1,n+1) for s in (0,1)};seen=set()
 for c in F:
  if len(c)!=3 or len(set(map(abs,c)))!=3 or not(all(x>0 for x in c) or all(x<0 for x in c)):return False
  key=tuple(sorted(c))
  if key in seen:return False
  seen.add(key)
  for v in c:
   if not isinstance(v,int) or not 1<=abs(v)<=n:return False
   cnt[abs(v),int(v>0)]+=1
 return all(c==2 for c in cnt.values())
def good(F,env):
 return all(any(env[abs(v)]==int(v>0) for v in c) for c in F)
def enumerate_pins(F,n,p):
 free=[v for v in range(1,n+1) if v not in p]
 for row in product((0,1),repeat=len(free)):
  env=dict(p);env.update(zip(free,row))
  if good(F,env):yield env
def counts(F,n,x,p):
 rest=[v for v in range(1,n+1) if v!=x and v not in p]
 seen=[]
 for b in (0,1):
  a={tuple(e[v] for v in rest) for e in enumerate_pins(F,n,{**p,x:b})}
  seen.append(a)
 return (len(seen[0]),len(seen[1]),len(seen[0]&seen[1]))
def implication(F,n,x,p,b):
 assert valid(F,n) and x not in p
 # test x=b implies x=1-b by falsifying each opposite branch source tail.
 targets=[c for c in F if (x if b else -x) in c]
 assert len(targets)==2
 tests=0
 for c in targets:
  pins=dict(p);pins[x]=b
  for v in c:
   if abs(v)==x:continue
   bit=int(v<0)
   if abs(v) in pins and pins[abs(v)]!=bit:break
   pins[abs(v)]=bit
  else:
   tests+=1
   if next(enumerate_pins(F,n,pins),None) is not None:return False,tests
 return True,tests
for F,n in ((F9,9),(Z6,6)):
 assert valid(F,n)
 print('original',n,'models',sum(1 for _ in enumerate_pins(F,n,{})))
 for x,p in ((1,{7:0,9:0}) if n==9 else (1,{6:0}),):
  a,b,i=counts(F,n,x,p)
  d0,k0=implication(F,n,x,p,0);d1,k1=implication(F,n,x,p,1)
  assert d0==(a==i) and d1==(b==i)
  print('pivot',x,'common pins',p,'counts',(a,b,i),'implications',(d0,d1),'paid calls',k0+k1)
print('PROVED restricted theorem; finite controls PASS; P versus NP OPEN')
