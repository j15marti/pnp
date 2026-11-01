#!/usr/bin/env python3
"""GATE304 compact independent source-incidence certificate checker.
Standard library only. Symbolic inequality holds for every valid canonical source;
finite enumeration below is a falsification control, not an all-input proof."""
import itertools
from collections import Counter,defaultdict
S={
"Y6":("123 145 246 356","124 136 235 456"),
"F9":("156 238 135 469 247 789","468 167 234 358 129 579"),
"F15":("1,2,7;1,3,8;4,5,9;4,6,10;2,3,5;6,11,12;7,11,13;8,12,14;9,13,15;10,14,15","1,2,11;2,3,11;1,3,12;4,5,13;5,6,14;4,6,15;7,8,12;8,9,13;9,10,14;10,7,15")}
def source(name):
 p,q=S[name]
 if name=="F15": f=lambda a:[tuple(int(x) for x in c.split(",")) for c in a.split(";")]
 else: f=lambda a:[tuple(int(x) for x in c) for c in a.split()]
 return f(p)+[tuple(-v for v in c) for c in f(q)]
def valid(F):
 if not F or any(len(c)!=3 or len(set(map(abs,c)))!=3 or len(set(v>0 for v in c))!=1 for c in F):return False
 if len({tuple(sorted(c)) for c in F})!=len(F):return False
 n=max(abs(v) for c in F for v in c);o=Counter((abs(x),x>0) for c in F for x in c)
 return set(abs(v) for c in F for v in c)==set(range(1,n+1)) and all(o[x,s]==2 for x in range(1,n+1) for s in (0,1))
def check(F,p):
 n=max(abs(v) for c in F for v in c); t=len(p);a=sum(p.values());b=t-a
 cover=[0,0];free_covered=defaultdict(lambda:[0,0]);edges=[];u=0
 for j,c in enumerate(F):
  if any(abs(v) in p and p[abs(v)]==int(v>0) for v in c):
   cover[int(c[0]>0)]+=1
   for v in c:
    if abs(v) not in p:free_covered[abs(v)][int(v>0)]+=1
  else:
   u+=1;v=[abs(x) for x in c if abs(x) not in p]
   if len(v)==2:edges.append((j,v[0],v[1]))
 triangles=[]
 for e in itertools.combinations(edges,3):
  deg=Counter(v for _,x,y in e for v in (x,y))
  if len(deg)==3 and all(v==2 for v in deg.values()):triangles.append(tuple(sorted(x[0] for x in e)))
 used=set();nu=0
 for tri in sorted(set(triangles)):
  if used.isdisjoint(tri):nu+=1;used.update(tri)
 eta=sum(min(v) for v in free_covered.values())
 cminus,cplus=cover
 delta=2*(n-t)-u-eta-nu
 floor_old=2*n//3-2*t-2*t//3
 d=abs(cplus-cminus)
 dmin=max(0,(2*a+2)//3-2*b,(2*b+2)//3-2*a)
 assert delta>=floor_old+d>=floor_old+dmin
 assert cplus<=(2*a) and cminus<=(2*b)
 assert eta<=2*min(cplus,cminus) and 3*nu<=len(edges)<=2*t
 if not (a and b): assert eta==0
 if t==1:assert delta==2*n//3
 return delta,d,dmin
for name in S:
 F=source(name);assert valid(F);n=max(abs(v) for c in F for v in c)
 windows=[range(1,n+1)] if n!=15 else [range(1,7),range(10,16)]
 tested=positive=strong=0
 for v in windows:
  for z in itertools.product((0,1,2),repeat=len(v)):
   p={i:b for i,b in zip(v,z) if b!=2}
   delta,d,dmin=check(F,p);tested+=1;positive+=d>0;strong+=d>=2
 print(name,"tested",tested,"observed-cover-gain-positive",positive,"gain-at-least-2",strong)
assert check(source("F15"),{1:1,2:1,3:1,4:1})[0]>=3
print("PASS: proof is combinatorial, tests are finite; P versus NP OPEN")
