#!/usr/bin/env python3
"""LSPV-3 GATE327: source dominance versus exact continuation (OFFLINE finite census)."""
import collections,json
Z=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6))
F=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
def good(f,n):
 if n%3 or len(f)*3!=4*n:return False
 seen=set();h=collections.Counter()
 for c in f:
  if len(c)!=3 or len({abs(x) for x in c})!=3 or not(all(x>0 for x in c) or all(x<0 for x in c)) or any(not 1<=abs(x)<=n for x in c):return False
  t=tuple(sorted(c))
  if t in seen:return False
  seen.add(t)
  for v in c:h[abs(v),v>0]+=1
 return all(h[i,s]==2 for i in range(1,n+1) for s in (False,True))
def sat(f,a):return all(any(((a>>(abs(x)-1))&1)==int(x>0) for x in c) for c in f)
def run(f,n):
 assert good(f,n)
 truth=[sat(f,a) for a in range(1<<n)]
 count=collections.Counter()
 for S in range(1<<n):
  pv=[i for i in range(n) if S>>i&1];fv=[i for i in range(n) if not S>>i&1]
  g=[]
  for z in range(1<<len(pv)):
   a=sum((1<<i) for k,i in enumerate(pv) if z>>k&1)
   co=0
   for u in range(1<<len(fv)):
    q=a|sum((1<<i) for k,i in enumerate(fv) if u>>k&1)
    if truth[q]:co|=1<<u
   b=0;dead=False
   for j,c in enumerate(f):
    if any((S>>(abs(x)-1)&1) and ((a>>(abs(x)-1)&1)==int(x>0)) for x in c):b|=1<<j
    elif all(S>>(abs(x)-1)&1 for x in c):dead=True
   g.append((co,b,dead,co.bit_count()))
  for p in g:
   for q in g:
    co,bb,d,pc=p;qo,qb,qd,qc=q
    srcdom=d or (not qd and (bb&~qb)==0)
    srcsame=d==qd and (d or bb==qb)
    dom=(co&~qo)==0;same=co==qo
    assert not srcdom or dom
    assert not srcsame or same
    assert pc!=qc or (not dom or same)
    count['pairs']+=1
    count['semantic_dom']+=dom;count['source_dom']+=srcdom
    count['semantic_equal']+=same;count['source_equal']+=srcsame
    count['missed_dom']+=dom and not srcdom
    count['equalcount_diff']+=(pc==qc and not same)
 return {'models':sum(truth),**count}
assert not good(Z+(Z[0],),6) and not good(Z[:-1],6)
z=run(Z,6);f=run(F,9)
assert (z['pairs'],z['missed_dom'],z['equalcount_diff'])==(15625,1646,1164)
assert (f['pairs'],f['missed_dom'],f['equalcount_diff'])==(1953125,200390,66800)
print(json.dumps({'Z6':z,'F9':f,'status':'COMPUTATIONAL census; PROVED elementary lemma; P vs NP OPEN'},indent=2))
